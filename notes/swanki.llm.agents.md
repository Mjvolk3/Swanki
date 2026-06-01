---
id: vs9w1m3vz8uxghuz9g0poby
title: Agents
desc: ''
updated: 1773322227376
created: 1773322227376
---

## 2026.03.12 - Centralized pydantic-ai agent registry

Single module defining all pydantic-ai agents used across the codebase -- one agent per output type. Replaces the scattered `instructor.patch(OpenAI())` and `OpenAI()` instantiations that previously lived in each call site.

- 5 structured-output agents: `document_summary_agent`, `card_gen_agent`, `card_feedback_agent`, `audio_feedback_agent`, `lecture_critic_agent`
- 1 shared raw-text agent: `text_agent` (output_type=str, retries=3) used by all plain-text LLM calls
- `get_model_string(config)` helper builds `"provider:model"` strings from Hydra config dicts

Created as part of the instructor-to-pydantic-ai migration (Step 5 of [[plan.major-refactor-sequence.plan-0]]).

## 2026.04.26 - Solution-manual mode agents

Added 4 new structured-output agents for [[swanki.pipeline.problem_set]]:

- `problem_enumeration_agent` (output: `ProblemEnumerationResponse`, retries=3) — LLM-fallback enumeration when regex misses problems.
- `problem_pairing_agent` (output: `ProblemPairingResponse`, retries=2) — Stage-3 fallback in `pair_problems_across_pages` for problems whose solution markers don't match the regex (Bishop with un-tagged worked solutions).
- `card_plan_classifier_agent` (output: `CardPlanResponse`, retries=2) — reserved for future LLM-driven card-plan decisions; v1 uses heuristic-only.
- `problem_card_gen_agent` (output: `ProblemCardBatchResponse`, retries=3) — generates the actual problem-set cards per problem.

All four response types live in [[swanki.models.problem_set]] (NOT in `pipeline/problem_set.py`) so this file's imports don't cycle back through the pipeline module.

## 2026.04.26 - Section classifier agent for mode=full integrated routing

Added `section_classifier_agent: Agent[None, ClassificationResult]` (retries=2). Used as a low-confidence fallback by [[swanki.pipeline.section_classifier]]'s `classify_sections()` when the heading-driven pass can't disambiguate (e.g. PDFs without clean `## Heading` anchors). Imports `ClassificationResult` from [[swanki.models.sections]] — same pattern as the problem-set agents.


## 2026.05.21 - Glossary mode agents

Added two structured-output agents for [[swanki.pipeline.glossary]]: `glossary_enumeration_agent` (output `GlossaryEnumerationResponse`, retries=3) for LLM-assisted enumeration of definition units from OCR'd wordlist markdown, and `definition_card_gen_agent` (output `DefinitionCardBatchResponse`, retries=3) for batched per-term card generation. Both response types live in [[swanki.models.glossary]] so this module's imports don't cycle back through the pipeline package.

## 2026.05.30 - Register `chunk_edit_agent`

Added `chunk_edit_agent: Agent[None, ChunkEditResponse]` (retries=2) for
comment-driven single-chunk audio edits, consumed by
[[swanki.audio.comment_edit]] via `with_safety_retry`. `ChunkEditResponse`
lives in [[swanki.models.cards]]. Plan:
[[plan.swanki-comment-driven-chunk-edits.2026.05.30]].

## 2026.06.01 - card_correctness_agent

`card_correctness_agent: Agent[None, CardCorrectnessAssessment]` (`retries=3`), used by the post-generation correctness gate ([[swanki.pipeline.card_correctness]]) one call per card through `with_safety_retry`. Model resolved per-call via `get_model_string` (reuses `models.llm` = `gpt-5.5`, or a nullable `card_correctness_gate.model` override). `CardCorrectnessAssessment` lives in [[swanki.models.cards]]. Plan: [[plan.post-creation-llm-card-correctness-gate.2026.06.01]].
