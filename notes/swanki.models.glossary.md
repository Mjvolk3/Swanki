---
id: glsmodelsglossary000001
title: Glossary Models
desc: Pydantic models for glossary mode — GlossaryUnit, DefinitionCardPlan, GlossaryTag, and the enumeration / card-batch response wrappers
updated: 1779321600000
created: 1779321600000
---

## 2026.05.21 - Initial implementation

Foundation models for `mode=glossary` (GRE wordlist definition cards), mirroring [[swanki.models.problem_set]]:

- `slugify_term` — lowercases, collapses non-alphanumeric runs to single hyphens, trims; produces the `[a-z0-9-]+` term slug used in the tag.
- `GlossaryUnit{term, definition, char_count}` — single-shape. Part-of-speech and multiple senses stay as prose inside `definition` (no per-sense fields), the same "LLM renders content, schema stays single-shape" decision as `ProblemUnit`.
- `DefinitionCardPlan{n_cards, include_main}` with a consistency `model_validator` (v1: always one card). Shape mirrors `CardPlan` so the future encyclopedia elaboration upgrade can extend it without restructuring callers.
- `GlossaryEnumerationResponse` / `DefinitionCardBatchResponse` live here (NOT in pipeline/glossary.py) so `llm/agents.py` can import the response types without cycling through the pipeline module — same reason as the problem-set response wrappers.
- `GlossaryTag` (`<citation_key>.glossary.<term_slug>`) — strict-regex parse/render round-trip mirroring `ProblemTag`. The coverage audit keys on a parsed term slug rather than fragile string ops.

See [[plan.glossary-definition-cards-gre-wordlist.2026.05.21]].
