"""
tests/test_abs_bookmarks.py
[[tests.test_abs_bookmarks]]
https://github.com/Mjvolk3/Swanki/tree/main/tests/test_abs_bookmarks.py
Test file: tests/test_abs_bookmarks.py

Tests for scripts/abs_bookmarks.py -- the /api/me JSON->model mapping and
citation-key filtering, fully mocked (no ABS network, no token file).
"""

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import abs_bookmarks as ab  # noqa: E402


def test_to_bookmark_maps_api_me_shape():
    raw = {
        "libraryItemId": "3d4a9ce9",
        "time": 3192.4,
        "title": "He mentions 2020 here",
        "createdAt": 1779000000000,
    }
    b = ab._to_bookmark(raw)
    assert b.library_item_id == "3d4a9ce9"
    assert b.time_s == 3192.4
    assert b.note == "He mentions 2020 here"
    assert b.created_at == 1779000000000


def test_to_bookmark_tolerates_missing_fields():
    b = ab._to_bookmark({"libraryItemId": "x"})
    assert b.library_item_id == "x"
    assert b.time_s == 0.0
    assert b.note == ""
    assert b.created_at == 0


@patch.object(ab, "_token", lambda: "tok")
def test_get_bookmarks_filters_by_citation_key_and_sorts():
    me_json = {
        "bookmarks": [
            {"libraryItemId": "A", "time": 10, "title": "old hamming note",
             "createdAt": 100},
            {"libraryItemId": "B", "time": 20, "title": "unrelated",
             "createdAt": 300},
            {"libraryItemId": "A", "time": 30, "title": "new note",
             "createdAt": 200},
        ]
    }

    def _get(url, **kw):
        m = MagicMock()
        if url.endswith("/api/me"):
            m.json.return_value = me_json
        else:  # /api/items/<id>
            m.status_code = 200
            title = "hammingArtDoingScience2020" if url.endswith("/A") else "Other Book"
            m.json.return_value = {"media": {"metadata": {"title": title}}}
        return m

    with patch.object(ab.requests, "Session") as S:
        sess = S.return_value
        sess.headers = {}
        sess.get.side_effect = _get
        out = ab.get_bookmarks(citation_key="hammingArtDoingScience2020")

    # Only item A bookmarks (title match), newest createdAt first.
    assert [b.library_item_id for b in out] == ["A", "A"]
    assert [b.created_at for b in out] == [200, 100]
    assert out[0].item_title == "hammingArtDoingScience2020"
