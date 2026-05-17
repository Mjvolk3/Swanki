"""
swanki/audio/surgical.py
[[swanki.audio.surgical]]
https://github.com/Mjvolk3/Swanki/tree/main/swanki/audio/surgical.py
Test file: tests/test_audio_surgical.py

Surgical single-chunk re-TTS + restitch. Given a chunk manifest and a set
of chunk-index edits, re-render only those chunks and restitch the final
audio, leaving every untouched chunk byte-identical. Generalizes the
one-off scripts/regen_campagne_lecture_chunks.py pattern so any audio-quality
fix (a code-level scrubber fix, or hand-corrected chunk text) can be applied
without a full pipeline regeneration.
"""

import json
from collections.abc import Mapping
from pathlib import Path

import requests

from ._common import restitch_from_chunks, text_to_speech


def fish_speech_healthy(server_url: str, timeout: float = 5.0) -> bool:
    """Return True if the Fish Speech server answers an HTTP probe.

    Fish has no retry path and a single failed chunk aborts a batch, so the
    CLI pre-flights this before any re-TTS.

    Args:
        server_url: Base URL of the Fish Speech server.
        timeout: Per-request timeout in seconds.

    Returns:
        True when the server responds (any HTTP status), False on a
        connection/timeout error.
    """
    probe = server_url.rstrip("/") + "/v1/health"
    resp = requests.get(probe, timeout=timeout)
    if resp.status_code != 404:
        return resp.ok
    # Server reachable but no /v1/health route: a reachable root still
    # proves the process is up enough to accept TTS POSTs.
    return requests.get(server_url, timeout=timeout).status_code < 500


def regenerate_and_restitch(
    manifest_path: Path,
    chunk_edits: Mapping[int, str | None],
    *,
    audio_type: str | None = None,
    output_path: Path | None = None,
    speed: float = 1.1,
    tts_kwargs: Mapping[str, object] | None = None,
    section_pause_ms: int | None = None,
) -> Path:
    """Re-TTS selected chunks and restitch the final audio.

    For each ``index -> text`` in ``chunk_edits``: a non-None value replaces
    that chunk's recorded text (and is persisted back to the manifest so the
    transcript record stays truthful and future restitches stay correct); a
    None value re-renders the chunk's existing text unchanged (use when an
    upstream code fix means re-rendering the same text now yields correct
    audio). Only the named chunks' mp3s are rewritten; every other chunk
    file is reused untouched by :func:`restitch_from_chunks`.

    Args:
        manifest_path: Path to the chunk ``chunk_manifest.json``.
        chunk_edits: Map of chunk ``index`` to replacement text, or None to
            re-render the existing text.
        audio_type: When given, asserted equal to ``manifest["audio_type"]``
            so a wrong manifest (e.g. lecture vs reading) fails loudly --
            chunk indices are local per audio type.
        output_path: Final restitched mp3. Defaults to
            ``manifest_path.parent.parent / manifest["output_file"]``.
        speed: Playback speed passed to TTS (Fish renders ~1.1 for Swanki).
        tts_kwargs: Provider kwargs forwarded to :func:`text_to_speech`
            (e.g. provider, server_url, reference_id, temperature, format).
        section_pause_ms: Optional override forwarded to restitch.

    Returns:
        The restitched output mp3 path.
    """
    assert manifest_path.exists(), f"Manifest missing: {manifest_path}"
    manifest = json.loads(manifest_path.read_text())

    if audio_type is not None:
        actual = manifest.get("audio_type")
        assert actual == audio_type, (
            f"Manifest audio_type is {actual!r}, expected {audio_type!r} -- "
            "chunk indices are local per audio type; wrong manifest."
        )
    assert "postprocessor" in manifest, (
        "Manifest has no postprocessor block; restitch would not reproduce "
        "the original silence/gain. Refusing to surgically restitch."
    )

    chunks_dir = manifest_path.parent
    by_idx = {c["index"]: c for c in manifest["chunks"]}
    kwargs = dict(tts_kwargs or {})

    text_changed = False
    for idx, new_text in chunk_edits.items():
        assert idx in by_idx, f"Chunk index {idx} not in manifest"
        chunk = by_idx[idx]
        render_text = chunk["text"] if new_text is None else new_text
        if new_text is not None and new_text != chunk["text"]:
            chunk["text"] = new_text
            text_changed = True
        out = chunks_dir / chunk["file"]
        print(f"re-TTS chunk {idx} -> {out.name}")
        text_to_speech(
            text=render_text,
            voice_id="",
            output_path=out,
            api_key="",
            speed=speed,
            **kwargs,
        )

    if text_changed:
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
        print(f"updated manifest text for {manifest_path.name}")

    if output_path is None:
        output_path = manifest_path.parent.parent / manifest["output_file"]
    print(f"restitching -> {output_path}")
    restitch_from_chunks(
        manifest_path, output_path, section_pause_ms=section_pause_ms
    )
    return output_path
