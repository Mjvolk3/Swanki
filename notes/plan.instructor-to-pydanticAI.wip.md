---
id: t4435hi0hdk9yc9yul40jei
title: wip
desc: ''
updated: 1773239855577
created: 1773239855577
---
PydanticAI Migration — Work In Progress

Scratchpad for tracking fine-grained progress on [[plan.instructor-to-pydanticAI.plan-0]] (Step 5 of [[plan.major-refactor-sequence.plan-0]]).

**Status: COMPLETE** — All phases finished 2026-03-12.

## Prerequisites (Steps 1-4)

- [x] Step 1: Audio decoupling complete
- [x] Step 2: Config refactor complete
- [x] Step 3: Character segmentation complete
- [x] Step 4: Lecture transcript refactor complete

## Call Site Inventory (21 total)

### Structured output calls (instructor → pydanticAI Agent)

| #   | File                      | Line | Function                                | response_model              | Tenacity | System Prompt |
|-----|---------------------------|------|-----------------------------------------|-----------------------------|----------|---------------|
| 1   | `pipeline/pipeline.py`    | 634  | `generate_document_summary`             | `DocumentSummary`           | No       | Static        |
| 2   | `pipeline/pipeline.py`    | 837  | `_generate_cards_for_page_with_context` | `CardGenerationResponse`    | Yes      | Static        |
| 3   | `pipeline/pipeline.py`    | 924  | `_generate_cards_for_page_with_context` | `CardGenerationResponse`    | Yes      | Static        |
| 4   | `pipeline/pipeline.py`    | 1147 | `_generate_image_cards_for_page`        | `CardGenerationResponse`    | No       | Dynamic       |
| 5   | `pipeline/pipeline.py`    | 1458 | `_generate_cards_with_context_all`      | `CardGenerationResponse`    | Yes      | Static        |
| 6   | `pipeline/pipeline.py`    | 1544 | `_generate_cards_with_context_all`      | `CardGenerationResponse`    | Yes      | Static        |
| 7   | `pipeline/pipeline.py`    | 1789 | `_generate_image_cards_for_page`        | `CardGenerationResponse`    | No       | Dynamic       |
| 8   | `pipeline/pipeline.py`    | 2752 | `_evaluate_cards`                       | `CardFeedback`              | Yes      | Static        |
| 9   | `pipeline/pipeline.py`    | 2857 | `_refine_cards`                         | `CardGenerationResponse`    | Yes      | Dynamic       |
| 10  | `pipeline/pipeline.py`    | 3008 | `_generate_audio_feedback`              | `AudioTranscriptFeedback`   | No       | Static        |
| 11  | `audio/lecture.py`        | 70   | `critique_transcript_chunks`            | `LectureTranscriptFeedback` | No       | Static        |
| 12  | `audio/lecture.py`        | 314  | `generate_and_validate_chunk`           | `LectureTranscriptFeedback` | No       | Dynamic       |
| 13  | `audio/lecture.py`        | 851  | `_refine_transcript`                    | `LectureTranscriptFeedback` | No       | Static        |
| 14  | `utils/pdf_classifier.py` | 80   | `classify_pdf`                          | `PDFCutPlan`                | No       | Static        |

### Raw text calls (OpenAI client → pydanticAI Agent with output_type=str)

| #   | File                            | Line | Function                   | Retry            | System Prompt |
|-----|---------------------------------|------|----------------------------|------------------|---------------|
| 15  | `pipeline/pipeline.py`          | 3091 | `_refine_audio_transcript` | No               | Static        |
| 16  | `audio/card.py`                 | 190  | `generate_card_transcript` | Manual loop      | Static        |
| 17  | `audio/card.py`                 | 576  | `_humanize_citation`       | Manual loop      | Static        |
| 18  | `audio/reading.py`              | 98   | `generate_reading_audio`   | Manual loop      | Static        |
| 19  | `audio/reading.py`              | 257  | `_humanize_latex`          | Manual loop      | Static        |
| 20  | `audio/summary.py`              | 79   | `generate_summary_audio`   | Manual loop      | Static        |
| 21  | `processing/image_processor.py` | 400  | `_generate_image_summary`  | Manual + backoff | Dynamic       |

### Client initialization sites (removed after migration)

| File                   | Line | Pattern                           | Function                 |
|------------------------|------|-----------------------------------|--------------------------|
| `pipeline/pipeline.py` | 145  | `instructor.patch(OpenAI())`      | `__init__`               |
| `pipeline/pipeline.py` | 2190 | `OpenAI()` raw                    | `generate_audio`         |
| `audio/lecture.py`     | 527  | `instructor.from_openai()`        | `generate_lecture_audio` |
| `audio/lecture.py`     | 839  | `instructor.patch(openai_client)` | `_refine_transcript`     |

---

## Phase 0: Centralize Client Creation

- [x] Created `swanki/llm/__init__.py` and `swanki/llm/agents.py` (agent registry pattern instead of separate client module)

## Phase 1: Migrate pdf_classifier.py (proof of concept)

- [x] Added `pydantic-ai` to `pyproject.toml`
- [x] Created `PDFCutPlan` agent in registry
- [x] Migrated `classify_pdf` call site

## Phase 2: Migrate Audio Modules

- [x] `audio/summary.py` — 1 call site migrated
- [x] `audio/reading.py` — 2 call sites migrated
- [x] `audio/card.py` — 2 call sites migrated, hardcoded `gpt-4o-mini` fixed
- [x] `audio/lecture.py` — 3 structured call sites migrated, critique loop preserved

## Phase 3: Migrate pipeline.py

- [x] 6 agents created in registry for pipeline call sites
- [x] All 13 pipeline call sites migrated (#1-10, #15)
- [x] Self-critic feedback → refinement loop preserved
- [x] Old client initialization removed

## Phase 4: Multi-Provider Configs and Cleanup

- [x] Added `swanki/conf/models/anthropic.yaml` preset
- [x] Removed `instructor` and `tenacity` from dependencies
- [x] Migrated `image_processor.py` vision call (#21)
- [x] Cleaned all `import instructor` / `from openai import OpenAI` references
- [x] `ruff check` + `ruff format` clean
- [x] `mypy --strict` clean
- [x] All test mocks updated

---

## Progress Log

| Date       | Phase | What was done                                                            | Blockers |
|------------|-------|--------------------------------------------------------------------------|----------|
| 2026-03-12 | 0-4   | Complete migration: 6 agents, 21 call sites, deps removed, tests updated | None     |
