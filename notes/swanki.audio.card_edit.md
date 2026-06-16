---
id: 4b9pxgzm8qklwywyfahvqau
title: Card_edit
desc: ''
updated: 1781900000000
created: 1781900000000
---

## 2026.06.15 - Precise per-chunk card audio editing (`edit_card_chunk`)

New module unifying complementary CARD audio editing with the pure-audio
editor in [[swanki.audio.comment_edit]] (`edit_chunk`). Card audio uses a
NESTED per-card manifest (`card_chunks/{uuid}_manifest.json` with
`sides.front.chunks` / `sides.back.chunks`) that `edit_chunk` does not
understand. `edit_card_chunk(card_manifest_path, side, idx, *, comment |
new_text | speech_only, model, tts_kwargs)` is a thin ADAPTER that does NOT
touch `edit_chunk` (load-bearing for the audio-fix-from-annotations skill).
Plan: [[plan.precise-card-audio-editing.2026.06.15]].

Flow for a side with editable tts chunks:

- Read the nested manifest, assert `side in {front, back}`, reject `back` when
  `back_file` is null.
- Select `sides[side]["chunks"]`, EXCLUDE the citation chunk (index 0, read-
  only, never re-TTSed), re-index the remaining tts chunks to contiguous 0-based
  so the caller's `idx` addresses tts chunks only.
- Write a SYNTHETIC FLAT manifest to `card_chunks/_sideedit/{uuid}_{side}_
  manifest.json` shaped like a `write_chunk_manifest` output: top-level
  `audio_type` (`"card"`), `output_file` (`../{side_file}` so it resolves to the
  canonical side mp3 under `gen-md-complementary-audio/`), `bookend_start=None`,
  `bookend_end=None`, `postprocessor={}`, resolved `speed`, and a `chunks` list
  where each chunk carries the re-indexed `index`, `section=0`,
  `boundary="paragraph"`, original `text`, and `file` with a `../` prefix (the
  synthetic manifest sits one level below the real chunk mp3s in
  `card_chunks/`). `postprocessor={}` + every chunk in `section=0` reproduces
  the gen-time `combine_audio(crossfade_ms=0)` direct concat -- no inter-chunk
  silence.
- Call `edit_chunk(synthetic_path, idx, ...)` UNCHANGED: it re-TTSs the one real
  `card_chunks/*.mp3` in place, archives to `card_chunks/_sideedit/_edits/`,
  persists the shaped text into the SYNTHETIC manifest, and restitches the BODY
  (citation excluded) into the canonical side mp3.
- Re-prepend the citation (front only, when `citation_audio` is set):
  `combine_audio([citation, side_mp3], side_mp3, crossfade_ms=0)` -- the SAME
  combine as the original render.
- Propagate the edited chunk's shaped `text` BACK into the nested manifest's
  matching `sides[side]["chunks"]` entry (the nested manifest stays source of
  truth), append a card-tagged line (`card_id`, `side`, `original_index`,
  `reindexed_idx`, `action`) to `_sideedit/_edits/edits_log.jsonl`, and delete
  the synthetic manifest (the `_edits/` audit trail is kept).

**Speed.** Resolved from the nested manifest's `speed` field (added 2026.06.15,
see [[swanki.audio.card]]) else `_SPEED_BY_AUDIO_TYPE["card"]` (1.6) for legacy
manifests, and written into the synthetic manifest so `edit_chunk` reuses it.

**Whole-side re-TTS fallback.** When a side has NO editable tts chunks (a
direct-write / single-chunk side with no `card_chunks` entry, or a legacy
manifest), `edit_card_chunk` falls back to re-TTSing the ENTIRE side from its
transcript -- absorbing and retiring the `scripts/regen_card_audio_side.py`
stopgap. Transcript source order: nested-manifest chunk `text` joined back, else
the `complementary_transcripts/*_{side}.md` Generated-Transcript block; raises
`RuntimeError` if neither is recoverable (never silently TTS nothing). `new_text`
replaces the transcript wholesale. Citation re-prepended for front; `combine_
audio(crossfade_ms=0)` overwrites the side mp3.

Fail-fast, no try/except. SLURM harness + Anki swap live in
[[scripts.swanki_card_edit]]. Tests: `tests/test_audio_card_edit.py` (offline;
real `edit_chunk` runs with TTS/restitch/combine patched).
