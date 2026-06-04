"""
tests/test_delivery_markers.py
[[tests.test_delivery_markers]]
https://github.com/Mjvolk3/Swanki/tree/main/tests/test_delivery_markers.py

Unit tests for ``.delivery.json`` markers (``swanki/delivery/markers.py``):
round-trip persistence and the resume-on-redrain query surface.
"""

from pathlib import Path

from swanki.delivery.markers import (
    MARKER_FILENAME,
    STATUS_DEFERRED,
    DeliveryMarkers,
)


class TestDeliveryMarkers:
    def test_mark_persists_to_disk(self, tmp_path: Path) -> None:
        m = DeliveryMarkers.load(tmp_path)
        m.mark("zotero", when="2026-06-04T10:00:00")
        assert (tmp_path / MARKER_FILENAME).is_file()
        reloaded = DeliveryMarkers.load(tmp_path)
        assert reloaded.is_done("zotero")
        assert reloaded.data["zotero"]["at"] == "2026-06-04T10:00:00"

    def test_round_trip_multiple_targets(self, tmp_path: Path) -> None:
        m = DeliveryMarkers.load(tmp_path)
        m.mark("zotero", when="t1")
        m.mark("anki", when="t2")
        m.mark("abs", STATUS_DEFERRED, when="t3")
        reloaded = DeliveryMarkers.load(tmp_path)
        assert reloaded.is_done("zotero")
        assert reloaded.is_done("anki")
        assert not reloaded.is_done("abs")  # deferred != done
        assert reloaded.data["abs"]["status"] == STATUS_DEFERRED

    def test_all_done(self, tmp_path: Path) -> None:
        m = DeliveryMarkers.load(tmp_path)
        m.mark("zotero", when="t")
        assert not m.all_done(["zotero", "anki"])
        m.mark("anki", when="t")
        assert m.all_done(["zotero", "anki"])

    def test_resume_skips_done_targets(self, tmp_path: Path) -> None:
        # Simulate a crash after zotero: the marker survives, redrain resumes.
        DeliveryMarkers.load(tmp_path).mark("zotero", when="t")
        resumed = DeliveryMarkers.load(tmp_path)
        assert resumed.is_done("zotero")
        assert not resumed.is_done("anki")

    def test_empty_when_no_file(self, tmp_path: Path) -> None:
        m = DeliveryMarkers.load(tmp_path)
        assert m.data == {}
        assert not m.is_done("zotero")
