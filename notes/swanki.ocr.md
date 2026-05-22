---
id: ocr0swanki0pkg0001
title: ocr
desc: ''
updated: 1779300000000
created: 1779300000000
---

## 2026-05-21 — New OCR package: dual-path dispatch (mathpix | mineru)

New `swanki/ocr/` package added to support a second OCR backend (MinerU) alongside Mathpix, selected by `models.ocr.provider` (default `mathpix`).

- `convert_to_markdown(provider, *, pages, pdf_path, output_base, ocr_config)` dispatches to `convert_pages_mathpix` or `convert_pdf_mineru`; raises `ValueError` for unknown providers.
- Dispatch mirrors the existing TTS provider switch in `pipeline.py` (string-branch on a config key, no Protocol/factory).
- Both providers return naturally-sorted `md-singles/page-N.md` paths so every downstream stage (cleaner, segmenter, classifier, image-card placement) is unchanged.

Rationale and full design history: [[plan.transition-ocr-to-mineru-dual-path.2026.05.19]].
Related: [[swanki.ocr.mathpix]], [[swanki.ocr.mineru]], [[scripts.run_mineru_swanki]].
