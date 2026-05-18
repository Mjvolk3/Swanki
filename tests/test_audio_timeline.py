"""
tests/test_audio_timeline.py
[[tests.test_audio_timeline]]
https://github.com/Mjvolk3/Swanki/tree/main/tests/test_audio_timeline.py
Test file: tests/test_audio_timeline.py

Exactness tests for the chunk-time mapping: the `chunk_timeline.json`
sidecar must describe the bytes actually assembled (measured, never
re-derived). No Fish server; synthetic silent mp3 chunks via ffmpeg.
"""

import json

import pytest
from pydub import AudioSegment

from swanki.audio._common import (
    TIMELINE_FILENAME,
    ChunkTimeline,
    chunk_time_window,
    chunk_time_window_abs,
    restitch_from_chunks,
    time_to_chunk,
)

SR = "192k"


def _mk(path, ms):
    AudioSegment.silent(duration=ms).export(str(path), format="mp3", bitrate=SR)
    return path


def _manifest(tmp, *, tail_trim=0):
    ck = tmp / "lecture_chunks"
    ck.mkdir(parents=True)
    # Unequal lengths, 2 sections, start+end bookends.
    _mk(ck / "bs.mp3", 700)
    _mk(ck / "be.mp3", 600)
    specs = [  # (index, section, file, intended_ms, boundary)
        (0, 0, "c0.mp3", 1500, "paragraph"),
        (1, 0, "c1.mp3", 900, "sentence"),
        (2, 0, "c2.mp3", 1200, "paragraph"),
        (3, 1, "c3.mp3", 800, "paragraph"),
        (4, 1, "c4.mp3", 1100, "sentence"),
    ]
    chunks = []
    for idx, sec, fn, ms, b in specs:
        _mk(ck / fn, ms)
        chunks.append(
            {"index": idx, "section": sec, "text": f"t{idx}", "file": fn,
             "boundary": b}
        )
    manifest = {
        "audio_type": "lecture",
        "output_file": "paper-lecture-audio.mp3",
        "bookend_start": "bs.mp3",
        "bookend_end": "be.mp3",
        "postprocessor": {
            "section_pause_ms": 5000,
            "chunk_pause_ms": 700,
            "chunk_pause_ms_by_boundary": {"paragraph": 1100, "sentence": 500},
            "chunk_tail_trim_ms": tail_trim,
            "chunk_crossfade_ms": 0,
            "gain_match_target_dbfs": None,
            "bookend_pause_ms": 500,
        },
        "chunks": chunks,
    }
    mp = ck / "chunk_manifest.json"
    mp.write_text(json.dumps(manifest))
    return mp, ck, specs


def test_sidecar_equals_independent_oracle(tmp_path):
    """With trim=0/crossfade=0, recompute offsets independently from the
    loaded segment lengths and assert the sidecar matches exactly.
    """
    mp, ck, specs = _manifest(tmp_path)
    out = tmp_path / "paper-lecture-audio.mp3"
    restitch_from_chunks(mp, out)
    tl = ChunkTimeline.model_validate_json(
        (ck / TIMELINE_FILENAME).read_text()
    )
    bmap = {"paragraph": 1100, "sentence": 500}

    # Oracle: replay the exact assembly arithmetic over the *loaded* lengths.
    bs_len = len(AudioSegment.from_mp3(str(ck / "bs.mp3")))
    assert tl.bookend_start is not None
    assert tl.bookend_start.offset_ms == 0
    assert tl.bookend_start.duration_ms == bs_len
    assert tl.bookend_start.end_ms == bs_len
    pos = bs_len + 500  # bookend_pause
    by_idx = {c.index: c for c in tl.chunks}
    for sec in (0, 1):
        sec_specs = [s for s in specs if s[1] == sec]
        pos += 5000  # section_pause precedes every section (bookend before s0)
        for j, (idx, _s, fn, _ms, b) in enumerate(sec_specs):
            if j > 0:
                pos += bmap[b]  # inter-chunk gap (boundary of THIS chunk)
            seg = len(AudioSegment.from_mp3(str(ck / fn)))
            c = by_idx[idx]
            assert c.offset_ms == pos, f"chunk{idx} offset {c.offset_ms}!={pos}"
            assert c.duration_ms == seg
            assert c.end_ms == pos + seg
            pos += seg
    pos += 500  # bookend_pause before end bookend
    be_len = len(AudioSegment.from_mp3(str(ck / "be.mp3")))
    assert tl.bookend_end.offset_ms == pos
    assert tl.total_duration_ms == pos + be_len


def test_total_matches_restitched_file(tmp_path):
    mp, ck, _ = _manifest(tmp_path)
    out = tmp_path / "o.mp3"
    restitch_from_chunks(mp, out)
    tl = ChunkTimeline.model_validate_json(
        (ck / TIMELINE_FILENAME).read_text()
    )
    actual = len(AudioSegment.from_mp3(str(out)))
    # mp3 re-encode adds a little frame padding; tight tolerance.
    assert abs(tl.total_duration_ms - actual) <= 60


def test_roundtrip_window_and_time_to_chunk(tmp_path):
    mp, ck, specs = _manifest(tmp_path)
    restitch_from_chunks(mp, tmp_path / "o.mp3")
    for idx, _s, _f, _ms, _b in specs:
        a, b = chunk_time_window(ck, "lecture", idx)
        assert b > a
        mid = (a + b) // 2
        assert time_to_chunk(ck, "lecture", mid) == idx


def test_absolute_offset_and_abs_helper(tmp_path):
    mp, ck, _ = _manifest(tmp_path)
    restitch_from_chunks(mp, tmp_path / "o.mp3")
    base = chunk_time_window(ck, "lecture", 3)
    shifted = chunk_time_window(ck, "lecture", 3, absolute_offset_ms=120000)
    assert shifted == (base[0] + 120000, base[1] + 120000)
    assert chunk_time_window_abs(
        ck, "lecture", 3, preceding_chapter_durations_ms=120000
    ) == shifted
    assert time_to_chunk(ck, "lecture", shifted[0] + 1,
                         absolute_offset_ms=120000) == 3


def test_audio_type_mismatch_raises(tmp_path):
    mp, ck, _ = _manifest(tmp_path)
    restitch_from_chunks(mp, tmp_path / "o.mp3")
    with pytest.raises(AssertionError, match="audio.type"):
        chunk_time_window(ck, "reading", 0)


def test_determinism_byte_identity(tmp_path):
    """Two restitches of identical inputs yield an identical sidecar
    (proxy for the refactor not changing assembled bytes).
    """
    mp, ck, _ = _manifest(tmp_path)
    restitch_from_chunks(mp, tmp_path / "o1.mp3")
    s1 = (ck / TIMELINE_FILENAME).read_text()
    restitch_from_chunks(mp, tmp_path / "o2.mp3")
    s2 = (ck / TIMELINE_FILENAME).read_text()
    assert s1 == s2


def test_tail_trim_is_measured_not_predicted(tmp_path):
    """A chunk with long trailing silence trimmed by `_load` must have a
    timeline duration SHORTER than its raw mp3 length -- proving the
    timeline measures the trimmed segment, never predicts from the file.
    """
    mp, ck, _ = _manifest(tmp_path, tail_trim=400)
    # c1 is 900ms of pure silence -> _load's silence-aware trim fires.
    raw_c1 = len(AudioSegment.from_mp3(str(ck / "c1.mp3")))
    restitch_from_chunks(mp, tmp_path / "o.mp3")
    tl = ChunkTimeline.model_validate_json(
        (ck / TIMELINE_FILENAME).read_text()
    )
    c1 = next(c for c in tl.chunks if c.index == 1)
    assert c1.duration_ms < raw_c1, (
        f"trimmed duration {c1.duration_ms} not < raw {raw_c1} "
        "-- timeline is predicting, not measuring"
    )


def test_sidecar_missing_recompute_fallback(tmp_path):
    mp, ck, _ = _manifest(tmp_path)
    restitch_from_chunks(mp, tmp_path / "o.mp3")
    ref = chunk_time_window(ck, "lecture", 2)
    (ck / TIMELINE_FILENAME).unlink()
    # No sidecar -> recompute via the SAME accumulator, persist, answer.
    assert chunk_time_window(ck, "lecture", 2) == ref
    assert (ck / TIMELINE_FILENAME).exists()
