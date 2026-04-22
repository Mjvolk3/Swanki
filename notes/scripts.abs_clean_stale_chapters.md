---
id: ulfv49cjnn0p0oxfitfsx1n
title: Abs_clean_stale_chapters
desc: ''
updated: 1776884682993
created: 1776884682993
---

## 2026.04.22 - Initial version

ABS's library scan updates a book's `audioFiles` when the folder contents change, but leaves the `chapters` JSON untouched. For a Swanki paper that is re-uploaded with a newer `{timestamp}-{hash}` filename, the scan produces one current audio file alongside stale chapter entries pointing at the old (now-deleted) filenames — Prologue then shows phantom chapters. The cron pipeline had no way to recover; deleting files with `rm` did not fix it.

This script is the cleanup. After each refresh cycle it:

- Queries the ABS SQLite DB for every book whose `chapters` is non-empty.
- Computes the set of current audio-file stems (filename without extension) from the book's `audioFiles` JSON.
- Compares each chapter `title` against that set. ABS names chapter titles after file stems, so a stem no longer present in `audioFiles` is a definitive signal that the chapter is stale.
- POSTs `{"chapters": []}` to `/api/items/:id/chapters` for each stale book. Using the API (not a direct SQLite write) ensures ABS's in-memory state updates atomically — no server restart required.

The subset check is tolerant of books with multiple intentional tracks: as long as every chapter title matches a current file stem, nothing is cleared. It triggers only when at least one chapter references a filename that no longer exists on disk.