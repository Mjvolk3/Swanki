---
id: omnb95lki75u83b71a3trlg
title: Presentation
desc: ''
updated: 1773789877267
created: 1773789877267
---

## 2026.03.17 - Add presentation generation package

New `swanki/presentation/` package for generating slide presentations from Swanki-processed paper data. Provides CLI (`swanki-present`) and programmatic API (`run()`). Loads document summaries, image summaries, and PDFs from `$SWANKI_DATA/{citation_key}/`, generates slide content via LLM (instructor + OpenAI), extracts/crops figures, and renders to Reveal.js HTML via pandoc.

- CLI entry point registered in `pyproject.toml` as `swanki-present`
- `_find_latest_version()` auto-discovers the highest numbered output directory
- `run()` orchestrates the full pipeline: spec -> LLM -> figures -> render
