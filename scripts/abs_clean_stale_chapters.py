"""
scripts/abs_clean_stale_chapters.py
[[scripts.abs_clean_stale_chapters]]
https://github.com/Mjvolk3/Swanki/tree/main/scripts/abs_clean_stale_chapters.py

Clear ABS chapter metadata that points at audio files no longer present.

After swanki_abs_sync pulls new audio into a book's folder and ABS's library
scan updates `audioFiles`, the `chapters` JSON on the book can still reference
old filenames (ABS derives chapter titles from filenames when a book has
multiple tracks, and doesn't re-derive them when the file set changes).
Prologue then shows phantom chapters pointing at deleted tracks.

Rule (stable across regens that keep track counts the same but change
timestamps): every chapter title must match the stem of an audioFile
currently on the book. If any chapter title is absent from the current
audioFiles, clear the chapters array.

Run via the ABS API so in-memory state is updated too (a direct SQLite
write would leave ABS serving stale in-memory data until restart).
"""

import json
import os
import sqlite3
import sys
from pathlib import Path

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


def _stem(name: str) -> str:
    """Filename stem matching ABS's chapter-title convention (no extension)."""
    return name.rsplit(".", 1)[0] if "." in name else name


def find_books_with_stale_chapters(db_path: str) -> list[tuple[str, str, str]]:
    """Return (libraryItem_id, book_id, title) for every book whose chapters
    reference any filename absent from its current audioFiles."""
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
            _stem(af.get("metadata", {}).get("filename", "")) for af in audio_files
        }
        chapter_titles = {ch.get("title", "") for ch in chapters}
        if not chapter_titles.issubset(current_stems):
            stale.append((row["li_id"], row["book_id"], row["title"]))
    return stale


def clear_chapters_via_api(item_id: str, token: str) -> bool:
    """POST an empty chapters array to update both DB and in-memory state."""
    r = httpx.post(
        f"{ABS_URL}/api/items/{item_id}/chapters",
        headers={
            "Authorization": f"Bearer {token}",
            "User-Agent": "swanki-abs-clean/1.0",
            "Content-Type": "application/json",
        },
        json={"chapters": []},
        timeout=30.0,
    )
    r.raise_for_status()
    return True


def main() -> int:
    if not Path(TOKEN_FILE).exists():
        print(f"error: API token file missing: {TOKEN_FILE}", file=sys.stderr)
        return 1
    token = Path(TOKEN_FILE).read_text().strip()

    stale = find_books_with_stale_chapters(ABS_DB)
    if not stale:
        print("no stale chapters — nothing to do")
        return 0

    print(f"clearing stale chapters on {len(stale)} book(s):")
    for item_id, book_id, title in stale:
        print(f"  {title[:60]:<60}  item={item_id[:8]}  book={book_id[:8]}")
        clear_chapters_via_api(item_id, token)
    print("done")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
