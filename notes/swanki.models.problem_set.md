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
