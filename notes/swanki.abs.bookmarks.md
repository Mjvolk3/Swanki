---
id: 6ua8e24yga2dtqx7l744ita
title: Bookmarks
desc: ''
updated: 1781029342134
created: 1781029342134
---

## 2026.06.09 - Bookmark fetch + windowed wipe-on-replace default

Port of `scripts/abs_bookmarks.py` (history at [[scripts.abs_bookmarks]]) plus
the windowed wipe the clear-and-re-mark workflow was waiting for
([[scripts.abs_clear_bookmarks]], memory `feedback_abs_clear_and_remark`):
`clear_bookmarks(citation_key=..., windows=[(start_s, end_s), ...])` deletes
only bookmarks inside the item-global windows of replaced audio; everything
else survives. No windows = the legacy whole-item clear. Dry-run by default,
`--yes` to delete; deletion is irreversible -- archive bookmark notes first.

- Window math warning (the one place a wrong timeline silently deletes the
  wrong bookmarks): windows must come from the OLD (pre-restitch) chunk
  timeline, shifted by the durations of the ABS item's preceding audio files.
  `edit_chunk`'s returned window is NEW-timeline and per-file; never feed it
  to a wipe.
- `time_s` is the playhead when the note was SAVED (lags the issue by
  minutes): pad windows forward and dry-run first.

## 2026.06.12 - add_bookmark: swanki-attributed create (the outbound half)

`add_bookmark(content_key=..., time_s=..., note=...)` lets swanki leave
markers the user sees in Prologue — first use: pointing at the two CH04
`[break]`/`[long-break]` A/B spots from the 2026-06-10 listening-note batch
so the user knows where to listen. Notes are prefixed with `SWANKI_MARK`
(`🦢 swanki:`) so machine-left bookmarks are unmistakable next to the user's
own.

- **Time semantics are the inverse of the wipe:** the caller passes a
  FILE-LOCAL time for the content key; `file_offset_in_item` walks the item's
  `audioFiles` in track order (same cumulative walk as
  `chapters_from_audiofiles`) and shifts to item-global before POSTing.
  Created on every library item serving the file (one per projection);
  raises `LookupError` if none do.
- Final time is floored to a whole second so the eventual
  `delete_bookmark` hits the int-keyed DELETE endpoint
  ([[swanki.abs.client]] `bookmark_time_key`).
- For exact in-file times, read the measured `chunk_timeline.json` sidecar
  (chunk `offset_ms`), NOT a cumsum of chunk mp3 durations — the stitch
  inserts content-aware inter-chunk silence (~40s total on CH04).
