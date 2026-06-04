"""
swanki/delivery/markers.py
[[swanki.delivery.markers]]
https://github.com/Mjvolk3/Swanki/tree/main/swanki/delivery/markers.py
Test file: tests/test_delivery_markers.py

Per-target delivery markers, persisted as ``.delivery.json`` in a job's output
dir. They make queue DONE a verifiable state: a job is delivered only when each
enabled target has a success timestamp. After a crash mid-delivery a re-drain
reads the markers and resumes from the first unmarked target instead of
re-pushing everything.
"""

import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

MARKER_FILENAME = ".delivery.json"

# Delivery order. DONE means delivered in this sequence: the Zotero backup
# (source of truth) first, then the Anki server, then ABS.
TARGET_ORDER = ("zotero", "anki", "abs")

# An ABS leg that has been queued for the once-at-drain refresh but not yet
# confirmed by a completed refresh.
STATUS_DEFERRED = "deferred"


@dataclass
class DeliveryMarkers:
    """Read/write the ``.delivery.json`` marker map for one output dir.

    The on-disk shape is ``{"<target>": {"status": "...", "at": "<iso8601>"}}``.
    Mutations are written through immediately so a crash leaves an accurate
    record.
    """

    path: Path
    data: dict[str, dict[str, str]]

    @classmethod
    def load(cls, output_dir: Path) -> "DeliveryMarkers":
        """Load markers for ``output_dir``, or an empty set if none exist."""
        path = output_dir / MARKER_FILENAME
        data: dict[str, dict[str, str]] = {}
        if path.is_file():
            data = json.loads(path.read_text())
        return cls(path=path, data=data)

    def _write(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(
            json.dumps(self.data, indent=2, ensure_ascii=False)
        )

    def mark(self, target: str, status: str = "done", *, when: str | None = None) -> None:
        """Record a target's delivery status and persist immediately.

        Args:
            target: One of ``TARGET_ORDER``.
            status: ``"done"``, ``STATUS_DEFERRED``, or a failure marker.
            when: ISO-8601 timestamp; defaults to ``datetime.now``. Injectable
                so callers (and tests) stay deterministic.
        """
        stamp = when if when is not None else datetime.now().isoformat()
        self.data[target] = {"status": status, "at": stamp}
        self._write()

    def is_done(self, target: str) -> bool:
        """True when ``target`` has a recorded ``done`` status."""
        return self.data.get(target, {}).get("status") == "done"

    def all_done(self, targets: list[str]) -> bool:
        """True when every target in ``targets`` is ``done``."""
        return all(self.is_done(t) for t in targets)
