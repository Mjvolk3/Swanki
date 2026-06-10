"""
tests/test_audio_comment_edit.py
[[tests.test_audio_comment_edit]]
https://github.com/Mjvolk3/Swanki/tree/main/tests/test_audio_comment_edit.py
Test file: tests/test_audio_comment_edit.py

Tests for swanki.audio.comment_edit -- comment-driven chunk edits. TTS,
restitch, timeline, and the LLM agent are all patched (no Fish, no ffmpeg,
no network).
"""

import json
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import pytest

from swanki.audio.comment_edit import edit_chunk
from swanki.models.cards import ChunkEditResponse

FISH_KWARGS = {
    "provider": "fish_speech",
    "server_url": "http://localhost:8080",
    "reference_id": "test-voice",
    "temperature": 0.8,
    "format": "mp3",
    "preprocessor": {},
}

# Same voice with the opt-in bit-string scrubber ON, so the preprocessor's
# effect is observable. The scrubber is default-off (codeword-scope fix, PR #39),
# so an empty preprocessor leaves "110" alone.
FISH_VERBALIZE = {**FISH_KWARGS, "preprocessor": {"verbalize_bit_strings": True}}


def _manifest(
    tmp: Path,
    *,
    with_post: bool = True,
    audio_type: str = "lecture",
    speed: float | None = None,
) -> Path:
    chunks_dir = tmp / f"{audio_type}_chunks"
    chunks_dir.mkdir(parents=True)
    chunks = []
    for i in range(3):
        f = f"paper_chunk{i}.mp3"
        (chunks_dir / f).write_bytes(b"old-audio-%d" % i)
        chunks.append(
            {"index": i, "section": 0, "text": f"shaped text {i}.", "file": f,
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
    if speed is not None:
        m["speed"] = speed
    if not with_post:
        del m["postprocessor"]
    mp = chunks_dir / "chunk_manifest.json"
    mp.write_text(json.dumps(m))
    return mp


@patch("swanki.audio.comment_edit.chunk_time_window", return_value=(0, 1000))
@patch("swanki.audio.comment_edit.restitch_from_chunks")
@patch("swanki.audio.comment_edit.text_to_speech")
def test_explicit_new_text_runs_preprocessor(tts, restitch, _ctw, tmp_path):
    mp = _manifest(tmp_path)
    res = edit_chunk(
        mp, 1, new_text="The codeword 110 has parity.", tts_kwargs=FISH_VERBALIZE
    )
    # Preprocessor ran on the NEW text: bit string verbalized, not bare.
    sent = tts.call_args.kwargs["text"]
    assert "one-one-zero" in sent
    assert "110" not in sent
    assert tts.call_args.kwargs["output_path"].name == "paper_chunk1.mp3"
    assert tts.call_count == 1
    # Manifest persisted the shaped text; siblings untouched.
    saved = json.loads(mp.read_text())
    assert saved["chunks"][1]["text"] == sent
    assert saved["chunks"][0]["text"] == "shaped text 0."
    restitch.assert_called_once()
    assert res.action == "edit_text"
    assert res.output_file.name == "paper-lecture-audio.mp3"
    assert (res.start_ms, res.end_ms) == (0, 1000)


@patch("swanki.audio.comment_edit.chunk_time_window", return_value=(0, 1000))
@patch("swanki.audio.comment_edit.restitch_from_chunks")
@patch("swanki.audio.comment_edit.text_to_speech")
def test_speech_only_rerolls_stored_text_verbatim(tts, restitch, _ctw, tmp_path):
    mp = _manifest(tmp_path)
    before = mp.read_text()
    res = edit_chunk(mp, 2, speech_only=True, tts_kwargs=FISH_KWARGS)
    assert tts.call_args.kwargs["text"] == "shaped text 2."  # verbatim
    assert mp.read_text() == before  # manifest unchanged
    restitch.assert_called_once()
    assert res.action == "speech_only"


@patch("swanki.audio.comment_edit.chunk_time_window", return_value=(0, 1000))
@patch("swanki.audio.comment_edit.restitch_from_chunks")
@patch("swanki.audio.comment_edit.text_to_speech")
@patch("swanki.audio.comment_edit.with_safety_retry")
def test_comment_path_agent_edit_text(safety, tts, restitch, _ctw, tmp_path):
    safety.return_value = SimpleNamespace(
        output=ChunkEditResponse(
            action="edit_text",
            revised_text="The codeword 110 stays.",
            rationale="rewrite per comment",
        )
    )
    mp = _manifest(tmp_path)
    res = edit_chunk(
        mp, 0, comment="say the bits", tts_kwargs=FISH_VERBALIZE,
        model="openai:gpt-5.5",
    )
    assert "one-one-zero" in tts.call_args.kwargs["text"]
    restitch.assert_called_once()
    assert res.action == "edit_text"


@patch("swanki.audio.comment_edit.chunk_time_window", return_value=(0, 1000))
@patch("swanki.audio.comment_edit.restitch_from_chunks")
@patch("swanki.audio.comment_edit.text_to_speech")
@patch("swanki.audio.comment_edit.with_safety_retry")
def test_needs_section_regen_does_not_touch_audio(safety, tts, restitch, _ctw, tmp_path):
    safety.return_value = SimpleNamespace(
        output=ChunkEditResponse(
            action="needs_section_regen",
            revised_text=None,
            rationale="conceptual, not a single-chunk fix",
        )
    )
    mp = _manifest(tmp_path)
    res = edit_chunk(
        mp, 0, comment="make the point stronger", tts_kwargs=FISH_KWARGS,
        model="openai:gpt-5.5",
    )
    tts.assert_not_called()
    restitch.assert_not_called()
    assert res.action == "needs_section_regen"
    assert res.output_file is None


@patch("swanki.audio.comment_edit.text_to_speech")
def test_missing_reference_id_fails_loud(tts, tmp_path):
    mp = _manifest(tmp_path)
    bad = {**FISH_KWARGS, "reference_id": ""}
    with pytest.raises(AssertionError, match="reference_id"):
        edit_chunk(mp, 0, speech_only=True, tts_kwargs=bad)
    tts.assert_not_called()


@patch("swanki.audio.comment_edit.text_to_speech")
def test_missing_postprocessor_refused(tts, tmp_path):
    mp = _manifest(tmp_path, with_post=False)
    with pytest.raises(AssertionError, match="postprocessor"):
        edit_chunk(mp, 0, speech_only=True, tts_kwargs=FISH_KWARGS)
    tts.assert_not_called()


@patch("swanki.audio.comment_edit.chunk_time_window", return_value=(0, 1000))
@patch("swanki.audio.comment_edit.restitch_from_chunks")
@patch("swanki.audio.comment_edit.text_to_speech")
def test_audit_trail_written(tts, restitch, _ctw, tmp_path):
    mp = _manifest(tmp_path)
    edit_chunk(mp, 1, new_text="A simple edit.", tts_kwargs=FISH_KWARGS)
    edits = mp.parent / "_edits"
    assert edits.is_dir()
    # Baseline chunk audio + text archived.
    assert list(edits.glob("chunk1_*.mp3"))
    txts = list(edits.glob("chunk1_*.txt"))
    assert txts and txts[0].read_text() == "shaped text 1."
    assert list(edits.glob("manifest_*.json"))
    # One log record with all required keys.
    log_lines = (edits / "edits_log.jsonl").read_text().splitlines()
    assert len(log_lines) == 1
    rec = json.loads(log_lines[0])
    assert set(rec) >= {
        "ts", "idx", "comment", "old_text", "new_text", "action",
        "rationale", "output_file", "git_hash",
    }
    assert rec["idx"] == 1
    assert rec["action"] == "edit_text"
    assert rec["old_text"] == "shaped text 1."


@patch("swanki.audio.comment_edit.chunk_time_window", return_value=(0, 1000))
@patch("swanki.audio.comment_edit.restitch_from_chunks")
@patch("swanki.audio.comment_edit.text_to_speech")
def test_speed_resolves_from_manifest(tts, _rs, _ctw, tmp_path):
    # The manifest records the gen speed; edit_chunk re-TTSs at that exact speed.
    mp = _manifest(tmp_path, audio_type="summary", speed=1.1)
    edit_chunk(mp, 0, speech_only=True, tts_kwargs=FISH_KWARGS)
    assert tts.call_args.kwargs["speed"] == 1.1


@patch("swanki.audio.comment_edit.chunk_time_window", return_value=(0, 1000))
@patch("swanki.audio.comment_edit.restitch_from_chunks")
@patch("swanki.audio.comment_edit.text_to_speech")
def test_speed_falls_back_to_audio_type_map_for_legacy_manifest(tts, _rs, _ctw, tmp_path):
    # Legacy manifest (no speed field) -> per-audio-type fallback (lecture=1.0),
    # NOT edit_chunk's old hardcoded 1.1.
    mp = _manifest(tmp_path, audio_type="lecture")  # no speed key
    assert "speed" not in json.loads(mp.read_text())
    edit_chunk(mp, 0, speech_only=True, tts_kwargs=FISH_KWARGS)
    assert tts.call_args.kwargs["speed"] == 1.0


@patch("swanki.audio.comment_edit.chunk_time_window", return_value=(0, 1000))
@patch("swanki.audio.comment_edit.restitch_from_chunks")
@patch("swanki.audio.comment_edit.text_to_speech")
def test_explicit_speed_overrides_manifest_and_map(tts, _rs, _ctw, tmp_path):
    mp = _manifest(tmp_path, audio_type="lecture", speed=1.0)
    edit_chunk(mp, 0, speech_only=True, tts_kwargs=FISH_KWARGS, speed=1.3)
    assert tts.call_args.kwargs["speed"] == 1.3
