"""
swanki/audio/comment_edit.py
[[swanki.audio.comment_edit]]
https://github.com/Mjvolk3/Swanki/tree/main/swanki/audio/comment_edit.py
Test file: tests/test_audio_comment_edit.py

Comment-driven precise audio chunk edits with a ``_edits/`` intervention audit
trail. A reviewer comment (ABS bookmark / Zotero annotation) drives a single-
chunk re-TTS: ``chunk_edit_agent`` rewrites the chunk text (or flags it a
delivery-only re-roll), the new prose runs through the SAME preprocessor chain
a fresh full-gen uses, only that one chunk mp3 is re-rendered, and the chapter
audio is restitched. Classification, the single human-review gate, and
publishing stay in the audio-fix-from-annotations skill; this module is the
swanki-native "apply" step, replacing one-off ``fix_*.py`` scripts.
"""

import json
import logging
import subprocess
from datetime import UTC, datetime
from pathlib import Path

from pydantic import BaseModel, Field

from ..llm.agents import chunk_edit_agent
from ..llm.safety import with_safety_retry
from ..models.cards import ChunkEditResponse
from ._common import (
    append_chunk_pause,
    chunk_time_window,
    preprocess_for_tts,
    restitch_from_chunks,
    text_to_speech,
)

logger = logging.getLogger(__name__)

_CHUNK_EDIT_INSTRUCTIONS = (
    "You revise ONE chunk of an audio transcript in response to a reviewer's "
    "comment about how it sounded. You are given the chunk's current text, the "
    "adjacent chunks for continuity, the audio type, and the comment. Choose "
    "exactly one action:\n"
    "- edit_text: the comment asks for a wording/content change you can make "
    "WITHIN this single chunk. Return the full rewritten chunk in revised_text "
    "as plain prose (no markdown, no pause tags), preserving the speaker's "
    "voice (books are first-person) and the flow into the neighboring chunks. "
    "Change only what the comment requires.\n"
    "- speech_only: the text is correct but the delivery/prosody is wrong "
    "(e.g. a question read with a flat tone, words jammed together). "
    "revised_text stays null.\n"
    "- needs_section_regen: the comment is conceptual or structural and cannot "
    "be satisfied by editing this one chunk (e.g. 'make the main point "
    "stronger', 'the anecdotes are out of order').\n"
    "- cannot_fix: the comment is not actionable on this chunk."
)


class ChunkEditResult(BaseModel):
    """Outcome of an :func:`edit_chunk` call, returned to the calling skill."""

    action: str = Field(description="Action taken (edit_text/speech_only) or escalated")
    rationale: str = Field(description="One-sentence reason for the action")
    output_file: Path | None = Field(
        default=None,
        description="Restitched chapter audio; None when no re-TTS happened",
    )
    start_ms: int | None = Field(
        default=None, description="Edited chunk start in the restitched audio"
    )
    end_ms: int | None = Field(
        default=None, description="Edited chunk end in the restitched audio"
    )


def _git_short_hash() -> str:
    """Return ``git rev-parse --short HEAD`` for provenance, or '' if unavailable."""
    result = subprocess.run(
        ["git", "rev-parse", "--short", "HEAD"],
        capture_output=True,
        text=True,
    )
    return result.stdout.strip() if result.returncode == 0 else ""


def _agent_rewrite(
    chunk: dict,
    by_idx: dict[int, dict],
    idx: int,
    comment: str,
    audio_type: str,
    model: str,
) -> ChunkEditResponse:
    """Ask ``chunk_edit_agent`` how to act on one comment, with safety retry."""
    prev_text = (by_idx.get(idx - 1) or {}).get("text", "")
    next_text = (by_idx.get(idx + 1) or {}).get("text", "")
    user_msg = (
        f"AUDIO TYPE: {audio_type}\n\n"
        f"REVIEWER COMMENT:\n{comment}\n\n"
        f"PREVIOUS CHUNK (context, do not edit):\n{prev_text}\n\n"
        f"TARGET CHUNK (the one to consider editing):\n{chunk['text']}\n\n"
        f"NEXT CHUNK (context, do not edit):\n{next_text}"
    )
    # with_safety_retry types its agent param as Agent[None, str]; passing a
    # structured-output agent is the same accepted pattern used throughout
    # pipeline.py (a safety.py typing limitation, not a real mismatch).
    result = with_safety_retry(
        chunk_edit_agent,  # type: ignore[arg-type]
        user_msg,
        instructions=_CHUNK_EDIT_INSTRUCTIONS,
        model=model,
        label=f"chunk edit {idx}",
    )
    return result.output


def _archive_chunk(
    chunks_dir: Path, chunk: dict, manifest: dict, stamp: str
) -> None:
    """Snapshot the prior chunk audio+text and the manifest into ``_edits/``.

    Called BEFORE any overwrite, so the first edit captures the original
    baseline and repeated edits to one chunk build a full evolution trail.
    """
    edits_dir = chunks_dir / "_edits"
    edits_dir.mkdir(exist_ok=True)
    idx = chunk["index"]
    src_mp3 = chunks_dir / chunk["file"]
    if src_mp3.exists():
        (edits_dir / f"chunk{idx}_{stamp}.mp3").write_bytes(src_mp3.read_bytes())
    (edits_dir / f"chunk{idx}_{stamp}.txt").write_text(chunk["text"])
    (edits_dir / f"manifest_{stamp}.json").write_text(
        json.dumps(manifest, indent=2) + "\n"
    )


def _append_edit_log(
    chunks_dir: Path,
    *,
    idx: int,
    comment: str | None,
    old_text: str,
    new_text: str | None,
    action: str,
    rationale: str,
    output_file: Path | None,
    stamp: str,
) -> None:
    """Append one JSON record per intervention to ``_edits/edits_log.jsonl``."""
    edits_dir = chunks_dir / "_edits"
    edits_dir.mkdir(exist_ok=True)
    record = {
        "ts": stamp,
        "idx": idx,
        "comment": comment,
        "old_text": old_text,
        "new_text": new_text,
        "action": action,
        "rationale": rationale,
        "output_file": str(output_file) if output_file else None,
        "git_hash": _git_short_hash(),
    }
    with (edits_dir / "edits_log.jsonl").open("a") as f:
        f.write(json.dumps(record) + "\n")


def edit_chunk(
    manifest_path: Path,
    idx: int,
    *,
    comment: str | None = None,
    new_text: str | None = None,
    speech_only: bool = False,
    tts_kwargs: dict,
    speed: float = 1.1,
    model: str | None = None,
    section_pause_ms: int | None = None,
) -> ChunkEditResult:
    """Apply one reviewer comment to one audio chunk and restitch the chapter.

    Three render paths (the caller/skill chooses by which arg it passes):
      - ``speech_only=True``: re-roll the stored chunk text VERBATIM (Fish
        temperature gives a fresh take). The stored text is already shaped, so
        nothing is re-preprocessed.
      - ``comment=...`` (the typical path): ``chunk_edit_agent`` decides the
        action; ``edit_text`` rewrites the prose, ``speech_only`` re-rolls, and
        ``needs_section_regen`` / ``cannot_fix`` are returned WITHOUT touching
        audio (the human escalates).
      - ``new_text=...``: use the caller's verbatim replacement prose.

    For ``edit_text``, new prose runs the full chain
    (``preprocess_for_tts(..., add_pauses=True)`` then ``append_chunk_pause``)
    so it matches how a fresh full-gen builds and stores a chunk; the resulting
    shaped text is persisted to the manifest. Every edit archives the prior
    chunk + manifest into ``_edits/`` first. ``restitch_from_chunks`` rewrites
    ``chunk_timeline.json``; the returned window is the edited chunk's NEW
    position so the caller can re-mark ABS bookmarks (which do not migrate).

    Args:
        manifest_path: Path to the chunk ``chunk_manifest.json``.
        idx: Target chunk index (audio-type-local).
        comment: Reviewer comment to drive the agent rewrite.
        new_text: Explicit replacement prose (bypasses the agent).
        speech_only: Re-roll the stored text without a content change.
        tts_kwargs: Provider config incl. the ``preprocessor`` sub-tree and the
            paper's reference voice; passed to ``text_to_speech`` (which reads
            only the flat provider keys) and ``preprocess_for_tts``.
        speed: Playback speed for TTS.
        model: pydantic-ai model string; required for the ``comment`` path.
        section_pause_ms: Optional restitch override.

    Returns:
        A :class:`ChunkEditResult` with the action, rationale, restitched
        output path, and the edited chunk's new ``(start_ms, end_ms)``.
    """
    assert manifest_path.exists(), f"Manifest missing: {manifest_path}"
    assert speech_only or new_text is not None or comment is not None, (
        "edit_chunk needs one of speech_only=True, new_text=..., or comment=..."
    )
    manifest = json.loads(manifest_path.read_text())
    assert "postprocessor" in manifest, (
        "Manifest has no postprocessor block; restitch cannot reproduce the "
        "original silence/gain. Refusing to edit."
    )
    audio_type = manifest["audio_type"]
    by_idx = {c["index"]: c for c in manifest["chunks"]}
    assert idx in by_idx, f"Chunk index {idx} not in manifest"
    chunk = by_idx[idx]

    provider = str(tts_kwargs.get("provider", "elevenlabs"))
    if provider == "fish_speech":
        assert tts_kwargs.get("reference_id"), (
            "fish_speech provider requires a reference_id in tts_kwargs; "
            "without it the edited chunk renders in the wrong voice."
        )

    # Resolve action + the raw new prose (if any).
    raw_new: str | None = None
    if speech_only:
        action, rationale = "speech_only", "caller requested a speech-only re-roll"
    elif new_text is not None:
        action, rationale, raw_new = "edit_text", "explicit caller-supplied text", new_text
    else:
        assert comment is not None  # guaranteed by the args assert above
        assert model, "model (pydantic-ai model string) required for the comment path"
        resp = _agent_rewrite(chunk, by_idx, idx, comment, audio_type, model)
        action, rationale = resp.action, resp.rationale
        if action in ("needs_section_regen", "cannot_fix"):
            return ChunkEditResult(action=action, rationale=rationale)
        if action == "edit_text":
            assert resp.revised_text, "agent returned edit_text without revised_text"
            raw_new = resp.revised_text

    # New prose gets the full original chain (scrubbers + pauses + boundary
    # strip); speech_only re-rolls the already-shaped stored text verbatim.
    if action == "edit_text":
        assert raw_new is not None  # set by every edit_text path above
        render_text = append_chunk_pause(
            preprocess_for_tts(raw_new, tts_kwargs, add_pauses=True), provider
        )
    else:
        render_text = chunk["text"]

    # Archive BEFORE overwriting (first edit captures the baseline).
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    chunks_dir = manifest_path.parent
    old_text = chunk["text"]
    _archive_chunk(chunks_dir, chunk, manifest, stamp)

    # Persist the shaped text so the manifest matches a fresh gen.
    if action == "edit_text":
        chunk["text"] = render_text
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")

    # Re-TTS only this chunk's mp3, in place.
    out_mp3 = chunks_dir / chunk["file"]
    text_to_speech(
        text=render_text,
        voice_id="",
        output_path=out_mp3,
        api_key="",
        speed=speed,
        **tts_kwargs,
    )

    # Restitch the chapter audio (rewrites chunk_timeline.json).
    output_file = manifest_path.parent.parent / manifest["output_file"]
    restitch_from_chunks(manifest_path, output_file, section_pause_ms=section_pause_ms)

    start_ms, end_ms = chunk_time_window(chunks_dir, audio_type, idx)

    _append_edit_log(
        chunks_dir,
        idx=idx,
        comment=comment,
        old_text=old_text,
        new_text=render_text if action == "edit_text" else None,
        action=action,
        rationale=rationale,
        output_file=output_file,
        stamp=stamp,
    )
    return ChunkEditResult(
        action=action,
        rationale=rationale,
        output_file=output_file,
        start_ms=start_ms,
        end_ms=end_ms,
    )
