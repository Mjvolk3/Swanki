"""
scripts/zotero_backfill_processed_tags.py
[[scripts.zotero_backfill_processed_tags]]
https://github.com/Mjvolk3/Swanki/tree/main/scripts/zotero_backfill_processed_tags.py

Backfill Swanki processing-state tags on Zotero items.

For every item whose children include at least one Swanki-style zip
(``{key}-{YYYYMMDDTHHMM}-{shorthash}.zip``):

  - add the 🦊 tag if missing — older uploads predate the auto-tagging
    code, and any single failed Zotero call after a successful upload
    can also leave the tag missing.
  - remove the 💸 tag if present — that tag flags items still awaiting
    processing, so once a Swanki zip exists it is no longer needed.

Defaults to dry-run; pass ``--apply`` to mutate Zotero. Set
``--library-id`` / ``--library-type`` to override the env-var defaults.

Run:
    python scripts/zotero_backfill_processed_tags.py            # dry-run
    python scripts/zotero_backfill_processed_tags.py --apply    # commit
"""

import argparse
import os
import re
import sys

from dotenv import load_dotenv
from pyzotero import zotero

load_dotenv()

ZIP_PATTERN = re.compile(
    r"^(?P<key>.+)-(?P<ts>\d{8}T\d{4})-(?P<hash>[a-f0-9]+)\.zip$"
)
PROCESSED_TAG = "🦊"
PENDING_TAG = "💸"


def fetch_all(zot: zotero.Zotero, **kwargs: object) -> list[dict]:
    items, start, limit = [], 0, 100
    while True:
        batch = zot.items(start=start, limit=limit, **kwargs)  # type: ignore[arg-type]
        if not isinstance(batch, list) or not batch:
            break
        items.extend(batch)
        start += limit
        if len(batch) < limit:
            break
    return items


def parents_with_swanki_zip(zot: zotero.Zotero) -> set[str]:
    """Single bulk pass over all attachments → set of parent keys that
    have at least one Swanki-style zip child."""
    parents: set[str] = set()
    attachments = fetch_all(zot, itemType="attachment")
    for att in attachments:
        d = att.get("data", {})
        name = d.get("filename", "") or ""
        if not name.endswith(".zip") or not ZIP_PATTERN.match(name):
            continue
        parent_key = d.get("parentItem")
        if parent_key:
            parents.add(parent_key)
    return parents


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n", 1)[0])
    ap.add_argument("--apply", action="store_true", help="actually mutate Zotero")
    ap.add_argument(
        "--library-id",
        default=os.environ.get("ZOTERO_LIBRARY_ID"),
        help="Zotero library id (default: $ZOTERO_LIBRARY_ID)",
    )
    ap.add_argument(
        "--library-type",
        default=os.environ.get("ZOTERO_LIBRARY_TYPE", "user"),
        choices=("user", "group"),
    )
    args = ap.parse_args()

    api_key = os.environ.get("ZOTERO_API_KEY")
    if not api_key or not args.library_id:
        print(
            "error: ZOTERO_API_KEY and a library id are required",
            file=sys.stderr,
        )
        return 1

    zot = zotero.Zotero(args.library_id, args.library_type, api_key)
    mode = "APPLY" if args.apply else "DRY-RUN"
    print(
        f"[{mode}] library={args.library_type}/{args.library_id}  "
        f"add={PROCESSED_TAG!r}  remove={PENDING_TAG!r}"
    )

    parent_keys = parents_with_swanki_zip(zot)
    print(f"  found {len(parent_keys)} item(s) with a Swanki zip")

    added = removed = 0
    for parent_key in sorted(parent_keys):
        try:
            it = zot.item(parent_key)
        except Exception as e:
            print(f"  warn: skip {parent_key} ({e})")
            continue
        d = it.get("data", {})
        if d.get("itemType") in ("attachment", "note"):
            continue
        tags = list(d.get("tags", []))
        existing = {t["tag"] for t in tags}
        new_tags = [t for t in tags if t["tag"] != PENDING_TAG]
        will_remove = PENDING_TAG in existing
        will_add = PROCESSED_TAG not in existing
        if will_add:
            new_tags.append({"tag": PROCESSED_TAG})
        if not (will_add or will_remove):
            continue
        ck = d.get("citationKey") or parent_key
        ops = []
        if will_add:
            ops.append(f"+{PROCESSED_TAG}")
            added += 1
        if will_remove:
            ops.append(f"-{PENDING_TAG}")
            removed += 1
        print(f"  {' '.join(ops):<6}  {ck}")
        if args.apply:
            it["data"]["tags"] = new_tags
            zot.update_item(it)

    print(
        f"\nsummary: {PROCESSED_TAG} added on {added} item(s), "
        f"{PENDING_TAG} removed from {removed} item(s)"
    )
    if not args.apply:
        print("(dry-run — re-run with --apply to commit)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
