"""
scripts/_swanki_zotero_artifacts.py
[[scripts._swanki_zotero_artifacts]]
https://github.com/Mjvolk3/Swanki/tree/main/scripts/_swanki_zotero_artifacts.py
Test file: tests/test_swanki_anki_sync.py

Shared "newest artifact per content-prefix" lookup over Zotero child attachments.

``sync_to_zotero`` (swanki/sync/zotero.py) uploads Swanki outputs as
timestamped attachments shaped ``<prefix>-<YYYYMMDDThhmm>-<commit>.<ext>``.
A single Zotero item (paper or multi-chapter book) accumulates several of
these over re-runs. ``swanki_abs_sync.py`` and ``swanki_anki_sync.py`` both
need to resolve the newest attachment per prefix; this module is the
single implementation they share.
"""

import re
from typing import Any

from pyzotero import zotero

_TS_GROUP = r"(?P<ts>\d{8}T\d{4})"
_HASH_GROUP = r"(?P<hash>[a-f0-9]+)"


def _artifact_pattern(suffix: str) -> re.Pattern[str]:
    """Build a regex matching ``<key>-<ts>-<hash><suffix>`` filenames.

    Args:
        suffix: Filename extension including the leading dot (``.zip``,
            ``.apkg``). Treated as a literal; do not pass a regex.

    Returns:
        A compiled regex with named groups ``key``, ``ts``, ``hash``.
    """
    return re.compile(
        rf"^(?P<key>.+)-{_TS_GROUP}-{_HASH_GROUP}{re.escape(suffix)}$"
    )


# Pre-built patterns for the two extensions Swanki currently emits.
ZIP_PATTERN = _artifact_pattern(".zip")
APKG_PATTERN = _artifact_pattern(".apkg")


def _latest_artifact(
    zot: zotero.Zotero,
    item_key: str,
    pattern: re.Pattern[str],
) -> list[dict[str, Any]]:
    """Return the newest attachment per distinct content-prefix on an item.

    A Zotero item may carry many attachments matching the timestamped
    Swanki naming convention (one per chapter for books, multiple
    timestamps as re-runs accumulate). Group by the ``key`` regex capture,
    keep the newest ``ts`` per group, return one attachment per group.

    Args:
        zot: A configured ``pyzotero.zotero.Zotero`` client.
        item_key: The Zotero parent item key whose children to scan.
        pattern: A compiled regex from ``_artifact_pattern`` selecting one
            extension family (zips, apkgs).

    Returns:
        Attachment dicts (as returned by ``zot.children``), one per
        content-prefix, holding the newest timestamp in each group.
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
    """Newest ``.zip`` attachment per content-prefix on a Zotero item.

    See ``_latest_artifact`` for behavior. Thin wrapper preserving the
    historical name used by ``swanki_abs_sync.py``.
    """
    return _latest_artifact(zot, item_key, ZIP_PATTERN)


def latest_zip(zot: zotero.Zotero, item_key: str) -> dict[str, Any] | None:
    """Single newest ``.zip`` attachment across all prefixes (back-compat).

    Returns ``None`` when no matching attachment exists. Multi-chapter
    callers should use ``latest_zips`` instead.
    """
    zips = latest_zips(zot, item_key)
    if not zips:
        return None
    return max(
        zips,
        key=lambda c: ZIP_PATTERN.match(c["data"]["filename"]).group("ts"),  # type: ignore[union-attr]
    )


def latest_apkgs(zot: zotero.Zotero, item_key: str) -> list[dict[str, Any]]:
    """Newest ``.apkg`` attachment per content-prefix on a Zotero item.

    Same grouping behavior as ``latest_zips`` (one attachment per chapter
    base, newest timestamp wins).
    """
    return _latest_artifact(zot, item_key, APKG_PATTERN)
