"""
tests/test_zotero_prune.py
[[tests.test_zotero_prune]]
https://github.com/Mjvolk3/Swanki/tree/main/tests/test_zotero_prune.py

Unit tests for the Zotero replace-prior-versions behavior: after a
successful upload, ``_prune_prior_attachments`` deletes prior swanki ZIP /
apkg attachments on the parent item that share the same chapter base,
leaving only the most recent artifact per chapter.
"""

from unittest.mock import MagicMock

from swanki.sync.zotero import _chapter_base, _prune_prior_attachments


class TestChapterBase:
    def test_truncates_at_chapter_marker(self) -> None:
        assert _chapter_base(
            "alcamoSchaumsOutlineMicrobiology2010_CH01_introduction-to-microbiology"
        ) == "alcamoSchaumsOutlineMicrobiology2010_CH01"

    def test_returns_legacy_bare_chapter_form_unchanged(self) -> None:
        assert _chapter_base("alcamoSchaumsOutlineMicrobiology2010_CH01") == \
            "alcamoSchaumsOutlineMicrobiology2010_CH01"

    def test_paper_without_chapter_passes_through(self) -> None:
        # Papers (no `_CH##`) use the full content_key as their slot key.
        assert _chapter_base("bishop2024_deep-learning") == "bishop2024_deep-learning"

    def test_two_digit_chapter(self) -> None:
        assert _chapter_base("textbook_CH12_advanced-topics") == "textbook_CH12"


class TestPrunePriorAttachments:
    def test_deletes_prior_zips_for_same_chapter(self) -> None:
        zot = MagicMock()
        zot.children.return_value = [
            {
                "key": "OLD1",
                "data": {
                    "itemType": "attachment",
                    "filename": "book_CH01-20260504T2127-abc123.zip",
                },
            },
            {
                "key": "OLD2",
                "data": {
                    "itemType": "attachment",
                    "filename": "book_CH01_intro-20260505T1312-def456.zip",
                },
            },
            {
                "key": "NEW",
                "data": {
                    "itemType": "attachment",
                    "filename": "book_CH01_intro-20260506T1057-ghi789.zip",
                },
            },
        ]
        deleted = _prune_prior_attachments(
            zot,
            item_key="ITEM",
            content_key="book_CH01_intro",
            just_uploaded_filename="book_CH01_intro-20260506T1057-ghi789.zip",
        )
        assert deleted == 2
        deleted_keys = {call.args[0]["key"] for call in zot.delete_item.call_args_list}
        assert deleted_keys == {"OLD1", "OLD2"}

    def test_does_not_delete_other_chapters(self) -> None:
        zot = MagicMock()
        zot.children.return_value = [
            {
                "key": "CH2",
                "data": {
                    "itemType": "attachment",
                    "filename": "book_CH02-20260504T2127-abc123.zip",
                },
            },
            {
                "key": "CH1",
                "data": {
                    "itemType": "attachment",
                    "filename": "book_CH01-20260504T2127-abc123.zip",
                },
            },
        ]
        deleted = _prune_prior_attachments(
            zot, "ITEM", "book_CH01_intro",
            "book_CH01_intro-20260506T1057-ghi789.zip",
        )
        assert deleted == 1
        assert zot.delete_item.call_args_list[0].args[0]["key"] == "CH1"

    def test_deletes_legacy_apkg_form(self) -> None:
        # April 2026 used bare `_CH01-problem-set.apkg` (no timestamp).
        # Same chapter base, so prune it.
        zot = MagicMock()
        zot.children.return_value = [
            {
                "key": "LEGACY",
                "data": {
                    "itemType": "attachment",
                    "filename": "book_CH01-problem-set.apkg",
                },
            },
        ]
        deleted = _prune_prior_attachments(
            zot, "ITEM", "book_CH01_intro",
            "book_CH01_intro-20260506T1057-ghi789.zip",
        )
        assert deleted == 1

    def test_does_not_delete_just_uploaded(self) -> None:
        # Defensive: if Zotero's index already shows the new upload, do NOT
        # delete it. (Avoids a self-destruct on race conditions.)
        zot = MagicMock()
        zot.children.return_value = [
            {
                "key": "JUST",
                "data": {
                    "itemType": "attachment",
                    "filename": "book_CH01_intro-20260506T1057-ghi789.zip",
                },
            },
        ]
        deleted = _prune_prior_attachments(
            zot, "ITEM", "book_CH01_intro",
            "book_CH01_intro-20260506T1057-ghi789.zip",
        )
        assert deleted == 0
        zot.delete_item.assert_not_called()

    def test_ignores_non_attachment_children(self) -> None:
        # Notes, linked URLs, etc. on the parent must not be touched even
        # if their "filename" field happens to start with the chapter base.
        zot = MagicMock()
        zot.children.return_value = [
            {
                "key": "NOTE",
                "data": {
                    "itemType": "note",
                    "filename": "book_CH01-anything.zip",
                },
            },
            {
                "key": "PDF",
                "data": {
                    "itemType": "attachment",
                    "filename": "ParentBook.pdf",  # not a swanki artifact
                },
            },
        ]
        deleted = _prune_prior_attachments(
            zot, "ITEM", "book_CH01_intro",
            "book_CH01_intro-new.zip",
        )
        assert deleted == 0
