---
id: c0isilrgix01d6oyh5ytcvq
title: Section Classifier
desc: Heading-driven (with LLM fallback) page classifier — emits PageLabels for content-aware routing in mode=full
updated: 1777608400000
created: 1777608400000
---

## 2026.04.26 - Initial implementation

Foundation classifier for `mode=full`'s integrated routing. Walks per-page cleaned markdown and emits a `ClassificationResult` (one `PageLabel` per page).

**Heading-driven anchors:**
- `## Theory and Problems` → `main_content` (Schaum's chapter body even when heavy Q&A).
- `## Multiple Choice / Matching / True/False / Completion / Review Questions / Problems / Exercises / Practice Problems` → `review_exercises`.
- `Preface / Table of Contents / Copyright / Dedication` → `front_matter` (only on first 5 pages, downgrades if other content cues present).
- `Index / Glossary / Bibliography / References` → `back_matter` (heuristic; downgraded if conflicting cues).
- Back-of-book `^Chapter N\nMultiple Choice` blocks → after Q-A pairing, re-classified to `review_exercises` with `paired_answer_page` set to the question section.

**Overlap density** for `main_content` pages = `min(1.0, n_problem_starters * 50 / n_chars)`. Tuned so 20 problems in 5000 chars ≈ 0.5. Used downstream by `_generate_main_cards` to modulate card density when overlap is high (deferred to follow-up).

**LLM fallback** (`section_classifier_agent`) when heading-driven confidence is below `pipeline.solution_manual.section_classifier_min_confidence` (default 0.7). Sends the first 1500 chars of each page as a sample.

**Override workflow:** classifier persists to `<output_dir>/section-classification.yaml`. To override, hand-edit the YAML and pass `+pipeline.solution_manual.classification_override=path/to/edited.yaml` on the next run.

**Helpers:**
- `merge_main_content` — concat only main_content pages (segmenter input + audio source masking).
- `filter_files_by_kind` — subset of cleaned-md files by kind (used by `Pipeline.process_full` to route pages).
- `original_page_indices` — translate filtered-page idx → original-document idx for image-summary lookup.

First validated on a synthetic 4-page Schaum's-style fixture: pages 0-1 → `main_content` (Theory and Problems, 71% density), page 2 → `review_exercises` (Multiple Choice), page 3 → `back_matter` (Index). Heading-driven path with confidence 1.00.
