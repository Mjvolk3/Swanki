---
id: 6qory1480sm0q1p4pr68bl5
title: Test_audio_lecture
desc: ''
updated: 1773270049648
created: 1773269920310
---

## 2026.03.11 - Add 11 tests for Step 4 lecture transcript refactor

Added tests covering all new functionality from Step 4 of the major refactor sequence ([[plan.major-refactor-sequence.plan-0]]):

- `test_chunk_by_headers_unnumbered` / `test_chunk_by_headers_mixed` — verify broadened header regex handles `## Methods` style and mixed numbered/unnumbered headers.
- `test_generate_and_validate_chunk_no_budget` — confirm chunk generation works without the removed budget params, using mocked OpenAI and instructor clients.
- `test_refine_transcript_length_enforcement` — verify ratio-based length feedback injection when transcript exceeds 70% of source words.
- `test_build_si_index_extended_data_figs` / `_supplementary_figs` / `_methods` / `_empty` — exercise SI marker parsing for Extended Data Figures, Supplementary Figures, Table S, Methods headers, and empty input.
- `test_extract_relevant_si_finds_reference` / `_no_references` / `_fuzzy_match` — test per-section SI reference lookup including fuzzy normalization of "Fig." vs "Figure".
