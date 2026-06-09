---
id: yj4v1xvnx4vx7r33bjkdrfu
title: Abs
desc: ''
updated: 1781029289173
created: 1781029289173
---

## 2026.06.09 - ABS core module: one-pass consolidation of the scripts/ ABS layer

New package consolidating all Audiobookshelf logic that previously lived as ten
loosely-coupled files in `scripts/` (four HTTP stacks -- requests/httpx/urllib/
inline curl -- triplicated `resolve_library`/citation-key/token logic, four
scripts with no decision record). Per [[plan.abs-crud-core-module.2026.06.09]],
the migration is one-pass: `swanki/abs/` lands, three shims stay
(`scripts/abs_refresh.sh` for the 5-min cron + legacy publish scripts,
`scripts/abs_bookmarks.py` + `scripts/abs_clear_bookmarks.py` for the
audio-fix-from-annotations skill), and seven scripts are deleted in the same
commit (`swanki_abs_sync.py`, `abs_setup_libraries.py`,
`abs_setup_collections.py`, `abs_sync_zotero_collections.py`,
`abs_enrich_metadata.py`, `abs_clean_stale_chapters.py`,
`abs_set_chapter_titles.py`).

- Submodules: [[swanki.abs.client]] (one hardened httpx `ABSClient`),
  [[swanki.abs.projections]] (routing home), [[swanki.abs.sync]] (Zotero zip
  pull/extract), [[swanki.abs.libraries]], [[swanki.abs.collections]],
  [[swanki.abs.metadata]], [[swanki.abs.chapters]], [[swanki.abs.bookmarks]]
  (windowed wipe-on-replace default), [[swanki.abs.refresh]] (full + targeted),
  [[swanki.abs.__main__]] (CLI).
- The delivery subsystem stays a consumer: `AbsTarget` now calls
  `full_refresh(wait=True)` directly instead of subprocessing the bash script
  ([[swanki.delivery]]); `python -m swanki.delivery finalize-abs` and the SLURM
  finalizer are untouched.
