"""
swanki/sync/zotero.py
[[swanki.sync.zotero]]
https://github.com/Mjvolk3/Swanki/tree/main/swanki/sync/zotero.py

Upload Swanki outputs (apkg, audio) to Zotero as timestamped attachments.
"""

import hashlib
import logging
import os
import re
import subprocess
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Any, cast

import httpx
from pyzotero import zotero

from .zotero_client import make_zotero_client, with_zotero_retry

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


def upload_attachment(
    zot: zotero.Zotero, item_key: str, zip_path: Path, zip_name: str
) -> str:
    """Upload one imported_file attachment via Zotero's low-level file API.

    Bypasses pyzotero's ``attachment_simple`` (1.11.0 returns a failure dict
    without raising, even on a 5-byte file) and runs the documented four-step
    full-upload flow: create the attachment item, request upload
    authorization, POST the bytes to S3, then register the upload. Every step
    raises ``RuntimeError`` on an unexpected status (never ``assert`` — those
    are stripped under ``python -O`` and would silently revive the
    prune-deletes-good-zips data-loss bug).

    The base URL is built from the pyzotero client's already-pluralized
    attributes (``zot.library_type`` is ``"users"``/``"groups"``), so group
    libraries work without re-reading env or hardcoding ``/users/``.

    Args:
        zot: Authenticated pyzotero client (source of endpoint/library/key).
        item_key: Parent Zotero item key the attachment is filed under.
        zip_path: Local path to the zip file to upload.
        zip_name: Attachment title and filename to register in Zotero.

    Returns:
        The new attachment item's key.

    Raises:
        RuntimeError: If any of the four steps returns an unexpected status
            (create not 200 / no success, auth not 200, S3 not 200|201,
            register not 204), including a 412 write-token replay on create.
    """
    data = zip_path.read_bytes()
    md5 = hashlib.md5(data).hexdigest()
    filesize = len(data)
    # Nonzero milliseconds: a zero mtime yields 400 "File modification time
    # not provided" from the upload-authorization endpoint.
    mtime = int(os.stat(zip_path).st_mtime * 1000)

    base = f"{zot.endpoint}/{zot.library_type}/{zot.library_id}"
    headers: dict[str, str] = {
        "Zotero-API-Key": cast(str, zot.api_key),
        "Zotero-API-Version": "3",
    }

    # 1. CREATE the attachment item under the parent from the API template.
    template: dict[str, Any] = httpx.get(
        f"{zot.endpoint}/items/new?itemType=attachment&linkMode=imported_file",
        headers=headers,
        timeout=60,
    ).json()
    template.update(
        parentItem=item_key,
        title=zip_name,
        filename=zip_name,
        contentType="application/octet-stream",
    )
    create = httpx.post(
        f"{base}/items",
        headers={
            **headers,
            "Content-Type": "application/json",
            # Random idempotency token: a retried create WITHOUT one makes a
            # duplicate attachment item. A 412 means token replay -> hard raise.
            "Zotero-Write-Token": os.urandom(16).hex(),
        },
        json=[template],
        timeout=120,
    )
    if create.status_code != 200:
        raise RuntimeError(
            f"Zotero create-attachment failed: {create.status_code}: "
            f"{create.text[:200]}"
        )
    create_body: dict[str, Any] = create.json()
    if "0" not in create_body.get("success", {}):
        raise RuntimeError(
            f"Zotero create-attachment reported no success: "
            f"{create_body.get('failed')}"
        )
    new_key: str = create_body["success"]["0"]

    # 2. Upload AUTHORIZATION.
    auth = httpx.post(
        f"{base}/items/{new_key}/file",
        headers={
            **headers,
            "Content-Type": "application/x-www-form-urlencoded",
            "If-None-Match": "*",
        },
        data={
            "md5": md5,
            "filename": zip_name,
            "filesize": filesize,
            "mtime": mtime,
        },
        timeout=120,
    )
    if auth.status_code != 200:
        raise RuntimeError(
            f"Zotero upload-authorization failed: {auth.status_code}: "
            f"{auth.text[:200]}"
        )
    auth_body: dict[str, Any] = auth.json()
    if auth_body.get("exists"):
        # Identical md5 already stored -> maps to the old `unchanged` success.
        return new_key

    # 3. POST the bytes to S3. Content-Type MUST be auth["contentType"]
    # verbatim (S3 signs over it; anything else -> 403 SignatureDoesNotMatch).
    # Stream prefix+bytes+suffix to avoid a 2x-memory copy on large zips.
    s3 = httpx.post(
        auth_body["url"],
        headers={"Content-Type": auth_body["contentType"]},
        content=iter(
            [auth_body["prefix"].encode(), data, auth_body["suffix"].encode()]
        ),
        timeout=httpx.Timeout(600.0, connect=60.0),
    )
    if s3.status_code not in (200, 201):
        raise RuntimeError(
            f"Zotero S3 upload failed: {s3.status_code}: {s3.text[:200]}"
        )

    # 4. REGISTER the upload.
    register = httpx.post(
        f"{base}/items/{new_key}/file",
        headers={
            **headers,
            "Content-Type": "application/x-www-form-urlencoded",
            "If-None-Match": "*",
        },
        data={"upload": auth_body["uploadKey"]},
        timeout=120,
    )
    if register.status_code != 204:
        raise RuntimeError(
            f"Zotero register-upload failed: {register.status_code}: "
            f"{register.text[:200]}"
        )
    return new_key


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

    # Hardened client: lifts pyzotero's 30s per-call read timeout (it overrides
    # any client-level timeout) so item-find pagination on a slow/flaky API has
    # headroom. Transient 5xx/timeouts are retried at the call site below.
    zot = make_zotero_client(library_id, library_type, api_key)

    # Find the parent item
    item_key = with_zotero_retry(lambda: _find_zotero_item(zot, citation_key))
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

        # Low-level 4-step upload (create -> auth -> S3 -> register). Replaces
        # pyzotero's attachment_simple, which returned a silent failure dict
        # here (1.11.0) and never raised. upload_attachment RAISES on any bad
        # status, so the prune below never runs on a failed upload and prior
        # good zips survive -- the same invariant the deleted d350add assert
        # protected, now enforced by control flow.
        upload_attachment(zot, item_key, zip_path, zip_name)
        uploaded = packed

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
