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

## 2026.06.01 - Sync-log note pagination bug (85 duplicate notes)

`_find_or_create_sync_note` looked for the existing "Swanki Sync Log" note via `zot.children(parent_key)` — but bare `children()` returns only the FIRST PAGE (~25 items). Once a parent item accumulated enough children (attachments + the note itself), the existing log note fell off page 1, the find loop missed it, and every subsequent sync CREATED A NEW note. Observed on the Hamming book item (`DFL6A2YH`) after the 10-chapter CH regen: **85 "Swanki Sync Log" notes** instead of 1 — a self-reinforcing loop (more notes → note pushed further past page 1 → guaranteed miss).

Fix: paginate with `zot.everything(zot.children(parent_key))` so the find scans ALL children. (`_prune_prior_attachments` was unaffected — it already passes `limit=200`, enough to cover current item sizes; bump to `everything()` if any item ever exceeds 200 children.)

One-off cleanup: merged the 85 notes' unique log lines (196 entries) into the keeper note `99J7V2QC` and deleted the other 84; also deleted the 10 stale `_NN_slug` ZIPs left behind by the `_NN_`→`_CH##_` content_key rename (their `_chapter_base` differs from the new keys so prune never matched them). Item left clean: 1 sync note + 10 CH ZIPs + source PDF.

