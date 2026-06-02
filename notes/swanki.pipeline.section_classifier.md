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

## 2026.05.29 - Broaden review-heading detection to H1-H3

`_REVIEW_HEADINGS` was anchored to `^##` (H2 only), but Bishop-style packed PDFs ([[scripts.book_solution_pack]]) emit the end-of-chapter exercises section as an H1 `# Exercises` rather than H2. Broadened the prefix from `^##` to `^#{1,3}` so H1-H3 review headings (Multiple Choice / Matching / True/False / Completion / Review Questions / Problems / Exercises / Practice Problems) all route to `review_exercises`. This keeps the classifier and the new Stage 3 statement/solution partition in [[swanki.pipeline.problem_set]] (`_EXERCISES_HEADING`, also H1-H3) in agreement on where the exercises region begins.

## 2026.05.30 - `join_pages` glues mid-sentence page breaks

`merge_main_content` (and the reading fallback in [[swanki.pipeline.pipeline]] at the `cleaned_files` branch) concatenated `clean-md-singles` pages with a bare `"\n\n"`. Downstream, `add_tts_pauses` ([[swanki.audio._common]]) blanket-promotes every `\n\n` to a Fish `[pause]`. But pages routinely end mid-sentence — Hamming Ch1 has 4 of 8 pages doing so (p1→p2 "...being right,", p2→p3 "...I went to Bell" | "Telephone Laboratories", p4→p5 "...knowledge when" | "they arise", p7→p8 inside the computer-advantages list). The blanket promotion dropped an audible `[pause]` mid-sentence at each seam — surfaced by an orange ABS comment on the p4→p5 gap.

Fix: new `join_pages(texts)` joins with `"\n\n"` only when the prior page ends a sentence (`_SENTENCE_TERMINAL_RE`: terminal `.!?:;` or a closing bracket/quote after it); otherwise it glues with a single space so the sentence is spoken continuously. Routed both `merge_main_content` and the pipeline reading fallback through it; this covers reading **and** lecture (both read from `main_content_text`). NOT fixed in `add_tts_pauses` line 70 itself, because that blanket rule also produces the *intended* inter-item pauses inside word-tables (e.g. Ch1 table 2 "Economics — far cheaper; Speed — far faster"). Verified on Ch1 `_12`: `[pause]` count 47→43 (exactly the 4 mid-sentence seams), every sentence-end pause preserved. Existing audio needs a reading+lecture re-gen to pick this up. Tests in `tests/test_section_classifier.py`.

## 2026.06.01 - Back-matter false-positive: anchor cues + positional tail guard

`_BACK_MATTER = re.compile(r"\b(Index|Glossary|Bibliography|References)\b", re.IGNORECASE)` matched those words ANYWHERE in prose. On Hamming ch04 (`_CH04_history-of-computers-software`) it matched "index" in "I needed **index** registers" on page-4 (mid-chapter), flipped that page to `back_matter` at confidence 1.0, and — because `current_kind` is sticky across the loop — pages 4-8 inherited `back_matter`. `filter_files_by_kind("main_content")` then dropped 6 of 9 pages, so card-gen saw only 2 segments → **4 cards (old ch04 had 14)**. ch04 was the only chapter hit; the other 9 were 100% `main_content`.

Fix is **trigger-only** — the sticky cascade itself is load-bearing (real paper References span the last 2-3 pages; Schaum's answer keys span ~12 pages and `_pair_answer_keys` re-promotes them to `review_exercises`), so de-stickying was rejected as it would split legitimate multi-page back-matter. Two stacked guards on the *start* of a back_matter run instead:

1. Anchor `_BACK_MATTER` (and symmetrically `_FRONT_MATTER`) to a markdown heading: `^#{1,6}\s+(Index|Glossary|Bibliography|References)\b` with `MULTILINE`. Real back-matter in this corpus is always a promoted heading (`## References`, `# Bibliography`, `## Bibliography and Notes`); prose mentions ("index registers", "original references", "a preface to...") no longer match.
2. Positional tail guard in `_heading_classify`: the back_matter flip additionally requires `i >= int(total * 0.8)` (last ~20% of pages). A stray real heading mid-document can't start a back_matter run; a genuine tail heading still flips and cascades through the rest of the back-matter.

Benign-vs-malignant trade: a real but un-promoted (no `#`) back-matter line now falls to `main_content` (a few extra reference-list cards — benign) instead of dropping a content page (malignant); the LLM fallback still covers genuinely ambiguous middles. Stickiness, confidence model, `_pair_answer_keys`, review/theory/chapter regexes, and all configs unchanged. Verified: re-classifying ch04's `clean-md-singles` now yields all `main_content`; a real paper (`campagneClinicalPharmacokineticsPharmacodynamics2021`, 17 pp) still tags only its last page `back_matter`. Tests in `tests/test_section_classifier.py` (`_heading_classify` cases: mid-prose "index registers" stays main; tail `## References` is back_matter; mid-doc `## References` is rejected by the guard; multi-page tail back-matter stays contiguous; front-matter prose vs heading).
