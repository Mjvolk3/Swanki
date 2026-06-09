"""
swanki/abs/chapters.py
[[swanki.abs.chapters]]
https://github.com/Mjvolk3/Swanki/tree/main/swanki/abs/chapters.py
Test file: tests/test_abs_chapters.py

Chapter hygiene: stale-clean + canonical retitle, merged (refresh steps 5-6).
The two legacy scripts shared the filename->content_key derivation; one home.

Read/write split (load-bearing): book state is READ from the ABS sqlite DB
(``ABS_DB`` env) but always WRITTEN via the API -- a direct sqlite write would
leave ABS serving stale in-memory data until restart.

Stale rule: every chapter title must either exactly match the stem of a
current audioFile, or be a prefix of one followed by ``-`` (the
``-{summary,reading,lecture}-<TS>-<hash>`` suffix swanki appends). The prefix
form lets manually-cleaned titles survive cron cycles. Otherwise the chapter
array is cleared, and the retitle pass repopulates it deterministically from
audioFile filenames -- titles AND boundaries (cumulative per-file durations,
0.5s drift tolerance; durations shift across re-renders without any title
change, which once left a chapter marker 130s short of its mp3).

``fix_item_chapters`` is the per-item form for the targeted refresh: it reads
audioFiles from the API (no sqlite needed) and reposts canonical chapters for
just that item.
"""

import json
import os
import re
import sqlite3
from typing import Any

from swanki.abs.client import ABSClient

DEFAULT_ABS_DB = (
    "/home/michaelvolk/Documents/projects/infra/abs/config/absdatabase.sqlite"
)

# Strip swanki's per-file suffix to recover the content_key. The suffix shape
# is `-<audio_type>-<YYYYMMDDTHHMM>-<git_short_hash>.<ext>`.
_SUFFIX_RE = re.compile(
    r"-(?:lecture|reading|summary)-\d{8}T\d{4}-[0-9a-f]+\.(?:mp3|m4a|m4b|wav)$"
)

BOUND_TOL_S = 0.5  # sub-second boundary drift acceptable


def abs_db_default() -> str:
    """The ABS sqlite path (``ABS_DB`` env override)."""
    return os.environ.get("ABS_DB", DEFAULT_ABS_DB)


def _stem(name: str) -> str:
    """Filename stem matching ABS's chapter-title convention (no extension)."""
    return name.rsplit(".", 1)[0] if "." in name else name


def content_key_from_filename(fname: str) -> str:
    """Return the content_key portion of an audioFile filename.

    Falls through to the filename stem when the swanki suffix is absent, so
    non-swanki audioFiles keep a sensible label.
    """
    stripped = _SUFFIX_RE.sub("", fname)
    if stripped != fname:
        return stripped
    return _stem(fname)


def chapters_from_audiofiles(
    audio_files: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Build the canonical ABS chapters array from an audioFiles list.

    Ordered by ``index`` with cumulative ``start``/``end`` seconds and
    ``title`` set to each file's content_key.
    """
    ordered = sorted(audio_files, key=lambda af: af.get("index", 0))
    chapters: list[dict[str, Any]] = []
    cursor = 0.0
    for i, af in enumerate(ordered):
        fname = af.get("metadata", {}).get("filename", "")
        duration = float(af.get("duration", 0.0))
        end = cursor + duration
        chapters.append(
            {
                "id": i,
                "title": content_key_from_filename(fname),
                "start": cursor,
                "end": end,
            }
        )
        cursor = end
    return chapters


def _chapters_match(
    current: list[dict[str, Any]], desired: list[dict[str, Any]]
) -> bool:
    """Whether existing chapters already carry the canonical titles + bounds."""
    return len(current) == len(desired) and all(
        (c.get("title") or "") == d["title"]
        and abs(float(c.get("start", 0)) - d["start"]) < BOUND_TOL_S
        and abs(float(c.get("end", 0)) - d["end"]) < BOUND_TOL_S
        for c, d in zip(current, desired)
    )


def find_books_with_stale_chapters(
    db_path: str,
) -> list[tuple[str, str, str]]:
    """Return ``(libraryItem_id, book_id, title)`` per book with stale chapters.

    Stale = any chapter title that neither exactly matches a current audioFile
    stem nor is a ``-``-suffixed prefix of one.
    """
    con = sqlite3.connect(db_path)
    con.row_factory = sqlite3.Row
    rows = con.execute(
        """
        SELECT li.id AS li_id, b.id AS book_id, b.title, b.chapters, b.audioFiles
        FROM books b
        JOIN libraryItems li ON li.mediaId = b.id
        WHERE b.chapters IS NOT NULL
          AND b.chapters != '[]'
          AND b.chapters != ''
        """
    ).fetchall()
    con.close()

    stale: list[tuple[str, str, str]] = []
    for row in rows:
        try:
            chapters = json.loads(row["chapters"] or "[]")
            audio_files = json.loads(row["audioFiles"] or "[]")
        except json.JSONDecodeError:
            continue
        if not chapters:
            continue
        current_stems = {
            _stem(af.get("metadata", {}).get("filename", ""))
            for af in audio_files
        }
        chapter_titles = {
            ch.get("title", "") for ch in chapters if ch.get("title")
        }

        def _valid(title: str) -> bool:
            return any(
                stem == title or stem.startswith(f"{title}-")
                for stem in current_stems
            )

        if not all(_valid(t) for t in chapter_titles):
            stale.append((row["li_id"], row["book_id"], row["title"]))
    return stale


def clean_stale_chapters(client: ABSClient, db_path: str | None = None) -> int:
    """Clear the chapters array on every book referencing deleted audioFiles.

    Returns:
        Count of books cleared.
    """
    stale = find_books_with_stale_chapters(db_path or abs_db_default())
    if not stale:
        print("no stale chapters — nothing to do")
        return 0
    print(f"clearing stale chapters on {len(stale)} book(s):")
    for item_id, book_id, title in stale:
        print(f"  {title[:60]:<60}  item={item_id[:8]}  book={book_id[:8]}")
        client.post_chapters(item_id, [])
    return len(stale)


def find_books_needing_chapter_titles(
    db_path: str,
) -> list[
    tuple[str, str, str, list[dict[str, Any]], list[dict[str, Any]]]
]:
    """Return rows for every book whose chapters need setting or refreshing.

    A book needs an update when its chapters JSON is empty OR any existing
    title/boundary differs from the canonical form derived from its current
    audioFiles. Skips books with no audioFiles.
    """
    con = sqlite3.connect(db_path)
    con.row_factory = sqlite3.Row
    rows = con.execute(
        """
        SELECT li.id AS li_id, b.id AS book_id, b.title, b.chapters, b.audioFiles
        FROM books b
        JOIN libraryItems li ON li.mediaId = b.id
        WHERE b.audioFiles IS NOT NULL AND b.audioFiles != '[]'
        """
    ).fetchall()
    con.close()

    needing: list[
        tuple[str, str, str, list[dict[str, Any]], list[dict[str, Any]]]
    ] = []
    for row in rows:
        audio_files = json.loads(row["audioFiles"] or "[]")
        if not audio_files:
            continue
        desired = chapters_from_audiofiles(audio_files)
        if not desired:
            continue
        current_raw = row["chapters"] or "[]"
        current = json.loads(current_raw) if current_raw else []
        if _chapters_match(current, desired):
            continue
        needing.append(
            (row["li_id"], row["book_id"], row["title"], current, desired)
        )
    return needing


def set_chapter_titles(client: ABSClient, db_path: str | None = None) -> int:
    """Set canonical chapter titles on every ABS book that needs an update.

    Returns:
        Count of books updated.
    """
    needing = find_books_needing_chapter_titles(db_path or abs_db_default())
    if not needing:
        print("all chapter titles already canonical — nothing to do")
        return 0

    print(f"setting chapter titles on {len(needing)} book(s):")
    for item_id, _book_id, title, current, desired in needing:
        if not current:
            action = "set"
        elif len(current) != len(desired):
            action = f"refresh ({len(current)}->{len(desired)} chapters)"
        elif any(
            (c.get("title") or "") != d["title"]
            for c, d in zip(current, desired)
        ):
            action = "refresh (titles changed)"
        else:
            action = "refresh (boundaries shifted)"
        print(f"  {title[:60]:<60}  item={item_id[:8]}  {action}")
        client.post_chapters(item_id, desired)
    return len(needing)


def fix_item_chapters(client: ABSClient, item_id: str) -> bool:
    """Repost canonical chapters for ONE item, reading audioFiles via the API.

    The targeted-refresh form: after a republish the item's chapters reference
    the deleted old filename until this runs; waiting for the next full
    refresh would leave the item broken in the player for up to a cron cycle.

    Returns:
        True when chapters were updated, False when already canonical.
    """
    item = client.item(item_id)
    audio_files = item.get("media", {}).get("audioFiles", [])
    if not audio_files:
        return False
    desired = chapters_from_audiofiles(audio_files)
    current = item.get("media", {}).get("chapters", [])
    if _chapters_match(current, desired):
        return False
    client.post_chapters(item_id, desired)
    return True
