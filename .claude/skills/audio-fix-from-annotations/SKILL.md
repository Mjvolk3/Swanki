---
description: Map orange Zotero/ABS annotations to exact audio chunks, then surgically re-TTS + restitch + republish after one human-review gate
user_invocable: true
arguments: "<citation_key> [--color orange] [--from-bookmarks]"
---

# Audio Fix from Annotations

Turn color-coded review notes into precise single-chunk audio fixes without
a full regeneration. Default color **orange**. Exactly **one** human-review
gate; after approval the fix is applied and published end-to-end.

Why this is safe to automate: chunk re-TTS + restitch is seconds (not the
long Mathpix/full-gen pipeline the user runs in their own terminal), and the
review gate is the control point.

## Phase 1 - Resolve inputs

1. Args: `<citation_key>` (required); `--color` (default `orange`);
   `--from-bookmarks` to also pull ABS bookmarks.
2. Zotero annotations: `python scripts/zotero_annotations.py <citation_key> --color orange`
   (or import `get_annotations` + `COLOR_MAP["orange"]`). Each has highlighted
   `text`, `comment`, `page`.
3. If `--from-bookmarks`: `python scripts/abs_bookmarks.py --citation-key <citation_key>`
   (or import `scripts/abs_bookmarks.get_bookmarks`). A bookmark `time` is the
   playhead WHEN SAVED -- it lags the issue by minutes; use it ONLY to pick
   the chapter/file, never as a chunk boundary.

## Phase 2 - Resolve the live dir + audio_type

- The ABS-served filename is ground truth. Under `SWANKI_DATA`
  (`/scratch/projects/torchcell-scratch/Swanki_Data/<...>`), pick the
  **highest `_N`** paper/chapter dir whose `*_chunks/chunk_manifest.json`
  `output_file` + chunk filename set matches the served filename.
- `audio_type` = `manifest["audio_type"]`; cross-check the
  `-lecture-`/`-reading-`/`-summary-` infix in the served name. Assert they
  agree before any lookup (chunk indices are audio-type-local).
- Pure-Zotero path (no bookmark, the common case for papers): `citation_key`
  -> SWANKI_DATA dir; if multiple audio types exist, content-match each
  annotation against every type's chunk text and report which matched.
- If two dirs match identically, STOP and ask the user -- do not guess.

## Phase 3 - Locate chunks (content-match + exact timeline)

- For each annotation, find the chunk whose `manifest.chunks[].text` contains
  the highlighted source phrase (normalize whitespace/punctuation). This is
  authoritative; the bookmark `time` only narrows the chapter/audio_type.
- Report each hit's precise window via
  `swanki.audio.chunk_time_window(chunks_dir, audio_type, idx)` (and
  `chunk_time_window_abs(...)` / `time_to_chunk(...)` for ABS-stitched books,
  passing the summed preceding chapter-file durations). The
  `chunk_timeline.json` sidecar is exact (measured at restitch); if absent it
  is recomputed via the same accumulator on first query.
- Classify each: highlighted phrase present in chunk text -> **text+speech**
  (edit chunk text, re-TTS). Delivery/artifact issue, no source-text change
  -> **speech-only** (`chunk_edits[idx] = None`). The human is final arbiter.

## Phase 4 - Single human-review gate

Present ONE consolidated table: annotation/comment -> matched chunk
index/section -> current text -> proposed new text (or "speech-only
re-render") -> reported MM:SS. The proposed action must be editable here.
Exactly one approval prompt. **No re-TTS before approval.**

## Phase 5 - Apply (post-approval, unattended)

The actual edit + re-TTS + restitch is swanki code, NOT a bespoke script:
call `swanki.audio.comment_edit.edit_chunk` once per approved intervention.
It runs the preprocessor on new prose (so an edit matches a fresh full-gen),
re-TTSs only that chunk, restitches (rewriting `chunk_timeline.json`), and
writes a `_edits/` audit trail (prior chunk mp3+text + manifest snapshot +
`edits_log.jsonl`) automatically.

1. Fish preflight: `swanki.audio.surgical.fish_speech_healthy(server_url)`;
   if down, retry with backoff a few times, then abort with a clear message.
2. Read reference voice / `tts_kwargs` (incl. the `preprocessor` sub-tree) and
   `speed` from the paper's model config / original manifest -- never hardcode;
   books stay first-person. A Fish `tts_kwargs` with no `reference_id` makes
   `edit_chunk` fail loud.
3. For each approved row, call
   `edit_chunk(manifest_path, idx, *, comment=<reviewer note> | new_text=<exact
   words> | speech_only=True, tts_kwargs=<voice>, model=<llm string>,
   speed=<paper speed>)`. The comment path is typical (the agent rewrites);
   pass `new_text` only when you've decided the exact wording, `speech_only`
   for a delivery re-roll. It returns the action taken and the edited chunk's
   NEW `(start_ms, end_ms)` for ABS re-marking.
4. If `edit_chunk` returns `needs_section_regen` or `cannot_fix`, do NOT
   auto-apply -- surface the rationale to the user (conceptual/stylistic
   comments are handled by editing `conf/prompts/*.yaml`, not here).

## Phase 6 - Publish (provenance-correct)

1. `git add` changed chunk(s)/manifest/sidecar/output + module notes + weekly
   (commit trio); commit.
2. Rebase onto `main` if behind. **Order matters**: commit -> rebase ->
   `swanki.sync.zotero.sync_to_zotero(citation_key, output_dir, audio_prefix,
   content_key)` so the embedded `_git_short_hash` is the final one. If a
   rebase happens AFTER sync, re-sync.
3. Poll the abs-refresh flock (`/tmp/abs-refresh.lock`) until free, then run
   `bash scripts/abs_refresh.sh` (a scheduled run otherwise silently skips).
4. Report: synced zip filename, commit hash, and confirm the fox tag (Zotero
   unicode marker) is present on the item (idempotent in `sync_to_zotero`).

## Rules

- Default color orange; one review gate; never trust raw ABS bookmark time
  for chunk identity; assert `audio_type`; commit-before-sync; Fish preflight.
- No `try/except` (fail fast); reuse `swanki.audio.comment_edit.edit_chunk`
  for the apply step (it owns the agent rewrite, preprocessor, re-TTS,
  restitch, and `_edits/` audit) -- never hand-write a `fix_*.py` script and
  never free-type the replacement transcript inline.
- The long full-pipeline regeneration is NOT this skill -- this is the
  surgical, single-chunk path only.
