"""
scripts/abs_clear_bookmarks.py
[[scripts.abs_clear_bookmarks]]
https://github.com/Mjvolk3/Swanki/tree/main/scripts/abs_clear_bookmarks.py
Test file: tests/test_abs_clear_bookmarks.py

Bulk-clear the current user's Audiobookshelf bookmarks for an item, keyed by
citation key. Use after replacing/regenerating a chapter: bookmark times are
absolute offsets into the item's global timeline and ABS does not re-map them
when a track is swapped, so the "clear and re-mark" workflow is preferred over
migrating timestamps. Reuses `get_bookmarks` + the token loader from
`scripts/abs_bookmarks.py`; deletion via `DELETE /api/me/item/{id}/bookmark/{time}`.

Dry-run by default -- pass `--yes` to actually delete.
"""

import argparse

import requests

from scripts.abs_bookmarks import ABS_URL, _token, get_bookmarks


def clear_bookmarks(*, citation_key: str, dry_run: bool = True) -> int:
    """Delete every ABS bookmark whose item matches `citation_key`.

    Args:
        citation_key: Substring matched (case-insensitive) against item title /
            note by `get_bookmarks`.
        dry_run: When True, list what would be deleted and delete nothing.

    Returns:
        Count of bookmarks deleted (0 in dry-run).
    """
    bms = get_bookmarks(citation_key=citation_key)
    print(f"{len(bms)} bookmark(s) match '{citation_key}':")
    for b in bms:
        t = int(b.time_s)
        print(f"  [{b.item_title}] @ {t // 60}:{t % 60:02d}  {b.note[:70]}")
    if dry_run:
        print("\nDRY RUN -- nothing deleted. Re-run with --yes to clear.")
        return 0

    s = requests.Session()
    s.headers["Authorization"] = f"Bearer {_token()}"
    deleted = 0
    for b in bms:
        tv = int(b.time_s) if b.time_s == int(b.time_s) else b.time_s
        r = s.delete(
            f"{ABS_URL}/api/me/item/{b.library_item_id}/bookmark/{tv}",
            timeout=30,
        )
        r.raise_for_status()
        deleted += 1
    print(f"\nDeleted {deleted} bookmark(s).")
    return deleted


def main() -> None:
    """CLI: clear ABS bookmarks for a citation key (dry-run unless --yes)."""
    p = argparse.ArgumentParser(description="Clear Audiobookshelf bookmarks")
    p.add_argument("--citation-key", required=True)
    p.add_argument(
        "--yes", action="store_true", help="Actually delete (default: dry run)"
    )
    args = p.parse_args()
    clear_bookmarks(citation_key=args.citation_key, dry_run=not args.yes)


if __name__ == "__main__":
    main()
