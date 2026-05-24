---
id: skyzo28yjvb7aey5uo69c0p
title: Safety
desc: ''
updated: 1779602565866
created: 1779602565866
---

## 2026.05.24 - Generalized biosec-refusal retry wrapper

Lifts the lecture-only `_gen_with_safety_retry` (per
[[swanki.audio.lecture]] 2026.04.26) into a generic helper that works with any
pydantic-ai `Agent`. Motivated by the iCBF batch: `qu` (CRISPR) and `swanson`
(SARS-CoV-2 nanobody) both died at `card_gen_agent.run_sync` calls inside
`swanki/pipeline/pipeline.py`, where the prior helper couldn't be applied
because it was hardcoded to `text_agent` and returned `str`. With a
parametric agent + structured-output passthrough, the same educational-context
preamble pattern now unblocks card-generation, card-feedback, and card-refine
calls in addition to lecture sections.

**Module contents.**

- `SAFETY_REFUSAL_MARKERS` -- tuple of substrings (`"invalid_prompt"`,
  `"limited access to this content for safety"`). Callers can also import this
  to detect a terminal safety refusal after the helper re-raises (lecture.py
  uses this to convert the exception into the empty-string sentinel its flow
  expects).
- `EDU_CONTEXT_PREAMBLE` -- the canonical preamble injected on retry. Rewritten
  per user framing 2026.05.23: *"derived from an already-published,
  peer-reviewed scientific paper. There is no new information here; this is
  educational restatement of public literature only."* Generic across lecture
  / card / summary / reading paths.
- `with_safety_retry(agent, user_message, *, instructions, model,
  model_settings=None, max_safety_retries=2, label="")` -- generic. Re-raises
  on terminal failure so callers' existing try/except can decide whether to
  continue (per-image card branch in pipeline.py) or fall back to an
  empty-string sentinel (lecture.py).

**Why re-raise instead of always returning `""`?** Different callers want
different terminal behaviors. The image-card branch already has
`except Exception: ... continue`, so the helper raises and the caller skips
the image. The lecture per-section caller wants an empty string so downstream
can drop that section gracefully -- it wraps the helper in its own try/except
and converts safety exceptions to `""`. One source of truth for the preamble +
markers, two callers with different terminal contracts.

**Why parametric on agent (not hardcoded to one).** Structured-output agents
(`card_gen_agent` → `CardGenerationResponse`, `card_feedback_agent` →
`CardFeedback`, ...) all share the same `agent.run_sync(msg, instructions=,
model=, model_settings=)` signature. The helper just forwards through and
returns the `RunResult`; caller pulls `.output`. No type coupling.

See [[swanki.pipeline.pipeline]] (2026.05.24) for the six wrapped call sites
that unblock biology-content papers, and [[swanki.audio.lecture]] (2026.05.24)
for the refactor that makes lecture.py's helper a thin wrapper around this
shared one.
