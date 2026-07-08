---
id: b6rige2nzfcmz777j7m15wh
title: Card_replace
desc: ''
updated: 1783475209000
created: 1783475209000
---

## 2026.07.07 - Surgical one-for-one card replacement (`replace_card`)

New orchestrator that swaps an ENTIRE card wholesale in the live headless Anki
collection, where [[swanki.audio.card_edit]] (`edit_card_chunk`) only rewrites one
chunk of one side. Public entry `replace_card(card_manifest_path, *, new_front_text,
new_back_text, citation_key, tts_kwargs, ankiconnect_url, note_id=None, output_dir=None,
tag_format, sync_after)`. Plan: [[plan.surgical-card-replacement.2026.07.07]].

`card_replace.py` is a THIN orchestrator over stable parts — it adds no new TTS,
field, or AnkiConnect primitives:

- **Both audio sides re-TTSed** by reusing `card_edit._whole_side_retts` once per
  side with explicit `new_text` (front = new front prose, back = new back prose).
  That is the SAME assembly as gen time: chunk → `append_chunk_pause` → preprocess →
  TTS, citation re-prepended front-only, `combine_audio(crossfade_ms=0)`, card speed
  (1.6 fallback). No both-sides helper was added (would duplicate the stable PR46
  assembly); the retired `regen_card_audio_side.py` stopgap is not resurrected.
- **Fields rebuilt INDEPENDENTLY** via the pure `anki_processor.prepare_for_anki`.
  Front md = `@{citation_key}: {new_front_text}` (double-prefix guarded like
  `cards.to_md`) + `[audio-front]({front_mp3.name})`; back md = `{new_back_text}` (no
  prefix) + `[audio-back]({back_mp3.name})`. Built separately so `prepare_for_anki`
  appends exactly ONE `[sound:]` tag per field (handed a combined string it would
  append both).
- **Note located by uuid-regex.** The mp3 basenames embed the card uuid, which lands
  in the field's `[sound:]` tag, so `findNotes` on `"Front:re:{uuid}" OR "Back:re:{uuid}"`
  addresses the card; asserts EXACTLY one hit (hard-fail on 0 / >1). A numeric
  `--note-id` override is accepted (required in the text-only degrade, where no
  `[sound:]` uuid exists to match).
- **Live patch, never `importPackage`.** Anki GUID = `sha256(Front, Back, Feedback)`.
  `updateNoteFields` freezes the OLD note's GUID onto the NEW content, so id / GUID /
  scheduling survive. Feedback (ord 2) is preserved verbatim from `notesInfo` (required
  in the fields dict or AnkiConnect rejects). Then `storeMediaFile` overwrites both mp3s
  under their uuid-stable basenames (no rename), and one AnkiWeb `sync`. It deliberately
  does NOT re-export a full apkg to Zotero (GUID-divergence boundary stays paused) and
  takes no ABS step (per-card audio ships inside the apkg `[sound:]`).
- **On-disk md kept consistent** via `_update_markdown`: locate the card in
  `cards-with-audio.md` by uuid (embedded in the `[audio-*]` uri), `model_copy` a
  reconstructed `PlainCard` with the new front/back text (uuid + tags + audio uris
  preserved), and splice the re-rendered block into BOTH `cards-with-audio.md` and
  `cards-plain.md` at the same ordinal (both files are written from the identical
  ordered gated list, so ordinals align). No-op when the audio md is absent.
- **Manifest-absent degrade** (`_replace_text_only`): requires `note_id`, skips audio
  regen + `storeMediaFile`, rebuilds text-only fields, `updateNoteFields`, one `sync`.

Uses the fail-fast `delivery.targets.anki.ankiconnect_call` (raises on any error) for
every collection mutation — never the `AnkiProcessor` try/except wrappers.

Tests (`tests/test_audio_card_replace.py`, offline — `_whole_side_retts` and
`ankiconnect_call` patched): both-sides regen with explicit per-side `new_text`;
front @citation + one `[sound:front]`, back no prefix + one `[sound:back]`; uuid-regex
unique / 0 / >1; note-id override skips `findNotes`; Feedback preserved; text-only
degrade requires note_id; md files patched via `model_copy` with uuid preserved.

### Correctness-gate propagation fix (motivating context)

The first real use cleans up 5 mis-shipped alcamo cards (CH01, CH03, CH04 x2, CH05)
that reached Anki because `generate_outputs` applied the gate to a LOCAL `cards` var
but returned only the `paths` dict — the three call sites kept the pre-gate `all_cards`
and passed it to audio / apkg / `send_to_anki`. Fix: `generate_outputs` now returns
`(outputs, cards)` and every call site (solution_manual, glossary, full) reassigns
`all_cards` to the gated kept list. The gate still runs EXACTLY ONCE (it is
non-idempotent — parallel LLM calls, clobbers `correctness-assessment.json`), so
threading its output is the only consistent fix. See [[swanki.pipeline]].
