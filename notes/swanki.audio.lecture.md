---
id: 5919f28fc4494149b81400c
title: Lecture
desc: ''
updated: 1773142603440
created: 1773142603440
---

## 2026.03.10 - Educational lecture generation with semantic chunking and self-refinement

Extracted from monolithic audio module. Implements `chunk_by_headers` for semantic section splitting, `generate_and_validate_chunk` with per-section LLM critique, and an iterative refinement loop (`_refine_transcript`) targeting 50% of source length. Uses `instructor` for structured `LectureTranscriptFeedback` responses.

## 2026.03.11 - Lecture transcript refactor (Step 4)

Major overhaul addressing two problems: false mid-lecture conclusions when SI pages follow the main paper, and broken per-section word budgets causing excessively long lectures. Part of ([[plan.major-refactor-sequence.plan-0]]).

- **Length control refactor**: Removed `section_budget_words` / `section_max_words` params from `generate_and_validate_chunk()`. Critique prompt now checks quality only (LaTeX, citations, lists, tone). Length enforcement moved to `_refine_transcript()` via source-word ratio — injects length-reduction feedback when ratio > 0.7, logs warning when < 0.3. System prompt target changed to "40-60% of source manuscript length".
- **Broadened `chunk_by_headers()`**: Now matches unnumbered headers (`## Methods`, `## Results`) in addition to numbered (`## 1.0 Introduction`). Uses two regex patterns tried in order: numbered first, unnumbered fallback. Requires h2+ to avoid matching h1 titles.
- **SI splitting**: `generate_lecture_audio()` accepts `si_start_page` to split `markdown_files` into main and SI. Main content is chunked; SI is indexed separately.
- **SI indexing**: New `build_si_index()` parses SI content at markers (Extended Data Fig, Supplementary Fig, Table S, Methods headers) into a `dict[str, str]`. New `extract_relevant_si()` scans each main section for SI references and returns matched snippets with fuzzy key normalization.
- **SI enrichment**: Per-section SI snippets passed to `generate_and_validate_chunk()` via `si_reference_content` param, appended to user message. Single-pass path passes truncated SI directly. SI instructions appended to system prompt.
- **SI balance constraint**: When SI content is provided, critique prompt includes an SI BALANCE CHECK requiring at least 50% main paper coverage.

## 2026.03.12 - Migrate from instructor/OpenAI to pydantic-ai agents

Replaced dual-client pattern (`instructor.from_openai()` + `instructor.patch()`) with `lecture_critic_agent` and shared `text_agent` from `swanki.llm.agents`. Removed `openai_client` and `instructor_client` parameters from all functions. Three structured call sites now use `lecture_critic_agent.run_sync()` for critique and `text_agent.run_sync()` for generation/refinement. Critique-regenerate loop preserved identically. Part of Step 5 ([[plan.major-refactor-sequence.plan-0]]).
