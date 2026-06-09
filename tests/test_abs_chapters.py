"""
tests/test_abs_chapters.py
[[tests.test_abs_chapters]]
https://github.com/Mjvolk3/Swanki/tree/main/tests/test_abs_chapters.py
Test file: tests/test_abs_chapters.py

Tests for swanki/abs/chapters.py -- content_key derivation, cumulative
chapter bounds, the stale/canonical sqlite queries, and the per-item API
fix-up (including its re-run no-op). Fixture sqlite + mocked transport.
"""

import json
import sqlite3

import httpx

from swanki.abs.chapters import (
    _chapters_match,
    chapters_from_audiofiles,
    content_key_from_filename,
    find_books_needing_chapter_titles,
    find_books_with_stale_chapters,
    fix_item_chapters,
)
from swanki.abs.client import ABSClient

FNAME = (
    "hammingArtDoingScience2020_03_history-of-computers-hardware"
    "-lecture-20260514T1010-7d23dec.mp3"
)
KEY = "hammingArtDoingScience2020_03_history-of-computers-hardware"


def test_content_key_from_filename_strips_suffix():
    assert content_key_from_filename(FNAME) == KEY


def test_content_key_from_filename_fall_through_to_stem():
    assert content_key_from_filename("manually-added.mp3") == "manually-added"
    assert content_key_from_filename("no-extension") == "no-extension"


def _af(idx: int, fname: str, duration: float) -> dict:
    return {
        "index": idx,
        "duration": duration,
        "metadata": {"filename": fname},
    }


def test_chapters_from_audiofiles_cumulative_bounds_in_index_order():
    chapters = chapters_from_audiofiles(
        [
            _af(2, "k_02_b-lecture-20260514T1010-abc.mp3", 100.0),
            _af(1, "k_01_a-lecture-20260514T1010-abc.mp3", 60.5),
        ]
    )
    assert [c["title"] for c in chapters] == ["k_01_a", "k_02_b"]
    assert chapters[0]["start"] == 0.0
    assert chapters[0]["end"] == 60.5
    assert chapters[1]["start"] == 60.5
    assert chapters[1]["end"] == 160.5


def test_chapters_match_tolerates_subsecond_drift():
    desired = [{"id": 0, "title": "t", "start": 0.0, "end": 100.0}]
    assert _chapters_match([{"title": "t", "start": 0.4, "end": 100.4}], desired)
    assert not _chapters_match(
        [{"title": "t", "start": 0.0, "end": 100.6}], desired
    )
    assert not _chapters_match(
        [{"title": "other", "start": 0.0, "end": 100.0}], desired
    )


# -- sqlite queries -------------------------------------------------------------


def _db(tmp_path, *, chapters: list, audio_files: list) -> str:
    path = str(tmp_path / "absdatabase.sqlite")
    con = sqlite3.connect(path)
    con.execute("CREATE TABLE books (id TEXT, title TEXT, chapters TEXT, audioFiles TEXT)")
    con.execute("CREATE TABLE libraryItems (id TEXT, mediaId TEXT)")
    con.execute(
        "INSERT INTO books VALUES ('B1', 'hamming', ?, ?)",
        (json.dumps(chapters), json.dumps(audio_files)),
    )
    con.execute("INSERT INTO libraryItems VALUES ('LI1', 'B1')")
    con.commit()
    con.close()
    return path


def test_find_stale_accepts_exact_and_prefix_titles(tmp_path):
    audio_files = [_af(1, FNAME, 100.0)]
    # Prefix form (manually-cleaned title): valid, not stale.
    db = _db(tmp_path, chapters=[{"title": KEY}], audio_files=audio_files)
    assert find_books_with_stale_chapters(db) == []
    # Title referencing a deleted file: stale.
    (tmp_path / "x").mkdir()
    db2 = _db(
        tmp_path / "x",
        chapters=[{"title": "old-deleted-file"}],
        audio_files=audio_files,
    )
    assert find_books_with_stale_chapters(db2) == [("LI1", "B1", "hamming")]


def test_find_needing_titles_skips_canonical_books(tmp_path):
    audio_files = [_af(1, FNAME, 100.0)]
    canonical = [{"id": 0, "title": KEY, "start": 0.0, "end": 100.0}]
    db = _db(tmp_path, chapters=canonical, audio_files=audio_files)
    assert find_books_needing_chapter_titles(db) == []

    (tmp_path / "y").mkdir()
    db2 = _db(tmp_path / "y", chapters=[], audio_files=audio_files)
    needing = find_books_needing_chapter_titles(db2)
    assert len(needing) == 1
    assert needing[0][4][0]["title"] == KEY


# -- per-item API fix-up ---------------------------------------------------------


def _item_client(item_json: dict, posted: list) -> ABSClient:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.method == "POST":
            posted.append(json.loads(request.content))
            return httpx.Response(200, json={})
        return httpx.Response(200, json=item_json)

    return ABSClient(
        base_url="https://abs.test",
        token="tok",
        transport=httpx.MockTransport(handler),
    )


def test_fix_item_chapters_posts_then_noops():
    audio_files = [_af(1, FNAME, 100.0)]
    stale_item = {
        "media": {
            "audioFiles": audio_files,
            "chapters": [{"title": "old", "start": 0.0, "end": 90.0}],
        }
    }
    posted: list = []
    assert fix_item_chapters(_item_client(stale_item, posted), "LI1") is True
    assert posted[0]["chapters"][0]["title"] == KEY

    canonical_item = {
        "media": {
            "audioFiles": audio_files,
            "chapters": posted[0]["chapters"],
        }
    }
    posted2: list = []
    # Re-run on canonical state is a no-op (idempotency).
    assert fix_item_chapters(_item_client(canonical_item, posted2), "LI1") is False
    assert posted2 == []
