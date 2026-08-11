"""Tests for the image-leak gate.

The judge and rewrite calls are stubbed, so these exercise the gate's control
flow -- clean pass-through, repair loop, attempt budget, fail-open paths -- not
the model's judgement.
"""

from pathlib import Path

import pytest

from swanki.models.cards import CardContent, ImageLeakVerdict, PlainCard
from swanki.pipeline import image_leak_gate as gate


def _card(
    front="What does the figure show?",
    back="It shows X.",
    img="images/a.jpg",
    desc="A chart with two axes.",
):
    c = PlainCard(
        front=CardContent(text=front),
        back=CardContent(text=back),
        tags=["t"],
        difficulty="easy",
    )
    c.front.image_path = img
    c.front.image_summary_perceptual = desc
    return c


def _verdict(leaks, severity="severe", what="the mechanism"):
    return ImageLeakVerdict(
        leaks=leaks,
        severity=severity if leaks else "none",
        what_leaks=what if leaks else "",
        reasoning="because",
    )


@pytest.fixture
def stub_image(monkeypatch):
    monkeypatch.setattr(gate, "_resolve_image", lambda card, base: object())


class TestCleanPath:
    def test_clean_card_is_untouched(self, monkeypatch, stub_image):
        monkeypatch.setattr(gate, "_judge", lambda c, s, m: _verdict(False))
        card = _card()
        cards, audit = gate.run_image_leak_gate([card], "m", Path("/tmp"))
        assert [a.verdict for a in audit] == ["clean"]
        assert card.front.image_summary_perceptual == "A chart with two axes."
        assert audit[0].attempts == 0

    def test_cards_without_front_image_are_skipped(self, monkeypatch):
        monkeypatch.setattr(gate, "_judge", lambda c, s, m: pytest.fail("judged"))
        plain = PlainCard(
            front=CardContent(text="q"),
            back=CardContent(text="a"),
            tags=["t"],
            difficulty="easy",
        )
        cards, audit = gate.run_image_leak_gate([plain], "m", Path("/tmp"))
        assert audit == []
        assert cards == [plain]


class TestRepairLoop:
    def test_leaky_card_is_rewritten_and_accepted(self, monkeypatch, stub_image):
        seen = {"n": 0}

        def judge(card, spoken, model):
            seen["n"] += 1
            return _verdict(seen["n"] == 1)  # leaks first, clean after rewrite

        monkeypatch.setattr(gate, "_judge", judge)
        monkeypatch.setattr(gate, "_rewrite", lambda c, i, m, p: "Two labelled boxes.")
        card = _card()
        _, audit = gate.run_image_leak_gate([card], "m", Path("/tmp"))
        assert audit[0].verdict == "rewritten"
        assert audit[0].attempts == 1
        assert card.front.image_summary_perceptual == "Two labelled boxes."
        assert audit[0].original_description == "A chart with two axes."

    def test_budget_exhausted_keeps_best_attempt_as_unresolved(
        self, monkeypatch, stub_image
    ):
        monkeypatch.setattr(gate, "_judge", lambda c, s, m: _verdict(True))
        monkeypatch.setattr(gate, "_rewrite", lambda c, i, m, p: "still leaky")
        card = _card()
        _, audit = gate.run_image_leak_gate([card], "m", Path("/tmp"), max_attempts=2)
        assert audit[0].verdict == "unresolved"
        assert audit[0].attempts == 2
        # best answer-blind attempt is kept over the judge-rejected original
        assert card.front.image_summary_perceptual == "still leaky"

    def test_rewrite_is_told_what_leaked(self, monkeypatch, stub_image):
        got = {}

        def rewrite(card, image, model, previous):
            got["previous"] = previous
            return "redone"

        monkeypatch.setattr(
            gate, "_judge", lambda c, s, m: _verdict(True, what="the ratio")
        )
        monkeypatch.setattr(gate, "_rewrite", rewrite)
        gate.run_image_leak_gate([_card()], "m", Path("/tmp"), max_attempts=1)
        assert got["previous"] == "the ratio"


class TestFailOpen:
    def test_judge_failure_keeps_card_and_records_it(self, monkeypatch, stub_image):
        def boom(card, spoken, model):
            raise RuntimeError("judge down")

        monkeypatch.setattr(gate, "_judge", boom)
        card = _card()
        _, audit = gate.run_image_leak_gate([card], "m", Path("/tmp"))
        assert audit[0].verdict == "judge_failed"
        assert card.front.image_summary_perceptual == "A chart with two axes."

    def test_missing_image_cannot_be_rewritten(self, monkeypatch):
        monkeypatch.setattr(gate, "_judge", lambda c, s, m: _verdict(True))
        monkeypatch.setattr(gate, "_resolve_image", lambda card, base: None)
        _, audit = gate.run_image_leak_gate([_card()], "m", Path("/tmp"))
        assert audit[0].verdict == "unresolved"
        assert audit[0].attempts == 0

    def test_rewrite_failure_falls_back_to_unresolved(self, monkeypatch, stub_image):
        def boom(card, image, model, previous):
            raise RuntimeError("vision down")

        monkeypatch.setattr(gate, "_judge", lambda c, s, m: _verdict(True))
        monkeypatch.setattr(gate, "_rewrite", boom)
        _, audit = gate.run_image_leak_gate([_card()], "m", Path("/tmp"))
        assert audit[0].verdict == "unresolved"


class TestFallbackDescription:
    def test_interpretive_summary_is_assessed_when_perceptual_absent(
        self, monkeypatch, stub_image
    ):
        seen = {}

        def judge(card, spoken, model):
            seen["spoken"] = spoken
            return _verdict(False)

        monkeypatch.setattr(gate, "_judge", judge)
        card = _card(desc=None)
        card.front.image_summary_perceptual = None
        card.front.image_summary = "old interpretive text"
        gate.run_image_leak_gate([card], "m", Path("/tmp"))
        assert seen["spoken"] == "old interpretive text"


class TestAudit:
    def test_audit_round_trips_to_json(self, monkeypatch, stub_image, tmp_path):
        monkeypatch.setattr(gate, "_judge", lambda c, s, m: _verdict(False))
        _, audit = gate.run_image_leak_gate([_card()], "m", Path("/tmp"))
        out = tmp_path / "image-leak-assessment.json"
        gate.write_audit(audit, out)
        import json

        rows = json.loads(out.read_text())
        assert rows[0]["verdict"] == "clean"
        assert "original_description" in rows[0]


class TestSpokenLengthCap:
    """The front description is read aloud before answering, so it is bounded."""

    def test_perceptual_at_the_cap_is_accepted(self):
        from swanki.models.document import PERCEPTUAL_MAX_CHARS, ImageDescription

        d = ImageDescription(perceptual="x" * PERCEPTUAL_MAX_CHARS, interpretive="ok")
        assert len(d.perceptual) == PERCEPTUAL_MAX_CHARS

    def test_over_cap_is_rejected_so_the_agent_retries(self):
        import pydantic

        from swanki.models.document import PERCEPTUAL_MAX_CHARS, ImageDescription

        with pytest.raises(pydantic.ValidationError):
            ImageDescription(
                perceptual="x" * (PERCEPTUAL_MAX_CHARS + 1), interpretive="ok"
            )

    def test_interpretive_is_not_capped(self):
        """Only the front is read before answering; the back may be as long as needed."""
        from swanki.models.document import PERCEPTUAL_MAX_CHARS, ImageDescription

        d = ImageDescription(
            perceptual="short", interpretive="y" * (PERCEPTUAL_MAX_CHARS * 3)
        )
        assert len(d.interpretive) == PERCEPTUAL_MAX_CHARS * 3

    def test_gate_rewrite_prompt_states_the_shared_cap(self):
        from swanki.models.document import PERCEPTUAL_MAX_WORDS
        from swanki.pipeline.image_leak_gate import REWRITE_PROMPT

        rendered = REWRITE_PROMPT.format(
            question="q", extra="", max_words=PERCEPTUAL_MAX_WORDS
        )
        assert f"under {PERCEPTUAL_MAX_WORDS} words" in rendered
