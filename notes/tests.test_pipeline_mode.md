---
id: 0zsp6pl5ue3ndhnkdt6cqj0
title: Test_pipeline_mode
desc: ''
updated: 1773243583496
created: 1773243583496
---

## 2026.03.11 - Initial test suite for audio_only pipeline mode

Six unit tests covering the `mode=audio_only` branch in `process_full()` and the cards guard in `generate_audio()`. Tests mock all heavy pipeline methods (LLM calls, PDF split, markdown conversion) and verify that card generation stages are skipped while shared stages still run.

## 2026.03.11 - Update mock for segment rename

Updated mock fixture to reference `_generate_cards_for_segment` (renamed from `_generate_cards_for_page_with_context` in the segmentation refactor).

## 2026.03.12 - Remove OpenAI client mock for pydantic-ai migration

Removed `mock_openai_client` from the test fixture since the pipeline no longer initializes an OpenAI client directly. Pipeline tests now only mock pipeline methods, not LLM clients.
