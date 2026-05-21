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

content_list.json schema is the documented MinerU 2.x pipeline-backend schema; capture a real run during rollout to confirm. See [[plan.transition-ocr-to-mineru-dual-path.2026.05.19]].
