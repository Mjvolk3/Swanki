"""
scripts/abs_enrich_metadata.py
[[scripts.abs_enrich_metadata]]
https://github.com/Mjvolk3/Swanki/tree/main/scripts/abs_enrich_metadata.py

Enrich ABS items with author metadata + cover images derived from Zotero.

For each ABS item (identified by its folder-name == citekey / base-citekey):

  * Author — last author for papers, first author for books. Set via
    ``PATCH /api/items/:id/media`` with ``{metadata: {authorName: ...}}``.
  * Cover — ``cover.jpg`` rendered from page 1 of the Zotero PDF attachment
    using ``pdftoppm`` (poppler-utils). Written into the item folder so ABS
    picks it up on next scan.

Idempotent: skips cover generation when ``cover.jpg`` is already present.
Author updates are PATCHed every run (cheap and rewrites the same value).

Path translation: ABS reports item paths as ``/audiobooks/...`` (container
view). The script rewrites that prefix to ``$SWANKI_ABS_ROOT`` (host view)
before writing files.
"""

import json
import os
import re
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path

import yaml
from dotenv import load_dotenv
from pyzotero import zotero

load_dotenv()

DEFAULT_ABS_URL = "https://abs.michaelvolk.dev"
DEFAULT_PROJECTIONS = (
    Path.home() / "Documents/projects/infra/abs/projections.yml"
)
DEFAULT_ABS_ROOT = Path.home() / "Documents/projects/Swanki_ABS"
CONTAINER_PREFIX = "/audiobooks"
BOOK_TYPES = {"book", "bookSection"}
CHAPTER_SUFFIX = re.compile(r"_CH\d+_.*$")


def load_token() -> str:
    token_file = os.environ.get("ABS_API_TOKEN_FILE")
    if token_file:
        return Path(token_file).expanduser().read_text().strip()
    return os.environ["ABS_API_TOKEN"].strip()


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


def _creator_name(c):
    parts = []
    if c.get("firstName"):
        parts.append(c["firstName"])
    if c.get("lastName"):
        parts.append(c["lastName"])
    if not parts and c.get("name"):
        parts.append(c["name"])
    return " ".join(parts) or None


def derive_authors(zot_item, kind):
    """All authors in Zotero order; first author = primary display."""
    del kind
    creators = [
        c for c in zot_item["data"].get("creators", [])
        if c.get("creatorType") == "author"
    ]
    names = [n for n in (_creator_name(c) for c in creators) if n]
    return names


def get_pdf_attachment(zot, item_key):
    for child in zot.children(item_key):
        d = child.get("data", {})
        if (d.get("contentType") == "application/pdf"
                or d.get("filename", "").lower().endswith(".pdf")):
            return child
    return None


def render_cover(pdf_bytes: bytes, dest: Path) -> None:
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


def libs_for_projection(base, token, proj_name):
    data = api(base, token, "GET", "/api/libraries")
    libs = data.get("libraries", data) if isinstance(data, dict) else data
    result = []
    for lib in libs:
        for folder in lib.get("folders", []):
            path = folder.get("fullPath", "")
            parts = path.strip("/").split("/")
            if len(parts) < 3 or not parts[-1].startswith("Swanki-"):
                continue
            segments = parts[-1].split("-", 2)
            if len(segments) != 3 or parts[-2] != proj_name:
                continue
            _, kind, _ = segments
            result.append({"id": lib["id"], "kind": kind})
    return result


def library_items(base, token, library_id):
    data = api(
        base, token, "GET",
        f"/api/libraries/{library_id}/items?limit=10000",
    )
    return data.get("results", data) if isinstance(data, dict) else data


def update_authors(base, token, item_id, author_names):
    api(
        base, token, "PATCH", f"/api/items/{item_id}/media",
        {"metadata": {"authors": [{"name": n} for n in author_names]}},
    )


def container_to_host(container_path: str, abs_root: Path) -> Path:
    if not container_path.startswith(CONTAINER_PREFIX):
        raise ValueError(f"unexpected container path: {container_path}")
    return abs_root / container_path[len(CONTAINER_PREFIX):].lstrip("/")


def main():
    base = os.environ.get("ABS_URL", DEFAULT_ABS_URL)
    abs_root = Path(os.environ.get("SWANKI_ABS_ROOT", DEFAULT_ABS_ROOT))
    projections_path = Path(
        sys.argv[1] if len(sys.argv) > 1 else DEFAULT_PROJECTIONS
    )
    with projections_path.open() as f:
        projections = yaml.safe_load(f)["projections"]

    token = load_token()
    zotero_api_key = os.environ["ZOTERO_API_KEY"]

    for proj_name, cfg in projections.items():
        lib_id, lib_type = resolve_library(cfg["zotero"])
        tag = cfg["zotero"].get("tag")

        print(f"\n=== Projection: {proj_name} ===")
        zot = zotero.Zotero(lib_id, lib_type, zotero_api_key)
        zot_items = fetch_items(zot, tag)

        by_group: dict[str, tuple[dict, str]] = {}
        for item in zot_items:
            kind = classify(item)
            ckey = citation_key(item)
            if not ckey:
                continue
            by_group.setdefault(group_key(ckey, kind), (item, kind))

        libs = libs_for_projection(base, token, proj_name)
        author_updates = 0
        cover_updates = 0
        for lib in libs:
            for item in library_items(base, token, lib["id"]):
                title = (
                    item.get("media", {}).get("metadata", {}).get("title")
                    or item.get("relPath")
                )
                if not title or title not in by_group:
                    continue
                zot_item, kind = by_group[title]

                authors = derive_authors(zot_item, kind)
                if authors:
                    update_authors(base, token, item["id"], authors)
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


if __name__ == "__main__":
    main()
