---
id: u3azhzn887jolwka91ou2vf
title: plan-0
desc: ''
updated: 1773196349067
created: 1773153018677
---

## Problem

The codebase is 100% OpenAI-coupled in two distinct ways:

1. **Instructor-patched `OpenAI()`** — structured extraction (cards, summaries, feedback critique)
2. **Raw `OpenAI()` client** — free-form text generation (audio transcripts, image summaries, citation humanization)

Both must be addressed for multi-provider support (Anthropic Claude, etc.).

### Where OpenAI Is Hardcoded

| Location                            | Pattern                                       | Purpose                                       |
|-------------------------------------|-----------------------------------------------|-----------------------------------------------|
| `pipeline/pipeline.py:145`          | `instructor.patch(OpenAI())`                  | Card gen, summary, feedback                   |
| `pipeline/pipeline.py:2190`         | `OpenAI()` raw                                | Audio transcript generation                   |
| `audio/lecture.py:527`              | `instructor.from_openai()`                    | Lecture critique (structured)                 |
| `audio/lecture.py:273`              | raw `openai_client.chat.completions.create()` | Lecture transcript generation                 |
| `audio/card.py:190,576`             | raw `client.chat.completions.create()`        | Card audio transcripts, citation humanization |
| `audio/reading.py:98,257`           | raw `openai_client.chat.completions.create()` | Reading audio (2-pass)                        |
| `audio/summary.py:79`               | raw `openai_client.chat.completions.create()` | Summary narration                             |
| `processing/image_processor.py:119` | `OpenAI()` raw                                | Vision-based image summarization              |
| `utils/pdf_classifier.py:80`        | `instructor.from_openai(OpenAI())`            | Page classification                           |

**Note:** `card.py:577` hardcodes `"gpt-4o-mini"` for citation humanization — the only place a model name is hardcoded rather than configured via Hydra.

## Three Options

### Option A: Stay with instructor + add litellm

**Approach:** Use litellm as a drop-in replacement for the raw `OpenAI()` client, and use instructor's litellm integration for structured calls.

- litellm provides an OpenAI-compatible interface for 100+ providers
- instructor already supports `instructor.from_litellm(completion)`
- Raw calls: `litellm.completion()` has the same signature as `openai.chat.completions.create()`
- Model names become `"anthropic/claude-sonnet-4-20250514"`, `"openai/gpt-5"`, etc.

**Pros:**

- Minimal code restructuring — same call patterns, just swap client creation
- Per-call `response_model` stays first-class
- Per-call tenacity `Retrying` objects still work
- `response_model=None` still works (it's just a raw litellm call)
- Smallest migration effort

**Cons:**

- litellm is a large dependency with many transitive deps
- litellm is a third-party translation layer — adds a point of failure
- Provider-specific features (like Anthropic's extended thinking) harder to access

### Option B: Migrate to pydanticAI

**Approach:** Replace both instructor and raw OpenAI calls with pydanticAI `Agent` objects.

**Pros:**

- Native multi-provider support (OpenAI, Anthropic, Gemini, etc.)
- Maintained by the Pydantic team — tight Pydantic v2 integration
- Built-in observability via Logfire
- Growing ecosystem, likely to become the standard

**Cons:**

- Agent-oriented design doesn't fit Swanki's stateless extraction pattern
- Need 6+ separate `Agent` instances (one per `response_model`)
- Per-call tenacity retry strategies lost — only integer retries or transport-level config
- `response_model=None` (raw text output, used in pipeline.py:3094) has no equivalent
- Dual-client pattern in lecture.py (raw for generation, instructor for critique) becomes awkward
- 13+ call sites across 3 files to restructure
- Async-first design, Swanki is synchronous

### Option C: Thin abstraction layer (DIY)

**Approach:** Create `swanki/llm/client.py` with a factory that returns a provider-appropriate client based on Hydra config. Keep instructor for structured calls.

```python
# swanki/llm/client.py
def create_client(provider: str, api_key: str) -> OpenAI | Anthropic:
    ...

def create_instructor_client(provider: str, api_key: str) -> instructor.Instructor:
    ...
```

**Pros:**

- Full control, no extra dependencies
- Can use each provider's native SDK features
- Can be as thin or thick as needed

**Cons:**

- Must maintain provider-specific code paths
- Each new provider requires manual integration
- Vision API differences between providers are non-trivial

## Decision: Migrate to pydanticAI (Option B)

We are familiar with pydanticAI and want multi-provider support (Anthropic Claude, etc.). The agent-oriented design concerns are manageable — pydanticAI agents can be used as lightweight structured-output extractors without full agent workflows.

## Migration Risk: Self-Critic and Retry Mechanisms

The highest-risk area of this migration is faithfully replicating instructor's self-critic/refinement patterns in pydanticAI. Swanki relies heavily on these — card feedback loops, lecture transcript critique, audio transcript validation — and subtle behavioral differences could degrade output quality silently.

To mitigate this, we have cloned both libraries locally as reference:

- **instructor**: `/Users/michaelvolk/Documents/projects/instructor`
- **pydantic-ai**: `/Users/michaelvolk/Documents/projects/pydantic-ai`

During migration, consult these repos directly to understand:

1. **Retry + validation loops** — how instructor's `max_retries` with `response_model` validation triggers re-prompting vs how pydanticAI's `retries` param and `output_validator` decorator work. Instructor re-sends the validation error as a follow-up message; confirm pydanticAI does the same.
2. **Self-critique pattern** — instructor's `response_model` validation errors become part of the conversation context for the retry. In pydanticAI, use `@agent.output_validator` to replicate this. Read `pydantic_ai_slim/pydantic_ai/agent.py` and `pydantic_ai_slim/pydantic_ai/result.py` for the retry mechanics.
3. **Structured output enforcement** — instructor patches the OpenAI client to inject JSON schema into the API call. PydanticAI uses its own output parsing. Compare failure modes (malformed JSON, partial responses, schema violations).
4. **Tenacity integration** — some Swanki calls wrap instructor calls in tenacity `Retrying` objects with custom wait/stop strategies. PydanticAI only supports integer retries natively. Determine which calls need external tenacity wrapping preserved.

For each migrated call site, verify that the retry/validation behavior matches by comparing outputs on the same input before and after migration.

## Addressing the Cons

| Concern                          | Solution                                                                                           |
|----------------------------------|----------------------------------------------------------------------------------------------------|
| 6+ Agent instances needed        | Define them in a central `swanki/llm/agents.py` — one agent per output type is clean separation    |
| Per-call tenacity retries lost   | Use pydanticAI's `retries` param (integer) + wrap critical calls with external tenacity if needed  |
| `response_model=None` (raw text) | Use `Agent` with `output_type=str` — pydanticAI supports plain string output                       |
| Dual-client in lecture.py        | Two agents: `Agent[..., str]` for generation, `Agent[..., LectureTranscriptFeedback]` for critique |
| Async-first design               | pydanticAI provides `agent.run_sync()` for synchronous usage                                       |

## Migration Plan

### Phase 0 — Centralize client creation (no library change)

Create `swanki/llm/client.py` to centralize all `OpenAI()` instantiation. All files import from this module. Add `provider` field to Hydra models config. Zero behavior change — just preparation.

**Files to modify:**

- `swanki/pipeline/pipeline.py` — replace `OpenAI()` at lines 145, 2190
- `swanki/audio/lecture.py` — replace `instructor.from_openai()` at line 527
- `swanki/utils/pdf_classifier.py` — replace `instructor.from_openai(OpenAI())` at line 80
- `swanki/processing/image_processor.py` — replace `OpenAI()` at line 119
- `.swanki_config/models/default.yaml` — add `provider: openai`

**New files:**

- `swanki/llm/__init__.py`
- `swanki/llm/client.py`

### Phase 1 — Migrate pdf_classifier.py (lowest risk, 1 call site)

Replace the single instructor call in `classify_pdf()` with a pydanticAI agent. This is the proof-of-concept phase.

```python
from pydantic_ai import Agent

pdf_classifier_agent = Agent(
    "openai:gpt-5",
    output_type=PDFCutPlan,
    retries=2,
    system_prompt="...",
)

result = pdf_classifier_agent.run_sync(user_prompt)
plan = result.output
```

**Files to modify:**

- `swanki/utils/pdf_classifier.py`
- `pyproject.toml` — add `pydantic-ai`, keep `instructor` temporarily

### Phase 2 — Migrate audio modules (medium risk)

Replace raw `OpenAI()` and instructor calls in audio modules:

- `swanki/audio/lecture.py` — dual-client becomes two agents:
  - `lecture_generator = Agent("openai:gpt-5", output_type=str)` for transcript generation
  - `lecture_critic = Agent("openai:gpt-5", output_type=LectureTranscriptFeedback)` for critique

- `swanki/audio/card.py` — raw OpenAI calls become:
  - `card_transcript_agent = Agent(..., output_type=str)` for transcript generation
  - `citation_agent = Agent(..., output_type=str)` for citation humanization
  - Fix hardcoded `"gpt-4o-mini"` → use configured model

- `swanki/audio/reading.py` — two-pass LLM becomes two agents:
  - `latex_humanizer = Agent(..., output_type=str)` for pass 1
  - `audio_optimizer = Agent(..., output_type=str)` for pass 2

- `swanki/audio/summary.py` — single raw call becomes one agent

### Phase 3 — Migrate pipeline.py (highest risk, 13+ call sites)

Replace all instructor calls in the main pipeline:

- `CardGenerationResponse` extraction (multiple call sites with different retry configs)
- `DocumentSummary` extraction
- `CardFeedback` critique calls
- `AudioTranscriptFeedback` calls
- The `response_model=None` call at line 3094 → `Agent[..., str]`

Define all agents in `swanki/llm/agents.py`:

```python
card_gen_agent = Agent("openai:gpt-5", output_type=CardGenerationResponse, retries=3)
summary_agent = Agent("openai:gpt-5", output_type=DocumentSummary, retries=3)
card_feedback_agent = Agent("openai:gpt-5", output_type=CardFeedback, retries=2)
audio_feedback_agent = Agent("openai:gpt-5", output_type=AudioTranscriptFeedback, retries=2)
```

### Phase 4 — Multi-provider configs and cleanup

- Add Anthropic model config preset to `.swanki_config/models/`
- Remove `instructor` dependency from `pyproject.toml`
- Remove tenacity dependency if no longer used elsewhere
- Test full pipeline with both OpenAI and Anthropic models

## Agent Registry Design

All agents live in `swanki/llm/agents.py`. The model is configured at runtime from Hydra config:

```python
# swanki/llm/agents.py
from pydantic_ai import Agent
from swanki.models.cards import CardGenerationResponse, CardFeedback
from swanki.models.pipeline import DocumentSummary

card_gen_agent = Agent(
    "openai:gpt-5",
    output_type=CardGenerationResponse,
    retries=3,
)

# At call time, override model from Hydra config:
result = card_gen_agent.run_sync(
    user_prompt,
    model="anthropic:claude-sonnet-4-20250514",
)
```

## Sequencing Note (see [[plan.major-refactor-sequence.plan-0]])

This is **step 5** (final) of the major refactor sequence.

### Adjustments from prior steps

- All `.swanki_config/` references become `swanki/conf/` (config refactor completed in step 2)
- `swanki/conf/models/default.yaml` is where `provider: openai` gets added (Phase 0)
- Anthropic model preset goes to `swanki/conf/models/anthropic.yaml`
- Card generation method is now `_generate_cards_for_segment()` (renamed in step 3) — agent calls must use this name
- `lecture.py` now has additional functions from step 4: `build_si_index()`, `extract_relevant_si()`, `generate_and_validate_chunk()` has `si_reference_content` param — all LLM calls in these functions must also be migrated
- `LectureTranscriptFeedback` now has `si_balance` field (added in step 4) — the lecture critic agent must handle it
- Phase 2 agent count increases: lecture module now has 2 generation agents + 1 critic (was 1+1), plus the new SI-aware prompt patterns

### Quality gates for this step

- All new/modified code must pass `mypy --strict` on touched files
- Google-style docstrings on all functions in `swanki/llm/agents.py`, `swanki/llm/client.py`
- Frontmatter header blocks on new files per project conventions
- Frontmatter updated via `/update-py-notes` for all touched `.py` files
- Unit tests for agent registry (mock pydanticAI agents, verify correct output types)
- Unit tests for client factory (verify correct provider instantiation)
- Integration tests with `@pytest.mark.llm` for at least one end-to-end agent call
- Sphinx docs updated for new `swanki/llm/` module, `provider` config option
- `ruff check` and `ruff format` pass
- Verify `instructor` and `tenacity` fully removed from `pyproject.toml`

## Open Questions

1. Which Anthropic models to target? Claude Sonnet for cost-efficiency, Opus for quality?
2. Should TTS also be multi-provider? Currently ElevenLabs only, but OpenAI TTS config exists.
3. How to handle vision (image summarization)? Anthropic vision API differs from OpenAI's.
4. pydanticAI model string format — confirm exact model ID format for Hydra configs.
5. Dynamic system prompts — many prompts are built inline with f-strings containing page content, word counts, etc. Need to use pydanticAI's `system_prompt` decorator with dynamic deps or pass as `user_prompt` content.
