---
id: m30e27m30p1rf577f4wzmdj
title: Abs_set_chapter_titles
desc: ''
updated: 1778775908852
created: 1778775908852
---

## 2026.05.14 - Initial: deterministic chapter titles after every refresh

ABS auto-derives chapter titles from filenames the first time it scans a multi-track audiobook, but it does NOT re-derive them when the file set changes. After a re-render the prior titles either (a) still match prefix-form and survive `abs_clean_stale_chapters`, or (b) get cleared, leaving the chapters JSON empty so the UI falls back to "Chapter 1" / "Chapter 2" auto-numbering. This script repopulates the array deterministically so the listener sees the canonical content_key (`hammingArtDoingScience2020_03_history-of-computers-hardware`) instead of "Chapter 3".

Naming rule: each chapter title is the audioFile filename minus swanki's `-{summary,reading,lecture}-<TS>-<hash>.<ext>` suffix. Matches the prefix-form `abs_clean_stale_chapters` preserves on subsequent runs, so re-renders leave titles unchanged.

`chapters_from_audiofiles` builds the array sorted by `index` with cumulative `start`/`end` from each file's `duration`. Sub-second drift is acceptable -- BookPlayer / Audiobookshelf only use chapter boundaries for navigation, not for transport accuracy.

Idempotent: skips books whose chapter titles already match the desired form (same length AND each title equal to the corresponding desired title in order). Wired into `scripts/abs_refresh.sh` as step 6/7, after `abs_clean_stale_chapters` (step 5) clears any stale titles and before the library scan (step 7). Posts via `POST /api/items/<id>/chapters` so DB + ABS in-memory state both update.

## 2026.05.14 - Bounds-aware idempotency check (catches stale chapter boundaries after re-render)

Bug surfaced after the Hamming v2 rerun: ABS UI showed Ch1 and Ch2 "grouped" — the displayed Ch1 marker ended 132.8s before the actual Ch01 mp3 ended (709.5s vs 842.3s), so Ch2's marker landed inside Ch01's audio. Root cause: the idempotency check in `find_books_needing_chapter_titles` compared length and titles only, NOT `start`/`end` boundaries. Audio durations changed across the v1->v2 re-render (different chunker, different TTS sampling) but titles stayed canonical, so the script skipped the re-set and stale boundaries persisted.

Fix: the check now also compares each chapter's `start` and `end` against the desired cumulative durations with a 0.5s tolerance (sub-second drift acceptable; the player only uses chapter boundaries for navigation, not transport accuracy). Per-book log line gains a "boundaries shifted" action label so this case is obvious in the run log going forward.

This pairs with the existing `abs_clean_stale_chapters` pattern: that script clears titles whose stem no longer prefix-matches any audioFile (catches removed/renamed files); this script then sets titles AND boundaries from the current audioFiles. Both run as steps 5 and 6 of `scripts/abs_refresh.sh`.
