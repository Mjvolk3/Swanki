---
id: b6hhxha51tszd752c9s08ft
title: Problem Set Models
desc: Pydantic models for solution-manual mode — problem units, card plans, provenance, problem-solution pairing, ProblemTag parser/renderer, and pydantic-ai response wrappers
updated: 1777607710601
created: 1777607710601
---

## 2026.04.26 - Initial implementation

Foundation Pydantic models for `mode=solution_manual`. Owns:

- `ProblemSubtype` and `CardSubtype` literals.
- `ProblemPart`, `ProblemUnit` — one numbered problem with statement, optional inline solution, parts, page span, char count, and referenced figures/equations.
- `CardPlan` (with consistency model_validator), `ProvenanceSpan`/`ProblemProvenance`/`ProvenanceLog`.
- `ProblemLocation`, `ProblemPairing`, `PairingResult` — far-apart problem-solution pairing artifact persisted to `<output_dir>/problem-pairings.yaml`.
- `ProblemTag` — strongly-typed parser/renderer for the `<citation_key>.problem.<id>` tag (replaces fragile `str.startswith` audit logic with a strict regex round-trip).
- Four pydantic-ai response wrappers (`ProblemEnumerationResponse`, `CardPlanResponse`, `ProblemCardBatchResponse`, `ProblemPairingResponse`).

**Why response wrappers live here, not in `pipeline/problem_set.py`:** `llm/agents.py` imports response types from `models/`, and `pipeline/problem_set.py` imports the agents. Importing response types from the pipeline module would cycle.

## 2026.05.04 - ProblemTag regex extended for chapter-prefixed IDs

Updated `_PROBLEM_TAG_RE` to accept chapter-prefixed problem IDs introduced by the MC / Matching / True-False / Completion enumeration work. The middle alternation went from `[0-9]+\.[0-9]+|MC-\d+|[A-Z]+-\d+` to `[0-9]+\.[0-9]+|[A-Z]+(?:-CH\d+)?-\d+`. The `(?:-CH\d+)?` group covers the chapter-prefixed primary form (`MC-CH1-7`, `MAT-CH1-3`, `TF-CH1-7`, `CMP-CH2-9`) while the optional makes it pick up the bare fallback form (`MC-7`, `MAT-3`) used when chapter context is unknown. Verified empirically: the prior regex rejected `MC-CH1-7` because `[A-Z]+-\d+` requires the prefix-letters to be immediately followed by `-\d+`, not by `-CH\d+-\d+`. Without this fix, `audit_coverage` Part 3 (which calls `ProblemTag.parse` per `problem_main` card tag) would hard-fail with every newly-enumerated review-section problem reported as missing-from-cards.

No other model changes — `ProblemSubtype` Literal already covered all five subtypes from the initial implementation, and `ProblemUnit` shape is unchanged because subtype-specific data (MC choices, Column B options, T/F replacement word, Completion blank position) is encoded as prose inside `statement` and `solution` rather than as new optional fields. That keeps the schema single-shape and makes the LLM the single source of card-content rendering.
