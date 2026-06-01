"""
tests/test_card_correctness.py
[[tests.test_card_correctness]]

Unit tests for the post-generation LLM correctness gate. The agent is never
called: ``_assess_card`` is monkeypatched per-card so the gate's filtering,
fix-application, audit completeness, ordering, and fail-open behavior are
tested deterministically.
"""

from __future__ import annotations

import logging

import pytest
import yaml

from swanki.models.cards import (
    CardContent,
    CardCorrectnessAssessment,
    PlainCard,
)
from swanki.models.document import DocumentSummary
from swanki.pipeline import card_correctness
from swanki.pipeline.card_correctness import (
    _apply_assessment,
    run_correctness_gate,
    write_audit,
)


def _card(front: str, back: str = "answer", subtype: str = "regular") -> PlainCard:
    return PlainCard(
        front=CardContent(text=front),
        back=CardContent(text=back),
        tags=["microbiology"],
        card_subtype=subtype,
    )


@pytest.fixture
def summary() -> DocumentSummary:
    return DocumentSummary(
        title="Chem Basis of Microbiology",
        authors=["Alcamo"],
        main_topic="microbial chemistry",
        key_contributions=["bonding", "biomolecules"],
        methodology="textbook Q&A",
        summary=" ".join(["word"] * 120),
    )


def _verdict_by_front(mapping: dict[str, CardCorrectnessAssessment | None]):
    """Return a fake ``_assess_card`` keyed on the card's front text."""

    def fake(card, source_context, doc_summary, model_string):
        return mapping[card.front.text]

    return fake


def test_pass_keeps_card_unchanged(monkeypatch, summary):
    monkeypatch.setattr(
        card_correctness,
        "_assess_card",
        _verdict_by_front(
            {"Q": CardCorrectnessAssessment(verdict="pass", reason="correct")}
        ),
    )
    kept, audit = run_correctness_gate([_card("Q")], summary, "src", "m")
    assert len(kept) == 1
    assert kept[0].front.text == "Q"
    assert audit[0].verdict == "pass"
    assert audit[0].corrected_front is None


def test_fixed_replaces_content_and_logs_original(monkeypatch, summary):
    monkeypatch.setattr(
        card_correctness,
        "_assess_card",
        _verdict_by_front(
            {
                "bad front": CardCorrectnessAssessment(
                    verdict="fixed",
                    reason="wrong answer",
                    corrected_front="good front",
                    corrected_back="good back",
                )
            }
        ),
    )
    kept, audit = run_correctness_gate(
        [_card("bad front", "bad back")], summary, "src", "m"
    )
    assert len(kept) == 1
    assert kept[0].front.text == "good front"
    assert kept[0].back.text == "good back"
    assert audit[0].verdict == "fixed"
    assert audit[0].original_front == "bad front"
    assert audit[0].original_back == "bad back"
    assert audit[0].corrected_front == "good front"


def test_fixed_only_one_side(monkeypatch, summary):
    monkeypatch.setattr(
        card_correctness,
        "_assess_card",
        _verdict_by_front(
            {
                "keep front": CardCorrectnessAssessment(
                    verdict="fixed", reason="back wrong", corrected_back="new back"
                )
            }
        ),
    )
    kept, _ = run_correctness_gate(
        [_card("keep front", "old back")], summary, "src", "m"
    )
    assert kept[0].front.text == "keep front"
    assert kept[0].back.text == "new back"


def test_dropped_excluded_but_logged(monkeypatch, summary):
    monkeypatch.setattr(
        card_correctness,
        "_assess_card",
        _verdict_by_front(
            {
                "nonsense": CardCorrectnessAssessment(
                    verdict="dropped", reason="all options wrong"
                )
            }
        ),
    )
    kept, audit = run_correctness_gate([_card("nonsense")], summary, "src", "m")
    assert kept == []
    assert audit[0].verdict == "dropped"
    assert audit[0].original_front == "nonsense"


def test_assessment_failure_keeps_card_fail_open(monkeypatch, summary):
    monkeypatch.setattr(
        card_correctness, "_assess_card", _verdict_by_front({"Q": None})
    )
    kept, audit = run_correctness_gate([_card("Q")], summary, "src", "m")
    assert len(kept) == 1
    assert audit[0].verdict == "assessment_failed"


def test_audit_one_entry_per_card_and_order_preserved(monkeypatch, summary):
    mapping = {
        "a": CardCorrectnessAssessment(verdict="pass", reason="ok"),
        "b": CardCorrectnessAssessment(verdict="dropped", reason="bad"),
        "c": CardCorrectnessAssessment(
            verdict="fixed", reason="fix", corrected_front="C"
        ),
        "d": None,
    }
    monkeypatch.setattr(
        card_correctness, "_assess_card", _verdict_by_front(mapping)
    )
    cards = [_card("a"), _card("b"), _card("c"), _card("d")]
    kept, audit = run_correctness_gate(cards, summary, "src", "m", max_workers=4)

    assert [e.original_front for e in audit] == ["a", "b", "c", "d"]
    assert [e.verdict for e in audit] == [
        "pass",
        "dropped",
        "fixed",
        "assessment_failed",
    ]
    assert len(audit) == len(cards)
    assert [k.front.text for k in kept] == ["a", "C", "d"]
    assert len(kept) + sum(1 for e in audit if e.verdict == "dropped") == len(cards)


def test_empty_input_returns_empty(summary):
    kept, audit = run_correctness_gate([], summary, "src", "m")
    assert kept == []
    assert audit == []


def test_all_dropped_yields_empty_kept_without_error(monkeypatch, summary):
    monkeypatch.setattr(
        card_correctness,
        "_assess_card",
        _verdict_by_front(
            {
                "x": CardCorrectnessAssessment(verdict="dropped", reason="bad"),
                "y": CardCorrectnessAssessment(verdict="dropped", reason="bad"),
            }
        ),
    )
    kept, audit = run_correctness_gate(
        [_card("x"), _card("y")], summary, "src", "m"
    )
    assert kept == []
    assert len(audit) == 2


def test_apply_assessment_pure_dropped():
    kept_card, entry = _apply_assessment(
        _card("q"),
        CardCorrectnessAssessment(verdict="dropped", reason="bad"),
    )
    assert kept_card is None
    assert entry.verdict == "dropped"


def test_fixed_verdict_requires_correction():
    with pytest.raises(ValueError):
        CardCorrectnessAssessment(verdict="fixed", reason="missing correction")


def test_write_audit_atomic_with_summary(monkeypatch, summary, tmp_path):
    monkeypatch.setattr(
        card_correctness,
        "_assess_card",
        _verdict_by_front(
            {
                "p": CardCorrectnessAssessment(verdict="pass", reason="ok"),
                "d": CardCorrectnessAssessment(verdict="dropped", reason="bad"),
            }
        ),
    )
    _, audit = run_correctness_gate([_card("p"), _card("d")], summary, "src", "m")
    out = tmp_path / "correctness-assessment.yaml"
    write_audit(audit, out)

    assert out.exists()
    assert not (tmp_path / "correctness-assessment.yaml.tmp").exists()
    loaded = yaml.safe_load(out.read_text())
    assert loaded["summary"]["total"] == 2
    assert loaded["summary"]["passed"] == 1
    assert loaded["summary"]["dropped"] == 1
    assert len(loaded["cards"]) == 2


def test_dropped_reason_and_original_text_logged_for_report(
    monkeypatch, summary, tmp_path
):
    """A rejection report needs the reason AND the original card text on disk."""
    monkeypatch.setattr(
        card_correctness,
        "_assess_card",
        _verdict_by_front(
            {
                "wrong q": CardCorrectnessAssessment(
                    verdict="dropped", reason="every option is chemically wrong"
                )
            }
        ),
    )
    _, audit = run_correctness_gate(
        [_card("wrong q", "wrong a")], summary, "src", "m"
    )
    out = tmp_path / "correctness-assessment.yaml"
    write_audit(audit, out)

    loaded = yaml.safe_load(out.read_text())
    dropped = [c for c in loaded["cards"] if c["verdict"] == "dropped"]
    assert len(dropped) == 1
    assert dropped[0]["reason"] == "every option is chemically wrong"
    assert dropped[0]["original_front"] == "wrong q"
    assert dropped[0]["original_back"] == "wrong a"


def test_dropped_card_emits_warning_with_reason(monkeypatch, summary, caplog):
    monkeypatch.setattr(
        card_correctness,
        "_assess_card",
        _verdict_by_front(
            {
                "bad": CardCorrectnessAssessment(
                    verdict="dropped", reason="contradicts established chemistry"
                )
            }
        ),
    )
    with caplog.at_level(logging.WARNING, logger="swanki.pipeline.card_correctness"):
        run_correctness_gate([_card("bad")], summary, "src", "m")
    assert any(
        "DROPPED" in r.message and "contradicts established chemistry" in r.getMessage()
        for r in caplog.records
    )
