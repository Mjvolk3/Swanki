---
id: 46f4r51t6nhtefjiadck0qp
title: Chapters
desc: ''
updated: 1781029335527
created: 1781029335527
---

## 2026.06.09 - Stale-clean + canonical retitle, merged (two deleted scripts)

Merges the deleted `scripts/abs_clean_stale_chapters.py` and
`scripts/abs_set_chapter_titles.py` (histories at
[[scripts.abs_clean_stale_chapters]] / [[scripts.abs_set_chapter_titles]]) --
they shared the filename->content_key derivation. All their hard-won rules
carry over: the exact-or-`-`-suffixed-prefix stale test (manually-cleaned
titles survive cron cycles), cumulative per-file duration bounds with the 0.5s
drift tolerance (durations shift across re-renders without title changes; the
symptom was a chapter marker 130s short of its mp3), and the sqlite-read /
API-write split (a direct sqlite write leaves ABS serving stale in-memory
state until restart).

- New `fix_item_chapters(client, item_id)`: the per-item form for the targeted
  refresh -- reads audioFiles from the API (no sqlite), reposts canonical
  chapters only when titles/bounds differ. This is what keeps a republished
  chapter from pointing at a deleted file until the next full refresh.
