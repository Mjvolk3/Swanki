"""
swanki/delivery/targets/abs.py
[[swanki.delivery.targets.abs]]
https://github.com/Mjvolk3/Swanki/tree/main/swanki/delivery/targets/abs.py
Test file: tests/test_delivery_abs.py

ABS SyncTarget: refresh the audiobookshelf state from Zotero. The 7-step
refresh (``swanki.abs.refresh.full_refresh``) is a library-wide operation, so
it is debounced: per job the orchestrator only records the ABS leg as
``deferred``, and the queue drainer fires one refresh after the pending queue
empties. The refresh uses a blocking lock (``wait=True``) so a contended
drain never silently skips, unlike the cron path's non-blocking mode.

Thin adapter by design: delivery is a consumer of ABS capability, not the
owner of its internals -- the cron shim, SLURM finalizer, and interactive use
call the same ``swanki.abs`` API without delivery in the loop.
"""

import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class AbsTarget:
    """Run the in-package ABS full refresh to land audio on the ABS server."""

    name = "abs"

    def __init__(self, repo_dir: Path | None = None, *, wait: bool = True) -> None:
        """Keep the historical signature; ``repo_dir`` is no longer used."""
        self.repo_dir = repo_dir
        self.wait = wait

    def refresh(self, *, dry_run: bool = False) -> bool:
        """Run the ABS refresh once.

        Args:
            dry_run: When true, log the call and run nothing.

        Returns:
            True on a successful refresh.
        """
        if dry_run:
            print(f"  [dry-run] abs: would run full_refresh(wait={self.wait})")
            return True
        from swanki.abs.refresh import full_refresh

        logger.info("AbsTarget: full_refresh(wait=%s)", self.wait)
        full_refresh(wait=self.wait)
        print("  abs: refresh complete")
        return True
