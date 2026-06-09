"""
swanki/abs/collections.py
[[swanki.abs.collections]]
https://github.com/Mjvolk3/Swanki/tree/main/swanki/abs/collections.py
Test file: tests/test_abs_projections.py

Mirror Zotero collections as ABS collections (refresh step 3). For each
projection: fetch tag-filtered items, invert ``item.data.collections`` to
{zotero_collection -> [items]} (an item in multiple Zotero collections shows
up in multiple ABS collections, mirroring Zotero semantics), then upsert one
ABS collection per (zotero collection x audiotype) into the matching library.

Reconcile-don't-wipe (load-bearing): existing ABS collections matched by name
have their book list reconciled -- additions AND removals in Zotero propagate
-- while ABS collections whose names match no Zotero collection are left
untouched, so manually-curated collections safely coexist.

The manifest-driven ``scripts/abs_setup_collections.py`` (citekey lists in
projections.yml) was absorbed-by-deletion: it was referenced by nothing and
the Zotero mirror supersedes it.
"""

from collections import defaultdict
from typing import Any

from swanki.abs.client import ABSClient
from swanki.abs.libraries import build_library_index, library_items_by_title
from swanki.abs.projections import (
    citation_key,
    classify,
    group_key,
    resolve_library,
)
from swanki.abs.sync import fetch_items
from swanki.sync.zotero_client import make_zotero_client


def upsert_collection(
    client: ABSClient,
    library_id: str,
    name: str,
    item_ids: list[str],
    existing_by_name: dict[str, dict[str, Any]],
) -> str:
    """Create or reconcile one ABS collection to exactly ``item_ids``."""
    if name in existing_by_name:
        coll_id = existing_by_name[name]["id"]
        current = set(client.collection_books(coll_id))
        target = set(item_ids)
        for book_id in target - current:
            client.add_collection_book(coll_id, book_id)
        for book_id in current - target:
            client.remove_collection_book(coll_id, book_id)
        return "updated"

    if not item_ids:
        return "skipped (empty)"
    client.create_collection(library_id, name, item_ids)
    return "created"


def mirror_zotero_collections(
    client: ABSClient,
    projections: dict[str, dict[str, Any]],
    zotero_api_key: str,
) -> None:
    """Mirror every projection's Zotero collections into ABS."""
    lib_index = build_library_index(client)
    all_abs_collections = client.collections()
    items_cache: dict[str, dict[str, str]] = {}

    for proj_name, cfg in projections.items():
        lib_id, lib_type = resolve_library(cfg["zotero"])
        tag = cfg["zotero"].get("tag")
        audiotypes = cfg["audiotypes"]

        print(f"\n=== Projection: {proj_name} ===")
        zot = make_zotero_client(lib_id, lib_type, zotero_api_key)
        zot_colls = {c["key"]: c["data"]["name"] for c in zot.collections()}
        items = fetch_items(zot, tag)
        print(f"  {len(items)} item(s), {len(zot_colls)} zotero collection(s)")

        coll_members: dict[str, list[tuple[str, str]]] = defaultdict(list)
        for item in items:
            kind = classify(item)
            ckey = citation_key(item)
            if not ckey:
                continue
            group = group_key(ckey, kind)
            for coll_key in item["data"].get("collections", []):
                coll_members[coll_key].append((kind, group))

        for coll_key, members in coll_members.items():
            coll_name = zot_colls.get(coll_key, coll_key)
            groups_by_kind: dict[str, set[str]] = defaultdict(set)
            for kind, group in members:
                groups_by_kind[kind].add(group)

            for kind, groups in groups_by_kind.items():
                for audiotype in audiotypes:
                    target_lib = lib_index.get(
                        (proj_name, kind, audiotype.lower())
                    )
                    if not target_lib:
                        continue
                    if target_lib not in items_cache:
                        items_cache[target_lib] = library_items_by_title(
                            client, target_lib
                        )
                    abs_items = items_cache[target_lib]
                    matched = [abs_items[g] for g in groups if g in abs_items]
                    missing_ct = sum(1 for g in groups if g not in abs_items)

                    abs_name = f"{coll_name} — {audiotype.capitalize()}"
                    existing_by_name = {
                        c["name"]: c
                        for c in all_abs_collections
                        if c.get("libraryId") == target_lib
                    }
                    action = upsert_collection(
                        client, target_lib, abs_name, matched, existing_by_name
                    )
                    note = f"  (missing: {missing_ct})" if missing_ct else ""
                    print(
                        f"  {action}: {abs_name}  [{len(matched)} items]{note}"
                    )
