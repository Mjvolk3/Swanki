"""
swanki/audio/manifest.py
[[swanki.audio.manifest]]
https://github.com/Mjvolk3/Swanki/tree/main/swanki/audio/manifest.py
Test file: tests/test_audio_manifest.py

Audio manifest tracking — records which output directory holds the current
version of each audio type and what settings produced it.
"""

import hashlib
import json
import logging
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


def _hash_string(s: str) -> str:
    """SHA-256 hash truncated to 12 hex chars."""
    return hashlib.sha256(s.encode()).hexdigest()[:12]


def read_manifest(paper_dir: Path) -> dict[str, Any]:
    """Read the audio manifest for a paper directory.

    Args:
        paper_dir: Top-level paper directory in Swanki_Data
            (e.g., ``Swanki_Data/merzbacher...``).

    Returns:
        Manifest dict, or empty dict if no manifest exists.
    """
    manifest_path = paper_dir / "_audio_manifest.json"
    if manifest_path.exists():
        return json.loads(manifest_path.read_text())  # type: ignore[no-any-return]
    return {}


def write_manifest(paper_dir: Path, manifest: dict[str, Any]) -> Path:
    """Write the audio manifest for a paper directory.

    Args:
        paper_dir: Top-level paper directory in Swanki_Data.
        manifest: Manifest dict to write.

    Returns:
        Path to the written manifest file.
    """
    manifest_path = paper_dir / "_audio_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, default=str))
    logger.info(f"Updated audio manifest: {manifest_path}")
    return manifest_path


def update_manifest_entry(
    paper_dir: Path,
    citation_key: str,
    audio_type: str,
    output_dir: Path,
    filename: str,
    tts_model: str,
    prompt_hash: str,
    word_count: int = 0,
) -> None:
    """Update a single audio type entry in the manifest.

    Args:
        paper_dir: Top-level paper directory.
        citation_key: Paper citation key.
        audio_type: One of "lecture", "summary", "reading", "cards".
        output_dir: The output subdirectory containing the file.
        filename: Audio filename.
        tts_model: ElevenLabs model ID used.
        prompt_hash: Hash of the system prompt that generated the transcript.
        word_count: Word count of the transcript.
    """
    manifest = read_manifest(paper_dir)

    if "citation_key" not in manifest:
        manifest["citation_key"] = citation_key

    if "audio" not in manifest:
        manifest["audio"] = {}

    manifest["audio"][audio_type] = {
        "file": filename,
        "output_dir": output_dir.name,
        "generated_at": datetime.now(UTC).isoformat(),
        "tts_model": tts_model,
        "prompt_hash": prompt_hash,
        "word_count": word_count,
    }

    write_manifest(paper_dir, manifest)


def find_audio_file(paper_dir: Path, audio_type: str) -> Path | None:
    """Find the current audio file for a given type using the manifest.

    Falls back to scanning output directories if no manifest exists.

    Args:
        paper_dir: Top-level paper directory.
        audio_type: One of "lecture", "summary", "reading".

    Returns:
        Path to the audio file, or None if not found.
    """
    suffix_map = {
        "lecture": "-lecture-audio.mp3",
        "summary": "-summary-audio.mp3",
        "reading": "-reading-audio.mp3",
    }
    suffix = suffix_map.get(audio_type)
    if not suffix:
        return None

    # Try manifest first
    manifest = read_manifest(paper_dir)
    if "audio" in manifest and audio_type in manifest["audio"]:
        entry = manifest["audio"][audio_type]
        candidate = paper_dir / entry["output_dir"] / entry["file"]
        if candidate.exists():
            return candidate

    # Fallback: scan output dirs in reverse order (highest _N first = newest)
    output_dirs = sorted(
        [d for d in paper_dir.iterdir() if d.is_dir() and d.name != "__pycache__"],
        key=lambda d: d.name,
        reverse=True,
    )
    for d in output_dirs:
        for f in d.iterdir():
            if f.name.endswith(suffix):
                return f

    return None


def export_collection(
    data_dir: Path,
    citation_keys: list[str],
    output_dir: Path,
    audio_types: list[str] | None = None,
    collection_name: str = "swanki-export",
) -> Path:
    """Export audio files for a collection of papers into a zip.

    Creates a structured zip: ``collection_name/lecture/``,
    ``collection_name/summary/``, ``collection_name/transcript/``.

    Args:
        data_dir: Path to Swanki_Data directory.
        citation_keys: List of citation keys to include.
        output_dir: Directory to write the zip file.
        audio_types: Audio types to include. Defaults to all three.
        collection_name: Name for the top-level directory in the zip.

    Returns:
        Path to the created zip file.
    """
    import shutil
    import tempfile
    import zipfile

    if audio_types is None:
        audio_types = ["lecture", "summary", "reading"]

    # Map audio_type to folder name in zip
    folder_map = {
        "lecture": "Lecture",
        "summary": "Summary",
        "reading": "Transcript",
    }

    staging = Path(tempfile.mkdtemp()) / collection_name
    for audio_type in audio_types:
        (staging / folder_map.get(audio_type, audio_type)).mkdir(
            parents=True, exist_ok=True
        )

    found: dict[str, list[str]] = {t: [] for t in audio_types}
    missing: dict[str, list[str]] = {t: [] for t in audio_types}

    for key in citation_keys:
        paper_dir = data_dir / key
        if not paper_dir.exists():
            logger.warning(f"Paper directory not found: {paper_dir}")
            for t in audio_types:
                missing[t].append(key)
            continue

        for audio_type in audio_types:
            audio_file = find_audio_file(paper_dir, audio_type)
            if audio_file:
                dest_folder = staging / folder_map.get(audio_type, audio_type)
                shutil.copy2(audio_file, dest_folder / audio_file.name)
                found[audio_type].append(key)
            else:
                missing[audio_type].append(key)

    # Log summary
    for t in audio_types:
        logger.info(
            f"{folder_map.get(t, t)}: {len(found[t])}/{len(citation_keys)} papers"
        )
        if missing[t]:
            logger.warning(f"  Missing {t}: {', '.join(missing[t])}")

    # Zip
    zip_path = output_dir / f"{collection_name}.zip"
    with zipfile.ZipFile(str(zip_path), "w", zipfile.ZIP_DEFLATED) as zf:
        for root, _, files in sorted(Path.walk(staging)):  # type: ignore[union-attr]
            for f in sorted(files):
                file_path = root / f
                arcname = str(file_path.relative_to(staging.parent))
                zf.write(file_path, arcname)

    # Cleanup staging
    shutil.rmtree(staging.parent if staging.parent.name.startswith("tmp") else staging)

    logger.info(f"Exported {zip_path} ({zip_path.stat().st_size / 1024 / 1024:.1f} MB)")
    return zip_path
