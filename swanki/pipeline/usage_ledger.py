"""
swanki/pipeline/usage_ledger.py
[[swanki.pipeline.usage_ledger]]
https://github.com/Mjvolk3/Swanki/tree/main/swanki/pipeline/usage_ledger.py
Test file: tests/test_usage_ledger.py

Per-run token accounting for LLM calls.

Swanki logged no token usage anywhere, so the cost of a run could only ever be
reconstructed after the fact from job logs and guesswork. This ledger records
one row per LLM call -- label, tier, model, tokens -- and writes them to
``llm-usage.json`` so a run's spend is inspectable from its own output
directory.

It reports tokens and counts only. Deliberately no pricing constants: prices
change out of band and a stale table in the repo is worse than no table, since
it produces confident wrong numbers.
"""

import json
import logging
import os
import threading
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from .pricing import cost_usd

logger = logging.getLogger(__name__)


@dataclass
class UsageRow:
    """One LLM call's token usage.

    ``reasoning_tokens`` is nested under ``output_detail`` rather than sitting
    beside ``output_tokens`` because the Responses API already counts reasoning
    inside ``output_tokens`` -- recording them as siblings double-counts.
    Likewise ``input_tokens`` already includes anything served from cache, so
    ``cache_read_tokens`` is a breakdown of it, not an addition to it.
    """

    label: str
    tier: str
    model: str
    input_tokens: int = 0
    cache_read_tokens: int = 0
    output_tokens: int = 0
    output_detail: dict[str, int] = field(default_factory=dict)
    requests: int = 0
    tool_calls: int = 0
    failed_attempts: int = 0
    cost_usd: float | None = None


def row_from_usage(
    usage: Any, *, label: str, tier: str, model: str, failed_attempts: int = 0
) -> UsageRow:
    """Build a :class:`UsageRow` from a pydantic-ai ``RunUsage``.

    Every field is read defensively and coerced to ``int``: pydantic-ai is
    untyped here, ``reasoning_tokens`` is not a first-class attribute (it
    arrives inside the provider-specific ``details`` dict and only on the
    Responses path), and a non-OpenAI provider supplies neither.

    Args:
        usage: A pydantic-ai ``RunUsage``, or None.
        label: Call-site identifier, used for the by-label rollup.
        tier: Which model tier served the call.
        model: The resolved pydantic-ai model string.
        failed_attempts: Retried attempts whose tokens are not recoverable.

    Returns:
        A populated row; token fields are zero when usage is unavailable.
    """
    row = UsageRow(
        label=label or "unlabelled",
        tier=tier,
        model=model,
        failed_attempts=failed_attempts,
    )
    if usage is None:
        return row
    row.input_tokens = int(getattr(usage, "input_tokens", 0) or 0)
    row.cache_read_tokens = int(getattr(usage, "cache_read_tokens", 0) or 0)
    row.output_tokens = int(getattr(usage, "output_tokens", 0) or 0)
    row.requests = int(getattr(usage, "requests", 0) or 0)
    row.tool_calls = int(getattr(usage, "tool_calls", 0) or 0)
    details = getattr(usage, "details", None) or {}
    reasoning = int(details.get("reasoning_tokens", 0) or 0)
    if reasoning:
        row.output_detail = {"reasoning_tokens": reasoning}
    row.cost_usd = cost_usd(
        model, row.input_tokens, row.cache_read_tokens, row.output_tokens
    )
    return row


class UsageLedger:
    """Thread-safe accumulator of :class:`UsageRow`.

    Several call sites run inside ``ThreadPoolExecutor`` pools, so ``record``
    takes a lock. Callers inside a pool may instead return their rows and fold
    them in on the collecting thread; the lock makes the direct path safe
    either way.
    """

    def __init__(self) -> None:
        """Start with no rows and a fresh lock."""
        self._rows: list[UsageRow] = []
        self._lock = threading.Lock()

    def record(self, row: UsageRow) -> None:
        """Append one row."""
        with self._lock:
            self._rows.append(row)

    def extend(self, rows: list[UsageRow]) -> None:
        """Append rows collected off-thread."""
        with self._lock:
            self._rows.extend(rows)

    def rows(self) -> list[UsageRow]:
        """Return a snapshot copy of the recorded rows."""
        with self._lock:
            return list(self._rows)

    def clear(self) -> None:
        """Drop all rows (used between runs and by tests)."""
        with self._lock:
            self._rows.clear()

    def summary(self) -> dict[str, Any]:
        """Aggregate rows into per-call records plus by-tier and by-label rollups.

        The by-tier rollup is what validates or falsifies a claim like "85% of
        calls are mechanical"; the by-label rollup identifies which call site is
        worth moving next.
        """
        rows = self.rows()

        def _blank() -> dict[str, float]:
            return {
                "calls": 0,
                "input_tokens": 0,
                "cache_read_tokens": 0,
                "output_tokens": 0,
                "reasoning_tokens": 0,
                "failed_attempts": 0,
                "cost_usd": 0.0,
                "unpriced_calls": 0,
            }

        by_tier: dict[str, dict[str, float]] = {}
        by_label: dict[str, dict[str, float]] = {}
        totals = _blank()
        for r in rows:
            for bucket in (
                by_tier.setdefault(r.tier, _blank()),
                by_label.setdefault(r.label, _blank()),
                totals,
            ):
                bucket["calls"] += 1
                bucket["input_tokens"] += r.input_tokens
                bucket["cache_read_tokens"] += r.cache_read_tokens
                bucket["output_tokens"] += r.output_tokens
                bucket["reasoning_tokens"] += r.output_detail.get("reasoning_tokens", 0)
                bucket["failed_attempts"] += r.failed_attempts
                if r.cost_usd is None:
                    bucket["unpriced_calls"] += 1
                else:
                    bucket["cost_usd"] = round(bucket["cost_usd"] + r.cost_usd, 6)
        return {
            "totals": totals,
            "by_tier": by_tier,
            "by_label": by_label,
            "calls": [asdict(r) for r in rows],
        }


LEDGER = UsageLedger()
"""Process-wide ledger. One swanki run is one process, so this is run-scoped."""


def write_usage(path: Path, ledger: UsageLedger | None = None) -> dict[str, Any]:
    """Merge this process's rows into ``path`` and write it atomically.

    Merging rather than truncating means an ``audio_only`` rerun adds to the
    same run record instead of erasing what generation already reported.
    Temp-then-rename means a killed SLURM job cannot leave a half-written file
    that looks like a complete accounting.

    Args:
        path: Destination ``llm-usage.json``.
        ledger: Ledger to write; defaults to the process-wide one.

    Returns:
        The payload written.
    """
    led = ledger if ledger is not None else LEDGER
    rows = [asdict(r) for r in led.rows()]
    if path.exists():
        existing = json.loads(path.read_text(encoding="utf-8"))
        rows = list(existing.get("calls", [])) + rows

    merged = UsageLedger()
    merged.extend(
        [
            UsageRow(
                label=c.get("label", "unlabelled"),
                tier=c.get("tier", "generation"),
                model=c.get("model", ""),
                input_tokens=int(c.get("input_tokens", 0)),
                cache_read_tokens=int(c.get("cache_read_tokens", 0)),
                output_tokens=int(c.get("output_tokens", 0)),
                output_detail=dict(c.get("output_detail", {})),
                requests=int(c.get("requests", 0)),
                tool_calls=int(c.get("tool_calls", 0)),
                failed_attempts=int(c.get("failed_attempts", 0)),
                cost_usd=c.get("cost_usd"),
            )
            for c in rows
        ]
    )
    payload = merged.summary()

    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    os.replace(tmp, path)
    t = payload["totals"]
    logger.info(
        f"llm usage: {t['calls']} calls, {t['input_tokens']} in / "
        f"{t['output_tokens']} out ({t['reasoning_tokens']} reasoning), "
        f"${t['cost_usd']:.2f}"
        + (f" [{t['unpriced_calls']} unpriced]" if t["unpriced_calls"] else "")
        + f" -> {path}"
    )
    return payload
