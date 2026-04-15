"""
scripts/zip_swanki_mp3s.py
[[scripts.zip_swanki_mp3s]]
https://github.com/Mjvolk3/Swanki/tree/main/scripts/zip_swanki_mp3s.py

Query Zotero for items tagged 🦊, download their most recent zip
attachments, extract MP3s, classify Book vs Paper, and repack into
~/Downloads/swanki.zip organized by class and audio type for BookPlayer.
"""

import io
import os
import re
import zipfile
from collections import defaultdict
from pathlib import Path

from dotenv import load_dotenv
from pyzotero import zotero

load_dotenv()

ZOTERO_API_KEY = os.environ["ZOTERO_API_KEY"]
ZOTERO_LIBRARY_ID = os.environ["ZOTERO_LIBRARY_ID"]
ZOTERO_LIBRARY_TYPE = os.environ.get("ZOTERO_LIBRARY_TYPE", "user")
FOX_TAG = "🦊"
BASE_DIR = "MV-Swanki"

# Zotero itemTypes that count as "Book"
BOOK_TYPES = {"book", "bookSection"}

# Pattern for zip filenames: {citationKey}-{timestamp}-{hash}.zip
# e.g. bishopDeepLearningFoundations2024_CH02_probabilities-20260407T2115-67b26c4.zip
ZIP_PATTERN = re.compile(
    r"^(?P<key>.+)-(?P<ts>\d{8}T\d{4})-(?P<hash>[a-f0-9]+)\.zip$"
)

# Pattern for MP3s inside the zips
MP3_PATTERN = re.compile(
    r"^(?P<key>.+)-(?P<type>summary|reading|lecture)"
    r"(?:-\d{8}T\d{4}-[a-f0-9]+)?\.mp3$"
)


def connect() -> zotero.Zotero:
    return zotero.Zotero(ZOTERO_LIBRARY_ID, ZOTERO_LIBRARY_TYPE, ZOTERO_API_KEY)


def get_fox_tagged_items(zot: zotero.Zotero) -> list[dict]:
    """Fetch all top-level items tagged with 🦊."""
    items = []
    start = 0
    limit = 100
    while True:
        batch = zot.items(tag=FOX_TAG, start=start, limit=limit)
        if not batch:
            break
        items.extend(batch)
        start += limit
        if len(batch) < limit:
            break
    return items


def classify_item(item: dict) -> str:
    """Return 'Book' or 'Paper' based on Zotero itemType."""
    item_type = item["data"].get("itemType", "")
    return "Book" if item_type in BOOK_TYPES else "Paper"


def get_zip_attachments(zot: zotero.Zotero, item_key: str) -> list[dict]:
    """Get .zip child attachments for an item."""
    children = zot.children(item_key)
    return [
        c for c in children
        if c.get("data", {}).get("filename", "").endswith(".zip")
    ]


def deduplicate_zips(zips: list[dict]) -> list[dict]:
    """Keep only the most recent zip per citation key prefix.

    Groups by the citation key portion of the filename, keeps
    the one with the latest timestamp.
    """
    groups: dict[str, list[tuple[str, dict]]] = defaultdict(list)

    for att in zips:
        filename = att["data"]["filename"]
        m = ZIP_PATTERN.match(filename)
        if not m:
            continue
        groups[m.group("key")].append((m.group("ts"), att))

    keepers = []
    for _key, entries in groups.items():
        entries.sort(key=lambda e: e[0], reverse=True)
        keepers.append(entries[0][1])
    return keepers


def main():
    zot = connect()
    print("Fetching items tagged with 🦊...")
    items = get_fox_tagged_items(zot)
    print(f"Found {len(items)} tagged items")

    # Collect zip attachments per item: (class, citation_key, attachment)
    to_download: list[tuple[str, str, dict]] = []

    for item in items:
        item_class = classify_item(item)
        item_key = item["key"]
        title = item["data"].get("title", item_key)
        citation_key = item["data"].get("citationKey", "") or ""
        if not citation_key:
            extra = item["data"].get("extra", "")
            m = re.search(r"Citation Key:\s*(\S+)", extra)
            if m:
                citation_key = m.group(1)
        zips = get_zip_attachments(zot, item_key)
        if not zips:
            continue
        deduped = deduplicate_zips(zips)
        for att in deduped:
            filename = att["data"]["filename"]
            to_download.append((item_class, citation_key, att))
            print(f"  [{item_class}] {title} -> {filename}")

    if not to_download:
        print("No zip attachments found.")
        return

    # Build output zip by extracting MP3s from each downloaded zip
    zip_path = Path.home() / "Downloads" / "swanki.zip"
    print(f"\nBuilding zip at {zip_path} ...")

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_STORED) as out_zf:
        for item_class, citation_key, att in to_download:
            filename = att["data"]["filename"]
            att_key = att["key"]
            try:
                content = zot.file(att_key)
            except Exception as e:
                print(f"  SKIP (download failed): {filename} — {e}")
                continue

            # Extract MP3s from the downloaded zip
            with zipfile.ZipFile(io.BytesIO(content)) as inner_zf:
                for name in inner_zf.namelist():
                    if not name.lower().endswith(".mp3"):
                        continue
                    m = MP3_PATTERN.match(name)
                    audio_type = m.group("type") if m else "other"
                    if item_class == "Book":
                        arc_path = f"{BASE_DIR}/{item_class}/{citation_key}/{audio_type}/{name}"
                    else:
                        arc_path = f"{BASE_DIR}/{item_class}/{audio_type}/{name}"
                    out_zf.writestr(arc_path, inner_zf.read(name))
                    print(f"  Added: {arc_path}")

    print(f"\nDone! Zip written to: {zip_path}")
    print(f"Size: {zip_path.stat().st_size / (1024*1024):.1f} MB")


if __name__ == "__main__":
    main()
