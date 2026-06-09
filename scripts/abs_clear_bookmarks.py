"""
scripts/abs_clear_bookmarks.py
[[scripts.abs_clear_bookmarks]]
https://github.com/Mjvolk3/Swanki/tree/main/scripts/abs_clear_bookmarks.py
Test file: tests/test_abs_bookmarks.py

Thin CLI shim over ``swanki/abs/bookmarks.py``. The clear-and-re-mark
rationale stands (bookmark times are absolute offsets into the item's global
timeline; ABS does not re-map them when a track is swapped, so clearing beats
migrating timestamps) -- the mechanism gained the windowed wipe-on-replace
default: ``--window START_S END_S`` (repeatable) deletes only bookmarks inside
the replaced audio's item-global windows. Omit windows for the legacy
whole-item clear.

Dry-run by default -- pass ``--yes`` to actually delete (irreversible; archive
bookmark notes first).
"""

import argparse

from swanki.abs.bookmarks import clear_bookmarks


def main() -> None:
    """CLI: clear ABS bookmarks for a citation key (dry-run unless --yes)."""
    p = argparse.ArgumentParser(description="Clear Audiobookshelf bookmarks")
    p.add_argument("--citation-key", required=True)
    p.add_argument(
        "--window",
        nargs=2,
        action="append",
        metavar=("START_S", "END_S"),
        help="item-global window; repeatable; omit for whole-item clear",
    )
    p.add_argument(
        "--yes", action="store_true", help="Actually delete (default: dry run)"
    )
    args = p.parse_args()
    windows = (
        [(float(s), float(e)) for s, e in args.window] if args.window else None
    )
    clear_bookmarks(
        citation_key=args.citation_key, windows=windows, dry_run=not args.yes
    )


if __name__ == "__main__":
    main()
