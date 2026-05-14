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

## 2026.03.12 - Update mocks for pydantic-ai migration

Updated test mocks from patching `instructor`/`OpenAI` clients to patching `swanki.audio.lecture.lecture_critic_agent.run_sync` and `swanki.audio.lecture.text_agent.run_sync`. Mock return values now use pydantic-ai `RunResult`-style objects with `.output` attribute.

## 2026.05.14 - LectureTranscriptFeedback validator coverage

Four tests for the `@model_validator(mode="after")` that flips `done=False` when bridge/repeated-phrase issues are populated. The default-construction test (`test_lecture_feedback_default_done_passes_through`) is the regression guard for existing call sites that construct with the original four kwargs — the new fields are defaulted so nothing breaks. The three flip tests cover the validator firing on `repeated_phrases` non-empty, `bridge_quality=False`, and the Pydantic 2 `model_validate(model.model_dump() | {...})` round-trip pattern that callers must use (because `model_copy(update=...)` does NOT re-run validators).
