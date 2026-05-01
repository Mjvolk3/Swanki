---
id: 1n02ce8fc2qh2pv5efje22p
title: Chapter Index
desc: Build, persist, and load chapter-index.yaml — numbered equations, figures, and theorems extracted from a chapter's cleaned markdown for cross-chapter reference resolution
updated: 1777607710601
created: 1777607710601
---

## 2026.04.26 - Initial implementation

Foundation extractor that pairs with solution-manual mode's reference resolver. Walks per-page cleaned markdown and emits a strongly-typed `ChapterIndex` containing:

- `NumberedEquation` — pulled by two patterns: trailing-paren form (`$$...$$ (1.2)`) and in-block tag form (`\tag{1.2}` inside a `$$...$$` block). Equations without an ID are not indexed (cross-references are by ID only).
- `NumberedFigure` — direct dotted-form regex on `![alt](url)\n+ Fig N.M:` blocks. Does NOT reuse `swanki.utils.content.extract_figure_captions` because that helper's `\d+[a-z]?` pattern only matches single-segment numbers, not the dotted `1.4` form Schaum's and Bishop use.
- `NumberedTheorem` — anchored regex matching `Theorem|Lemma|Proposition|Definition|Corollary` + dotted ID.

Persisted to `<output_dir>/chapter-index.yaml` for downstream solution-manual runs to consume via `solution_manual.chapter_indexes` config (cross-chapter resolution from prior runs).

In v1 the chapter-index emission only runs in `mode=full`. `mode=solution_manual` builds an in-memory index from the current run's content but does not persist it (the override path treats the entire input as problem-set content with no separate "chapter content" to index).
