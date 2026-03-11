---
id: t4435hi0hdk9yc9yul40jei
title: wip
desc: ''
updated: 1773239855577
created: 1773239855577
---
PydanticAI Migration — Work In Progress

Scratchpad for tracking fine-grained progress on [[plan.instructor-to-pydanticAI.plan-0]] (Step 5 of [[plan.major-refactor-sequence.plan-0]]).

## Prerequisites (Steps 1-4)

- [x] Step 1: Audio decoupling complete
- [ ] Step 2: Config refactor complete
- [ ] Step 3: Character segmentation complete
- [ ] Step 4: Lecture transcript refactor complete

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

### 0.1 Create `swanki/llm/` package

- [ ] Create `swanki/llm/__init__.py` with frontmatter
- [ ] Create `swanki/llm/client.py` with frontmatter
- [ ] Implement `create_openai_client(config) -> OpenAI`
- [ ] Implement `create_instructor_client(config) -> instructor.Instructor`
- [ ] Google-style docstrings on both functions
- [ ] Unit test: `tests/test_llm_client.py` — mock OpenAI, verify client creation

### 0.2 Replace all `OpenAI()` instantiations

- [ ] `pipeline/pipeline.py:145` — `self.instructor = create_instructor_client(config)`
- [ ] `pipeline/pipeline.py:2190` — `openai_client = create_openai_client(config)`
- [ ] `audio/lecture.py:527` — `instructor_client = create_instructor_client(config)`
- [ ] `audio/lecture.py:839` — `instructor_client = create_instructor_client(config)`
- [ ] `processing/image_processor.py` — `self.openai_client = create_openai_client(config)`
- [ ] `utils/pdf_classifier.py:80` — `client = create_instructor_client(config)`

### 0.3 Add provider config

- [ ] Add `provider: openai` to `swanki/conf/models/default.yaml`
- [ ] Verify: full pipeline still works identically (zero behavior change)

### 0.4 Quality gate

- [ ] `ruff check` + `ruff format` on touched files
- [ ] `mypy --strict` on `swanki/llm/`
- [ ] `pytest tests/ -x` passes
- [ ] Commit: "Centralize OpenAI client creation in swanki/llm/client.py"

---

## Phase 1: Migrate pdf_classifier.py (proof of concept)

### 1.1 Add pydantic-ai dependency

- [ ] Add `pydantic-ai` to `pyproject.toml` dependencies
- [ ] Keep `instructor` temporarily (still used elsewhere)
- [ ] `pip install -e .` in swanki conda env

### 1.2 Study pydanticAI patterns

- [ ] Read `/Users/michaelvolk/Documents/projects/pydantic-ai/pydantic_ai_slim/pydantic_ai/agent.py` — understand `Agent.__init__`, `run_sync`
- [ ] Read `/Users/michaelvolk/Documents/projects/pydantic-ai/pydantic_ai_slim/pydantic_ai/result.py` — understand output validation + retry
- [ ] Read `/Users/michaelvolk/Documents/projects/instructor/instructor/patch.py` — understand how instructor injects response_model
- [ ] Document key differences in this note (below in "Findings" section)

### 1.3 Migrate the call site

- [ ] Create `PDFCutPlan` agent in `swanki/llm/agents.py` (start the registry)
- [ ] Replace `instructor.from_openai(OpenAI())` → `pdf_classifier_agent.run_sync()`
- [ ] Map `response_model=PDFCutPlan` → `output_type=PDFCutPlan`
- [ ] Verify system prompt is passed correctly (static, module-level `SYSTEM_PROMPT`)
- [ ] Remove instructor import from `pdf_classifier.py`

### 1.4 Verify

- [ ] Run `swanki-cut` on a test PDF — output matches pre-migration
- [ ] `mypy --strict` on `pdf_classifier.py` and `swanki/llm/agents.py`
- [ ] Unit test: mock agent, verify `PDFCutPlan` output type
- [ ] Commit: "Migrate pdf_classifier to pydanticAI (proof of concept)"

---

## Phase 2: Migrate Audio Modules

### 2.1 `audio/summary.py` (simplest — 1 raw call)

- [ ] Create `summary_narrator_agent = Agent(..., output_type=str)` in `agents.py`
- [ ] Replace call site #20 (line 79)
- [ ] Remove `openai_client` parameter, accept model config instead
- [ ] Replace manual retry loop with agent `retries` param
- [ ] Verify: summary audio output matches pre-migration
- [ ] Unit test: mock agent

### 2.2 `audio/reading.py` (2 raw calls, 2-pass pipeline)

- [ ] Create `latex_humanizer_agent = Agent(..., output_type=str)` in `agents.py`
- [ ] Create `audio_optimizer_agent = Agent(..., output_type=str)` in `agents.py`
- [ ] Replace call site #18 (line 98) — reading transcript generation
- [ ] Replace call site #19 (line 257) — LaTeX humanization
- [ ] Replace manual retry loops with agent `retries` param
- [ ] Remove `openai_client` parameter
- [ ] Verify: reading audio output matches
- [ ] Unit tests: mock both agents

### 2.3 `audio/card.py` (2 raw calls + hardcoded model)

- [ ] Create `card_transcript_agent = Agent(..., output_type=str)` in `agents.py`
- [ ] Create `citation_humanizer_agent = Agent(..., output_type=str)` in `agents.py`
- [ ] Replace call site #16 (line 190) — card transcript generation
- [ ] Replace call site #17 (line 576) — citation humanization
- [ ] **Fix hardcoded `"gpt-4o-mini"`** at line 577 → use configured model from agent
- [ ] Replace manual retry loops with agent `retries` param
- [ ] Remove `client` / `openai_client` parameters
- [ ] Verify: card audio output matches
- [ ] Unit tests: mock both agents

### 2.4 `audio/lecture.py` (3 structured + 2 init sites)

This is the most complex audio module — dual-client pattern with critique loop.

- [ ] Create `lecture_generator_agent = Agent(..., output_type=str)` in `agents.py`
- [ ] Create `lecture_critic_agent = Agent(..., output_type=LectureTranscriptFeedback)` in `agents.py`
- [ ] Replace call site #11 (line 70) — `critique_transcript_chunks`
- [ ] Replace call site #12 (line 314) — `generate_and_validate_chunk` (dynamic prompt with section content)
- [ ] Replace call site #13 (line 851) — `_refine_transcript` critique
- [ ] Remove client init at line 527 (`instructor.from_openai`)
- [ ] Remove client init at line 839 (`instructor.patch`)
- [ ] **Critical**: verify critique → regenerate loop works identically
  - [ ] Read instructor retry behavior in `/Users/michaelvolk/Documents/projects/instructor/instructor/patch.py`
  - [ ] Read pydanticAI output_validator in `/Users/michaelvolk/Documents/projects/pydantic-ai/pydantic_ai_slim/pydantic_ai/agent.py`
  - [ ] Confirm: validation errors become conversation context for retry
- [ ] Handle `si_reference_content` param (from step 4) in agent call
- [ ] Handle `si_balance` field on `LectureTranscriptFeedback` (from step 4)
- [ ] Remove `openai_client` and `instructor_client` parameters from all functions
- [ ] Verify: lecture audio output matches
- [ ] Unit tests: mock both agents, test critique loop

### 2.5 Phase 2 quality gate

- [ ] `ruff check` + `ruff format` on all audio modules
- [ ] `mypy --strict` on `swanki/audio/`
- [ ] All existing audio tests pass: `pytest tests/test_audio_*.py -x`
- [ ] Commit: "Migrate audio modules from OpenAI/instructor to pydanticAI"

---

## Phase 3: Migrate pipeline.py (highest risk)

### 3.1 Create remaining agents in registry

- [ ] `card_gen_agent = Agent(..., output_type=CardGenerationResponse, retries=3)`
- [ ] `summary_agent = Agent(..., output_type=DocumentSummary, retries=3)`
- [ ] `card_feedback_agent = Agent(..., output_type=CardFeedback, retries=2)`
- [ ] `audio_feedback_agent = Agent(..., output_type=AudioTranscriptFeedback, retries=2)`
- [ ] `card_refiner_agent = Agent(..., output_type=CardGenerationResponse, retries=2)`
- [ ] `audio_refiner_agent = Agent(..., output_type=str)` — for `response_model=None` call
- [ ] Google-style docstrings on all agents

### 3.2 Migrate `generate_document_summary` (call site #1)

- [ ] Replace line 634 instructor call → `summary_agent.run_sync()`
- [ ] Static system prompt — pass as `system_prompt` param or agent-level
- [ ] Verify: `DocumentSummary` output matches

### 3.3 Migrate card generation calls (call sites #2-7)

These are the most numerous and use tenacity wrapping.

- [ ] Replace call site #2 (line 837) — regular cards with tenacity
- [ ] Replace call site #3 (line 924) — cloze cards with tenacity
- [ ] Replace call site #4 (line 1147) — image cards (dynamic prompt)
- [ ] Replace call site #5 (line 1458) — regular cards all-pages with tenacity
- [ ] Replace call site #6 (line 1544) — cloze cards all-pages with tenacity
- [ ] Replace call site #7 (line 1789) — image cards interleaved (dynamic prompt)
- [ ] **Tenacity decision**: use pydanticAI `retries` param for simple cases; preserve external tenacity wrapper for `retry_if_exception_type(ValidationError)` cases
- [ ] **Note**: method may be renamed to `_generate_cards_for_segment` by step 3 — use current name at time of execution
- [ ] Verify: card generation output matches

### 3.4 Migrate self-critic calls (call sites #8-10)

**This is the highest-risk sub-step.** The card feedback → refinement loop is core to output quality.

- [ ] Replace call site #8 (line 2752) — `_evaluate_cards` → `card_feedback_agent.run_sync()`
  - [ ] Tenacity: `stop_after_attempt(2)` + `wait_exponential` → evaluate if pydanticAI `retries=2` is sufficient
  - [ ] Verify: `CardFeedback` output (done, issues, recommendations) matches
- [ ] Replace call site #9 (line 2857) — `_refine_cards` → `card_refiner_agent.run_sync()`
  - [ ] Tenacity: `retry_if_exception_type(ValidationError)` — **must preserve this**
  - [ ] Dynamic system prompt (f-string with feedback) — pass as user_prompt or dynamic system_prompt
  - [ ] Verify: refined cards match quality
- [ ] Replace call site #10 (line 3008) — `_generate_audio_feedback` → `audio_feedback_agent.run_sync()`
  - [ ] Verify: `AudioTranscriptFeedback` output matches

### 3.5 Migrate raw text call (call site #15)

- [ ] Replace call site #15 (line 3091) — `_refine_audio_transcript` → `audio_refiner_agent.run_sync()`
- [ ] This was `response_model=None` — now `output_type=str`
- [ ] Verify: refined transcript text matches

### 3.6 Remove old client initialization

- [ ] Remove `self.instructor = instructor.patch(OpenAI())` at line 145
- [ ] Remove `OpenAI(api_key=...)` at line 2190
- [ ] Remove `import instructor` from pipeline.py
- [ ] Remove `from openai import OpenAI` from pipeline.py (if no other uses)
- [ ] Pipeline now receives agents from `swanki/llm/agents.py`

### 3.7 Phase 3 quality gate

- [ ] `ruff check` + `ruff format` on `pipeline.py`
- [ ] `mypy --strict` on `swanki/pipeline/`
- [ ] All existing tests pass: `pytest tests/ -x`
- [ ] Unit tests for agent interactions in pipeline (mock agents)
- [ ] Commit: "Migrate pipeline.py from instructor to pydanticAI (13 call sites)"

---

## Phase 4: Multi-Provider Configs and Cleanup

### 4.1 Add Anthropic model preset

- [ ] Create `swanki/conf/models/anthropic.yaml` with Claude model IDs
- [ ] Verify: `swanki ... models=anthropic` resolves correctly

### 4.2 Remove old dependencies

- [ ] Remove `instructor` from `pyproject.toml`
- [ ] Check if `tenacity` is still used anywhere — remove if not
- [ ] Check if `openai` is still needed (pydanticAI may depend on it) — keep if transitive
- [ ] `pip install -e .` — verify clean install

### 4.3 Update image_processor.py

- [ ] Replace call site #21 (line 400) — vision call
- [ ] **Note**: vision API differs between providers — may need provider-specific handling
- [ ] Create `image_summary_agent = Agent(..., output_type=str)` in `agents.py`
- [ ] Handle base64 image passing (OpenAI vs Anthropic format differences)

### 4.4 Final cleanup

- [ ] Remove all `import instructor` statements across codebase
- [ ] Remove all `from openai import OpenAI` that aren't needed
- [ ] Search for any remaining `OpenAI()` or `instructor` references
- [ ] Update `swanki/llm/client.py` — may simplify now that instructor is gone
- [ ] Update Sphinx docs for `swanki/llm/` module

### 4.5 Final quality gate

- [ ] `ruff check` + `ruff format` on entire `swanki/` package
- [ ] `mypy --strict` on entire `swanki/` package
- [ ] Full test suite passes: `pytest tests/ -x`
- [ ] Integration test (`@pytest.mark.llm`): at least one end-to-end agent call
- [ ] `grep -r "instructor" swanki/` returns nothing
- [ ] `grep -r "from openai import" swanki/` returns nothing (or only transitive)
- [ ] Commit: "Complete pydanticAI migration: remove instructor, add multi-provider support"

---

## Findings / Notes

_Space for recording discoveries during migration — differences between instructor and pydanticAI behavior, gotchas, decisions made._

### Retry behavior comparison

_TODO: Fill in after reading both codebases in Phase 1.2_

### Dynamic system prompt patterns

_TODO: Document how to handle f-string prompts in pydanticAI (system_prompt decorator vs inline)_

### Vision API differences

_TODO: Document OpenAI vs Anthropic vision call format differences_

---

## Progress Log

| Date | Phase | What was done | Blockers |
|------|-------|---------------|----------|
|------|-------|---------------|----------|
