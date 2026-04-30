"""
scripts/swanki_abs_sync.py
[[scripts.swanki_abs_sync]]
https://github.com/Mjvolk3/Swanki/tree/main/scripts/swanki_abs_sync.py

Sync Zotero libraries into an audiobookshelf-ready folder tree.

Reads ``infra/abs/projections.yml`` and for each projection pulls Zotero
items (optionally tag-filtered), downloads the latest mp3 zip per item,
and extracts audio into six per-projection audiobook libraries:

    Swanki_ABS/<projection>/
        Swanki-Paper-Summary/<citekey>/
        Swanki-Paper-Reading/<citekey>/
        Swanki-Paper-Lecture/<citekey>/
        Swanki-Book-Summary/<base_citekey>/
        Swanki-Book-Reading/<base_citekey>/
        Swanki-Book-Lecture/<base_citekey>/

Book chapters are grouped by stripping the ``_CH##_...`` suffix so a single
ABS book contains all chapters as ordered tracks. Re-runs skip mp3s whose
(timestamped + hashed) filename already exists on disk.
"""

import io
import os
import re
import sys
import zipfile
from pathlib import Path

import yaml
from dotenv import load_dotenv
from pyzotero import zotero

load_dotenv()

BOOK_TYPES = {"book", "bookSection"}
ZIP_PATTERN = re.compile(
    r"^(?P<key>.+)-(?P<ts>\d{8}T\d{4})-(?P<hash>[a-f0-9]+)\.zip$"
)
MP3_PATTERN = re.compile(
    r"^(?P<key>.+)-(?P<type>summary|reading|lecture)"
    r"(?:-\d{8}T\d{4}-[a-f0-9]+)?\.mp3$"
)
CHAPTER_SUFFIX = re.compile(r"_CH\d+_.*$")

DEFAULT_PROJECTIONS = (
    Path.home() / "Documents/projects/infra/abs/projections.yml"
)
DEFAULT_ABS_ROOT = Path.home() / "Documents/projects/Swanki_ABS"


def load_projections(path: Path) -> dict:
    with path.open() as f:
        return yaml.safe_load(f)["projections"]


def resolve_library(cfg: dict) -> tuple[str, str]:
    if "library_id" in cfg:
        lib_id = str(cfg["library_id"])
    else:
        lib_id = os.environ[cfg["library_id_env"]]
    return lib_id, cfg.get("library_type", "user")


def citation_key(item: dict) -> str:
    key = item["data"].get("citationKey", "") or ""
    if key:
        return key
    extra = item["data"].get("extra", "")
    m = re.search(r"Citation Key:\s*(\S+)", extra)
    return m.group(1) if m else item["key"]


def classify(item: dict) -> str:
    return "Book" if item["data"].get("itemType") in BOOK_TYPES else "Paper"


def group_key(citekey: str, kind: str) -> str:
    if kind == "Book":
        return CHAPTER_SUFFIX.sub("", citekey)
    return citekey


def fetch_items(zot: zotero.Zotero, tag: str | None) -> list[dict]:
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


def latest_zips(zot: zotero.Zotero, item_key: str) -> list[dict]:
    """Return one zip per distinct content prefix on the item — the newest of each.

    A book item may carry multiple zips (one per chapter, with prefix like
    ``{citation_key}_01-...`` and ``{citation_key}_02-...``). Earlier code
    picked only the single newest zip across the item, which discarded all
    but one chapter. Group by prefix, then keep the newest in each group.
    """
    by_prefix: dict[str, tuple[str, dict]] = {}
    for child in zot.children(item_key):
        name = child.get("data", {}).get("filename", "")
        if not name.endswith(".zip"):
            continue
        m = ZIP_PATTERN.match(name)
        if not m:
            continue
        prefix = m.group("key")
        ts = m.group("ts")
        prev = by_prefix.get(prefix)
        if prev is None or ts > prev[0]:
            by_prefix[prefix] = (ts, child)
    return [c for _, c in by_prefix.values()]


def latest_zip(zot: zotero.Zotero, item_key: str) -> dict | None:
    """Back-compat: newest zip (single) — defers to ``latest_zips`` and
    returns the most recent if any exist."""
    zips = latest_zips(zot, item_key)
    if not zips:
        return None
    return max(
        zips,
        key=lambda c: ZIP_PATTERN.match(c["data"]["filename"]).group("ts"),  # type: ignore[union-attr]
    )


def extract_audio(
    zip_bytes: bytes,
    audiotypes: set[str],
    dest_root: Path,
    kind: str,
    group: str,
) -> int:
    count = 0
    with zipfile.ZipFile(io.BytesIO(zip_bytes)) as zf:
        for name in zf.namelist():
            if not name.lower().endswith(".mp3"):
                continue
            m = MP3_PATTERN.match(Path(name).name)
            if not m:
                continue
            audio_type = m.group("type")
            if audio_type not in audiotypes:
                continue
            lib = f"Swanki-{kind}-{audio_type.capitalize()}"
            target_dir = dest_root / lib / group
            target_dir.mkdir(parents=True, exist_ok=True)
            target = target_dir / Path(name).name
            if target.exists():
                continue
            # Republished audio gets a fresh timestamp+hash. Without removing
            # the prior file ABS treats both as separate chapters of the same
            # book. One (key, audio_type) tuple should map to one mp3.
            for stale in target_dir.glob("*.mp3"):
                if stale.name == target.name:
                    continue
                sm = MP3_PATTERN.match(stale.name)
                if (
                    sm
                    and sm.group("key") == m.group("key")
                    and sm.group("type") == audio_type
                ):
                    stale.unlink()
                    print(f"  - {stale.relative_to(dest_root.parent)} (replaced)")
            target.write_bytes(zf.read(name))
            print(f"  + {target.relative_to(dest_root.parent)}")
            count += 1
    return count


def sync_projection(
    name: str, cfg: dict, abs_root: Path, api_key: str
) -> None:
    lib_id, lib_type = resolve_library(cfg["zotero"])
    tag = cfg["zotero"].get("tag")
    audiotypes = set(cfg["audiotypes"])
    dest_root = abs_root / name
    dest_root.mkdir(parents=True, exist_ok=True)

    print(
        f"\n=== Projection: {name} "
        f"(Zotero {lib_type}/{lib_id}, tag={tag!r}) ==="
    )
    zot = zotero.Zotero(lib_id, lib_type, api_key)
    items = fetch_items(zot, tag)
    print(f"  {len(items)} item(s) matched")

    total = 0
    for item in items:
        kind = classify(item)
        ckey = citation_key(item)
        if not ckey:
            continue
        group = group_key(ckey, kind)
        for att in latest_zips(zot, item["key"]):
            try:
                content = zot.file(att["key"])
            except Exception as e:
                # Stale attachment metadata pointing to a missing file; skip
                # it instead of aborting the whole sync.
                print(
                    f"  warn: skipping {att.get('data',{}).get('filename','?')} "
                    f"(key={att.get('key','?')}): {e}"
                )
                continue
            total += extract_audio(content, audiotypes, dest_root, kind, group)
    print(f"  extracted {total} new mp3(s)")


def main() -> None:
    projections_path = Path(
        sys.argv[1] if len(sys.argv) > 1 else DEFAULT_PROJECTIONS
    )
    api_key = os.environ["ZOTERO_API_KEY"]
    projections = load_projections(projections_path)
    abs_root = Path(os.environ.get("SWANKI_ABS_ROOT", DEFAULT_ABS_ROOT))
    abs_root.mkdir(parents=True, exist_ok=True)

    for name, cfg in projections.items():
        sync_projection(name, cfg, abs_root, api_key)


if __name__ == "__main__":
    main()
