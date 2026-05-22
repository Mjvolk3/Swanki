---
id: scripts0runmineru0001
title: run_mineru_swanki
desc: ''
updated: 1779300000000
created: 1779300000000
---

## 2026-05-21 — MinerU worker for the isolated swanki-mineru env

Stdlib-only CLI worker run under the `swanki-mineru` conda env, invoked as a subprocess by [[swanki.ocr.mineru]]. Adapted from iBioFoundry-AI's `run_mineru.py`.

- Defers `from mineru.cli.common import do_parse` until after `_ensure_hf_home()` — MinerU reads the HF cache path at import time, so HF_HOME must be set first.
- `_ensure_hf_home` falls back to `$SWANKI_DATA/models/mineru/hf_cache` (Swanki uses `SWANKI_DATA`, not iBioFoundry's `DATA_ROOT`).
- Flattens MinerU's nested `{scratch}/{stem}/auto/` tree to `--out-dir`: `{stem}.md`, `{stem}_content_list.json`, `{stem}_middle.json`, and `images/` (kept as `images/`, not `{stem}_images/`, so the relative `img_path` in content_list resolves directly in the splitter).
- Exit codes: 0 ok, 2 PDF missing, 3 no md produced, 4 HF_HOME underivable.

See [[plan.transition-ocr-to-mineru-dual-path.2026.05.19]].
