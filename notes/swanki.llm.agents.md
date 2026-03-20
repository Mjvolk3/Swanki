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
