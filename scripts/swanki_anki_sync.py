"""
scripts/swanki_anki_sync.py
[[scripts.swanki_anki_sync]]
https://github.com/Mjvolk3/Swanki/tree/main/scripts/swanki_anki_sync.py
Test file: tests/test_swanki_anki_sync.py

The walk-all manual "push to anki" command (Sync Terminology). For each
projection where ``push_anki`` is truthy it walks fox-tagged Zotero items,
resolves the newest ``.apkg`` per chapter, imports each via AnkiConnect, then
triggers one AnkiWeb sync at the end.

The AnkiConnect primitives (``ankiconnect_call``, ``verify_ankiconnect``, the
request/response models) now live in the installed package at
``swanki/delivery/targets/anki.py`` and are imported here so the queue's
per-item delivery and this manual command share one implementation. The
per-item delivery path is ``python -m swanki.delivery``.

Prerequisites (see ``notes/anki.headless-sync.md``): a headless Anki with the
AnkiConnect addon reachable at ``http://127.0.0.1:8765`` (env ``ANKI_HOST`` /
``ANKI_PORT``); for Flatpak Anki the staging dir must be in the
``--filesystem`` allowlist.
"""

import argparse
import os
import sys
from pathlib import Path
from typing import Any

from _swanki_zotero_artifacts import latest_apkgs
from dotenv import load_dotenv
from pyzotero import zotero
from swanki_abs_sync import (
    DEFAULT_PROJECTIONS,
    citation_key,
    fetch_items,
    load_projections,
    resolve_library,
)

from swanki.delivery.targets.anki import (
    ANKICONNECT_VERSION as ANKICONNECT_VERSION,
)
from swanki.delivery.targets.anki import (
    AnkiConnectRequest as AnkiConnectRequest,
)
from swanki.delivery.targets.anki import (
    AnkiConnectResponse as AnkiConnectResponse,
)
from swanki.delivery.targets.anki import (
    ImportPackageParams,
    ankiconnect_call,
    verify_ankiconnect,
)

load_dotenv()

DEFAULT_STAGE_ROOT = Path("/scratch/Swanki_Anki_Stage")


def push_projection(
    name: str,
    cfg: dict[str, Any],
    api_key: str,
    url: str,
    stage_root: Path,
    dry_run: bool,
) -> int:
    """Resolve and import the latest apkg per fox-tagged item in one projection.

    Args:
        name: Projection name (log prefix + staging subdir).
        cfg: Raw projection config dict (same shape ``swanki_abs_sync`` reads).
        api_key: Zotero API key.
        url: AnkiConnect endpoint URL.
        stage_root: Absolute staging-dir root; subdir ``<projection>/`` is made.
        dry_run: When true, print the plan and skip downloads + POSTs.

    Returns:
        Count of attachments successfully imported (or planned, in dry-run).
    """
    if not cfg.get("push_anki", True):
        print(f"\n=== Projection: {name} -- push_anki=false, skipping anki ===")
        return 0

    lib_id, lib_type = resolve_library(cfg["zotero"])
    tag = cfg["zotero"].get("tag")
    stage_dir = (stage_root / name).resolve()
    stage_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n=== Projection: {name} (Zotero {lib_type}/{lib_id}, tag={tag!r}) ===")
    zot = zotero.Zotero(lib_id, lib_type, api_key)
    items = fetch_items(zot, tag)
    print(f"  {len(items)} item(s) matched")

    imported = 0
    for item in items:
        ckey = citation_key(item)
        if not ckey:
            continue
        for att in latest_apkgs(zot, item["key"]):
            filename = att["data"]["filename"]
            target = stage_dir / filename
            if dry_run:
                print(f"  [dry-run] + {ckey}: would import {target}")
                imported += 1
                continue
            try:
                content = zot.file(att["key"])
            except Exception as e:
                # Stale attachment metadata pointing to a missing file; skip
                # instead of aborting the projection.
                print(f"  ! {ckey}: skipping {filename} (key={att['key']}): {e}")
                continue
            target.write_bytes(content)
            ankiconnect_call(
                url, "importPackage", ImportPackageParams(path=str(target)).model_dump()
            )
            print(f"  + {ckey}: imported {filename}")
            imported += 1
    print(f"  imported {imported} apkg(s)")
    return imported


def main() -> None:
    """CLI entry. Push enabled projections, then trigger one AnkiWeb sync."""
    parser = argparse.ArgumentParser(
        description=(
            "Push latest .apkg per Zotero item to AnkiConnect, "
            "then sync once at the end."
        )
    )
    parser.add_argument(
        "projections_path",
        nargs="?",
        type=Path,
        default=DEFAULT_PROJECTIONS,
        help="Path to projections YAML (default: %(default)s)",
    )
    parser.add_argument(
        "--projection",
        metavar="NAME",
        help="Limit to a single projection; default = all push_anki-enabled.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the resolved plan without downloading or POSTing.",
    )
    args = parser.parse_args()

    host = os.environ.get("ANKI_HOST", "127.0.0.1")
    port = int(os.environ.get("ANKI_PORT", "8765"))
    url = f"http://{host}:{port}"
    stage_root = Path(os.environ.get("SWANKI_ANKI_STAGE", str(DEFAULT_STAGE_ROOT)))
    api_key = os.environ["ZOTERO_API_KEY"]
    projections = load_projections(args.projections_path)

    if args.projection:
        if args.projection not in projections:
            sys.exit(
                f"projection {args.projection!r} not found in {args.projections_path}"
            )
        projections = {args.projection: projections[args.projection]}

    # Fail-fast ping before touching Zotero.
    version = verify_ankiconnect(url)
    print(f"AnkiConnect {url} -- version {version}")

    total = 0
    for name, cfg in projections.items():
        total += push_projection(name, cfg, api_key, url, stage_root, args.dry_run)

    if total == 0:
        print("\nNothing to import; skipping final sync.")
        return

    if args.dry_run:
        print("\n[dry-run] would POST sync to AnkiConnect")
        return

    print("\nTriggering AnkiWeb sync ...")
    ankiconnect_call(url, "sync")
    print("sync ok")


if __name__ == "__main__":
    main()
