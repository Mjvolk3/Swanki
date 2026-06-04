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
        self, citation_key: str, output_dir: Path, audio_prefix: str, content_key: str
    ) -> None:
        """Capture the lookup key + output dir to upload from."""
        self.citation_key = citation_key
        self.output_dir = output_dir
        self.audio_prefix = audio_prefix
        self.content_key = content_key

    def push(self, *, dry_run: bool = False) -> bool:
        """Upload to Zotero (no-op log in dry-run).

        Returns:
            True once the upload call returns (it tags the parent item and
            prunes prior versions internally).
        """
        if dry_run:
            print(f"  [dry-run] zotero: would sync_to_zotero({self.citation_key})")
            return True
        from swanki.sync.zotero import sync_to_zotero

        sync_to_zotero(
            citation_key=self.citation_key,
            output_dir=self.output_dir,
            audio_prefix=self.audio_prefix,
            content_key=self.content_key,
        )
        return True
