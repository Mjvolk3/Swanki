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
