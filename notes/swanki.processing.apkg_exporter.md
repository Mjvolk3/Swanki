---
id: yo9ks4y8u3j0uhunotsxzcb
title: Apkg Exporter
desc: ''
updated: 1773144184343
created: 1773144184343
---

## 2026.05.05 - Per-card complementary audio not embedded in apkg

`_find_media` searched `base_dir` and its parents (up to 3 levels) but not immediate subdirectories. `prepare_for_anki` strips the directory prefix when converting `[audio-front](gen-md-complementary-audio/foo.mp3)` to `[sound:foo.mp3]`, so the apkg packager re-locates the file by basename alone. Per-card audio lives in `<output_dir>/gen-md-complementary-audio/`, which the original lookup never touched — every export quietly logged "0 media files" while the cards still carried `[sound:...]` references that pointed nowhere. Verified empirically against `_CH01_7`: 61 cards, 122 mp3s on disk, 0 in the apkg → re-export with the patched lookup gives 122 in the apkg and a 27 MB file.

Fix iterates `base_dir.iterdir()` between the direct-hit check and the parent-walk fallback. Two regression tests cover the new path: `test_find_media_searches_immediate_subdirectories` (direct unit test) and `test_media_bundling_resolves_subdirectory` (end-to-end apkg packaging via `[audio-front](subdir/...)` link form).
