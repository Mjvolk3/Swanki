---
id: 2jyv97zdg99272497i279k7
title: Schaum Chapter Pack
desc: Preprocessing helper — chops one chapter's pages and the specific back-of-book pages with that chapter's answer key, concatenates into a single PDF for solution_manual mode
updated: 1777607710601
created: 1777607710601
---

## 2026.04.26 - Initial implementation

CLI tool for assembling the input PDF that `mode=solution_manual` consumes. Wraps `qpdf` (page extraction) + `pdfunite` (concatenation) — both already used by `scripts/zotero_paper_import.py` and `swanki/cut.py`.

Convention: pass the **smallest** `--answer-key-pages` range covering only the target chapter's answers, NOT the entire back-of-book region. Other chapters' answers that share the same physical page are tolerated by the regex pairer (it keys on `^Chapter N`), but extra pages bloat OCR cost and LLM context for no benefit.

For Schaum's Microbiology (Alcamo, 2nd ed.) the per-chapter ranges are:

| Chapter | Pages | Answer key |
|---|---|---|
| Ch1 | 8-18 | 328-328 |
| Ch2+ | TBD | TBD |

First validated 2026.04.26 on Ch1 — packed PDF (12 pages) ran end-to-end through the swanki pipeline producing 31 cards + summary/lecture/reading audio + Zotero sync.
