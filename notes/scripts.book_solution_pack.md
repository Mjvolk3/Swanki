---
id: odvb9iut147c5z3p12wbrqb
title: Book_solution_pack
desc: ''
updated: 1780075606458
created: 1780075606458
---

## 2026.05.29 - Pack a chapter when solutions live in a SEPARATE manual

Packs one chapter for solution_manual mode when the worked solutions are NOT back-of-book pages of the chapter's own source but live in a SEPARATE solution-manual PDF (Bishop-style). Concatenates an already-extracted chapter PDF (body + end-of-chapter Exercises, via `qpdf` slice) with the page slice of the separate solutions manual covering that chapter's solutions (via `pdfunite`). The slice should be the SMALLEST inclusive 1-indexed range covering this chapter — extra pages only inflate OCR cost and the LLM context window; neighboring chapters' blocks on a boundary page are tolerated because enumeration/pairing keys on book problem IDs.

Sibling of `scripts/schaum_chapter_pack.py`, which handles the other layout (solutions in back-of-book pages of the SAME source). The packed PDF is the input that [[swanki.pipeline.problem_set]] Stage 3 LLM content-pairing consumes, with the statement/solution boundary detected by `_partition_statement_solution_regions` (review heading detection broadened in [[swanki.pipeline.section_classifier]]).

