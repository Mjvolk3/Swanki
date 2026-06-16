"""
tests/test_audio_card_edit.py
[[tests.test_audio_card_edit]]
https://github.com/Mjvolk3/Swanki/tree/main/tests/test_audio_card_edit.py
Test file: tests/test_audio_card_edit.py

Tests for swanki.audio.card_edit -- precise per-chunk editing of card audio.
The real edit_chunk runs, but its TTS / restitch / timeline boundaries and the
card_edit combine are all patched (no Fish, no ffmpeg, no network). The
unchanged edit_chunk core is covered by tests/test_audio_comment_edit.py.
"""

import json
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import pytest

from swanki.audio.card_edit import edit_card_chunk
from swanki.models.cards import ChunkEditResponse

FISH_KWARGS = {
    "provider": "fish_speech",
    "server_url": "http://localhost:8080",
    "reference_id": "test-voice",
    "temperature": 0.8,
    "format": "mp3",
    "preprocessor": {},
}


def _card_manifest(
    tmp: Path,
    *,
    with_back: bool = True,
    front_citation: bool = True,
    front_tts: int = 2,
    back_tts: int = 2,
    speed: float | None = None,
) -> Path:
    """Write a nested per-card manifest plus chunk + citation mp3 stubs."""
    audio_dir = tmp / "gen-md-complementary-audio"
    chunks_dir = audio_dir / "card_chunks"
    chunks_dir.mkdir(parents=True)
    uuid = "card-uuid-1"

    (audio_dir / "key_citation.mp3").write_bytes(b"citation-audio")
    (audio_dir / f"key_{uuid}_front.mp3").write_bytes(b"front-side")
    (audio_dir / f"key_{uuid}_back.mp3").write_bytes(b"back-side")

    def _tts(side: str, n: int, base_index: int) -> list[dict]:
        out = []
        for i in range(n):
            fname = f"key_card_7_{side}_chunk{i}.mp3"
            (chunks_dir / fname).write_bytes(b"chunk-%d" % i)
            out.append(
                {
                    "index": base_index + i,
                    "type": "tts",
                    "text": f"shaped {side} text {i}.",
                    "file": fname,
                }
            )
        return out

    front_chunks: list[dict] = []
    base = 0
    if front_citation:
        front_chunks.append({"index": 0, "type": "citation", "file": "key_citation.mp3"})
        base = 1
    front_chunks += _tts("front", front_tts, base)

    sides: dict = {"front": {"chunks": front_chunks}}
    if with_back:
        sides["back"] = {"chunks": _tts("back", back_tts, 0)}

    manifest = {
        "audio_type": "card",
        "card_id": uuid,
        "card_index": 7,
        "front_file": f"key_{uuid}_front.mp3",
        "back_file": f"key_{uuid}_back.mp3" if with_back else None,
        "citation_audio": "../key_citation.mp3" if front_citation else None,
        "sides": sides,
    }
    if speed is not None:
        manifest["speed"] = speed
    mp = chunks_dir / f"{uuid}_manifest.json"
    mp.write_text(json.dumps(manifest, indent=2))
    return mp


# --- the per-chunk (synthetic-manifest) path --------------------------------


@patch("swanki.audio.card_edit.combine_audio")
@patch("swanki.audio.comment_edit.chunk_time_window", return_value=(0, 1000))
@patch("swanki.audio.comment_edit.restitch_from_chunks")
@patch("swanki.audio.comment_edit.text_to_speech")
def test_front_edit_reindexes_excluding_citation(tts, _rs, _ctw, combine, tmp_path):
    mp = _card_manifest(tmp_path)
    # idx 0 addresses the FIRST tts chunk (citation invisible).
    res = edit_card_chunk(mp, "front", 0, new_text="New first.", tts_kwargs=FISH_KWARGS)
    assert res.side == "front"
    # original_index is the nested-manifest position: citation at 0, tts at 1.
    assert res.original_index == 1
    # The re-TTSed mp3 is the first front tts chunk.
    assert tts.call_args.kwargs["output_path"].name == "key_card_7_front_chunk0.mp3"
    # Citation never sent to TTS.
    assert all(
        "citation" not in c.kwargs["output_path"].name for c in tts.call_args_list
    )


@patch("swanki.audio.card_edit.combine_audio")
@patch("swanki.audio.comment_edit.chunk_time_window", return_value=(0, 1000))
@patch("swanki.audio.comment_edit.restitch_from_chunks")
@patch("swanki.audio.comment_edit.text_to_speech")
def test_front_reprepends_citation_first(tts, _rs, _ctw, combine, tmp_path):
    mp = _card_manifest(tmp_path)
    edit_card_chunk(mp, "front", 0, new_text="New first.", tts_kwargs=FISH_KWARGS)
    combine.assert_called_once()
    files = combine.call_args[0][0]
    assert files[0].name == "key_citation.mp3"  # citation prepended FIRST
    assert combine.call_args.kwargs["crossfade_ms"] == 0


@patch("swanki.audio.card_edit.combine_audio")
@patch("swanki.audio.comment_edit.chunk_time_window", return_value=(0, 1000))
@patch("swanki.audio.comment_edit.restitch_from_chunks")
@patch("swanki.audio.comment_edit.text_to_speech")
def test_back_edit_does_not_prepend_citation(tts, _rs, _ctw, combine, tmp_path):
    mp = _card_manifest(tmp_path)
    res = edit_card_chunk(mp, "back", 1, new_text="New back.", tts_kwargs=FISH_KWARGS)
    assert res.side == "back"
    assert res.original_index == 1  # no citation on back, idx == position
    assert tts.call_args.kwargs["output_path"].name == "key_card_7_back_chunk1.mp3"
    combine.assert_not_called()  # back has no citation re-prepend


def test_back_raises_when_back_file_null(tmp_path):
    mp = _card_manifest(tmp_path, with_back=False)
    with pytest.raises(AssertionError, match="no back side"):
        edit_card_chunk(mp, "back", 0, speech_only=True, tts_kwargs=FISH_KWARGS)


@patch("swanki.audio.card_edit.combine_audio")
@patch("swanki.audio.comment_edit.chunk_time_window", return_value=(0, 1000))
@patch("swanki.audio.comment_edit.restitch_from_chunks")
@patch("swanki.audio.comment_edit.text_to_speech")
def test_synthetic_manifest_shape(tts, _rs, _ctw, combine, tmp_path):
    mp = _card_manifest(tmp_path)
    captured: dict = {}

    def _capture(manifest_path, *a, **k):
        captured["data"] = json.loads(Path(manifest_path).read_text())
        captured["path"] = Path(manifest_path)

    with patch(
        "swanki.audio.card_edit.edit_chunk",
        side_effect=lambda p, idx, **k: _capture(p)
        or SimpleNamespace(action="speech_only", rationale="r"),
    ):
        edit_card_chunk(mp, "front", 0, speech_only=True, tts_kwargs=FISH_KWARGS)

    data = captured["data"]
    assert captured["path"].parent.name == "_sideedit"
    assert data["audio_type"] == "card"
    assert data["postprocessor"] == {}
    assert data["bookend_start"] is None and data["bookend_end"] is None
    # 2 front tts chunks, citation excluded, re-indexed contiguous from 0.
    assert [c["index"] for c in data["chunks"]] == [0, 1]
    for c in data["chunks"]:
        assert c["section"] == 0
        assert c["boundary"] == "paragraph"
        assert c["file"].startswith("../")  # resolve from _sideedit/
    # output_file resolves to the canonical side mp3.
    resolved = (captured["path"].parent.parent / data["output_file"]).resolve()
    assert resolved == (mp.parent.parent / "key_card-uuid-1_front.mp3").resolve()


@patch("swanki.audio.card_edit.combine_audio")
@patch("swanki.audio.comment_edit.chunk_time_window", return_value=(0, 1000))
@patch("swanki.audio.comment_edit.restitch_from_chunks")
@patch("swanki.audio.comment_edit.text_to_speech")
def test_speed_resolves_from_manifest(tts, _rs, _ctw, combine, tmp_path):
    mp = _card_manifest(tmp_path, speed=1.45)
    edit_card_chunk(mp, "front", 0, speech_only=True, tts_kwargs=FISH_KWARGS)
    assert tts.call_args.kwargs["speed"] == 1.45


@patch("swanki.audio.card_edit.combine_audio")
@patch("swanki.audio.comment_edit.chunk_time_window", return_value=(0, 1000))
@patch("swanki.audio.comment_edit.restitch_from_chunks")
@patch("swanki.audio.comment_edit.text_to_speech")
def test_speed_falls_back_to_card_default(tts, _rs, _ctw, combine, tmp_path):
    mp = _card_manifest(tmp_path)  # no speed key
    assert "speed" not in json.loads(mp.read_text())
    edit_card_chunk(mp, "front", 0, speech_only=True, tts_kwargs=FISH_KWARGS)
    assert tts.call_args.kwargs["speed"] == 1.6


@patch("swanki.audio.card_edit.combine_audio")
@patch("swanki.audio.comment_edit.chunk_time_window", return_value=(0, 1000))
@patch("swanki.audio.comment_edit.restitch_from_chunks")
@patch("swanki.audio.comment_edit.text_to_speech")
def test_audit_writeback_and_cleanup(tts, _rs, _ctw, combine, tmp_path):
    mp = _card_manifest(tmp_path)
    res = edit_card_chunk(mp, "front", 1, new_text="Edited second.", tts_kwargs=FISH_KWARGS)
    assert res.action == "edit_text"

    sideedit = mp.parent / "_sideedit"
    # Synthetic manifest deleted on success.
    assert not (sideedit / "card-uuid-1_front_manifest.json").exists()
    # Audit log carries a card-tagged record.
    log = (sideedit / "_edits" / "edits_log.jsonl").read_text().splitlines()
    card_recs = [json.loads(x) for x in log if "card_id" in x]
    assert card_recs
    rec = card_recs[-1]
    assert rec["card_id"] == "card-uuid-1"
    assert rec["side"] == "front"
    assert rec["original_index"] == 2  # citation 0, tts at 1 and 2
    assert rec["reindexed_idx"] == 1
    # Edited shaped text propagated back to the nested manifest.
    saved = json.loads(mp.read_text())
    front = saved["sides"]["front"]["chunks"]
    assert front[2]["text"] == tts.call_args.kwargs["text"]
    assert front[1]["text"] == "shaped front text 0."  # sibling untouched


@patch("swanki.audio.card_edit.combine_audio")
@patch("swanki.audio.comment_edit.chunk_time_window", return_value=(0, 1000))
@patch("swanki.audio.comment_edit.restitch_from_chunks")
@patch("swanki.audio.comment_edit.text_to_speech")
@patch("swanki.audio.comment_edit.with_safety_retry")
def test_comment_path_agent_edit(safety, tts, _rs, _ctw, combine, tmp_path):
    safety.return_value = SimpleNamespace(
        output=ChunkEditResponse(
            action="edit_text", revised_text="Agent rewrite.", rationale="per comment"
        )
    )
    mp = _card_manifest(tmp_path)
    res = edit_card_chunk(
        mp, "front", 0, comment="fix it", model="openai:gpt-5.5", tts_kwargs=FISH_KWARGS
    )
    assert res.action == "edit_text"
    assert "Agent rewrite" in tts.call_args.kwargs["text"]


# --- the whole-side re-TTS fallback -----------------------------------------


@patch("swanki.audio.card_edit.combine_audio")
@patch("swanki.audio.card_edit.text_to_speech")
def test_whole_side_fallback_from_nested_text(tts, combine, tmp_path):
    # A single-chunk back side has no card_chunks entry -> empty chunks list,
    # so it falls back to whole-side re-TTS from the transcript sidecar.
    mp = _card_manifest(tmp_path, back_tts=0)
    # Provide a transcript sidecar (no nested tts text recoverable).
    tdir = tmp_path / "complementary_transcripts"
    tdir.mkdir()
    (tdir / "key_card-uuid-1_back.md").write_text(
        "**Generated Transcript:**\nThe whole back answer.\n"
    )
    res = edit_card_chunk(mp, "back", 0, speech_only=True, tts_kwargs=FISH_KWARGS)
    assert res.action == "whole_side_retts"
    assert tts.called
    combine.assert_called_once()


@patch("swanki.audio.card_edit.combine_audio")
@patch("swanki.audio.card_edit.text_to_speech")
def test_whole_side_fallback_front_prepends_citation(tts, combine, tmp_path):
    mp = _card_manifest(tmp_path, front_tts=0)  # citation-only front, no tts chunks
    tdir = tmp_path / "complementary_transcripts"
    tdir.mkdir()
    (tdir / "key_card-uuid-1_front.md").write_text(
        "**Generated Transcript:**\nThe whole front question.\n**Citation Added:** Key\n"
    )
    edit_card_chunk(mp, "front", 0, speech_only=True, tts_kwargs=FISH_KWARGS)
    files = combine.call_args[0][0]
    assert files[0].name == "key_citation.mp3"  # citation re-prepended for front


@patch("swanki.audio.card_edit.combine_audio")
@patch("swanki.audio.card_edit.text_to_speech")
def test_whole_side_fallback_raises_without_transcript(tts, combine, tmp_path):
    mp = _card_manifest(tmp_path, back_tts=0)  # no nested back text, no sidecar
    with pytest.raises(RuntimeError, match="No transcript recoverable"):
        edit_card_chunk(mp, "back", 0, speech_only=True, tts_kwargs=FISH_KWARGS)
    tts.assert_not_called()
