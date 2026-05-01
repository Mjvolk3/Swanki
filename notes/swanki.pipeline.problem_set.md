---
id: fdrhn9xj7mabuv9r5olalvz
title: Problem Set Pipeline
desc: Solution-manual mode core — enumerate, pair, resolve refs, generate cards, audit coverage. Used by mode=solution_manual override and (future) classifier-driven mode=full per-section routing.
updated: 1777607710601
created: 1777607710601
---

## 2026.04.26 - Initial implementation

Foundation module for `mode=solution_manual` (whole-document override path). Six top-level functions:

1. **`enumerate_problems`** — regex-first, pulls `^\d+\.\d+\b` blocks from cleaned markdown, splits each into statement (first paragraph) + solution (rest). LLM fallback (`problem_enumeration_agent`) is wired but not yet exercised; v1 relies on regex.
2. **`pair_problems_across_pages`** — three-stage pairing:
   - **Stage 0:** initialize one `ProblemPairing(statement, solutions=[])` per enumerated problem. Stage 0 guarantees `len(pairings.pairings) == len(problems)` so audit Part 1 is meaningful.
   - **Stage 1:** lift inline solutions (Schaum's `1.1` Q&A) into the pairing.
   - **Stage 2:** regex on `^Solution\s+N\.M` and `^Chapter\s+N\s*\nMultiple Choice` back-of-book blocks.
   - **Stage 3:** wired (`problem_pairing_agent`) but not yet exercised — reserved for Bishop with worked-solutions PDFs that lack explicit `Solution N.M` markers.
3. **`resolve_references`** — inlines `equation (X.Y)` / `Theorem X.Y` text from `ChapterIndex` into problem.statement and problem.solution. Collects `Figure X.Y` references into `problem.referenced_figures` for image attachment on cards.
4. **`classify_card_plan`** — heuristic-only in v1 (no LLM). Subproblem-driven (`(a)/(b)/(c)` parts) → 1 main + N subs (capped at 3). Long single-part problems (`char_count > long_problem_chars`, default 4000) → 2 cards (main + overview). Else → 1 main card.
5. **`generate_cards_for_problem`** — calls `problem_card_gen_agent`. Stamps `card_subtype` from the plan in order (the LLM defaults to `"regular"` in `PlainCard`, so trusting the plan is more robust than trusting the LLM). Appends the canonical `<citation_key>.problem.<id>` tag (audit Part 3 keys on it via `ProblemTag.parse`). Honors `enable_full_solution_cards` flag (downgrades the plan if disabled, default off).
6. **`audit_coverage`** — three-part hard-fail before APKG export:
   - **Part 1:** every enumerated problem appears in `pairings.pairings`.
   - **Part 2:** every pairing has ≥1 solution unless `allow_unsolved=True` (default False — zero tolerance).
   - **Part 3:** exactly one `card_subtype="problem_main"` card per paired problem, parsed via `ProblemTag` (catches missing, extra, AND duplicate via `Counter`).
7. **`run_solution_manual_override`** — whole-document orchestrator called from `Pipeline.process_full` when `mode=solution_manual`. Persists `problem-pairings.yaml` and `cards-debug.yaml` BEFORE the audit so failures preserve the LLM output for inspection.

**First end-to-end run:** Schaum's Microbiology Ch1 (PDF pages 8-18 chapter + page 328 back-of-book answer key) produced 30 `problem_main` + 1 `problem_overview` card via 30+1 LLM calls. Audit passed; the artifacts landed in `<key>-problem-set.apkg`. The cards-debug + pairings-yaml dump caught the original `card_subtype` defaulting bug (LLM was emitting cards without `card_subtype`, audit fired correctly with "30 problems missing from cards"); fix was to stamp the subtype from the plan after the LLM call.

**Deferred to follow-up:** classifier-driven `mode=full` per-section routing (`run_problem_set_for_section` is not yet implemented), Stage-3 LLM pairing fallback, and overlap-aware modulation of the prose card-gen pipeline.
