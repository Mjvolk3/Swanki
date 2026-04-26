---
id: za0yc7jlyummfm4e65m5ko1
title: Swanki_abs_sync
desc: ''
updated: 1777166018068
created: 1777166018068
---

## 2026.04.25 - Replace stale per-paper mp3s on republish

Before: each republished audio file landed alongside the prior version because filenames embed `{timestamp}-{hash}` and the only existence check was "does this exact filename already exist." A Paper directory is supposed to hold exactly one mp3 per audio type; instead it accumulated old mp3s, and ABS surfaced each one as a separate chapter of the same book. Same failure mode for book chapters when a single `_CH##` was rerun.

`extract_audio` now scans the target directory before writing and unlinks any mp3 whose `(key, audio_type)` matches the incoming file. Different `key`s in the same dir (e.g. other chapters of a book) are left alone, so multi-chapter books still work. Companion script `scripts/abs_clean_stale_chapters.py` then drops the orphaned `chapters` metadata pointing at the deleted files.
