"""
tests/test_source_corrections.py
[[tests.test_source_corrections]]
https://github.com/Mjvolk3/Swanki/tree/main/tests/test_source_corrections.py
Test file: tests/test_source_corrections.py

Tests for swanki.audio.source_corrections -- the opt-in source-correction apply
layer. Fixtures are drawn from the Kuchel CH02-CH05 spoken/silent correction
list. TTS, restitch, and the chunk-timeline lookup are patched (no Fish, no
ffmpeg, no network), mirroring tests/test_audio_comment_edit.py.
"""

import json
from pathlib import Path
from unittest.mock import patch

import pytest
import yaml
from pydantic import ValidationError

from swanki.audio.source_corrections import apply_source_corrections
from swanki.models.cards import SourceCorrection

FISH_KWARGS = {
    "provider": "fish_speech",
    "server_url": "http://localhost:8080",
    "reference_id": "test-voice",
    "temperature": 0.8,
    "format": "mp3",
    "preprocessor": {},
}


def _manifest(tmp: Path, *, audio_type: str, texts: list[str]) -> Path:
    """Write a minimal chunk manifest + chunk mp3s and return the manifest path."""
    chunks_dir = tmp / f"{audio_type}_chunks"
    chunks_dir.mkdir(parents=True)
    chunks = []
    for i, text in enumerate(texts):
        f = f"paper_chunk{i}.mp3"
        (chunks_dir / f).write_bytes(b"old-audio-%d" % i)
        chunks.append(
            {"index": i, "section": 0, "text": text, "file": f,
             "boundary": "paragraph"}
        )
    m = {
        "audio_type": audio_type,
        "output_file": f"paper-{audio_type}-audio.mp3",
        "bookend_start": None,
        "bookend_end": None,
        "postprocessor": {"section_pause_ms": 5000},
        "chunks": chunks,
    }
    mp = chunks_dir / "chunk_manifest.json"
    mp.write_text(json.dumps(m))
    return mp


def _spec(tmp: Path, rows: list[dict]) -> Path:
    p = tmp / "spec.yaml"
    p.write_text(yaml.safe_dump(rows))
    return p


def _patched():
    """Patch TTS/restitch/timeline so no Fish or ffmpeg is needed."""
    return (
        patch("swanki.audio.comment_edit.text_to_speech"),
        patch("swanki.audio.comment_edit.restitch_from_chunks"),
        patch("swanki.audio.comment_edit.chunk_time_window", return_value=(0, 1000)),
        patch("swanki.audio.source_corrections.restitch_from_chunks"),
    )


# ---------------------------------------------------------------------------
# Apply-layer behavior
# ---------------------------------------------------------------------------


def test_override_reading_gets_spoken_note_midchunk(tmp_path):
    # Kuchel CH03-55: saturated -> unsaturated fatty acids (a genuine source
    # override; the listener must hear the dispute).
    mp = _manifest(
        tmp_path,
        audio_type="reading",
        texts=[
            "Cells store energy as fat.",
            "Membranes are rich in saturated fatty acids. They pack tightly "
            "and raise the melting point of the bilayer.",
            "The next section covers transport.",
        ],
    )
    spec = _spec(
        tmp_path,
        [{
            "id": "ch03-fatty-55",
            "track": "reading",
            "wrong_text": "saturated fatty acids",
            "corrected_text": "unsaturated fatty acids",
            "reason": "the cited membranes are fluid, so the acyl chains are unsaturated",
            "kind": "override",
        }],
    )
    p_tts, p_rs, p_ctw, p_srs = _patched()
    with p_tts as tts, p_rs, p_ctw, p_srs as srs:
        entries = apply_source_corrections(
            spec, {"reading": mp}, tts_kwargs=FISH_KWARGS,
            audit_path=tmp_path / "audit.json",
        )
    # Exactly one chunk re-TTS'd; the sent text is the stored text verbatim.
    assert tts.call_count == 1
    sent = tts.call_args.kwargs["text"]
    assert "Swanki correction" in sent
    assert "unsaturated fatty acids" in sent
    # The corrected prose replaced the source in the READING sentence (the note
    # deliberately repeats the source phrase, so a bare absence check is wrong).
    reading_sentence = sent.split("[pause]")[0]
    assert "unsaturated fatty acids" in reading_sentence
    assert "saturated fatty acids" not in reading_sentence.replace(
        "unsaturated fatty acids", ""
    )
    # Framing [pause] tags survived and the note is mid-chunk (not boundary).
    assert sent.count("[pause]") == 2
    assert not sent.startswith("[pause]")
    assert not sent.rstrip().endswith("[pause]")
    # One restitch fired for the touched track.
    srs.assert_called_once()
    e = entries[0]
    assert e.status == "applied" and e.spoken is True and e.chunk_index == 1
    # Manifest persisted the shaped text + the applied id.
    saved = json.loads(mp.read_text())
    assert "Swanki correction" in saved["chunks"][1]["text"]
    assert saved["chunks"][1]["applied_corrections"] == ["ch03-fatty-55"]
    # Audit written.
    audit = json.loads((tmp_path / "audit.json").read_text())
    assert audit["summary"]["applied"] == 1 and audit["summary"]["spoken"] == 1


def test_override_preshaped_note_text_survives_verbatim(tmp_path):
    # Kuchel CH03-79: monoterpene C10H15 -> C10H16, note pre-shaped so the
    # formula is spoken correctly and NOT scrubbed.
    note = (
        "[pause] Swanki correction: the source prints C 10 H 15, but the "
        "monoterpene formula is C 10 H 16 [pause]"
    )
    mp = _manifest(
        tmp_path,
        audio_type="reading",
        texts=[
            "Terpenes are built from isoprene units.",
            "A monoterpene has the formula C10H15 in the printed table. "
            "It is volatile and fragrant.",
        ],
    )
    spec = _spec(
        tmp_path,
        [{
            "id": "ch03-terpene-79",
            "track": "reading",
            "wrong_text": "C10H15",
            "corrected_text": "C10H16",
            "reason": "two isoprene units give ten carbons and sixteen hydrogens",
            "kind": "override",
            "note_text": note,
        }],
    )
    p_tts, p_rs, p_ctw, p_srs = _patched()
    with p_tts as tts, p_rs, p_ctw, p_srs:
        apply_source_corrections(
            spec, {"reading": mp}, tts_kwargs=FISH_KWARGS,
            audit_path=tmp_path / "audit.json",
        )
    sent = tts.call_args.kwargs["text"]
    # The pre-shaped note is present verbatim (spaced formula intact).
    assert "C 10 H 16" in sent
    assert sent.count("[pause]") == 2
    assert not sent.startswith("[pause]")


def test_restoration_is_silent_no_note(tmp_path):
    # Kuchel CH04-150: Try -> Tyr, a mechanical OCR restoration (no note).
    mp = _manifest(
        tmp_path,
        audio_type="reading",
        texts=[
            "The aromatic residues are important.",
            "Phenylalanine and Try absorb ultraviolet light strongly.",
        ],
    )
    spec = _spec(
        tmp_path,
        [{
            "id": "ch04-tyr-150",
            "track": "reading",
            "wrong_text": "Try",
            "corrected_text": "Tyr",
            "reason": "OCR garble of the tyrosine three-letter code",
            "kind": "restoration",
        }],
    )
    p_tts, p_rs, p_ctw, p_srs = _patched()
    with p_tts as tts, p_rs, p_ctw, p_srs:
        entries = apply_source_corrections(
            spec, {"reading": mp}, tts_kwargs=FISH_KWARGS,
            audit_path=tmp_path / "audit.json",
        )
    sent = tts.call_args.kwargs["text"]
    assert "Tyr" in sent
    assert "Swanki correction" not in sent
    assert "[pause]" not in sent
    e = entries[0]
    assert e.status == "applied" and e.spoken is False


def test_reading_wrong_text_not_found_raises(tmp_path):
    mp = _manifest(
        tmp_path, audio_type="reading",
        texts=["Nothing here matches.", "Still nothing relevant."],
    )
    spec = _spec(
        tmp_path,
        [{
            "id": "ch02-missing",
            "track": "reading",
            "wrong_text": "6 CO2",
            "corrected_text": "6 O2",
            "reason": "the reactant is molecular oxygen",
            "kind": "override",
        }],
    )
    p_tts, p_rs, p_ctw, p_srs = _patched()
    with p_tts, p_rs, p_ctw, p_srs, pytest.raises(AssertionError, match="not found"):
        apply_source_corrections(
            spec, {"reading": mp}, tts_kwargs=FISH_KWARGS,
            audit_path=tmp_path / "audit.json",
        )


def test_idempotency_apply_twice_equals_once(tmp_path):
    mp = _manifest(
        tmp_path,
        audio_type="reading",
        texts=[
            "Intro sentence.",
            "Membranes are rich in saturated fatty acids. They pack tightly.",
        ],
    )
    spec = _spec(
        tmp_path,
        [{
            "id": "ch03-fatty-55",
            "track": "reading",
            "wrong_text": "saturated fatty acids",
            "corrected_text": "unsaturated fatty acids",
            "reason": "the membranes are fluid",
            "kind": "override",
        }],
    )
    p_tts, p_rs, p_ctw, p_srs = _patched()
    with p_tts, p_rs, p_ctw, p_srs:
        apply_source_corrections(
            spec, {"reading": mp}, tts_kwargs=FISH_KWARGS,
            audit_path=tmp_path / "audit1.json",
        )
    after_first = mp.read_text()
    note_count = after_first.count("Swanki correction")
    assert note_count == 1

    p_tts, p_rs, p_ctw, p_srs = _patched()
    with p_tts as tts2, p_rs, p_ctw, p_srs as srs2:
        entries = apply_source_corrections(
            spec, {"reading": mp}, tts_kwargs=FISH_KWARGS,
            audit_path=tmp_path / "audit2.json",
        )
    # Second run: no re-TTS, no restitch, all already_applied, text unchanged.
    tts2.assert_not_called()
    srs2.assert_not_called()
    assert [e.status for e in entries] == ["already_applied"]
    assert mp.read_text() == after_first
    assert mp.read_text().count("Swanki correction") == note_count


def test_lecture_wrong_text_absent_is_not_applicable(tmp_path):
    # Lecture is paraphrased first-person prose; a literal miss is expected and
    # records not_applicable rather than raising.
    mp = _manifest(
        tmp_path,
        audio_type="lecture",
        texts=[
            "So today I want to walk you through the fatty acids in membranes.",
            "They keep the bilayer fluid, which really matters for transport.",
        ],
    )
    before = mp.read_text()
    spec = _spec(
        tmp_path,
        [{
            "id": "ch03-fatty-55",
            "track": "lecture",
            "wrong_text": "saturated fatty acids",
            "corrected_text": "unsaturated fatty acids",
            "reason": "the membranes are fluid",
            "kind": "override",
        }],
    )
    p_tts, p_rs, p_ctw, p_srs = _patched()
    with p_tts as tts, p_rs, p_ctw, p_srs:
        entries = apply_source_corrections(
            spec, {"lecture": mp}, tts_kwargs=FISH_KWARGS,
            audit_path=tmp_path / "audit.json",
        )
    tts.assert_not_called()
    assert entries[0].status == "not_applicable"
    assert entries[0].chunk_index is None
    assert mp.read_text() == before  # no mutation


def test_lecture_literal_match_substitutes_silently(tmp_path):
    # When a lecture chunk DOES contain wrong_text, substitute silently (no note
    # even though kind is override -- lecture is paraphrase, Decision 7).
    mp = _manifest(
        tmp_path,
        audio_type="lecture",
        texts=[
            "Here the printed table lists C10H15 for the monoterpene, which we "
            "will revisit.",
        ],
    )
    spec = _spec(
        tmp_path,
        [{
            "id": "ch03-terpene-79",
            "track": "lecture",
            "wrong_text": "C10H15",
            "corrected_text": "C10H16",
            "reason": "ten carbons, sixteen hydrogens",
            "kind": "override",
        }],
    )
    p_tts, p_rs, p_ctw, p_srs = _patched()
    with p_tts as tts, p_rs, p_ctw, p_srs:
        entries = apply_source_corrections(
            spec, {"lecture": mp}, tts_kwargs=FISH_KWARGS,
            audit_path=tmp_path / "audit.json",
        )
    sent = tts.call_args.kwargs["text"]
    assert "C10H16" in sent
    assert "Swanki correction" not in sent  # silent on the paraphrase track
    assert entries[0].status == "applied" and entries[0].spoken is False


# ---------------------------------------------------------------------------
# Pydantic validators
# ---------------------------------------------------------------------------


def test_kind_outside_literal_fails():
    with pytest.raises(ValidationError):
        SourceCorrection(
            id="x", track="reading", wrong_text="a", corrected_text="b",
            reason="r", kind="bogus",
        )


def test_override_without_reason_fails():
    with pytest.raises(ValidationError, match="override"):
        SourceCorrection(
            id="x", track="reading", wrong_text="a", corrected_text="b",
            reason="", kind="override",
        )


def test_restoration_with_note_text_fails():
    with pytest.raises(ValidationError, match="restoration"):
        SourceCorrection(
            id="x", track="reading", wrong_text="a", corrected_text="b",
            reason="", kind="restoration", note_text="[pause] no [pause]",
        )
