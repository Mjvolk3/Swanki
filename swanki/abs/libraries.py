"""
swanki/abs/libraries.py
[[swanki.abs.libraries]]
https://github.com/Mjvolk3/Swanki/tree/main/swanki/abs/libraries.py
Test file: tests/test_abs_projections.py

ABS library setup + lookup helpers (refresh step 2 and shared routing).

``ensure_libraries`` idempotently creates the per-projection audiobook
libraries that ``sync`` populates (``/audiobooks/<proj>/Swanki-<Kind>-<Type>``;
existing folders are left untouched). ``build_library_index`` inverts the ABS
folder layout into ``(projection, kind, audiotype) -> library_id`` -- audiotype
is normalized to lowercase on both store and lookup (the legacy scripts
disagreed on case, which left ``abs_setup_collections.py`` lookups silently
missing). ``library_items_by_title`` maps item title/folder-name -> item id;
folder name == citation key (group key for books) is the contract that ties
ABS items back to Zotero -- unmatched folders are intentionally skippable so
non-swanki items can coexist in the same libraries.
"""

from typing import Any

from swanki.abs.client import ABSClient

KINDS = ("Paper", "Book")


def ensure_libraries(
    client: ABSClient, projections: dict[str, dict[str, Any]]
) -> int:
    """Idempotently create each projection's audiobook libraries.

    Returns:
        Count of libraries created (existing folders are skipped).
    """
    libs = client.libraries()
    by_folder = {
        folder["fullPath"]: lib
        for lib in libs
        for folder in lib.get("folders", [])
    }
    existing_names = {lib["name"] for lib in libs}
    print(f"Found {len(libs)} existing libraries on {client.base_url}")

    added = 0
    for proj_name, cfg in projections.items():
        kinds = cfg.get("kinds") or list(KINDS)
        for kind in kinds:
            for audiotype in cfg["audiotypes"]:
                folder = (
                    f"/audiobooks/{proj_name}/"
                    f"Swanki-{kind}-{audiotype.capitalize()}"
                )
                if folder in by_folder:
                    print(f"  = {by_folder[folder]['name']}  (at {folder})")
                    continue

                simple = f"{kind} — {audiotype.capitalize()}"
                name = (
                    simple
                    if simple not in existing_names
                    else f"{proj_name}: {simple}"
                )
                client.create_library(name, folder)
                print(f"  + {name}  ->  {folder}")
                existing_names.add(name)
                added += 1
    print(f"Added {added} librar{'y' if added == 1 else 'ies'}")
    return added


def build_library_index(client: ABSClient) -> dict[tuple[str, str, str], str]:
    """Map ``(projection, kind, audiotype_lower) -> library_id``.

    Derived from each library's folder path
    ``/audiobooks/<projection>/Swanki-<Kind>-<Audiotype>``. Non-swanki
    folders are skipped.
    """
    index: dict[tuple[str, str, str], str] = {}
    for lib in client.libraries():
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


def library_items_by_title(
    client: ABSClient, library_id: str
) -> dict[str, str]:
    """Map item title (or folder name) -> ABS item id for one library."""
    items: dict[str, str] = {}
    for item in client.library_items(library_id):
        media = item.get("media", {})
        metadata = media.get("metadata", {})
        title = metadata.get("title") or item.get("path", "").split("/")[-1]
        if title:
            items[title] = item["id"]
    return items
