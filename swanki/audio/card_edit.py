"""
swanki/audio/card_edit.py
[[swanki.audio.card_edit]]
https://github.com/Mjvolk3/Swanki/tree/main/swanki/audio/card_edit.py
Test file: tests/test_audio_card_edit.py

Precise per-chunk editing of complementary CARD audio, unified with the pure-
audio editor in ``comment_edit.edit_chunk``. Card audio uses a nested per-card
manifest (``card_chunks/{uuid}_manifest.json`` with ``sides.front``/``sides.back``)
that ``edit_chunk`` does not understand. ``edit_card_chunk`` translates one side
into a synthetic FLAT manifest (citation excluded, tts chunks re-indexed) under
``card_chunks/_sideedit/``, delegates to the UNCHANGED ``edit_chunk`` for the
single-chunk re-TTS + ``_edits/`` audit, re-prepends the citation (front only),
writes the canonical side mp3, and propagates the shaped text back into the
nested manifest. Direct-write / single-chunk sides and legacy manifests with no
editable tts chunks fall back to a whole-side re-TTS (absorbing the retired
``scripts/regen_card_audio_side.py`` stopgap).
"""

import json
import re
from pathlib import Path

from pydantic import BaseModel, Field

from ._common import (
    append_chunk_pause,
    chunk_text,
    combine_audio,
    text_to_speech,
)
from .card import _preprocess_for_tts
from .comment_edit import _SPEED_BY_AUDIO_TYPE, ChunkEditResult, edit_chunk


class CardChunkEditResult(BaseModel):
    """Outcome of an :func:`edit_card_chunk` call.

    Echoes :class:`swanki.audio.comment_edit.ChunkEditResult` and adds the card
    side and the ORIGINAL (nested-manifest) chunk list position so the caller
    knows which physical card chunk moved.
    """

    action: str = Field(description="Action taken or escalated, from edit_chunk")
    rationale: str = Field(description="One-sentence reason for the action")
    side: str = Field(description="Card side edited: front or back")
    side_file: Path = Field(description="Canonical side mp3 written")
    original_index: int = Field(
        description="Position in the nested manifest's sides[side]['chunks']"
    )


def _resolve_speed(manifest: dict) -> float:
    """Resolve the re-TTS speed: nested-manifest ``speed`` else the card fallback."""
    speed = manifest.get("speed")
    if speed is None:
        return _SPEED_BY_AUDIO_TYPE["card"]
    return float(speed)


def _load_side_transcript(
    output_dir: Path, card_id: str, side: str, side_chunks: list[dict]
) -> str:
    """Recover a whole-side transcript for the re-TTS fallback.

    Primary source is the nested-manifest chunk ``text`` joined back; backstop
    is the ``complementary_transcripts/*_{side}.md`` Generated-Transcript block
    written at gen time.

    Args:
        output_dir: Pipeline output dir (parent of gen-md-complementary-audio).
        card_id: Card uuid, used to locate the transcript sidecar.
        side: front or back.
        side_chunks: The nested-manifest ``sides[side]['chunks']`` list.

    Returns:
        The recovered transcript text.

    Raises:
        RuntimeError: When no transcript is recoverable.
    """
    tts_texts = [
        c["text"] for c in side_chunks if c.get("type") == "tts" and c.get("text")
    ]
    if tts_texts:
        return "\n\n".join(tts_texts)

    transcripts_dir = output_dir / "complementary_transcripts"
    matches = (
        sorted(transcripts_dir.glob(f"*{card_id}*{side}.md"))
        if transcripts_dir.is_dir()
        else []
    )
    if matches:
        text = matches[0].read_text()
        m = re.search(
            r"\*\*Generated Transcript:\*\*\s*(.*?)(?:\s*\*\*Citation Added|\Z)",
            text,
            re.S,
        )
        if m and m.group(1).strip():
            return m.group(1).strip()

    raise RuntimeError(
        f"No transcript recoverable for card {card_id} side {side}: nested "
        f"manifest has no tts chunk text and no parseable "
        f"complementary_transcripts/*_{side}.md"
    )


def _whole_side_retts(
    *,
    card_manifest_path: Path,
    side: str,
    manifest: dict,
    side_chunks: list[dict],
    new_text: str | None,
    speed: float,
    tts_kwargs: dict,
) -> Path:
    """Re-TTS an entire side from its transcript and overwrite the side mp3.

    Mirrors the front/back assembly in
    :func:`swanki.audio.card.generate_card_audio`: chunk the transcript,
    ``append_chunk_pause`` + preprocess + TTS each chunk, re-prepend the
    citation audio (front only), ``combine_audio(crossfade_ms=0)``. Absorbs the
    retired ``scripts/regen_card_audio_side.py`` stopgap.

    Args:
        card_manifest_path: Path to the nested per-card manifest.
        side: front or back.
        manifest: Parsed nested manifest dict.
        side_chunks: The ``sides[side]['chunks']`` list (may be empty/missing).
        new_text: Verbatim replacement transcript; overrides the recovered one.
        speed: Resolved re-TTS speed.
        tts_kwargs: Provider config forwarded to ``text_to_speech``.

    Returns:
        The canonical side mp3 path that was overwritten.
    """
    card_chunks_dir = card_manifest_path.parent
    audio_dir = card_chunks_dir.parent
    output_dir = audio_dir.parent
    provider = str(tts_kwargs.get("provider", "fish_speech"))

    side_file = manifest["front_file"] if side == "front" else manifest["back_file"]
    side_mp3 = audio_dir / side_file

    transcript = (
        new_text
        if new_text is not None
        else _load_side_transcript(output_dir, manifest["card_id"], side, side_chunks)
    )

    work = card_chunks_dir / "_sideedit"
    work.mkdir(parents=True, exist_ok=True)
    chunk_paths: list[Path] = []

    if side == "front" and manifest.get("citation_audio"):
        citation = (card_chunks_dir / manifest["citation_audio"]).resolve()
        assert citation.exists(), f"citation audio missing: {citation}"
        chunk_paths.append(citation)

    for i, chunk in enumerate(chunk_text(transcript)):
        cp = work / f"{manifest['card_id']}_{side}_retts_chunk{i}.mp3"
        paused = append_chunk_pause(chunk, provider)
        text_to_speech(
            _preprocess_for_tts(paused, tts_kwargs), "", cp, "", speed, **tts_kwargs
        )
        chunk_paths.append(cp)

    combine_audio(chunk_paths, side_mp3, crossfade_ms=0)
    return side_mp3


def edit_card_chunk(
    card_manifest_path: Path,
    side: str,
    idx: int,
    *,
    comment: str | None = None,
    new_text: str | None = None,
    speech_only: bool = False,
    model: str | None = None,
    tts_kwargs: dict,
) -> CardChunkEditResult:
    """Apply one precise edit to one chunk of one card side, citation preserved.

    Reads the nested per-card manifest, selects ``sides[side]['chunks']``, and:
      - When the side has editable tts chunks: builds a synthetic FLAT manifest
        under ``card_chunks/_sideedit/`` (citation excluded, tts chunks
        re-indexed contiguous 0-based) and delegates to the UNCHANGED
        :func:`swanki.audio.comment_edit.edit_chunk` for the single-chunk
        re-TTS + ``_edits/`` audit. The citation (front only) is then
        re-prepended with ``combine_audio(crossfade_ms=0)`` into the canonical
        side mp3, the edited shaped text is propagated back into the nested
        manifest, and the synthetic manifest is deleted.
      - When the side has NO editable tts chunks (direct-write / single-chunk
        side, or a legacy manifest): falls back to a whole-side re-TTS.

    Args:
        card_manifest_path: Path to ``card_chunks/{uuid}_manifest.json``.
        side: ``"front"`` or ``"back"``.
        idx: tts-chunk-local index (citation invisible; 0 == first tts chunk).
        comment: Reviewer comment driving the agent rewrite.
        new_text: Explicit replacement prose (bypasses the agent). In the
            whole-side fallback this replaces the entire side transcript.
        speech_only: Re-roll the stored chunk text without a content change.
        model: pydantic-ai model string; required for the ``comment`` path.
        tts_kwargs: Provider config (incl. ``preprocessor`` + reference voice).

    Returns:
        A :class:`CardChunkEditResult`.

    Raises:
        RuntimeError: When the whole-side fallback finds no transcript.
    """
    assert card_manifest_path.exists(), f"Card manifest missing: {card_manifest_path}"
    assert side in {"front", "back"}, f"side must be front or back, got {side!r}"

    manifest = json.loads(card_manifest_path.read_text())
    if side == "back":
        assert manifest.get("back_file"), (
            "card has no back side (back_file is null); cannot edit back"
        )

    speed = _resolve_speed(manifest)
    side_chunks: list[dict] = manifest["sides"].get(side, {}).get("chunks", [])
    tts_chunks = [c for c in side_chunks if c.get("type") == "tts"]

    side_file = manifest["front_file"] if side == "front" else manifest["back_file"]
    audio_dir = card_manifest_path.parent.parent
    side_mp3 = audio_dir / side_file

    # No editable tts chunks -> whole-side re-TTS fallback.
    if not tts_chunks:
        written = _whole_side_retts(
            card_manifest_path=card_manifest_path,
            side=side,
            manifest=manifest,
            side_chunks=side_chunks,
            new_text=new_text,
            speed=speed,
            tts_kwargs=tts_kwargs,
        )
        return CardChunkEditResult(
            action="whole_side_retts",
            rationale="side has no editable tts chunks; re-TTSed from transcript",
            side=side,
            side_file=written,
            original_index=-1,
        )

    assert 0 <= idx < len(tts_chunks), (
        f"tts-chunk idx {idx} out of range (side {side} has {len(tts_chunks)} tts chunks)"
    )

    # Build the synthetic FLAT manifest: citation excluded, tts re-indexed.
    sideedit_dir = card_manifest_path.parent / "_sideedit"
    sideedit_dir.mkdir(parents=True, exist_ok=True)
    synthetic_chunks = [
        {
            "index": j,
            "section": 0,
            "boundary": "paragraph",
            "text": chunk["text"],
            "file": f"../{chunk['file']}",
        }
        for j, chunk in enumerate(tts_chunks)
    ]
    synthetic = {
        "audio_type": manifest["audio_type"],
        "output_file": f"../{side_file}",
        "bookend_start": None,
        "bookend_end": None,
        "postprocessor": {},
        "speed": speed,
        "chunks": synthetic_chunks,
    }
    synthetic_path = sideedit_dir / f"{manifest['card_id']}_{side}_manifest.json"
    synthetic_path.write_text(json.dumps(synthetic, indent=2))

    # Delegate the single-chunk re-TTS + restitch (body only) to edit_chunk.
    result: ChunkEditResult = edit_chunk(
        synthetic_path,
        idx,
        comment=comment,
        new_text=new_text,
        speech_only=speech_only,
        tts_kwargs=tts_kwargs,
        model=model,
    )

    # The original nested-manifest list position of the edited tts chunk.
    original_index = side_chunks.index(tts_chunks[idx])

    if result.action in ("needs_section_regen", "cannot_fix"):
        synthetic_path.unlink()
        return CardChunkEditResult(
            action=result.action,
            rationale=result.rationale,
            side=side,
            side_file=side_mp3,
            original_index=original_index,
        )

    # edit_chunk wrote the BODY (citation excluded) to the canonical side mp3.
    # Re-prepend the citation for front when present (same combine as gen time).
    if side == "front" and manifest.get("citation_audio"):
        citation = (card_manifest_path.parent / manifest["citation_audio"]).resolve()
        assert citation.exists(), f"citation audio missing: {citation}"
        combine_audio([citation, side_mp3], side_mp3, crossfade_ms=0)

    # Propagate the edited shaped text back into the nested manifest.
    if result.action == "edit_text":
        edited = json.loads(synthetic_path.read_text())
        side_chunks[original_index]["text"] = edited["chunks"][idx]["text"]
        manifest["sides"][side]["chunks"] = side_chunks
        card_manifest_path.write_text(json.dumps(manifest, indent=2))

    # Append a card-tagged line to the _edits/ log edit_chunk created.
    edits_dir = sideedit_dir / "_edits"
    edits_dir.mkdir(parents=True, exist_ok=True)
    edits_log = edits_dir / "edits_log.jsonl"
    with edits_log.open("a") as f:
        f.write(
            json.dumps(
                {
                    "card_id": manifest["card_id"],
                    "side": side,
                    "original_index": original_index,
                    "reindexed_idx": idx,
                    "action": result.action,
                }
            )
            + "\n"
        )

    synthetic_path.unlink()
    return CardChunkEditResult(
        action=result.action,
        rationale=result.rationale,
        side=side,
        side_file=side_mp3,
        original_index=original_index,
    )
