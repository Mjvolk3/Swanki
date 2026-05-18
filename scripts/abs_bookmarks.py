"""
scripts/abs_bookmarks.py
[[scripts.abs_bookmarks]]
https://github.com/Mjvolk3/Swanki/tree/main/scripts/abs_bookmarks.py
Test file: tests/test_abs_bookmarks.py

Fetch the current user's Audiobookshelf bookmarks via the ABS REST API
(`/api/me`). Replaces the macOS-only BookPlayer SQLite path for gilahyper.
Importable `get_bookmarks()` + thin CLI; the JSON->model mapping is isolated
in `_to_bookmark` so a wrong field name is a one-line, fixture-tested fix.

NOTE: an ABS bookmark `time` is the playhead WHEN THE NOTE WAS SAVED -- it
lags the actual issue by minutes. Use it only to pick the chapter/file;
locate the chunk by content-match + the chunk_timeline sidecar.
"""

import argparse
import os
from pathlib import Path
from typing import Any

import requests
from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv(dotenv_path=str(Path.cwd() / ".env"))

ABS_URL = os.environ.get("ABS_URL", "https://abs.michaelvolk.dev")
ABS_API_TOKEN_FILE = os.environ.get(
    "ABS_API_TOKEN_FILE",
    str(Path.home() / "Documents/projects/infra/abs/.api-token"),
)


class AbsBookmark(BaseModel):
    """One Audiobookshelf user bookmark."""

    library_item_id: str = Field(description="ABS libraryItem id")
    time_s: float = Field(description="Playhead seconds when the note was saved")
    note: str = Field(description="Bookmark note / title text")
    created_at: int = Field(default=0, description="Epoch ms, 0 if absent")
    item_title: str = Field(default="", description="Resolved item title")


def _token() -> str:
    return Path(ABS_API_TOKEN_FILE).read_text().strip()


def _to_bookmark(raw: dict[str, Any]) -> AbsBookmark:
    """Map one `/api/me` bookmark dict to the model. Isolated so a schema
    drift is a one-line fix, fixture-tested in tests/test_abs_bookmarks.py.
    """
    return AbsBookmark(
        library_item_id=str(raw.get("libraryItemId", "")),
        time_s=float(raw.get("time", 0) or 0),
        note=str(raw.get("title", "") or ""),
        created_at=int(raw.get("createdAt", 0) or 0),
    )


def _item_title(session: requests.Session, library_item_id: str) -> str:
    r = session.get(
        f"{ABS_URL}/api/items/{library_item_id}",
        params={"expanded": 1},
        timeout=30,
    )
    if r.status_code != 200:
        return ""
    return (
        r.json().get("media", {}).get("metadata", {}).get("title", "") or ""
    )


def get_bookmarks(
    *, citation_key: str | None = None
) -> list[AbsBookmark]:
    """Return the current user's ABS bookmarks, newest first.

    Args:
        citation_key: When given, keep only bookmarks whose resolved item
            title contains the key (case-insensitive).

    Returns:
        Bookmarks sorted by `created_at` descending.
    """
    s = requests.Session()
    s.headers["Authorization"] = f"Bearer {_token()}"
    me = s.get(f"{ABS_URL}/api/me", timeout=30).json()
    out: list[AbsBookmark] = []
    title_cache: dict[str, str] = {}
    for raw in me.get("bookmarks", []):
        bm = _to_bookmark(raw)
        if bm.library_item_id not in title_cache:
            title_cache[bm.library_item_id] = _item_title(
                s, bm.library_item_id
            )
        bm.item_title = title_cache[bm.library_item_id]
        if citation_key and citation_key.lower() not in (
            bm.item_title.lower() + " " + bm.note.lower()
        ):
            continue
        out.append(bm)
    out.sort(key=lambda b: b.created_at, reverse=True)
    return out


def main() -> None:
    """CLI: list ABS bookmarks, optionally filtered by citation key."""
    p = argparse.ArgumentParser(description="Fetch Audiobookshelf bookmarks")
    p.add_argument("--citation-key", default=None)
    p.add_argument("--json", action="store_true", help="Emit JSON")
    args = p.parse_args()
    bms = get_bookmarks(citation_key=args.citation_key)
    if args.json:
        print(
            "[" + ",".join(b.model_dump_json() for b in bms) + "]"
        )
        return
    for b in bms:
        t = int(b.time_s)
        print(
            f"[{b.item_title}] @ {t // 60}:{t % 60:02d}  item={b.library_item_id}"
        )
        print(f"  {b.note}")


if __name__ == "__main__":
    main()
