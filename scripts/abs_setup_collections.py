"""
scripts/abs_setup_collections.py
[[scripts.abs_setup_collections]]
https://github.com/Mjvolk3/Swanki/tree/main/scripts/abs_setup_collections.py

Declarative ABS collection setup.

Reads the ``collections:`` section of each projection in
``infra/abs/projections.yml`` and materializes ABS Collections via the REST
API. Each manifest entry spawns one collection per requested audiotype,
scoped to the audiotype's library (e.g. a "Genomic LMs" entry with
``audiotypes: [summary, lecture]`` creates two collections — one in
``Paper — Summary``, one in ``Paper — Lecture``).

Re-runnable: existing collections have their book list reconciled (missing
items added, orphans removed). Missing citekeys are logged, not fatal.

Manifest shape:

    projections:
      <name>:
        audiotypes: [summary, reading, lecture]
        collections:
          - name: "Genomic Language Models"
            kind: Paper          # Paper or Book
            audiotypes: [summary, lecture]   # optional, defaults to projection's
            citekeys:
              - zvyaginGenSLMsGenomescaleLanguage2023
              - cuiScGPTBuildingFoundation2024
"""

import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

import yaml

DEFAULT_ABS_URL = "https://abs.michaelvolk.dev"
DEFAULT_PROJECTIONS = (
    Path.home() / "Documents/projects/infra/abs/projections.yml"
)


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


def build_library_index(base, token):
    """Map (projection, kind, audiotype) -> library_id from folder paths."""
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
            index[(parts[-2], kind, audiotype.lower())] = lib["id"]
    return index


def list_library_items(base, token, library_id):
    """Map folder-name/title -> item_id for items in a library."""
    data = api(base, token, "GET", f"/api/libraries/{library_id}/items?limit=10000")
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
    colls = data.get("collections", data) if isinstance(data, dict) else data
    return colls


def collection_books(base, token, collection_id):
    data = api(base, token, "GET", f"/api/collections/{collection_id}")
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
    lib_index = build_library_index(base, token)
    all_collections = list_collections(base, token)

    items_cache: dict[str, dict[str, str]] = {}

    for proj_name, cfg in projections.items():
        collections = cfg.get("collections") or []
        if not collections:
            print(f"[{proj_name}] no collections defined, skipping")
            continue

        print(f"\n=== Projection: {proj_name} ===")
        for entry in collections:
            topic = entry["name"]
            kind = entry["kind"]
            audiotypes = entry.get("audiotypes") or cfg["audiotypes"]
            citekeys = entry["citekeys"]

            for audiotype in audiotypes:
                lib_id = lib_index.get((proj_name, kind, audiotype.capitalize()))
                if not lib_id:
                    print(f"  ! no {kind}/{audiotype} library for {proj_name}")
                    continue
                if lib_id not in items_cache:
                    items_cache[lib_id] = list_library_items(base, token, lib_id)
                items = items_cache[lib_id]

                matched = [items[ck] for ck in citekeys if ck in items]
                missing = [ck for ck in citekeys if ck not in items]

                name = f"{topic} — {audiotype.capitalize()}"
                existing_by_name = {
                    c["name"]: c
                    for c in all_collections
                    if c.get("libraryId") == lib_id
                }
                action = upsert_collection(
                    base, token, lib_id, name, matched, existing_by_name
                )
                note = (
                    f"  (missing: {', '.join(missing)})" if missing else ""
                )
                print(f"  {action}: {name}  [{len(matched)} items]{note}")


if __name__ == "__main__":
    main()
