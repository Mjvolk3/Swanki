---
id: 86je3irxsdghpon5i5ffqaz
title: Zotero
desc: ''
updated: 1775269939846
created: 1775269939846
---

## 2026.04.03 - Zotero attachment upload for Swanki outputs

Uploads apkg and audio files as timestamped child attachments on the corresponding Zotero library item, enabling automatic sync to other machines via Zotero's built-in sync.

- **Timestamped filenames**: `{citation_key}-{type}-{YYYYMMDDTHHMI}-{git_hash}.{ext}` — versions accumulate, old ones pruned manually.
- **Item lookup**: Splits camelCase citation key into search words, matches against the `extra` field where Better BibTeX stores citation keys.
- **Sync log**: Creates/appends to a "Swanki Sync Log" child note on the Zotero item documenting each upload.
- **Git hash**: Embeds abbreviated commit hash in filenames for traceability back to the code version that generated the output.
- **Hydra config**: `zotero=sync` enables upload; off by default. Credentials from `.env` (`ZOTERO_API_KEY`, `ZOTERO_LIBRARY_ID`).

## 2026.04.15 - Zip bundling, content_key, and book-chapter support

Bundle every Swanki output for a run into a single timestamped zip before upload, support book-chapter content separately from the BibTeX key, and harden item lookup and the upload itself for slow/large transfers.

- **Single zip per run**: All output files are packed into `{file_key}-{timestamp}-{commit}.zip` and uploaded once instead of N individual attachments. Drastically reduces Zotero API calls and produces a clean, atomic version per run. Sync log entry now lists the contained files as a `<ul>` under an `<h3>` per upload.
- **content_key vs citation_key split**: New `content_key` parameter distinguishes the filename identifier from the Zotero lookup key. For papers they're the same. For book chapters the BibTeX key (e.g. `bishop2024`) drives Zotero lookup while `content_key` (e.g. `bishop2024_CH01_deep-learning-revolution`) names the bundled files so multiple chapters from one book don't collide.
- **Better camelCase splitting**: `_find_zotero_item()` now also splits `UPPER` → `Upper` runs and filters compound tokens longer than 15 characters, then caps the search to 5 words. Fixes lookup failures for keys like `cardiffSystemsLevelModelingCRISPRBased2024`.
- **Upload timeout patch**: pyzotero's internal `httpx.post` call uses the default httpx timeout, which kills large bundle uploads. We monkey-patch `httpx.post` for the duration of the `attachment_simple` call to set a 600s read / 60s connect timeout, then restore. Wrapped in try/finally so failures don't poison the global httpx state.

## 2026.04.17 - Robust citation-key lookup and fox-emoji tag on upload

Two ergonomic fixes for the upload path. First, `_find_zotero_item` was unable to locate `zvyaginGenSLMsGenomescaleLanguage2023` because its over-split camelCase search ("zvyagin Gen SLMs Genomescale Language") ANDs to zero results on Zotero's full-text search, and the fallback only checked `extra` — missing items whose citation key lives in Zotero 7's native `citationKey` field. Second, the user tracks Swanki-uploaded papers by a 🦊 tag on the parent item; uploads were leaving no visible marker.

- **Progressive query strategy (matches `scripts/zotero_paper_import.py::find_item_by_citation_key`)**: try title-words first, then all words, then the first two title-words, each under both default and `qmode=everything`. Stops at the first item whose `extra` contains `Citation Key: {key}` or whose native `citationKey` field matches.
- **Extracted `_match_citation_key` helper**: checks BBT `Citation Key: {key}` in `extra` AND Zotero 7 `citationKey`. Shared shape with the import script.
- **🦊 tag appended on successful upload**: After the zip upload and sync-note update, `_find_zotero_item` refetches the parent item and `zot.add_tags(item, "🦊")` if not already present. Idempotent — a second upload of the same paper leaves the tag untouched.

## 2026.04.26 - APKG glob picks up filename suffix

Caught during the first end-to-end Schaum's Ch1 run: the apkg source pattern in `_OUTPUT_TYPES` was hard-coded to `{citation_key}.apkg` and silently skipped files matching the new `apkg_filename_suffix` knob (e.g. `<key>-problem-set.apkg`). The mp3s uploaded fine but the apkg was missing from Zotero.

Switched the apkg pattern to `{citation_key}*.apkg` and updated the loop to glob the output dir, iterating over all matches. The dest_name template now uses `{stem}` so the suffix is preserved in the Zotero attachment name. Backward-compatible: literal patterns still return 0 or 1 matches; the legacy `<key>.apkg` form still works.

## 2026.05.18 - Replace prior versions; stop stacking artifacts

ABS is now the iteration surface for audio review, so Zotero should hold only the latest swanki artifact per chapter, not the full history. Prior behavior stacked attachments — `VPZK6ESQ` (the Schaum's Microbiology parent item) had 13 attachments from 11+ regen cycles before this change.

Added `_prune_prior_attachments`: after a successful `zot.attachment_simple(...)` upload, list children of the parent item and `zot.delete_item` any attachment whose filename matches `^<chapter_base>.*\.(?:zip|apkg)$`, excluding the just-uploaded filename. The chapter base is derived by `_chapter_base(content_key)` which truncates at `_CH<digits>` — so `MyBook_CH01`, `MyBook_CH01_intro`, and a future `MyBook_CH01_revised` all share base `MyBook_CH01` and replace each other.

Runs AFTER upload, never before — guarantees we never leave an item with zero artifacts if the upload itself fails (e.g. the same `httpx.ReadTimeout` that has hit several past runs). Defensive: filters `itemType == "attachment"`, refuses to delete the just-uploaded filename, ignores notes and non-matching filenames (like the source book PDF).

One-off cleanup: ran the prune helper directly against `VPZK6ESQ` (keeping today's `2CBKWQH8`) — deleted 12 stale items (8 historical ZIPs + 3 legacy `_CH01-problem-set.apkg` + 1 even older 7a08fcb ZIP). Tests live in `tests/test_zotero_prune.py` covering chapter-base extraction, same-chapter replacement, other-chapter preservation, legacy apkg form, just-uploaded protection, and non-attachment skip.


## 2026.06.04 - Hardened client for flaky Zotero API

Part of [[swanki.delivery]] ([[plan.delivery-subsystem-source-target-sync.2026.06.04]]).
`sync_to_zotero` now builds its client via `make_zotero_client` (lifts the
pyzotero per-call read timeout) and wraps the item-find pagination in
`with_zotero_retry` (retry 5xx/timeouts, skip 404). See [[swanki.sync.zotero_client]]
for why the module-global timeout lever is the effective one. Still the sole
writer of the fox tag and the git-commit-hash provenance. Unchanged: the 600s
`httpx.post` upload patch, chapter-base pruning, the sync-log note.

## 2026.06.05 - Paginate the sync-log note lookup (kill duplicate-note explosion)

`_find_or_create_sync_note` looked up the existing "Swanki Sync Log" note with a
bare `zot.children(parent_key)`, which returns only the FIRST page (~25 items).
Once a parent item accumulated enough attachments/notes, the sync-log note fell
off page 1, the find-loop missed it, and every subsequent sync created a brand
new note — observed as 85 duplicate "Swanki Sync Log" notes on a single item.

Fixed by wrapping the call in pyzotero's `zot.everything(zot.children(parent_key))`,
which follows all pages. This is the same class of bug `#34` hardened on the
attachment-find path (it added `limit=200` to `_prune_prior_attachments`'s
`children()` call at line 158) but left the sync-note path here untouched.

Originally filed as PR #25 (2026.06.01); `#34`'s zotero-client refactor landed
first and made that branch conflict, and the un-paginated call was live on main
again. Re-applied here on current main with a regression test
(`tests/test_zotero_sync_note.py`) that mocks a sync-log note off page 1 and
asserts `everything()` surfaces it instead of creating a duplicate. PR #25 closed
as superseded.

## 2026.07.21 - Check attachment_simple return (silent-upload-failure guard)

pyzotero 1.11.0's `attachment_simple` returns `{'success','failure','unchanged'}`
and does NOT raise when the S3 upload/registration fails. `sync_to_zotero`
previously discarded that return and set `uploaded = packed` on no-exception,
then ran `_prune_prior_attachments` -- so a silently-failed upload DELETED the
prior good zips while storing nothing, leaving the Zotero item with ZERO
artifacts. Observed live: an entire Kuchel 5-chapter re-delivery pruned every
prior zip and uploaded none (ABS survived because it reads local stamped mp3s,
and `sync_projection` skips items with no zip, so no wipe). Fix: capture the
result and `assert result.get("success") or result.get("unchanged")` before the
prune (fail fast; prior versions survive on failure). Dropped the broad
`except Exception: return` so genuine upload errors also propagate loudly.
Regression: `tests/test_zotero_upload_guard.py` (no-success -> raises + no
`delete_item`; success -> proceeds to prune). NOTE the low-level uploader in
`scratchpad/zupload.py` was used one-off to repair the pruned Kuchel zips;
adopting it inside `sync_to_zotero` (replacing the flaky `attachment_simple`) is
a sensible follow-up.
