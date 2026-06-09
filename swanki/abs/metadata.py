"""
swanki/abs/metadata.py
[[swanki.abs.metadata]]
https://github.com/Mjvolk3/Swanki/tree/main/swanki/abs/metadata.py
Test file: tests/test_abs_projections.py

Enrich ABS items with author metadata + cover images derived from Zotero
(refresh step 4). ABS items match Zotero items by title/folder-name ==
citation key (group key for books); unmatched items are silently skipped --
intentional, so manually-added ABS items coexist (documented contract).

Idempotency (load-bearing): cover generation is skipped when ``cover.jpg``
already exists (PDF download + pdftoppm render is the expensive leg); author
PATCHes run every pass (cheap, rewrites the same value).

Path translation: ABS reports item paths in its container view
(``/audiobooks/...``); the host view is ``$SWANKI_ABS_ROOT``.
"""

import subprocess
import tempfile
from pathlib import Path
from typing import Any, cast

from swanki.abs.client import ABSClient
from swanki.abs.libraries import build_library_index
from swanki.abs.projections import (
    citation_key,
    classify,
    group_key,
    resolve_library,
)
from swanki.abs.sync import fetch_items
from swanki.sync.zotero_client import make_zotero_client

CONTAINER_PREFIX = "/audiobooks"


def _creator_name(c: dict[str, Any]) -> str | None:
    parts = []
    if c.get("firstName"):
        parts.append(c["firstName"])
    if c.get("lastName"):
        parts.append(c["lastName"])
    if not parts and c.get("name"):
        parts.append(c["name"])
    return " ".join(parts) or None


def derive_authors(zot_item: dict[str, Any]) -> list[str]:
    """All authors in Zotero order; first author = primary display."""
    creators = [
        c
        for c in zot_item["data"].get("creators", [])
        if c.get("creatorType") == "author"
    ]
    return [n for n in (_creator_name(c) for c in creators) if n]


def get_pdf_attachment(zot: Any, item_key: str) -> dict[str, Any] | None:
    """First PDF attachment child of a Zotero item, or None."""
    for child in zot.children(item_key):
        d = child.get("data", {})
        if d.get("contentType") == "application/pdf" or d.get(
            "filename", ""
        ).lower().endswith(".pdf"):
            return cast(dict[str, Any], child)
    return None


def render_cover(pdf_bytes: bytes, dest: Path) -> None:
    """Render page 1 of a PDF to ``dest`` (jpg) via pdftoppm."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(suffix=".pdf") as tmp:
        tmp.write(pdf_bytes)
        tmp.flush()
        prefix = dest.with_suffix("")
        subprocess.run(
            [
                "pdftoppm", "-jpeg", "-f", "1", "-l", "1",
                "-r", "100", "-singlefile",
                tmp.name, str(prefix),
            ],
            check=True,
            capture_output=True,
        )
    # pdftoppm -singlefile writes <prefix>.jpg
    produced = prefix.with_suffix(".jpg")
    if produced != dest and produced.exists():
        produced.rename(dest)


def container_to_host(container_path: str, abs_root: Path) -> Path:
    """Rewrite an ABS container path (``/audiobooks/...``) to the host view."""
    if not container_path.startswith(CONTAINER_PREFIX):
        raise ValueError(f"unexpected container path: {container_path}")
    return abs_root / container_path[len(CONTAINER_PREFIX):].lstrip("/")


def enrich_metadata(
    client: ABSClient,
    projections: dict[str, dict[str, Any]],
    abs_root: Path,
    zotero_api_key: str,
) -> None:
    """Set authors + covers on every matched ABS item, per projection."""
    lib_index = build_library_index(client)

    for proj_name, cfg in projections.items():
        lib_id, lib_type = resolve_library(cfg["zotero"])
        tag = cfg["zotero"].get("tag")

        print(f"\n=== Projection: {proj_name} ===")
        zot = make_zotero_client(lib_id, lib_type, zotero_api_key)
        zot_items = fetch_items(zot, tag)

        by_group: dict[str, tuple[dict[str, Any], str]] = {}
        for item in zot_items:
            kind = classify(item)
            ckey = citation_key(item)
            if not ckey:
                continue
            by_group.setdefault(group_key(ckey, kind), (item, kind))

        proj_lib_ids = [
            lib_id_
            for (proj, _kind, _at), lib_id_ in lib_index.items()
            if proj == proj_name
        ]
        author_updates = 0
        cover_updates = 0
        for library_id in proj_lib_ids:
            for item in client.library_items(library_id):
                title = (
                    item.get("media", {}).get("metadata", {}).get("title")
                    or item.get("relPath")
                )
                if not title or title not in by_group:
                    continue
                zot_item, _kind = by_group[title]

                authors = derive_authors(zot_item)
                if authors:
                    client.update_authors(item["id"], authors)
                    author_updates += 1

                container_folder = item.get("path")
                if not container_folder:
                    continue
                host_folder = container_to_host(container_folder, abs_root)
                cover = host_folder / "cover.jpg"
                if cover.exists():
                    continue
                pdf_att = get_pdf_attachment(zot, zot_item["key"])
                if not pdf_att:
                    continue
                pdf_bytes = zot.file(pdf_att["key"])
                render_cover(pdf_bytes, cover)
                cover_updates += 1
                print(f"  cover: {title}")

        print(
            f"  {author_updates} author updates, "
            f"{cover_updates} covers generated"
        )
