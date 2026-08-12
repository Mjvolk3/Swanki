"""
swanki/pipeline/run_agent.py
[[swanki.pipeline.run_agent]]
https://github.com/Mjvolk3/Swanki/tree/main/swanki/pipeline/run_agent.py
Test file: tests/test_usage_ledger.py

The single seam every LLM call passes through.

Swanki had no choke point: the model string was resolved at ~20 places and 14
call sites bypassed even the safety wrapper by calling ``agent.run_sync``
directly. Routing calls to different model tiers and accounting for their
tokens are therefore the same problem -- one missing seam -- so this module is
both.

``run_agent`` delegates to :func:`swanki.llm.safety.with_safety_retry` (so
migrated bare-``run_sync`` sites gain biosec-refusal handling as a side effect),
then records the call's token usage into the run ledger. It returns the agent's
full ``RunResult``, matching ``with_safety_retry`` so callers keep using
``.output``.

Tiers name intent, not a model: ``generation`` for work that invents content or
judges whether content is right, ``utility`` for mechanical transformation. What
each resolves to is config.
"""

import logging
from typing import Any

from pydantic_ai import Agent

from ..llm.agents import get_model_string
from ..llm.safety import with_safety_retry
from .usage_ledger import LEDGER, UsageLedger, UsageRow, row_from_usage

logger = logging.getLogger(__name__)

GENERATION = "generation"
UTILITY = "utility"
TIERS = (GENERATION, UTILITY)

_TIER_MODELS: dict[str, str] = {}
"""Resolved model per tier, registered once at pipeline start.

Populated by :func:`configure_tiers`. Empty until then, in which case every
call falls back to the model string its caller passed -- so an unconfigured run
(a script, a test, a partial rerun) behaves exactly as it did before tiering.
Written once during setup and read-only afterwards, so the thread pools on this
path need no lock.
"""


def configure_tiers(models_config: dict[str, Any]) -> dict[str, str]:
    """Register the tier models for this run and log what each resolved to.

    Logging the resolution once at startup is the guard against a silent
    mis-tier: pydantic-ai accepts an unknown model name and falls back to a
    generic profile, so a typo would otherwise run happily on the wrong model.

    Args:
        models_config: The inner ``models`` mapping.

    Returns:
        The registered tier-to-model mapping.
    """
    _TIER_MODELS.clear()
    _TIER_MODELS.update(resolve_tier_models(models_config))
    for tier, model in _TIER_MODELS.items():
        logger.info(f"llm tier {tier}: {model}")
    return dict(_TIER_MODELS)


def resolve_tier_models(models_config: dict[str, Any]) -> dict[str, str]:
    """Resolve both tiers to pydantic-ai model strings.

    ``models.llm`` stays the generation tier so the three gate configs, whose
    ``model: null`` means "reuse ``models.llm``", keep resolving to the strong
    model with no change. The utility tier reads ``models.llm.utility`` and
    falls back to the generation model when unset, which keeps behaviour
    identical on a config that predates this split.

    Args:
        models_config: The inner ``models`` mapping (already unwrapped from the
            doubled Hydra key), expected to hold an ``llm`` block.

    Returns:
        Mapping of tier name to model string.
    """
    llm_config = models_config.get("llm", {}) or {}
    generation = get_model_string(llm_config)
    utility_cfg = llm_config.get("utility") or {}
    if utility_cfg:
        utility = get_model_string(
            {
                "provider": utility_cfg.get(
                    "provider", llm_config.get("provider", "openai")
                ),
                "model": utility_cfg.get("model", llm_config.get("model", "gpt-4")),
            }
        )
    else:
        utility = generation
        logger.debug("no models.llm.utility configured; utility tier reuses generation")
    return {GENERATION: generation, UTILITY: utility}


def validate_tier(tier: str) -> str:
    """Return ``tier`` if known, else raise.

    A mistyped tier must fail loudly here. pydantic-ai does not validate model
    names -- an unknown one falls back to a generic profile and runs, producing
    plausible output from the wrong model, so a silent default would be worse
    than a crash.

    Raises:
        ValueError: If ``tier`` is not one of :data:`TIERS`.
    """
    if tier not in TIERS:
        raise ValueError(f"unknown model tier {tier!r}; expected one of {TIERS}")
    return tier


def run_agent(
    agent: Agent[Any, Any],
    user_message: Any,
    *,
    model: str,
    label: str,
    tier: str = GENERATION,
    instructions: str | None = None,
    model_settings: dict[str, Any] | None = None,
    max_safety_retries: int = 2,
    ledger: UsageLedger | None = None,
) -> Any:
    """Run one agent call with safety retry and token accounting.

    Args:
        agent: A pydantic-ai ``Agent``.
        user_message: ``str``, or ``list`` for multimodal calls.
        model: Resolved pydantic-ai model string for this call.
        label: Call-site identifier; drives the by-label rollup, so it should
            name the work ("card transcript", "regular cards") rather than the
            module.
        tier: Which tier this call site belongs to. Recorded, and validated.
        instructions: Optional system prompt.
        model_settings: Optional dict forwarded to the agent.
        max_safety_retries: Preamble-prepended retries on a safety refusal.
        ledger: Ledger to record into; defaults to the process-wide one.

    Returns:
        The agent's full ``RunResult``; callers use ``.output``.
    """
    validate_tier(tier)
    # The registered tier model wins; the caller's string is the fallback for
    # runs that never called configure_tiers.
    effective_model = _TIER_MODELS.get(tier) or model
    result = with_safety_retry(
        agent,
        user_message,
        instructions=instructions,
        model=effective_model,
        model_settings=model_settings,
        max_safety_retries=max_safety_retries,
        label=label,
    )
    record_result(result, label=label, tier=tier, model=effective_model, ledger=ledger)
    return result


def record_result(
    result: Any,
    *,
    label: str,
    tier: str,
    model: str,
    failed_attempts: int = 0,
    ledger: UsageLedger | None = None,
) -> UsageRow:
    """Record a completed run's usage into the ledger.

    Split out from :func:`run_agent` so call sites inside a thread pool can
    build their row on the worker and fold it in on the collecting thread.

    Args:
        result: A pydantic-ai ``RunResult``, or None.
        label: Call-site identifier.
        tier: Tier that served the call.
        model: Resolved model string.
        failed_attempts: Retried attempts whose tokens are unrecoverable.
        ledger: Ledger to record into; defaults to the process-wide one.

    Returns:
        The row appended.
    """
    usage = result.usage() if result is not None and hasattr(result, "usage") else None
    row = row_from_usage(
        usage, label=label, tier=tier, model=model, failed_attempts=failed_attempts
    )
    (ledger if ledger is not None else LEDGER).record(row)
    return row
