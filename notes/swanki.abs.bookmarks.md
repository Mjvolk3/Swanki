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
