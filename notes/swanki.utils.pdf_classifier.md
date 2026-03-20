---
id: a4fx5un94fxqguy7h5kpjvw
title: Pdf_classifier
desc: ''
updated: 1773321063249
created: 1773321063249
---

## 2026.03.12 - Migrate from instructor to pydantic-ai and add docstrings

Replaced `instructor.from_openai(OpenAI())` call with inline `Agent(output_type=PDFCutPlan, retries=3)` from pydantic-ai. Agent created inline in `classify_pdf()` rather than in the agent registry to avoid circular imports with `PDFCutPlan`. Added frontmatter docstring, class docstrings for `PageLabel` and `PDFCutPlan`, fixed ambiguous variable name (`l` to `line`). All ruff and mypy --strict errors resolved. Part of Step 5 ([[plan.major-refactor-sequence.plan-0]]).
