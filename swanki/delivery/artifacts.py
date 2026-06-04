"""
swanki/delivery/artifacts.py
[[swanki.delivery.artifacts]]
https://github.com/Mjvolk3/Swanki/tree/main/swanki/delivery/artifacts.py
Test file: tests/test_swanki_anki_sync.py

Newest-artifact-per-content-prefix selection over timestamped Swanki outputs.

``sync_to_zotero`` (swanki/sync/zotero.py) emits artifacts shaped
``<prefix>-<YYYYMMDDThhmm>-<commit>.<ext>``; a single Zotero item (or local
output dir) accumulates several over re-runs. Resolving "the current artifact
per chapter base" is shared by the Zotero source, the Anki target, and the
legacy scripts -- this is the single implementation. ``scripts/
_swanki_zotero_artifacts.py`` is a thin re-export of this module so the
script CLIs and their tests keep importing the same names.
"""

import re
from typing import Any

from pyzotero import zotero

_TS_GROUP = r"(?P<ts>\d{8}T\d{4})"
_HASH_GROUP = r"(?P<hash>[a-f0-9]+)"


def artifact_pattern(suffix: str) -> re.Pattern[str]:
    """Build a regex matching ``<key>-<ts>-<hash><suffix>`` filenames.

    Args:
        suffix: Filename extension including the leading dot (``.zip``,
            ``.apkg``). Treated as a literal; do not pass a regex.

    Returns:
        A compiled regex with named groups ``key``, ``ts``, ``hash``.
    """
    return re.compile(rf"^(?P<key>.+)-{_TS_GROUP}-{_HASH_GROUP}{re.escape(suffix)}$")


# Pre-built patterns for the two extensions Swanki currently emits.
ZIP_PATTERN = artifact_pattern(".zip")
APKG_PATTERN = artifact_pattern(".apkg")


def _latest_artifact(
    zot: zotero.Zotero,
    item_key: str,
    pattern: re.Pattern[str],
) -> list[dict[str, Any]]:
    """Return the newest attachment per distinct content-prefix on an item.

    Group ``zot.children`` attachments by the ``key`` regex capture, keep the
    newest ``ts`` per group, and return one attachment per group.

    Args:
        zot: A configured ``pyzotero.zotero.Zotero`` client.
        item_key: The Zotero parent item key whose children to scan.
        pattern: A compiled regex from ``artifact_pattern`` selecting one
            extension family.

    Returns:
        Attachment dicts, one per content-prefix, holding the newest timestamp.
    """
    by_prefix: dict[str, tuple[str, dict[str, Any]]] = {}
    for child in zot.children(item_key):
        name = child.get("data", {}).get("filename", "")
        m = pattern.match(name)
        if not m:
            continue
        prefix = m.group("key")
        ts = m.group("ts")
        prev = by_prefix.get(prefix)
        if prev is None or ts > prev[0]:
            by_prefix[prefix] = (ts, child)
    return [c for _, c in by_prefix.values()]


def latest_zips(zot: zotero.Zotero, item_key: str) -> list[dict[str, Any]]:
    """Newest ``.zip`` attachment per content-prefix on a Zotero item."""
    return _latest_artifact(zot, item_key, ZIP_PATTERN)


def latest_zip(zot: zotero.Zotero, item_key: str) -> dict[str, Any] | None:
    """Single newest ``.zip`` attachment across all prefixes (back-compat).

    Returns ``None`` when no matching attachment exists. Multi-chapter callers
    should use ``latest_zips`` instead.
    """
    zips = latest_zips(zot, item_key)
    if not zips:
        return None
    return max(
        zips,
        key=lambda c: ZIP_PATTERN.match(c["data"]["filename"]).group("ts"),  # type: ignore[union-attr]
    )


def latest_apkgs(zot: zotero.Zotero, item_key: str) -> list[dict[str, Any]]:
    """Newest ``.apkg`` attachment per content-prefix on a Zotero item."""
    return _latest_artifact(zot, item_key, APKG_PATTERN)
