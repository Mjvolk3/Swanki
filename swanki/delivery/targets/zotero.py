"""
swanki/delivery/targets/zotero.py
[[swanki.delivery.targets.zotero]]
https://github.com/Mjvolk3/Swanki/tree/main/swanki/delivery/targets/zotero.py
Test file: tests/test_delivery_orchestrator.py

Zotero SyncTarget: the backup / provenance sink. Wraps ``sync_to_zotero`` so
the delivery orchestrator can run it first in the Zotero -> Anki -> ABS order.
``sync_to_zotero`` stays the sole writer of the fox tag and the sole embedder
of the git commit hash; this target only sequences the call.
"""

import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class ZoteroBackupTarget:
    """Upload the run's artifacts to Zotero as the versioned backup."""

    name = "zotero"

    def __init__(
        self,
        citation_key: str,
        output_dir: Path,
        audio_prefix: str,
        content_key: str,
        merge_tracks: set[str] | str | None = None,
    ) -> None:
        """Capture the lookup key + output dir to upload from.

        Args:
            citation_key: BibTeX key for the Zotero item lookup.
            output_dir: Pipeline output dir to upload from.
            audio_prefix: Audio file prefix passed to ``sync_to_zotero``.
            content_key: Content key naming the artifact files.
            merge_tracks: forwarded to ``sync_to_zotero`` — ``None`` full
                replace, a track subset, or ``"auto"`` to merge only the tracks
                present in ``output_dir`` (see that function).
        """
        self.citation_key = citation_key
        self.output_dir = output_dir
        self.audio_prefix = audio_prefix
        self.content_key = content_key
        self.merge_tracks = merge_tracks

    def push(self, *, dry_run: bool = False) -> bool:
        """Upload to Zotero (no-op log in dry-run).

        Returns:
            True once the upload call returns (it tags the parent item and
            prunes prior versions internally).
        """
        if dry_run:
            mode = "merge" if self.merge_tracks is not None else "full-replace"
            print(
                f"  [dry-run] zotero: would sync_to_zotero({self.citation_key}, "
                f"{mode}={self.merge_tracks if self.merge_tracks is not None else ''})"
            )
            return True
        from swanki.sync.zotero import sync_to_zotero

        sync_to_zotero(
            citation_key=self.citation_key,
            output_dir=self.output_dir,
            audio_prefix=self.audio_prefix,
            content_key=self.content_key,
            merge_tracks=self.merge_tracks,
        )
        return True
