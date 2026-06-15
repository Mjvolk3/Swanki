---
id: bv3eou6b06gmqekax1gkcse
title: Document
desc: ''
updated: 1773333551247
created: 1773333551247
---

## 2026.03.12 - Strict model config and new ImageSummary fields

Added `model_config = ConfigDict(extra="forbid")` to both `ImageSummary` and `DocumentSummary`. Added `alt_text` and `context` fields to `ImageSummary` to capture image alt text and surrounding document context for richer card generation. Modernized type annotations (`Optional[X]` -> `X | None`, `List` -> `list`, `Dict` -> `dict`). Applied ruff formatting.

## 2026.05.31 - TableSummary model

Added `TableSummary` (returned by [[swanki.processing.table_processor]]): `page_stem`, `occurrence_idx` (page-order key), `caption` (verbatim when present), `summary` (generated one-sentence; `None` when a caption exists), `source_block`. A `summary` validator collapses to one sentence and caps at 40 words, because the table landmark is a navigational cue, not a content read. Plan: [[plan.reading-table-figure-landmarks.2026.05.31]].

## 2026.06.12

Added `ImageDescription` (a structured-output model with `perceptual` and `interpretive` fields) and a `perceptual: str | None` field on `ImageSummary`. One vision call now produces both descriptions: the perceptual half (only what is visually present, never the answer) is spoken on a card front so audio-only learners can picture the figure without it leaking the answer; the interpretive half is the existing takeaway summary. `perceptual` on `ImageSummary` defaults to `None` so records serialized before the split still deserialize (forward-only). See [[plan.two-field-image-descriptions-audio-only.2026.06.12]].
