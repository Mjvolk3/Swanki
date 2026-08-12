"""Tests for the LLM usage ledger and the run_agent seam.

No network: the agent and the safety wrapper are stubbed, so these exercise
tier resolution, row shape, thread-safety and merge-on-write -- not any model.
"""

import json
import threading
from types import SimpleNamespace

import pytest

from swanki.pipeline import run_agent as ra
from swanki.pipeline.usage_ledger import (
    UsageLedger,
    UsageRow,
    row_from_usage,
    write_usage,
)


def _usage(inp=0, out=0, reasoning=0, cache=0, requests=1, tool_calls=0):
    details = {"reasoning_tokens": reasoning} if reasoning else {}
    return SimpleNamespace(
        input_tokens=inp,
        output_tokens=out,
        cache_read_tokens=cache,
        requests=requests,
        tool_calls=tool_calls,
        details=details,
    )


class TestRowFromUsage:
    def test_reasoning_nests_under_output_not_beside_it(self):
        """Responses output_tokens already includes reasoning; siblings double-count."""
        row = row_from_usage(
            _usage(inp=100, out=80, reasoning=60),
            label="l",
            tier="generation",
            model="m",
        )
        assert row.output_tokens == 80
        assert row.output_detail == {"reasoning_tokens": 60}
        assert row.output_detail["reasoning_tokens"] <= row.output_tokens

    def test_missing_reasoning_leaves_detail_empty(self):
        row = row_from_usage(
            _usage(inp=10, out=5), label="l", tier="utility", model="m"
        )
        assert row.output_detail == {}

    def test_none_usage_yields_a_zeroed_row_not_a_crash(self):
        row = row_from_usage(None, label="l", tier="generation", model="m")
        assert (row.input_tokens, row.output_tokens, row.label) == (0, 0, "l")

    def test_absent_attributes_are_tolerated(self):
        """A non-OpenAI provider supplies neither reasoning nor cache fields."""
        row = row_from_usage(
            SimpleNamespace(input_tokens=7), label="l", tier="generation", model="m"
        )
        assert row.input_tokens == 7 and row.output_tokens == 0


class TestSummary:
    def test_rollups_split_by_tier_and_label(self):
        led = UsageLedger()
        led.record(
            UsageRow(
                "card transcript",
                "utility",
                "cheap",
                100,
                0,
                50,
                {"reasoning_tokens": 10},
            )
        )
        led.record(UsageRow("card transcript", "utility", "cheap", 100, 0, 50, {}))
        led.record(
            UsageRow(
                "regular cards",
                "generation",
                "strong",
                900,
                0,
                400,
                {"reasoning_tokens": 300},
            )
        )
        s = led.summary()
        assert s["totals"]["calls"] == 3
        assert s["by_tier"]["utility"]["calls"] == 2
        assert s["by_tier"]["generation"]["input_tokens"] == 900
        assert s["by_label"]["card transcript"]["output_tokens"] == 100
        assert s["by_tier"]["utility"]["reasoning_tokens"] == 10


class TestThreadSafety:
    def test_concurrent_record_preserves_every_row(self):
        """Four 8-thread pools exist in the pipeline; a lost row is a silent undercount."""
        led = UsageLedger()

        def work():
            for _ in range(50):
                led.record(UsageRow("l", "generation", "m", 1, 0, 1, {}))

        threads = [threading.Thread(target=work) for _ in range(16)]
        [t.start() for t in threads]
        [t.join() for t in threads]
        assert len(led.rows()) == 16 * 50
        assert led.summary()["totals"]["input_tokens"] == 800


class TestWriteUsage:
    def test_writes_payload_and_leaves_no_temp_file(self, tmp_path):
        led = UsageLedger()
        led.record(UsageRow("l", "generation", "m", 5, 0, 3, {}))
        out = tmp_path / "llm-usage.json"
        write_usage(out, led)
        payload = json.loads(out.read_text())
        assert payload["totals"]["calls"] == 1
        assert not list(tmp_path.glob("*.tmp"))

    def test_second_write_merges_rather_than_truncates(self, tmp_path):
        """An audio_only rerun must add to the run record, not erase it."""
        out = tmp_path / "llm-usage.json"
        first = UsageLedger()
        first.record(UsageRow("gen", "generation", "m", 10, 0, 5, {}))
        write_usage(out, first)

        second = UsageLedger()
        second.record(UsageRow("audio", "generation", "m", 20, 0, 7, {}))
        payload = write_usage(out, second)

        assert payload["totals"]["calls"] == 2
        assert payload["totals"]["input_tokens"] == 30
        assert set(payload["by_label"]) == {"gen", "audio"}


class TestTierResolution:
    def test_generation_reads_models_llm_unchanged(self):
        models = {"llm": {"provider": "openai-responses", "model": "gpt-5.6-sol"}}
        assert (
            ra.resolve_tier_models(models)["generation"]
            == "openai-responses:gpt-5.6-sol"
        )

    def test_utility_falls_back_to_generation_when_unconfigured(self):
        """Keeps a pre-split config behaving identically."""
        models = {"llm": {"provider": "openai-responses", "model": "gpt-5.6-sol"}}
        tiers = ra.resolve_tier_models(models)
        assert tiers["utility"] == tiers["generation"]

    def test_utility_inherits_provider_so_both_tiers_stay_on_responses(self):
        """Reasoning models refuse function tools on chat/completions; never split providers."""
        models = {
            "llm": {
                "provider": "openai-responses",
                "model": "gpt-5.6-sol",
                "utility": {"model": "gpt-5.4-mini"},
            }
        }
        assert (
            ra.resolve_tier_models(models)["utility"] == "openai-responses:gpt-5.4-mini"
        )

    def test_unknown_tier_raises_rather_than_defaulting(self):
        """pydantic-ai accepts unknown model names silently; a typo must fail here."""
        with pytest.raises(ValueError, match="unknown model tier"):
            ra.validate_tier("utilty")


class TestRunAgent:
    def test_records_usage_and_returns_the_result(self, monkeypatch):
        led = UsageLedger()
        result = SimpleNamespace(
            output="hi", usage=lambda: _usage(inp=11, out=4, reasoning=2)
        )
        monkeypatch.setattr(ra, "with_safety_retry", lambda *a, **k: result)
        got = ra.run_agent(
            object(),
            "msg",
            model="m",
            label="card transcript",
            tier=ra.UTILITY,
            ledger=led,
        )
        assert got is result
        (row,) = led.rows()
        assert (row.tier, row.label, row.input_tokens) == (
            "utility",
            "card transcript",
            11,
        )
        assert row.output_detail == {"reasoning_tokens": 2}

    def test_rejects_a_bad_tier_before_calling_the_model(self, monkeypatch):
        monkeypatch.setattr(
            ra, "with_safety_retry", lambda *a, **k: pytest.fail("model was called")
        )
        with pytest.raises(ValueError):
            ra.run_agent(object(), "msg", model="m", label="l", tier="nope")

    def test_forwards_settings_through_to_the_safety_wrapper(self, monkeypatch):
        seen = {}

        def fake(agent, msg, **kw):
            seen.update(kw)
            return SimpleNamespace(output="x", usage=lambda: _usage())

        monkeypatch.setattr(ra, "with_safety_retry", fake)
        ra.run_agent(
            object(),
            "msg",
            model="openai-responses:m",
            label="l",
            instructions="sys",
            model_settings={"max_tokens": 8000},
            ledger=UsageLedger(),
        )
        assert seen["model"] == "openai-responses:m"
        assert seen["model_settings"] == {"max_tokens": 8000}
        assert seen["instructions"] == "sys"
