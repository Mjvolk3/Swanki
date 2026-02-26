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
