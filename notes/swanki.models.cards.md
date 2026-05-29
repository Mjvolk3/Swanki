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

## 2026.04.26 - card_subtype field on PlainCard

Added a `card_subtype: Literal[...]` discriminator field with default `"regular"` (preserves existing behavior — cloze and image are still inferred from content). Solution-manual mode sets explicit values: `"problem_main"`, `"subproblem"`, `"problem_overview"`, `"full_solution"`. Audit Part 3 in [[swanki.pipeline.problem_set]]'s `audit_coverage` keys on this field — the LLM defaults the value to `"regular"` if it omits the field, so `generate_cards_for_problem` stamps the right subtype from the CardPlan after the LLM call (trusts the plan, not the LLM).

`LongFormCardContent` and `FullSolutionCard` (the uncapped sibling classes for the optional full-solution problem-set card) are NOT yet shipped; they're gated by `enable_full_solution_cards: false` in `swanki/conf/pipeline/solution_manual.yaml`. Will land with the gap-filling provenance work.

## 2026.05.14 - LectureTranscriptFeedback gains bridge_quality + repeated_phrases dimensions

Two new fields plus a `@model_validator(mode="after")` that flips `done=False` when either dimension flags an issue. Both are defaulted (`bridge_quality=True`, `repeated_phrases=[]`) so existing four-kwarg construction in tests and call sites keeps working unchanged.

- `bridge_quality: bool` — Theme 12. Set to `False` by the lecture critic when any section after the first opens cold (no one-sentence bridge from the prior topic). The Hamming Ch 2 "space and time" pivot was the listener's reported failure mode.
- `repeated_phrases: list[str]` — Theme 5. Populated either by the LLM critic or by `swanki.audio._common.detect_repeated_phrases` (deterministic n-gram scanner) wired into `_refine_transcript`. Each entry is a verbatim 5+ word phrase that occurred 3+ times; the refiner gets the list as explicit feedback to vary.

The validator centralizes the gate: callers populate fields without also remembering to flip `done`. Pydantic 2 quirk recorded in the docstring — `model_copy(update=...)` does NOT re-run validators; callers wanting the validator to fire after a field update must use `model_validate(self.model_dump() | {...})`.

## 2026.05.19 - PlainCard.user_feedback for review-time triage channel

Added `user_feedback: str = Field("", description="User-authored feedback for review-time triage")` to `PlainCard`. Purpose: free-text channel the user fills in **inside Anki during review** (typically alongside marking + suspending a bad card). A future daily job will pull marked+suspended notes whose Feedback field is non-empty, write a triage report, and auto-open GitHub issues per card flagged for escalation (per the answered scope question — pipeline deferred, only the data plumbing landed in this change).

Naming intentionally diverges from the existing `CardFeedback` (LLM self-refine output): `user_feedback` is human, not LLM. Defaults to empty so every existing call site keeps working unchanged.

Round-trip: `to_md()` emits a single-line `<!-- user-feedback: TEXT -->` marker right before the tags line in all three branches (cloze, regular-with-audio, plain), only when non-empty. [[swanki.processing.anki_processor]] `extract_cards()` strips that marker out of the card body and surfaces the captured text on the dict so it never bleeds into Front/Back content during `prepare_for_anki`. Both Anki export paths ([[swanki.processing.apkg_exporter]] for .apkg and the AnkiConnect `send_cards_from_file` flow) write it to a new `Feedback` field (ord 2) on both the Basic and Cloze note types. Templates were NOT touched — the field is silent in review so cards render identically. The user just opens the editor mid-review, fills the field, marks, suspends.

Note-type schema change requires a one-time migration on any pre-existing Anki collection: `scripts/anki_add_feedback_field.py` calls AnkiConnect's `modelFieldAdd` for both Basic and Cloze, idempotent. Must run on the laptop (gilahyper has no Anki client per the `anki=default` rule). Without it, importing a newer .apkg on top of the old two-field model is brittle. Model IDs stay stable (seeds unchanged), so once migrated the imports drop in cleanly.

Daily-pull design (not implemented):
- AnkiConnect query: `tag:marked is:suspended Feedback:_*` (the `_*` matches any non-empty string).
- For each hit, produce one bullet in a dated Dendron triage note (front + back + feedback + tags + citation key parsed from the `@<key>:` prefix).
- For cards the user flags for escalation, call the `gh-issue` skill path to open a GitHub issue with the card content and feedback as the body. The triage report stays the source of truth; deletes/fixes are still hand-pulled, not auto-applied.

## 2026.05.29 - user_feedback marker on all three to_md branches (finalized)

Finalized state of the review-time triage channel (extends the 2026.05.19 design above). `PlainCard.user_feedback: str = Field("", ...)` now emits its `<!-- user-feedback: {text} -->` marker — only when non-empty, immediately before the tag line — in ALL THREE `to_md()` branches: Basic, Cloze, and the image-card branch. Keeping the marker on the image branch matters so feedback authored on an image card also round-trips (the earlier pass only covered the text branches in practice).

Distinct from `CardFeedback` (the LLM self-refine signal) — `user_feedback` is human-authored at review time. The matching extractor/strip and the `Feedback` field write live in [[swanki.processing.anki_processor]] (AnkiConnect path) and [[swanki.processing.apkg_exporter]] (.apkg path, field registered at ord 2 on both models); round-trip tests in [[tests.test_models_validation]] and [[tests.test_apkg_exporter]].

