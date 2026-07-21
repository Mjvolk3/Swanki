"""
tests/test_reading_correctness.py
[[tests.test_reading_correctness]]

Unit tests for the report-only audio correctness critic. Modes 1 and 2 are
deterministic and tested with real fixtures (no LLM mock); mode 3 monkeypatches
``_assess_lecture`` -- as ``tests/test_card_correctness.py`` monkeypatches
``_assess_card`` -- so fail-open and report-only behavior is exercised without a
network call.
"""

from __future__ import annotations

import json

from swanki.audio import reading_correctness
from swanki.audio.reading_correctness import (
    diff_chunk,
    run_lecture_factual_pass,
    validate_acronym_double_emit,
    write_lecture_audit,
    write_reading_audit,
)
from swanki.models.cards import LectureFactualAssessment

# ---------------------------------------------------------------------------
# Mode 1: normalized clause diff (deterministic)
# ---------------------------------------------------------------------------

# The production splice: this clause was lifted from one page and injected into
# unrelated reading chunks (CH03). A length-ratio floor is blind to it.
_SPLICE = "MicroRNAs can be as small as 22 nucleotide residues long."


def test_spliced_clause_flagged_as_inserted():
    source = (
        "The ribosome translates messenger RNA into protein. "
        "Translation proceeds in three phases."
    )
    transcript = (
        "The ribosome translates messenger RNA into protein. "
        "Translation proceeds in three phases. " + _SPLICE
    )
    result = diff_chunk(0, source, transcript, fell_back=False)
    assert not result.not_assessed
    joined = " ".join(result.inserted)
    assert "22" in joined and "nucleotide" in joined
    assert result.dropped == []


def test_duplicated_sentence_flagged():
    source = "Alpha begins the process. Beta ends the process."
    # Beta duplicated in the transcript.
    transcript = (
        "Alpha begins the process. Beta ends the process. Beta ends the process."
    )
    result = diff_chunk(0, source, transcript, fell_back=False)
    assert any("beta ends the process" == d for d in result.duplicated)


def test_clean_chunk_has_no_findings_despite_legit_expansion():
    # Legit Pass-2 first-use acronym expansion must NOT register as drift: the
    # source's "ATP" and the transcript's "adenosine triphosphate, ATP"
    # normalize to the same sentence.
    source = "The ATP molecule stores chemical energy. It is essential."
    transcript = (
        "The adenosine triphosphate, ATP molecule stores chemical energy. "
        "It is essential."
    )
    result = diff_chunk(0, source, transcript, fell_back=False)
    assert result.inserted == []
    assert result.dropped == []
    assert result.duplicated == []


def test_fell_back_chunk_is_not_assessed_never_pass():
    # Pass-2 fallback returns input verbatim -> a trivially clean diff. It must
    # be marked not_assessed so the audit never launders it as verified-clean.
    source = "Some source prose that will be echoed back verbatim."
    result = diff_chunk(3, source, source, fell_back=True)
    assert result.not_assessed is True
    assert result.fell_back is True
    assert result.inserted == []
    assert result.dropped == []


# ---------------------------------------------------------------------------
# Mode 2: acronym double-emit validator (deterministic)
# ---------------------------------------------------------------------------


def test_letter_spelled_after_expansion_flagged():
    # The two-layer phantom name: Pass-2 first-use expansion followed by the
    # scrubber's letter-spelled acronym.
    transcript = "It uses adenosine triphosphate, A-T-P sulfurylase in the pathway."
    findings = validate_acronym_double_emit(transcript, allowlist=set())
    assert len(findings) >= 1
    adj = [f for f in findings if f.kind == "letter_spelled_after_expansion"]
    assert adj and adj[0].acronym == "ATP"


def test_allowlisted_acronym_not_flagged():
    transcript = "It uses adenosine triphosphate, A-T-P sulfurylase in the pathway."
    findings = validate_acronym_double_emit(transcript, allowlist={"ATP"})
    assert findings == []


def test_roman_numeral_and_allowlisted_acronym_not_flagged():
    # "II" -> "two" is a Roman-numeral carve-out and never letter-spelled; an
    # allowlisted acronym stays bare. Neither is a double-emit.
    transcript = "World War two reshaped the USA and its allies."
    findings = validate_acronym_double_emit(transcript, allowlist={"USA"})
    assert findings == []


def test_roman_numeral_letterspell_carveout():
    # Even if a Roman numeral were letter-spelled, the carve-out suppresses it.
    transcript = "The world war, I-I era changed everything."
    findings = validate_acronym_double_emit(transcript, allowlist=set())
    assert all(f.acronym != "II" for f in findings)


def test_cross_chunk_double_expansion_flagged():
    # Same acronym first-use expanded twice (chunks blind to each other).
    transcript = (
        "First we meet flux balance analysis, FBA here. "
        "Later, flux balance analysis, FBA appears again."
    )
    findings = validate_acronym_double_emit(transcript, allowlist=set())
    cross = [f for f in findings if f.kind == "cross_chunk_double_expansion"]
    assert cross and cross[0].acronym == "FBA"


# ---------------------------------------------------------------------------
# Mode 3: lecture factual pass (monkeypatched assessment)
# ---------------------------------------------------------------------------


def test_lecture_pass_verdict_recorded(monkeypatch):
    monkeypatch.setattr(
        reading_correctness,
        "_assess_lecture",
        lambda t, c, m: LectureFactualAssessment(verdict="pass", reason="sound"),
    )
    entries = run_lecture_factual_pass("transcript", "ctx", "openai:gpt-5")
    assert len(entries) == 1
    assert entries[0].verdict == "pass"


def test_lecture_assessment_failure_is_fail_open(monkeypatch):
    monkeypatch.setattr(reading_correctness, "_assess_lecture", lambda t, c, m: None)
    entries = run_lecture_factual_pass("transcript", "ctx", "openai:gpt-5")
    assert entries[0].verdict == "assessment_failed"


def test_lecture_dropped_is_report_only(monkeypatch):
    # A 'dropped' verdict is RECORDED but the pass returns the transcript
    # untouched -- report-only never mutates audio.
    transcript = "The mitochondrion is the powerhouse of the cell."
    monkeypatch.setattr(
        reading_correctness,
        "_assess_lecture",
        lambda t, c, m: LectureFactualAssessment(
            verdict="dropped", reason="claim is unfixable", claim="bad claim"
        ),
    )
    entries = run_lecture_factual_pass(transcript, "ctx", "openai:gpt-5")
    assert entries[0].verdict == "dropped"
    assert entries[0].claim == "bad claim"
    # The transcript string is unchanged (the function has no mutation surface).
    assert transcript == "The mitochondrion is the powerhouse of the cell."


# ---------------------------------------------------------------------------
# Audit writers (atomic temp-then-rename JSON)
# ---------------------------------------------------------------------------


def test_write_reading_audit_atomic_with_summary(tmp_path):
    chunks = [
        diff_chunk(0, "A sentence here.", "A sentence here. " + _SPLICE, False),
        diff_chunk(1, "Echoed verbatim.", "Echoed verbatim.", True),
    ]
    acronym = validate_acronym_double_emit(
        "adenosine triphosphate, A-T-P sulfurylase", allowlist=set()
    )
    out = tmp_path / "reading-correctness-assessment.json"
    write_reading_audit(chunks, acronym, out)

    assert out.exists()
    assert not (tmp_path / "reading-correctness-assessment.json.tmp").exists()
    loaded = json.loads(out.read_text())
    assert loaded["summary"]["total_chunks"] == 2
    assert loaded["summary"]["not_assessed_chunks"] == 1
    assert loaded["summary"]["assessed_chunks"] == 1
    assert loaded["summary"]["chunks_with_insertions"] == 1
    assert loaded["summary"]["acronym_findings"] >= 1
    assert len(loaded["chunks"]) == 2


def test_write_lecture_audit_atomic_with_summary(monkeypatch, tmp_path):
    monkeypatch.setattr(reading_correctness, "_assess_lecture", lambda t, c, m: None)
    entries = run_lecture_factual_pass("t", "ctx", "m")
    out = tmp_path / "lecture-correctness-assessment.json"
    write_lecture_audit(entries, out)

    assert out.exists()
    loaded = json.loads(out.read_text())
    assert loaded["summary"]["total"] == 1
    assert loaded["summary"]["assessment_failed"] == 1
    assert len(loaded["claims"]) == 1
