"""
tests/test_abs_sync.py
[[tests.test_abs_sync]]
https://github.com/Mjvolk3/Swanki/tree/main/tests/test_abs_sync.py
Test file: tests/test_abs_sync.py

Tests for swanki/abs/sync.py extraction idempotency -- the load-bearing rules:
re-runs skip mp3s already on disk, and a republished same-(key, type) mp3
replaces the stale file instead of accumulating phantom chapters. Also covers
the cards-only-zip fallback: ``found`` must distinguish a bundle with no audio
at all from one whose audio this projection filters out.
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
    r1 = extract_audio(z, {"lecture", "summary"}, dest, "Book", "hamming")
    assert r1.written == 2
    # Second run extracts nothing (filenames already on disk), but still
    # reports the zip as audio-bearing so the caller stops walking older zips.
    r2 = extract_audio(z, {"lecture", "summary"}, dest, "Book", "hamming")
    assert r2.written == 0
    assert r2.found == {"lecture", "summary"}


def test_extract_audio_replaces_stale_same_key_and_type(tmp_path: Path):
    dest = tmp_path / "proj"
    dest.mkdir()
    extract_audio(
        _zip(OLD, OTHER_TYPE), {"lecture", "summary"}, dest, "Book", "hamming"
    )
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
    r = extract_audio(_zip(OLD, OTHER_TYPE), {"lecture"}, dest, "Book", "hamming")
    assert r.written == 1
    assert not (dest / "Swanki-Book-Summary").exists()
    # found is pre-filter: the summary track was present, just not wanted here.
    assert r.found == {"lecture", "summary"}


def test_extract_audio_cards_only_zip_reports_no_audio(tmp_path: Path):
    """A gate re-run emits an .apkg-only zip; it must not look audio-bearing."""
    dest = tmp_path / "proj"
    dest.mkdir()
    r = extract_audio(
        _zip("hamming_CH02_foundations-20260817T1742-ecea5d4.apkg"),
        {"lecture", "summary"},
        dest,
        "Book",
        "hamming",
    )
    assert r.written == 0
    assert r.found == set()


def test_zips_by_prefix_orders_newest_first():
    """Cards-only newest zip must not hide the older audio-bearing bundle."""
    from swanki.delivery.artifacts import zips_by_prefix

    children = [
        {
            "key": "CARDS",
            "data": {"filename": "hamming_CH04_sw-20260817T1742-ecea5d4.zip"},
        },
        {
            "key": "AUDIO",
            "data": {"filename": "hamming_CH04_sw-20260610T1907-926b415.zip"},
        },
        {
            "key": "OTHER",
            "data": {"filename": "hamming_CH05_app-20260610T1915-926b415.zip"},
        },
        {"key": "NOPE", "data": {"filename": "not-an-artifact.zip"}},
    ]

    class _Zot:
        def children(self, _key):
            return children

    grouped = zips_by_prefix(_Zot(), "I")
    assert sorted(grouped) == ["hamming_CH04_sw", "hamming_CH05_app"]
    # Newest first, so the caller reaches the cards-only zip before falling
    # through to the bundle that carries the mp3s.
    assert [a["key"] for a in grouped["hamming_CH04_sw"]] == ["CARDS", "AUDIO"]


def test_inherit_cover_prefers_existing_over_pdf_render(tmp_path: Path):
    """A new projection adopts the curated cover instead of rendering the PDF."""
    from swanki.abs.metadata import inherit_cover

    existing = tmp_path / "michaelvolk" / "Swanki-Book-Lecture" / "hamming"
    existing.mkdir(parents=True)
    (existing / "cover.jpg").write_bytes(b"curated-art")

    dest_dir = tmp_path / "mv-rp" / "Swanki-Book-Lecture" / "hamming"
    dest_dir.mkdir(parents=True)
    dest = dest_dir / "cover.jpg"

    assert inherit_cover(tmp_path, "hamming", dest) is True
    assert dest.read_bytes() == b"curated-art"
    # No cover anywhere for an unknown group -> caller falls back to rendering.
    assert inherit_cover(tmp_path, "unknown-key", dest_dir / "other.jpg") is False
