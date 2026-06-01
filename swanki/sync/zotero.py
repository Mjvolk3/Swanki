"""
swanki/sync/zotero.py
[[swanki.sync.zotero]]
https://github.com/Mjvolk3/Swanki/tree/main/swanki/sync/zotero.py

Upload Swanki outputs (apkg, audio) to Zotero as timestamped attachments.
"""

import logging
import os
import re
import shutil
import subprocess
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Any

import httpx
from pyzotero import zotero

logger = logging.getLogger(__name__)

# Swanki output types to upload: (glob pattern, name template).
# The apkg pattern uses a wildcard so it matches both the legacy
# `<key>.apkg` and the suffixed `<key>-problem-set.apkg` produced by
# solution-manual mode (see Pipeline._apkg_filename).
_OUTPUT_TYPES = [
    ("{citation_key}*.apkg", "{stem}-{timestamp}-{commit}.apkg"),
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


def _match_citation_key(item: dict, citation_key: str) -> bool:
    """Check if a Zotero item matches a citation key."""
    data = item["data"]
    extra = data.get("extra", "")
    if f"Citation Key: {citation_key}" in extra:
        return True
    if data.get("citationKey") == citation_key:
        return True
    return False


def _find_zotero_item(zot: zotero.Zotero, citation_key: str) -> str | None:
    """Find a Zotero item key matching a citation key.

    Splits the camelCase key into words and searches with progressively
    fewer terms (Zotero API ANDs all terms). Filters client-side on
    BetterBibTeX `Citation Key:` in `extra` or Zotero 7 `citationKey`.
    """
    import re

    s = re.sub(r"([a-z])([A-Z])", r"\1 \2", citation_key)
    s = re.sub(r"([a-zA-Z])(\d)", r"\1 \2", s)
    s = re.sub(r"(\d)([a-zA-Z])", r"\1 \2", s)
    words = s.split()
    # Drop 1-char title words ("V", etc.); Zotero AND-search can't locate them
    # when the title renders the same idea with a non-ASCII token (e.g. "β").
    title_words = [w for w in words if len(w) > 1 and w[0].isupper()]

    queries = []
    # Literal citation key with qmode=everything searches the `extra` field
    # where BetterBibTeX stores `Citation Key: <key>` — guaranteed hit when
    # the item actually exists. Put first.
    queries.append((citation_key, "everything"))
    if title_words:
        queries.append((" ".join(title_words), None))
        queries.append((" ".join(title_words), "everything"))
    queries.append((" ".join(words), None))
    queries.append((" ".join(words), "everything"))
    if len(title_words) > 2:
        queries.append((" ".join(title_words[:2]), None))
    # Fallback: first word alone (usually the author prefix) — catches cases
    # where the title token doesn't match the citation-key's CamelCase split.
    if words:
        queries.append((words[0], "everything"))

    for q, qmode in queries:
        kwargs: dict[str, object] = {"q": q}
        if qmode:
            kwargs["qmode"] = qmode
        for item in zot.items(**kwargs):
            if item["data"]["itemType"] == "attachment":
                continue
            if _match_citation_key(item, citation_key):
                return item["data"]["key"]

    # Last-resort fallback: paginate the full library and match client-side.
    # Zotero's search API does not index the native `citationKey` field, so
    # Zotero 7 items whose key isn't also in title/extra/authors require this
    # linear scan. Slow but bulletproof.
    start = 0
    while True:
        batch = zot.items(start=start, limit=100)
        if not batch:
            break
        for item in batch:
            if item["data"]["itemType"] == "attachment":
                continue
            if _match_citation_key(item, citation_key):
                return item["data"]["key"]
        if len(batch) < 100:
            break
        start += 100
    return None


def _chapter_base(content_key: str) -> str:
    """Truncate ``content_key`` at the chapter marker ``_CH<digits>``.

    Returns the prefix INCLUDING ``_CH##`` so it can be used as the stable
    "slot" for prior-attachment pruning. ``MyBook_CH01_intro`` and the
    legacy ``MyBook_CH01`` and a future ``MyBook_CH01_revised`` all share
    chapter base ``MyBook_CH01``. For content_keys without ``_CH##`` (e.g.
    papers), returns the full content_key unchanged.
    """
    m = re.match(r"^(.+_CH\d+)", content_key)
    return m.group(1) if m is not None else content_key


def _prune_prior_attachments(
    zot: Any,
    item_key: str,
    content_key: str,
    just_uploaded_filename: str,
) -> int:
    """Delete prior swanki ZIP/apkg attachments sharing the chapter base.

    Called AFTER a successful upload so the parent item is left with only
    the most recent artifact per chapter. Keeps Zotero lean since iteration
    on audio happens in ABS, not by stacking historical versions.

    Filters: itemType=attachment, filename starts with the chapter base
    (per ``_chapter_base``) and ends in ``.zip`` or ``.apkg``. The just-
    uploaded filename is defensively excluded.

    Returns:
        Count of attachments deleted.
    """
    base = _chapter_base(content_key)
    pattern = re.compile(rf"^{re.escape(base)}.*\.(?:zip|apkg)$")
    deleted = 0
    children = zot.children(item_key, limit=200)
    for child in children:
        if child["data"].get("itemType") != "attachment":
            continue
        fn = child["data"].get("filename", "")
        if not pattern.match(fn):
            continue
        if fn == just_uploaded_filename:
            continue
        logger.info(f"Pruning prior attachment: {fn} ({child['key']})")
        zot.delete_item(child)
        deleted += 1
    return deleted


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
    # Paginate through ALL children: `children()` alone returns only the first
    # page (~25), so once the item accumulates enough attachments/notes the
    # existing "Swanki Sync Log" note falls off page 1, the find below misses
    # it, and every sync creates a NEW note (observed: 85 duplicate notes).
    children = zot.everything(zot.children(parent_key))
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
    content_key: str = "",
) -> None:
    """Upload Swanki outputs to Zotero as timestamped attachments.

    Uploads apkg and any generated audio files as child attachments of the
    corresponding Zotero library item. Each file gets a timestamp in its
    name so multiple versions accumulate.

    Args:
        citation_key: BibTeX key for Zotero item lookup.
        output_dir: Swanki output directory containing generated files.
        audio_prefix: Audio file prefix (e.g. "citationKey-fish").
        content_key: Content identifier for filenames. Defaults to citation_key.
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

    # content_key is used for filenames (distinguishes chapters);
    # citation_key is used for Zotero item lookup.
    file_key = content_key if content_key else citation_key

    timestamp = datetime.now().strftime("%Y%m%dT%H%M")
    commit = _git_short_hash()
    uploaded: list[str] = []

    import zipfile

    with tempfile.TemporaryDirectory() as tmpdir:
        # Collect files into zip
        zip_name = f"{file_key}-{timestamp}-{commit}.zip"
        zip_path = Path(tmpdir) / zip_name
        packed: list[str] = []

        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
            for source_pattern, name_template in _OUTPUT_TYPES:
                source_glob = source_pattern.format(
                    citation_key=file_key, prefix=audio_prefix
                )
                # Glob to support patterns with `*` (e.g. apkg with optional
                # filename suffix). For literal patterns, glob returns 0 or 1.
                matches = sorted(output_dir.glob(source_glob))
                if not matches:
                    logger.debug(f"Skipping {source_glob} (no matches)")
                    continue

                for source_path in matches:
                    dest_name = name_template.format(
                        citation_key=file_key,
                        stem=source_path.stem,
                        timestamp=timestamp,
                        commit=commit,
                    )
                    zf.write(source_path, dest_name)
                    packed.append(dest_name)

        if not packed:
            logger.warning("No files found to upload to Zotero")
            return

        zip_size_mb = zip_path.stat().st_size / 1024 / 1024
        logger.info(f"Uploading {zip_name} ({zip_size_mb:.1f} MB) to Zotero...")

        # Patch httpx default timeout for large file uploads.
        # pyzotero's _upload.py uses bare httpx.post() with default timeout
        # which is too short for large files over slow connections.
        _original_post = httpx.post

        def _patched_post(*args: object, **kwargs: object) -> object:
            kwargs.setdefault("timeout", httpx.Timeout(600.0, connect=60.0))  # type: ignore[arg-type]
            return _original_post(*args, **kwargs)  # type: ignore[arg-type]

        httpx.post = _patched_post  # type: ignore[assignment]
        try:
            zot.attachment_simple([str(zip_path)], parentid=item_key)
            uploaded = packed
        except Exception as e:
            logger.warning(f"Failed to upload {zip_name}: {e}")
            print(f"  Upload failed: {zip_name} ({e})")
            return
        finally:
            httpx.post = _original_post  # type: ignore[assignment]

    # Prune prior versions on the same chapter so Zotero stores only the
    # most recent artifact. Runs AFTER a successful upload so we never
    # leave the item with zero artifacts if the upload itself failed.
    pruned = _prune_prior_attachments(zot, item_key, file_key, zip_name)
    if pruned:
        logger.info(f"Pruned {pruned} prior Zotero attachment(s)")

    # Update sync log note
    note_item, note_html = _find_or_create_sync_note(zot, item_key)
    file_lines = "".join(f"<li>{f}</li>" for f in uploaded)
    log_entry = (
        f"<h3>{timestamp} ({commit})</h3>\n"
        f"<ul>{file_lines}</ul>\n"
    )
    note_item["data"]["note"] = note_html + log_entry
    zot.update_item(note_item)

    # Tag parent item with 🦊 to signify a successful Swanki upload
    parent_item = zot.item(item_key)
    existing_tags = {t["tag"] for t in parent_item["data"].get("tags", [])}
    if "🦊" not in existing_tags:
        zot.add_tags(parent_item, "🦊")

    logger.info(f"Synced {len(uploaded)} files to Zotero item {item_key}")
    for f in uploaded:
        print(f"  Uploaded: {f}")
