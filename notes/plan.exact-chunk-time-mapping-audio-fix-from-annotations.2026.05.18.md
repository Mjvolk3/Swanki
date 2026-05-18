---
id: 9j5i30sc5dd7xeka3xwe91d
title: Exact Chunk-Time Mapping + Audio-Fix-from-Annotations
desc: ''
updated: 1779143667730
created: 1779143667730
---

## Context

We can re-TTS a single chunk surgically (`swanki/audio/surgical.py`), but we have no truthful way to answer "the listener flagged an issue at MM:SS in the ABS audio — which chunk is that?" Today the only way to map a timestamp to a chunk is to re-derive timing by independently summing predicted chunk lengths plus configured pauses. That re-derivation has been **proven wrong by ~5s on one lecture and ~11s on another**: chunk mp3 lengths are not the raw TTS output. `_load` (`swanki/audio/_common.py:1073`) applies a silence-aware tail trim whose cut point depends on `detect_silence` over the actual audio content. The trimmed length is therefore *unknowable without loading the file* — pure prediction is impossible. The only correct timeline is the one measured during the real assembly walk.

Two deliverables, one shared spine:

1. **Exact chunk↔time mapping** — refactor assembly so a single pure accumulator yields per-chunk offsets *as a byproduct of the same traversal that builds the audio* (exact by construction). `restitch_from_chunks` persists those measured offsets to a `chunk_timeline.json` sidecar. Query functions read the sidecar.
2. **`/audio-fix-from-annotations <citation_key>` skill** — orange Zotero highlights (and/or ABS bookmarks) → locate the offending chunk(s) via content-match and the timeline → exactly **one** human-review gate → surgical re-TTS → restitch → commit → sync to Zotero → ABS refresh, so BookPlayer reflects the fix.

This plan is built for autonomous execution (uber-implement): no approval gate between plan and code; the reducer-critic is the only gate. The skill's single human-review step is a *runtime* feature of the skill spec, not an implementation checkpoint.

## Relevant Files

- `swanki/audio/_common.py` MODIFY — `combine_audio_with_section_pauses` (`:1006`; inner `_load` `:1073` silence-aware trim, `_gap_ms_for` `:1125`, section grouping `:1134`, start/end bookends `:1115`/`:1160`, crossfade append `:1144`), `restitch_from_chunks` (`:1211`), `write_chunk_manifest` (`:1167`). Add: private `_accumulate_timeline`, frozen pydantic sidecar model, public `chunk_time_window` / `time_to_chunk` / `chunk_time_window_abs`.
- `swanki/audio/__init__.py` MODIFY — currently exports `restitch_from_chunks`, `regenerate_and_restitch`, the generators. Add the three query functions to imports + `__all__`.
- `swanki/audio/surgical.py` REFERENCE — `regenerate_and_restitch` (`:47`) re-TTS edited chunks then calls `restitch_from_chunks` (`:128`); `fish_speech_healthy` (`:24`) HTTP preflight. **No code change needed for sidecar persistence**: surgical restitches through `restitch_from_chunks`, so once that writes the sidecar, surgical inherits the rewrite for free. Only its test is extended.
- `scripts/abs_bookmarks.py` NEW — sibling of `scripts/zotero_annotations.py`: `load_dotenv(dotenv_path=...)`, pydantic record model, importable functions + thin `argparse` CLI. Calls ABS `/api/me`.
- `scripts/zotero_annotations.py` REFERENCE — `get_annotations` (`:54`), `COLOR_MAP` (`:33`, `orange = "#f19837"`), default color is currently `magenta`; the skill passes `orange`. Reuses `ZoteroConfig`/`connect`/`find_item_by_citation_key`/`get_pdf_attachments` imported from `scripts/zotero_paper_import.py`.
- `scripts/zotero_paper_import.py` REFERENCE — `ZoteroConfig`, `connect`, `find_item_by_citation_key`, `get_pdf_attachments`.
- `swanki/sync/zotero.py` REFERENCE — `sync_to_zotero` (`:145`; args `citation_key`, `output_dir`, `audio_prefix`, `content_key`), `_git_short_hash` (`:31`, embedded into uploaded note at `:182`), `_OUTPUT_TYPES` (`:23`), fox tag (Zotero unicode marker) idempotent add at `:247-251`.
- `scripts/abs_refresh.sh` REFERENCE — flock pattern: `exec 200>/tmp/abs-refresh.lock` then `flock -n 200` (`:21-26`); env `ABS_API_TOKEN_FILE` default `~/Documents/projects/infra/abs/.api-token`, `ABS_URL` default `https://abs.michaelvolk.dev`; library scan at `:62-64`.
- `.claude/skills/fetch-bookmarks/SKILL.md` REFERENCE ONLY — macOS-only BookPlayer SQLite path (`/Users/...`), absent on gilahyper. Left **untouched**; the new skill uses ABS `/api/me` instead.
- `.claude/skills/audio-fix-from-annotations/SKILL.md` NEW — frontmatter (`description`, `user_invocable: true`, `arguments`) + phased markdown body.
- `tests/test_audio_timeline.py` NEW — no-Fish synthetic-mp3 timeline tests (pattern from `tests/test_audio_common.py`).
- `tests/test_audio_surgical.py` MODIFY — extend the mocked-TTS test to assert the sidecar is rewritten after restitch.
- `notes/swanki.audio._common.md` MODIFY, `notes/swanki.audio.surgical.md` MODIFY, `notes/scripts.abs_bookmarks.md` NEW — dated decision sections per commit-trio.

## Key Design Decisions

- **One assembly code path, no exceptions.** `combine_audio_with_section_pauses` is the sole audio assembler (`restitch_from_chunks` already delegates to it). Re-deriving timing anywhere else is forbidden — that independent re-derivation is exactly the proven ~5s/~11s drift. Both deliverables route through one shared accumulator.
- **Measure-during-assembly, not predict.** Chunk durations come from real loaded-and-trimmed `AudioSegment` lengths. `_load`'s trim is content-dependent (`detect_silence`), so a chunk's contribution is only knowable after loading it. Pure offline prediction is impossible; state this explicitly in code/docstring/note so nobody "optimizes" it into a predictor later.
- **Refactor extracts a pure timeline walk; assembly consumes it.** Introduce `_accumulate_timeline(...)` that performs the *exact same* per-segment sequence the current loop performs (gain-match, `_load` trim, `_gap_ms_for` inter-chunk silence, `section_pause_ms` between sections, bookend pauses, crossfade) and returns both the assembled `AudioSegment` and the per-chunk offset/duration records. `combine_audio_with_section_pauses` walks that single result instead of re-implementing the loop. Exact by construction: the offsets describe the very bytes that were exported.
- **Byte-identical guarantee is non-negotiable.** The refactor must produce assembled-audio bytes *identical* to pre-refactor for identical inputs. Frozen constants stay frozen: `tail_buffer_ms=350` (`:1100`), `gain_match_target_dbfs=-25.0` (caller), `chunk_pause_ms_by_boundary` paragraph=1100/sentence=500, `section_pause_ms=2000`, `bookend_pause_ms=500`. Crossfade math via `AudioSegment.append(..., crossfade=)` must be preserved because crossfade *shortens* the timeline (overlap), so offsets must account for it — the shared walk inherits this automatically since it *is* the assembly.
- **Sidecar is the source of truth, written where surgical restitch runs.** `restitch_from_chunks` writes `chunk_timeline.json` next to `chunk_manifest.json` (same dir, `manifest_path.parent`). Measured offsets only. Frozen pydantic model (CLAUDE.md mandates pydantic for structure). Schema (frozen; minor additive fields OK):
  ```
  ChunkTimeline{ audio_type, total_duration_ms,
    bookend_start: Span|None, bookend_end: Span|None,
    sections: [ Section{ index, start_ms, end_ms, gap_before_ms } ],
    chunks: [ ChunkSpan{ index, section, file, offset_ms, duration_ms, end_ms } ] }
  Span{ offset_ms, duration_ms, end_ms }
  ```
- **Query API: three public functions, sidecar-backed.** `chunk_time_window(source, audio_type, chunk_index, *, absolute_offset_ms=0) -> tuple[int,int]` returns `(start_ms, end_ms)` for one chunk; `time_to_chunk(source, audio_type, position_ms, *, absolute_offset_ms=0) -> int` is the inverse (which chunk contains this position); `chunk_time_window_abs(source, audio_type, chunk_index, *, preceding_chapter_durations_ms) -> tuple[int,int]` shifts the window by preceding-chapter durations for the ABS chapter-stitched view. `source` accepts a chunks dir, a `chunk_manifest.json` path, or an `output_dir` — resolved to the sidecar. Each asserts `manifest["audio_type"] == audio_type` (mirrors `surgical.py:87-92`; chunk indices are audio-type-local). `absolute_offset_ms` is added by callers when the ABS item is one chapter inside a stitched book; `chunk_time_window_abs` is the structured form of that for multi-chapter books.
- **Sidecar-missing fallback recomputes via the same accumulator.** If the sidecar is absent (older renders), the query loads the manifest's chunk files and runs `_accumulate_timeline` (the *same* shared walk — never an independent re-derivation), writes the sidecar, then answers. This keeps "one code path" true even for legacy data.
- **ABS bookmark `time` → chapter granularity ONLY.** ABS bookmark timestamps locate the *chapter/file*, not the chunk (BookPlayer rounds, lags, and the listener bookmarks slightly after the issue). Use `time` + served filename to pick the file/audio_type; then locate the specific chunk by **content-matching the highlighted source phrase against `manifest.chunks[].text`**, and report the precise MM:SS from the sidecar. Never trust the raw bookmark second as a chunk boundary.
- **Live-dir resolution: served filename is ground truth.** The ABS-served filename (and the highlighted text) decides which `SWANKI_DATA` paper directory and which `_N` regeneration is authoritative: pick the **highest `_N`** dir whose `chunk_manifest.json` `output_file` + chunk-filename set matches the ABS-served filename. Cross-check `audio_type` from `manifest["audio_type"]` against the `-lecture-`/`-reading-`/`-summary-` infix in the served name; assert before any lookup. Pure-Zotero path (annotation, no bookmark — the primary path for papers): `citation_key` → `SWANKI_DATA` dir → content-match the highlight across each audio_type's chunk text; report which audio_type/chunk matched.
- **Annotation classification heuristic, human is arbiter.** If the highlighted source phrase is present in some chunk's text → treat as text+speech fix (edit chunk text + re-TTS). If the annotation describes a delivery/artifact problem with no source-text change → speech-only fix (`chunk_edits[idx] = None`, re-render same text; already supported by `regenerate_and_restitch`). Both classifications are *surfaced in the single review diff*; the human confirms or overrides. Many-to-one / one-to-many annotations collapse into **one** consolidated `chunk_edits` map → one review → one restitch → one publish.
- **Auto-publish after the one approval.** Stopping at restitch leaves BookPlayer stale (previously flagged as a mistake). After the single human approval the skill runs the full chain unattended: `regenerate_and_restitch` → `git commit` → rebase-onto-main if needed → `sync_to_zotero` (re-embeds `_git_short_hash`) → poll the abs-refresh flock → `scripts/abs_refresh.sh`. Short surgical re-TTS is *exempt* from the "let user run long pipelines in terminal" rule (it's seconds, not a full pipeline); a full pipeline regeneration would not be.
- **Provenance order is load-bearing.** finalize → `git commit` → rebase-if-needed → `sync_to_zotero` (embeds the *post-rebase* short hash into the uploaded note) → poll `/tmp/abs-refresh.lock` → `abs_refresh.sh`. If a rebase happens *after* sync, re-sync so the embedded hash is truthful. The fox tag (Zotero unicode marker) add is already idempotent (`zotero.py:247-251`), no special handling.
- **Reference voice from manifest/config, never hardcoded.** Surgical re-TTS must reuse the exact reference voice the original render used (read from manifest/config; e.g. the Hamming `hamming-20260428T1135-science-vs-engineering` reference), passed through `tts_kwargs`. Books speak first-person (narrator owns the material); papers third-person seminar — preserved by reusing original render settings, not re-deciding.
- **ABS access is `/api/me` only.** `scripts/abs_bookmarks.py` hits `https://abs.michaelvolk.dev/api/me` (token file `~/Documents/projects/infra/abs/.api-token`), returning typed records `{libraryItemId, time (raw seconds), note text, createdAt}`. The macOS SQLite path in `fetch-bookmarks` does not exist on gilahyper; that skill is left alone.

## Approach

### Phase 1 — `_accumulate_timeline` extraction (`swanki/audio/_common.py`)

Extract the body of `combine_audio_with_section_pauses` (`:1112-1164`: bookend-start, the section/chunk loop with `_load`+`_gain_match`+`_gap_ms_for`+crossfade, section pauses, bookend-end) into a private `_accumulate_timeline(sections, *, <all the knob params>, bookend_start, bookend_end, ...)`. It performs the identical operations in the identical order and returns `(combined: AudioSegment, timeline: ChunkTimeline)`. Offsets are read off the *running* `combined` object: before appending a chunk, record `offset_ms = len(combined)` (or the section's running cursor accounting for the crossfade overlap), append, then `duration_ms = len(combined) - offset_ms` so the recorded span is precisely the chunk's footprint in the final mix (crossfade shortening included automatically). Section `start_ms`/`gap_before_ms` and bookend spans recorded the same way.

`combine_audio_with_section_pauses` becomes: build the timeline via `_accumulate_timeline`, `combined.export(...)` exactly as before (same bitrate `192k`), discard the timeline (it does not write the sidecar — only restitch does, since restitch is the surgical/measured path and the original render is reproduced by it anyway). The shared-traversal contract, stated once for the implementer:

```
_accumulate_timeline walks segments S0..Sn in assembly order, maintaining
`combined`. For each chunk: off=len(combined); combined=append(load(chunk));
dur=len(combined)-off. combine_audio_with_section_pauses MUST consume this
exact `combined` (no second assembly) → offsets describe the exported bytes.
```

Self-verify here: a diff of the new `combine_audio_with_section_pauses` against the old must show *only* delegation — no changed `_load`/`_gap_ms_for`/crossfade/export logic.

### Phase 2 — sidecar model + write in `restitch_from_chunks`

Add the frozen pydantic models (`ChunkTimeline`, `Section`, `ChunkSpan`, `Span`) near the top of `_common.py`. In `restitch_from_chunks` (`:1275`), capture the `ChunkTimeline` returned from the shared walk (refactor restitch to call a variant of `combine` that returns the timeline, or have it call `_accumulate_timeline` + export itself — keep one export site). Write `chunk_timeline.json` to `manifest_path.parent` via `model_dump_json(indent=2)`. `audio_type`, per-chunk `file`/`section`/`index` come from the manifest; offsets/durations from the measured walk. Log the path like `write_chunk_manifest` does.

### Phase 3 — public query functions + exports

Implement `chunk_time_window`, `time_to_chunk`, `chunk_time_window_abs` in `_common.py`. Shared resolver: `source` → sidecar path (if dir: `dir/chunk_timeline.json`; if manifest path: `parent/chunk_timeline.json`; if output_dir: search for the chunks subdir's sidecar). Load+validate the manifest, assert `audio_type`. If sidecar present → validate into `ChunkTimeline` and answer. If absent → run `_accumulate_timeline` over the manifest's chunk files (same walk), persist, then answer. `time_to_chunk` returns the index of the `ChunkSpan` whose `[offset_ms, end_ms)` contains `position_ms - absolute_offset_ms` (clamp to nearest if the position lands in an inter-chunk gap; document the gap rule). `chunk_time_window_abs` = `chunk_time_window` window shifted by `preceding_chapter_durations_ms`. Export all three from `swanki/audio/__init__.py` (`__all__` + import line) alongside the existing surgical/restitch exports.

### Phase 4 — `scripts/abs_bookmarks.py` (NEW)

Mirror `scripts/zotero_annotations.py` structure exactly: frontmatter docstring, `from dotenv import load_dotenv` with an **explicit** `dotenv_path` (script is run via PYTHONPATH=repo-root, cwd may differ), pydantic `AbsBookmark{library_item_id, time_s, note, created_at}`, an importable `get_bookmarks(*, citation_key: str | None = None) -> list[AbsBookmark]` that GETs `${ABS_URL}/api/me` with `Authorization: Bearer <token-file-contents>`, and a thin `argparse` CLI (`--citation-key`, `--json`). Field names in the `/api/me` JSON are probed at build time against a captured fixture (see Open Questions); isolate the JSON→model mapping in one small function so it is testable with a fixture and trivially patchable.

### Phase 5 — `.claude/skills/audio-fix-from-annotations/SKILL.md` (NEW)

Frontmatter: `description`, `user_invocable: true`, `arguments: "<citation_key> [--color orange] [--from-bookmarks]"`. Phased body:

1. **Resolve inputs.** Default color `orange`. Pull Zotero annotations via `scripts/zotero_annotations.get_annotations(zot, item_key, color_hex=COLOR_MAP["orange"])`. Optionally pull ABS bookmarks via `scripts/abs_bookmarks.get_bookmarks(citation_key=...)`.
2. **Resolve live dir + audio_type.** From served filename / citation key pick the highest `_N` `SWANKI_DATA` dir whose manifest matches; assert `manifest["audio_type"]` vs the served-name infix. ABS bookmark `time` → chapter/file only.
3. **Locate chunks.** Content-match each highlight against `manifest.chunks[].text`. Bookmark `time` → sidecar MM:SS via `time_to_chunk` for reporting/confirmation only. Classify each hit text+speech vs speech-only.
4. **Single human-review gate.** Present a consolidated table: annotation → matched chunk index/section → current text → proposed new text (or "speech-only re-render") → reported MM:SS. **Exactly one** approval prompt. No re-TTS before approval.
5. **Apply (post-approval, unattended).** Fish preflight `fish_speech_healthy(server_url)`; if down, retry loop with backoff, abort with a clear message after N tries. Build one consolidated `chunk_edits` map. Call `regenerate_and_restitch(manifest_path, chunk_edits, audio_type=<asserted>, tts_kwargs=<reference voice from manifest/config>)`. Verify every *untouched* chunk mp3 is sha256 byte-identical to its pre-run hash (capture hashes before re-TTS).
6. **Publish.** `git add` changed chunk(s)/manifest/sidecar/output + commit (commit-trio incl. notes + weekly); rebase onto main if behind; `sync_to_zotero(citation_key, output_dir, audio_prefix, content_key)`; if a rebase happened after sync, re-sync. Poll `/tmp/abs-refresh.lock` (flock wait) then run `scripts/abs_refresh.sh`. Print: synced filename, commit hash, and confirm the fox tag (Zotero unicode marker) is present.

### Phase 6 — tests + notes

`tests/test_audio_timeline.py` (Phase: see Verification). Extend `tests/test_audio_surgical.py`. Dated decision sections in `notes/swanki.audio._common.md`, `notes/swanki.audio.surgical.md`, NEW `notes/scripts.abs_bookmarks.md`; update weekly note (commit-trio rule).

## Gotchas

- **Independent timeline re-derivation drifts ~5s/~11s.** The entire reason for the shared accumulator. Sidestep: every timing answer flows through `_accumulate_timeline`/sidecar — grep the diff for any second summation of chunk lengths and delete it.
- **Crossfade shortens the timeline.** `AudioSegment.append(..., crossfade=ms)` overlaps audio, so naive `sum(durations)+pauses` overshoots. Sidestep: measure `len(combined)` deltas around each append (the shared walk does this inherently); never sum.
- **Trim is content-dependent → no prediction.** `_load` `:1073` cuts inside trailing silence via `detect_silence`; identical text can yield different mp3 lengths. Sidestep: only measure after `_load`; never compute expected length from text.
- **Chunk indices are audio-type-local.** A lecture chunk 7 ≠ reading chunk 7. Sidestep: assert `manifest["audio_type"]` in every query (mirror `surgical.py:87-92`) and in the skill before lookup.
- **ABS bookmark lag/rounding.** The bookmarked second is *after* the issue and rounded. Sidestep: bookmark `time` selects file/chapter only; chunk is found by content-match, MM:SS reported from the sidecar.
- **Latest `_N` dir resolution.** Multiple regenerations exist under `SWANKI_DATA`; an old dir's manifest will mis-map. Sidestep: served filename is ground truth — pick the highest `_N` whose manifest `output_file` + chunk filenames match it; assert before lookup.
- **Git hash after rebase.** `sync_to_zotero` embeds `_git_short_hash` (`zotero.py:182`). Committing/syncing then rebasing makes the embedded hash stale. Sidestep: commit → rebase → *then* sync; if rebased after sync, re-sync.
- **abs-refresh flock contention.** `scripts/abs_refresh.sh` self-skips if `/tmp/abs-refresh.lock` is held (cron may hold it). Sidestep: the skill polls/waits for the lock to free before invoking, so the refresh is not silently skipped.
- **Fish single-failure aborts the batch + voice must match.** Fish has no internal retry; a wrong reference voice produces an audibly different chunk. Sidestep: `fish_speech_healthy` preflight + bounded retry loop; reference voice/`tts_kwargs` read from manifest/config, never hardcoded.
- **macOS BookPlayer SQLite absent on gilahyper.** `fetch-bookmarks`' DB path is `/Users/...`. Sidestep: new skill uses ABS `/api/me`; do not touch `fetch-bookmarks`.
- **Script execution env.** Helper scripts run with `PYTHONPATH=<repo-root>` and `ffmpeg` on PATH (`~/miniconda3/envs/swanki/bin/ffmpeg`); cwd is not guaranteed. Sidestep: `abs_bookmarks.py` uses an explicit `dotenv_path=` (not bare `load_dotenv()`), and tests reference the env's ffmpeg explicitly.
- **Concurrent worktree agents + shared state.** Another agent (solution-manual branch) may be active; `SWANKI_DATA` and Claude auto-memory are shared across worktrees. Sidestep: keep auto-memory writes additive (topic files, never overwrite `MEMORY.md`); consider a short lock around the manifest while editing it during a fix run.
- **Frozen constants / byte-identity.** `tail_buffer_ms=350`, `gain_match_target_dbfs=-25.0`, paragraph=1100/sentence=500, `section_pause_ms=2000`, `bookend_pause_ms=500`. Sidestep: the refactor moves code, changes no constant; the byte-length regression test (below) guards it.
- **Pre-existing non-regression failures.** `test_humanize_latex` and `test_generate_reading_audio_mocked` already fail on main — exclude from the pass/fail judgment; do not "fix" them in this work.

## Verification

No Fish server is used. ffmpeg is present at `~/miniconda3/envs/swanki/bin/ffmpeg`; synthetic chunks are `AudioSegment.silent(...)` exported to mp3 (pattern from `tests/test_audio_common.py`).

- **`tests/test_audio_timeline.py` (NEW):**
  - Build unequal-length silent chunks across **multiple sections** plus start/end bookends; render through `combine_audio_with_section_pauses` with a known postprocessor using `chunk_tail_trim_ms=0` (deterministic lengths, no `detect_silence` variance). Assert each sidecar `offset_ms`/`duration_ms`/`end_ms` per chunk equals the position **re-measured from the restitched output file** (load the final mp3, slice, compare within a small ffmpeg/encode tolerance).
  - Round-trip: `chunk_time_window(...)` then `time_to_chunk(<midpoint>)` returns the original index for every chunk.
  - `absolute_offset_ms` arithmetic and `chunk_time_window_abs(preceding_chapter_durations_ms=...)` arithmetic correct.
  - `audio_type` mismatch raises (wrong audio_type vs manifest).
  - **Byte-length refactor regression guard:** for fixed inputs, the combined output length (and ideally sha256) equals a pre-refactor reference captured for the same inputs — proves the refactor changed no audio bytes.
  - **Separate `tail_trim>0` test:** with `chunk_tail_trim_ms>0` so trimming actually fires, assert the sidecar offsets equal the **measured** positions in the restitched file (proves measured-not-predicted; a predictor would be wrong here).
- **`tests/test_audio_surgical.py` (MODIFY):** with `text_to_speech` mocked, run `regenerate_and_restitch` and assert `chunk_timeline.json` exists and is rewritten (mtime/content changes) after restitch, and validates against the pydantic model.
- **Lint/type:** `ruff` and `mypy` per the project's documented strategy on changed files only; pre-existing excluded failures are not regressions.
- **Skill end-to-end is out of PR scope (manual).** The skill is user-invoked later against live Zotero/ABS/Fish. This PR unit-tests the *helpers* (timeline functions, `scripts/abs_bookmarks.py` JSON→model mapping via a captured fixture) and ships the SKILL.md; the full annotation→publish exercise is a documented manual follow-up, noted in the dendron decision section.

## Open Questions

Documented assumptions — uber-implement proceeds; the reducer-critic is the only gate. None block implementation.

- **ABS `/api/me` JSON field names** are probed at build against a captured response fixture. The JSON→`AbsBookmark` mapping is isolated in one function so a wrong field name is a one-line fix and is fixture-tested. Assumption: bookmarks are reachable under `/api/me` (media-progress/bookmarks subtree); if ABS exposes them under a different endpoint, only `scripts/abs_bookmarks.py`'s URL changes.
- **Sidecar schema is adopted as frozen** as specified (`audio_type`, `total_duration_ms`, `chunks[]`, `bookend_start/end`, `sections[]`); minor additive fields are allowed without a migration. No versioning field unless a breaking change later requires one.
- **Annotation-without-bookmark is the primary path for papers** (content-match across manifests). The classification heuristic (highlighted phrase present in chunk text → text+speech; else speech-only) is a heuristic only — the single human-review gate is the arbiter; the skill must make the proposed action editable at that gate.
- **Many-to-one / one-to-many annotations** collapse into one consolidated `chunk_edits` map → one review → one restitch → one publish. Assumption: a single review pass is acceptable even when several annotations touch one chunk or one annotation spans several chunks.
- **`SWANKI_DATA` live-dir tie-break:** highest `_N` whose manifest matches the served filename. Assumption: filename + chunk-set match uniquely identifies the authoritative regeneration; if two dirs match identically, fail loudly and ask the user rather than guess.
