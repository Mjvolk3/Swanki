"""
swanki/audio/source_corrections.py
[[swanki.audio.source-corrections]]
https://github.com/Mjvolk3/Swanki/tree/main/swanki/audio/source_corrections.py
Test file: tests/test_source_corrections.py

Opt-in source-correction APPLY layer. Reads a HAND-AUTHORED per-chapter YAML
spec of ``SourceCorrection`` rows and applies each to a reading/lecture manifest
chunk, then re-TTSs the touched chunks and restitches ONCE per track.

This is the "next layer" the report-only reading critic
(``swanki/audio/reading_correctness.py``) leaves open: it turns a verified
source-fidelity finding into corrected, re-voiced audio without re-implementing
re-TTS or drifting the manifest / ``chunk_timeline.json`` / mp3 out of sync. It
is a HIGHER bar than the critic (every ``override`` is human-verified against
the printed source) and is NEVER auto-populated from critic findings.

Two behaviors branch purely on the authored ``kind``:

- ``override`` -- the source is genuinely wrong. Substitute the corrected prose
  AND (reading only) splice a spoken ``[pause] Swanki correction: ... [pause]``
  note mid-chunk so the listener hears the dispute.
- ``restoration`` -- a mechanical fix (number-bug, splice removal, OCR garble,
  Try->Tyr). Substitute SILENTLY; no spoken note.

Lecture is first-person reformulated prose: no spoken notes even for overrides,
and no LLM rewriting in v1. A lecture correction applies only when ``wrong_text``
literally matches a lecture chunk (silent substitution); otherwise the applier
records ``not_applicable``. Reading FAILS LOUD when ``wrong_text`` is not found.

Each override-note chunk is stored PRE-SHAPED and re-rolled VERBATIM through the
``speech_only`` path of :func:`swanki.audio.comment_edit.edit_chunk` (no re-
preprocess, so formulas/quantities in the note are spoken as authored). The
single ``restitch_from_chunks`` per track is hoisted out via ``restitch=False``.
Requires a live Fish context (``edit_chunk`` asserts a ``reference_id``).
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import yaml  # type: ignore[import-untyped]

from ..models.cards import CorrectionAuditEntry, SourceCorrection
from ._common import restitch_from_chunks
from .comment_edit import _git_short_hash, edit_chunk

_TERMINATOR_RE = re.compile(r"[.!?]")


def load_correction_spec(spec_path: Path) -> list[SourceCorrection]:
    """Load and validate a per-chapter correction spec (YAML).

    Accepts either a top-level list of rows or a ``{corrections: [...]}`` wrapper.
    Each row is parsed through :class:`SourceCorrection`, so an invalid ``kind``
    or an ``override`` missing its ``reason`` fails loud at load time.

    Args:
        spec_path: Path to the ``<citation_key>.yaml`` correction spec.

    Returns:
        The parsed, validated correction rows in authored order.
    """
    assert spec_path.exists(), f"Correction spec missing: {spec_path}"
    raw = yaml.safe_load(spec_path.read_text())
    rows = raw["corrections"] if isinstance(raw, dict) else raw
    assert isinstance(rows, list), (
        f"Correction spec {spec_path} must be a list (or a 'corrections:' list)"
    )
    return [SourceCorrection.model_validate(row) for row in rows]


def _default_note(corr: SourceCorrection) -> str:
    """Assemble the default spoken note when the author supplied no ``note_text``.

    The framing ``[pause]`` tags are internal to the chunk once spliced mid-chunk,
    so they survive the verbatim ``speech_only`` re-roll.
    """
    return (
        f"[pause] Swanki correction: the source says {corr.wrong_text}, but "
        f"{corr.corrected_text} is correct, because {corr.reason} [pause]"
    )


def _splice_note(text: str, needle: str, note: str) -> str:
    """Splice ``note`` adjacent to the sentence containing ``needle``, mid-chunk.

    NEVER placed at ``text[0]`` or ``text[-1]``: ``append_chunk_pause`` strips
    leading+trailing ``[pause]`` tags for Fish, so a boundary note's framing
    pauses would vanish. Guarantees non-pause text before AND after the note.

    Args:
        text: Chunk text AFTER the ``wrong_text -> corrected_text`` substitution.
        needle: The just-substituted ``corrected_text`` to anchor on.
        note: The pre-shaped spoken note (with framing ``[pause]`` tags).

    Returns:
        The chunk text with the note spliced in mid-chunk.
    """
    pos = text.find(needle)
    assert pos != -1, "corrected_text vanished before splice"
    after = pos + len(needle)
    m = _TERMINATOR_RE.search(text, after)
    end = m.end() if m else len(text)
    if text[end:].strip():
        # Following text exists -> splice after the substitution sentence.
        return f"{text[:end].rstrip()} {note} {text[end:].lstrip()}"
    # Substitution is in the LAST sentence. Splice before its sentence start so
    # the correction sentence follows the note and both stay mid-chunk.
    starts = [t.end() for t in _TERMINATOR_RE.finditer(text[:pos])]
    if starts and starts[-1] > 0:
        cut = starts[-1]
        return f"{text[:cut].rstrip()} {note} {text[cut:].lstrip()}"
    # Single-sentence chunk: splice right after the substituted phrase so text
    # precedes AND follows the note.
    return f"{text[:after].rstrip()} {note} {text[after:].lstrip()}"


def _snippet(text: str, limit: int = 200) -> str:
    """Trim ``text`` to ``limit`` chars for the audit entry."""
    return text if len(text) <= limit else text[: limit - 1] + "…"


def _apply_one(
    corr: SourceCorrection,
    manifest_path: Path,
    *,
    tts_kwargs: dict,
    speed: float | None,
    git_hash: str,
) -> CorrectionAuditEntry:
    """Apply one correction to its manifest chunk and re-TTS that chunk verbatim.

    Reading fails loud when ``wrong_text`` is not found; lecture records
    ``not_applicable``. An already-applied id short-circuits (idempotency). The
    single per-track restitch is deferred to the batch (``restitch=False``).
    """
    spoken = corr.kind == "override" and corr.track == "reading"
    manifest = json.loads(manifest_path.read_text())
    chunks = manifest["chunks"]

    # Idempotency: a chunk already carrying this id short-circuits. Checked
    # BEFORE the wrong_text scan, whose needle is gone after a prior apply.
    for c in chunks:
        if corr.id in c.get("applied_corrections", []):
            return CorrectionAuditEntry(
                id=corr.id,
                track=corr.track,
                chunk_index=c["index"],
                kind=corr.kind,
                status="already_applied",
                spoken=spoken,
                wrong_snippet=_snippet(corr.wrong_text),
                corrected_snippet=_snippet(corr.corrected_text),
                git_hash=git_hash,
            )

    target = next((c for c in chunks if corr.wrong_text in c["text"]), None)
    if target is None:
        assert corr.track == "lecture", (
            f"Reading correction {corr.id!r}: wrong_text not found in any chunk "
            f"({corr.wrong_text!r}). Source re-OCR'd or chunk boundaries shifted."
        )
        return CorrectionAuditEntry(
            id=corr.id,
            track=corr.track,
            chunk_index=None,
            kind=corr.kind,
            status="not_applicable",
            spoken=False,
            wrong_snippet=_snippet(corr.wrong_text),
            corrected_snippet=_snippet(corr.corrected_text),
            git_hash=git_hash,
        )

    new_text = target["text"].replace(corr.wrong_text, corr.corrected_text)
    if spoken:
        note = corr.note_text or _default_note(corr)
        new_text = _splice_note(new_text, corr.corrected_text, note)
    target["text"] = new_text
    target.setdefault("applied_corrections", []).append(corr.id)

    # Persist the assembled verbatim text so edit_chunk's speech_only re-roll
    # reads the already-shaped text (no re-preprocess of formulas/quantities).
    manifest_path.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n"
    )
    edit_chunk(
        manifest_path,
        target["index"],
        speech_only=True,
        tts_kwargs=tts_kwargs,
        speed=speed,
        restitch=False,
    )
    return CorrectionAuditEntry(
        id=corr.id,
        track=corr.track,
        chunk_index=target["index"],
        kind=corr.kind,
        status="applied",
        spoken=spoken,
        wrong_snippet=_snippet(corr.wrong_text),
        corrected_snippet=_snippet(corr.corrected_text),
        git_hash=git_hash,
    )


def _write_audit(entries: list[CorrectionAuditEntry], path: Path) -> None:
    """Write the correction audit to ``path`` atomically (temp then rename)."""
    payload = {
        "summary": {
            "total": len(entries),
            "applied": sum(1 for e in entries if e.status == "applied"),
            "already_applied": sum(
                1 for e in entries if e.status == "already_applied"
            ),
            "not_applicable": sum(
                1 for e in entries if e.status == "not_applicable"
            ),
            "spoken": sum(1 for e in entries if e.spoken),
        },
        "corrections": [e.model_dump() for e in entries],
    }
    tmp = path.with_suffix(path.suffix + ".tmp")
    with open(tmp, "w") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    tmp.rename(path)


def apply_source_corrections(
    spec_path: Path,
    manifest_by_track: dict[str, Path],
    *,
    tts_kwargs: dict,
    audit_path: Path,
    speed: float | None = None,
) -> list[CorrectionAuditEntry]:
    """Apply a per-chapter correction spec to the given manifest track(s).

    Corrections whose ``track`` is absent from ``manifest_by_track`` are skipped
    (the pipeline invokes this once per generated track). Each applied
    correction re-TTSs exactly its one chunk (``restitch=False``); after all
    substitutions a track's audio is restitched ONCE. A JSON audit is emitted
    atomically.

    Args:
        spec_path: Path to the ``<citation_key>.yaml`` correction spec.
        manifest_by_track: Map of ``"reading"``/``"lecture"`` to the track's
            ``chunk_manifest.json``. Only present tracks are processed.
        tts_kwargs: Provider config (incl. Fish ``reference_id``) for the re-TTS.
        audit_path: Destination for the JSON correction audit.
        speed: Optional re-TTS speed; ``None`` reuses each manifest's own speed.

    Returns:
        One :class:`CorrectionAuditEntry` per processed correction.
    """
    corrections = load_correction_spec(spec_path)
    git_hash = _git_short_hash()
    entries: list[CorrectionAuditEntry] = []
    touched_tracks: set[str] = set()

    for corr in corrections:
        manifest_path = manifest_by_track.get(corr.track)
        if manifest_path is None:
            continue
        entry = _apply_one(
            corr,
            manifest_path,
            tts_kwargs=tts_kwargs,
            speed=speed,
            git_hash=git_hash,
        )
        entries.append(entry)
        if entry.status == "applied":
            touched_tracks.add(corr.track)

    for track in touched_tracks:
        manifest_path = manifest_by_track[track]
        manifest = json.loads(manifest_path.read_text())
        output_file = manifest_path.parent.parent / manifest["output_file"]
        restitch_from_chunks(manifest_path, output_file)

    _write_audit(entries, audit_path)
    return entries
