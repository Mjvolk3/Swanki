---
id: 4nwc1gf6jx7icivzed22r27
title: Cards
desc: ''
updated: 1773268780327
created: 1773268780327
---

## 2026.03.11 - Add si_balance field to LectureTranscriptFeedback and fix pre-existing lint issues

Added `si_balance: bool` field (default `True`) to `LectureTranscriptFeedback` for tracking whether SI content dominates a lecture section. This is part of Step 4 (lecture transcript refactor) of the major refactor sequence ([[plan.major-refactor-sequence.plan-0]]).

Also fixed two pre-existing ruff issues: removed unused `placeholder_patterns` variable in `validate_text_content`, changed docstring to raw string (`r"""`) on `LectureTranscriptFeedback` to satisfy D301. Added frontmatter and extended mypy overrides to cover `swanki.models.*`.

## 2026.03.12 - Fix LaTeX brace validation for split subscripts

Added auto-fix and validation for malformed LaTeX subscript braces (e.g. `W_{i}j}` -> `W_{ij}`) that were slipping through the self-refine loop. The existing regex fixers handled missing or orphaned braces but not the "split subscript" pattern where the brace closes too early.

- New regex catches `W_{i}j}` pattern and merges it into `W_{ij}`
- Added brace-balance check inside `$...$` spans that flags unbalanced braces as a `math_issues` error, triggering pydantic-ai retry

## 2026.03.13 - Auto-fix LaTeX issues instead of relying on LLM retries

LLM-generated cards had recurring LaTeX problems that the validator caught but the LLM could not fix within the 3-retry limit, causing pipeline crashes. Shifted strategy from validation-only to auto-fix-then-validate: programmatic fixes handle common patterns, validation remains as a safety net.

### Auto-fixes added (pre-validation)

- Double closing braces in subscripts: `_{ij}}` -> `_{ij}`
- Unbalanced braces inside `$...$` spans: append missing `}` (e.g. `$\sigma_{\mathrm{DNA}$` -> `$\sigma_{\mathrm{DNA}}$`)
- Bare subscript+superscript patterns wrapped in `$`: `V_{i}^{\max}` -> `$V_{i}^{\max}$`
- Bare subscript-only patterns wrapped in `$`: `L_{0}` -> `$L_{0}$`

### Validation improvements

- Extended brace-balance check to `\(...\)` delimiters (previously only `$...$`)
- Single math issue now triggers retry (removed pass-through that only logged a warning)
- Added 14 context words to Pattern 7 (isolated variable detection) for better coverage of mathematical prose
