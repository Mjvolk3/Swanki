---
id: joluv8aovvanvchzp4meheg
title: Zotero_paper_import
desc: ''
updated: 1772090361742
created: 1772090361742
---

## 2026.02.26 - Add Zotero paper import and preparation script

End-to-end automation for importing papers from Zotero into Swanki_Data. Given a citation key, the script downloads PDFs via the Zotero API, detects and removes reference pages, produces a `_clean.pdf`, and writes the swanki `.sh` runner script -- replacing a manual multi-step workflow.

- Pydantic models (`ZoteroConfig`, `DownloadResult`, `PrepareResult`) structure config and results
- `find_item_by_citation_key` splits camelCase keys into words for Zotero's AND-based search, with `qmode=everything` fallback
- Matches on BetterBibTeX `Citation Key:` in `extra` or Zotero 7 native `citationKey`
- `clean_pdf` detects references via regex on extracted text, cuts with `swanki-cut`, unites with `pdfunite`
- Handles optional SI PDFs (`_si.pdf`, `_SI.pdf`, `_si1.pdf`)
- CLI accepts multiple keys and `--download-only` flag
- Paired with `/zotero-paper-import` skill for conversational use

## 2026.03.08 - LLM-based page classification with regex fallback

Replace the simple references-only regex with a two-tier page classification system. When `OPENAI_API_KEY` is available, the LLM classifier (`pdf_classifier.classify_pdf`) labels every page and returns keep-ranges, cutting not just references but also acknowledgments, supporting information, and supplementary materials. Falls back to an expanded regex (`END_MATTER_PATTERNS`) when the LLM is unavailable. This enables cleaner PDFs for flashcard generation by removing all non-educational end-matter.

- `PrepareResult` now carries `keep_ranges: list[tuple[int, int]]` and `used_llm: bool` instead of a single `refs_page`
- `_get_keep_ranges()` dispatches to LLM or regex, with graceful `ImportError` fallback
- `pdf_classifier` is imported via `importlib.util` to avoid pulling in the full `swanki` dependency chain
- SI PDFs also go through the same classification pipeline

## 2026.03.12 - Multi-range PDF cutting and qpdf migration

Support keeping multiple non-contiguous page ranges in a single PDF -- needed for Nature and Cell papers where Extended Data figures or STAR Methods appear after references. Previously the regex fallback produced a single cut point at the first end-matter heading, discarding everything after it including valuable supplemental content.

- Replaced `swanki-cut` (broken due to `instructor` import chain) with `qpdf` for page extraction
- New `_classify_pages_regex()` walks pages with a state machine: enters cut zone on end-matter headings, exits on resume-educational headings, re-enters on tail-cut patterns
- `RESUME_EDUCATIONAL_PATTERNS` detects Extended Data, STAR Methods, Supplemental/Supplementary figures
- `TAIL_CUT_PATTERNS` detects Nature Portfolio reporting summaries appended by the publisher
- `END_MATTER_PATTERNS` expanded with Online content, Author contributions, Declaration/Competing interests
- `_labels_to_ranges()` converts per-page keep/cut labels into multi-range tuples for cutting

## 2026.03.14 - Fix attachment ordering and qpdf warning tolerance

Zotero can return PDF attachments in arbitrary order, causing the SI PDF to be saved as the main article and vice versa. Added `_is_main_article()` heuristic that inspects the attachment `title` and `filename` fields to sort the main article first. Also made `cut_pdf` tolerate qpdf exit code 3 (warnings with successful output), which some structurally imperfect PDFs trigger.

- `_is_main_article()` checks for "Full Text PDF" in title and SI indicators ("supplement", "moesm", "esm") in title/filename
- `get_pdf_attachments()` now sorts results so main article comes before supplementary PDFs
- `cut_pdf()` accepts exit code 3 (qpdf warnings) instead of raising `CalledProcessError`
