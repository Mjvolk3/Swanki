"""
tests/test_zotero_merge.py
[[tests.test_zotero_merge]]
https://github.com/Mjvolk3/Swanki/tree/main/tests/test_zotero_merge.py

Unit tests for merge-aware Zotero delivery: a partial regen (e.g. an
audio-only lecture re-render) re-stamps only the regenerated tracks and
carries every other member of the current bundle forward verbatim, so the
Zotero backup stays additive instead of being wiped to the partial set.
"""

import io
import zipfile
from pathlib import Path
from unittest.mock import MagicMock, patch

from swanki.sync.zotero import (
    ALL_TRACKS,
    _load_existing_bundle,
    _member_track,
    sync_to_zotero,
)


def _bundle_bytes(names: list[str]) -> bytes:
    """Build an in-memory zip with the given member names (1-byte payloads)."""
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        for n in names:
            zf.writestr(n, b"x")
    return buf.getvalue()


class TestMemberTrack:
    def test_audio_members_classified_by_infix(self) -> None:
        assert _member_track("k-lecture-20260720T1314-abc123.mp3") == "lecture"
        assert _member_track("k-summary-20260709T2109-def456.mp3") == "summary"
        assert _member_track("k-reading-20260709T2109-def456.mp3") == "reading"

    def test_apkg_is_cards_regardless_of_stem(self) -> None:
        assert _member_track("k-20260709T2109-def456.apkg") == "cards"
        assert _member_track("k-problem-set-20260709T2109-def456.apkg") == "cards"

    def test_unknown_member_is_none(self) -> None:
        assert _member_track("k-notes.txt") is None

    def test_all_tracks_are_recognized(self) -> None:
        # Every track the packer emits must round-trip through the classifier.
        assert ALL_TRACKS == {"cards", "lecture", "summary", "reading"}


class TestLoadExistingBundle:
    def test_downloads_and_reads_newest_zip(self) -> None:
        zot = MagicMock()
        zot.everything.return_value = [
            {
                "key": "OLD",
                "data": {
                    "itemType": "attachment",
                    "filename": "k-20260709T2109-old.zip",
                },
            },
            {
                "key": "NEW",
                "data": {
                    "itemType": "attachment",
                    "filename": "k-20260720T1314-new.zip",
                },
            },
        ]
        zot.file.return_value = _bundle_bytes(
            ["k-lecture-20260720T1314-new.mp3", "k-summary-20260720T1314-new.mp3"]
        )
        members = _load_existing_bundle(zot, "ITEM", "k")
        # Picked the newest zip (by filename sort), not the old one.
        zot.file.assert_called_once_with("NEW")
        assert set(members) == {
            "k-lecture-20260720T1314-new.mp3",
            "k-summary-20260720T1314-new.mp3",
        }

    def test_legacy_bare_apkg_is_a_one_member_bundle(self) -> None:
        zot = MagicMock()
        zot.everything.return_value = [
            {
                "key": "APKG",
                "data": {
                    "itemType": "attachment",
                    "filename": "k-20260709T2109-old.apkg",
                },
            },
        ]
        zot.file.return_value = b"apkg-bytes"
        members = _load_existing_bundle(zot, "ITEM", "k")
        assert members == {"k-20260709T2109-old.apkg": b"apkg-bytes"}

    def test_no_prior_attachment_returns_none(self) -> None:
        zot = MagicMock()
        zot.everything.return_value = []
        assert _load_existing_bundle(zot, "ITEM", "k") is None


class TestSyncMergePath:
    def _run(self, tmp_path: Path, merge_tracks, existing, present_tracks):
        """Drive sync_to_zotero with a mocked client; return uploaded members."""
        out = tmp_path / "out"
        out.mkdir()
        # Canonical source files for the tracks present in the regen dir.
        names = {
            "lecture": "k-lecture-audio.mp3",
            "summary": "k-summary-audio.mp3",
            "reading": "k-reading-audio.mp3",
            "cards": "k.apkg",
        }
        for t in present_tracks:
            (out / names[t]).write_bytes(b"new")

        # Capture the uploaded members WHILE the tempdir zip still exists (it is
        # removed when sync_to_zotero's TemporaryDirectory context exits).
        captured: set[str] = set()

        def _capture(paths, parentid):  # noqa: ANN001
            with zipfile.ZipFile(paths[0]) as zf:
                captured.update(zf.namelist())

        zot = MagicMock()
        zot.attachment_simple.side_effect = _capture
        with (
            patch("swanki.sync.zotero.make_zotero_client", return_value=zot),
            patch("swanki.sync.zotero._find_zotero_item", return_value="ITEM"),
            patch("swanki.sync.zotero.with_zotero_retry", side_effect=lambda f: f()),
            patch("swanki.sync.zotero._git_short_hash", return_value="newsha"),
            patch("swanki.sync.zotero._prune_prior_attachments", return_value=0),
            patch(
                "swanki.sync.zotero._find_or_create_sync_note",
                return_value=({"data": {"note": ""}}, ""),
            ),
            patch.dict("os.environ", {"ZOTERO_API_KEY": "x", "ZOTERO_LIBRARY_ID": "1"}),
        ):
            if existing is not None:
                zot.everything.return_value = [
                    {
                        "key": "OLD",
                        "data": {
                            "itemType": "attachment",
                            "filename": "k-20260709T2109-old.zip",
                        },
                    },
                ]
                zot.file.return_value = _bundle_bytes(existing)
            else:
                zot.everything.return_value = []
            zot.item.return_value = {"data": {"tags": []}}
            sync_to_zotero(
                citation_key="k",
                output_dir=out,
                audio_prefix="k",
                merge_tracks=merge_tracks,
            )
        return captured

    def test_lecture_only_merge_preserves_other_tracks(self, tmp_path: Path) -> None:
        existing = [
            "k-lecture-20260709T2109-old.mp3",
            "k-summary-20260709T2109-old.mp3",
            "k-reading-20260709T2109-old.mp3",
            "k-20260709T2109-old.apkg",
        ]
        members = self._run(
            tmp_path,
            merge_tracks={"lecture"},
            existing=existing,
            present_tracks=["lecture"],
        )
        # Lecture re-stamped with the new sha; the other three carried verbatim.
        assert any(m.startswith("k-lecture-") and "newsha" in m for m in members)
        assert "k-summary-20260709T2109-old.mp3" in members
        assert "k-reading-20260709T2109-old.mp3" in members
        assert "k-20260709T2109-old.apkg" in members
        # Exactly one lecture member (no stale duplicate).
        assert sum(_member_track(m) == "lecture" for m in members) == 1

    def test_auto_infers_present_tracks(self, tmp_path: Path) -> None:
        existing = [
            "k-lecture-20260709T2109-old.mp3",
            "k-summary-20260709T2109-old.mp3",
        ]
        members = self._run(
            tmp_path,
            merge_tracks="auto",
            existing=existing,
            present_tracks=["lecture"],
        )
        assert any("newsha" in m and _member_track(m) == "lecture" for m in members)
        assert "k-summary-20260709T2109-old.mp3" in members

    def test_full_replace_ignores_existing_bundle(self, tmp_path: Path) -> None:
        # merge_tracks=None: only what is in the dir goes up; the old summary is
        # NOT carried, matching the historical wipe-and-replace contract.
        existing = ["k-summary-20260709T2109-old.mp3"]
        members = self._run(
            tmp_path,
            merge_tracks=None,
            existing=existing,
            present_tracks=["lecture"],
        )
        assert any(_member_track(m) == "lecture" for m in members)
        assert not any(_member_track(m) == "summary" for m in members)

    def test_merge_with_no_prior_bundle_packs_present(self, tmp_path: Path) -> None:
        # First-ever sync + auto: nothing to merge into, so pack what is present.
        members = self._run(
            tmp_path,
            merge_tracks="auto",
            existing=None,
            present_tracks=["lecture", "summary"],
        )
        assert {_member_track(m) for m in members} == {"lecture", "summary"}
