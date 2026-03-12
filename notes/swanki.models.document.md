---
id: bv3eou6b06gmqekax1gkcse
title: Document
desc: ''
updated: 1773333551247
created: 1773333551247
---

## 2026.03.12 - Strict model config and new ImageSummary fields

Added `model_config = ConfigDict(extra="forbid")` to both `ImageSummary` and `DocumentSummary`. Added `alt_text` and `context` fields to `ImageSummary` to capture image alt text and surrounding document context for richer card generation. Modernized type annotations (`Optional[X]` -> `X | None`, `List` -> `list`, `Dict` -> `dict`). Applied ruff formatting.
