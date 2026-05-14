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

## 2026.05.14 - humanize_chapter_slug for Theme 8 (chapter intro humanization)

`humanize_citation_key` rendered chapter content_keys like `hammingArtDoingScience2020_03_history-of-computers-hardware` as "Hamming, Art Doing Science, 2020, 03, history of computers hardware" — the listener heard "zero three" and reported (Theme 8) that chapter intros should read "Chapter 3: history of computers hardware" instead.

`humanize_chapter_slug(citation_key) -> str | None` is the additive helper. Match: `^(?P<base>[A-Za-z][A-Za-z0-9]+)_(?P<num>\d{1,3})_(?P<slug>[a-z][a-z0-9-]+)$`. Returns `f"Chapter {int(num)}: {slug.replace('-', ' ')}"` (drops leading zeros via `int()`) or `None` for non-chapter inputs so callers can fall back to `humanize_citation_key`. The `@` prefix is stripped to match the base helper's contract.

Wired into `swanki/audio/_common.py:generate_bookend_audio`: when the citation_key matches the chapter pattern AND `audio_type == "lecture"`, the announcement template becomes `"Chapter 3: history of computers hardware. From Hamming, Art Doing Science, 2020. <paper_title>."` instead of the prior `"Today's lecture is posted as: hammingArtDoingScience2020, 03, history of computers hardware."`. The "From <base>" segment is built by re-calling `humanize_citation_key(citation_key.split("_", 1)[0])` to humanize just the base. End-of-lecture announcement becomes "And with that we conclude Chapter 3: history of computers hardware."
