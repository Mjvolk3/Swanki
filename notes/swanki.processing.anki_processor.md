---
id: qytur9zpslhrjz64krmav08
title: Anki Processor
desc: ''
updated: 1773013975831
created: 1773013975831
---

## 2026.03.08 - Extract card-processing functions to module level

Lift card parsing, formatting, and extraction logic out of `AnkiProcessor` methods into standalone module-level functions (`parse_tags`, `split_front_back`, `extract_cards`, `format_card_html`, `format_cloze_html`, etc.). This enables `ApkgExporter` to reuse the same parsing and HTML formatting without depending on AnkiConnect. The `AnkiProcessor` methods now delegate to these functions, preserving backward compatibility.

## 2026.03.12 - Type annotation modernization and ruff formatting

Replaced `typing` generics (`List`, `Dict`, `Tuple`, `Set`, `Optional`) with Python 3.10+ builtins (`list`, `dict`, `tuple`, `set`, `X | None`). Removed unused `json` import. Applied ruff formatting: double quotes, Google-style docstring headers (`Returns:` instead of `Returns`), line wrapping.
