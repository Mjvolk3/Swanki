---
id: y6fda5zpnqgqjjycnm1rfh2
title: Test_segmenter
desc: ''
updated: 1773263539723
created: 1773263539723
---

## 2026.03.11 - Initial test suite for segmenter module

Eleven unit tests across four test classes covering all four segmenter functions: combine preserves images and returns correct page offsets; split respects newlines, falls back to spaces, handles short/empty content, returns correct char ranges, and preserves equations; write creates numbered files; and build_segment_to_page_map correctly identifies overlapping pages including single-page segments.
