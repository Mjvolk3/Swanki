"""
swanki/sync/zotero.py
[[swanki.sync.zotero]]
https://github.com/Mjvolk3/Swanki/tree/main/swanki/sync/zotero.py

Upload Swanki outputs (apkg, audio) to Zotero as timestamped attachments.
"""

import logging
import os
import shutil
import subprocess
import tempfile
from datetime import datetime
from pathlib import Path

from pyzotero import zotero

logger = logging.getLogger(__name__)

# Swanki output types to upload: (glob pattern, name template)
_OUTPUT_TYPES = [
    ("{citation_key}.apkg", "{citation_key}-{timestamp}-{commit}.apkg"),
    ("{prefix}-lecture-audio.mp3", "{citation_key}-lecture-{timestamp}-{commit}.mp3"),
    ("{prefix}-summary-audio.mp3", "{citation_key}-summary-{timestamp}-{commit}.mp3"),
    ("{prefix}-reading-audio.mp3", "{citation_key}-reading-{timestamp}-{commit}.mp3"),
]


def _git_short_hash() -> str:
    """Get the abbreviated git commit hash of the Swanki repo."""
    result = subprocess.run(
        ["git", "rev-parse", "--short", "HEAD"],
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent.parent,
    )
    return result.stdout.strip() or "unknown"


def _find_zotero_item(zot: zotero.Zotero, citation_key: str) -> str | None:
    """Find a Zotero item key by citation key stored in the extra field.

    Args:
        zot: Authenticated Zotero client.
        citation_key: Citation key to search for.

    Returns:
        Zotero item key, or None if not found.
    """
    import re

    # Split camelCase citation key into search words (e.g. "luoWhenCausal2020" -> "luo When Causal")
    words = re.sub(r"([a-z])([A-Z])", r"\1 \2", citation_key)
    search_term = re.sub(r"\d+$", "", words).strip()

    results = zot.items(q=search_term, limit=20)

    for item in results:
        data = item["data"]
        if data["itemType"] == "attachment":
            continue
        extra = data.get("extra", "")
        if citation_key in extra:
            return data["key"]

    return None


def _find_or_create_sync_note(
    zot: zotero.Zotero, parent_key: str
) -> tuple[dict, str]:
    """Find or create a 'Swanki Sync Log' child note.

    Args:
        zot: Authenticated Zotero client.
        parent_key: Parent item key.

    Returns:
        Tuple of (full_item_dict, existing_html_content).
    """
    children = zot.children(parent_key)
    for child in children:
        data = child["data"]
        if data["itemType"] == "note" and "Swanki Sync Log" in data.get("note", ""):
            return child, data["note"]

    # Create new note
    template = zot.item_template("note")
    template["note"] = "<h2>Swanki Sync Log</h2>\n"
    resp = zot.create_items([template], parentid=parent_key)
    new_key = resp["successful"]["0"]["key"]
    # Fetch the full item to get version
    new_item = zot.item(new_key)
    return new_item, "<h2>Swanki Sync Log</h2>\n"


def sync_to_zotero(
    citation_key: str,
    output_dir: Path,
    audio_prefix: str,
) -> None:
    """Upload Swanki outputs to Zotero as timestamped attachments.

    Uploads apkg and any generated audio files as child attachments of the
    corresponding Zotero library item. Each file gets a timestamp in its
    name so multiple versions accumulate.

    Args:
        citation_key: Paper citation key (must exist in Zotero extra field).
        output_dir: Swanki output directory containing generated files.
        audio_prefix: Audio file prefix (e.g. "citationKey-fish").
    """
    api_key = os.getenv("ZOTERO_API_KEY")
    library_id = os.getenv("ZOTERO_LIBRARY_ID")
    library_type = os.getenv("ZOTERO_LIBRARY_TYPE", "user")

    assert api_key, "ZOTERO_API_KEY not set"
    assert library_id, "ZOTERO_LIBRARY_ID not set"

    zot = zotero.Zotero(library_id, library_type, api_key)

    # Find the parent item
    item_key = _find_zotero_item(zot, citation_key)
    assert item_key, f"Could not find Zotero item for citation key: {citation_key}"
    logger.info(f"Found Zotero item {item_key} for {citation_key}")

    timestamp = datetime.now().strftime("%Y%m%dT%H%M")
    commit = _git_short_hash()
    uploaded: list[str] = []

    with tempfile.TemporaryDirectory() as tmpdir:
        for source_pattern, name_template in _OUTPUT_TYPES:
            source_name = source_pattern.format(
                citation_key=citation_key, prefix=audio_prefix
            )
            source_path = output_dir / source_name

            if not source_path.exists():
                logger.debug(f"Skipping {source_name} (not found)")
                continue

            dest_name = name_template.format(
                citation_key=citation_key, timestamp=timestamp, commit=commit
            )
            dest_path = Path(tmpdir) / dest_name
            shutil.copy2(source_path, dest_path)

            logger.info(f"Uploading {dest_name} to Zotero...")
            zot.attachment_simple([str(dest_path)], parentid=item_key)
            uploaded.append(dest_name)

    if not uploaded:
        logger.warning("No files found to upload to Zotero")
        return

    # Update sync log note
    note_item, note_html = _find_or_create_sync_note(zot, item_key)
    file_list = ", ".join(
        f.rsplit("-", 1)[0].split("-", 1)[-1] if "-" in f else "apkg"
        for f in uploaded
    )
    log_entry = f"<p>{timestamp} — Uploaded {file_list}</p>\n"
    note_item["data"]["note"] = note_html + log_entry
    zot.update_item(note_item)

    logger.info(f"Synced {len(uploaded)} files to Zotero item {item_key}")
    for f in uploaded:
        print(f"  Uploaded: {f}")
