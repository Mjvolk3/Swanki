---
id: zu4k1my40l53o2c9ns4ru5m
title: Formatting
desc: ''
updated: 1773333556998
created: 1773333556998
---

## 2026.03.12 - Type annotation modernization and ruff formatting

Replaced `typing.List` with `list`. Applied ruff formatting: double quotes, Google-style docstring headers, raw docstrings for backslash-containing functions. No behavioral changes.

## 2026.03.15 - Rewrite humanize_citation_key for proper TTS rendering

The old implementation produced unnatural output like "Bunne, How Build Virtual2024" -- year glued to last word, no comma separation, hyphenated authors broken. Rewrote with three fixes:

- **Year extraction**: Regex strips trailing 4-digit year before camelCase splitting, then re-adds it as a comma-separated segment. "bunneHowBuildVirtual2024" -> "Bunne, How Build Virtual, 2024".
- **Hyphenated author names**: Detects `lowercase-lowercase` pattern at start of key (e.g., "ahlmann-eltze", "moreno-paz", "espinel-rios") and preserves the hyphen while capitalizing each part. "Ahlmann-Eltze, Deep Learning Based Gene Perturbation, 2025".
- **"et al" handling**: "johnsonEtAl2022" now produces "Johnson et al, 2022" without extra comma before "et al".

Extracted `_split_camel_case()` helper for reuse across the author and title splitting paths. Also handles digit/letter boundaries ("50MCells" -> "50 M Cells").
