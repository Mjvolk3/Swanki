"""
swanki/audio/card_replace.py
[[swanki.audio.card_replace]]
https://github.com/Mjvolk3/Swanki/tree/main/swanki/audio/card_replace.py
Test file: tests/test_audio_card_replace.py

Surgical one-for-one CARD replacement in a live headless Anki collection. Where
``card_edit.edit_card_chunk`` rewrites ONE chunk of ONE side, ``replace_card``
swaps an ENTIRE card wholesale: new front text, new back text, BOTH audio sides
re-TTSed in place, the Front/Back fields rebuilt, and the live note patched via
AnkiConnect ``updateNoteFields`` + ``storeMediaFile`` (+ one AnkiWeb ``sync``) so
the note keeps its id / GUID / scheduling (no reimport, no GUID recompute).

It is a thin orchestrator over stable parts: it reuses ``card_edit._whole_side_retts``
for the per-side re-TTS assembly (citation re-prepend front-only, ``crossfade_ms=0``,
card speed), the pure ``anki_processor.prepare_for_anki`` for md->field HTML, and the
fail-fast ``delivery.targets.anki.ankiconnect_call`` for every collection mutation. It
also patches the on-disk ``cards-with-audio.md`` / ``cards-plain.md`` via ``model_copy``
(uuid preserved). Manifest-absent degrades to a text-only field update (``note_id``
required). This is a LIVE-COLLECTION PATCH only: it does NOT re-export a full apkg to
Zotero and takes no ABS step (per-card audio ships inside the apkg ``[sound:]``).
"""

import base64
import json
import logging
import re
from pathlib import Path

from pydantic import BaseModel, Field

from ..delivery.targets.anki import ankiconnect_call
from ..models.cards import CardContent, PlainCard
from ..processing.anki_processor import extract_cards, prepare_for_anki
from ..utils.formatting import humanize_citation_key
from .card_edit import _resolve_speed, _whole_side_retts

logger = logging.getLogger(__name__)

_AUDIO_FRONT_RE = re.compile(r"\[audio-front\]\(([^)]+)\)")
_AUDIO_BACK_RE = re.compile(r"\[audio-back\]\(([^)]+)\)")
_MEDIA_LINE_RE = re.compile(
    r"^\s*(?:\[audio-(?:front|back)\]\([^)]*\)|!\[[^\]]*\]\([^)]*\))\s*$"
)


class CardReplaceResult(BaseModel):
    """Outcome of a :func:`replace_card` call."""

    note_id: int = Field(description="AnkiConnect note id that was patched")
    front_file: Path | None = Field(
        default=None, description="Canonical front mp3 re-TTSed (None in text-only)"
    )
    back_file: Path | None = Field(
        default=None, description="Canonical back mp3 re-TTSed (None in text-only)"
    )
    synced: bool = Field(description="Whether a final AnkiWeb sync was issued")
    degraded: bool = Field(description="True when the manifest was absent (text-only)")


def _prefixed_front(citation_key: str, text: str) -> str:
    """Prepend ``@{citation_key}: `` unless already present (guards double-prefix)."""
    humanized = humanize_citation_key(citation_key)
    if text.startswith(f"@{citation_key}:") or text.startswith(f"{humanized}:"):
        return text
    return f"@{citation_key}: {text}"


def _resolve_note_id(url: str, uuid: str, note_id: int | None) -> int:
    """Resolve the live note id: explicit override, else uuid-regex with a unique hit.

    The re-TTSed side mp3 filenames embed the card uuid, which appears in the
    field's ``[sound:...]`` tag, so ``findNotes`` on ``Front:re:{uuid}`` /
    ``Back:re:{uuid}`` addresses exactly the card. Asserts a unique match.

    Args:
        url: AnkiConnect endpoint.
        uuid: Card uuid embedded in the ``[sound:]`` media filename.
        note_id: Optional caller override (used verbatim when given).

    Returns:
        The resolved note id.

    Raises:
        AssertionError: When the uuid-regex query does not match exactly one note.
    """
    if note_id is not None:
        return note_id
    query = f'"Front:re:{uuid}" OR "Back:re:{uuid}"'
    hits = ankiconnect_call(url, "findNotes", {"query": query})
    assert len(hits) == 1, (
        f"expected exactly one note matching uuid {uuid!r}, got {len(hits)}: {hits}"
    )
    return int(hits[0])


def _existing_feedback(url: str, note_id: int) -> str:
    """Confirm the note via ``notesInfo`` and return its preserved Feedback value.

    Feedback (ord 2) must be present in the ``updateNoteFields`` payload or
    AnkiConnect rejects the whole-field overwrite; it is preserved verbatim,
    never regenerated.
    """
    info = ankiconnect_call(url, "notesInfo", {"notes": [note_id]})
    assert len(info) == 1, f"notesInfo returned {len(info)} entries for note {note_id}"
    fields = info[0]["fields"]
    assert "Feedback" in fields, (
        f"note {note_id} has no Feedback field; replace_card targets Basic+Feedback notes"
    )
    return fields["Feedback"]["value"]


def _store_media(url: str, mp3: Path) -> None:
    """Overwrite the collection media entry under the mp3's (uuid-stable) basename."""
    assert mp3.exists(), f"side mp3 missing: {mp3}"
    ankiconnect_call(
        url,
        "storeMediaFile",
        {
            "filename": mp3.name,
            "data": base64.b64encode(mp3.read_bytes()).decode("ascii"),
        },
    )


def _content_text(raw: str) -> str:
    """Sanitize a parsed block side into a valid ``CardContent`` text (1-500 chars).

    The reconstructed card is only a scaffold for ``model_copy`` (its front/back
    are immediately overwritten with the new text), so this just needs to yield a
    non-empty, in-bounds string: drop audio/image markdown lines, strip any
    leading citation prefix, collapse blank lines, and truncate.
    """
    kept = [
        line
        for line in raw.splitlines()
        if line.strip() and not _MEDIA_LINE_RE.match(line)
    ]
    text = re.sub(r"^@\S+:\s*", "", " ".join(kept)).strip()
    return (text or "placeholder")[:500]


def _split_blocks(text: str) -> tuple[str, list[str]]:
    """Split card markdown into a (prefix, blocks) pair that re-concatenates exactly.

    Each block is the exact substring from one ``## `` heading up to the next, so
    ``prefix + "".join(blocks) == text``. Block N's trailing blank lines belong to
    block N, so replacing one block preserves inter-card spacing.
    """
    idxs = [m.start() for m in re.finditer(r"(?m)^## ", text)]
    if not idxs:
        return text, []
    prefix = text[: idxs[0]]
    bounds = idxs + [len(text)]
    blocks = [text[bounds[k] : bounds[k + 1]] for k in range(len(idxs))]
    return prefix, blocks


def _locate_block(blocks: list[str], uuid: str) -> int:
    """Return the ordinal of the unique block whose text embeds ``uuid``."""
    hits = [k for k, b in enumerate(blocks) if uuid in b]
    assert len(hits) == 1, (
        f"expected exactly one markdown block embedding uuid {uuid!r}, got {len(hits)}"
    )
    return hits[0]


def _rebuild_card(block: str, uuid: str) -> PlainCard:
    """Reconstruct a :class:`PlainCard` (uuid + tags + audio uris) from a md block."""
    parsed = extract_cards(block.splitlines())
    assert len(parsed) == 1, f"block did not parse to exactly one card: {parsed!r}"
    card = parsed[0]
    assert card["tags"], f"card block for uuid {uuid!r} has no tags to preserve"
    front_uri_m = _AUDIO_FRONT_RE.search(block)
    back_uri_m = _AUDIO_BACK_RE.search(block)
    return PlainCard(
        front=CardContent(text=_content_text(card["front"])),
        back=CardContent(text=_content_text(card["back"])),
        tags=card["tags"],
        card_id=uuid,
        audio_front_uri=front_uri_m.group(1) if front_uri_m else None,
        audio_back_uri=back_uri_m.group(1) if back_uri_m else None,
    )


def _update_markdown(
    output_dir: Path,
    uuid: str,
    new_front_text: str,
    new_back_text: str,
    citation_key: str,
    tag_format: str,
) -> None:
    """Patch the target card block in cards-with-audio.md and cards-plain.md.

    Locates the card by uuid in cards-with-audio.md (the uuid is embedded in its
    ``[audio-*]`` uri), ``model_copy``s a reconstructed card with the new front /
    back text (uuid + tags + audio uris preserved), and splices the re-rendered
    block into BOTH files at the same ordinal (both files are written from the
    identical ordered gated list, so ordinals align). No-op when the audio md is
    absent (text-only / audio-less deck).
    """
    audio_path = output_dir / "cards-with-audio.md"
    plain_path = output_dir / "cards-plain.md"
    if not audio_path.exists():
        logger.warning(
            "cards-with-audio.md absent under %s; skipping on-disk md patch", output_dir
        )
        return

    audio_prefix, audio_blocks = _split_blocks(audio_path.read_text())
    ordinal = _locate_block(audio_blocks, uuid)
    base = _rebuild_card(audio_blocks[ordinal], uuid)
    new_card = base.model_copy(
        update={
            "front": CardContent(text=new_front_text),
            "back": CardContent(text=new_back_text),
        }
    )

    audio_blocks[ordinal] = new_card.to_md(
        include_audio=True, citation_key=citation_key, tag_format=tag_format
    )
    audio_path.write_text(audio_prefix + "".join(audio_blocks))

    assert plain_path.exists(), f"cards-plain.md missing: {plain_path}"
    plain_prefix, plain_blocks = _split_blocks(plain_path.read_text())
    assert len(plain_blocks) == len(audio_blocks), (
        "cards-plain.md and cards-with-audio.md block counts diverge "
        f"({len(plain_blocks)} vs {len(audio_blocks)}); cannot align by ordinal"
    )
    plain_blocks[ordinal] = new_card.to_md(
        include_audio=False, citation_key=citation_key, tag_format=tag_format
    )
    plain_path.write_text(plain_prefix + "".join(plain_blocks))


def _replace_text_only(
    *,
    url: str,
    note_id: int,
    citation_key: str,
    new_front_text: str,
    new_back_text: str,
    sync_after: bool,
) -> CardReplaceResult:
    """Manifest-absent degrade: rebuild text-only fields and patch the note in place."""
    front_field = prepare_for_anki(_prefixed_front(citation_key, new_front_text))
    back_field = prepare_for_anki(new_back_text)
    feedback = _existing_feedback(url, note_id)
    ankiconnect_call(
        url,
        "updateNoteFields",
        {
            "note": {
                "id": note_id,
                "fields": {
                    "Front": front_field,
                    "Back": back_field,
                    "Feedback": feedback,
                },
            }
        },
    )
    if sync_after:
        ankiconnect_call(url, "sync")
    return CardReplaceResult(
        note_id=note_id,
        front_file=None,
        back_file=None,
        synced=sync_after,
        degraded=True,
    )


def replace_card(
    card_manifest_path: Path,
    *,
    new_front_text: str,
    new_back_text: str,
    citation_key: str,
    tts_kwargs: dict,
    ankiconnect_url: str,
    note_id: int | None = None,
    output_dir: Path | None = None,
    tag_format: str = "slugified",
    sync_after: bool = True,
) -> CardReplaceResult:
    """Replace one card wholesale in the live headless Anki collection.

    Regenerates BOTH audio sides in place (whole-side re-TTS honoring the new
    text, citation re-prepended front-only), rebuilds the Front / Back fields
    independently, patches the located note via ``updateNoteFields`` +
    ``storeMediaFile`` (Feedback preserved), patches the on-disk md files, and
    issues one AnkiWeb ``sync``. The note keeps its id / GUID / scheduling.

    Args:
        card_manifest_path: Path to ``card_chunks/{uuid}_manifest.json``. When it
            does NOT exist, degrades to a text-only field update (``note_id`` req).
        new_front_text: New front prose (WITHOUT the ``@citation:`` prefix).
        new_back_text: New back prose (no citation prefix).
        citation_key: Citation key prepended to the front field.
        tts_kwargs: Provider config forwarded to the whole-side re-TTS.
        ankiconnect_url: AnkiConnect HTTP endpoint.
        note_id: Optional numeric note-id override (required in the text-only path).
        output_dir: Pipeline output dir holding the md files (defaults to the
            manifest's ``audio_dir.parent``).
        tag_format: Tag format for the re-rendered md blocks.
        sync_after: Issue a final AnkiWeb ``sync`` when true.

    Returns:
        A :class:`CardReplaceResult`.

    Raises:
        AssertionError: On a missing back side, a non-unique note match, a missing
            Feedback field, or a manifest-absent call without ``note_id``.
    """
    if not card_manifest_path.exists():
        assert note_id is not None, (
            f"manifest absent ({card_manifest_path}); text-only degrade requires note_id"
        )
        return _replace_text_only(
            url=ankiconnect_url,
            note_id=note_id,
            citation_key=citation_key,
            new_front_text=new_front_text,
            new_back_text=new_back_text,
            sync_after=sync_after,
        )

    manifest = json.loads(card_manifest_path.read_text())
    uuid = manifest["card_id"]
    assert manifest.get("back_file"), (
        "card has no back side (back_file is null); replace_card needs both sides"
    )
    audio_dir = card_manifest_path.parent.parent
    output_dir = output_dir or audio_dir.parent
    front_mp3 = audio_dir / manifest["front_file"]
    back_mp3 = audio_dir / manifest["back_file"]
    assert front_mp3.exists(), f"front mp3 missing: {front_mp3}"
    assert back_mp3.exists(), f"back mp3 missing: {back_mp3}"

    speed = _resolve_speed(manifest)
    front_written = _whole_side_retts(
        card_manifest_path=card_manifest_path,
        side="front",
        manifest=manifest,
        side_chunks=manifest["sides"].get("front", {}).get("chunks", []),
        new_text=new_front_text,
        speed=speed,
        tts_kwargs=tts_kwargs,
    )
    back_written = _whole_side_retts(
        card_manifest_path=card_manifest_path,
        side="back",
        manifest=manifest,
        side_chunks=manifest["sides"].get("back", {}).get("chunks", []),
        new_text=new_back_text,
        speed=speed,
        tts_kwargs=tts_kwargs,
    )

    front_field = prepare_for_anki(
        f"{_prefixed_front(citation_key, new_front_text)}\n\n"
        f"[audio-front]({front_written.name})"
    )
    back_field = prepare_for_anki(
        f"{new_back_text}\n\n[audio-back]({back_written.name})"
    )

    nid = _resolve_note_id(ankiconnect_url, uuid, note_id)
    feedback = _existing_feedback(ankiconnect_url, nid)
    ankiconnect_call(
        ankiconnect_url,
        "updateNoteFields",
        {
            "note": {
                "id": nid,
                "fields": {
                    "Front": front_field,
                    "Back": back_field,
                    "Feedback": feedback,
                },
            }
        },
    )
    _store_media(ankiconnect_url, front_written)
    _store_media(ankiconnect_url, back_written)

    _update_markdown(
        output_dir, uuid, new_front_text, new_back_text, citation_key, tag_format
    )

    if sync_after:
        ankiconnect_call(ankiconnect_url, "sync")

    return CardReplaceResult(
        note_id=nid,
        front_file=front_written,
        back_file=back_written,
        synced=sync_after,
        degraded=False,
    )
