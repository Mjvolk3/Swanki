---
id: ocr0mathpix0mod0001
title: mathpix
desc: ''
updated: 1779300000000
created: 1779300000000
---

## 2026-05-21 — Mathpix per-page OCR extracted from pipeline

`convert_pages_mathpix(pages, output_base)` is the Mathpix path, extracted verbatim from the old `Pipeline.convert_to_markdown` per-page loop.

- Switched from `os.system` to `subprocess.run(["script", "-qc", "mpx convert ...", "/dev/null"])` so we capture stderr and check a real `returncode` (the `script -qc` pseudo-TTY satisfies mpx's `process.stdout.clearLine()` requirement documented in CLAUDE.md).
- Warn-and-continue per failed page; `RuntimeError` only if zero pages convert. Behavior is otherwise equivalent to the legacy loop so `provider=mathpix` (default) runs are unaffected.
- Imports `_natural_sort_key` from `swanki.processing.markdown_cleaner` (its true definition site) — NOT from `pipeline.py` — to avoid a circular import.

See [[plan.transition-ocr-to-mineru-dual-path.2026.05.19]].
