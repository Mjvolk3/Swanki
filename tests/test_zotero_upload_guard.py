"""
tests/test_zotero_upload_guard.py
[[tests.test_zotero_upload_guard]]
https://github.com/Mjvolk3/Swanki/tree/main/tests/test_zotero_upload_guard.py

Guard against the silent-upload-failure data-loss trap: pyzotero's
``attachment_simple`` returns ``{'success','failure','unchanged'}`` and does NOT
raise when the S3 upload fails. ``sync_to_zotero`` must inspect that return and
fail fast on a no-success result, so the prune step never deletes the prior good
zips (observed with pyzotero 1.11.0 silently failing every upload, leaving the
Zotero item with zero artifacts).
"""

from pathlib import Path
from unittest.mock import MagicMock

import pytest

import swanki.sync.zotero as zmod
from swanki.sync.zotero import sync_to_zotero


def _prep(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, result: dict[str, object]
) -> MagicMock:
    monkeypatch.setenv("ZOTERO_API_KEY", "k")
    monkeypatch.setenv("ZOTERO_LIBRARY_ID", "1")
    (tmp_path / "bookX-reading-audio.mp3").write_bytes(b"audio")
    zot = MagicMock()
    zot.attachment_simple.return_value = result
    monkeypatch.setattr(zmod, "make_zotero_client", lambda *a, **k: zot)
    monkeypatch.setattr(zmod, "_find_zotero_item", lambda *a, **k: "ITEM")
    return zot


def test_no_success_raises_and_does_not_prune(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    zot = _prep(
        monkeypatch, tmp_path,
        {"success": [], "failure": [{"title": "bookX.zip"}], "unchanged": []},
    )
    with pytest.raises(AssertionError, match="reported no success"):
        sync_to_zotero("bookX", tmp_path, "bookX", content_key="bookX")
    # The prune must NOT run on a failed upload -- prior attachments survive.
    zot.delete_item.assert_not_called()


def test_success_result_proceeds_to_prune(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    zot = _prep(monkeypatch, tmp_path, {"success": ["NEWKEY"], "failure": [], "unchanged": []})
    monkeypatch.setattr(zmod, "_prune_prior_attachments", lambda *a, **k: 0)
    monkeypatch.setattr(zmod, "_find_or_create_sync_note", lambda *a, **k: ({"data": {"note": ""}}, ""))
    # Reaches prune + note update without raising; no assertion on the upload.
    sync_to_zotero("bookX", tmp_path, "bookX", content_key="bookX")
    zot.attachment_simple.assert_called_once()
