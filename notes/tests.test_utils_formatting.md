---
id: j03exhfsr1ad89h0vf8zszx
title: Test_utils_formatting
desc: ''
updated: 1778743098696
created: 1778743098697
---

## 2026.05.14 - Initial: chapter-slug humanization (Theme 8)

Tests for `swanki.utils.formatting.humanize_chapter_slug` (NEW) and a regression guard for `humanize_citation_key` against chapter inputs.

- `humanize_chapter_slug` (7): two-digit `_03_` Hamming chapter, single-digit `_1_` no-padding, two-digit chapter number, non-chapter returns `None`, empty input returns `None`, missing chapter number returns `None`, `@`-prefix stripping.
- `humanize_citation_key` regression (2): chapter input still produces the legacy comma-joined format; base-only input ("hammingArtDoingScience2020") still produces "Hamming, Art Doing Science, 2020".

Pure-string tests; no ffmpeg dependency.
