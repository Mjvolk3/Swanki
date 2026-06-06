"""
tests/test_delivery_anki.py
[[tests.test_delivery_anki]]
https://github.com/Mjvolk3/Swanki/tree/main/tests/test_delivery_anki.py

Unit tests for the canonical AnkiConnect client + per-item AnkiTarget
(``swanki/delivery/targets/anki.py``). Migrated from the AnkiConnect-primitive
tests in test_swanki_anki_sync.py. Mocks ``requests.post``; no live network.
"""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from swanki.delivery.targets.anki import (
    AnkiTarget,
    ankiconnect_call,
    verify_ankiconnect,
)

_POST = "swanki.delivery.targets.anki.requests.post"


class TestAnkiConnectCall:
    def test_returns_result_field(self) -> None:
        mock_resp = MagicMock()
        mock_resp.json.return_value = {"result": True, "error": None}
        with patch(_POST, return_value=mock_resp):
            assert ankiconnect_call("http://x", "importPackage", {"path": "a"}) is True

    def test_raises_on_action_error(self) -> None:
        mock_resp = MagicMock()
        mock_resp.json.return_value = {"result": None, "error": "deck missing"}
        with patch(_POST, return_value=mock_resp):
            with pytest.raises(RuntimeError, match="deck missing"):
                ankiconnect_call("http://x", "importPackage", {"path": "a"})

    def test_posts_correct_body_shape(self) -> None:
        mock_resp = MagicMock()
        mock_resp.json.return_value = {"result": None, "error": None}
        with patch(_POST, return_value=mock_resp) as post:
            ankiconnect_call("http://x", "sync")
        body = post.call_args.kwargs["json"]
        assert body == {"action": "sync", "version": 6, "params": {}}


class TestVerifyAnkiConnect:
    def test_accepts_min_version(self) -> None:
        with patch("swanki.delivery.targets.anki.ankiconnect_call", return_value=6):
            assert verify_ankiconnect("http://x") == 6

    def test_rejects_below_min_version(self) -> None:
        with patch("swanki.delivery.targets.anki.ankiconnect_call", return_value=5):
            with pytest.raises(AssertionError, match="below minimum"):
                verify_ankiconnect("http://x")


class TestAnkiTarget:
    def test_no_apkgs_skips(self) -> None:
        with patch(_POST) as post:
            assert AnkiTarget("http://x").push([]) == 0
        post.assert_not_called()

    def test_dry_run_posts_nothing(self, tmp_path: Path) -> None:
        apkg = tmp_path / "a.apkg"
        apkg.write_bytes(b"x")
        with patch(_POST) as post:
            assert AnkiTarget("http://x").push([apkg], dry_run=True) == 1
        post.assert_not_called()

    def test_imports_each_then_one_sync(self, tmp_path: Path) -> None:
        apkgs = [tmp_path / "a.apkg", tmp_path / "b.apkg"]
        for a in apkgs:
            a.write_bytes(b"x")
        mock_resp = MagicMock()
        mock_resp.json.return_value = {"result": True, "error": None}
        # First call (version) returns 6, rest return True.
        with patch(_POST, return_value=mock_resp) as post:
            mock_resp.json.side_effect = [
                {"result": 6, "error": None},  # version
                {"result": True, "error": None},  # import a
                {"result": True, "error": None},  # import b
                {"result": None, "error": None},  # sync
            ]
            n = AnkiTarget("http://x").push(apkgs)
        assert n == 2
        actions = [c.kwargs["json"]["action"] for c in post.call_args_list]
        assert actions == ["version", "importPackage", "importPackage", "sync"]
        # importPackage params must be ONLY {path}: the headless Anki build
        # rejects a deleteExisting kwarg. Guards against reintroducing it.
        import_calls = [
            c for c in post.call_args_list
            if c.kwargs["json"]["action"] == "importPackage"
        ]
        for c in import_calls:
            assert set(c.kwargs["json"]["params"]) == {"path"}

    def test_no_sync_when_disabled(self, tmp_path: Path) -> None:
        apkg = tmp_path / "a.apkg"
        apkg.write_bytes(b"x")
        mock_resp = MagicMock()
        with patch(_POST, return_value=mock_resp) as post:
            mock_resp.json.side_effect = [
                {"result": 6, "error": None},
                {"result": True, "error": None},
            ]
            AnkiTarget("http://x", sync_after=False).push([apkg])
        actions = [c.kwargs["json"]["action"] for c in post.call_args_list]
        assert "sync" not in actions
