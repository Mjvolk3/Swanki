---
id: ejhxz269g54x0xbnyorbbkn
title: Abs_clear_bookmarks
desc: ''
updated: 1779394449858
created: 1779394449858
---

## 2026.05.21 - Bulk-clear ABS bookmarks for the clear-and-remark loop

New helper supporting the active book-editing workflow: when a chapter is regenerated/replaced, ABS bookmarks do not auto-migrate (a bookmark is an absolute offset into the item's global multi-track timeline, so within-chapter marks become unsalvageable and later-chapter marks shift by the duration delta). Rather than migrate timestamps, we clear and re-mark on the fresh audio -- the durable address for an issue is the chunk text (content-match), not the timestamp.

- `clear_bookmarks(citation_key, dry_run=True)` reuses `get_bookmarks` + `_token` from `scripts/abs_bookmarks.py` and deletes via `DELETE /api/me/item/{id}/bookmark/{time}`.
- Dry-run by default (lists what would be deleted); `--yes` performs the deletion. CLI: `python -m scripts.abs_clear_bookmarks --citation-key <key> [--yes]`.
- Deletion is irreversible on ABS, so archive substantive bookmark notes to a dated note before a bulk clear (see `swanki.audio.hamming-bookmarks-archive.2026.05.21`).

## 2026.06.09 - Shim CLI; mechanism superseded by the windowed wipe

The clear-and-re-mark rationale stands; the implementation moved to
[[swanki.abs.bookmarks]] and gained the windowed wipe-on-replace default this
note anticipated: `--window START_S END_S` (repeatable) deletes only bookmarks
inside the replaced audio's item-global windows. Omit windows for the legacy
whole-item clear. Dry-run default and `--yes` survive unchanged.
