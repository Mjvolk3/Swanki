"""
scripts/abs_sync_zotero_collections.py
[[scripts.abs_sync_zotero_collections]]
https://github.com/Mjvolk3/Swanki/tree/main/scripts/abs_sync_zotero_collections.py

Mirror Zotero collections as ABS collections.

For each projection in ``infra/abs/projections.yml``:

    1. Fetch tag-filtered items from the projection's Zotero library
    2. Invert ``item.data.collections`` to {zotero_collection → [items]}
       — an item in multiple Zotero collections shows up in multiple
       ABS collections (mirrors Zotero semantics)
    3. For each Zotero collection with items, for each audiotype, upsert
       an ABS collection named ``"<zotero name> — <Audiotype>"`` in the
       matching audiobook library.

Re-runnable: existing ABS collections (matched by name) have their book
list reconciled — additions and removals in Zotero propagate. ABS
collections whose names don't match any Zotero collection are left
untouched (safe for manually-curated collections coexisting).
"""

import json
import os
import re
import sys
import urllib.request
from collections import defaultdict
from pathlib import Path

import yaml
from dotenv import load_dotenv
from pyzotero import zotero

load_dotenv()

DEFAULT_ABS_URL = "https://abs.michaelvolk.dev"
DEFAULT_PROJECTIONS = (
    Path.home() / "Documents/projects/infra/abs/projections.yml"
)
BOOK_TYPES = {"book", "bookSection"}
CHAPTER_SUFFIX = re.compile(r"_CH\d+_.*$")


def load_token() -> str:
    token_file = os.environ.get("ABS_API_TOKEN_FILE")
    if token_file:
        return Path(token_file).expanduser().read_text().strip()
    token = os.environ.get("ABS_API_TOKEN")
    if token:
        return token.strip()
    raise SystemExit(
        "Set ABS_API_TOKEN_FILE (path to token file) or ABS_API_TOKEN."
    )


def api(base, token, method, path, body=None):
    url = f"{base.rstrip('/')}{path}"
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(
        url,
        data=data,
        method=method,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "swanki-abs-setup/1.0",
        },
    )
    with urllib.request.urlopen(req) as resp:
        raw = resp.read().decode()
    return json.loads(raw) if raw else {}


def resolve_library(cfg):
    if "library_id" in cfg:
        return str(cfg["library_id"]), cfg.get("library_type", "user")
    return os.environ[cfg["library_id_env"]], cfg.get("library_type", "user")


def citation_key(item):
    key = item["data"].get("citationKey", "") or ""
    if key:
        return key
    extra = item["data"].get("extra", "")
    m = re.search(r"Citation Key:\s*(\S+)", extra)
    return m.group(1) if m else item["key"]


def classify(item):
    return "Book" if item["data"].get("itemType") in BOOK_TYPES else "Paper"


def group_key(citekey, kind):
    if kind == "Book":
        return CHAPTER_SUFFIX.sub("", citekey)
    return citekey


def fetch_items(zot, tag):
    items, start, limit = [], 0, 100
    while True:
        batch = (
            zot.items(tag=tag, start=start, limit=limit)
            if tag
            else zot.items(start=start, limit=limit)
        )
        if not batch:
            break
        items.extend(batch)
        start += limit
        if len(batch) < limit:
            break
    return items


def fetch_collection_names(zot):
    return {c["key"]: c["data"]["name"] for c in zot.collections()}


def build_library_index(base, token):
    data = api(base, token, "GET", "/api/libraries")
    libs = data.get("libraries", data) if isinstance(data, dict) else data
    index = {}
    for lib in libs:
        for folder in lib.get("folders", []):
            path = folder.get("fullPath", "")
            parts = path.strip("/").split("/")
            if len(parts) < 3 or not parts[-1].startswith("Swanki-"):
                continue
            segments = parts[-1].split("-", 2)
            if len(segments) != 3:
                continue
            _, kind, audiotype = segments
            index[(parts[-2], kind, audiotype)] = lib["id"]
    return index


def list_library_items(base, token, library_id):
    data = api(
        base, token, "GET",
        f"/api/libraries/{library_id}/items?limit=10000",
    )
    results = data.get("results", data) if isinstance(data, dict) else data
    items = {}
    for item in results:
        media = item.get("media", {})
        metadata = media.get("metadata", {})
        title = metadata.get("title") or item.get("path", "").split("/")[-1]
        if title:
            items[title] = item["id"]
    return items


def list_collections(base, token):
    data = api(base, token, "GET", "/api/collections")
    return data.get("collections", data) if isinstance(data, dict) else data


def collection_books(base, token, coll_id):
    data = api(base, token, "GET", f"/api/collections/{coll_id}")
    return [b["id"] for b in data.get("books", [])]


def upsert_collection(base, token, library_id, name, item_ids, existing_by_name):
    if name in existing_by_name:
        coll_id = existing_by_name[name]["id"]
        current = set(collection_books(base, token, coll_id))
        target = set(item_ids)
        for book_id in target - current:
            api(base, token, "POST",
                f"/api/collections/{coll_id}/book", {"id": book_id})
        for book_id in current - target:
            api(base, token, "DELETE",
                f"/api/collections/{coll_id}/book/{book_id}")
        return "updated"

    if not item_ids:
        return "skipped (empty)"
    api(base, token, "POST", "/api/collections", {
        "libraryId": library_id,
        "name": name,
        "books": item_ids,
    })
    return "created"


def main():
    base = os.environ.get("ABS_URL", DEFAULT_ABS_URL)
    projections_path = Path(
        sys.argv[1] if len(sys.argv) > 1 else DEFAULT_PROJECTIONS
    )
    with projections_path.open() as f:
        projections = yaml.safe_load(f)["projections"]

    token = load_token()
    zotero_api_key = os.environ["ZOTERO_API_KEY"]
    lib_index = build_library_index(base, token)
    all_abs_collections = list_collections(base, token)
    items_cache: dict[str, dict[str, str]] = {}

    for proj_name, cfg in projections.items():
        lib_id, lib_type = resolve_library(cfg["zotero"])
        tag = cfg["zotero"].get("tag")
        audiotypes = cfg["audiotypes"]

        print(f"\n=== Projection: {proj_name} ===")
        zot = zotero.Zotero(lib_id, lib_type, zotero_api_key)
        zot_colls = fetch_collection_names(zot)
        items = fetch_items(zot, tag)
        print(
            f"  {len(items)} item(s), "
            f"{len(zot_colls)} zotero collection(s)"
        )

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
                        (proj_name, kind, audiotype.capitalize())
                    )
                    if not target_lib:
                        continue
                    if target_lib not in items_cache:
                        items_cache[target_lib] = list_library_items(
                            base, token, target_lib
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
                        base, token, target_lib, abs_name, matched,
                        existing_by_name,
                    )
                    note = f"  (missing: {missing_ct})" if missing_ct else ""
                    print(
                        f"  {action}: {abs_name}  "
                        f"[{len(matched)} items]{note}"
                    )


if __name__ == "__main__":
    main()
