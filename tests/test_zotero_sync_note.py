"""
tests/test_zotero_sync_note.py
[[tests.test_zotero_sync_note]]
https://github.com/Mjvolk3/Swanki/tree/main/tests/test_zotero_sync_note.py

Unit tests for ``_find_or_create_sync_note``: the lookup must paginate through
ALL children via ``zot.everything`` so an existing "Swanki Sync Log" note that
has fallen off the first results page is still found, instead of spawning a
duplicate note on every sync (observed: 85 duplicates on one item).
"""

from unittest.mock import MagicMock

from swanki.sync.zotero import _find_or_create_sync_note


def _note(key: str, html: str) -> dict:
    return {"key": key, "data": {"itemType": "note", "note": html}}


def _attachment(key: str, filename: str) -> dict:
    return {"key": key, "data": {"itemType": "attachment", "filename": filename}}


class TestFindOrCreateSyncNote:
    def test_finds_note_that_fell_off_first_page(self) -> None:
        # Simulate the bug condition: page 1 (what bare children() returns) holds
        # only attachments; the sync-log note is on a later page. everything()
        # follows all pages and returns the full list including the note.
        sync_note = _note("SYNC", "<h2>Swanki Sync Log</h2>\n<p>prior</p>")
        page1 = [_attachment(f"A{i}", f"book_CH01-v{i}.zip") for i in range(25)]
        full = page1 + [sync_note]

        zot = MagicMock()
        zot.children.return_value = page1
        zot.everything.return_value = full

        item, html = _find_or_create_sync_note(zot, "PARENT")

        zot.everything.assert_called_once_with(zot.children.return_value)
        assert item is sync_note
        assert html == sync_note["data"]["note"]
        zot.create_items.assert_not_called()

    def test_creates_note_when_none_exists(self) -> None:
        zot = MagicMock()
        zot.children.return_value = []
        zot.everything.return_value = [_attachment("A1", "book_CH01.zip")]
        zot.item_template.return_value = {"note": ""}
        zot.create_items.return_value = {"successful": {"0": {"key": "NEW"}}}
        zot.item.return_value = {"key": "NEW", "data": {"note": "<h2>Swanki Sync Log</h2>\n"}}

        item, html = _find_or_create_sync_note(zot, "PARENT")

        zot.create_items.assert_called_once()
        assert html == "<h2>Swanki Sync Log</h2>\n"
        assert item["key"] == "NEW"
