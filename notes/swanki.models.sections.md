---
id: 0l58vc9ctzy6tm3jjkvura9
title: Sections Models
desc: Pydantic models for content-section classification — PageLabel (per-page source of truth), ContentSection (RLE-derived view), ClassificationResult
updated: 1777608400000
created: 1777608400000
---

## 2026.04.26 - Initial implementation

Foundation Pydantic models for the section-aware routing layer in `mode=full`. Three types:

- **`PageLabel`** — per-page record (the source of truth). Carries `kind` (main_content / review_exercises / front_matter / back_matter), `heading_anchor` (diagnostic), `overlap_density` (0-1, problem-shape signal for main_content), `confidence`, `paired_answer_page` (back-of-book pages link to question pages), and `note` (freeform diagnostic).
- **`ContentSection`** — derived view: run-length-encoded same-kind PageLabels. Built by `sections_from_page_labels()` and consumed by routing logic in `Pipeline.process_full`.
- **`ClassificationResult`** — top-level output. `page_labels` is the primary artifact; `sections` are derived via a `model_validator(mode="after")` that runs RLE if not already populated. Persisted to `<output_dir>/section-classification.yaml` for introspection — the user can hand-edit and re-run with `pipeline.solution_manual.classification_override`.

The page-level granularity has a known limit: within-page transitions (e.g. a `## Multiple Choice` heading appearing mid-page after a paragraph of theory) get one label and ~½ page of content is misrouted. Schaum's Ch1 has clean page-aligned section boundaries so this isn't hit in practice yet.
