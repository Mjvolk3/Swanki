"""
tests/test_abs_sync.py
[[tests.test_abs_sync]]
https://github.com/Mjvolk3/Swanki/tree/main/tests/test_abs_sync.py
Test file: tests/test_abs_sync.py

Tests for swanki/abs/sync.py extraction idempotency -- the load-bearing rules:
re-runs skip mp3s already on disk, and a republished same-(key, type) mp3
replaces the stale file instead of accumulating phantom chapters.
"""

import io
import zipfile
from pathlib import Path

from swanki.abs.sync import MP3_PATTERN, extract_audio

OLD = "hamming_CH02_foundations-lecture-20260514T1010-7d23dec.mp3"
NEW = "hamming_CH02_foundations-lecture-20260609T1132-7f7e8e4.mp3"
OTHER_TYPE = "hamming_CH02_foundations-summary-20260514T1010-7d23dec.mp3"


def _zip(*names: str) -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        for n in names:
            zf.writestr(n, b"mp3-bytes")
    return buf.getvalue()


def test_mp3_pattern_groups():
    m = MP3_PATTERN.match(NEW)
    assert m is not None
    assert m.group("key") == "hamming_CH02_foundations"
    assert m.group("type") == "lecture"
    assert m.group("ts") == "20260609T1132"
    # Un-timestamped legacy names still match, with ts absent.
    legacy = MP3_PATTERN.match("k-lecture.mp3")
    assert legacy is not None and legacy.group("ts") is None


def test_extract_audio_rerun_is_noop(tmp_path: Path):
    dest = tmp_path / "proj"
    dest.mkdir()
    z = _zip(OLD, OTHER_TYPE)
    n1 = extract_audio(z, {"lecture", "summary"}, dest, "Book", "hamming")
    assert n1 == 2
    # Second run extracts nothing (filenames already on disk).
    n2 = extract_audio(z, {"lecture", "summary"}, dest, "Book", "hamming")
    assert n2 == 0


def test_extract_audio_replaces_stale_same_key_and_type(tmp_path: Path):
    dest = tmp_path / "proj"
    dest.mkdir()
    extract_audio(_zip(OLD, OTHER_TYPE), {"lecture", "summary"}, dest, "Book", "hamming")
    extract_audio(_zip(NEW), {"lecture", "summary"}, dest, "Book", "hamming")

    lecture_dir = dest / "Swanki-Book-Lecture" / "hamming"
    names = sorted(p.name for p in lecture_dir.glob("*.mp3"))
    # Old lecture replaced by the republished one; one (key, type) = one mp3.
    assert names == [NEW]
    # The other audio type is untouched.
    summary_dir = dest / "Swanki-Book-Summary" / "hamming"
    assert [p.name for p in summary_dir.glob("*.mp3")] == [OTHER_TYPE]


def test_extract_audio_respects_audiotype_filter(tmp_path: Path):
    dest = tmp_path / "proj"
    dest.mkdir()
    n = extract_audio(_zip(OLD, OTHER_TYPE), {"lecture"}, dest, "Book", "hamming")
    assert n == 1
    assert not (dest / "Swanki-Book-Summary").exists()
