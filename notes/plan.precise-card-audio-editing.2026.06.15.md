---
id: db37apsr5qnl9e8h3r25a3r
title: Precise card audio editing in swanki source
desc: ''
updated: 1781900000000
created: 1781900000000
---

## Goal and context

Build precise, per-chunk editing of **complementary card audio** into swanki SOURCE,
unified with the pure-audio editor in `swanki/audio/comment_edit.py` (`edit_chunk`).
`edit_chunk` understands only the flat chapter manifest
(`<type>_chunks/chunk_manifest.json`, `write_chunk_manifest`, `_common.py:1739`). Card
audio uses a DIFFERENT, nested manifest written by `generate_card_audio`
(`card.py:567-611`): `gen-md-complementary-audio/card_chunks/{uuid}_manifest.json` with
`sides.front.chunks` / `sides.back.chunks`. The only existing tool is the stopgap
`scripts/regen_card_audio_side.py`, which re-TTSs a WHOLE side from the saved transcript
(no per-chunk granularity, no `_edits/` audit, no agent rewrite).

This plan adds `swanki/audio/card_edit.py::edit_card_chunk`, a thin adapter that
translates the nested card manifest into a synthetic FLAT manifest and delegates to the
UNCHANGED `edit_chunk`, then re-prepends the citation and writes the side mp3 back. For
direct-write / single-chunk sides (typically backs) and legacy/missing manifests it falls
back to the stopgap's whole-side re-TTS. Adds a SLURM harness, a decoupled Anki media
swap, and tests in `tests/`.

**Retention is confirmed working** (verified against live `$SWANKI_DATA`). Chunked sides
ARE editable per-chunk on real cards today; see R1.

## Design decisions

1. **New module, do NOT touch `edit_chunk`.** `card_edit.py` exposes
   `edit_card_chunk(card_manifest_path, side, idx, *, comment=None, new_text=None,
   speech_only=False, model=None, tts_kwargs)`. The adapter owns all card-shape
   knowledge and calls `edit_chunk` exactly as the lecture/summary/reading paths do.
   Rationale: `edit_chunk` is load-bearing for the shipped `audio-fix-from-annotations`
   skill; widening its contract risks regressions for zero gain — the card shape is fully
   expressible as a synthetic flat manifest.

2. **Synthetic flat manifest, citation excluded.** `sides[side]["chunks"]` is a list where
   index 0 may be `{"type":"citation"}` (read-only, no `text`) followed by
   `{"type":"tts","text":...,"file":...}` entries. Chunk mp3 basenames are named
   `{citation_key}_{page_base}_{card_index}_{side}_chunk{i}.mp3` with `page_base=="card"`
   and a NUMERIC `card_index` (e.g. `..._card_7_front_chunk0.mp3`) — the uuid is NOT in the
   chunk filename; the basename lives in `chunk["file"]`, which the adapter reads, so this
   is fine. The adapter:
   - selects `sides[side]["chunks"]`, asserts the side exists;
   - EXCLUDES the citation chunk (never re-TTSed);
   - re-indexes the remaining `tts` chunks to contiguous 0-based `index` (so the caller's
     `idx` addresses tts chunks only, citation invisible);
   - writes a SYNTHETIC FLAT manifest to `card_chunks/_sideedit/{uuid}_{side}_manifest.json`
     shaped like a `write_chunk_manifest` output: top-level `audio_type` (the card
     manifest's `audio_type`, i.e. `"card"`), `output_file`, `bookend_start=None`,
     `bookend_end=None`, `postprocessor={}`, `speed` (resolved, decision 4), and a `chunks`
     list where each chunk carries `index` (re-indexed), `section=0`,
     `boundary="paragraph"`, original `text`, original `file`. Because the synthetic
     manifest sits under `card_chunks/_sideedit/` (one level below the real chunk mp3s in
     `card_chunks/`), `chunk["file"]` paths get a `../` prefix. `output_file` follows
     `edit_chunk`'s rule (`comment_edit.py:313`: `manifest_path.parent.parent /
     output_file`); `parent.parent` is `gen-md-complementary-audio/`, so `output_file` is
     just the side mp3 basename (e.g. `{citation_key}_{uuid}_front.mp3`).
   - `postprocessor={}` is correct: card chunks combine with `combine_audio(crossfade_ms=0)`
     (`card.py:531,565`) — direct concat, zero inter-chunk silence/gain. With every chunk
     in `section=0`, `restitch_from_chunks` inserts no pauses, reproducing that. See R4.

3. **`edit_chunk` does per-chunk work; the adapter restitches the BODY only.** The adapter
   calls `edit_chunk(synthetic_path, idx, comment=..., new_text=..., speech_only=...,
   tts_kwargs=..., model=...)` UNCHANGED. `edit_chunk` re-TTSs the one real
   `card_chunks/*.mp3` in place, archives to `card_chunks/_sideedit/_edits/`, persists
   shaped text into the SYNTHETIC manifest, and restitches the chunks into `output_file` —
   a BODY-ONLY mp3 (citation excluded). The adapter then:
   - re-prepends the real citation (front only, per `card.py:502`) when
     `card_manifest["citation_audio"]` is set: `combine_audio([citation_path, body_mp3],
     side_mp3, crossfade_ms=0)`, the SAME combine as the original render (`card.py:531`).
     `citation_audio` is stored as `../{name}` relative to `card_chunks/`; resolve there.
   - writes the result to the canonical side mp3
     (`gen-md-complementary-audio/{front_file|back_file}`);
   - propagates the edited chunk's shaped `text` from the synthetic manifest BACK into the
     nested card manifest's matching `sides[side]["chunks"]` entry (re-indexed -> original
     list position). The nested manifest stays source of truth; the synthetic one is
     scratch.
   - deletes the synthetic manifest on success; LEAVES `_sideedit/_edits/` (the audit
     trail).
   - appends a card-tagged line (card_id, side, original list index, re-indexed idx) to the
     `_sideedit/_edits/edits_log.jsonl` that `edit_chunk` created — `edit_chunk`'s own
     record only knows the re-indexed idx.

4. **Speed.** The card manifest has NO top-level `speed` field today (confirmed). Add one in
   `generate_card_audio` (record the gen-time `speed`, `card.py:376`). The adapter resolves
   synthetic-manifest `speed` = card manifest `speed` if present, else
   `_SPEED_BY_AUDIO_TYPE["card"]` (== 1.6, `comment_edit.py:171`), and writes it into the
   synthetic manifest so `edit_chunk` reuses it via its own resolution
   (`comment_edit.py:244-251`) with no `speed=` override.

5. **Whole-side fallback (absorb the stopgap).** A side has no editable tts chunks when:
   (a) it was a direct-write / single-chunk side (no-citation single-chunk front,
   `card.py:493-497`; single-chunk back, `card.py:538-542` — `needs_combination` False or
   `len(back_chunks)==1`, so no `card_chunks` entry); or (b)
   `card_chunks/{uuid}_manifest.json` is missing (legacy). Confirmed real: the live cell
   card's BACK side has no `card_chunks` entry. In these cases `edit_card_chunk` falls back
   to WHOLE-SIDE re-TTS — exactly `regen_card_audio_side.py`'s logic: load the side
   transcript, `chunk_text`, `append_chunk_pause` + `_preprocess_for_tts` per chunk, TTS at
   the resolved speed, re-prepend citation (front only) if present,
   `combine_audio(crossfade_ms=0)`, overwrite the side mp3. Transcript source order: the
   nested-manifest chunk `text` joined back; else `complementary_transcripts/*_{side}.md`
   parsed via the stopgap's `load_transcript` regex (Generated Transcript block). If NO
   transcript is recoverable, raise (`RuntimeError`) — never silently TTS nothing.
   `new_text`, if given, replaces the transcript wholesale here. After this lands, DELETE
   `scripts/regen_card_audio_side.py` + `.sbatch`.

6. **SLURM harness (thin).** `scripts/swanki_card_edit.sbatch` mirrors
   `swanki_audio_edit.sbatch`: one GPU, in-job Fish via apptainer, derive a free port,
   `export SWANKI_FISH_PORTS="$port"`, health-poll — reuse that sbatch's Fish bring-up block
   VERBATIM. It calls `scripts/swanki_card_edit.py`, which reuses `swanki_audio_edit.py`'s
   `build_fish_tts_kwargs` to assemble `tts_kwargs`, calls `ensure_fish_speech_reference`
   (`_common.py:1064`) to register the voice on the in-job server BEFORE editing, then
   invokes `edit_card_chunk`.

7. **Anki media swap (decoupled).** A discrete `swap_anki_media(side_mp3, sound_filename)`
   in `swanki_card_edit.py` does post-restitch delivery: AnkiConnect `storeMediaFile`
   (base64 of the rewritten side mp3, OVERWRITING the unchanged `[sound:...]` filename — the
   filename is stable, R6) then one `sync`. OUTSIDE `edit_card_chunk` so the editor stays
   pure and testable; the entry calls it only when `--anki` is passed.

8. **`_edits/` location.** `edit_chunk` writes archives + `edits_log.jsonl` under
   `synthetic_manifest_path.parent / "_edits"` == `card_chunks/_sideedit/_edits/`. That is
   the desired location; the adapter appends its card-tagged line there.

## Retention (R1 — confirmed working, NOT a bug)

Verified against live `$SWANKI_DATA`: `card_chunks/` IS retained, at
`gen-md-complementary-audio/card_chunks/` (NOT directly under the output dir). An earlier
manual check mis-pathed it (`<output_dir>/card_chunks`), which is the ONLY reason the
stopgap re-TTSed from transcript. There is no retention bug for chunked sides.

Confirmed on the real cell card (`ballHowLifeWorks2023_CH01_..._0`, uuid `9cff566f-...`):
its `card_chunks/9cff566f-..._manifest.json` exists; `sides.front.chunks` =
`[{index:0,type:citation}, {index:1,type:tts, file:"..._card_7_front_chunk0.mp3"}]`; the
tts chunk mp3 exists on disk. CHUNK-LEVEL front editing is therefore viable on the real
card with the existing manifest. The same card's BACK side has no `card_chunks` entry
(single chunk, no citation, written directly) — the decision-5 fallback covers it.

Action items (NOT a "fix"):
- Verification only: confirm `generate_card_audio` writes + retains
  `card_chunks/{uuid}_manifest.json` on a fresh `audio=complementary_summary` run.
- Guardrail: keep "never auto-prune `card_chunks/`". The only nearby `rmtree`/`unlink` are
  `manifest.py:223` (temp staging dir for the packaged zip — a `tempfile.mkdtemp` tree, NOT
  `card_chunks/`) and `mineru.py:104` (OCR raw dir). The historical post-combine
  `p.unlink()` is already gone, so no active delete exists. Note this in the
  `swanki.audio.card` dendron note. No retention work item.

## Implementation steps (ordered)

1. **`swanki/audio/card.py` `generate_card_audio`:** add top-level `"speed": speed` to both
   manifest dicts (`card.py:575-586`, `card.py:599-609`). Keep
   `combine_audio(crossfade_ms=0)` unchanged. (No retention change — retention works.)

2. **Create `swanki/audio/card_edit.py`** with the CLAUDE.md frontmatter docstring and
   `edit_card_chunk(...)`. Imports: `comment_edit.edit_chunk`,
   `comment_edit._SPEED_BY_AUDIO_TYPE`, `_common.combine_audio`,
   `_common.append_chunk_pause`, `_common.chunk_text`, `card._preprocess_for_tts`, plus a
   small local `_load_side_transcript`. Order: load card manifest; assert `side in
   {"front","back"}`; reject `side=="back"` when `back_file` is null; locate
   `sides[side]["chunks"]`; if no `tts` chunks or manifest missing -> whole-side fallback
   (decision 5); else build synthetic manifest (decision 2), resolve speed (decision 4),
   call `edit_chunk` (decision 3), re-prepend citation + write side mp3, propagate text back
   to nested manifest, append card-tagged audit line, delete synthetic manifest. Return a
   result object echoing `edit_chunk`'s `ChunkEditResult` plus `side` and original index.
   Fail-fast, no try/except.

3. **Create `scripts/swanki_card_edit.py`** — argparse entry mirroring
   `swanki_audio_edit.py`: `--card-manifest` (or `--output-dir --card-uuid`), `--side`,
   `--idx`, `--comment`/`--new-text`/`--speech-only`, `--voice`, `--model`, optional
   `--anki`. Reuse `build_fish_tts_kwargs`, resolve in-job Fish URL from
   `SWANKI_FISH_PORTS`, call `ensure_fish_speech_reference`, dispatch to `edit_card_chunk`,
   then optionally `swap_anki_media` (decision 7).

4. **Create `scripts/swanki_card_edit.sbatch`** — copy `swanki_audio_edit.sbatch`, rename
   job/env vars, reuse the Fish bring-up block verbatim, call `swanki_card_edit.py`.

5. **Create `tests/test_audio_card_edit.py`** (see Test plan).

6. **Delete** `scripts/regen_card_audio_side.py` + `scripts/regen_card_audio_side.sbatch`
   once steps 2-3 cover their behavior. Grep for references (queue scripts, notes) and
   repoint at `swanki_card_edit`.

7. **Dendron + weekly (CLAUDE.md commit trio):** append dated sections to
   `notes/swanki.audio.card.md` (speed field + retention guardrail), create
   `notes/swanki.audio.card_edit.md` and `notes/scripts.swanki_card_edit.md`, update the
   weekly note.

## Test plan

`tests/test_audio_card_edit.py` mirrors `tests/test_audio_comment_edit.py`: patch at the
boundary, never invoke ffmpeg/Fish/network. Patch `swanki.audio.card_edit.edit_chunk` (or
`text_to_speech`/`restitch_from_chunks` seen THROUGH `comment_edit` to exercise the real
`edit_chunk`), `swanki.audio.card_edit.combine_audio`, and for the agent path the
`with_safety_retry`/`chunk_edit_agent` indirection. A `_card_manifest(tmp, ...)` fixture
writes `card_chunks/{uuid}_manifest.json` (front: citation + 2 tts chunks; back: 2 tts
chunks) plus chunk mp3 stubs and the citation stub. Cases:

- **Side navigation:** `front` and `back` edit the right chunks; `back` with
  `back_file=None` raises.
- **Citation read-only + re-prepended:** citation never passed to TTS; front
  `combine_audio` called with citation path FIRST (`call_args[0][0][0] == citation_path`);
  back-side edit does NOT prepend citation.
- **Synthetic manifest shape:** `_sideedit/{uuid}_{side}_manifest.json` has top-level
  `chunks`, every chunk `section==0` / `boundary=="paragraph"`, `postprocessor=={}`,
  `output_file` the side mp3 basename (resolving to `gen-md-complementary-audio/<side>.mp3`),
  and re-index excludes citation (idx 0 -> first tts chunk).
- **Speed resolution:** manifest `speed=1.45` -> synthetic `1.45`; manifest without `speed`
  -> `1.6`.
- **Whole-side fallback:** manifest-less / single-chunk direct-write side triggers
  transcript re-TTS (`text_to_speech` called per `chunk_text` piece, citation re-prepended
  for front); RAISES when no transcript is recoverable.
- **Audit + write-back:** `_sideedit/_edits/edits_log.jsonl` contains a record tagged
  `card_id`/`side`/original-index; nested manifest's `sides[side]["chunks"][k]["text"]`
  updated for the edited chunk; synthetic manifest deleted on success.
- **Regression guard:** the existing `tests/test_audio_comment_edit.py` suite already covers
  the unchanged `edit_chunk`; add a comment pointing to it.

## Out of scope (explicit)

- `audio-fix-from-annotations` card-awareness: cards have no whole-side
  `chunk_timeline.json` (the side mp3 is citation + body), so ABS-bookmark-to-chunk mapping
  does not apply. Card edits are driven by `--idx`/`--comment` directly.
- Changing the card `[sound:...]` filename: the Anki swap OVERWRITES the existing media
  filename so the note reference is untouched (R6).

## Risks

- **R2 (transcript recoverability):** the whole-side fallback needs a side transcript. The
  nested-manifest chunk `text` is the primary source; `complementary_transcripts/*_{side}.md`
  is the backstop. Write a tiny per-side transcript sidecar at gen time only if the `.md`
  parse proves fragile.
- **R4 (citation->body seam):** the re-prepend MUST use `combine_audio(crossfade_ms=0)`,
  identical to the original render (`card.py:531`) — one combine call, no pause/gain step.
  The body restitch via `edit_chunk` uses `postprocessor={}` + single `section=0`, so it
  inserts no silence. The seam matches.
- **R5 (parallel-edit races):** `_sideedit/{uuid}_{side}_...` namespacing isolates concurrent
  edits of different cards/sides on the shared `card_chunks/` dir. The real chunk mp3 is
  per-card-unique already. Two edits to the SAME side are inherently serial.
- **R6 (filename stability for Anki swap):** the side mp3 basename
  (`{citation_key}_{uuid}_{side}.mp3`) is derived from stable inputs (`card.py:439-443`) and
  reused on edit, so `[sound:...]` never changes and `storeMediaFile` overwrites in place.
  Confirm the Anki media filename equals the side mp3 basename (it does).

## Verification

Per CLAUDE.md, on changed/new files: `ruff check` and `ruff format --check`, then `mypy`
(Google convention). Run new tests with the conda env's ffmpeg on PATH:

```bash
conda activate swanki
ruff check swanki/audio/card_edit.py swanki/audio/card.py scripts/swanki_card_edit.py
mypy swanki/audio/card_edit.py swanki/audio/card.py
pytest tests/test_audio_card_edit.py -q
pytest tests/test_audio_comment_edit.py tests/test_audio_card.py -q
```

The last line confirms the pure-audio path and card generation are unregressed. On
completion `scripts/regen_card_audio_side.py` + `.sbatch` are deleted, their behavior folded
into `edit_card_chunk`'s whole-side fallback.

## Cut for brevity

- Removed the lengthy R1 "Gap A / Gap B / git-log root-cause" diagnosis and the "always
  write the manifest / unify single-chunk writes" fix work item — both rested on a path
  error; retention is confirmed working, so the only surviving R1 actions are a one-line
  verification and the keep-the-guardrail note.
