"""
tests/test_zotero_upload_guard.py
[[tests.test_zotero_upload_guard]]
https://github.com/Mjvolk3/Swanki/tree/main/tests/test_zotero_upload_guard.py

Guard against the silent-upload-failure data-loss trap. ``sync_to_zotero`` now
uploads via the low-level ``upload_attachment`` four-step flow (create -> auth ->
S3 -> register) instead of pyzotero's ``attachment_simple`` (1.11.0 returned a
failure dict without raising, even on a 5-byte file). ``upload_attachment``
RAISES on any bad HTTP status, so the prune step never deletes the prior good
zips on a failed upload. These tests drive the flow by monkeypatching
``httpx.get``/``httpx.post`` with an ordered chain of fake responses.
"""

from pathlib import Path
from unittest.mock import MagicMock

import httpx
import pytest

import swanki.sync.zotero as zmod
from swanki.sync.zotero import sync_to_zotero


class _FakeResponse:
    """Minimal stand-in for ``httpx.Response`` (status_code + ``.json()``)."""

    def __init__(
        self, status_code: int, json_data: object = None, text: str = ""
    ) -> None:
        self.status_code = status_code
        self._json = json_data if json_data is not None else {}
        self.text = text

    def json(self) -> object:
        return self._json


def _prep(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> MagicMock:
    """Env + a MagicMock zot with the attrs upload_attachment reads.

    Routes prune/note/tag through the mock zot by patching
    ``make_zotero_client`` + ``_find_zotero_item``. A planted prior attachment
    makes ``_prune_prior_attachments`` call ``zot.delete_item`` on success.
    """
    monkeypatch.setenv("ZOTERO_API_KEY", "k")
    monkeypatch.setenv("ZOTERO_LIBRARY_ID", "1")
    (tmp_path / "bookX-reading-audio.mp3").write_bytes(b"audio")
    zot = MagicMock()
    zot.endpoint = "https://api.zotero.org"
    zot.library_type = "users"
    zot.library_id = "1"
    zot.api_key = "k"
    # Prior attachment sharing the chapter base -> prune deletes it on success.
    zot.children.return_value = [
        {
            "key": "OLD",
            "data": {"itemType": "attachment", "filename": "bookX-prior.zip"},
        }
    ]
    monkeypatch.setattr(zmod, "make_zotero_client", lambda *a, **k: zot)
    monkeypatch.setattr(zmod, "_find_zotero_item", lambda *a, **k: "ITEM")
    return zot


def _template_get() -> MagicMock:
    """Fake ``httpx.get`` returning the attachment template."""
    return MagicMock(
        side_effect=[
            _FakeResponse(
                200, {"itemType": "attachment", "linkMode": "imported_file"}
            )
        ]
    )


def test_success_flow_reaches_prune_note_tag(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """Full 4-step success -> prune (delete_item) + note + tag all reached."""
    zot = _prep(monkeypatch, tmp_path)
    monkeypatch.setattr(httpx, "get", _template_get())
    post = MagicMock(
        side_effect=[
            _FakeResponse(200, {"success": {"0": "NEWKEY"}}),  # create
            _FakeResponse(  # auth
                200,
                {
                    "url": "https://s3.example/upload",
                    "contentType": "application/octet-stream",
                    "prefix": "PRE",
                    "suffix": "SUF",
                    "uploadKey": "UP",
                },
            ),
            _FakeResponse(201),  # s3
            _FakeResponse(204),  # register
        ]
    )
    monkeypatch.setattr(httpx, "post", post)

    sync_to_zotero("bookX", tmp_path, "bookX", content_key="bookX")

    assert post.call_count == 4
    zot.delete_item.assert_called_once()  # prune reached
    zot.update_item.assert_called_once()  # sync-log note reached
    zot.add_tags.assert_called_once()  # fox tag reached


def test_register_failure_raises_and_does_not_prune(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """A non-204 register RAISES and never reaches the prune (no data loss)."""
    zot = _prep(monkeypatch, tmp_path)
    monkeypatch.setattr(httpx, "get", _template_get())
    post = MagicMock(
        side_effect=[
            _FakeResponse(200, {"success": {"0": "NEWKEY"}}),  # create
            _FakeResponse(  # auth
                200,
                {
                    "url": "https://s3.example/upload",
                    "contentType": "application/octet-stream",
                    "prefix": "PRE",
                    "suffix": "SUF",
                    "uploadKey": "UP",
                },
            ),
            _FakeResponse(201),  # s3
            _FakeResponse(500, text="boom"),  # register fails
        ]
    )
    monkeypatch.setattr(httpx, "post", post)

    with pytest.raises(RuntimeError, match="register-upload failed"):
        sync_to_zotero("bookX", tmp_path, "bookX", content_key="bookX")

    zot.delete_item.assert_not_called()


def test_exists_short_circuits_before_s3(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """An identical md5 (``exists``) skips S3/register but still prunes+notes+tags."""
    zot = _prep(monkeypatch, tmp_path)
    monkeypatch.setattr(httpx, "get", _template_get())
    post = MagicMock(
        side_effect=[
            _FakeResponse(200, {"success": {"0": "NEWKEY"}}),  # create
            _FakeResponse(200, {"exists": True}),  # auth -> short-circuit
        ]
    )
    monkeypatch.setattr(httpx, "post", post)

    sync_to_zotero("bookX", tmp_path, "bookX", content_key="bookX")

    assert post.call_count == 2  # no S3, no register
    zot.delete_item.assert_called_once()  # prune still reached
    zot.update_item.assert_called_once()  # note still reached
    zot.add_tags.assert_called_once()  # tag still reached
