"""
swanki/abs/sync.py
[[swanki.abs.sync]]
https://github.com/Mjvolk3/Swanki/tree/main/swanki/abs/sync.py
Test file: tests/test_abs_sync.py

Zotero -> disk audio sync (step 1 of the full refresh; the slow leg). For each
projection, pull tag-filtered Zotero items, download the newest mp3 zip per
content-prefix, and extract audio into the per-projection audiobook libraries:

    Swanki_ABS/<projection>/Swanki-<Kind>-<Audiotype>/<group>/

Idempotency rules (load-bearing, ported verbatim from
``scripts/swanki_abs_sync.py``):

* an mp3 whose timestamped+hashed filename already exists on disk is skipped;
* a republished mp3 (same ``(key, audio_type)``, new timestamp+hash) replaces
  the stale file -- without the removal ABS treats both as separate chapters;
* a Zotero attachment whose file is missing (stale metadata) is skipped with a
  warning instead of aborting the whole sync (deliberate, 2026.05.27 note).
"""

import io
import os
import re
import zipfile
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field
from pyzotero import zotero

from swanki.abs.projections import (
    citation_key,
    classify,
    group_key,
    load_projections,
    resolve_library,
)
from swanki.sync.zotero_client import make_zotero_client

MP3_PATTERN = re.compile(
    r"^(?P<key>.+)-(?P<type>summary|reading|lecture)"
    r"(?:-(?P<ts>\d{8}T\d{4})-[a-f0-9]+)?\.mp3$"
)

DEFAULT_ABS_ROOT = Path.home() / "Documents/projects/Swanki_ABS"


def abs_root_default() -> Path:
    """The on-disk ABS library root (``SWANKI_ABS_ROOT`` env override)."""
    return Path(os.environ.get("SWANKI_ABS_ROOT", DEFAULT_ABS_ROOT))


def fetch_items(zot: zotero.Zotero, tag: str | None) -> list[dict[str, Any]]:
    """All Zotero items in the library, optionally tag-filtered (paginated)."""
    items: list[dict[str, Any]] = []
    start, limit = 0, 100
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


def replace_stale(target_dir: Path, key: str, audio_type: str, keep: str) -> None:
    """Remove stale same-``(key, audio_type)`` mp3s, keeping ``keep``.

    Republished audio gets a fresh timestamp+hash; without removing the prior
    file ABS treats both as separate chapters of the same book. One
    ``(key, audio_type)`` tuple maps to one mp3.
    """
    for stale in target_dir.glob("*.mp3"):
        if stale.name == keep:
            continue
        sm = MP3_PATTERN.match(stale.name)
        if sm and sm.group("key") == key and sm.group("type") == audio_type:
            stale.unlink()
            print(f"  - {stale.relative_to(target_dir.parents[2])} (replaced)")


class ExtractResult(BaseModel):
    """Outcome of extracting one Zotero zip."""

    written: int = Field(default=0, description="New mp3s written to disk")
    found: set[str] = Field(
        default_factory=set,
        description="Audio types the zip carried, before the audiotype filter",
    )


def extract_audio(
    zip_bytes: bytes,
    audiotypes: set[str],
    dest_root: Path,
    kind: str,
    group: str,
) -> ExtractResult:
    """Extract matching mp3s from one Zotero zip into the library tree.

    Returns:
        ``written`` counts new mp3s (existing filenames are skipped);
        ``found`` reports every audio type present in the zip regardless of
        the projection's filter, so callers can tell "this bundle has no
        audio at all" (a cards-only re-run) from "this bundle's audio is
        filtered out by this projection".
    """
    result = ExtractResult()
    with zipfile.ZipFile(io.BytesIO(zip_bytes)) as zf:
        for name in zf.namelist():
            if not name.lower().endswith(".mp3"):
                continue
            m = MP3_PATTERN.match(Path(name).name)
            if not m:
                continue
            audio_type = m.group("type")
            result.found.add(audio_type)
            if audio_type not in audiotypes:
                continue
            lib = f"Swanki-{kind}-{audio_type.capitalize()}"
            target_dir = dest_root / lib / group
            target_dir.mkdir(parents=True, exist_ok=True)
            target = target_dir / Path(name).name
            if target.exists():
                continue
            replace_stale(target_dir, m.group("key"), audio_type, target.name)
            target.write_bytes(zf.read(name))
            print(f"  + {target.relative_to(dest_root.parent)}")
            result.written += 1
    return result


def sync_projection(
    name: str, cfg: dict[str, Any], abs_root: Path, api_key: str
) -> None:
    """Sync audio mp3s for one projection, unless ``push_audio`` is false."""
    from swanki.delivery.artifacts import zips_by_prefix

    if not cfg.get("push_audio", True):
        print(f"\n=== Projection: {name} -- push_audio=false, skipping audio ===")
        return
    lib_id, lib_type = resolve_library(cfg["zotero"])
    tag = cfg["zotero"].get("tag")
    audiotypes = set(cfg["audiotypes"])
    dest_root = abs_root / name
    dest_root.mkdir(parents=True, exist_ok=True)

    print(f"\n=== Projection: {name} (Zotero {lib_type}/{lib_id}, tag={tag!r}) ===")
    zot = make_zotero_client(lib_id, lib_type, api_key)
    items = fetch_items(zot, tag)
    print(f"  {len(items)} item(s) matched")

    total = 0
    for item in items:
        kind = classify(item)
        ckey = citation_key(item)
        if not ckey:
            continue
        group = group_key(ckey, kind)
        for prefix, attachments in zips_by_prefix(zot, item["key"]).items():
            # Newest first, falling through cards-only zips (an .apkg-only
            # re-run) to the newest bundle that actually carries audio.
            for att in attachments:
                try:
                    content = zot.file(att["key"])
                except Exception as e:
                    # Stale attachment metadata pointing to a missing file;
                    # skip it instead of aborting the whole sync.
                    print(
                        f"  warn: skipping "
                        f"{att.get('data', {}).get('filename', '?')} "
                        f"(key={att.get('key', '?')}): {e}"
                    )
                    continue
                result = extract_audio(content, audiotypes, dest_root, kind, group)
                total += result.written
                if result.found:
                    break
            else:
                print(f"  warn: no audio-bearing zip for {prefix}")
    print(f"  extracted {total} new mp3(s)")


def sync_all(
    projections_path: Path | None = None, abs_root: Path | None = None
) -> None:
    """Sync every projection (the legacy ``swanki_abs_sync.py`` main)."""
    api_key = os.environ["ZOTERO_API_KEY"]
    projections = load_projections(projections_path)
    root = abs_root if abs_root is not None else abs_root_default()
    root.mkdir(parents=True, exist_ok=True)

    for name, cfg in projections.items():
        sync_projection(name, cfg, root, api_key)
