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

## 2026.03.13 - Span-based LaTeX auto-wrap prevents pipeline crashes

LLM-generated cards with broken `$` delimiters (e.g. `$V_{i}^{\min}=$V_{i}^{\max}$=0$`) caused unwinnable retry loops. The bare expression `V_{i}^{\max}` sat between two `$` spans, and the old lookbehind/lookahead-based auto-wrap skipped it because `$` was adjacent -- even though it belonged to a different span. After 3 retries, pydantic-ai crashed the entire pipeline.

### Span-based auto-wrap

- Replaced `(?<!\$)`/`(?!\$)` lookbehind/lookahead with span-position checking: compute all `$...$` span intervals, only wrap expressions whose start position falls outside every span
- Extended subscript+superscript pattern to handle partially-braced forms: `V_{i}^\max`, `V_{i}^max` (not just `V_{i}^{\max}`)

### Validation auto-fixes instead of ValueError

- Bare math detected in validation (patterns 1-5: sub+super, sub-only, functions, equations, matrix ops, Greek letters) is now auto-wrapped in `$` instead of raising `ValueError`
- Only unbalanced braces inside existing `$...$` spans still raise errors (these cannot be fixed programmatically)
- Removed patterns 6 (Unicode Greek) and 7 (isolated capital letters) -- these had high false-positive rates and were causing unnecessary retries

## 2026.03.14 - Robust LaTeX brace auto-fix replaces crash-on-retry

The LaTeX brace validator was crashing the pipeline when LLMs generated patterns like `$\mathrm{IPP}}$` (excess braces) or `$N_{\mathrm{chem}$` (missing braces) that persisted through all 3 retries. Changed the final brace-balance check from raising `ValueError` to auto-fixing: strips excess closing braces (`depth < 0`) and appends missing ones (`depth > 0`). Both the early fix pass and the final validation pass now handle both directions. This unblocked merzbacherModelingHostPathway2025 and martiPredictionMetabolicDynamics2025 which were failing on `\mathrm{}` patterns.

## 2026.05.14 - LectureTranscriptFeedback gains bridge_quality + repeated_phrases dimensions

Two new fields plus a `@model_validator(mode="after")` that flips `done=False` when either dimension flags an issue. Both are defaulted (`bridge_quality=True`, `repeated_phrases=[]`) so existing four-kwarg construction in tests and call sites keeps working unchanged.

- `bridge_quality: bool` — Theme 12. Set to `False` by the lecture critic when any section after the first opens cold (no one-sentence bridge from the prior topic). The Hamming Ch 2 "space and time" pivot was the listener's reported failure mode.
- `repeated_phrases: list[str]` — Theme 5. Populated either by the LLM critic or by `swanki.audio._common.detect_repeated_phrases` (deterministic n-gram scanner) wired into `_refine_transcript`. Each entry is a verbatim 5+ word phrase that occurred 3+ times; the refiner gets the list as explicit feedback to vary.

The validator centralizes the gate: callers populate fields without also remembering to flip `done`. Pydantic 2 quirk recorded in the docstring — `model_copy(update=...)` does NOT re-run validators; callers wanting the validator to fire after a field update must use `model_validate(self.model_dump() | {...})`.
