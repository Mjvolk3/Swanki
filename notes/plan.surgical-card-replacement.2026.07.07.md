---
id: osnm53yefk44wa2n2rv2ye5
title: 'Surgical single-card replacement + gate propagation fix'
desc: ''
updated: 1783473071229
created: 1783473071229
---

## Context

Two coupled problems. First, a **capability gap**: swanki can surgically edit one
chunk of one card side (`edit_card_chunk`, PR46, stable since 2026-06-16) but has
no first-class way to replace an ENTIRE card one-for-one — new front text, new back
text, both audio sides regenerated, patched in place in the live headless Anki
collection with GUID and scheduling preserved. Today that requires a full paper
regen (expensive, re-mints card GUIDs, orphans scheduling) or hand-editing the
collection. We want a `replace_card` orchestrator that mirrors the STABLE
`card_edit` trio and swaps a card wholesale without a reimport.

Second, a **latent correctness-gate wiring bug** that motivates the first real use.
`generate_outputs` (`pipeline.py:1968`) applies `_apply_correctness_gate` to a LOCAL
`cards` variable, correctly writes the gated list to `cards-plain.md` and the first
`.apkg`, but **returns only a `paths` dict** (`pipeline.py:2089`). All three call
sites (`533` full, `337` solution_manual, `359` glossary) keep their pre-gate
`all_cards` and pass it onward — so `generate_audio` (`cards-with-audio.md`, line
`2450`), the stage-9b apkg re-export, and `send_to_anki` all ship the UNcorrected
cards. Cards the gate dropped or that were meant to be corrected still reach Anki.
This shipped 5 wrong alcamo cards (CH01, CH03, CH04 x2, CH05). The fix makes the
gate's kept list the single source of truth; `replace_card` then cleans up the 5
already-live cards without a full regen.

Scope boundary: `replace_card` is a **live-collection patch only** — `updateNoteFields`
+ `storeMediaFile` + one AnkiWeb `sync`. It deliberately does NOT re-export a full
`.apkg` to Zotero; that GUID-divergence boundary stays paused (see
`project_card_unify_regen`). No ABS step: per-card complementary audio ships inside
the apkg `[sound:]`, not an ABS projection.

## Relevant Files

| Path | Action | Purpose | Stance |
| --- | --- | --- | --- |
| `swanki/audio/card_replace.py` | NEW | Thin orchestrator: locate live note, regen both sides, rebuild fields, patch collection, update md files | n-a |
| `scripts/swanki_replace_card.py` | NEW | SLURM CLI; mirrors `swanki_card_edit.py` (Fish ref setup, `build_fish_tts_kwargs`, `swap_anki_media`) | n-a |
| `scripts/swanki_replace_card.sbatch` | NEW | In-job Fish bring-up; mirrors `swanki_card_edit.sbatch` | n-a |
| `tests/test_audio_card_replace.py` | NEW | Unit tests mirroring `test_audio_card_edit.py` (patch TTS/combine) | n-a |
| `notes/swanki.audio.card_replace.md` | NEW | Paired dendron note for the orchestrator | n-a |
| `notes/scripts.swanki_replace_card.md` | NEW | Paired dendron note for the CLI | n-a |
| `swanki/pipeline/pipeline.py` | MODIFY | `generate_outputs` returns the kept list; reassign `all_cards` at `337`/`359`/`533` | in-flux |
| `swanki/audio/card_edit.py` | REFERENCE | Reuse `_whole_side_retts` (111-173) via `edit_card_chunk` whole-side fallback (176) with explicit `new_text` | stable |
| `swanki/audio/card.py` | REFERENCE | Manifest + filename shape: `{key}_{uuid}_{side}.mp3`, `card_chunks/{uuid}_manifest.json` (367-591) | stable |
| `swanki/audio/comment_edit.py` | REFERENCE | `edit_chunk`, `_SPEED_BY_AUDIO_TYPE` (card=1.6) | stable |
| `swanki/audio/_common.py` | REFERENCE | `text_to_speech`, `chunk_text`, `append_chunk_pause`, `combine_audio`, `ensure_fish_speech_reference` | stable |
| `swanki/processing/anki_processor.py` | REFERENCE | Import `prepare_for_anki` (540); `process_content` (470) — both pure, do NOT modify | stable-but-note-stale |
| `swanki/delivery/targets/anki.py` | REFERENCE | `ankiconnect_call` (57, fail-fast), `default_ankiconnect_url` (109) | stable |
| `scripts/swanki_audio_edit.py` | REFERENCE | `build_fish_tts_kwargs` source pattern | stable |
| `swanki/models/cards.py` | REFERENCE | `to_md` citation prefix (1072-1083); `model_copy` preserves `card_id` | in-flux |

## Key Design Decisions

1. **Fix the gate bug by RETURNING the kept list, not by hoisting a second gate
   call.** `generate_outputs` already runs `_apply_correctness_gate` internally at
   the correct point (before any markdown/apkg is written). Make it `return outputs,
   cards` (or attach the kept list to the returned structure) and reassign
   `all_cards = ...` at all three call sites. Rejected: calling the gate a second
   time in `run()` before `generate_audio`. The gate is **non-idempotent** — it
   fires parallel LLM calls (cost), and it clobbers `correctness-assessment.json`.
   A second call would double-charge and could yield a different filtered set,
   diverging `cards-plain.md` from `cards-with-audio.md`. Running it exactly once
   and threading its output is the only consistent fix.

2. **`replace_card` is a live-collection patch, never `importPackage`.** Anki GUID
   is `sha256(Front, Back, Feedback)`. `updateNoteFields` freezes the OLD note's
   GUID onto NEW content; the note keeps its `id`/GUID/scheduling. If we instead
   rebuilt an apkg and `importPackage`d it, the recomputed GUID would differ from
   the frozen one and Anki would treat the corrected card as a NEW note — orphaning
   review history as a duplicate. So the replace path is strictly `updateNoteFields`
   + `storeMediaFile` (x2) + one `sync`, and it does NOT re-export/re-sync a full
   apkg to Zotero (that is the deliberately-paused unify-regen boundary). It DOES
   patch `cards-with-audio.md` / `cards-plain.md` on disk via `model_copy` (safe:
   uuid preserved, no GUID recompute happens from a markdown edit alone).

3. **Reuse the whole-side re-TTS path once per side; do not add a both-sides
   helper.** `edit_card_chunk(..., new_text=...)` already falls back to
   `_whole_side_retts` when a side has no editable tts chunks, and `_whole_side_retts`
   honors an explicit `new_text` that overrides the recovered transcript. Call it
   twice (front, then back) with the new text for each side. Rejected: writing a new
   `regen_both_sides` helper — it would duplicate the STABLE PR46 chunk/pause/preprocess/
   citation-prepend/`combine_audio(crossfade_ms=0)` assembly. Back `.chunks` can be
   empty; always pass `new_text` so the fallback never tries to recover a transcript.
   This absorbs the retired `regen_card_audio_side.py` stopgap — do not resurrect it.

4. **Rebuild Front and Back fields INDEPENDENTLY via imported `prepare_for_anki`.**
   `prepare_for_anki` extracts `[audio-front]`/`[audio-back]` markdown links, runs
   `process_content`, then appends `[sound:basename]` at the end. If handed one
   combined card string it would append BOTH sound tags to a single field. So build
   the front md (carrying `[audio-front](...)` + the `@citation:` prefix) and the
   back md (carrying `[audio-back](...)`, NO citation prefix) separately, call
   `prepare_for_anki` on each, and map to the note's Front / Back fields. Note:
   `process_content` leaves newlines literal (no `<br>` conversion) and passes
   remote `<img src>` through verbatim — do NOT reimplement md->html; just import the
   pure function.

5. **Locate the live note by uuid-regex, assert exactly one match.** The mp3
   filenames embed the card uuid (`{key}_{uuid}_front.mp3`), which appears inside
   the field's `[sound:...]` tag. Query `findNotes` with `Front:re:{uuid}` /
   `Back:re:{uuid}`, assert the hit count is exactly 1 (fail on 0 or >1), confirm via
   `notesInfo`. Rejected as the only path: requiring the caller to pass a numeric
   note-id — brittle and unknowable from the manifest alone. But we DO accept an
   optional `--note-id` override for the text-only degrade case, where no `[sound:]`
   uuid exists in the field to match on.

6. **`storeMediaFile` under the byte-stable uuid filename; never mint a new uuid.**
   Filenames embed the uuid, not the text, so re-TTS overwrites `{key}_{uuid}_side.mp3`
   in place and `storeMediaFile` overwrites the collection media entry under the same
   basename — the `[sound:]` tag in the field stays valid without a rename. Minting a
   new uuid for a replacement would strand the old media and force a field rewrite for
   no benefit.

7. **Reuse `ankiconnect_call` (fail-fast), not the `AnkiProcessor` try/except
   wrappers.** `delivery/targets/anki.ankiconnect_call` raises on any error (per repo
   fail-fast rule). The `AnkiProcessor` methods wrap AnkiConnect in try/except; we do
   not touch or call those. Feedback field (ord 2) MUST be present in the Basic note's
   fields dict passed to `updateNoteFields` or AnkiConnect rejects — preserve the
   existing Feedback verbatim (do not regenerate it).

8. **Branch on manifest existence.** Manifest present (`card_chunks/{uuid}_manifest.json`):
   full audio + field regen. Manifest absent: text-only field update, and require
   `--note-id` (no uuid `[sound:]` to match). This keeps the tool usable for
   audio-less cards without special-casing inside the audio path.

## Approach

`card_replace.py` is a **thin orchestrator over stable parts**. The public entry —
`replace_card(card_manifest_path, *, new_front_text, new_back_text, note_id=None,
citation_key, tts_kwargs, ankiconnect_url, ...)` — executes in this order:

1. **Load + validate.** Parse the nested manifest; derive `audio_dir =
   manifest.parent.parent`, uuid = `manifest["card_id"]`. Assert the front/back mp3
   paths resolve. `ensure_fish_speech_reference` + a Fish health-gate before any TTS.
2. **Regen both sides.** Call the `card_edit` whole-side re-TTS path once per side
   with explicit `new_text` (front = `new_front_text`, back = `new_back_text`). Front
   re-prepends the citation audio; back does not. Both use `combine_audio(crossfade_ms=0)`
   and speed 1.6. Side mp3s are overwritten in place under their uuid filenames.
3. **Rebuild fields.** Construct front md (`@{citation_key}: {new_front_text}` +
   `[audio-front]({front_mp3})`) and back md (`{new_back_text}` +
   `[audio-back]({back_mp3})`) independently; run each through the imported
   `prepare_for_anki`. Preserve the existing Feedback field from `notesInfo`.
4. **Locate the note.** If `note_id` was passed, use it; else `findNotes` on
   `Front:re:{uuid} OR Back:re:{uuid}`, assert exactly one, confirm via `notesInfo`.
5. **Patch collection.** `updateNoteFields` with the full `{Front, Back, Feedback}`
   dict (whole-field overwrite). Then `storeMediaFile` each mp3 under its uuid
   basename (read bytes, base64).
6. **Update on-disk md.** Load the card from `cards-plain.md`/`cards-with-audio.md`
   by uuid, `model_copy` with new front/back text (uuid preserved), rewrite both
   files. This keeps the markdown source of truth consistent with the live note.
7. **One AnkiWeb `sync`.**

Text-only degrade (no manifest): skip steps 1-2 and the audio parts of 3/5; require
`note_id`; `updateNoteFields` with rebuilt text-only fields; one `sync`.

`swanki_replace_card.py` mirrors `swanki_card_edit.py`: arg parsing, `build_fish_tts_kwargs`,
`ensure_fish_speech_reference`, `swap_anki_media` helper, then calls `replace_card`.
`swanki_replace_card.sbatch` mirrors `swanki_card_edit.sbatch`: brings up in-job Fish
on the single allocated GPU (`apptainer --nv`), `COMPILE=0` (short edit, compile cost
not amortized), teardown via a bash `trap` (not the SLURM epilog).

**Out of scope:** retuning the correctness gate (factual-only high-acceptance is a
documented rule — the bug is wiring, not judgment); full-apkg re-export or Zotero
re-sync; ABS refresh; any new TTS engine; minting new card ids; touching the
`AnkiProcessor` try/except wrappers or `process_content`/`prepare_for_anki` internals.

## Gotchas

1. **GUID content-hash divergence** — full-apkg re-export recomputes
   `sha256(Front,Back,Feedback)` and `importPackage` orphans scheduling; sidestep +
   rationale in Decision 2.
2. **`updateNoteFields` overwrites the whole field.** Partial edits are impossible;
   rebuild the complete field HTML including the `[sound:]`/`<img>` tags via
   `prepare_for_anki`. Sidestep: always construct the full field string.
3. **`prepare_for_anki` appends BOTH sound tags to one string** — build Front and Back
   md separately, one `[audio-*]` link each (Decision 4).
4. **`process_content` leaves newlines literal** (no `<br>`) — reuse the pure function
   unchanged, do not reimplement md->html (Decision 4).
5. **Empty back `.chunks`** — always pass `new_text` so the whole-side fallback re-TTS
   without needing transcript recovery (Decision 3).
6. **Citation prefix + audio prepend are front-only; `crossfade_ms=0`** — branch on
   side in both field build and the re-TTS call (Decision 4, Approach step 2).
7. **Note-match ambiguity** — uuid-regex must assert exactly 1 hit (0 or >1 hard-fail);
   confirm via `notesInfo`, allow `--note-id` override (Decision 5).
8. **Byte-stable filenames only** — never mint a new uuid; overwrite
   `{key}_{uuid}_side.mp3` so `storeMediaFile` and the `[sound:]` tag stay valid
   (Decision 6).
9. **Fish readiness.** `ensure_fish_speech_reference` + health-gate before TTS;
   `COMPILE=0` for short edits.
10. **SLURM epilog reaps GPU procs on job end.** In-job Fish sidesteps cross-job kills;
    tear Fish down via a bash `trap` in the sbatch, not the epilog.
11. **Manifest-absent path** — requires `--note-id`, text-only field update (Decision 8).
12. **Feedback field (ord 2) required** in the `updateNoteFields` fields dict or
    AnkiConnect rejects; preserve the existing value, do not regenerate it (Decision 7).
13. **Issue `#22`: remote `<img>` URLs pass through `process_content` verbatim.** A
    replaced field can inherit an unbundled remote Mathpix image reference; note the
    risk, do not solve it here.
14. **Unpinned deps** (pydantic>=2, pydantic-ai>=0.1, requests unpinned,
    requires-python>=3.13). Verify against installed versions rather than trusting
    floors when running tests locally.

## Verification

- **Unit tests (`tests/test_audio_card_replace.py`, NEW):** mirror
  `tests/test_audio_card_edit.py` — patch `text_to_speech` and `combine_audio` so NO
  Fish/TTS runs in tests. Cover: (a) both-sides regen calls the whole-side re-TTS
  path with explicit `new_text` per side; (b) Front field carries `@citation:` prefix
  + one `[sound:front]`, Back field has no prefix + one `[sound:back]`; (c)
  uuid-regex note-match asserts exactly one, raises on 0/>1; (d) `updateNoteFields`
  fields dict includes Feedback (preserved); (e) manifest-absent degrades to text-only
  and requires `note_id`; (f) `cards-plain.md`/`cards-with-audio.md` updated via
  `model_copy` with uuid preserved.
- **Gate regression (`tests/test_card_correctness.py`, extend):** assert that after
  `generate_outputs`, the reassigned `all_cards` equals the gated kept list, and that
  `cards-with-audio.md` + the note pushed to Anki reflect the gated list (not the
  pre-gate `all_cards`). Assert the gate runs exactly once (no second invocation).
- **Commands:**
  - `~/opt/miniconda3/envs/swanki/bin/Swanki python -m pytest tests/test_audio_card_replace.py tests/test_card_correctness.py -q`
  - `mypy` on changed files: `swanki/audio/card_replace.py swanki/pipeline/pipeline.py scripts/swanki_replace_card.py`
  - `ruff check` on the same changed files.
- **Manual smoke:** the FIRST real run is the 5 mis-shipped alcamo cards (CH01, CH03,
  CH04 x2, CH05). Before running, verify each of the 5 has a comp-audio manifest
  (`card_chunks/{uuid}_manifest.json` present -> audio+field path) vs text-only
  (`--note-id` required). Run one card end-to-end via `swanki_replace_card.sbatch`
  against SLURM in-job Fish, confirm the note updates in place (same id/GUID/scheduling),
  media overwrites under the uuid filename, and one AnkiWeb sync lands.

## Open Questions

1. **Text-only match** — defaulting to requiring `--note-id` when no manifest exists,
   unless told otherwise.
2. **Feedback field** — defaulting to preserving the existing Feedback on replace (not
   regenerating), unless told otherwise.
3. **Zotero backup apkg** — defaulting to leaving `replace_card` live-only and letting
   the Zotero backup apkg lag until a separate deliberate re-export, unless told otherwise.
4. **ABS** — defaulting to no ABS step (comp audio ships inside the apkg `[sound:]`,
   not an ABS projection), unless told otherwise.
5. **Alcamo pre-flight** — defaulting to verifying each of the 5 cards' manifest/audio
   presence before the first run rather than assuming all 5 are audio-backed, unless
   told otherwise.
