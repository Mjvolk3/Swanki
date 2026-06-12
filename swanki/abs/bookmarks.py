"""
swanki/abs/bookmarks.py
[[swanki.abs.bookmarks]]
https://github.com/Mjvolk3/Swanki/tree/main/swanki/abs/bookmarks.py
Test file: tests/test_abs_bookmarks.py

ABS user bookmarks: fetch + windowed wipe + swanki-attributed create.
``add_bookmark`` is the outbound half of the listening-note loop: swanki
drops a marker the user sees in Prologue (e.g. "listen here for the A/B
pause-tag spot"). Notes are prefixed with ``SWANKI_MARK`` so machine-left
bookmarks are unmistakable next to the user's own. The caller passes a
FILE-LOCAL time for a content key; the helper shifts it to the item-global
timeline (book items stitch all chapter tracks, and bookmark ``time`` is
global across them) and creates the bookmark on every library item serving
that file (one per projection).

Fetch/wipe half: bookmarks are ephemeral issue
flags ([[scripts.abs_clear_bookmarks]], 2026-05-21): after replacing audio the
addressed bookmarks are deleted, never timestamp-migrated -- the durable
address of an issue is chunk-text content-match, not a timestamp.

The windowed wipe (``clear_bookmarks(..., windows=...)``) is the default
post-replace behavior: delete only bookmarks inside the item-global time
windows of the replaced chunks; everything else survives. Windows MUST be
computed on the OLD (pre-restitch) timeline and shifted by the durations of
the ABS item's preceding audio files -- bookmark ``time`` is global across the
item's stitched multi-file timeline while chunk windows are per-file
(``edit_chunk``'s returned window is NEW-timeline and must never feed a wipe).
No windows = whole-item clear (the legacy clear-and-re-mark degenerate case).

NOTE: a bookmark ``time`` is the playhead WHEN THE NOTE WAS SAVED -- it lags
the actual issue by up to minutes, so callers pad windows forward and keep
dry-run-first. Deletion is irreversible; archive bookmark notes before
clearing. The JSON->model mapping is isolated in ``_to_bookmark`` so a schema
drift is a one-line, fixture-tested fix.
"""

from typing import Any

from pydantic import BaseModel, Field

from swanki.abs.client import ABSClient
from swanki.abs.libraries import library_items_by_title
from swanki.abs.projections import group_key, kind_for_key

SWANKI_MARK = "\U0001f9a2 swanki"


class AbsBookmark(BaseModel):
    """One Audiobookshelf user bookmark."""

    library_item_id: str = Field(description="ABS libraryItem id")
    time_s: float = Field(description="Playhead seconds when the note was saved")
    note: str = Field(description="Bookmark note / title text")
    created_at: int = Field(default=0, description="Epoch ms, 0 if absent")
    item_title: str = Field(default="", description="Resolved item title")


def _to_bookmark(raw: dict[str, Any]) -> AbsBookmark:
    """Map one ``/api/me`` bookmark dict to the model."""
    return AbsBookmark(
        library_item_id=str(raw.get("libraryItemId", "")),
        time_s=float(raw.get("time", 0) or 0),
        note=str(raw.get("title", "") or ""),
        created_at=int(raw.get("createdAt", 0) or 0),
    )


def _item_title(client: ABSClient, library_item_id: str) -> str:
    item = client.item(library_item_id)
    return item.get("media", {}).get("metadata", {}).get("title", "") or ""


def get_bookmarks(
    *, citation_key: str | None = None, client: ABSClient | None = None
) -> list[AbsBookmark]:
    """Return the current user's ABS bookmarks, newest first.

    Args:
        citation_key: When given, keep only bookmarks whose resolved item
            title or note contains the key (case-insensitive).
        client: Optional pre-built client (tests); defaults to env-configured.

    Returns:
        Bookmarks sorted by ``created_at`` descending.
    """
    c = client if client is not None else ABSClient()
    me = c.me()
    out: list[AbsBookmark] = []
    title_cache: dict[str, str] = {}
    for raw in me.get("bookmarks", []):
        bm = _to_bookmark(raw)
        if bm.library_item_id not in title_cache:
            title_cache[bm.library_item_id] = _item_title(
                c, bm.library_item_id
            )
        bm.item_title = title_cache[bm.library_item_id]
        if citation_key and citation_key.lower() not in (
            bm.item_title.lower() + " " + bm.note.lower()
        ):
            continue
        out.append(bm)
    out.sort(key=lambda b: b.created_at, reverse=True)
    return out


def in_windows(
    time_s: float, windows: list[tuple[float, float]] | None
) -> bool:
    """Whether a bookmark time falls inside any window (None = everywhere)."""
    if windows is None:
        return True
    return any(start <= time_s <= end for start, end in windows)


def format_bookmark(b: AbsBookmark) -> str:
    """One display line for a bookmark (mm:ss + truncated note)."""
    t = int(b.time_s)
    return f"[{b.item_title}] @ {t // 60}:{t % 60:02d}  {b.note[:70]}"


def clear_bookmarks(
    *,
    citation_key: str,
    windows: list[tuple[float, float]] | None = None,
    dry_run: bool = True,
    client: ABSClient | None = None,
) -> int:
    """Delete the item's bookmarks, optionally restricted to time windows.

    Args:
        citation_key: Substring matched (case-insensitive) against item title
            / note by ``get_bookmarks``.
        windows: Item-global ``(start_s, end_s)`` windows; only bookmarks
            inside any window are deleted. None deletes all (whole-item clear).
        dry_run: When True (default), list what would be deleted and delete
            nothing.
        client: Optional pre-built client.

    Returns:
        Count of bookmarks deleted (0 in dry-run).
    """
    c = client if client is not None else ABSClient()
    bms = [
        b
        for b in get_bookmarks(citation_key=citation_key, client=c)
        if in_windows(b.time_s, windows)
    ]
    scope = "all" if windows is None else f"{len(windows)} window(s)"
    print(f"{len(bms)} bookmark(s) match '{citation_key}' ({scope}):")
    for b in bms:
        print(f"  {format_bookmark(b)}")
    if dry_run:
        print("\nDRY RUN -- nothing deleted. Re-run with --yes to clear.")
        return 0

    for b in bms:
        c.delete_bookmark(b.library_item_id, b.time_s)
    print(f"\nDeleted {len(bms)} bookmark(s).")
    return len(bms)


def clear_bookmarks_in_windows(
    citation_key: str,
    windows: list[tuple[float, float]],
    *,
    dry_run: bool = True,
    client: ABSClient | None = None,
) -> int:
    """Windowed wipe-on-replace: the named form of ``clear_bookmarks``."""
    return clear_bookmarks(
        citation_key=citation_key, windows=windows, dry_run=dry_run, client=client
    )


def file_offset_in_item(
    item: dict[str, Any], content_key: str, audio_type: str
) -> float | None:
    """Seconds of item audio preceding the content_key's file.

    Walks the item's ``audioFiles`` in track order (the same cumulative walk
    as ``chapters_from_audiofiles``) and returns the start offset of the file
    named ``{content_key}-{audio_type}-<TS>-<hash>``, or None when the item
    doesn't serve that file.

    Raises:
        LookupError: Two audioFiles match the prefix (a stale-replace bug --
            the refresh guarantees one live file per content_key+type).
    """
    ordered = sorted(
        item.get("media", {}).get("audioFiles", []),
        key=lambda af: af.get("index", 0),
    )
    prefix = f"{content_key}-{audio_type}-"
    cursor = 0.0
    hit: float | None = None
    for af in ordered:
        fname = af.get("metadata", {}).get("filename", "")
        if fname.startswith(prefix):
            if hit is not None:
                raise LookupError(
                    f"multiple audioFiles match {prefix!r} in item "
                    f"{item.get('id', '?')}"
                )
            hit = cursor
        cursor += float(af.get("duration", 0.0))
    return hit


def add_bookmark(
    *,
    content_key: str,
    time_s: float,
    note: str,
    audio_type: str = "lecture",
    client: ABSClient | None = None,
) -> list[AbsBookmark]:
    """Create a swanki-attributed bookmark at a file-local time.

    Args:
        content_key: Full content key naming the audio file (chapter key for
            books, citation key for papers).
        time_s: Seconds LOCAL to that file; shifted to the item-global
            timeline before creation.
        note: Bookmark text; prefixed with ``SWANKI_MARK`` so it reads as
            machine-left in Prologue/ABS.
        audio_type: Which of the file's audio types (lecture/reading/summary).
        client: Optional pre-built client.

    Returns:
        One ``AbsBookmark`` per library item the bookmark was created on
        (the same book is served by one item per projection).

    Raises:
        LookupError: No ABS item serves the content_key's audio file.
    """
    c = client if client is not None else ABSClient()
    group = group_key(content_key, kind_for_key(content_key))
    title = f"{SWANKI_MARK}: {note}"
    created: list[AbsBookmark] = []
    for lib in c.libraries():
        item_id = library_items_by_title(c, lib["id"]).get(group)
        if item_id is None:
            continue
        offset = file_offset_in_item(c.item(item_id), content_key, audio_type)
        if offset is None:
            continue
        t = float(int(offset + time_s))
        c.create_bookmark(item_id, t, title)
        created.append(
            AbsBookmark(
                library_item_id=item_id, time_s=t, note=title, item_title=group
            )
        )
    if not created:
        raise LookupError(
            f"no ABS item serves {content_key!r} ({audio_type})"
        )
    return created
