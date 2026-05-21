---
id: ocr0mineru0mod0001
title: mineru
desc: ''
updated: 1779300000000
created: 1779300000000
---

## 2026-05-21 — MinerU OCR via isolated subprocess + per-page splitter

`convert_pdf_mineru(pdf_path, output_base, ocr_config)` runs MinerU on the whole PDF once (one model load) via a subprocess into the isolated `swanki-mineru` conda env (Python 3.11, torch<2.11), then splits the flat output into `md-singles/page-N.md`.

Key decisions:

- **Subprocess, not in-process.** Swanki is Python 3.13; MinerU pins torch<2.11 and bundles a paddleocr fork, so it lives in a separate conda env invoked through `scripts/run_mineru_swanki.py`. The subprocess boundary also cleanly handles GPU pinning (`CUDA_VISIBLE_DEVICES`) and the HF_HOME-before-import ordering.
- **Fresh every run.** `mineru-raw/` is `rmtree`d each call — no idempotency short-circuit — until MinerU output proves stable (operator directive).
- **Lazy HF_HOME.** Resolved here from `models.ocr.hf_home` or `$SWANKI_DATA/models/mineru/hf_cache`, never via `${oc.env:...}` yaml interpolation, so the default Mathpix path never depends on `SWANKI_DATA` at Hydra compose time.
- **GPU 3.** Defaults `CUDA_VISIBLE_DEVICES=3` (the GPU freed from Fish by `scripts/free-gpu-for-mineru.sh`).
- **Page-split via `content_list.json`.** MinerU emits one flat `.md` with NO page markers; `split_content_list_to_pages` groups blocks by `page_idx`, renders text/heading/equation/image/table (skipping `header`/`footer`/`page_number`/etc.), copies images to `output_base/images/` so `ImageProcessor` resolves them, and backfills an empty `page-N.md` for every page in `1..num_pages` (count from `PdfReader`) to keep the per-page index 1:1 and contiguous with the source PDF — downstream stages index these positionally.

content_list.json schema is the documented MinerU 2.x pipeline-backend schema. See [[plan.transition-ocr-to-mineru-dual-path.2026.05.19]].

## 2026-05-21 — Validated against a real MinerU run (mineru 2.7.6)

Ran the runner on the 9-page Wigner paper (GPU 3, pipeline backend). Findings:

- Schema confirmed: `text` blocks carry `type`/`text`/`text_level`/`bbox`/`page_idx`; headings use `text_level`. All 9 pages present and contiguous (page_idx 0-8).
- **New block type `discarded`** — MinerU's own noise bucket (the reprint/copyright footer landed here). It was NOT in the documented schema and initially leaked into `page-1.md` via the fallback branch. Added `discarded` to `_SKIP_TYPES`; MinerU's own flat `.md` omits these too, so skipping aligns us with native output.
- **Per-page reconstruction is clean**: splitter output is byte-for-byte equivalent to MinerU's native flat `.md` (modulo trailing whitespace), so the `content_list.json` -> per-page approach is not lossy. The persistent-MinerU-server-per-page idea remains a viable future simplification for Mathpix-parity, but is not needed for output quality.
- This paper had no image/table/equation blocks (text-only); those branches remain covered by the hand-built unit fixture against the documented schema.
