---
id: igujo963toc5s6pt8a0q454
title: 09
desc: ''
updated: 1781026837895
created: 1781026837895
---

## Context

All Audiobookshelf logic lives in `scripts/` as ten loosely-coupled files: nine Python scripts plus
`scripts/abs_refresh.sh`, an 87-line bash orchestrator that a live cron entry runs every 5 minutes
(`*/5 * * * * .../abs_refresh.sh`) and that the delivery subsystem (PR `#34`) shells out to via
`AbsTarget`. The scripts grew organically and it shows:

- **Four HTTP stacks.** requests (`abs_bookmarks.py`, `abs_clear_bookmarks.py`), httpx
  (`abs_set_chapter_titles.py`, `abs_clean_stale_chapters.py`), urllib (`abs_enrich_metadata.py`,
  `abs_setup_*.py`, `abs_sync_zotero_collections.py`), and raw curl for the library-scan step inside
  `abs_refresh.sh`. No retry anywhere; the curl scan fails silently.
- **Triplicated logic.** `resolve_library()` is copy-pasted (`swanki_abs_sync.py:57`,
  `abs_enrich_metadata.py:75`), as is the citation-key fallback chain and the token loader.
- **No decision record.** Four scripts (`abs_enrich_metadata.py`, `abs_setup_libraries.py`,
  `abs_setup_collections.py`, `abs_sync_zotero_collections.py`) have no dendron notes at all.

Two operational problems motivate the build now:

1. **Slow republish loop.** The only path to land one regenerated chapter on ABS is the full 7-step
   refresh, ~20 minutes -- dominated by step 1's Zotero multi-projection repagination and zip
   downloads, not by ABS itself (the scan trigger is a cheap POST). A targeted path -- drop the
   local file, scan one library, fix that item's chapters, verify -- takes seconds.
2. **Bookmark wipe is all-or-nothing.** `abs_clear_bookmarks.py` clears every bookmark on an item.
   After a surgical chunk edit (`swanki/audio/comment_edit.py:edit_chunk`, PR `#41`), only the
   bookmarks inside the edited window are resolved; the rest should survive.

This plan consolidates everything into a new `swanki/abs/` package: one `ABSClient`, the 7-step
refresh as a module function, a fast targeted refresh, and a windowed bookmark wipe wired into the
publish path. User decisions already made: **windowed wipe-on-replace is the default** (no
timestamp-migration math -- bookmarks are ephemeral issue flags; the durable address is chunk-text
content-match), and **the migration is one-pass** (all ~10 scripts move now, becoming thin shims or
deleted). The shim precedent is exact: `scripts/_swanki_zotero_artifacts.py` is already a re-export
shim over `swanki/delivery/artifacts.py`.

## Relevant Files

| Path | Action | Purpose | Stance |
| --- | --- | --- | --- |
| `swanki/abs/__init__.py` | NEW | Public API re-exports | n/a |
| `swanki/abs/client.py` | NEW | Single httpx `ABSClient`: token chain, retry, items, scan, chapters POST, bookmark DELETE | n/a |
| `swanki/abs/projections.py` | NEW | Pydantic projection models, `load_projections`, `resolve_library`, citation-key/classify/group_key routing | n/a |
| `swanki/abs/sync.py` | NEW | Zotero zip pull + idempotent `extract_audio` drop (from `swanki_abs_sync.py`) | n/a |
| `swanki/abs/libraries.py` | NEW | Idempotent library ensure (from `abs_setup_libraries.py`) | n/a |
| `swanki/abs/collections.py` | NEW | Zotero->ABS collection mirror, reconcile-don't-wipe (from `abs_sync_zotero_collections.py`) | n/a |
| `swanki/abs/metadata.py` | NEW | Author + cover enrichment (from `abs_enrich_metadata.py`) | n/a |
| `swanki/abs/chapters.py` | NEW | Stale-chapter clean + retitle, merged (shared filename->content_key derivation) | n/a |
| `swanki/abs/bookmarks.py` | NEW | `AbsBookmark`, `get_bookmarks`, `clear_bookmarks`, `clear_bookmarks_in_windows` | n/a |
| `swanki/abs/refresh.py` | NEW | `full_refresh` (7 steps, fcntl lock) + `targeted_refresh` (seconds-scale) | n/a |
| `swanki/abs/__main__.py` | NEW | `python -m swanki.abs` CLI | n/a |
| `scripts/abs_refresh.sh` | MODIFY | Becomes exec shim to `python -m swanki.abs refresh "$@"` | stable |
| `scripts/abs_bookmarks.py` | MODIFY | Becomes re-export shim (imported by `abs_clear_bookmarks.py` and the audio-fix skill) | stable |
| `scripts/abs_clear_bookmarks.py` | MODIFY | Becomes thin CLI shim; dry-run/`--yes` UX kept verbatim | stable rationale, superseded mechanism |
| `swanki/delivery/targets/abs.py` | MODIFY | `AbsTarget.refresh` calls `swanki.abs.refresh.full_refresh(wait=True)`, not subprocess | stable |
| `pyproject.toml` | MODIFY | Declare httpx (direct import today in `swanki/audio/_common.py`, `swanki/sync/zotero.py`; only transitive) | n/a |
| `.claude/skills/audio-fix-from-annotations/SKILL.md` | MODIFY | Opportunistic: point steps at `python -m swanki.abs`; shims mean nothing breaks if skipped | stable |
| `scripts/swanki_abs_sync.py` | DELETE | Absorbed into `swanki/abs/sync.py`; referenced only by `abs_refresh.sh` | stable |
| `scripts/abs_setup_libraries.py` | DELETE | Absorbed into `libraries.py`; referenced only by `abs_refresh.sh` | undocumented |
| `scripts/abs_setup_collections.py` | DELETE | Referenced by nothing; reconcile behavior captured in module notes | undocumented |
| `scripts/abs_sync_zotero_collections.py` | DELETE | Absorbed into `collections.py` | undocumented |
| `scripts/abs_enrich_metadata.py` | DELETE | Absorbed into `metadata.py` | undocumented |
| `scripts/abs_clean_stale_chapters.py` | DELETE | Absorbed into `chapters.py` | in-flux (04.30 suffix tolerance) |
| `scripts/abs_set_chapter_titles.py` | DELETE | Absorbed into `chapters.py` | in-flux (05.14 bounds idempotency) |
| `tests/test_abs_bookmarks.py` | MODIFY | Re-point imports at `swanki.abs.bookmarks`; fixtures unchanged | n/a |
| `tests/test_abs_client.py`, `_projections.py`, `_chapters.py`, `_sync.py`, `_refresh.py` | NEW | Mocked-transport coverage per module | n/a |
| `swanki/sync/zotero_client.py` | REFERENCE | Retry pattern donor (`_is_retryable`, `with_zotero_retry`) | stable |
| `swanki/audio/_common.py` | REFERENCE | `chunk_time_window` (:1973), `chunk_time_window_abs` (:2033) -- window math donors | stable |
| `swanki/audio/comment_edit.py` | REFERENCE | `edit_chunk` returns NEW-timeline window (:285-308) -- the old-window trap | stable |
| `swanki/delivery/__main__.py` | REFERENCE | `finalize-abs` subcommand (:71-72, :102) must keep working unchanged | stable |
| `scripts/swanki_finalize_abs.sbatch`, `scripts/swanki_job.sbatch` | REFERENCE | ABS_DIRTY marker + singleton finalizer; untouched | stable |
| `swanki/delivery/artifacts.py` | REFERENCE | Newest-artifact-per-content-prefix selection, reused by targeted refresh | stable |
| `scripts/_swanki_zotero_artifacts.py` | REFERENCE | The shim precedent to copy | stable |
| `~/Documents/projects/infra/abs/projections.yml` | REFERENCE | External routing config; stays outside the repo and outside Hydra | stable |
| `scripts/publish_regen_to_abs.sh` (+3 sibling one-shot publish scripts) | REFERENCE | Historical one-shots; keep working through the `abs_refresh.sh` shim, otherwise untouched | n/a |

## Key Design Decisions

1. **One httpx `ABSClient` with the zotero-client retry pattern.** Every ABS HTTP call goes through
   `client.py`: `httpx.Client(timeout=httpx.Timeout(180, connect=60))`, bounded exponential backoff
   on `httpx.TimeoutException`/`TransportError`/5xx, 404 terminal -- the exact classifier shape of
   `swanki/sync/zotero_client.py:_is_retryable`. Rejected: keeping requests (perpetuates the
   4-stack fragmentation) and per-module sessions or a `_common.py` (the client IS the common layer).
2. **Orchestration lives in `swanki/abs/refresh.py`, not in delivery.** `AbsTarget` stays a thin
   `SyncTarget` protocol adapter calling `full_refresh(wait=True)`. Rejected: moving the 7-step
   pipeline into `swanki/delivery/targets/abs.py` -- delivery is a consumer of ABS capability
   (PR `#34` is merged and stable), not the owner of ABS internals; the cron path and the audio-fix
   skill need the same orchestration without delivery in the loop.
3. **`scripts/abs_refresh.sh` survives as an exec shim.** The live crontab fires it every 5 minutes,
   four legacy publish scripts and the audio-fix skill reference it. A ~10-line
   `exec python -m swanki.abs refresh "$@"` shim makes the cutover atomic without touching crontab.
   Rejected: deleting it and editing crontab (couples a code merge to live-box state).
4. **The lock moves into Python: `fcntl.flock` on the same `/tmp/abs-refresh.lock`.** `flock(1)` and
   `fcntl.flock` are the same syscall on the same file, so during any mixed window an in-flight bash
   run and a module run still exclude each other; the bash shim carries no lock of its own.
   Non-blocking mode catches `BlockingIOError` and returns skipped -- a narrow, justified exception
   per the `with_zotero_retry` precedent; everything else still fails fast. Rejected: the `filelock`
   package (new dependency for one fcntl call) and keeping the lock in bash (the module must be
   callable without the shim).
5. **Windowed bookmark wipe runs at publish time in `swanki/abs/bookmarks.py`, never inside
   `edit_chunk`.** API: `clear_bookmarks_in_windows(citation_key, windows)`, windows in item-global
   seconds. Rejected: wiping from `swanki/audio/comment_edit.py` -- (a) layering: `swanki/audio/`
   must not talk to the ABS server; (b) timing: `edit_chunk` runs before the new audio lands on ABS,
   so wiping there destroys bookmarks while the old audio is still live, and a failed publish would
   orphan the wipe.
6. **Windows are computed on the OLD timeline with item-global offsets.** `edit_chunk` returns the
   chunk's NEW `(start_ms, end_ms)` while existing bookmarks sit on the old timeline, and bookmark
   `time` is item-global where chunk windows are per-file (traps and mechanics: Gotchas 1-2 and the
   Approach snippet). Rejected: timestamp migration of surviving bookmarks (explicit prior user
   decision -- clear-and-re-mark).
7. **Targeted refresh is drop + scan + per-item chapter fix-up + verify, sourced from local disk.**
   It skips steps 1-6 of the full refresh -- the ~20-minute cost is Zotero repagination, which the
   local-artifact source (delivery plan 2026.06.04 decision 1) makes unnecessary. It is NOT
   scan-only: a republished file has a new `-<TS>-<hash>` name, so the item's chapters point at a
   deleted file until stale-clean + retitle run for that item. Rejected: relying on the 5-minute
   cron to fix chapters eventually (leaves the item broken in Prologue for up to a cycle, and the
   cron path is non-blocking so it can skip).
8. **`chapters.py` merges stale-clean and retitle.** Both scripts share the filename->content_key
   derivation (`content_key_from_filename` stripping `-{summary,reading,lecture}-<TS>-<hash>.<ext>`),
   the suffix-tolerance rule for manually-set titles (04.30 note), and the 0.5s bounds-drift
   idempotency check (05.14 note). The sqlite-read / API-write split is preserved: read state from
   `absdatabase.sqlite` (`ABS_DB` env), write only via the API so ABS's in-memory state updates
   without a restart.
9. **`projections.py` is the single home for routing.** `resolve_library` and the citation-key
   fallback chain (`data.citationKey` -> `"Citation Key:"` regex on `extra` -> Zotero item key),
   each currently duplicated, become one function apiece with pydantic models for projection
   entries. `projections.yml` stays external at `~/Documents/projects/infra/abs/projections.yml`
   (delivery plan decision 7) -- every entry point takes a `projections_path` with that expanduser
   default; tests pass fixture YAML. Rejected: Hydra-izing it (server routing is infra, not
   pipeline config).
10. **Token chain is one function: `ABS_API_TOKEN_FILE` -> `ABS_API_TOKEN` -> default path, with
    `expanduser()` before read.** Today only `abs_enrich_metadata.py` honors the env-var fallback
    and not every script expands `~`; unifying removes a class of works-on-one-box bugs.
11. **One-pass migration with reference-verified dispositions.** Seven scripts are deleted
    (referenced only by `abs_refresh.sh` itself, or by nothing); three files become shims because
    live consumers exist (named per-row in the Relevant Files table). Rejected: incremental
    migration (each partial state needs its own shim story; no consumer blocks one pass).
12. **Declare httpx in `pyproject.toml`.** The swanki env already resolves httpx 0.28.1, but
    pyproject declares only `requests` (line 37) -- httpx arrives transitively via pyzotero while
    two swanki modules already import it directly. Pin `httpx>=0.28`. Drop `requests` only if
    nothing else in the repo uses it after migration; otherwise leave it.
13. **Deleted scripts' behavior becomes module documentation.** Four of the seven have no dendron
    notes; their load-bearing quirks (idempotency rules, silent skip of folders with no
    citation-key match, reconcile-don't-wipe collections) get captured in the new `swanki.abs.*`
    module notes as the durable record.

## Approach

**Order of work** -- bottom-up, so each layer is testable before its consumers move:

1. `client.py` + `projections.py` (the shared substrate).
2. Leaf modules `sync.py`, `libraries.py`, `collections.py`, `metadata.py`, `chapters.py`,
   `bookmarks.py` -- each a near-verbatim port of its script's logic onto `ABSClient`, preserving
   idempotency checks exactly.
3. `refresh.py` + `__main__.py`.
4. The cutover commit: shim `abs_refresh.sh`, shim `abs_bookmarks.py`/`abs_clear_bookmarks.py`,
   rewire `AbsTarget`, delete the seven scripts -- module landing and shim swap in the SAME commit,
   because the cron fires every 5 minutes and any window where `abs_refresh.sh` calls deleted
   scripts is a live breakage.
5. Targeted refresh + windowed wipe end-to-end against a real regenerated chapter.
6. Module dendron notes (capturing deleted-script behavior) + opportunistic skill doc updates.

**Client and projections.** `ABSClient` holds the base URL (`ABS_URL` env, default
`https://abs.michaelvolk.dev`), the token chain, one `httpx.Client`, and typed methods for the
small ABS surface actually used: `GET /api/libraries`, `GET /api/libraries/{id}/items`,
`GET /api/items/{id}?expanded=1`, author PATCH, `POST /api/items/{id}/chapters`,
`POST /api/libraries/{id}/scan`, `GET /api/me` (bookmarks),
`DELETE /api/me/item/{id}/bookmark/{time}`. The retry wrapper is a port of `with_zotero_retry`
with an httpx-only classifier. `projections.py` models the YAML (`push_audio`/`push_anki`, Zotero
library + tag, `audiotypes`) and exposes `resolve_library`, `citation_key`, `classify`,
`group_key` -- consumed by sync, collections, and metadata so the duplicated copies collapse.

**Refresh.** `full_refresh(wait: bool, projections_path: Path = DEFAULT)` reproduces the 7 steps of
`abs_refresh.sh` as function calls: zip pull, ensure libraries, mirror collections, enrich
metadata, clean stale chapters, set chapter titles, scan all libraries. Step 7's unretried inline
curl becomes `client.scan_library()` -- typed, retried, errors propagate instead of vanishing. The
fcntl lock wraps the whole function; `wait=False` returns a skipped status on `BlockingIOError`
(cron semantics), `wait=True` blocks (delivery semantics). The function is environment-agnostic --
bash-drainer, SLURM finalizer, cron shim, and interactive use all call the same API.

`targeted_refresh(citation_key, output_dir, projections_path=DEFAULT)`: select newest artifacts via
`swanki/delivery/artifacts.py`, route through `projections.py` to find EVERY projection carrying
the item (fan out -- an item can live in several projection libraries), drop the mp3 into each
`{abs_root}/{projection}/Swanki-{Kind}-{Audiotype}/{group}/` dir using the same
replace-stale-same-`(key, audio_type)` rule as `sync.extract_audio`, scan only the affected
libraries, run the per-item chapter fix-up (stale-clean + retitle for that one item), then verify
by polling the item until its `audioFiles` list the new filename. Seconds, not ~20 minutes.

**CLI.** `python -m swanki.abs` mirrors the `python -m swanki.delivery` precedent:
`refresh [--wait]` (full, default non-blocking to match cron), `refresh --target <citation_key>
--output-dir <dir>` (targeted), `bookmarks --citation-key <key>` (list), and
`clear-bookmarks --citation-key <key> [--window START END]... [--yes]` (dry-run default). The
`abs_refresh.sh` shim forwards `"$@"` so `--wait` keeps working for the four legacy scripts that
pass it.

**Windowed wipe and the publish path.** The audio-fix-from-annotations skill (the caller) drives:
it content-matches bookmarks to chunks, snapshots each target chunk's OLD window, runs
`edit_chunk`, publishes via targeted refresh, then wipes. The subtle part is the window math --
the one place a wrong sign or wrong timeline silently deletes the wrong bookmarks:

```python
# BEFORE edit_chunk (which restitches and rewrites chunk_timeline.json):
old_start_ms, old_end_ms = chunk_time_window(chunks_dir, audio_type, idx)
offset_ms = sum(...)  # durations of ABS-item audio files preceding this chapter file
window = ((old_start_ms + offset_ms) / 1000,
          (old_end_ms + offset_ms) / 1000 + pad_s)  # pad forward: playhead lags the issue
result = edit_chunk(...)   # result.start_ms/end_ms are NEW-timeline; never use for the wipe
targeted_refresh(...)      # new file lands on ABS
clear_bookmarks_in_windows(citation_key, [window])  # only after publish succeeds
```

`clear_bookmarks_in_windows` filters `get_bookmarks(citation_key=...)` by `time_s` in-window and
deletes via the client, keeping `abs_clear_bookmarks.py`'s UX verbatim: dry-run by default,
`--yes` to delete, archive-bookmark-notes-first warning (deletion is irreversible). The whole-item
clear remains the degenerate case (no windows = clear all), so the existing clear-and-re-mark
workflow loses nothing.

**Out of scope.** Incremental/delta Zotero sync to speed up the FULL refresh (the targeted path
covers the hot loop); touching the crontab; the encyclopedia/glossary work; bookmark timestamp
migration; the SLURM cutover itself (`notes/runbook.slurm-cutover.md` stays a separate task --
this module just must not assume either world).

## Gotchas

1. **`edit_chunk` returns the NEW-timeline window.** `restitch_from_chunks` rewrites
   `chunk_timeline.json` before `chunk_time_window` is called (comment_edit.py:285-289), so
   `ChunkEditResult.start_ms/end_ms` describe where the chunk lands AFTER the edit while bookmarks
   sit on the old timeline. Sidestep: snapshot `chunk_time_window(...)` before calling
   `edit_chunk`; never feed the result's window to the wipe.
2. **Bookmark `time` is item-global; chunk windows are per-file.** A multi-chapter ABS book
   stitches files end-to-end, so a bookmark at 7400s may be 200s into chapter 5. Convert via
   cumulative preceding-file durations (the `audioFiles[].duration` ordering
   `chapters_from_audiofiles` already walks); `chunk_time_window_abs` is the in-repo precedent.
3. **Bookmark `time_s` is the playhead when the note was saved, lagging the issue by up to
   minutes** (documented in `abs_bookmarks.py`'s header), so a bookmark flagging a chunk can sit
   past the chunk's end. Sidestep: pad the window forward (`pad_s`, generous default) and keep
   dry-run-first so the human sees the selection before `--yes`.
4. **The cron fires every 5 minutes during migration.** Sidestep: the single cutover commit
   (Approach step 4); the shared `/tmp/abs-refresh.lock` exclusion (Decision 4) covers any
   in-flight bash run.
5. **Multi-projection fan-out.** `projections.yml` can route one item into several projection
   libraries; dropping into only one leaves the others stale until the next full refresh.
   Sidestep: `targeted_refresh` iterates all projections whose tag/kind/audiotype routing matches,
   honoring `push_audio: false`.
6. **Idempotency checks are load-bearing.** Skip-existing mp3 + replace-stale-same-`(key, type)`
   (`swanki_abs_sync.py:121-138`), skip-existing `cover.jpg`, only-stale chapter deletion,
   skip-matching titles within 0.5s bounds drift, reconcile-don't-wipe collections
   (manually-curated ABS collections must survive). Sidestep: port each check verbatim; add
   re-run-twice tests asserting the second run is a no-op.
7. **Citation-key chain has three fallbacks** (`data.citationKey` -> `"Citation Key:"` regex on
   `extra` -> item key), and folders with no match are SILENTLY skipped by sync/enrich. The
   silence is intentional (non-swanki folders coexist) but undocumented. Sidestep: one function in
   `projections.py`, a three-case test, and the silent-skip documented in the module note.
8. **`tests/test_abs_bookmarks.py` imports `scripts.abs_bookmarks`.** Moving the model without
   the shim breaks the suite mid-PR. Sidestep: the shim re-exports `AbsBookmark`,
   `get_bookmarks`, `_to_bookmark`, `_token`, `ABS_URL` exactly as
   `_swanki_zotero_artifacts.py` does; re-point the test imports in the same PR.
9. **The bookmark DELETE endpoint keys on `{time}`.** `abs_clear_bookmarks.py:48` int-coerces
   when the float is integral; a float-formatted time that ABS stored as int 404s the delete --
   and 404 is non-retryable per the classifier, so it fails loudly. Sidestep: port the coercion
   and fixture-test both shapes.
10. **Both lock modes must survive with their semantics intact.** Cron path: non-blocking,
    skip-and-log (the next tick covers it). Delivery/finalizer path: blocking, never silently
    no-op (queue DONE means delivered). Sidestep: `wait` threaded from `AbsTarget` and the CLI;
    the Verification lock test asserts both.
11. **The SLURM finalizer must keep working unchanged.** `scripts/swanki_finalize_abs.sbatch:36`
    runs `python -m swanki.delivery finalize-abs` and clears the ABS_DIRTY marker on success;
    `swanki/delivery/__main__.py:71-72` routes that to `AbsTarget.refresh`. Sidestep: only
    `AbsTarget`'s internals change (subprocess -> function call); its `name`, signature,
    `wait=True` default, and dry-run printing stay.

## Verification

- `~/miniconda3/envs/swanki/bin/python -m pytest tests/ -x -q` -- full suite green, including the
  four `tests/test_delivery_*.py` files untouched and `tests/test_abs_bookmarks.py` re-pointed.
- New mocked-transport tests (httpx `MockTransport` or monkeypatched client):
  - token chain three-way (`ABS_API_TOKEN_FILE`, `ABS_API_TOKEN`, default path + expanduser);
  - retry classifier (timeout retried, 503 retried, 404 immediate failure);
  - citation-key chain three cases; `content_key_from_filename` suffix match + fall-through;
  - `chapters_from_audiofiles` cumulative start/end bounds;
  - windowed-wipe selection against a fixture bookmark list, including the item-global offset and
    forward pad; bookmark-delete time coercion (int vs float);
  - multi-projection fan-out routing from a fixture `projections.yml`.
- Re-run-twice idempotency tests: `extract_audio` into a tmpdir (second run extracts 0; stale
  same-key file replaced), chapter retitle (second run posts nothing), collection reconcile
  (no-op on identical state).
- Lock test: hold the fixture lock, assert `full_refresh(wait=False)` returns skipped without
  running step 1; release, assert it runs; `wait=True` blocks then proceeds.
- `python -m swanki.delivery finalize-abs --dry-run` prints the would-run line and exits 0
  (sbatch contract intact).
- `bash scripts/abs_refresh.sh` shim end-to-end on gilahyper once: logs the 7 steps, exits 0, and
  a second concurrent invocation logs the skip message (mixed bash/Python lock exclusion observed
  live).
- `python -m swanki.abs refresh --target <citation_key> --output-dir <dir>` against a freshly
  regenerated chapter: file lands in every routed projection dir, scan completes, item chapters
  show the new content_key title, wall-clock seconds.
- `python -m swanki.abs clear-bookmarks --citation-key X --window ...` dry-run against the live
  server lists only the in-window bookmarks; no `--yes` during verification.
- `/ruff` and `/mypy` skills on all new/modified Python files.
- After merge: watch two cron ticks in `~/.cache/abs-refresh.log` for clean runs, and confirm the
  Zotero->Anki->ABS `.delivery.json` markers still write on the next queued job.
