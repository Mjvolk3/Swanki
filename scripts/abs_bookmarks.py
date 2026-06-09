"""
scripts/abs_bookmarks.py
[[scripts.abs_bookmarks]]
https://github.com/Mjvolk3/Swanki/tree/main/scripts/abs_bookmarks.py
Test file: tests/test_abs_bookmarks.py

Thin re-export shim. The bookmark fetcher moved into the installed package at
``swanki/abs/bookmarks.py`` (one ABSClient, one token chain). This module
keeps the historical import path (``from scripts.abs_bookmarks import
get_bookmarks``) and CLI that the audio-fix-from-annotations skill uses.

NOTE: an ABS bookmark ``time`` is the playhead WHEN THE NOTE WAS SAVED -- it
lags the actual issue by minutes. Use it only to pick the chapter/file;
locate the chunk by content-match + the chunk_timeline sidecar.
"""

import argparse
import os
from pathlib import Path

from dotenv import load_dotenv

from swanki.abs.bookmarks import (
    AbsBookmark as AbsBookmark,
)
from swanki.abs.bookmarks import (
    _to_bookmark as _to_bookmark,
)
from swanki.abs.bookmarks import (
    get_bookmarks as get_bookmarks,
)
from swanki.abs.client import DEFAULT_ABS_URL
from swanki.abs.client import load_token as _token  # noqa: F401

load_dotenv(dotenv_path=str(Path.cwd() / ".env"))

ABS_URL = os.environ.get("ABS_URL", DEFAULT_ABS_URL)


def main() -> None:
    """CLI: list ABS bookmarks, optionally filtered by citation key."""
    p = argparse.ArgumentParser(description="Fetch Audiobookshelf bookmarks")
    p.add_argument("--citation-key", default=None)
    p.add_argument("--json", action="store_true", help="Emit JSON")
    args = p.parse_args()
    bms = get_bookmarks(citation_key=args.citation_key)
    if args.json:
        print("[" + ",".join(b.model_dump_json() for b in bms) + "]")
        return
    for b in bms:
        t = int(b.time_s)
        print(
            f"[{b.item_title}] @ {t // 60}:{t % 60:02d}  item={b.library_item_id}"
        )
        print(f"  {b.note}")


if __name__ == "__main__":
    main()
