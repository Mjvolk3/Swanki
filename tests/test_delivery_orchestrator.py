"""
tests/test_delivery_orchestrator.py
[[tests.test_delivery_orchestrator]]
https://github.com/Mjvolk3/Swanki/tree/main/tests/test_delivery_orchestrator.py

Unit tests for the delivery orchestrator (``swanki/delivery/orchestrator.py``)
and its CLI. Targets are exercised through mocks / dry-run so no network,
AnkiConnect, or ABS refresh is touched.
"""

from pathlib import Path
from unittest.mock import patch

import pytest

from swanki.delivery.markers import DeliveryMarkers
from swanki.delivery.orchestrator import build_source, deliver


def _stage(output_dir: Path) -> None:
    """Drop one apkg so the local source resolves something for Anki."""
    (output_dir / "bishop2024.apkg").write_bytes(b"x")


class TestBuildSource:
    def test_local(self, tmp_path: Path) -> None:
        assert build_source("local", tmp_path).name == "local"

    def test_zotero(self, tmp_path: Path) -> None:
        assert build_source("zotero", tmp_path).name == "zotero"

    def test_unknown_raises(self, tmp_path: Path) -> None:
        with pytest.raises(ValueError, match="unknown delivery source"):
            build_source("nope", tmp_path)


class TestDeliver:
    def test_full_order_dry_run(self, tmp_path: Path) -> None:
        _stage(tmp_path)
        result = deliver(
            citation_key="bishop2024",
            content_key="bishop2024",
            output_dir=tmp_path,
            audio_prefix="bishop2024-fish",
            dry_run=True,
        )
        # zotero + anki ran (in order); abs deferred.
        assert result.ran == ["zotero", "anki"]
        assert result.abs_deferred is True
        # dry-run writes no markers.
        assert not (tmp_path / ".delivery.json").exists()

    def test_live_writes_markers_in_order(self, tmp_path: Path) -> None:
        _stage(tmp_path)
        with (
            patch(
                "swanki.delivery.targets.zotero.ZoteroBackupTarget.push",
                return_value=True,
            ),
            patch("swanki.delivery.targets.anki.AnkiTarget.push", return_value=1),
        ):
            result = deliver(
                citation_key="bishop2024",
                content_key="bishop2024",
                output_dir=tmp_path,
                audio_prefix="bishop2024-fish",
            )
        assert result.delivered is True  # abs deferred is excluded
        m = DeliveryMarkers.load(tmp_path)
        assert m.is_done("zotero")
        assert m.is_done("anki")
        assert not m.is_done("abs")  # deferred
        assert m.data["abs"]["status"] == "deferred"

    def test_resume_skips_already_done(self, tmp_path: Path) -> None:
        _stage(tmp_path)
        DeliveryMarkers.load(tmp_path).mark("zotero", when="t")
        with (
            patch(
                "swanki.delivery.targets.zotero.ZoteroBackupTarget.push"
            ) as zpush,
            patch("swanki.delivery.targets.anki.AnkiTarget.push", return_value=1),
        ):
            result = deliver(
                citation_key="bishop2024",
                content_key="bishop2024",
                output_dir=tmp_path,
                audio_prefix="bishop2024-fish",
            )
        zpush.assert_not_called()  # already done -> skipped
        assert "zotero" not in result.ran
        assert "anki" in result.ran

    def test_enabled_subset(self, tmp_path: Path) -> None:
        _stage(tmp_path)
        with patch(
            "swanki.delivery.targets.anki.AnkiTarget.push", return_value=1
        ) as apush:
            result = deliver(
                citation_key="bishop2024",
                content_key="bishop2024",
                output_dir=tmp_path,
                audio_prefix="bishop2024-fish",
                enabled=["anki"],
            )
        apush.assert_called_once()
        assert result.ran == ["anki"]
        assert result.delivered is True

    def test_zotero_failure_propagates_with_partial_markers(
        self, tmp_path: Path
    ) -> None:
        _stage(tmp_path)
        with patch(
            "swanki.delivery.targets.zotero.ZoteroBackupTarget.push",
            side_effect=RuntimeError("zotero 504"),
        ):
            with pytest.raises(RuntimeError, match="zotero 504"):
                deliver(
                    citation_key="bishop2024",
                    content_key="bishop2024",
                    output_dir=tmp_path,
                    audio_prefix="bishop2024-fish",
                )
        # No markers written -- nothing succeeded before the failure.
        assert not DeliveryMarkers.load(tmp_path).is_done("zotero")

    def test_run_abs_inline_dry_run(self, tmp_path: Path) -> None:
        _stage(tmp_path)
        result = deliver(
            citation_key="bishop2024",
            content_key="bishop2024",
            output_dir=tmp_path,
            audio_prefix="bishop2024-fish",
            defer_abs=False,
            dry_run=True,
        )
        assert result.ran == ["zotero", "anki", "abs"]
        assert result.abs_deferred is False
