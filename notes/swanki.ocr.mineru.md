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

## 2026-05-21 — Default flipped to mineru + luoWhenCausalInference2020 vs Mathpix comparison

Flipped `models.ocr.provider` to `mineru` in all 5 model configs (default.yaml + fish_speech*). The in-code fallback in `pipeline.py` stays `mathpix` (zero-dependency safe default if a config omits the ocr block); the shipped user-facing default is now mineru. Use `models.ocr.provider=mathpix` per-run for handwriting.

Ran MinerU on `luoWhenCausalInference2020` (2-page Nature methods paper, 4 equations + 1 figure) and compared per-page md to the prior Mathpix `md-singles/`:

- **Math delimiters:** MinerU `$...$` / `$$...$$`; Mathpix `\(...\)` / `\[...\]`. Equivalent content; both downstream-safe (markdown_cleaner already normalizes mathpix's, MinerU is already `$`).
- **Images (MinerU win):** MinerU extracts local `images/<hash>.jpg` (6 files, persistent/offline); Mathpix emits expiring `https://cdn.mathpix.com/cropped/...` URLs. This was the original motivation and it holds.
- **Structure:** Mathpix emits semantic LaTeX (`\title`, `\begin{abstract}`, `\author`, `\caption{}`); MinerU emits flat `#` markdown headings and captures the running journal header ("CAUSALITY IN MACHINE LEARNING") as an H1. MinerU keeps the figure-caption text but not as an attached `\caption{}`. Net: MinerU ~+230 words/page (running header + inline caption text).
- **OCR character accuracy (Mathpix win, minor):** MinerU intermittently drops ligatures / chars in the abstract font — "efciently" (efficiently), "woul" (would); earlier Wigner run had "EFFECTIVENSS". Mathpix rendered all correctly. Real but minor and intermittent; it would propagate into card text. Worth watching; the `discarded` cleanup already removes the worst noise.

Verdict: differences are acceptable for the default flip given the local-image and zero-cost wins; the ligature regression is the one thing to monitor on text-dense pages.
