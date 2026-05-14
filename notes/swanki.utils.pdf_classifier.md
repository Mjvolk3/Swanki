---
id: a4fx5un94fxqguy7h5kpjvw
title: Pdf_classifier
desc: ''
updated: 1773321063249
created: 1773321063249
---

## 2026.03.12 - Migrate from instructor to pydantic-ai and add docstrings

Replaced `instructor.from_openai(OpenAI())` call with inline `Agent(output_type=PDFCutPlan, retries=3)` from pydantic-ai. Agent created inline in `classify_pdf()` rather than in the agent registry to avoid circular imports with `PDFCutPlan`. Added frontmatter docstring, class docstrings for `PageLabel` and `PDFCutPlan`, fixed ambiguous variable name (`l` to `line`). All ruff and mypy --strict errors resolved. Part of Step 5 ([[plan.major-refactor-sequence.plan-0]]).

## 2026.04.30 - Bump page classifier model to gpt-5.4-nano

Hardcoded model went from `openai:gpt-5-nano` (an unversioned alias retired by OpenAI) to `openai:gpt-5.4-nano-2026-03-17`. Same architectural slot — small/cheap classifier for per-page educational vs end-matter labelling — but the dated 5.4-nano gives reproducible behavior and is current in OpenAI's catalog. Companion bump in `swanki/conf/models/{default,fish_speech,fish_speech_audrey,fish_speech_hamming,fish_speech_bechtel}.yaml` moves the main LLM slot from `gpt-5.2-2025-12-11` to `gpt-5.4-2026-03-05`.
