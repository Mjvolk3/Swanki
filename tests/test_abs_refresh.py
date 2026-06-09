"""
tests/test_abs_refresh.py
[[tests.test_abs_refresh]]
https://github.com/Mjvolk3/Swanki/tree/main/tests/test_abs_refresh.py
Test file: tests/test_abs_refresh.py

Tests for swanki/abs/refresh.py -- both lock modes on the shared lock file,
newest-local-mp3 selection, and the targeted refresh end-to-end against a
fixture tree + mocked transport (multi-projection fan-out, push_audio=false
skip, scan + verify + per-item chapter fix-up).
"""

import fcntl
import json
from pathlib import Path

import httpx
import pytest

from swanki.abs import refresh as refresh_mod
from swanki.abs.client import ABSClient
from swanki.abs.refresh import (
    _acquire_lock,
    _newest_local_mp3s,
    full_refresh,
    targeted_refresh,
)

NEW = "hamming_CH02_foundations-lecture-20260609T1132-7f7e8e4.mp3"
OLD = "hamming_CH02_foundations-lecture-20260514T1010-7d23dec.mp3"


def test_lock_nonblocking_skips_while_held(tmp_path, monkeypatch):
    lock_file = str(tmp_path / "abs-refresh.lock")
    monkeypatch.setattr(refresh_mod, "LOCK_FILE", lock_file)

    holder = open(lock_file, "w")
    fcntl.flock(holder, fcntl.LOCK_EX)
    # Contended non-blocking acquisition returns None...
    assert _acquire_lock(wait=False) is None
    # ...and full_refresh(wait=False) skips without running any step.
    assert full_refresh(wait=False) is False

    fcntl.flock(holder, fcntl.LOCK_UN)
    holder.close()
    fh = _acquire_lock(wait=False)
    assert fh is not None
    fh.close()


def test_lock_blocking_proceeds_after_release(tmp_path, monkeypatch):
    lock_file = str(tmp_path / "abs-refresh.lock")
    monkeypatch.setattr(refresh_mod, "LOCK_FILE", lock_file)
    fh = _acquire_lock(wait=True)
    assert fh is not None
    fh.close()


def test_newest_local_mp3s_picks_latest_ts(tmp_path):
    (tmp_path / OLD).write_bytes(b"old")
    (tmp_path / NEW).write_bytes(b"new")
    (tmp_path / "other_key-lecture-20260609T1132-abc.mp3").write_bytes(b"x")
    picked = _newest_local_mp3s(tmp_path, "hamming_CH02_foundations")
    assert [p.name for p in picked] == [NEW]


# -- targeted refresh end-to-end --------------------------------------------------


def _projections_yml(tmp_path: Path) -> Path:
    yml = tmp_path / "projections.yml"
    yml.write_text(
        "projections:\n"
        "  mv-ll:\n"
        "    audiotypes: [lecture]\n"
        "    zotero: {library_id: 1}\n"
        "  mirror:\n"
        "    audiotypes: [lecture]\n"
        "    zotero: {library_id: 2}\n"
        "  off:\n"
        "    audiotypes: [lecture]\n"
        "    push_audio: false\n"
        "    zotero: {library_id: 3}\n"
    )
    return yml


def _abs_tree(tmp_path: Path) -> Path:
    root = tmp_path / "Swanki_ABS"
    for proj in ("mv-ll", "mirror", "off"):
        d = root / proj / "Swanki-Book-Lecture" / "hamming"
        d.mkdir(parents=True)
        (d / OLD).write_bytes(b"old")
    return root


def _abs_client(posted_chapters: list, scanned: list) -> ABSClient:
    libs = {
        "libraries": [
            {"id": "L1", "folders": [
                {"fullPath": "/audiobooks/mv-ll/Swanki-Book-Lecture"}]},
            {"id": "L2", "folders": [
                {"fullPath": "/audiobooks/mirror/Swanki-Book-Lecture"}]},
            {"id": "L3", "folders": [
                {"fullPath": "/audiobooks/off/Swanki-Book-Lecture"}]},
        ]
    }
    item = {
        "id": "I1",
        "media": {
            "metadata": {"title": "hamming"},
            "audioFiles": [
                {"index": 1, "duration": 100.0, "metadata": {"filename": NEW}}
            ],
            "chapters": [{"title": "stale", "start": 0.0, "end": 90.0}],
        },
    }

    def handler(request: httpx.Request) -> httpx.Response:
        path = request.url.path
        if path == "/api/libraries":
            return httpx.Response(200, json=libs)
        if path.endswith("/scan"):
            scanned.append(path.split("/")[3])
            return httpx.Response(200)
        if "/items" in path and "/api/libraries/" in path:
            return httpx.Response(200, json={"results": [item]})
        if path.startswith("/api/items/") and path.endswith("/chapters"):
            posted_chapters.append(json.loads(request.content))
            return httpx.Response(200, json={})
        if path.startswith("/api/items/"):
            return httpx.Response(200, json=item)
        return httpx.Response(404)

    return ABSClient(
        base_url="https://abs.test",
        token="tok",
        transport=httpx.MockTransport(handler),
    )


def test_targeted_refresh_fans_out_scans_and_fixes(tmp_path, monkeypatch):
    monkeypatch.setattr(refresh_mod, "LOCK_FILE", str(tmp_path / "lock"))
    yml = _projections_yml(tmp_path)
    root = _abs_tree(tmp_path)
    out = tmp_path / "out"
    out.mkdir()
    (out / NEW).write_bytes(b"new-audio")

    posted: list = []
    scanned: list = []
    result = targeted_refresh(
        citation_key="hamming_CH02_foundations",
        output_dir=out,
        projections_path=yml,
        abs_root=root,
        client=_abs_client(posted, scanned),
        sleep=lambda _s: None,
    )

    # Dropped into BOTH push_audio projections; the disabled one untouched.
    dropped_projs = {Path(p).parts[-4] for p in result.dropped}
    assert dropped_projs == {"mv-ll", "mirror"}
    assert not (root / "off" / "Swanki-Book-Lecture" / "hamming" / NEW).exists()
    # Stale same-(key, type) file replaced on disk.
    for proj in ("mv-ll", "mirror"):
        names = [
            p.name
            for p in (root / proj / "Swanki-Book-Lecture" / "hamming").glob("*.mp3")
        ]
        assert names == [NEW]
    # Only the two affected libraries scanned; chapters fixed per item.
    assert sorted(result.scanned_libraries) == ["L1", "L2"]
    assert sorted(scanned) == ["L1", "L2"]
    assert len(result.chapters_fixed) == 2
    assert posted[0]["chapters"][0]["title"] == "hamming_CH02_foundations"


def test_targeted_refresh_requires_existing_group_dir(tmp_path, monkeypatch):
    monkeypatch.setattr(refresh_mod, "LOCK_FILE", str(tmp_path / "lock"))
    yml = _projections_yml(tmp_path)
    root = tmp_path / "empty_root"
    root.mkdir()
    out = tmp_path / "out"
    out.mkdir()
    (out / NEW).write_bytes(b"new-audio")

    with pytest.raises(FileNotFoundError, match="full refresh"):
        targeted_refresh(
            citation_key="hamming_CH02_foundations",
            output_dir=out,
            projections_path=yml,
            abs_root=root,
            client=_abs_client([], []),
            sleep=lambda _s: None,
        )
