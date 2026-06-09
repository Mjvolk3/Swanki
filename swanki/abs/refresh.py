"""
swanki/abs/refresh.py
[[swanki.abs.refresh]]
https://github.com/Mjvolk3/Swanki/tree/main/swanki/abs/refresh.py
Test file: tests/test_abs_refresh.py

ABS refresh orchestration: the 7-step full refresh (the legacy
``scripts/abs_refresh.sh`` pipeline as function calls) and the seconds-scale
targeted refresh for one republished item.

Locking: ``fcntl.flock`` on the same ``/tmp/abs-refresh.lock`` the bash
orchestrator used -- flock(1) and fcntl.flock are the same syscall on the same
file, so during any mixed window an in-flight bash run and a module run still
exclude each other. ``wait=False`` (cron semantics) skips when contended; the
next tick covers it. ``wait=True`` (delivery semantics) blocks so a contended
drain never silently no-ops its ABS step -- queue DONE means delivered.

The targeted refresh is the hot republish loop: the full refresh costs ~20
minutes (Zotero multi-projection repagination + zip pulls, not ABS -- the scan
is a cheap POST), where dropping the local artifact, scanning only the routed
libraries, and fixing that one item's chapters takes seconds. It is NOT
scan-only: the republished file's new ``-<TS>-<hash>`` name leaves the item's
chapters pointing at a deleted file until the per-item fix-up runs.

Environment-agnostic by design: the bash-drainer, the SLURM finalizer
(``python -m swanki.delivery finalize-abs``), the cron shim, and interactive
use all call the same two functions.
"""

import fcntl
import os
import time
from datetime import datetime
from pathlib import Path
from typing import IO, Any

from pydantic import BaseModel, Field

from swanki.abs.chapters import (
    clean_stale_chapters,
    fix_item_chapters,
    set_chapter_titles,
)
from swanki.abs.client import ABSClient
from swanki.abs.collections import mirror_zotero_collections
from swanki.abs.libraries import (
    build_library_index,
    ensure_libraries,
    library_items_by_title,
)
from swanki.abs.metadata import enrich_metadata
from swanki.abs.projections import (
    group_key,
    kind_for_key,
    load_projections,
)
from swanki.abs.sync import (
    MP3_PATTERN,
    abs_root_default,
    replace_stale,
    sync_all,
)

LOCK_FILE = "/tmp/abs-refresh.lock"

VERIFY_TIMEOUT_S = 60.0
VERIFY_INTERVAL_S = 3.0


class TargetedRefreshResult(BaseModel):
    """Outcome of one targeted refresh."""

    dropped: list[str] = Field(
        default_factory=list, description="Host paths of mp3s dropped"
    )
    scanned_libraries: list[str] = Field(
        default_factory=list, description="Library ids scanned"
    )
    verified_items: list[str] = Field(
        default_factory=list, description="ABS item ids serving the new audio"
    )
    chapters_fixed: list[str] = Field(
        default_factory=list, description="ABS item ids whose chapters were reposted"
    )


def _log(msg: str) -> None:
    print(f"[{datetime.now().astimezone().strftime('%Y-%m-%dT%H:%M:%S%z')}] {msg}")


def _acquire_lock(wait: bool) -> IO[str] | None:
    """Take the refresh lock; None when contended in non-blocking mode.

    The narrow ``BlockingIOError`` catch is the non-blocking acquisition's
    inherent signal (same justified-exception precedent as the retry helper
    in swanki/sync/zotero_client.py).
    """
    fh = open(LOCK_FILE, "w")
    if wait:
        fcntl.flock(fh, fcntl.LOCK_EX)
        return fh
    try:
        fcntl.flock(fh, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        fh.close()
        return None
    return fh


def full_refresh(
    *,
    wait: bool = False,
    projections_path: Path | None = None,
    abs_root: Path | None = None,
    db_path: str | None = None,
) -> bool:
    """Run the end-to-end ABS refresh (idempotent; safe on a tight schedule).

    Steps: Zotero audio sync, ensure libraries, mirror collections, enrich
    metadata, clean stale chapters, set chapter titles, scan all libraries.

    Args:
        wait: Block for the lock (delivery semantics) instead of skipping
            when another refresh is in flight (cron semantics).
        projections_path: Override the external projections.yml location.
        abs_root: Override the on-disk library root.
        db_path: Override the ABS sqlite path (chapter reads).

    Returns:
        True when the refresh ran; False when skipped on a contended lock.
    """
    lock = _acquire_lock(wait)
    if lock is None:
        _log("another abs_refresh in progress — skipping")
        return False

    _log("=== abs_refresh start ===")
    projections = load_projections(projections_path)
    root = abs_root if abs_root is not None else abs_root_default()
    client = ABSClient()
    zotero_api_key = os.environ["ZOTERO_API_KEY"]

    _log("step 1/7 — sync audio from Zotero")
    sync_all(projections_path, root)

    _log("step 2/7 — ensure libraries (idempotent)")
    ensure_libraries(client, projections)

    _log("step 3/7 — mirror Zotero collections")
    mirror_zotero_collections(client, projections, zotero_api_key)

    _log("step 4/7 — enrich metadata")
    enrich_metadata(client, projections, root, zotero_api_key)

    _log("step 5/7 — clean stale chapters")
    clean_stale_chapters(client, db_path)

    _log("step 6/7 — set chapter titles")
    set_chapter_titles(client, db_path)

    _log("step 7/7 — scan libraries")
    for lib in client.libraries():
        client.scan_library(lib["id"])
        _log(f"  scanned {lib['id']}")

    _log("=== abs_refresh done ===")
    lock.close()
    return True


def _newest_local_mp3s(output_dir: Path, citation_key: str) -> list[Path]:
    """Newest mp3 per ``(key, audio_type)`` under ``output_dir`` for the key.

    Files without a timestamp suffix sort oldest.
    """
    newest: dict[tuple[str, str], tuple[str, Path]] = {}
    for path in output_dir.rglob("*.mp3"):
        m = MP3_PATTERN.match(path.name)
        if not m or m.group("key") != citation_key:
            continue
        ts = m.group("ts") or ""
        slot = (m.group("key"), m.group("type"))
        prev = newest.get(slot)
        if prev is None or ts > prev[0]:
            newest[slot] = (ts, path)
    return [p for _, p in newest.values()]


def targeted_refresh(
    *,
    citation_key: str,
    output_dir: Path,
    projections_path: Path | None = None,
    abs_root: Path | None = None,
    client: ABSClient | None = None,
    sleep: Any = time.sleep,
) -> TargetedRefreshResult:
    """Land one republished item on ABS in seconds (drop, scan, fix, verify).

    Routing is by existing group dir: the item's audio is dropped into every
    projection library dir that already carries the group (a republish always
    has a prior sync; a genuinely NEW item goes through the full refresh).
    Fan-out matters -- an item can live in several projection libraries, and
    dropping into only one leaves the others stale until the next full
    refresh.

    Always blocking (the publish path must never silently no-op).

    Args:
        citation_key: The content key naming the mp3s (chapter key for books).
        output_dir: Pipeline output dir holding the regenerated mp3(s).
        projections_path: Override the external projections.yml location.
        abs_root: Override the on-disk library root.
        client: Optional pre-built client (tests).
        sleep: Sleep function (injectable for tests).

    Returns:
        A ``TargetedRefreshResult``; raises when verification times out.
    """
    lock = _acquire_lock(wait=True)
    assert lock is not None  # blocking acquisition cannot return None

    result = TargetedRefreshResult()
    projections = load_projections(projections_path)
    root = abs_root if abs_root is not None else abs_root_default()
    c = client if client is not None else ABSClient()

    kind = kind_for_key(citation_key)
    group = group_key(citation_key, kind)
    mp3s = _newest_local_mp3s(output_dir, citation_key)
    if not mp3s:
        lock.close()
        raise FileNotFoundError(
            f"no mp3s for {citation_key!r} under {output_dir}"
        )

    # Drop into every routed projection that already carries the group.
    touched: set[tuple[str, str]] = set()  # (projection, audiotype_lower)
    for proj_name, cfg in projections.items():
        if not cfg.get("push_audio", True):
            continue
        audiotypes = set(cfg["audiotypes"])
        for mp3 in mp3s:
            m = MP3_PATTERN.match(mp3.name)
            assert m is not None  # filtered by _newest_local_mp3s
            audio_type = m.group("type")
            if audio_type not in audiotypes:
                continue
            dest_dir = (
                root / proj_name / f"Swanki-{kind}-{audio_type.capitalize()}" / group
            )
            if not dest_dir.is_dir():
                continue
            target = dest_dir / mp3.name
            if not target.exists():
                replace_stale(dest_dir, citation_key, audio_type, mp3.name)
                target.write_bytes(mp3.read_bytes())
                result.dropped.append(str(target))
                _log(f"dropped {target}")
            touched.add((proj_name, audio_type.lower()))

    if not touched:
        lock.close()
        raise FileNotFoundError(
            f"no existing projection dir carries {group!r} "
            f"(new items go through the full refresh)"
        )

    # Scan only the affected libraries; remember which audio types each serves.
    lib_index = build_library_index(c)
    types_by_lib: dict[str, set[str]] = {}
    for proj, at in touched:
        lib_id_ = lib_index.get((proj, kind, at))
        if lib_id_ is not None:
            types_by_lib.setdefault(lib_id_, set()).add(at)
    for lib_id in sorted(types_by_lib):
        c.scan_library(lib_id)
        result.scanned_libraries.append(lib_id)
        _log(f"scanned {lib_id}")

    # Verify each affected item serves the new filenames, then fix chapters.
    for lib_id, audio_types in sorted(types_by_lib.items()):
        relevant = {
            p.name
            for p in mp3s
            if (m := MP3_PATTERN.match(p.name))
            and m.group("type").lower() in audio_types
        }
        deadline = time.monotonic() + VERIFY_TIMEOUT_S
        while True:
            item_id = library_items_by_title(c, lib_id).get(group)
            if item_id is not None:
                item = c.item(item_id)
                served = {
                    af.get("metadata", {}).get("filename", "")
                    for af in item.get("media", {}).get("audioFiles", [])
                }
                if relevant <= served:
                    break
            if time.monotonic() > deadline:
                lock.close()
                raise TimeoutError(
                    f"library {lib_id}: item {group!r} not serving "
                    f"{sorted(relevant)} after {VERIFY_TIMEOUT_S:.0f}s"
                )
            sleep(VERIFY_INTERVAL_S)
        result.verified_items.append(item_id)
        if fix_item_chapters(c, item_id):
            result.chapters_fixed.append(item_id)
            _log(f"chapters fixed for {group} in {lib_id}")

    _log(
        f"targeted refresh done: {len(result.dropped)} file(s), "
        f"{len(result.scanned_libraries)} scan(s), "
        f"{len(result.chapters_fixed)} chapter fix(es)"
    )
    lock.close()
    return result
