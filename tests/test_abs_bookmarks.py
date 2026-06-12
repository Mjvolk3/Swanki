"""
tests/test_abs_bookmarks.py
[[tests.test_abs_bookmarks]]
https://github.com/Mjvolk3/Swanki/tree/main/tests/test_abs_bookmarks.py
Test file: tests/test_abs_bookmarks.py

Tests for swanki/abs/bookmarks.py -- the /api/me JSON->model mapping,
citation-key filtering, the windowed wipe selection, the bookmark-delete
time coercion, and the swanki-attributed create (file-local -> item-global
time shift). Fully mocked via httpx.MockTransport (no ABS network, no token
file).
"""

import json

import httpx
import pytest

from swanki.abs.bookmarks import (
    SWANKI_MARK,
    _to_bookmark,
    add_bookmark,
    clear_bookmarks,
    file_offset_in_item,
    get_bookmarks,
)
from swanki.abs.client import ABSClient

ME_JSON = {
    "bookmarks": [
        {"libraryItemId": "A", "time": 10, "title": "old hamming note",
         "createdAt": 100},
        {"libraryItemId": "B", "time": 20, "title": "unrelated",
         "createdAt": 300},
        {"libraryItemId": "A", "time": 30, "title": "new note",
         "createdAt": 200},
    ]
}

TITLES = {"A": "hammingArtDoingScience2020", "B": "Other Book"}


def _client(deleted: list[str] | None = None) -> ABSClient:
    """ABSClient over a MockTransport serving /api/me, items, and DELETEs."""

    def handler(request: httpx.Request) -> httpx.Response:
        path = request.url.path
        if request.method == "DELETE":
            if deleted is not None:
                deleted.append(path)
            return httpx.Response(200, json={})
        if path == "/api/me":
            return httpx.Response(200, json=ME_JSON)
        item_id = path.rsplit("/", 1)[-1]
        return httpx.Response(
            200,
            json={"media": {"metadata": {"title": TITLES.get(item_id, "")}}},
        )

    return ABSClient(
        base_url="https://abs.test",
        token="tok",
        transport=httpx.MockTransport(handler),
    )


def test_to_bookmark_maps_api_me_shape():
    raw = {
        "libraryItemId": "3d4a9ce9",
        "time": 3192.4,
        "title": "He mentions 2020 here",
        "createdAt": 1779000000000,
    }
    b = _to_bookmark(raw)
    assert b.library_item_id == "3d4a9ce9"
    assert b.time_s == 3192.4
    assert b.note == "He mentions 2020 here"
    assert b.created_at == 1779000000000


def test_to_bookmark_tolerates_missing_fields():
    b = _to_bookmark({"libraryItemId": "x"})
    assert b.library_item_id == "x"
    assert b.time_s == 0.0
    assert b.note == ""
    assert b.created_at == 0


def test_get_bookmarks_filters_by_citation_key_and_sorts():
    out = get_bookmarks(
        citation_key="hammingArtDoingScience2020", client=_client()
    )
    # Only item A bookmarks (title match), newest createdAt first.
    assert [b.library_item_id for b in out] == ["A", "A"]
    assert [b.created_at for b in out] == [200, 100]
    assert out[0].item_title == "hammingArtDoingScience2020"


def test_clear_bookmarks_dry_run_deletes_nothing():
    deleted: list[str] = []
    n = clear_bookmarks(
        citation_key="hammingArtDoingScience2020",
        dry_run=True,
        client=_client(deleted),
    )
    assert n == 0
    assert deleted == []


def test_clear_bookmarks_whole_item():
    deleted: list[str] = []
    n = clear_bookmarks(
        citation_key="hammingArtDoingScience2020",
        dry_run=False,
        client=_client(deleted),
    )
    assert n == 2
    assert len(deleted) == 2


def test_clear_bookmarks_windowed_selects_only_in_window():
    deleted: list[str] = []
    n = clear_bookmarks(
        citation_key="hammingArtDoingScience2020",
        windows=[(5.0, 15.0)],
        dry_run=False,
        client=_client(deleted),
    )
    # Only the time=10 bookmark falls inside the window; time=30 survives.
    assert n == 1
    assert deleted == ["/api/me/item/A/bookmark/10"]


def test_delete_bookmark_time_coercion():
    deleted: list[str] = []
    c = _client(deleted)
    c.delete_bookmark("A", 2105.0)
    c.delete_bookmark("A", 2105.5)
    # Integral floats coerce to int (ABS stores them as ints; 2105.0 404s).
    assert deleted == [
        "/api/me/item/A/bookmark/2105",
        "/api/me/item/A/bookmark/2105.5",
    ]


# -- add_bookmark ------------------------------------------------------------

BOOK_KEY = "hammingArtDoingScience2020"
CH04_KEY = f"{BOOK_KEY}_CH04_history-of-computers-software"

# Item-global layout: CH03 lecture (600s) precedes CH04 (964s).
BOOK_ITEM = {
    "id": "A",
    "media": {
        "metadata": {"title": BOOK_KEY},
        "audioFiles": [
            {
                "index": 2,
                "duration": 964.0,
                "metadata": {
                    "filename": f"{CH04_KEY}-lecture-20260610T1907-926b415.mp3"
                },
            },
            {
                "index": 1,
                "duration": 600.0,
                "metadata": {
                    "filename": f"{BOOK_KEY}_CH03_information-theory"
                    "-lecture-20260609T1200-0d95eaf.mp3"
                },
            },
        ],
    },
}


def _create_client(posted: list[tuple[str, dict]]) -> ABSClient:
    """MockTransport serving libraries/items and capturing bookmark POSTs."""

    def handler(request: httpx.Request) -> httpx.Response:
        path = request.url.path
        if request.method == "POST":
            posted.append((path, json.loads(request.content)))
            return httpx.Response(200, json={})
        if path == "/api/libraries":
            return httpx.Response(200, json={"libraries": [{"id": "lib1"}]})
        if path == "/api/libraries/lib1/items":
            return httpx.Response(200, json={"results": [BOOK_ITEM]})
        if path == "/api/items/A":
            return httpx.Response(200, json=BOOK_ITEM)
        return httpx.Response(404)

    return ABSClient(
        base_url="https://abs.test",
        token="tok",
        transport=httpx.MockTransport(handler),
    )


def test_file_offset_in_item_orders_by_index():
    assert file_offset_in_item(BOOK_ITEM, CH04_KEY, "lecture") == 600.0
    assert (
        file_offset_in_item(BOOK_ITEM, f"{BOOK_KEY}_CH03_information-theory", "lecture")
        == 0.0
    )
    assert file_offset_in_item(BOOK_ITEM, CH04_KEY, "reading") is None


def test_add_bookmark_shifts_to_item_global_and_marks_swanki():
    posted: list[tuple[str, dict]] = []
    created = add_bookmark(
        content_key=CH04_KEY,
        time_s=108.7,
        note="A/B [break] spot",
        client=_create_client(posted),
    )
    assert len(created) == 1
    path, body = posted[0]
    assert path == "/api/me/item/A/bookmark"
    # 600s of CH03 + 108.7s file-local, floored to int for delete parity.
    assert body["time"] == 708
    assert body["title"] == f"{SWANKI_MARK}: A/B [break] spot"
    assert created[0].time_s == 708.0
    assert created[0].item_title == BOOK_KEY


def test_add_bookmark_raises_when_no_item_serves_the_file():
    posted: list[tuple[str, dict]] = []
    with pytest.raises(LookupError):
        add_bookmark(
            content_key=f"{BOOK_KEY}_CH09_n-dimensional-space",
            time_s=10.0,
            note="x",
            client=_create_client(posted),
        )
    assert posted == []
