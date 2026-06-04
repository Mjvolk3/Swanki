"""
tests/test_swanki_anki_sync.py
[[tests.test_swanki_anki_sync]]
https://github.com/Mjvolk3/Swanki/tree/main/tests/test_swanki_anki_sync.py

Unit tests for the artifact helper (now ``swanki/delivery/artifacts.py``, re-
exported through ``scripts/_swanki_zotero_artifacts.py``) and the walk-all
``scripts/swanki_anki_sync.py`` manual command. AnkiConnect-primitive tests
live in ``tests/test_delivery_anki.py`` (the canonical home). Mocks pyzotero +
``requests.post``; no live network.
"""

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

# scripts/ isn't a package; add it to sys.path before importing modules
# under test. Mirrors how the scripts are invoked from the repo root.
SCRIPTS_DIR = str(Path(__file__).parent.parent / "scripts")
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

from _swanki_zotero_artifacts import (  # noqa: E402
    APKG_PATTERN,
    ZIP_PATTERN,
    _latest_artifact,
    latest_apkgs,
    latest_zips,
)


def _att(key: str, filename: str) -> dict:
    """Build a fake zot.children() attachment dict."""
    return {"key": key, "data": {"itemType": "attachment", "filename": filename}}


class TestLatestArtifact:
    def test_newest_per_prefix_zip(self) -> None:
        zot = MagicMock()
        zot.children.return_value = [
            _att("OLD", "bishop2024-20260101T1200-abc123.zip"),
            _att("NEW", "bishop2024-20260201T1200-def456.zip"),
            _att("OTHER", "bishop2024-20260115T1200-ghi789.zip"),
        ]
        result = _latest_artifact(zot, "ITEM", ZIP_PATTERN)
        assert len(result) == 1
        assert result[0]["key"] == "NEW"

    def test_groups_book_chapters_by_prefix(self) -> None:
        # Two chapters, one apkg each.
        zot = MagicMock()
        zot.children.return_value = [
            _att("CH1_OLD", "book_CH01_intro-20260101T1200-abc123.apkg"),
            _att("CH1_NEW", "book_CH01_intro-20260201T1200-def456.apkg"),
            _att("CH2_OLD", "book_CH02_circuits-20260101T1200-abc123.apkg"),
            _att("CH2_NEW", "book_CH02_circuits-20260201T1200-def456.apkg"),
        ]
        result = _latest_artifact(zot, "ITEM", APKG_PATTERN)
        keys = sorted(a["key"] for a in result)
        assert keys == ["CH1_NEW", "CH2_NEW"]

    def test_empty_returns_empty(self) -> None:
        zot = MagicMock()
        zot.children.return_value = []
        assert _latest_artifact(zot, "ITEM", APKG_PATTERN) == []

    def test_ignores_other_suffix(self) -> None:
        # Zip attachments are present; apkg pattern must ignore them.
        zot = MagicMock()
        zot.children.return_value = [
            _att("Z", "bishop2024-20260101T1200-abc123.zip"),
        ]
        assert _latest_artifact(zot, "ITEM", APKG_PATTERN) == []
        assert len(_latest_artifact(zot, "ITEM", ZIP_PATTERN)) == 1

    def test_ignores_non_matching_filenames(self) -> None:
        zot = MagicMock()
        zot.children.return_value = [
            _att("MIDDLEMAN", "swanki-sync-log.note"),
            _att("LEGACY", "book.apkg"),  # no timestamp
            _att("LEGACY2", "book-20260101.apkg"),  # no commit hash
            _att("REAL", "book-20260101T1200-abc123.apkg"),
        ]
        result = _latest_artifact(zot, "ITEM", APKG_PATTERN)
        assert [a["key"] for a in result] == ["REAL"]

    def test_apkg_wrapper(self) -> None:
        zot = MagicMock()
        zot.children.return_value = [_att("X", "ProblemSet-20260201T1200-abc.apkg")]
        assert [a["key"] for a in latest_apkgs(zot, "I")] == ["X"]

    def test_zip_wrapper(self) -> None:
        zot = MagicMock()
        zot.children.return_value = [_att("X", "Paper-20260201T1200-abc.zip")]
        assert [a["key"] for a in latest_zips(zot, "I")] == ["X"]


# Import the walk-all manual command lazily.
import swanki_anki_sync as sas  # noqa: E402

# push_projection calls the canonical ankiconnect_call, which posts via the
# target module's ``requests`` -- patch there, not on the shim.
_TARGET_POST = "swanki.delivery.targets.anki.requests.post"


class TestPushProjection:
    def test_skips_when_push_anki_false(self, tmp_path: Path) -> None:
        cfg = {"zotero": {"library_id": "1", "tag": "fox"}, "push_anki": False}
        n = sas.push_projection("p", cfg, "key", "http://x", tmp_path, dry_run=False)
        assert n == 0

    def test_dry_run_does_not_post(self, tmp_path: Path) -> None:
        cfg = {"zotero": {"library_id": "1", "tag": "fox"}, "push_anki": True}
        fake_item = {"key": "ITEM", "data": {"citationKey": "bishop2024"}}
        fake_att = _att("ATT", "bishop2024-20260201T1200-abc123.apkg")
        zot_inst = MagicMock()
        zot_inst.items.return_value = [fake_item]
        zot_inst.children.return_value = [fake_att]
        with (
            patch("swanki_anki_sync.zotero.Zotero", return_value=zot_inst),
            patch(_TARGET_POST) as post,
        ):
            n = sas.push_projection(
                "p", cfg, "key", "http://x", tmp_path, dry_run=True
            )
        assert n == 1
        post.assert_not_called()
        assert zot_inst.file.call_count == 0

    def test_real_run_imports_each_apkg(self, tmp_path: Path) -> None:
        cfg = {"zotero": {"library_id": "1", "tag": "fox"}, "push_anki": True}
        fake_item = {"key": "ITEM", "data": {"citationKey": "bishop2024"}}
        fake_att = _att("ATT", "bishop2024-20260201T1200-abc123.apkg")
        zot_inst = MagicMock()
        zot_inst.items.return_value = [fake_item]
        zot_inst.children.return_value = [fake_att]
        zot_inst.file.return_value = b"fake apkg bytes"
        mock_resp = MagicMock()
        mock_resp.json.return_value = {"result": True, "error": None}
        with (
            patch("swanki_anki_sync.zotero.Zotero", return_value=zot_inst),
            patch(_TARGET_POST, return_value=mock_resp) as post,
        ):
            n = sas.push_projection(
                "p", cfg, "key", "http://x", tmp_path, dry_run=False
            )
        assert n == 1
        staged = tmp_path / "p" / "bishop2024-20260201T1200-abc123.apkg"
        assert staged.exists()
        assert staged.read_bytes() == b"fake apkg bytes"
        body = post.call_args.kwargs["json"]
        assert body["action"] == "importPackage"
        assert body["params"]["path"] == str(staged.resolve())

    def test_skip_and_report_on_stale_attachment(self, tmp_path: Path) -> None:
        cfg = {"zotero": {"library_id": "1", "tag": "fox"}, "push_anki": True}
        fake_item = {"key": "ITEM", "data": {"citationKey": "bishop2024"}}
        fake_att = _att("ATT", "bishop2024-20260201T1200-abc123.apkg")
        zot_inst = MagicMock()
        zot_inst.items.return_value = [fake_item]
        zot_inst.children.return_value = [fake_att]
        zot_inst.file.side_effect = RuntimeError("attachment missing")
        with (
            patch("swanki_anki_sync.zotero.Zotero", return_value=zot_inst),
            patch(_TARGET_POST) as post,
        ):
            n = sas.push_projection(
                "p", cfg, "key", "http://x", tmp_path, dry_run=False
            )
        # Stale -> skipped, no importPackage POST.
        assert n == 0
        post.assert_not_called()
