---
id: adeac28210904270923c96e
title: Reading
desc: ''
updated: 1773142603440
created: 1773142603440
---

## 2026.03.10 - Full document reading with two-pass LLM processing

Extracted from monolithic audio module. Uses a two-pass approach: (1) `_humanize_latex` converts all LaTeX to natural text in 8000-token chunks, (2) LLM generates reading-optimized transcript in 3000-token chunks. Audio is chunked at a stricter 2000-char limit for quality.
