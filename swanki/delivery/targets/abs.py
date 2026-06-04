"""
swanki/delivery/targets/abs.py
[[swanki.delivery.targets.abs]]
https://github.com/Mjvolk3/Swanki/tree/main/swanki/delivery/targets/abs.py
Test file: tests/test_delivery_abs.py

ABS SyncTarget: refresh the audiobookshelf state from Zotero. The 7-step
refresh (``scripts/abs_refresh.sh`` -> ``swanki_abs_sync.py`` + collection
mirror + metadata + stale clean + chapter titles + library scan) is a
library-wide operation, so it is debounced: per job the orchestrator only
records the ABS leg as ``deferred``, and the queue drainer fires one refresh
after the pending queue empties. The refresh uses a blocking lock (``--wait``)
so a contended drain never silently skips, unlike the cron path's ``-n``.
"""

import logging
import subprocess
from pathlib import Path

logger = logging.getLogger(__name__)


class AbsTarget:
    """Run ``scripts/abs_refresh.sh`` to land audio on the ABS server."""

    name = "abs"

    def __init__(self, repo_dir: Path, *, wait: bool = True) -> None:
        """Store the repo dir holding ``scripts/abs_refresh.sh`` and lock mode."""
        self.repo_dir = repo_dir
        self.wait = wait

    @property
    def script(self) -> Path:
        """Path to ``scripts/abs_refresh.sh`` under the repo dir."""
        return self.repo_dir / "scripts" / "abs_refresh.sh"

    def refresh(self, *, dry_run: bool = False) -> bool:
        """Run the ABS refresh once.

        Args:
            dry_run: When true, log the command and run nothing.

        Returns:
            True on a successful refresh.

        Raises:
            FileNotFoundError: if ``abs_refresh.sh`` is absent.
            subprocess.CalledProcessError: if the refresh exits non-zero.
        """
        cmd = ["bash", str(self.script)]
        if self.wait:
            cmd.append("--wait")
        if dry_run:
            print(f"  [dry-run] abs: would run {' '.join(cmd)}")
            return True
        if not self.script.is_file():
            raise FileNotFoundError(f"abs_refresh.sh not found: {self.script}")
        logger.info("AbsTarget: %s", " ".join(cmd))
        subprocess.run(cmd, cwd=self.repo_dir, check=True)
        print("  abs: refresh complete")
        return True
