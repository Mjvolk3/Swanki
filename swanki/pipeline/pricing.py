"""
swanki/pipeline/pricing.py
[[swanki.pipeline.pricing]]
https://github.com/Mjvolk3/Swanki/tree/main/swanki/pipeline/pricing.py
Test file: tests/test_usage_ledger.py

Token prices, so a run's accounting can report dollars and not just counts.

Prices live in one table with a stated source and fetch date, because a price
buried in code with no provenance rots silently and then reports confident wrong
numbers. When a model is absent from the table its cost is reported as ``None``
rather than guessed -- an unpriced call must be visibly unpriced.

Source: https://developers.openai.com/api/docs/pricing, fetched 2026-08-11.
USD per 1M tokens, standard (non-batch, non-flex) tier.
"""

import logging
from typing import Any, NamedTuple

logger = logging.getLogger(__name__)


class Price(NamedTuple):
    """USD per 1M tokens for one model."""

    input: float
    cached_input: float
    output: float


# Longest prefix wins, so a specific variant is matched before its family.
PRICES: dict[str, Price] = {
    "gpt-5.6-sol": Price(5.00, 0.50, 30.00),
    "gpt-5.6-terra": Price(2.00, 0.20, 12.00),
    "gpt-5.6-luna": Price(0.20, 0.02, 1.20),
    "gpt-5.5": Price(5.00, 0.50, 30.00),
    "gpt-5.4-mini": Price(0.75, 0.075, 4.50),
    "gpt-5.4-nano": Price(0.20, 0.02, 1.25),
}


def price_for(model: str) -> Price | None:
    """Look up a model's price by longest matching prefix.

    Args:
        model: A pydantic-ai model string (``"openai-responses:gpt-5.6-sol"``)
            or a bare model name.

    Returns:
        The price, or None when the model is not in the table.
    """
    name = model.split(":", 1)[-1]
    matches = [p for p in PRICES if name.startswith(p)]
    if not matches:
        return None
    return PRICES[max(matches, key=len)]


def cost_usd(
    model: str, input_tokens: int, cached_input_tokens: int, output_tokens: int
) -> float | None:
    """Cost of one call in USD, or None when the model is unpriced.

    ``input_tokens`` is the provider's total and already includes anything
    served from cache, so the cached portion is billed at the cached rate and
    only the remainder at the full input rate. ``output_tokens`` already
    includes reasoning tokens, which is why reasoning is not billed separately.

    Args:
        model: Model string.
        input_tokens: Total input tokens, cached portion included.
        cached_input_tokens: Portion of the input served from cache.
        output_tokens: Output tokens, reasoning included.

    Returns:
        Cost in USD, or None if the model has no price entry.
    """
    p = price_for(model)
    if p is None:
        return None
    fresh = max(input_tokens - cached_input_tokens, 0)
    return (
        fresh * p.input
        + cached_input_tokens * p.cached_input
        + output_tokens * p.output
    ) / 1_000_000


def merge_overrides(overrides: dict[str, Any] | None) -> None:
    """Fold config-supplied prices into the table.

    Lets a run correct a stale price without a code change; keys are model-name
    prefixes and values are ``{input, cached_input, output}`` in USD per 1M.

    Args:
        overrides: Mapping of model prefix to a price mapping, or None.
    """
    if not overrides:
        return
    for name, vals in overrides.items():
        PRICES[name] = Price(
            float(vals["input"]), float(vals["cached_input"]), float(vals["output"])
        )
        logger.info(f"pricing override: {name} -> {PRICES[name]}")
