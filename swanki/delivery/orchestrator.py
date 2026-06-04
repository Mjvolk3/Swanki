"""
swanki/delivery/orchestrator.py
[[swanki.delivery.orchestrator]]
https://github.com/Mjvolk3/Swanki/tree/main/swanki/delivery/orchestrator.py
Test file: tests/test_delivery_orchestrator.py

The delivery orchestrator: run the enabled targets in the fixed
Zotero -> Anki -> ABS order, recording a per-target marker after each success
so a crashed re-drain resumes from the first unmarked target. ABS is debounced
-- per job it is only marked ``deferred`` (the queue fires one refresh after
the pending queue empties), so a job is "delivered" once Zotero and Anki land.
"""

import logging
from dataclasses import dataclass, field
from pathlib import Path

from swanki.delivery.markers import (
    STATUS_DEFERRED,
    TARGET_ORDER,
    DeliveryMarkers,
)
from swanki.delivery.source import LocalSource, SyncSource, ZoteroSource
from swanki.delivery.targets.anki import AnkiTarget
from swanki.delivery.targets.zotero import ZoteroBackupTarget

logger = logging.getLogger(__name__)


@dataclass
class DeliveryResult:
    """Outcome of a ``deliver`` call."""

    markers: DeliveryMarkers
    enabled: list[str]
    abs_deferred: bool = False
    ran: list[str] = field(default_factory=list)

    @property
    def delivered(self) -> bool:
        """True when every non-deferred enabled target is ``done``.

        ABS, when deferred, is excluded -- the queue confirms it via the
        once-at-drain refresh, not per job.
        """
        required = [t for t in self.enabled if not (t == "abs" and self.abs_deferred)]
        return self.markers.all_done(required)


def build_source(
    kind: str, output_dir: Path, stage_dir: Path | None = None
) -> SyncSource:
    """Construct the configured SyncSource.

    Args:
        kind: ``local`` or ``zotero``.
        output_dir: Pipeline output dir (used by ``local``).
        stage_dir: Download staging dir (used by ``zotero``); defaults to a
            ``.delivery-stage`` subdir of ``output_dir``.

    Returns:
        A ``LocalSource`` or ``ZoteroSource``.
    """
    if kind == "local":
        return LocalSource(output_dir)
    if kind == "zotero":
        return ZoteroSource(stage_dir or output_dir / ".delivery-stage")
    raise ValueError(f"unknown delivery source: {kind!r}")


def deliver(
    *,
    citation_key: str,
    content_key: str,
    output_dir: Path,
    audio_prefix: str,
    source_kind: str = "local",
    enabled: list[str] | None = None,
    defer_abs: bool = True,
    dry_run: bool = False,
) -> DeliveryResult:
    """Deliver one job's artifacts to the enabled targets in order.

    Targets run in ``TARGET_ORDER`` (Zotero -> Anki -> ABS). Each success is
    recorded in ``.delivery.json``; an already-done target is skipped so a
    re-drain resumes mid-delivery. A target failure raises (fail-fast) with the
    markers showing exactly how far delivery got.

    Args:
        citation_key: BibTeX key for the Zotero item.
        content_key: Content key naming the artifact files (defaults to key).
        output_dir: The pipeline output dir for this job.
        audio_prefix: Audio file prefix (passed to the Zotero backup).
        source_kind: ``local`` (default) or ``zotero``.
        enabled: Target names to run; defaults to all of ``TARGET_ORDER``.
        defer_abs: When true (default), ABS is only marked ``deferred`` here;
            the queue runs the actual refresh once at drain end.
        dry_run: Plan only; no uploads, imports, or refreshes.

    Returns:
        A ``DeliveryResult``.
    """
    enabled = enabled if enabled is not None else list(TARGET_ORDER)
    markers = DeliveryMarkers.load(output_dir)
    source = build_source(source_kind, output_dir)
    result = DeliveryResult(markers=markers, enabled=enabled)

    for target in TARGET_ORDER:
        if target not in enabled or markers.is_done(target):
            continue

        if target == "zotero":
            ZoteroBackupTarget(
                citation_key, output_dir, audio_prefix, content_key
            ).push(dry_run=dry_run)
            if not dry_run:
                markers.mark("zotero")
            result.ran.append("zotero")

        elif target == "anki":
            artifacts = source.resolve(citation_key, content_key)
            AnkiTarget().push(list(artifacts.apkgs), dry_run=dry_run)
            if not dry_run:
                markers.mark("anki")
            result.ran.append("anki")

        elif target == "abs":
            if defer_abs:
                if not dry_run:
                    markers.mark("abs", STATUS_DEFERRED)
                result.abs_deferred = True
            else:
                from swanki.delivery.targets.abs import AbsTarget

                AbsTarget(_repo_dir()).refresh(dry_run=dry_run)
                if not dry_run:
                    markers.mark("abs")
                result.ran.append("abs")

    return result


def _repo_dir() -> Path:
    """Swanki repo root (this file is ``<repo>/swanki/delivery/orchestrator.py``)."""
    return Path(__file__).resolve().parents[2]
