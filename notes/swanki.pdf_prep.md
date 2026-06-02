---
id: wv7sopnflm7w6uo3ic37da5v
title: Pdf Prep
desc: Pre-pipeline PDF input prep — chapter chop + (one or more, possibly non-contiguous) answer-key range concat into one packed PDF, pure-Python pypdf
updated: 1780443393199
created: 1780443393199
---

## 2026.06.02 - Initial implementation

`swanki/pdf_prep.py` is the library home for the chapter-chop + answer-key-concat step that previously lived only in the ad-hoc `scripts/schaum_chapter_pack.py`. Top-level sibling to [[swanki.cut]] (which also does PDF page surgery) — PDF prep is a pre-pipeline input-preparation concern, parallel to `cut`, not a `pipeline/` stage.

**API.** `pack_chapter(source_pdf, chapter_pages, answer_key_pages, output_pdf) -> int`. Page ranges are 1-based, inclusive (matching the source PDF's viewer/printed numbering). `answer_key_pages` accepts a single `(first, last)` tuple OR a list of them — answer keys spill across, or are split over, non-contiguous pages, so multiple ranges are appended in order after the chapter pages. Returns the packed page count. `_add_range` validates bounds and fails fast (`ValueError`) on a malformed or out-of-bounds range.

**Pure-Python `pypdf`, no subprocess.** The prior script shelled out to `qpdf` (page extraction) + `pdfunite` (concat). CI has `ffmpeg` but neither `qpdf` nor `pdfunite`, so a subprocess packer passes locally and silently fails CI. `pack_chapter` uses only `pypdf.PdfReader` / `PdfWriter` (`add_page` / `write`), which is pip-only and CI-safe. This drove the repo-wide migration off the deprecated `PyPDF2`: `pyproject.toml` now floors `pypdf>=4` (dropping bare `PyPDF2`) and the mypy override lists `pypdf` / `pypdf.*` for `ignore_missing_imports`. [[swanki.cut]] and the in-package importers (`swanki/ocr/mineru.py`, `swanki/processing/pdf_processor.py`, `swanki/utils/pdf_classifier.py`) were migrated to `pypdf` in lockstep — drop-in `PdfReader` / `PdfWriter`, no API changes — so `import swanki` stays sound against the new dependency floor. `scripts/zotero_paper_import.py` was deliberately left on its own import (out of scope; avoids widening the blast radius into the Zotero path).

**`scripts/schaum_chapter_pack.py` is now a thin shim** that re-exports `main` / `pack_chapter` from `swanki.pdf_prep` and forwards the original CLI flags unchanged (`--source` / `--chapter-pages` / `--answer-key-pages` / `--output`), so existing `.sh` and queue invocations keep working. `--answer-key-pages` is now repeatable (`action="append"`) for a non-contiguous key; a single occurrence is the common case and behaves exactly as before.

Tests: `tests/test_pdf_prep.py` builds blank in-memory PDFs and round-trips the page count for a single answer-key range, multiple non-contiguous ranges, an out-of-bounds range (raises), and parent-dir creation.
