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

1. Fish preflight: `swanki.audio.surgical.fish_speech_healthy(server_url)`;
   if down, retry with backoff a few times, then abort with a clear message.
2. Capture sha256 of every chunk mp3 (to verify untouched ones later).
3. Build ONE consolidated `chunk_edits` map; reference voice / `tts_kwargs`
   read from the paper's model config / original manifest (never hardcoded;
   books stay first-person).
4. `swanki.audio.surgical.regenerate_and_restitch(manifest_path, chunk_edits,
   audio_type=<asserted>, tts_kwargs=<reference voice>)` -- restitch also
   rewrites the `chunk_timeline.json` sidecar.
5. Verify every NOT-edited chunk mp3 is sha256-identical to its pre-run hash;
   fail loudly if any untouched chunk changed.

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
- No `try/except` (fail fast); reuse `regenerate_and_restitch` /
  `chunk_time_window` / `scripts/abs_bookmarks.py` -- do not reinvent.
- The long full-pipeline regeneration is NOT this skill -- this is the
  surgical, single-chunk path only.
