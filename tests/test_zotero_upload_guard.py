"""
tests/test_zotero_upload_guard.py
[[tests.test_zotero_upload_guard]]
https://github.com/Mjvolk3/Swanki/tree/main/tests/test_zotero_upload_guard.py

Guard against two upload traps in ``sync_to_zotero``:

1. Silent-upload-failure data loss: ``Zupload.upload()`` returns
   ``{'success','failure','unchanged'}`` and does NOT raise when registration or
   the S3 upload fails. ``sync_to_zotero`` must inspect that return and fail fast
   on a no-success result, so the prune step never deletes the prior good zips.
2. The directory-path registration bug: pyzotero 1.11.0's ``attachment_simple``
   registers the attachment with ``filename`` set to the full path it was handed,
   and the Zotero API rejects that with 400 "Stored-file filename ... cannot
   contain a directory path" -- so every upload of an out-of-cwd file failed.
   ``sync_to_zotero`` must register a BARE filename and pass the directory as
   ``basedir``.
"""

from pathlib import Path
from unittest.mock import MagicMock

import pytest

import swanki.sync.zotero as zmod
from swanki.sync.zotero import sync_to_zotero


def _prep(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, result: dict[str, object]
) -> tuple[MagicMock, MagicMock]:
    monkeypatch.setenv("ZOTERO_API_KEY", "k")
    monkeypatch.setenv("ZOTERO_LIBRARY_ID", "1")
    (tmp_path / "bookX-reading-audio.mp3").write_bytes(b"audio")
    zot = MagicMock()
    zot._attachment_template.return_value = {}
    upload = MagicMock()
    upload.return_value.upload.return_value = result
    monkeypatch.setattr(zmod, "make_zotero_client", lambda *a, **k: zot)
    monkeypatch.setattr(zmod, "_find_zotero_item", lambda *a, **k: "ITEM")
    monkeypatch.setattr(zmod, "Zupload", upload)
    return zot, upload


def test_no_success_raises_and_does_not_prune(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    zot, _ = _prep(
        monkeypatch,
        tmp_path,
        {"success": [], "failure": [{"title": "bookX.zip"}], "unchanged": []},
    )
    with pytest.raises(AssertionError, match="reported no success"):
        sync_to_zotero("bookX", tmp_path, "bookX", content_key="bookX")
    # The prune must NOT run on a failed upload -- prior attachments survive.
    zot.delete_item.assert_not_called()


def test_success_result_proceeds_to_prune(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    _, upload = _prep(
        monkeypatch,
        tmp_path,
        {"success": ["NEWKEY"], "failure": [], "unchanged": []},
    )
    monkeypatch.setattr(zmod, "_prune_prior_attachments", lambda *a, **k: 0)
    monkeypatch.setattr(
        zmod, "_find_or_create_sync_note", lambda *a, **k: ({"data": {"note": ""}}, "")
    )
    # Reaches prune + note update without raising; no assertion on the upload.
    sync_to_zotero("bookX", tmp_path, "bookX", content_key="bookX")
    upload.return_value.upload.assert_called_once()


def test_registers_bare_filename_with_basedir(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """The Zotero API 400s on a ``filename`` containing a directory path."""
    _, upload = _prep(
        monkeypatch,
        tmp_path,
        {"success": ["NEWKEY"], "failure": [], "unchanged": []},
    )
    monkeypatch.setattr(zmod, "_prune_prior_attachments", lambda *a, **k: 0)
    monkeypatch.setattr(
        zmod, "_find_or_create_sync_note", lambda *a, **k: ({"data": {"note": ""}}, "")
    )
    sync_to_zotero("bookX", tmp_path, "bookX", content_key="bookX")

    template = upload.call_args[0][1][0]
    basedir = Path(upload.call_args[1]["basedir"])
    filename = template["filename"]
    # What the API sees must be a bare name, or it 400s.
    assert "/" not in filename, f"filename must be bare, got {filename!r}"
    # ...and the bytes must still be findable, so basedir carries the directory.
    # pyzotero's bug was leaving this at Path("."), which cannot locate the file.
    assert basedir != Path(), "basedir must be the file's real directory"
    assert basedir.is_absolute()
