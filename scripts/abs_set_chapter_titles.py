"""
scripts/abs_set_chapter_titles.py
[[scripts.abs_set_chapter_titles]]
https://github.com/Mjvolk3/Swanki/tree/main/scripts/abs_set_chapter_titles.py

Set ABS chapter titles to the canonical content_key form for every book whose
chapters JSON is empty. Runs after abs_clean_stale_chapters in the abs_refresh
pipeline -- after that step clears titles whose stem no longer matches any
audioFile, this script repopulates them deterministically from the current
audioFile filenames so the listener never sees ABS's "Chapter 1" / "Chapter 2"
auto-numbering fallback in the UI.

Naming rule: each chapter title is the content_key, recovered from the
audioFile filename by stripping the swanki suffix
``-{summary,reading,lecture}-<TS>-<hash>.mp3``. So
``hammingArtDoingScience2020_03_history-of-computers-hardware-lecture-20260514T1010-7d23dec.mp3``
becomes ``hammingArtDoingScience2020_03_history-of-computers-hardware``. This
matches the prefix-form abs_clean_stale_chapters preserves across re-renders,
so once set the titles survive future cron cycles unchanged.

Chapter start/end are computed by cumulating the per-file ``duration`` in
audioFile track order (the ``index`` field). Posts via ABS's chapters API so
in-memory state updates immediately -- a direct SQLite write would leave ABS
serving stale data until restart.

Books whose chapters JSON is non-empty AND whose existing titles all match the
expected content_key form are skipped; this script is idempotent and safe to
run on every refresh.
"""

import json
import os
import re
import sqlite3
import sys
from pathlib import Path
from typing import Any

import httpx

ABS_DB = os.environ.get(
    "ABS_DB",
    "/home/michaelvolk/Documents/projects/infra/abs/config/absdatabase.sqlite",
)
ABS_URL = os.environ.get("ABS_URL", "https://abs.michaelvolk.dev")
TOKEN_FILE = os.environ.get(
    "ABS_API_TOKEN_FILE",
    str(Path.home() / "Documents/projects/infra/abs/.api-token"),
)

# Strip swanki's per-file suffix to recover the content_key. The suffix shape
# is `-<audio_type>-<YYYYMMDDTHHMM>-<git_short_hash>.<ext>` where audio_type is
# one of summary/reading/lecture and ext is one of mp3/m4a/m4b/wav.
_SUFFIX_RE = re.compile(
    r"-(?:lecture|reading|summary)-\d{8}T\d{4}-[0-9a-f]+\.(?:mp3|m4a|m4b|wav)$"
)


def content_key_from_filename(fname: str) -> str:
    """Return the content_key portion of an audioFile filename.

    Args:
        fname: Filename like ``key_03_slug-lecture-20260514T1010-7d23dec.mp3``.

    Returns:
        The content_key (``key_03_slug``) when the suffix matches, else the
        filename stem (filename minus its extension) as a fall-through. The
        fall-through guarantees we always emit a non-empty title and lets
        non-swanki audioFiles (e.g. manually added) keep a sensible label.
    """
    stripped = _SUFFIX_RE.sub("", fname)
    if stripped != fname:
        return stripped
    return fname.rsplit(".", 1)[0] if "." in fname else fname


def chapters_from_audiofiles(audio_files: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Build the ABS chapters array from an audioFiles list.

    Args:
        audio_files: ``b.audioFiles`` JSON list (each entry has ``index``,
            ``duration``, and ``metadata.filename``).

    Returns:
        A chapters list ordered by ``index`` with cumulative ``start`` / ``end``
        seconds and ``title`` set to each file's content_key.
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


def find_books_needing_chapter_titles(
    db_path: str,
) -> list[tuple[str, str, str, list[dict[str, Any]], list[dict[str, Any]]]]:
    """Return rows for every book that needs chapter titles set or refreshed.

    A book needs an update when EITHER its chapters JSON is empty / null OR
    any existing chapter title differs from the canonical content_key form
    derived from its current audioFiles. Skips books with no audioFiles.

    Returns:
        List of ``(libraryItem_id, book_id, title, current_chapters, desired_chapters)``.
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

    needing: list[tuple[str, str, str, list[dict[str, Any]], list[dict[str, Any]]]] = []
    for row in rows:
        audio_files = json.loads(row["audioFiles"] or "[]")
        if not audio_files:
            continue
        desired = chapters_from_audiofiles(audio_files)
        if not desired:
            continue
        current_raw = row["chapters"] or "[]"
        current = json.loads(current_raw) if current_raw else []
        # Same length AND same titles in order -> already canonical.
        if len(current) == len(desired) and all(
            (c.get("title") or "") == d["title"]
            for c, d in zip(current, desired)
        ):
            continue
        needing.append((row["li_id"], row["book_id"], row["title"], current, desired))
    return needing


def post_chapters(item_id: str, chapters: list[dict[str, Any]], token: str) -> None:
    """POST a chapters array to ABS so DB + in-memory state both update."""
    r = httpx.post(
        f"{ABS_URL}/api/items/{item_id}/chapters",
        headers={
            "Authorization": f"Bearer {token}",
            "User-Agent": "swanki-abs-set-chapter-titles/1.0",
            "Content-Type": "application/json",
        },
        json={"chapters": chapters},
        timeout=30.0,
    )
    r.raise_for_status()


def main() -> int:
    """Set canonical chapter titles on every ABS book that needs an update."""
    if not Path(TOKEN_FILE).exists():
        print(f"error: API token file missing: {TOKEN_FILE}", file=sys.stderr)
        return 1
    token = Path(TOKEN_FILE).read_text().strip()

    needing = find_books_needing_chapter_titles(ABS_DB)
    if not needing:
        print("all chapter titles already canonical — nothing to do")
        return 0

    print(f"setting chapter titles on {len(needing)} book(s):")
    for item_id, book_id, title, current, desired in needing:
        action = "set" if not current else f"refresh ({len(current)}->{len(desired)})"
        print(f"  {title[:60]:<60}  item={item_id[:8]}  {action}")
        post_chapters(item_id, desired, token)
    print("done")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
