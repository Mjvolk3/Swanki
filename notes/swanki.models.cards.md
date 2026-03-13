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
