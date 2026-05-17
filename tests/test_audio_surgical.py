"""
tests/test_audio_surgical.py
[[tests.test_audio_surgical]]
https://github.com/Mjvolk3/Swanki/tree/main/tests/test_audio_surgical.py
Test file: tests/test_audio_surgical.py

Tests for swanki.audio.surgical -- surgical re-TTS + restitch, with
text_to_speech and restitch_from_chunks mocked (no Fish, no ffmpeg).
"""

import json
from pathlib import Path
from unittest.mock import patch

import pytest

from swanki.audio.surgical import regenerate_and_restitch


def _manifest(tmp: Path, *, with_post: bool = True) -> Path:
    chunks_dir = tmp / "reading_chunks"
    chunks_dir.mkdir(parents=True)
    chunks = []
    for i in range(3):
        f = f"paper_chunk{i}.mp3"
        (chunks_dir / f).write_bytes(b"old-audio-%d" % i)
        chunks.append(
            {"index": i, "section": 0, "text": f"text {i}", "file": f,
             "boundary": "paragraph"}
        )
    m = {
        "audio_type": "reading",
        "output_file": "paper-reading-audio.mp3",
        "bookend_start": None,
        "bookend_end": None,
        "postprocessor": {"section_pause_ms": 5000},
        "chunks": chunks,
    }
    mp = chunks_dir / "chunk_manifest.json"
    if not with_post:
        del m["postprocessor"]
    mp.write_text(json.dumps(m))
    return mp


@patch("swanki.audio.surgical.restitch_from_chunks")
@patch("swanki.audio.surgical.text_to_speech")
def test_text_edit_persists_and_only_named_chunk_retts(tts, restitch, tmp_path):
    mp = _manifest(tmp_path)
    out = regenerate_and_restitch(
        mp, {1: "corrected text 1"}, audio_type="reading"
    )
    # Only chunk 1 re-rendered, with the corrected text.
    assert tts.call_count == 1
    assert tts.call_args.kwargs["text"] == "corrected text 1"
    assert tts.call_args.kwargs["output_path"].name == "paper_chunk1.mp3"
    # Manifest text updated for chunk 1, others untouched.
    saved = json.loads(mp.read_text())
    assert saved["chunks"][1]["text"] == "corrected text 1"
    assert saved["chunks"][0]["text"] == "text 0"
    restitch.assert_called_once()
    assert out.name == "paper-reading-audio.mp3"


@patch("swanki.audio.surgical.restitch_from_chunks")
@patch("swanki.audio.surgical.text_to_speech")
def test_none_edit_retts_existing_text_no_manifest_write(tts, restitch, tmp_path):
    mp = _manifest(tmp_path)
    before = mp.read_text()
    regenerate_and_restitch(mp, {2: None}, audio_type="reading")
    assert tts.call_args.kwargs["text"] == "text 2"
    assert mp.read_text() == before  # no rewrite when nothing changed
    restitch.assert_called_once()


@patch("swanki.audio.surgical.restitch_from_chunks")
@patch("swanki.audio.surgical.text_to_speech")
def test_audio_type_mismatch_fails_loud(tts, restitch, tmp_path):
    mp = _manifest(tmp_path)
    with pytest.raises(AssertionError, match="audio_type"):
        regenerate_and_restitch(mp, {0: None}, audio_type="lecture")
    tts.assert_not_called()


@patch("swanki.audio.surgical.restitch_from_chunks")
@patch("swanki.audio.surgical.text_to_speech")
def test_missing_postprocessor_refused(tts, restitch, tmp_path):
    mp = _manifest(tmp_path, with_post=False)
    with pytest.raises(AssertionError, match="postprocessor"):
        regenerate_and_restitch(mp, {0: None})
    tts.assert_not_called()


@patch("swanki.audio.surgical.restitch_from_chunks")
@patch("swanki.audio.surgical.text_to_speech")
def test_unknown_chunk_index_fails_loud(tts, restitch, tmp_path):
    mp = _manifest(tmp_path)
    with pytest.raises(AssertionError, match="index 99"):
        regenerate_and_restitch(mp, {99: "x"})
