"""
swanki/abs/__main__.py
[[swanki.abs.__main__]]
https://github.com/Mjvolk3/Swanki/tree/main/swanki/abs/__main__.py
Test file: tests/test_abs_refresh.py

CLI entry for the ABS module (mirrors ``python -m swanki.delivery``):

    python -m swanki.abs refresh [--wait]
    python -m swanki.abs refresh --target KEY --output-dir DIR
    python -m swanki.abs bookmarks --citation-key KEY [--json]
    python -m swanki.abs clear-bookmarks --citation-key KEY \
        [--window START END]... [--yes]

``refresh`` defaults to non-blocking (cron parity: skip when another refresh
holds the lock); ``--wait`` blocks (delivery parity). The targeted form
(``--target``) is always blocking -- the publish path must never silently
no-op. ``clear-bookmarks`` is dry-run unless ``--yes``.
"""

import argparse
import sys
from pathlib import Path

from dotenv import load_dotenv


def _cmd_refresh(args: argparse.Namespace) -> int:
    from swanki.abs.refresh import full_refresh, targeted_refresh

    projections_path = Path(args.projections) if args.projections else None
    if args.target:
        if not args.output_dir:
            sys.exit("refresh --target requires --output-dir")
        result = targeted_refresh(
            citation_key=args.target,
            output_dir=Path(args.output_dir),
            projections_path=projections_path,
        )
        print(result.model_dump_json(indent=2))
        return 0
    ran = full_refresh(wait=args.wait, projections_path=projections_path)
    return 0 if ran or not args.wait else 1


def _cmd_bookmarks(args: argparse.Namespace) -> int:
    from swanki.abs.bookmarks import get_bookmarks

    bms = get_bookmarks(citation_key=args.citation_key)
    if args.json:
        print("[" + ",".join(b.model_dump_json() for b in bms) + "]")
        return 0
    for b in bms:
        t = int(b.time_s)
        print(
            f"[{b.item_title}] @ {t // 60}:{t % 60:02d}  "
            f"item={b.library_item_id}"
        )
        print(f"  {b.note}")
    return 0


def _cmd_clear_bookmarks(args: argparse.Namespace) -> int:
    from swanki.abs.bookmarks import clear_bookmarks

    windows = (
        [(float(s), float(e)) for s, e in args.window] if args.window else None
    )
    clear_bookmarks(
        citation_key=args.citation_key,
        windows=windows,
        dry_run=not args.yes,
    )
    return 0


def main(argv: list[str] | None = None) -> int:
    """Parse args and dispatch the ABS subcommand."""
    load_dotenv()
    parser = argparse.ArgumentParser(prog="python -m swanki.abs")
    sub = parser.add_subparsers(dest="cmd", required=True)

    r = sub.add_parser("refresh", help="full (default) or targeted refresh")
    r.add_argument(
        "--wait",
        action="store_true",
        help="block for the lock instead of skipping (delivery semantics)",
    )
    r.add_argument("--target", default=None, metavar="CITATION_KEY")
    r.add_argument("--output-dir", default=None)
    r.add_argument("--projections", default=None, help="projections.yml path")
    r.set_defaults(func=_cmd_refresh)

    b = sub.add_parser("bookmarks", help="list ABS bookmarks")
    b.add_argument("--citation-key", default=None)
    b.add_argument("--json", action="store_true", help="Emit JSON")
    b.set_defaults(func=_cmd_bookmarks)

    cb = sub.add_parser(
        "clear-bookmarks", help="delete bookmarks (dry-run unless --yes)"
    )
    cb.add_argument("--citation-key", required=True)
    cb.add_argument(
        "--window",
        nargs=2,
        action="append",
        metavar=("START_S", "END_S"),
        help="item-global window; repeatable; omit for whole-item clear",
    )
    cb.add_argument(
        "--yes", action="store_true", help="Actually delete (default: dry run)"
    )
    cb.set_defaults(func=_cmd_clear_bookmarks)

    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    sys.exit(main())
