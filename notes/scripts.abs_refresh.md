---
id: i9vupzberl2ulptgyeqkt12
title: Abs_refresh
desc: ''
updated: 1776884676530
created: 1776884676530
---

End-to-end refresh that projects Zotero state into the Audiobookshelf library: pull the latest mp3 zips per item, mirror Zotero collections, enrich metadata, clean up stale per-book artifacts, and force ABS to rescan. Held together by a `flock` so back-to-back cron invocations cannot trample each other.

## 2026.04.22 - Added stale-chapter cleanup as step 5/6

Extended from 5 to 6 steps. The new step `abs_clean_stale_chapters.py` runs between metadata enrichment and the final library scan. It exists because ABS's scan updates `audioFiles` when a book's folder changes but does NOT re-derive the `chapters` JSON, leaving Prologue showing phantom chapters that point at deleted filenames. Adding it here makes every refresh idempotent with respect to chapter metadata.

- Renumbered log lines from `step N/5` to `step N/6`.
- No other logic changes; the `flock` lock and `--no-verify`-free script structure stay as-is.
## 2026.05.14 - Add abs_set_chapter_titles as step 6/7

`abs_clean_stale_chapters` (step 5) clears chapter titles whose stem no longer prefix-matches any current audioFile. After a fresh re-render that clear leaves the chapters JSON empty, and the ABS UI falls back to auto-numbering ("Chapter 1", "Chapter 2", ...). New step 6 (`abs_set_chapter_titles.py`) repopulates the array deterministically from the current audioFile filenames, restoring the canonical content_key labels (e.g. `hammingArtDoingScience2020_03_history-of-computers-hardware`) before the library scan in step 7. Idempotent on books whose titles already match.
