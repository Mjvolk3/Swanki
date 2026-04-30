---
id: 86dn58uv2qwvhve2dytipre
title: Solution Manual Mode for Problem-Set PDFs
desc: New Swanki mode for generating Anki cards from problem-set PDFs (Schaum's, Bishop) with deterministic problem enumeration, problem-solution pairing, cross-chapter reference resolution, and coverage audit
updated: 1777161207306
created: 1777130653542
---
k
Plan: Solution Manual Mode for Problem-Set PDFs

## Context

Swanki today generates cards from research-paper-style PDFs by char-segmenting cleaned markdown and asking the LLM for N regular + M cloze cards per segment. That model breaks for textbook problem sets (Schaum's Outlines, Bishop's Deep Learning, etc.) where:

1. Content is structured as numbered Q&A pairs (`1.1`, `1.2`, `2.1`, ...) rather than continuous prose. Char-segmentation slices across `1.4 / 1.5` boundaries and silently drops or scrambles problems.
2. Solutions reference equations, figures, and theorems from the chapter ("use equation (1.2)") that the learner cannot see on the card. Cards must be self-contained: refs must be inlined or images embedded.
3. Solutions can sit adjacent (Schaum's inline theory-problems), at the end of the chapter, or in a back-of-book answer key. Cross-chapter refs (Ch 5 references Ch 2) cannot be resolved from the problem-set PDF alone.
4. Some printed solutions skip steps. Learners need filled-in walkthroughs without seeing the gap-fill surgery on the card face.
5. Completeness is non-negotiable: if a chapter has 40 numbered problems, the deck must cover all 40. The current pipeline has no coverage audit.

Schaum's `alcamoSchaumsOutlineMicrobiology2010` Ch1 (PDF pages 8-18) plus its back-of-book answer-key region (PDF pages 328-336) are the empirical anchor — five distinct problem subtypes coexist within a single chapter:

| Subtype                         | Chapter side                      | Answer-key side       | Phase |
|---------------------------------|-----------------------------------|-----------------------|-------|
| Numbered theory-problem (`N.M`) | full Q + full A inline            | n/a                   | 1     |
| Multiple Choice                 | stem + (a)(b)(c)(d)               | letter only (`1. c`)  | 1     |
| Matching                        | column A items + column B options | letter mapping        | 2     |
| True/False                      | statement, one word underlined    | T or replacement word | 2     |
| Completion                      | fill-in-blank stem                | the missing word      | 2     |

Bishop's chapters are pattern-compatible: chapter PDF + appended worked-solutions PDF (official, user-handwritten, or both).

**One PDF, integrated routing.** The user provides the entire package (chapter + appended solutions) as a single PDF. A new section-classifier identifies which portions are prose-style "main content" (suitable for normal card-gen + lecture/summary audio) vs problem-set with paired solutions (suitable for problem-set card-gen). The pipeline routes each section through the appropriate stage and merges outputs. This avoids two failure modes the explicit-flag-only design suffered from:

1. **Lecture audio for problem sets** — Schaum's MC review or Bishop end-of-chapter problem lists read terribly as a lecture; they must be excluded from the audio source.
2. **Redundant card generation** — Schaum's main content IS Q&A. If both pipelines run unfiltered over it, two competing card sets emerge. The classifier sets an "overlap" flag when the same content is eligible for both; the main pipeline then receives a reduced card budget AND an instruction to skip example-question content (focus on underlying concepts). Problem-set pipeline still produces one card per problem.

**Two empirical cases the design must handle:**

- **Schaum's Ch1**: ~95% of the body is numbered theory-problems. Classifier marks the body as `main_content` with HIGH problem-set overlap; lecture/summary audio still uses this content (it IS the chapter), but main card-gen reduces to ~5% of normal density and is instructed to extract concepts rather than restate examples. The end-of-chapter MC review section + appended back-of-book answers route only to problem-set card-gen, not audio.
- **Bishop chapter**: prose body (sections 1.1, 1.2, ...) is `main_content` with NO overlap; problems block at end is `review_exercises`; appended worked-solutions PDF is paired with the problems block. Main card-gen runs normally on prose; audio sources prose only; problem-set card-gen runs on the problems+solutions pair.

The `chapter-index.yaml` artifact (numbered equations, figures, theorems with content) is emitted from any run with `main_content` sections, carrying forward the cross-chapter reference resolution capability. The earlier two-run workflow (chapter run → solution_manual run) collapses into a single integrated run.

## Kanban Issues

No directly related issues found. The Swanki repo's GitHub issue tracker is currently empty (verified via `gh issue list --state open`); work tracking happens in dendron weekly notes.

## Approach

Design decisions, locked from the planning conversation:

1. **One run, classifier-driven routing.** No `mode=solution_manual` top-level flag. `mode=full` (default) runs a section classifier after MarkdownCleaner that produces a `list[ContentSection]` with kind labels (`main_content`, `review_exercises`, `front_matter`, `back_matter`). Each section routes to the appropriate downstream stage. `mode=audio_only` continues to skip card-gen entirely. An optional `mode=solution_manual` is retained as an explicit override that forces every section to `review_exercises` (useful when the user provides a problem-set-only PDF and wants to bypass the classifier).
2. **Section-classifier.** Heading-driven first (`## Theory and Problems`, `## Multiple Choice`, `## Review Questions`, `## Problems`, `## Answers to Review Questions` — strong signals in Schaum's; Bishop uses `## Exercises`). LLM fallback (`section_classifier_agent`) when headings are absent or ambiguous. Output is a `ClassificationResult` carrying sections + per-section overlap density + paired answer-key spans.
3. **Overlap density.** A score in `[0, 1]` per `main_content` section measuring how much of its content is problem-shaped (numbered Q&A blocks, MC stems, etc.). When `overlap_density > 0.5`, the main pipeline runs with reduced card density (default `main_card_reduction_factor: 0.05` — 1/20th of normal) and an instruction injection ("treat numbered problems as illustrative; extract underlying concepts; do NOT restate the example questions verbatim"). Below threshold, main pipeline runs normally.
4. **Audio source masking.** Lecture and reading audio sources are filtered to `main_content` sections only (concatenated). Summary audio (built from `DocumentSummary`) is unaffected. Per-card audio is also unaffected (it follows the cards, not the source). For Schaum's where `main_content` is dominantly Q&A, the lecture is built from the Q&A — that IS the chapter — but `review_exercises` sections are excluded.
5. **Phase 1 problem-subtype scope** = numbered theory-problems (`N.M`) and Multiple Choice. Phase 2 = Matching / True-False / Completion. Pydantic schema accommodates Phase 2 from day one (`ProblemSubtype` enum) but only Phase 1 paths are wired and tested.
6. **Card structure per problem.** ≤5 cards: 1 `problem_main` + ≤3 `subproblem` (driven by `(a)/(b)/(c)` parts) + ≤1 `problem_overview` (only if main spans >2 pages) + ≤1 `full_solution` (uncapped). All capped types use the existing 500-char `CardContent.text` rule. Only `full_solution` is uncapped via a new `LongFormCardContent` sibling class.
7. **Length policy.** Default = compressed cards under 500 chars. If the printed solution would blow the cap, the main card carries a high-level view (intermediate results, mechanical steps elided), detail goes into `subproblem` cards (a/b/c), and the optional `full_solution` card carries the complete walkthrough with any LLM gap-filling. The full-solution card is the only escape hatch.
8. **Reference resolver.** Builds an in-memory index from (a) the current run's `clean-md-singles/` and (b) any supplied `chapter-index.yaml` files (still configurable via `solution_manual.chapter_indexes` for cross-chapter resolution from prior runs). Resolves `equation (X.Y)` / `Figure X.Y` / `Theorem X.Y` patterns by inlining LaTeX content into problem/solution text and attaching figure images to card backs. Unresolved refs surface as hard warnings on the card and in a sidecar log.
9. **Coverage audit (zero tolerance) — three-part.** The audit lives in `audit_coverage` and is the only thing standing between a partial run and APKG export. (1) Every enumerated problem must appear in `PairingResult.pairings` — if not, the problem-statement parser missed it. (2) Every pairing must have at least one solution unless `allow_unsolved=True` (config knob, default False). (3) Every pairing must be covered by exactly one `card_subtype="problem_main"` card, matched by tag `{citation_key}.problem.{id}`. Any miss in any part raises `CoverageError` and aborts before APKG export. The audit applies only to problem-set sections; `main_content` cards are concept-driven and have no enumerated contract.

12a. **Far-apart problem-solution pairing.** When the user supplies a single PDF with chapter + worked solutions appended (Bishop) or chapter + back-of-book answer key (Schaum's), the solution for problem 1.7 may sit hundreds of pages from the question. Pairing runs in three stages: (a) adjacent-text pairing for inline Q&A like Schaum's `1.1` blocks; (b) regex pairing on explicit `Solution N.M` headings or back-of-book `Chapter N / Multiple Choice / 1. c 2. c ...` blocks; (c) LLM fallback (`problem_pairing_agent`) for any problems still unpaired — the agent receives unmatched solution-shaped text spans and the open problems, returns `ProblemLocation` entries by content match. Result is a `PairingResult` persisted to `<output_dir>/problem-pairings.yaml` for introspection. The coverage audit reads this artifact, not the page locations.
10. **Provenance sidecar.** A YAML artifact tracks copy-vs-LLM-generated spans for `full_solution` cards. Maintainer-only — never rendered on the card face. Stored at `<output_dir>/provenance.yaml`.
11. **Output deck naming.** Single `<content_key>.apkg` deck containing both main and problem-set cards. Tags discriminate (`#problem-set`, `#chapter-{N}.problem.{id}` for problem-set cards; existing concept tags for main cards). The `apkg_filename_suffix` config knob is retained for the explicit `mode=solution_manual` override use case (`-problem-set` suffix). Centralize the two hard-coded `f"{self.citation_key}.apkg"` sites in `pipeline.py` (lines 426, 1770) into a single `Pipeline._apkg_filename()` helper.
12. **Per-card audio unchanged.** `swanki/audio/card.py` is functionally subtype-blind; problem cards flow through it unmodified. The full-solution card's longer text gets paragraph-chunked by the existing `chunk_text` path. Type signatures widened to `PlainCard | FullSolutionCard`. Image cards in problem-set sections use `card.back.image_path` directly without invoking the vision-summary pipeline.

Pipeline shape inside `mode=full` (default — classifier-driven dispatch replaces the segment-driven card-gen body at lines 285-393 of `process_full`):

```
clean markdown (existing) → image processing (existing)
  → ChapterIndex extraction (NEW) → write chapter-index.yaml (NEW)
  → DocumentSummary (existing)
  → SectionClassifier (NEW) → list[ContentSection] with overlap_density per section
  → For each section, route by section.kind:
    main_content sections (combined into the existing segmenter input):
      → segmenter.split_into_segments (existing)
      → for each segment: _generate_cards_for_segment (existing, with overlap-aware
        card-density modifier + instruction injection when overlap_density > 0.5)
      → image-card interleaving (existing)
      → list[PlainCard] (main cards)

    review_exercises sections (per section):
      → enumerate problems (regex first, LLM fallback) (NEW) → list[ProblemUnit]
      → pair problems with solutions (NEW) → annotated ProblemUnits
      → resolve cross-references against ChapterIndex + supplied prior indexes (NEW)
      → for each problem: classify card-plan + generate cards (NEW)
                           → list[PlainCard | FullSolutionCard]
      → coverage audit (NEW) — hard-fail per section

    front_matter / back_matter sections:
      → skipped entirely

  → merge all_cards = main_cards + problem_set_cards
  → write outputs: cards-plain.md, provenance.yaml, deck = <content_key>.apkg
  → audio:
      lecture: source = concat(main_content sections) (FILTERED — review_exercises excluded)
      reading: source = concat(main_content sections) (FILTERED)
      summary: from DocumentSummary (unfiltered)
      per-card: existing per-card flow (unchanged)
  → re-export apkg with audio
  → Anki send (existing)
  → Zotero sync (existing)
```

`mode=audio_only` skips card-gen entirely but still runs the classifier so audio sources can be filtered to `main_content`.

Optional `mode=solution_manual` (explicit override): bypass the classifier, treat every section as `review_exercises`. Use when the user knows the entire input is problem-set content (e.g., a worked-solutions PDF only). Implies `apkg_filename_suffix=-problem-set` automatically.

## File Specifications

### `swanki/models/sections.py` (NEW)

**Purpose:** Pydantic models for the section-classification layer. Used by `SectionClassifier` and consumed by `Pipeline.process_full` to route sections.

**Depends on:** stdlib + `pydantic`.

**Types:**

- `SectionKind = Literal["main_content", "review_exercises", "front_matter", "back_matter"]`
- `PageLabel(BaseModel)` — per-page classification record (the **source of truth** for routing). Persisted to `<output_dir>/section-classification.yaml` for introspection, debugging, and manual override.
  - `page_idx: int` — 0-indexed.
  - `kind: SectionKind`
  - `heading_anchor: str | None = None` — most recent markdown heading that determined this page's classification (e.g. `"## Multiple Choice"`). Diagnostic only.
  - `overlap_density: float = Field(ge=0.0, le=1.0, default=0.0)` — per-page problem-shape density. For `review_exercises` always 1.0; for `main_content` computed from problem-pattern count on this page; for matter pages, 0.0.
  - `confidence: float = Field(ge=0.0, le=1.0, default=1.0)` — confidence in this page's label. Heading-anchored pages get 1.0; LLM-only pages get the agent's reported confidence; ambiguous pages mid-transition get a lower value.
  - `paired_answer_page: int | None = None` — when a back-of-book answer page belongs to a `review_exercises` section earlier in the document, its index points back. Used during Q-A pairing.
  - `note: str | None = None` — freeform diagnostic ("re-classified from back_matter to review_exercises after pairing").
- `ContentSection(BaseModel)` — **derived view** of consecutive same-kind page labels (run-length encoding). Built by `sections_from_page_labels()`.
  - `kind: SectionKind`
  - `start_page: int` — 0-indexed inclusive.
  - `end_page: int` — 0-indexed inclusive.
  - `heading: str | None = None` — heading anchor of the first page (if any).
  - `overlap_density: float = Field(ge=0.0, le=1.0, default=0.0)` — section-level density (mean over pages, weighted by page char count if precision matters; mean-of-pages is fine for v1).
  - `paired_answer_section: int | None = None` — index of paired `review_exercises` section if any page within carries `paired_answer_page` to a section earlier.
- `ClassificationResult(BaseModel)`:
  - `page_labels: list[PageLabel]` — primary artifact, length == number of pages.
  - `sections: list[ContentSection]` — derived; populated by `sections_from_page_labels(page_labels)` at construction time (or via a `@model_validator(mode="after")`).
  - `confidence: float = Field(ge=0.0, le=1.0)` — overall classifier confidence (mean over `page_labels[i].confidence`, or min — pick min so a single low-confidence page surfaces).
  - `method: Literal["heading", "llm", "mixed"]` — which path produced the result.

**Helper:**

- `sections_from_page_labels(page_labels: list[PageLabel]) -> list[ContentSection]` — module-level function that run-length-encodes the page list into sections, computing per-section `overlap_density` (mean over included pages) and propagating heading anchors.

**Skeleton:**

```python
"""
swanki/models/sections.py
[[swanki.models.sections]]
https://github.com/Mjvolk3/Swanki/tree/main/swanki/models/sections.py
Test file: tests/test_sections_models.py

Pydantic models for content-section classification used by the section-aware
routing layer in Pipeline.process_full.
"""

from typing import Literal

from pydantic import BaseModel, Field, model_validator

SectionKind = Literal[
    "main_content", "review_exercises", "front_matter", "back_matter"
]


class PageLabel(BaseModel):
    page_idx: int
    kind: SectionKind
    heading_anchor: str | None = None
    overlap_density: float = Field(ge=0.0, le=1.0, default=0.0)
    confidence: float = Field(ge=0.0, le=1.0, default=1.0)
    paired_answer_page: int | None = None
    note: str | None = None


class ContentSection(BaseModel):
    kind: SectionKind
    start_page: int
    end_page: int
    heading: str | None = None
    overlap_density: float = Field(ge=0.0, le=1.0, default=0.0)
    paired_answer_section: int | None = None


class ClassificationResult(BaseModel):
    page_labels: list[PageLabel]
    sections: list[ContentSection] = Field(default_factory=list)
    confidence: float = Field(ge=0.0, le=1.0)
    method: Literal["heading", "llm", "mixed"]

    @model_validator(mode="after")
    def derive_sections_if_empty(self) -> "ClassificationResult":
        if not self.sections and self.page_labels:
            self.sections = sections_from_page_labels(self.page_labels)
        return self


def sections_from_page_labels(page_labels: list[PageLabel]) -> list[ContentSection]:
    """Run-length-encode page labels into ContentSection ranges.

    Consecutive pages with the same kind merge into one section. Section-level
    overlap_density is the mean of constituent page densities. The heading
    anchor of the first page becomes the section heading.
    """
    if not page_labels:
        return []
    sections: list[ContentSection] = []
    cur_kind = page_labels[0].kind
    cur_start = 0
    cur_heading = page_labels[0].heading_anchor
    for i in range(1, len(page_labels) + 1):
        boundary = i == len(page_labels) or page_labels[i].kind != cur_kind
        if boundary:
            span = page_labels[cur_start : i]
            density = sum(p.overlap_density for p in span) / len(span)
            sections.append(
                ContentSection(
                    kind=cur_kind,
                    start_page=cur_start,
                    end_page=i - 1,
                    heading=cur_heading,
                    overlap_density=density,
                )
            )
            if i < len(page_labels):
                cur_kind = page_labels[i].kind
                cur_start = i
                cur_heading = page_labels[i].heading_anchor
    return sections
```

Persistence (in `swanki/pipeline/section_classifier.py`): after `classify_sections()` completes, write `ClassificationResult.model_dump()` to `<output_dir>/section-classification.yaml`. This artifact is the audit trail. To override the classifier on a re-run, the user edits this YAML and passes `+pipeline.solution_manual.classification_override=path/to/edited.yaml` — `classify_sections` checks for this path first and returns the loaded `ClassificationResult` directly when present.

### `swanki/pipeline/section_classifier.py` (NEW)

**Purpose:** Classify cleaned per-page markdown into a `ClassificationResult`. Heading-driven first; LLM fallback (`section_classifier_agent`) when headings don't carry enough signal. Computes overlap density per `main_content` section. Pairs `review_exercises` sections with their corresponding back-of-book answer-key sections.

**Depends on:** `swanki.models.sections`, `swanki.llm.agents.section_classifier_agent`, `swanki.utils.content`, regex.

**Heading-driven classification:**

- `## Theory and Problems` → `main_content` start.
- `## Multiple Choice`, `## Matching`, `## True/False`, `## Completion`, `## Review Questions`, `## Problems`, `## Exercises` → `review_exercises`.
- `## Answers to Review Questions`, `## Solutions`, `Chapter \d+ / Multiple Choice` (back-of-book pattern) → `back_matter` initially, then re-classified to `review_exercises` and paired with the matching question section by chapter number.
- Front matter detection: if first content page contains `Preface`, `Contents`, `Copyright`, `Table of Contents` → `front_matter` until first `^# (CHAPTER|Chapter)` heading.
- Anything else → `main_content`.

**Overlap density:**

For each `main_content` section, count problem-shaped patterns and divide by content length:
- `^\d+\.\d+\s` lines (numbered theory-problem starters)
- `^\d+\.\s+(?:[A-Z]|\()` lines following an MC-style stem
- "Review Questions" or "Practice Problems" subheadings within the section

Density = (count_of_problem_starters * 50) / total_chars (heuristic; tuned so a section with ~20 numbered problems in 5000 chars hits ~0.5).

**LLM fallback:** invoked when `confidence < min_confidence` from heading-only pass. The agent receives the cleaned markdown (or a sample) and emits a `ClassificationResult` directly.

**Functions:**

- `classify_sections(clean_md_files: list[Path], config: dict) -> ClassificationResult` — top-level entry; tries heading-first then LLM.
- `_heading_classify(clean_md_files: list[Path]) -> ClassificationResult` — pure heading-driven pass.
- `_compute_overlap_density(section_text: str) -> float` — pattern count / length heuristic.
- `_pair_answer_keys(sections: list[ContentSection], texts: list[str]) -> list[ContentSection]` — finds back-of-book `^Chapter N$` blocks and links them to their `review_exercises` sections by chapter number.
- `_llm_classify(clean_md_files: list[Path], config: dict) -> ClassificationResult` — calls `section_classifier_agent`.
- `merge_main_content(clean_md_files: list[Path], sections: list[ContentSection]) -> str` — concatenates only the `main_content` sections' text into a single string for downstream segmentation + lecture/reading audio source.

**Skeleton:**

```python
"""
swanki/pipeline/section_classifier.py
[[swanki.pipeline.section_classifier]]
https://github.com/Mjvolk3/Swanki/tree/main/swanki/pipeline/section_classifier.py
Test file: tests/test_section_classifier.py

Section classification for content-aware routing: identify main_content vs
review_exercises sections, compute overlap density, pair Q-with-A across
the back-of-book region, and provide a filtered concatenation helper for
audio source masking.
"""

import logging
import re
from pathlib import Path
from typing import Any

import yaml

from ..llm.agents import get_model_string, section_classifier_agent
from ..models.sections import (
    ClassificationResult,
    ContentSection,
    PageLabel,
    SectionKind,
    sections_from_page_labels,
)

logger = logging.getLogger(__name__)


_PROBLEM_STARTER = re.compile(r"^\d+\.\d+\s+\S", re.MULTILINE)
_REVIEW_HEADINGS = re.compile(
    r"^##\s+(Multiple Choice|Matching|True/False|Completion|Review Questions|Problems|Exercises)\b",
    re.MULTILINE,
)
_THEORY_HEADING = re.compile(r"^##\s+Theory and Problems\b", re.MULTILINE)
_FRONT_MATTER = re.compile(r"\b(Preface|Table of Contents|Copyright)\b")
_CHAPTER_HEADER = re.compile(r"^#\s+(?:CHAPTER|Chapter)\s+\d+", re.MULTILINE)
_BACK_OF_BOOK_BLOCK = re.compile(
    r"^Chapter\s+(\d+)\s*\n\s*(Multiple Choice|Matching|True/False|Completion)",
    re.MULTILINE,
)


def classify_sections(
    clean_md_files: list[Path],
    config: dict[str, Any],
    output_dir: Path | None = None,
) -> ClassificationResult:
    """Classify pages into PageLabels; heading-first with LLM fallback.

    If pipeline.solution_manual.classification_override is set in config, load
    and return the override directly (skips classification entirely). This is the
    introspection / manual-correction path: edit the persisted YAML, point this
    knob at it, re-run.

    Persists the final ClassificationResult to <output_dir>/section-classification.yaml
    when output_dir is provided.
    """
    sm_config = config.get("pipeline", {}).get("solution_manual", {})
    override_path = sm_config.get("classification_override")
    if override_path:
        logger.info(f"Loading classification override from {override_path}")
        result = ClassificationResult.model_validate(
            yaml.safe_load(Path(override_path).read_text())
        )
    else:
        heading_result = _heading_classify(clean_md_files)
        min_confidence = sm_config.get("section_classifier_min_confidence", 0.7)
        if heading_result.confidence >= min_confidence:
            result = heading_result
        else:
            logger.info(
                f"Heading classifier confidence {heading_result.confidence:.2f} below "
                f"{min_confidence}; invoking LLM fallback"
            )
            result = _llm_classify(clean_md_files, config)

    if output_dir is not None:
        out_path = output_dir / "section-classification.yaml"
        out_path.write_text(yaml.safe_dump(result.model_dump(), sort_keys=False))
        logger.info(f"Wrote classification artifact: {out_path}")

    return result


def _heading_classify(clean_md_files: list[Path]) -> ClassificationResult:
    """Pure heading-driven classification — emits one PageLabel per page.

    Walks pages, tracks the most recent heading, sets each page's kind +
    heading_anchor + per-page overlap_density. Then calls _pair_answer_keys
    to re-classify back-of-book pages and link them to their question pages.
    Sections are derived from page_labels by the model_validator.
    """
    page_labels: list[PageLabel] = []
    texts = [f.read_text() for f in clean_md_files]
    current_kind: SectionKind = "main_content"
    current_anchor: str | None = None
    for i, text in enumerate(texts):
        # Detect headings on this page; transition kind if a section heading appears.
        # ... apply _FRONT_MATTER, _CHAPTER_HEADER, _THEORY_HEADING, _REVIEW_HEADINGS,
        #     _BACK_OF_BOOK_BLOCK regexes; update current_kind + current_anchor ...
        density = _compute_overlap_density(text) if current_kind == "main_content" else (
            1.0 if current_kind == "review_exercises" else 0.0
        )
        confidence = 1.0 if current_anchor else 0.6  # heading-anchored vs inferred
        page_labels.append(
            PageLabel(
                page_idx=i,
                kind=current_kind,
                heading_anchor=current_anchor,
                overlap_density=density,
                confidence=confidence,
            )
        )

    page_labels = _pair_answer_keys(page_labels, texts)
    overall_confidence = (
        sum(p.confidence for p in page_labels) / len(page_labels)
        if page_labels
        else 0.0
    )
    return ClassificationResult(
        page_labels=page_labels, confidence=overall_confidence, method="heading"
    )


def _compute_overlap_density(section_text: str) -> float:
    """Estimate problem-shape density of a main_content section."""
    n_problem_starters = len(_PROBLEM_STARTER.findall(section_text))
    n_chars = max(1, len(section_text))
    return min(1.0, (n_problem_starters * 50) / n_chars)


def _pair_answer_keys(
    page_labels: list[PageLabel], texts: list[str]
) -> list[PageLabel]:
    """Find back-of-book ^Chapter N / Multiple Choice blocks and re-classify
    those pages from back_matter → review_exercises. Link each re-classified
    page's paired_answer_page back to its corresponding question-section page.

    Mutates page_labels in place (annotates note='re-classified from back_matter
    to review_exercises after pairing') and returns it.
    """
    # ... walk pages classified back_matter; for each page whose text contains
    # a "^Chapter (\d+)\s*\n\s*(Multiple Choice|...)" anchor, find the earliest
    # review_exercises page in chapter N and set paired_answer_page; then flip
    # the back-matter page's kind to review_exercises ...
    return page_labels


def _llm_classify(
    clean_md_files: list[Path], config: dict[str, Any]
) -> ClassificationResult:
    """Fallback: ask section_classifier_agent to produce ClassificationResult."""
    prompts_root = config.get("prompts", {}).get("prompts", {})
    sm_prompts = prompts_root.get("solution_manual", {})
    system_prompt = sm_prompts.get("section_classifier", "")
    sample = "\n\n--- PAGE ---\n\n".join(f.read_text()[:1500] for f in clean_md_files)
    models_config = config.get("models", {}).get("models", {}).get("llm", {})
    result = section_classifier_agent.run_sync(
        sample, instructions=system_prompt, model=get_model_string(models_config)
    )
    return result.output


def merge_main_content(
    clean_md_files: list[Path], page_labels: list[PageLabel]
) -> str:
    """Concatenate only pages labeled main_content.

    Used by both the segmentation step (so the segmenter never sees problem-set
    content) and by audio/lecture.py / audio/reading.py source assembly.
    """
    return "\n\n".join(
        clean_md_files[p.page_idx].read_text()
        for p in page_labels
        if p.kind == "main_content"
    )


def filter_files_by_kind(
    clean_md_files: list[Path], page_labels: list[PageLabel], kind: SectionKind
) -> list[Path]:
    """Return the subset of cleaned-md files whose pages carry the given kind."""
    return [
        clean_md_files[p.page_idx] for p in page_labels if p.kind == kind
    ]


def _heading_confidence(page_labels: list[PageLabel]) -> float:
    """Heuristic: high confidence if most pages have a heading_anchor.
    Computed in _heading_classify directly via mean of per-page confidence.
    """
    if not page_labels:
        return 0.0
    return sum(p.confidence for p in page_labels) / len(page_labels)
```

### `swanki/models/problem_set.py` (NEW)

**Purpose:** Pydantic models for the solution-manual mode — problem units, card plans, provenance entries, chapter-index entries.

**Depends on:** stdlib only (`pydantic`, `typing.Literal`, `pathlib.Path`).

**Types:**

- `ProblemSubtype = Literal["theory_problem", "multiple_choice", "matching", "true_false", "completion"]` — Phase 1 wires `theory_problem` and `multiple_choice`; the others are reserved for Phase 2.
- `CardSubtype = Literal["regular", "cloze", "image", "problem_main", "subproblem", "problem_overview", "full_solution"]` — extends the implicit existing set (regular/cloze/image) with the four new problem-set kinds.
- `ProblemPart(BaseModel)` — one `(a)/(b)/(c)` part of a multi-part problem.
  - `label: str = Field(description="Part label like 'a', 'b', 'i'")`
  - `statement: str` — text of the sub-question.
  - `solution: str | None = None` — paired solution if found.
- `ProblemUnit(BaseModel)` — one numbered problem with its solution.
  - `problem_id: str = Field(description="Canonical book ID like '1.7' or 'MC-1' for unnumbered MC items")`
  - `subtype: ProblemSubtype`
  - `chapter: str | None = Field(default=None, description="Chapter number if known, e.g. '1' for Bishop CH01")`
  - `statement: str` — the question text (with cross-refs already inlined post-resolution).
  - `solution: str | None = None` — paired solution text (with cross-refs already inlined post-resolution).
  - `parts: list[ProblemPart] = Field(default_factory=list)` — populated only when `(a)/(b)/(c)` parts are detected.
  - `referenced_figures: list[str] = Field(default_factory=list, description="Figure IDs referenced (e.g. '1.4')")`
  - `referenced_equations: list[str] = Field(default_factory=list)`
  - `page_span: tuple[int, int] | None = None` — (start_page, end_page) for length heuristics.
  - `char_count: int = 0` — total character count of statement+solution after resolution; drives the >2-page overview decision.
- `CardPlan(BaseModel)` — output of the per-problem card-plan classifier.
  - `n_cards: int = Field(ge=1, le=5)` — total cards including overview/full_solution.
  - `include_main: bool = True` — always true; main card is mandatory.
  - `subproblem_labels: list[str] = Field(default_factory=list, max_length=3)` — labels of `(a)/(b)/(c)` parts to make their own cards.
  - `include_overview: bool = False` — true only when problem is "long" by config heuristic.
  - `include_full_solution: bool = False` — true when printed solution has gaps the LLM should fill, OR when length policy forces a separate uncapped card.
  - `@model_validator(mode="after") def check_n_cards_consistent(self): assert n_cards == int(include_main) + len(subproblem_labels) + int(include_overview) + int(include_full_solution)`
- `ProvenanceSpan(BaseModel)` — one annotated span in a full-solution card.
  - `text: str`
  - `origin: Literal["copy", "generated"]`
  - `source_ref: str | None = None` — pointer back to the printed-solution span (e.g. "lines 12-18 of solution") when `origin=copy`.
- `ProblemProvenance(BaseModel)` — provenance for one problem's full_solution card.
  - `problem_id: str`
  - `spans: list[ProvenanceSpan]`
- `ProvenanceLog(BaseModel)` — top-level YAML artifact wrapper.
  - `chapter_id: str | None = None`
  - `entries: list[ProblemProvenance] = Field(default_factory=list)`
- `ProblemEnumerationResponse(BaseModel)` — output for the LLM-fallback enumeration agent.
  - `problems: list[ProblemUnit]`
- `CardPlanResponse(BaseModel)` — output for the (Phase 2) LLM card-plan classifier.
  - `plan: CardPlan`
- `ProblemCardBatchResponse(BaseModel)` — output for the per-problem card generator. **Lives in `models/problem_set.py` (NOT `pipeline/problem_set.py`)** to break a circular import: `llm/agents.py` imports response types from `models/`, and `pipeline/problem_set.py` imports `problem_card_gen_agent` from `llm/agents.py`. Importing this response from a sibling pipeline module would cycle.
  - `cards: list[PlainCard | FullSolutionCard]` — union; full-solution cards are NOT a separate field. Downstream sites discriminate by `card.card_subtype`.
  - `provenance_entries: list[ProblemProvenance] = Field(default_factory=list)` — populated only when at least one full-solution card was generated.
- `ProblemLocation(BaseModel)` — where one piece of a problem (statement OR solution) lives in the document. Used when problems and their solutions sit far apart (e.g., Bishop's worked solutions appear hundreds of pages after the problem list).
  - `problem_id: str` — canonical book ID, e.g. `"1.7"`.
  - `role: Literal["statement", "solution"]`.
  - `page_idx: int` — page where the location starts.
  - `start_char: int = 0` — character offset within the page where the text begins.
  - `end_char: int` — character offset within the page where the text ends. For multi-page solutions, the location spans only the first page; additional `ProblemLocation(role="solution")` entries with later `page_idx` cover the rest.
  - `text: str` — the actual text at this location (statement or solution body).
- `ProblemPairing(BaseModel)` — one problem with its statement and zero-or-more solution locations.
  - `problem_id: str`.
  - `statement: ProblemLocation` — required.
  - `solutions: list[ProblemLocation] = Field(default_factory=list)` — empty when no solution was found.
  - `@model_validator(mode="after")` — when `solutions` is empty, set a flag the audit will read; do NOT raise here (zero-tolerance is enforced by `audit_coverage`, which can read `allow_unsolved` from config).
- `PairingResult(BaseModel)` — top-level pairing artifact. Persisted to `<output_dir>/problem-pairings.yaml` for introspection.
  - `pairings: list[ProblemPairing]`.
  - `unpaired_solutions: list[ProblemLocation] = Field(default_factory=list)` — solution-shaped text that didn't match any enumerated problem ID. Surfaces as a warning.
  - `method: Literal["regex", "llm", "mixed"]` — how the pairings were produced.
  - `confidence: float = Field(ge=0.0, le=1.0)`.
- `ProblemPairingResponse(BaseModel)` — output of the `problem_pairing_agent` Stage-3 LLM call. **Does NOT replace `PairingResult`**; the function `pair_problems_across_pages` builds the full `PairingResult` and uses this response only to merge new solution locations into existing pairings.
  - `solutions: list[ProblemLocation]` — each entry has `role="solution"` and a `problem_id` matching one of the unpaired problems passed in.

**Skeleton:**

```python
"""
swanki/models/problem_set.py
[[swanki.models.problem_set]]
https://github.com/Mjvolk3/Swanki/tree/main/swanki/models/problem_set.py
Test file: tests/test_problem_set_models.py

Pydantic models for solution-manual mode: problem units, card plans, provenance,
problem-solution pairing, the ProblemTag parser/renderer, and pydantic-ai
response wrappers (ProblemEnumerationResponse, CardPlanResponse,
ProblemCardBatchResponse, ProblemPairingResponse). Response types live here
(not pipeline/problem_set.py) to avoid a circular import with llm/agents.py.
"""

import re
from typing import Literal

from pydantic import BaseModel, Field, model_validator

from .cards import FullSolutionCard, PlainCard

ProblemSubtype = Literal[
    "theory_problem", "multiple_choice", "matching", "true_false", "completion"
]
CardSubtype = Literal[
    "regular", "cloze", "image",
    "problem_main", "subproblem", "problem_overview", "full_solution",
]


class ProblemPart(BaseModel):
    label: str = Field(description="Part label like 'a', 'b', 'i'")
    statement: str
    solution: str | None = None


class ProblemUnit(BaseModel):
    problem_id: str = Field(description="Canonical book ID like '1.7' or 'MC-1'")
    subtype: ProblemSubtype
    chapter: str | None = None
    statement: str
    solution: str | None = None
    parts: list[ProblemPart] = Field(default_factory=list)
    referenced_figures: list[str] = Field(default_factory=list)
    referenced_equations: list[str] = Field(default_factory=list)
    page_span: tuple[int, int] | None = None
    char_count: int = 0


class CardPlan(BaseModel):
    n_cards: int = Field(ge=1, le=5)
    include_main: bool = True
    subproblem_labels: list[str] = Field(default_factory=list, max_length=3)
    include_overview: bool = False
    include_full_solution: bool = False

    @model_validator(mode="after")
    def check_n_cards_consistent(self) -> "CardPlan":
        expected = (
            int(self.include_main)
            + len(self.subproblem_labels)
            + int(self.include_overview)
            + int(self.include_full_solution)
        )
        if self.n_cards != expected:
            raise ValueError(
                f"n_cards={self.n_cards} inconsistent with flags (expected {expected})"
            )
        return self


class ProvenanceSpan(BaseModel):
    text: str
    origin: Literal["copy", "generated"]
    source_ref: str | None = None


class ProblemProvenance(BaseModel):
    problem_id: str
    spans: list[ProvenanceSpan]


class ProvenanceLog(BaseModel):
    chapter_id: str | None = None
    entries: list[ProblemProvenance] = Field(default_factory=list)


class ProblemEnumerationResponse(BaseModel):
    problems: list["ProblemUnit"]


class CardPlanResponse(BaseModel):
    plan: CardPlan


class ProblemCardBatchResponse(BaseModel):
    cards: list[PlainCard | FullSolutionCard]
    provenance_entries: list[ProblemProvenance] = Field(default_factory=list)


class ProblemLocation(BaseModel):
    problem_id: str
    role: Literal["statement", "solution"]
    page_idx: int
    start_char: int = 0
    end_char: int = 0
    text: str


class ProblemPairing(BaseModel):
    problem_id: str
    statement: ProblemLocation
    solutions: list[ProblemLocation] = Field(default_factory=list)


class PairingResult(BaseModel):
    pairings: list[ProblemPairing]
    unpaired_solutions: list[ProblemLocation] = Field(default_factory=list)
    method: Literal["regex", "llm", "mixed"]
    confidence: float = Field(ge=0.0, le=1.0)


class ProblemPairingResponse(BaseModel):
    """Output of the Stage-3 LLM fallback in pair_problems_across_pages.

    The agent receives unpaired problems + unparsed review_exercises text spans;
    returns one ProblemLocation per match it finds. Omits problems it can't match.
    """

    solutions: list[ProblemLocation]


_PROBLEM_TAG_RE = re.compile(r"^([^.]+)\.problem\.([0-9]+\.[0-9]+|MC-\d+|[A-Z]+-\d+)$")


class ProblemTag(BaseModel):
    """Strongly-typed parser/renderer for the per-problem card tag.

    Replaces fragile str.startswith/removeprefix audit logic. ``parse`` returns
    None for malformed tags so downstream code can ignore non-problem tags
    cleanly.
    """

    citation_key: str
    problem_id: str

    def render(self) -> str:
        return f"{self.citation_key}.problem.{self.problem_id}"

    @classmethod
    def parse(cls, tag: str, citation_key: str) -> "ProblemTag | None":
        m = _PROBLEM_TAG_RE.match(tag)
        if m is None or m.group(1) != citation_key:
            return None
        return cls(citation_key=citation_key, problem_id=m.group(2))
```

### `swanki/pipeline/chapter_index.py` (NEW)

**Purpose:** Build, persist, and load the `chapter-index.yaml` artifact: numbered equations, figures, theorems with content, used by both `mode=full` (to emit) and `mode=solution_manual` (to resolve cross-refs).

**Depends on:** `pyyaml` (already a project dep via `pyproject.toml`), `pydantic`, regex.

> **Note:** Do NOT reuse `swanki.utils.content.extract_figure_captions` — its regex `\d+[a-z]?` only matches single-segment numbers like `"1"` or `"2a"`, NOT the dotted `"1.4"` form Schaum's and Bishop use. Write a direct dotted-form regex inline.

**Types:**

- `NumberedEquation(BaseModel)`: `id: str` (e.g. `"1.2"`), `latex: str` (the `$$...$$` content without delimiters), `page_idx: int`, `display: bool` (display vs inline).
- `NumberedFigure(BaseModel)`: `id: str`, `caption: str`, `image_path: str` (from the `![](...)` URL), `page_idx: int`.
- `NumberedTheorem(BaseModel)`: `id: str`, `kind: Literal["theorem", "lemma", "proposition", "definition", "corollary"]`, `statement: str`, `page_idx: int`.
- `ChapterIndex(BaseModel)`:
  - `chapter_id: str` — derived from `content_key` (e.g. `bishop2024_CH01`).
  - `equations: list[NumberedEquation] = Field(default_factory=list)`
  - `figures: list[NumberedFigure] = Field(default_factory=list)`
  - `theorems: list[NumberedTheorem] = Field(default_factory=list)`

**Functions:**

- `build_chapter_index(clean_md_files: list[Path], chapter_id: str) -> ChapterIndex` — scans the clean per-page markdown (post-MarkdownCleaner, where `\[...\]` is already converted to `$$...$$` per `markdown_cleaner.py:117-118`) to extract numbered items.
  - **Equations — two patterns** (must combine, not pick one):
    - **Trailing-paren form**: `r"\$\$([^$]+?)\$\$\s*(?:\(([0-9]+\.[0-9]+)\))?"` (DOTALL). Captures the LaTeX between `$$` delimiters and an optional `(N.M)` after the closing `$$`.
    - **In-block tag form**: scan `$$...$$` blocks for `\\tag\{([0-9]+\.[0-9]+)\}` inside; if matched, use the tag value as the equation ID.
    - Equations without an ID are NOT indexed (cross-references are by ID only).
  - **Figures — direct dotted-form regex** (do NOT use `extract_figure_captions`): `r"!\[([^\]]*)\]\(([^)]+)\)\s*\n+\s*(?:Fig\.|Figure)\s+([0-9]+\.[0-9]+)\s*[:|]\s*([^\n]+)"` (multiline). Group 1 = alt text, Group 2 = image_path, Group 3 = figure ID, Group 4 = caption. Ordering matters: this matches `![](url)` immediately followed by the caption block (which is how Mathpix/MarkdownCleaner emit figures per `markdown_cleaner.py:239-303`).
  - **Theorems**: regex `^(Theorem|Lemma|Proposition|Definition|Corollary)\s+([0-9.]+)[\s.:]+(.+?)(?=\n\n|\Z)` (multiline + DOTALL). Capture statement up to the next blank line or end-of-file.
  - Returns a `ChapterIndex` with `chapter_id`.
- `write_chapter_index(index: ChapterIndex, output_path: Path) -> None` — `yaml.safe_dump(index.model_dump(), ...)`.
- `load_chapter_index(yaml_path: Path) -> ChapterIndex` — `ChapterIndex.model_validate(yaml.safe_load(...))`.

**Skeleton:**

```python
"""
swanki/pipeline/chapter_index.py
[[swanki.pipeline.chapter_index]]
https://github.com/Mjvolk3/Swanki/tree/main/swanki/pipeline/chapter_index.py
Test file: tests/test_chapter_index.py

Build, persist, and load chapter-index.yaml for cross-chapter reference resolution.
"""

import re
from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, Field


class NumberedEquation(BaseModel):
    id: str
    latex: str
    page_idx: int
    display: bool = True


class NumberedFigure(BaseModel):
    id: str
    caption: str
    image_path: str
    page_idx: int


class NumberedTheorem(BaseModel):
    id: str
    kind: Literal["theorem", "lemma", "proposition", "definition", "corollary"]
    statement: str
    page_idx: int


class ChapterIndex(BaseModel):
    chapter_id: str
    equations: list[NumberedEquation] = Field(default_factory=list)
    figures: list[NumberedFigure] = Field(default_factory=list)
    theorems: list[NumberedTheorem] = Field(default_factory=list)


_EQUATION_BLOCK = re.compile(r"\$\$([^$]+?)\$\$\s*(?:\(([0-9]+\.[0-9]+)\))?", re.DOTALL)
_EQUATION_INLINE_TAG = re.compile(r"\\tag\{([0-9]+\.[0-9]+)\}")
_THEOREM = re.compile(
    r"^(Theorem|Lemma|Proposition|Definition|Corollary)\s+([0-9.]+)[\s.:]+(.+?)(?=\n\n|\Z)",
    re.MULTILINE | re.DOTALL,
)
_FIGURE_BLOCK = re.compile(
    r"!\[([^\]]*)\]\(([^)]+)\)\s*\n+\s*(?:Fig\.|Figure)\s+([0-9]+\.[0-9]+)\s*[:|]\s*([^\n]+)",
    re.MULTILINE,
)


def build_chapter_index(clean_md_files: list[Path], chapter_id: str) -> ChapterIndex:
    """Extract numbered equations, figures, theorems from cleaned per-page markdown.

    Args:
        clean_md_files: Per-page cleaned markdown (output of MarkdownCleaner).
        chapter_id: Identifier like 'bishop2024_CH01'.

    Returns:
        Populated ChapterIndex with equations, figures, theorems.
    """
    equations: list[NumberedEquation] = []
    figures: list[NumberedFigure] = []
    theorems: list[NumberedTheorem] = []

    for page_idx, md_file in enumerate(clean_md_files):
        text = md_file.read_text()

        # Equations: trailing-paren form OR in-block \tag{} form.
        for m in _EQUATION_BLOCK.finditer(text):
            latex = m.group(1).strip()
            eq_id = m.group(2)
            if eq_id is None:
                tag_match = _EQUATION_INLINE_TAG.search(latex)
                if tag_match:
                    eq_id = tag_match.group(1)
            if eq_id:
                equations.append(
                    NumberedEquation(id=eq_id, latex=latex, page_idx=page_idx)
                )

        for m in _THEOREM.finditer(text):
            kind = m.group(1).lower()
            t_id = m.group(2)
            stmt = m.group(3).strip()
            theorems.append(
                NumberedTheorem(id=t_id, kind=kind, statement=stmt, page_idx=page_idx)  # type: ignore[arg-type]
            )

        for m in _FIGURE_BLOCK.finditer(text):
            figures.append(
                NumberedFigure(
                    id=m.group(3),
                    caption=m.group(4).strip(),
                    image_path=m.group(2),
                    page_idx=page_idx,
                )
            )

    return ChapterIndex(
        chapter_id=chapter_id, equations=equations, figures=figures, theorems=theorems
    )


def write_chapter_index(index: ChapterIndex, output_path: Path) -> None:
    """Persist chapter index as YAML."""
    output_path.write_text(yaml.safe_dump(index.model_dump(), sort_keys=False))


def load_chapter_index(yaml_path: Path) -> ChapterIndex:
    """Load chapter index from YAML."""
    return ChapterIndex.model_validate(yaml.safe_load(yaml_path.read_text()))
```

### `swanki/pipeline/problem_set.py` (NEW)

**Purpose:** End-to-end solution-manual processing: enumerate problems, pair with solutions, resolve refs, classify card plans, generate cards, audit coverage. Called from `process_full` when `mode == "solution_manual"`.

**Depends on:** `swanki.models.problem_set`, `swanki.pipeline.chapter_index`, `swanki.models.cards`, `swanki.llm.agents`, `swanki.utils.content`.

**Types:** No new types are declared in this file. All response models (`ProblemEnumerationResponse`, `CardPlanResponse`, `ProblemCardBatchResponse`) live in `swanki/models/problem_set.py` (see that file's spec). This module imports them.

**Functions:**

- `enumerate_problems(clean_md_files: list[Path], chapter_id: str | None) -> list[ProblemUnit]`:
  1. Regex pass for `^(\d+)\.(\d+)\b` at line start → seed `theory_problem` units. ID = `"{chap}.{num}"`.
  2. Regex pass for `^Multiple Choice$` section header followed by `^(\d+)\.\s+(.+)` items → seed `multiple_choice` units with synthetic IDs `"MC-{n}"` (or `"MC-CH{N}-{n}"` if chapter known).
  3. (Phase 2 hooks) Sections `Matching`, `True/False`, `Completion` follow the same pattern but are not wired in v1 — the function detects them and logs a warning.
  4. If regex finds zero problems, fall back to LLM call: `problem_enumeration_agent.run_sync(prompt, ...)` returning `ProblemEnumerationResponse`. Use only on regex-failure to keep cost bounded.
  5. Always populate `page_span` from the markdown file index where the problem ID was first matched.
- `pair_problems_across_pages(problems: list[ProblemUnit], clean_md_files: list[Path], page_labels: list[PageLabel], config: dict[str, Any]) -> PairingResult`:
  - **Stage 0 — initialize.** For every enumerated `ProblemUnit`, create a `ProblemPairing(problem_id=p.problem_id, statement=ProblemLocation(role="statement", ...), solutions=[])`. The output `pairings` list ALWAYS has length == len(problems), even if no solutions are found later. This guarantees Audit Part 1 (every enumerated problem has a pairing entry) without needing to pass `problems` separately into `audit_coverage`.
  - **Stage 1 — adjacent pairing** (Schaum's inline theory-problems): if a problem's statement page contains the solution text immediately after the question, append one `ProblemLocation(role="solution", page_idx=same)` to its pairing.
  - **Stage 2 — regex pairing** (Schaum's MC + back-of-book; Bishop with explicit `Solution N.M` headings): scan all pages for `^Solution\s+(\d+)\.(\d+)` and `^Chapter\s+(\d+)\s*\n\s*Multiple Choice\s*\n\s*((?:[0-9]+\.\s*[a-z]\s*)+)` patterns. For each match, append a `ProblemLocation(role="solution", ...)` to the matching pairing. Solution markers that don't match any problem ID go into `result.unpaired_solutions`.
  - **Stage 3 — LLM fallback** (Bishop with worked-solutions PDF that lacks explicit `Solution N.M` headings):
    - **Input:** the still-unpaired problems (each with `problem_id` and `statement.text`) AND the text of every `review_exercises` page that does NOT contain a Stage-2 regex hit.
    - **Output contract:** `ProblemPairingResponse(solutions: list[ProblemLocation])` (NEW model in `models/problem_set.py`). Each `ProblemLocation.role == "solution"`. The agent omits problems it can't match — does NOT fabricate.
    - The function appends each returned location to its matching pairing.
  - **Method** in the result: `"regex"` if Stage 3 was not invoked; `"mixed"` if it was AND Stages 1-2 found anything; `"llm"` if Stages 1-2 found nothing.
  - **Persists** the result to `<output_dir>/problem-pairings.yaml`.
- `resolve_references(problem: ProblemUnit, current_chapter_index: ChapterIndex, prior_indexes: list[ChapterIndex]) -> ProblemUnit`:
  - Regex `equation\s*\(([0-9]+\.[0-9]+)\)`, `Figure\s+([0-9]+\.[0-9]+)`, `Theorem\s+([0-9]+\.[0-9]+)` in `statement` and `solution`.
  - Look up each ID first in `current_chapter_index`, then walk `prior_indexes`. On hit:
    - Equation: rewrite `"equation (1.2)"` → `"equation (1.2): $<latex>$"`.
    - Theorem: rewrite `"Theorem 2.4"` → `"Theorem 2.4 (<kind>): <statement-truncated>"` (truncate to 200 chars to keep card under cap).
    - Figure: append `image_path` to `problem.referenced_figures` so the card generator can attach it; do not rewrite the text reference (the card UI shows the image directly).
  - On miss: log `WARNING: unresolved reference {id} in problem {problem_id}`. Do NOT auto-strip — keep the visible "(equation 1.2)" reference and let coverage audit + user review surface the gap.
  - Updates `problem.char_count = len(statement) + len(solution or "")`.
- `classify_card_plan(problem: ProblemUnit, config: dict) -> CardPlan`:
  - Heuristic shortcut (no LLM call) when:
    - `problem.parts` has 0 entries AND `problem.char_count < 1500` → `CardPlan(n_cards=1, include_main=True)`.
    - `problem.parts` has 0 entries AND `problem.char_count > 4000` (>~2 pages) → `CardPlan(n_cards=2, include_main=True, include_overview=True)`.
    - `problem.parts` has N≥1 entries → `CardPlan(n_cards=1+min(3,N), include_main=True, subproblem_labels=[p.label for p in problem.parts][:3])`.
  - LLM call only when the heuristics are ambiguous (e.g., long single-part problems where the user might want a `full_solution` card to capture filled gaps): `card_plan_classifier_agent.run_sync(prompt, ...)`. Disabled by default in Phase 1 (sparse-solution detection deferred).
- `generate_cards_for_problem(problem: ProblemUnit, plan: CardPlan, doc_summary: DocumentSummary, citation_key: str, config: dict) -> tuple[list[PlainCard | FullSolutionCard], ProblemProvenance | None]`:
  - Reads system prompt from `config["prompts"]["prompts"]["solution_manual"]["problem_card_gen"]` (Hydra key path; see `swanki/conf/prompts/solution_manual.yaml` spec — keys are nested under `prompts.solution_manual.*`).
  - Builds the user prompt by formatting a template that includes: doc_summary acronyms/terms, problem.statement (resolved), problem.solution (resolved), required tags (`problem-set`, `chapter-{chapter}`, `{citation_key}.problem.{problem.problem_id}`), `plan.n_cards`, requested subtypes per plan, and citation_key.
  - **Honors `enable_full_solution_cards` flag**: if `config["pipeline"]["solution_manual"]["enable_full_solution_cards"] == False` and `plan.include_full_solution == True`, downgrade to `plan.include_full_solution = False` and decrement `plan.n_cards` before constructing the prompt. Log INFO.
  - Single LLM call via `problem_card_gen_agent.run_sync(prompt, instructions=system_prompt, model=get_model_string(...))` returning `ProblemCardBatchResponse`.
  - Each returned card already carries `card_subtype`. The pipeline trusts the LLM's subtype assignment and validates via `Pydantic`.
  - For `full_solution` cards in the batch, the response also returns a `ProblemProvenance` entry (the prompt asks the LLM to mark each emitted span with `origin: copy|generated`); we trust this annotation and persist it.
  - Returns `(response.cards, response.provenance_entries[0] if response.provenance_entries else None)`.
- `generate_cards_batched(problems: list[ProblemUnit], plans: list[CardPlan], doc_summary: DocumentSummary, citation_key: str, batch_size: int = 5) -> tuple[list[PlainCard], ProvenanceLog]`:
  - Iterates in chunks of `batch_size` calling `generate_cards_for_problem` per problem (kept simple in v1 — true batching across problems is a future optimization).
  - Aggregates cards and provenance.
- `audit_coverage(problems: list[ProblemUnit], pairings: PairingResult, cards: list[PlainCard | FullSolutionCard], citation_key: str, allow_unsolved: bool = False) -> None`:
  - **Three-part check**, all hard-fail. Pass `problems` AND `pairings` so Part 1 can verify the pairing process didn't silently drop entries.
  - **Part 1 — every enumerated problem appears in pairings.** Compute `enumerated_ids = {p.problem_id for p in problems}` and `paired_ids = {p.problem_id for p in pairings.pairings}`. If `enumerated_ids != paired_ids`, raise `CoverageError(missing=enumerated_ids - paired_ids)`. (Stage 0 of `pair_problems_across_pages` should make this impossible — this is the safety net.)
  - **Part 2 — every pairing has at least one solution** unless `allow_unsolved` is True. Compute `unsolved = {p.problem_id for p in pairings.pairings if not p.solutions}`. If unsolved and not allow_unsolved, raise `CoverageError(unsolved=unsolved)`.
  - **Part 3 — every pairing is covered by exactly one `card_subtype="problem_main"` card.** Parse main cards' tags using `ProblemTag.parse(tag, citation_key)`. Build `covered_counts: Counter[str]` keyed by `problem_id`. For each `pid` in `paired_ids`: if `covered_counts[pid] != 1`, the pid is missing (count 0) or duplicated (count > 1). Raise `CoverageError(missing=..., extra=...)` collecting both classes of failure.
  - Custom exception class `CoverageError(RuntimeError)` defined at module top, carries `missing: set[str]`, `extra: set[str]`, `unsolved: set[str]`, `duplicated: set[str]` for diagnostic.

- `class ProblemTag(BaseModel)` — strongly-typed parser/renderer for the per-problem card tag (`<citation_key>.problem.<id>`). Lives in `swanki/models/problem_set.py`. Replaces fragile `tag.startswith(...)` + `tag.removeprefix(...)` audit logic with a strict round-trip.
  - `citation_key: str`
  - `problem_id: str` — must match `^[0-9]+\.[0-9]+$` OR `^MC-\d+$` etc. (regex-validated).
  - `def render(self) -> str`: returns `f"{self.citation_key}.problem.{self.problem_id}"`.
  - `@classmethod def parse(cls, tag: str, citation_key: str) -> "ProblemTag | None"`: returns None if the tag doesn't match the strict pattern; this rejects malformed extensions like `bishop2024.problem.1.7.extra`.
- `run_problem_set_for_section(pipeline: "Pipeline", section: ContentSection, cleaned_files: list[Path], doc_summary: DocumentSummary, current_chapter_index: ChapterIndex, prior_indexes: list[ChapterIndex]) -> tuple[list[PlainCard | FullSolutionCard], list[ProblemProvenance]]`:
  - **Per-section** entry point; called from `Pipeline.process_full` once per `review_exercises` section emitted by the classifier.
  - Builds the per-section text by concatenating pages `section.start_page..section.end_page` from `cleaned_files`. If `section.paired_answer_section` is set, ALSO appends the paired section's pages so back-of-book answers travel alongside their question stems.
  - Calls `enumerate_problems(section_files, chapter_id=...)` → `pair_problems_across_pages(problems, section_files, page_labels, config)` → `resolve_references(p, current_chapter_index, prior_indexes)` per problem → `classify_card_plan(...)` per problem → `generate_cards_for_problem(...)` per problem.
  - Calls `audit_coverage(problems, pairings, cards, citation_key, allow_unsolved=...)` (hard-fail per section).
  - Returns `(cards, provenance_entries)` for this section. Caller merges across sections.
- `run_solution_manual_override(pipeline: "Pipeline", cleaned_files: list[Path], doc_summary: DocumentSummary, image_summaries: list[ImageSummary]) -> tuple[list[PlainCard | FullSolutionCard], ProvenanceLog]`:
  - **Whole-document** entry point used only when `mode=solution_manual` (explicit override). Treats the entire input as a single `review_exercises` section, skipping the classifier.
  - Loads `chapter_indexes` paths from config; calls `load_chapter_index` for each.
  - Builds `current_index = build_chapter_index(cleaned_files, chapter_id=pipeline.audio_prefix)`.
  - Calls `run_problem_set_for_section` with a synthetic `ContentSection(kind="review_exercises", start_page=0, end_page=len(cleaned_files)-1)`.
  - Persists `provenance.yaml` if any full-solution cards exist.
  - Returns `(cards, provenance_log)`.

**Skeleton:**

```python
"""
swanki/pipeline/problem_set.py
[[swanki.pipeline.problem_set]]
https://github.com/Mjvolk3/Swanki/tree/main/swanki/pipeline/problem_set.py
Test file: tests/test_problem_set.py

Solution-manual mode: enumerate problems, pair solutions, resolve refs, generate cards, audit.
"""

import logging
import re
from pathlib import Path
from typing import Any

import yaml

from ..llm.agents import (
    card_plan_classifier_agent,
    get_model_string,
    problem_card_gen_agent,
    problem_enumeration_agent,
    problem_pairing_agent,
)
from ..models.cards import FullSolutionCard, PlainCard
from ..models.document import DocumentSummary, ImageSummary
from ..models.problem_set import (
    CardPlan,
    PairingResult,
    ProblemCardBatchResponse,
    ProblemEnumerationResponse,
    ProblemLocation,
    ProblemPairing,
    ProblemProvenance,
    ProblemUnit,
    ProvenanceLog,
    ProvenanceSpan,
)
from ..models.sections import PageLabel
from .chapter_index import (
    ChapterIndex,
    build_chapter_index,
    load_chapter_index,
)

logger = logging.getLogger(__name__)


class CoverageError(RuntimeError):
    """Raised when problem coverage is incomplete."""

    def __init__(
        self,
        missing: set[str] | None = None,
        extra: set[str] | None = None,
        unsolved: set[str] | None = None,
    ) -> None:
        self.missing = missing or set()
        self.extra = extra or set()
        self.unsolved = unsolved or set()
        parts: list[str] = []
        if self.missing:
            parts.append(f"{len(self.missing)} problems not in cards: {sorted(self.missing)}")
        if self.extra:
            parts.append(f"{len(self.extra)} unexpected card IDs: {sorted(self.extra)}")
        if self.unsolved:
            parts.append(f"{len(self.unsolved)} problems with no solution: {sorted(self.unsolved)}")
        super().__init__("Coverage audit failed: " + "; ".join(parts))


_THEORY_PROBLEM = re.compile(r"^([0-9]+)\.([0-9]+)\b\s+(.+?)(?=^[0-9]+\.[0-9]+\b|\Z)",
                              re.MULTILINE | re.DOTALL)
_MC_HEADER = re.compile(r"^Multiple Choice\s*$", re.MULTILINE)
_MC_ITEM = re.compile(r"^([0-9]+)\.\s+(.+?)(?=^[0-9]+\.\s|\Z)", re.MULTILINE | re.DOTALL)
_MC_ANSWER_BLOCK = re.compile(
    r"^Chapter\s+([0-9]+)\s*\n\s*Multiple Choice\s*\n\s*((?:[0-9]+\.\s*[a-z]\s*)+)",
    re.MULTILINE,
)
_REF_EQUATION = re.compile(r"equation\s*\(([0-9]+\.[0-9]+)\)", re.IGNORECASE)
_REF_FIGURE = re.compile(r"Figure\s+([0-9]+\.[0-9]+)", re.IGNORECASE)
_REF_THEOREM = re.compile(r"Theorem\s+([0-9]+\.[0-9]+)", re.IGNORECASE)


def enumerate_problems(
    clean_md_files: list[Path], chapter_id: str | None
) -> list[ProblemUnit]:
    """Regex-first problem enumeration with LLM fallback on miss."""
    problems: list[ProblemUnit] = []
    full_text = "\n\n".join(f.read_text() for f in clean_md_files)
    chapter_num = chapter_id.split("_CH")[-1].lstrip("0") if chapter_id and "_CH" in chapter_id else None

    for m in _THEORY_PROBLEM.finditer(full_text):
        chap, num, body = m.group(1), m.group(2), m.group(3).strip()
        # Split body into statement (first paragraph) and solution (rest).
        # Schaum's puts the question on the first 1-2 lines, answer below.
        parts = body.split("\n\n", 1)
        statement = parts[0].strip()
        solution = parts[1].strip() if len(parts) > 1 else None
        problems.append(
            ProblemUnit(
                problem_id=f"{chap}.{num}",
                subtype="theory_problem",
                chapter=chap,
                statement=statement,
                solution=solution,
                char_count=len(statement) + len(solution or ""),
            )
        )

    # Multiple-choice: detect section, enumerate items inside it.
    # ... (see full implementation in __init_executor file)

    if not problems:
        # Regex found nothing. Fall back to LLM enumeration.
        # ... call problem_enumeration_agent.run_sync(...) ...
        pass

    return problems


def pair_problems_across_pages(
    problems: list[ProblemUnit],
    clean_md_files: list[Path],
    page_labels: list[PageLabel],
    config: dict[str, Any],
) -> PairingResult:
    """Build PairingResult by Stage 0 (init) → 1 (adjacent) → 2 (regex) → 3 (LLM fallback)."""
    # Stage 0: one ProblemPairing per problem, with empty solutions list.
    pairings = [
        ProblemPairing(
            problem_id=p.problem_id,
            statement=ProblemLocation(
                problem_id=p.problem_id,
                role="statement",
                page_idx=p.page_span.start_page if p.page_span else 0,
                start_char=0,
                end_char=len(p.statement),
                text=p.statement,
            ),
            solutions=[],
        )
        for p in problems
    ]
    pairings_by_id = {p.problem_id: p for p in pairings}
    unpaired_solutions: list[ProblemLocation] = []
    used_llm = False
    used_regex = False

    full_text = "\n\n".join(f.read_text() for f in clean_md_files)

    # Stage 1: adjacent — if a problem already has its solution inlined (e.g. Schaum's
    # theory-problem N.M with the answer paragraph immediately below), record it here.
    # ... walk problems, for each whose ProblemUnit.solution is not None, append a
    # ProblemLocation to its pairing.

    # Stage 2: regex pairing for ^Solution N.M and back-of-book MC blocks.
    # ... finditer over full_text; for each match, append solution to pairings_by_id[id]
    # or to unpaired_solutions if no matching id. Set used_regex=True if any match.

    # Stage 3: LLM fallback for any pairing with empty solutions.
    unpaired = [p for p in pairings if not p.solutions]
    if unpaired:
        review_text = _gather_unparsed_review_text(clean_md_files, page_labels)
        # ... build prompt: list of {problem_id, statement} + review_text spans
        prompts_root = config.get("prompts", {}).get("prompts", {})
        sm_prompts = prompts_root.get("solution_manual", {})
        system_prompt = sm_prompts.get("problem_pairing", "")
        result = problem_pairing_agent.run_sync(
            ...,  # constructed prompt
            instructions=system_prompt,
            model=get_model_string(config.get("models", {}).get("models", {}).get("llm", {})),
        )
        response: ProblemPairingResponse = result.output
        for loc in response.solutions:
            pair = pairings_by_id.get(loc.problem_id)
            if pair is not None:
                pair.solutions.append(loc)
            else:
                unpaired_solutions.append(loc)
        used_llm = True

    if used_llm and used_regex:
        method: Literal["regex", "llm", "mixed"] = "mixed"
    elif used_llm:
        method = "llm"
    else:
        method = "regex"

    return PairingResult(
        pairings=pairings,
        unpaired_solutions=unpaired_solutions,
        method=method,
        confidence=1.0 if not used_llm else 0.7,
    )


def resolve_references(
    problem: ProblemUnit,
    current_index: ChapterIndex,
    prior_indexes: list[ChapterIndex],
) -> ProblemUnit:
    """Inline equation/theorem text and collect figure refs for image attachment."""
    all_indexes = [current_index] + prior_indexes
    equations = {eq.id: eq for idx in all_indexes for eq in idx.equations}
    figures = {fig.id: fig for idx in all_indexes for fig in idx.figures}
    theorems = {t.id: t for idx in all_indexes for t in idx.theorems}

    def _inline(text: str) -> str:
        def _repl_eq(m: re.Match) -> str:
            eq_id = m.group(1)
            eq = equations.get(eq_id)
            if eq:
                return f"equation ({eq_id}): ${eq.latex}$"
            logger.warning(f"Unresolved equation reference ({eq_id}) in problem {problem.problem_id}")
            return m.group(0)

        def _repl_thm(m: re.Match) -> str:
            t_id = m.group(1)
            t = theorems.get(t_id)
            if t:
                stmt_short = t.statement[:200]
                return f"Theorem {t_id} ({t.kind}): {stmt_short}"
            logger.warning(f"Unresolved theorem reference {t_id} in problem {problem.problem_id}")
            return m.group(0)

        text = _REF_EQUATION.sub(_repl_eq, text)
        text = _REF_THEOREM.sub(_repl_thm, text)
        return text

    problem.statement = _inline(problem.statement)
    if problem.solution:
        problem.solution = _inline(problem.solution)

    # Collect figure refs for later image attachment.
    for text in [problem.statement, problem.solution or ""]:
        for m in _REF_FIGURE.finditer(text):
            fig_id = m.group(1)
            fig = figures.get(fig_id)
            if fig and fig.image_path not in problem.referenced_figures:
                problem.referenced_figures.append(fig.image_path)

    problem.char_count = len(problem.statement) + len(problem.solution or "")
    return problem


def classify_card_plan(problem: ProblemUnit, config: dict[str, Any]) -> CardPlan:
    """Heuristic-first card-plan classification with optional LLM disambiguation."""
    long_threshold = config.get("long_problem_chars", 4000)

    if problem.parts:
        n_subs = min(3, len(problem.parts))
        return CardPlan(
            n_cards=1 + n_subs,
            include_main=True,
            subproblem_labels=[p.label for p in problem.parts[:n_subs]],
        )

    if problem.char_count > long_threshold:
        return CardPlan(n_cards=2, include_main=True, include_overview=True)

    return CardPlan(n_cards=1, include_main=True)


def generate_cards_for_problem(
    problem: ProblemUnit,
    plan: CardPlan,
    doc_summary: DocumentSummary,
    citation_key: str,
    config: dict[str, Any],
) -> tuple[list[PlainCard | FullSolutionCard], ProblemProvenance | None]:
    """Single-problem card generation via problem_card_gen_agent."""
    sm_config = config.get("pipeline", {}).get("solution_manual", {})

    # Honor enable_full_solution_cards flag (Phase 1 default: False).
    if not sm_config.get("enable_full_solution_cards", False) and plan.include_full_solution:
        plan = plan.model_copy(update={
            "include_full_solution": False,
            "n_cards": plan.n_cards - 1,
        })
        logger.info(
            f"enable_full_solution_cards=False; downgrading plan for problem {problem.problem_id}"
        )

    prompts_root = config.get("prompts", {}).get("prompts", {})
    sm_prompts = prompts_root.get("solution_manual", {})
    system_prompt = sm_prompts.get("problem_card_gen", "")
    user_prompt = _format_problem_card_prompt(
        problem=problem,
        plan=plan,
        doc_summary=doc_summary,
        citation_key=citation_key,
    )

    models_config = config.get("models", {}).get("models", {}).get("llm", {})
    result = problem_card_gen_agent.run_sync(
        user_prompt,
        instructions=system_prompt,
        model=get_model_string(models_config),
    )
    response: ProblemCardBatchResponse = result.output

    # Attach figure images to card backs. card.back is CardContent for PlainCard,
    # LongFormCardContent for FullSolutionCard — both have image_path: str | None.
    for card in response.cards:
        if problem.referenced_figures and card.back.image_path is None:
            card.back.image_path = problem.referenced_figures[0]

    provenance = response.provenance_entries[0] if response.provenance_entries else None
    return response.cards, provenance


def _format_problem_card_prompt(
    problem: ProblemUnit,
    plan: CardPlan,
    doc_summary: DocumentSummary,
    citation_key: str,
) -> str:
    """Build the user prompt for problem_card_gen_agent.

    Includes resolved problem statement/solution, required tags, requested
    subtypes per plan, citation key, and acronym/terminology context.
    """
    required_tags = [
        "problem-set",
        f"chapter-{problem.chapter or 'unknown'}",
        f"{citation_key}.problem.{problem.problem_id}",
    ]
    requested_subtypes: list[str] = []
    if plan.include_main:
        requested_subtypes.append("problem_main")
    requested_subtypes.extend(["subproblem"] * len(plan.subproblem_labels))
    if plan.include_overview:
        requested_subtypes.append("problem_overview")
    if plan.include_full_solution:
        requested_subtypes.append("full_solution")

    return (
        f"Generate EXACTLY {plan.n_cards} cards for this problem.\n\n"
        f"Problem ID: {problem.problem_id}\n"
        f"Chapter: {problem.chapter}\n"
        f"Subtype: {problem.subtype}\n\n"
        f"Statement (cross-references already inlined):\n{problem.statement}\n\n"
        f"Solution:\n{problem.solution or '(no printed solution available)'}\n\n"
        f"Subproblem labels to break out: {plan.subproblem_labels}\n"
        f"Requested card_subtype values in order: {requested_subtypes}\n\n"
        f"Required tags on every card: {required_tags}\n"
        f"Citation key: {citation_key}\n\n"
        f"Document context — acronyms: {doc_summary.acronyms}\n"
        f"Document context — technical terms: {doc_summary.technical_terms}\n"
    )


def audit_coverage(
    problems: list[ProblemUnit],
    pairings: PairingResult,
    cards: list[PlainCard | FullSolutionCard],
    citation_key: str,
    allow_unsolved: bool = False,
) -> None:
    """Three-part hard-fail audit. See spec for details."""
    from collections import Counter

    enumerated_ids = {p.problem_id for p in problems}
    paired_ids = {p.problem_id for p in pairings.pairings}

    # Part 1: every enumerated problem appears in pairings.
    missing_from_pairings = enumerated_ids - paired_ids
    if missing_from_pairings:
        raise CoverageError(missing=missing_from_pairings)

    # Part 2: every pairing has at least one solution unless allow_unsolved.
    unsolved = {p.problem_id for p in pairings.pairings if not p.solutions}
    if unsolved and not allow_unsolved:
        raise CoverageError(unsolved=unsolved)

    # Part 3: every paired problem has exactly one problem_main card.
    main_card_counts: Counter[str] = Counter()
    for card in cards:
        if getattr(card, "card_subtype", "regular") != "problem_main":
            continue
        for tag in card.tags:
            parsed = ProblemTag.parse(tag, citation_key)
            if parsed is not None:
                main_card_counts[parsed.problem_id] += 1
    missing_main = {pid for pid in paired_ids if main_card_counts[pid] == 0}
    duplicated = {pid for pid in paired_ids if main_card_counts[pid] > 1}
    extra = set(main_card_counts) - paired_ids
    if missing_main or duplicated or extra:
        raise CoverageError(
            missing=missing_main, extra=extra, duplicated=duplicated
        )


def run_problem_set_for_section(
    pipeline: "Pipeline",
    section: ContentSection,
    cleaned_files: list[Path],
    doc_summary: DocumentSummary,
    current_chapter_index: ChapterIndex,
    prior_indexes: list[ChapterIndex],
    page_labels: list[PageLabel],
) -> tuple[list[PlainCard | FullSolutionCard], list[ProblemProvenance]]:
    """Per-section problem-set processing for mode=full classifier dispatch."""
    section_files = [
        cleaned_files[i] for i in range(section.start_page, section.end_page + 1)
    ]
    if section.paired_answer_section is not None:
        # ... append paired section's pages so back-of-book answers are visible ...
        pass
    problems = enumerate_problems(section_files, chapter_id=pipeline.audio_prefix)
    if not problems:
        return [], []
    pairings = pair_problems_across_pages(
        problems, section_files, page_labels, pipeline.config
    )
    problems = [
        resolve_references(p, current_chapter_index, prior_indexes) for p in problems
    ]
    plans = [classify_card_plan(p, pipeline.config.get("pipeline", {}).get("solution_manual", {})) for p in problems]

    all_cards: list[PlainCard | FullSolutionCard] = []
    provenance_entries: list[ProblemProvenance] = []
    for problem, plan in zip(problems, plans, strict=True):
        cards, prov = generate_cards_for_problem(
            problem, plan, doc_summary, pipeline.citation_key, pipeline.config
        )
        all_cards.extend(cards)
        if prov is not None:
            provenance_entries.append(prov)

    sm_config = pipeline.config.get("pipeline", {}).get("solution_manual", {})
    audit_coverage(
        problems, pairings, all_cards, pipeline.citation_key,
        allow_unsolved=sm_config.get("allow_unsolved", False),
    )
    return all_cards, provenance_entries


def run_solution_manual_override(
    pipeline: "Pipeline",
    cleaned_files: list[Path],
    doc_summary: DocumentSummary,
    image_summaries: list[ImageSummary],
) -> tuple[list[PlainCard | FullSolutionCard], ProvenanceLog]:
    """Whole-document fallback for explicit mode=solution_manual override.

    Treats the entire input as a single review_exercises section.
    """
    config = pipeline.config
    sm_config = config.get("pipeline", {}).get("solution_manual", {})
    chapter_id = pipeline.audio_prefix
    prior_indexes = [
        load_chapter_index(Path(p))
        for p in (sm_config.get("chapter_indexes", []) or [])
    ]
    current_index = build_chapter_index(cleaned_files, chapter_id=chapter_id)
    synthetic_section = ContentSection(
        kind="review_exercises", start_page=0, end_page=len(cleaned_files) - 1,
    )
    # Synthetic page_labels: every page is review_exercises for the override path.
    synthetic_page_labels = [
        PageLabel(page_idx=i, kind="review_exercises", overlap_density=1.0)
        for i in range(len(cleaned_files))
    ]
    cards, provenance_entries = run_problem_set_for_section(
        pipeline, synthetic_section, cleaned_files, doc_summary,
        current_index, prior_indexes, synthetic_page_labels,
    )
    provenance_log = ProvenanceLog(chapter_id=chapter_id, entries=provenance_entries)
    return cards, provenance_log
```

### `swanki/models/cards.py` (MODIFY)

**Current state:** `CardContent` (lines 44-622) has hard-capped 500-char `text` field; `PlainCard` (lines 625-1119) is the universal card model; `ImageCardContent` (lines 1122-1140) extends `CardContent` with required `image_summary`. `CardGenerationResponse` (lines 1184-1250) wraps `cards: list[PlainCard]`.

**Changes:**

1. **Add `card_subtype` field to `PlainCard`** as a typed, optional discriminator. Defaults preserve existing behavior (cloze/image inferred from content as today).

   Insert after the existing `audio_back_transcript` field (around line 703):

   ```python
   card_subtype: Literal[
       "regular", "cloze", "image",
       "problem_main", "subproblem", "problem_overview", "full_solution",
   ] = Field(default="regular", description="Card subtype for downstream styling/length policy")
   ```

2. **Add `LongFormCardContent` class** as a sibling of `ImageCardContent`, allowing `text` without the 500-char cap. Place immediately after `ImageCardContent` (line 1140):

   ```python
   class LongFormCardContent(BaseModel):
       """Content for full-solution cards — no length cap.

       Mirrors CardContent's fields but skips the max_length=500 constraint
       so a full worked solution (with LLM gap-filling) can be carried.
       LaTeX auto-fix and meta-content rejection still apply.
       """

       text: str = Field(..., min_length=1)
       requires_latex: bool = Field(default=False)
       audio_hint: str | None = Field(None)
       image_path: str | None = Field(None)
       image_summary: str | None = Field(None)

       @field_validator("text")
       def validate_text_content(cls, v: str) -> str:
           return _validate_card_text(v)
   ```

   Factor the existing `CardContent.validate_text_content` body (lines 96-622) into a **module-private `_validate_card_text(v: str) -> str` helper with NO length parameter**. The 500-char cap is enforced at the field level (`max_length=500` on `CardContent.text`); the validator body itself contains no length check, so the shared helper can be called as-is from both `CardContent` and `LongFormCardContent`. The cap automatically applies to `CardContent` and is automatically absent for `LongFormCardContent`.

3. **Factor tag validation into a module-private helper.** The existing `PlainCard.validate_tags` body (lines 705-741) contains pure logic that should be reused by `FullSolutionCard`. Pydantic v2's `field_validator` decorator wraps the function in a descriptor — `__func__` access is unreliable. Instead:

   ```python
   def _clean_card_tags(v: list[str]) -> list[str]:
       """Normalize tag list: strip '#' prefixes, replace underscores, drop empty,
       reject all-empty input, sanitize invalid characters. Used by both
       PlainCard.validate_tags and FullSolutionCard.validate_tags.
       """
       # ... move the body of PlainCard.validate_tags here ...
   ```

   Then in `PlainCard`:
   ```python
   @field_validator("tags", mode="before")
   def validate_tags(cls, v):
       return _clean_card_tags(v)
   ```

4. **Add `FullSolutionCard` class** after `LongFormCardContent`:

   ```python
   class FullSolutionCard(BaseModel):
       """Uncapped full-solution card for problem-set mode.

       Front uses CardContent (capped at 500). Back uses LongFormCardContent
       (uncapped). Carries the same audio/tag/id machinery as PlainCard.
       """

       front: CardContent
       back: LongFormCardContent
       tags: list[str] = Field(default_factory=list, min_length=1)
       difficulty: Literal["easy", "medium", "hard"] = "medium"
       audio_front_uri: str | None = None
       audio_back_uri: str | None = None
       card_id: str | None = None
       audio_front_transcript: str | None = None
       audio_back_transcript: str | None = None
       card_subtype: Literal["full_solution"] = "full_solution"

       @field_validator("tags", mode="before")
       def validate_tags(cls, v):
           return _clean_card_tags(v)

       @model_validator(mode="after")
       def ensure_card_id(self) -> "FullSolutionCard":
           if not self.card_id:
               self.card_id = str(uuid.uuid4())
           return self

       def to_md(
           self,
           include_audio: bool = False,
           audio_front_uri: str | None = None,
           audio_back_uri: str | None = None,
           citation_key: str | None = None,
           tag_format: str = "slugified",
       ) -> str:
           """Emit markdown identical in shape to PlainCard.to_md but with
           uncapped back text. Cloze branch is unreachable (subtype guarantees Q&A).
           Reuse the no-cloze branches of PlainCard.to_md verbatim — preferred
           approach is to factor that markdown-emission logic into a module-private
           `_card_to_md(...)` helper that both classes call.
           """
           # ... call shared _card_to_md helper or copy the regular-Q&A branches ...
   ```

   Important: do NOT add a `to_plain_card()` method — `FullSolutionCard` flows through `generate_outputs`, `to_md` writing, and APKG export as itself. The existing `AnkiProcessor`/`ApkgExporter` parse markdown (not Python objects), so they accept long-text cards without modification provided `to_md` emits valid `## front\n\nback\n\n#tags` markdown.

5. **Update `CardGenerationResponse`** to optionally accept `FullSolutionCard` entries:

   ```python
   class CardGenerationResponse(BaseModel):
       cards: list[PlainCard | FullSolutionCard] = Field(...)
       skipped_sections: list[str] = Field(default_factory=list)

       @field_validator("cards")
       def validate_card_count(cls, v):
           if len(v) == 0:
               raise ValueError("Must generate at least one card")
           return v
   ```

   This is a backward-compatible widening — existing call sites that produce only `PlainCard` keep working.

6. **Update `EnhancedCardGenerationResponse`** (line 1443) which inherits from `CardGenerationResponse`. The `cards` field is widened by inheritance — verify no overrides in this subclass redeclare a narrower type. If it does, also widen the override.

**Code diff sketch:**

```python
# swanki/models/cards.py

# 1. Factor shared validator body
def _validate_card_text(v: str, max_length: int | None) -> str:
    """Apply auto-fix + meta-content checks; enforce length only if max_length is given."""
    # ... existing lines 96-619 of CardContent.validate_text_content body ...
    if max_length is not None and len(v) > max_length:
        raise ValueError(f"Text exceeds max length {max_length}: {len(v)} chars")
    return v


class CardContent(BaseModel):
    text: str = Field(..., min_length=1, max_length=500)
    # ... unchanged fields ...

    @field_validator("text")
    def validate_text_content(cls, v):
        return _validate_card_text(v, max_length=500)


class PlainCard(BaseModel):
    # ... unchanged fields up through audio_back_transcript ...
    card_subtype: Literal[...] = Field(default="regular")  # NEW
    # ... unchanged validators ...


class ImageCardContent(CardContent):
    # ... unchanged ...


class LongFormCardContent(BaseModel):  # NEW
    text: str = Field(..., min_length=1)  # no max_length
    requires_latex: bool = False
    audio_hint: str | None = None
    image_path: str | None = None
    image_summary: str | None = None

    @field_validator("text")
    def validate_text_content(cls, v):
        return _validate_card_text(v, max_length=None)


class FullSolutionCard(BaseModel):  # NEW
    front: CardContent
    back: LongFormCardContent
    tags: list[str] = Field(default_factory=list, min_length=1)
    difficulty: Literal["easy", "medium", "hard"] = "medium"
    audio_front_uri: str | None = None
    audio_back_uri: str | None = None
    card_id: str | None = None
    audio_front_transcript: str | None = None
    audio_back_transcript: str | None = None
    card_subtype: Literal["full_solution"] = "full_solution"

    # ... validators (tag cleanup, ensure_card_id) — copy structure from PlainCard ...

    def to_md(self, include_audio: bool = False, ..., citation_key: str | None = None,
              tag_format: str = "slugified") -> str:
        # Same shape as PlainCard.to_md but uses self.back.text without 500-char cap.
        # Cloze branch is unreachable for full_solution (subtype guarantees Q&A).
        ...
```

### `swanki/llm/agents.py` (MODIFY)

**Current state:** Six pydantic-ai agents (lines 20-37). All bound to specific output models via `Agent(output_type=..., retries=N)`.

**Changes:** Add five agents at the end of the registry, before `text_agent`. All five response types live in `swanki/models/` (not `swanki/pipeline/`) to avoid circular imports — `pipeline/section_classifier.py` and `pipeline/problem_set.py` both import the agents from this file.

Add to the import block at the top of the file:

```python
from ..models.problem_set import (
    CardPlanResponse,
    ProblemCardBatchResponse,
    ProblemEnumerationResponse,
    ProblemPairingResponse,
)
from ..models.sections import ClassificationResult
```

Then add the five agents alongside the existing structured-output agents (immediately before `text_agent` at line 37):

```python
section_classifier_agent: Agent[None, ClassificationResult] = Agent(
    output_type=ClassificationResult, retries=2
)
problem_enumeration_agent: Agent[None, ProblemEnumerationResponse] = Agent(
    output_type=ProblemEnumerationResponse, retries=3
)
problem_pairing_agent: Agent[None, ProblemPairingResponse] = Agent(
    output_type=ProblemPairingResponse, retries=2
)
card_plan_classifier_agent: Agent[None, CardPlanResponse] = Agent(
    output_type=CardPlanResponse, retries=2
)
problem_card_gen_agent: Agent[None, ProblemCardBatchResponse] = Agent(
    output_type=ProblemCardBatchResponse, retries=3
)
```

System prompts are NOT bound to the agents at construction time — they are passed per-call via `agent.run_sync(prompt, instructions=...)` (see existing usage of `card_gen_agent.run_sync` in `pipeline.py:_generate_cards_for_segment`). The actual prompts come from `swanki/conf/prompts/solution_manual.yaml` — see that file's spec below.

### `swanki/pipeline/pipeline.py` (MODIFY)

**Current state:** `process_full` orchestrates the full pipeline (lines 153-449). Mode dispatch at lines 275-393. APKG path hard-coded at lines 426 and 1770. `generate_outputs` writes `cards-plain.md` and the deck (lines 1710-1826).

**Changes:**

1. **Replace the segment-driven card-gen body in `mode=full` with classifier-driven routing.** The new flow runs the classifier after `DocumentSummary`, then routes per section. Both `mode=full` and `mode=audio_only` run the classifier (audio_only needs filtered audio sources). `mode=solution_manual` (explicit override) bypasses the classifier and treats the whole document as `review_exercises`.

   ```python
   from .section_classifier import (
       classify_sections,
       filter_files_by_kind,
       merge_main_content,
   )
   from .problem_set import (
       CoverageError,
       run_problem_set_for_section,
       run_solution_manual_override,
   )

   # ... existing init, output_dir, mode read at line 209, image processing,
   #     chapter-index emission (mode in {"full", "audio_only"}), DocumentSummary ...

   # Classifier dispatch
   if mode == "solution_manual":
       # Explicit override: single synthetic review_exercises section
       self.citation_key = effective_key
       all_cards, provenance_log = run_solution_manual_override(
           self, cleaned_files, doc_summary, image_summaries
       )
       outputs = self.generate_outputs(all_cards, doc_summary, self.output_base)
       if provenance_log.entries:
           prov_path = self.output_base / "provenance.yaml"
           prov_path.write_text(
               yaml.safe_dump(provenance_log.model_dump(), sort_keys=False)
           )
           outputs["provenance"] = prov_path
       # main_content_text is empty in this mode; lecture/reading audio will use
       # the full content as a fallback (see audio source masking below).
       main_content_text: str | None = None
   else:
       # mode in {"full", "audio_only"}: classify + route
       self.state.current_stage = "section_classification"
       classification = classify_sections(
           cleaned_files, self.config, output_dir=self.output_base
       )
       logger.info(
           f"Classifier ({classification.method}, conf={classification.confidence:.2f}): "
           f"{len(classification.page_labels)} pages → {len(classification.sections)} sections"
       )
       main_content_text = merge_main_content(
           cleaned_files, classification.page_labels
       )

       if mode == "audio_only":
           all_cards = []
           outputs = {}
           self.citation_key = effective_key
       else:  # mode == "full"
           self.citation_key = effective_key
           # Build current chapter index for cross-reference resolution
           from .chapter_index import load_chapter_index
           current_index = build_chapter_index(cleaned_files, chapter_id=effective_key)
           prior_indexes = [
               load_chapter_index(Path(p))
               for p in (self.config.get("pipeline", {})
                                    .get("solution_manual", {})
                                    .get("chapter_indexes", []) or [])
           ]

           main_cards: list = []
           problem_set_cards: list = []
           provenance_entries: list = []

           # Route main_content sections into the existing segment-based card-gen.
           # Pass overlap_density via config so _generate_cards_for_segment can
           # reduce card count + inject the "avoid example questions" instruction.
           main_files = filter_files_by_kind(
               cleaned_files, classification.page_labels, "main_content"
           )
           if main_files:
               # Compute the highest overlap_density among main_content sections
               # so the modulation is uniform across the segmenter call.
               max_overlap = max(
                   (s.overlap_density for s in classification.sections
                    if s.kind == "main_content"),
                   default=0.0,
               )
               main_cards = self._generate_main_cards(
                   main_files, doc_summary, image_summaries,
                   overlap_density=max_overlap,
               )

           # Route review_exercises sections into the problem-set pipeline.
           for section in classification.sections:
               if section.kind != "review_exercises":
                   continue
               cards, prov = run_problem_set_for_section(
                   self, section, cleaned_files, doc_summary,
                   current_index, prior_indexes,
                   classification.page_labels,
               )
               problem_set_cards.extend(cards)
               provenance_entries.extend(prov)

           all_cards = main_cards + problem_set_cards
           self.state.cards_generated = len(all_cards)
           outputs = self.generate_outputs(all_cards, doc_summary, self.output_base)
           if provenance_entries:
               from ..models.problem_set import ProvenanceLog
               provenance_log = ProvenanceLog(
                   chapter_id=effective_key, entries=provenance_entries
               )
               prov_path = self.output_base / "provenance.yaml"
               prov_path.write_text(
                   yaml.safe_dump(provenance_log.model_dump(), sort_keys=False)
               )
               outputs["provenance"] = prov_path

   # main_content_text (if not None) feeds audio source masking — see step 6 below.
   ```

   `import yaml` at module top.

2. **Extract `_generate_main_cards` helper** from the existing segment-driven body (currently lines 285-393). Same logic as today (segmentation + per-segment card-gen + image-card interleaving), with three additions:
   - Accept an `overlap_density: float` parameter.
   - When `overlap_density >= 0.5` (configurable threshold from `pipeline.solution_manual.main_overlap_threshold`):
     - Multiply `cards_per_segment` and `cloze_per_segment` by `main_card_reduction_factor` (default 0.05). Round up to ≥1 if any cards are wanted at all.
     - Pass an extra instruction to the prompt body in `_generate_cards_for_segment`: "Note: this content includes numbered example questions. Treat them as illustrative; extract the underlying CONCEPTS being taught. Do NOT restate the example questions verbatim — focus on the principles, definitions, and mechanisms behind them."
   - **Handle the page-index remap correctly.** The helper receives `main_files: list[Path]` (the filtered subset of `cleaned_files`) AND the corresponding `original_page_indices: list[int]` (one entry per `main_files` item, giving its position in the original document). Char segmentation runs over `main_files` and produces segment-to-FILTERED-page maps; the helper translates back to original page indices using `original_page_indices` before any image-card lookup or `image_summaries[page_idx]` access. Specifically:

     ```python
     def _generate_main_cards(
         self,
         main_files: list[Path],
         original_page_indices: list[int],  # parallel to main_files
         doc_summary: DocumentSummary,
         image_summaries: list[ImageSummary],  # keyed by ORIGINAL page index
         overlap_density: float = 0.0,
     ) -> list[PlainCard]:
         combined, page_offsets = combine_markdown_files(main_files)
         segments = split_into_segments(combined, target_chars)
         seg_to_filtered_pages = build_segment_to_page_map(
             page_offsets, [(s, e) for _, s, e in segments], len(main_files)
         )
         # Translate each segment's filtered-page list to original-page indices.
         seg_to_original_pages = [
             [original_page_indices[fp] for fp in pages]
             for pages in seg_to_filtered_pages
         ]
         # ... per-segment card-gen + image-card interleaving uses seg_to_original_pages
         #     so image_summaries[page_idx] resolves correctly ...
     ```
   - Returns `list[PlainCard]` (existing return type).

   The classifier dispatch site in `process_full` now computes both lists together:

   ```python
   main_files: list[Path] = []
   original_page_indices: list[int] = []
   for pl in classification.page_labels:
       if pl.kind == "main_content":
           main_files.append(cleaned_files[pl.page_idx])
           original_page_indices.append(pl.page_idx)
   if main_files:
       main_cards = self._generate_main_cards(
           main_files, original_page_indices, doc_summary, image_summaries,
           overlap_density=max_overlap,
       )
   ```

2. **Widen `generate_outputs` signature** to accept the union: change the parameter type from `cards: list[PlainCard]` to `cards: list[PlainCard | FullSolutionCard]` (line 1711). Existing call sites pass `list[PlainCard]` which is a covariant subtype — no caller-side changes needed. Inside the loop body, `card.to_md(...)` is called — both `PlainCard.to_md` and `FullSolutionCard.to_md` have compatible signatures (per the `cards.py` MODIFY spec).

3. **Add `_apkg_filename(self) -> str` helper** to centralize APKG naming:

   ```python
   def _apkg_filename(self) -> str:
       """Compute the .apkg filename for this run.

       Uses content_key (via audio_prefix) as the base and appends a mode-specific
       suffix from the output config. Default suffix is empty (existing behavior).
       """
       output_config = self.config.get("output", {}).get("output", {})
       suffix = output_config.get("apkg_filename_suffix", "")
       base = self.audio_prefix if hasattr(self, "audio_prefix") else self.citation_key
       return f"{base}{suffix}.apkg"
   ```

   Replace both hard-coded sites:
   - Line 426: `apkg_path = self.output_base / f"{self.citation_key}.apkg"` → `apkg_path = self.output_base / self._apkg_filename()`
   - Line 1770: same substitution.

4. **Emit chapter-index in `mode=full`** as an additive step after image processing. Move the `mode = self.config.get("mode", "full")` read from its current position (line 276, after summary generation) to immediately after `effective_key = content_key if content_key else citation_key` (line 209). Then insert the chapter-index emission **only** in the `mode=full` branch, after image processing (line 268) and before summary generation (line 270):

   ```python
   # Inserted in the mode=full path (handled by structure of the dispatch).
   # In mode=audio_only and mode=solution_manual, this step is skipped:
   #   - audio_only doesn't need it (no downstream consumer in this run)
   #   - solution_manual doesn't index its OWN content; it consumes prior chapter indexes only.
   if mode == "full":
       from .chapter_index import build_chapter_index, write_chapter_index
       chapter_index = build_chapter_index(cleaned_files, chapter_id=effective_key)
       chapter_index_path = self.output_base / "chapter-index.yaml"
       write_chapter_index(chapter_index, chapter_index_path)
       logger.info(f"Wrote chapter index: {chapter_index_path}")
   ```

   Edge case 12 from the original draft suggested both `full` and `audio_only` should emit. Decision: **`full` only**. `audio_only` skips card generation and the chapter-index is intended for cross-chapter card resolution — emitting from `audio_only` is wasted work and could confuse downstream solution_manual runs that pull a not-quite-complete index.

5. **Add a fail-fast assertion** at the top of `process_full` (immediately after `mode` is read) to catch mode↔pipeline-preset misconfiguration:

   ```python
   if mode == "solution_manual":
       sm_segmentation = (
           self.config.get("pipeline", {}).get("processing", {}).get("segmentation")
       )
       if sm_segmentation != "none":
           raise ValueError(
               "mode=solution_manual requires pipeline=solution_manual "
               f"(processing.segmentation must be 'none', got {sm_segmentation!r}). "
               "Pass `pipeline=solution_manual` on the CLI."
           )
   ```

6. **Update help text in `swanki/__main__.py`** (separate file, called out as MODIFY below) — add `solution_manual` to the mode= line.

7. **Audit `_generate_cards_for_segment` and `_generate_image_cards_for_page`** are still called from `_generate_main_cards` (the extracted helper). Their bodies are unchanged except for the optional instruction-injection string when `overlap_density >= 0.5` (passed via a new keyword arg `extra_instructions: str = ""` defaulting to empty).

8. **Audio source masking — pass `main_content_text` to `generate_audio`.** Update `Pipeline.generate_audio` signature to accept an optional `main_content_text: str | None = None` parameter. When provided, the lecture and reading audio paths use this filtered text as their source instead of concatenating all `cleaned_files`. When `None` (the `mode=solution_manual` override case), fall back to current behavior (concatenate all cleaned files) — though in practice problem-set-only runs typically disable lecture/reading audio anyway.

   ```python
   def generate_audio(
       self,
       cards: list[PlainCard | FullSolutionCard],
       summary: DocumentSummary,
       outputs: dict[str, Path],
       cleaned_files: list[Path],
       image_summaries: list[ImageSummary],
       main_content_text: str | None = None,  # NEW
   ) -> None:
       # ... existing per-card audio dispatch ...

       lecture_source = main_content_text if main_content_text else "\n\n".join(
           f.read_text() for f in cleaned_files
       )
       # Pass lecture_source into generate_lecture_audio / generate_reading_audio
       # instead of cleaned_files.
   ```

   Wire the `main_content_text` argument through the `process_full` call site (line 411 in current code).

### `swanki/audio/card.py` (MODIFY)

**Current state:** `generate_card_audio(card: PlainCard, ...)` (lines 330-567), `generate_card_transcript(card: PlainCard, is_front: bool, ...)` (lines 32-221), `_build_transcript_system_prompt` (lines 768-893). All typed strictly as `PlainCard`. Functionally subtype-blind (only inspects `card.front.text`, `card.back.text`, `card.front.image_path`, `card.back.image_path`, `card.tags`, `card.audio_*` fields — all present on both `PlainCard` and `FullSolutionCard`).

**Changes:** Widen the type signatures to accept the union so mypy stays happy. No behavioral change.

1. **Add a type alias** at the top of `audio/card.py` (or in `models/cards.py` and re-export):

   ```python
   from ..models.cards import FullSolutionCard, PlainCard

   AnyCard = PlainCard | FullSolutionCard
   ```

2. **Update signatures**:

   ```python
   def generate_card_audio(
       card: AnyCard,
       card_index: int,
       page_base: str,
       audio_dir: Path,
       ...
   ) -> tuple[str | None, str | None]:
   ```

   ```python
   def generate_card_transcript(
       card: AnyCard,
       is_front: bool,
       model: str,
       citation_key: str,
       humanized_citation: str,
       ...
   ) -> str:
   ```

3. **Verify behavioral compatibility**: `is_cloze = "{{c" in card.front.text` (line 56) — for `FullSolutionCard` the front is `CardContent` (capped, can be cloze, but card_subtype="full_solution" is by convention Q&A, so `is_cloze` will be False). `card.front.image_path` access works on both. No further changes needed.

4. **Update call sites** in `swanki/pipeline/pipeline.py:generate_audio` to pass `cards: list[AnyCard]` (or the existing untyped iteration if no type annotation is on the loop variable).

### `swanki/audio/lecture.py` (MODIFY)

**Current state:** `generate_lecture_audio(cleaned_files: list[Path], ...)` consumes the full per-page markdown to build the lecture script.

**Changes:** Accept an optional `source_text: str | None = None`. When provided, use it as the source instead of concatenating `cleaned_files`. When `None`, fall back to current behavior. This lets the pipeline pass `main_content_text` (the filtered concatenation of `main_content` sections only) so review-exercise content is excluded from the lecture.

```python
def generate_lecture_audio(
    cleaned_files: list[Path],
    # ... existing params ...
    source_text: str | None = None,  # NEW
) -> Path | None:
    text = source_text if source_text is not None else "\n\n".join(
        f.read_text() for f in cleaned_files
    )
    # ... rest of existing implementation uses `text` instead of reading files ...
```

### `swanki/audio/reading.py` (MODIFY)

**Current state:** `generate_reading_audio(cleaned_files: list[Path], ...)` narrates the full document.

**Changes:** Same signature widening as `lecture.py`. When `source_text` is provided, use it instead. Reading audio that includes problem sets read aloud is undesirable; the filtered text excludes them.

### `swanki/audio/summary.py` — NO CHANGE.
Summary audio is generated from `DocumentSummary` (already an LLM-distilled artifact, not raw page text), so it is unaffected by the section split. Document this explicitly in the dendron note.

### `swanki/models/__init__.py` (MODIFY)

**Current state:** Re-exports `PlainCard`, `CardContent`, `CardGenerationResponse`, `CardFeedback`, `ImageCard`, `ImageCardContent`, `AudioTranscriptFeedback`, `LectureTranscriptFeedback`, `RefinementHistory`, `EnhancedCardGenerationResponse`, `DocumentSummary`, `ImageSummary`, `ProcessingState`.

**Changes:** Add re-exports for all new public types:

```python
from .cards import (
    # ... existing ...
    FullSolutionCard,        # NEW
    LongFormCardContent,     # NEW
)
from .problem_set import (
    CardPlan,                       # NEW
    CardPlanResponse,               # NEW
    CardSubtype,                    # NEW
    PairingResult,                  # NEW
    ProblemCardBatchResponse,       # NEW
    ProblemEnumerationResponse,     # NEW
    ProblemLocation,                # NEW
    ProblemPairing,                 # NEW
    ProblemPairingResponse,         # NEW (Stage-3 LLM fallback agent output)
    ProblemPart,                    # NEW
    ProblemProvenance,              # NEW
    ProblemSubtype,                 # NEW
    ProblemTag,                     # NEW (parser/renderer for {key}.problem.{id})
    ProblemUnit,                    # NEW
    ProvenanceLog,                  # NEW
    ProvenanceSpan,                 # NEW
)
from .sections import (
    ClassificationResult,    # NEW
    ContentSection,          # NEW
    PageLabel,               # NEW
    SectionKind,             # NEW
    sections_from_page_labels,  # NEW (helper for derived sections)
)
```

Update `__all__` to match.

### `swanki/__main__.py` (MODIFY)

**Current state:** CLI entry; help text at lines 116-148 lists `mode=<full|audio_only>`.

**Changes:** Update help text:

```python
mode=<full|audio_only|solution_manual>                                    Pipeline mode
```

Add an example near the bottom (around line 147):

```python
swanki pdf_path=ch01.pdf citation_key=alcamo2010 +content_key=alcamo2010_CH01 \
       mode=solution_manual pipeline=solution_manual \
       'pipeline.solution_manual.chapter_indexes=[/path/to/prior_ch.yaml]'
```

### `swanki/conf/config.yaml` (MODIFY)

**Current state:** lines 1-26. `mode: full` is already a top-level key.

**Changes:** No schema change — `mode: solution_manual` is a value override on the existing key. Document the new value in a comment:

```yaml
# mode: full         # default — segment-based card generation
# mode: audio_only   # skip cards, just audio
# mode: solution_manual  # problem-set PDFs (Schaum's, Bishop) — see pipeline=solution_manual
mode: full
```

### `swanki/conf/pipeline/solution_manual.yaml` (NEW)

This preset is now a SHARED settings block for the problem-set + classifier behavior, used by every `mode=full` run (which always activates the classifier-driven routing). The Hydra defaults list in `config.yaml` still selects `pipeline: default`, which carries the existing segmenter knobs. The `pipeline: solution_manual` preset is selected when the user wants the explicit override (`mode=solution_manual`) which forces problem-set-only output.

**Content:**

```yaml
defaults:
  - default
  - _self_

processing:
  # When pipeline=solution_manual is explicitly selected, skip segmentation
  # (whole document is treated as review_exercises). For default mode=full,
  # the user keeps pipeline=default and segmentation runs only on main_content
  # sections per the classifier output.
  segmentation: none
  image_cards:
    enabled: false  # solution_manual override doesn't use page-driven image cards

solution_manual:
  chapter_indexes: []  # list of paths to prior-chapter chapter-index.yaml artifacts
  long_problem_chars: 4000  # threshold above which include_overview=True
  batch_size: 5  # problems per LLM card-gen call (currently 1; reserved for future batching)
  enable_full_solution_cards: false  # Phase 1: leave off; turn on once gap-filling provenance is validated
  enable_llm_classifier: false  # Phase 1: heuristic-only card-plan classification
  coverage_audit: true  # hard-fail when problems are not covered
  # Section classifier knobs — apply to mode=full as well.
  section_classifier_min_confidence: 0.7  # below this, fall back to LLM classifier
  main_overlap_threshold: 0.5  # main_content sections at or above this density get reduced cards + instruction injection
  main_card_reduction_factor: 0.05  # multiplier on cards_per_segment / cloze_per_segment when overlap is high
  classification_override: null  # optional path to a hand-edited section-classification.yaml; when set, classifier is skipped and this file is used verbatim
  allow_unsolved: false  # when True, the audit accepts problems with no paired solution. Default False = zero-tolerance (audit raises CoverageError if any problem is unsolved).
```

The `solution_manual` block is read by both `mode=full` (classifier always runs, problem-set sections route through `run_problem_set_for_section`) and `mode=solution_manual` (override; skips classifier, calls `run_solution_manual_override`). The `processing.segmentation: none` only takes effect for the explicit override; under `pipeline: default`, segmentation continues to run on the filtered `main_content` text.

### `swanki/conf/output/default.yaml` (MODIFY) or `swanki/conf/output/problem_set.yaml` (NEW)

Two equivalent options. Pick one:

**Option A (preferred): add `apkg_filename_suffix: ""` to default.yaml** so all modes pick up the new key:

```yaml
output:
  base_dir: swanki-out
  formats:
    cards_plain: cards-plain.md
    cards_audio: cards-with-audio.md
    cards_combined: cards-combined.md
    summary: document-summary.md
  organize_by_type: true
  create_anki_deck: true
  tag_format: slugified
  apkg_filename_suffix: ""  # NEW; mode-specific overrides supply suffixes like "-problem-set"
```

Then add `swanki/conf/output/problem_set.yaml`:

```yaml
defaults:
  - default
  - _self_

output:
  apkg_filename_suffix: "-problem-set"
```

User invokes with `output=problem_set` to get `<key>-problem-set.apkg`.

### `swanki/conf/refinement/solution_manual.yaml` (NEW)

**Content:** Inherit from `default.yaml` and add three card-type-specific feedback prompts. The pipeline's `_self_refine_cards` looks up `feedback_prompts[f"{card_type}_cards"]`, so the keys must be `problem_main_cards`, `subproblem_cards`, `problem_overview_cards`, `full_solution_cards`.

```yaml
defaults:
  - default
  - _self_

refinement:
  content_types:
    - problem_main
    - subproblem
    - problem_overview
    - full_solution
  feedback_prompts:
    problem_main_cards: |-
      Check these problem-main cards from a textbook problem set:
      1. Self-containment: every reference (equation, figure, theorem) must be inlined or
         attached as an image — no "see equation (1.2)" without the equation visible.
      2. Problem identity: the front should preserve the book's problem number as a label
         ("Bishop, Problem 1.7: ...") but the actual question content is also visible.
      3. Length: ≤500 chars. If the printed solution is longer, this main card carries
         a high-level / final-result view, not the full walkthrough.
      4. Tags: must include #problem-set, #chapter-{chapter}, and #{citation_key}.problem.{id}.

      If all cards meet standards, set done=True.
    subproblem_cards: |-
      Check these subproblem cards (one per (a)/(b)/(c) part):
      1. Independence: each card stands alone — the learner can answer it without seeing the parent problem statement.
      2. Length: ≤500 chars per back. Compress mechanical steps; show key intermediate results.
      3. Tags: include the parent problem tag plus #subproblem.{label}.

      If all cards meet standards, set done=True.
    problem_overview_cards: |-
      Check overview cards (high-level walkthrough for problems >2 pages):
      1. Step list: 3-7 numbered or bulleted steps capturing the solution's logical flow.
      2. No detailed derivation — that belongs in subproblem cards or the full-solution card.
      3. Length: ≤500 chars.

      If all cards meet standards, set done=True.
    full_solution_cards: |-
      Check full-solution cards (uncapped, complete walkthrough with gap-filling):
      1. Self-containment as for problem_main, but with full step-by-step detail.
      2. LLM-generated spans must be marked in the provenance entry (origin: generated).
      3. Math correctness: any filled-in derivation must be mathematically valid.
      4. No length cap, but prefer concise explanation over verbose padding.

      If all cards meet standards, set done=True.

  refinement_prompts:
    problem_main_cards: |-
      Fix all issues identified in feedback. Maintain the problem-number label on the front.
      Inline any unresolved references (equation, figure, theorem) using the provided chapter index data.
    subproblem_cards: |-
      Fix all issues. Each card must stand alone — duplicate any context the learner needs.
    problem_overview_cards: |-
      Fix step-list issues. Aim for 3-7 high-level steps with intermediate results.
    full_solution_cards: |-
      Fix all issues. Update the provenance entry to reflect any new generated spans.
```

In v1 (Phase 1), `enable_full_solution_cards: false` in the pipeline preset means the full_solution feedback prompt is unused; keep it in place for Phase 2.

### `swanki/conf/prompts/solution_manual.yaml` (NEW)

**Content:** System prompts for the three new agents. Keys are nested under `prompts.solution_manual.*` to match the existing two-level convention in `swanki/conf/prompts/default.yaml` (`prompts.summary.*`, `prompts.cards.*`, `prompts.audio.*`). Pipeline reads via `config["prompts"]["prompts"]["solution_manual"]["problem_card_gen"]`.

```yaml
defaults:
  - default
  - _self_

prompts:
  solution_manual:
    section_classifier: |-
      You receive a sample of cleaned markdown from a textbook chapter PDF. Classify the document
      into a sequence of contiguous ContentSections with kind in {main_content, review_exercises,
      front_matter, back_matter}.

      - main_content: chapter body that teaches concepts. Even if it contains numbered Q&A
        ("1.1 What is X? Answer: ..."), it counts as main_content because it IS the chapter.
        For these sections, set overlap_density in [0,1] based on what fraction is problem-shaped.
      - review_exercises: end-of-chapter sections labeled Multiple Choice, Matching, True/False,
        Completion, Review Questions, Problems, Exercises, Practice — i.e., assessment material
        with paired or appended solutions. Set overlap_density=1.0.
      - front_matter: Copyright, Preface, Table of Contents, Dedication.
      - back_matter: Index, Glossary, Bibliography UNLESS the back-matter contains an
        "Answers to Review Questions" / "Solutions" block, in which case re-classify that span
        as review_exercises and set its paired_answer_section to the index of the corresponding
        question section (matched by chapter number).

      Cover every page. Do not invent sections. Set confidence appropriately.
    main_with_overlap_instruction: |-
      Note: this content includes numbered example questions or theory-problem Q&A blocks.
      Treat them as illustrative examples, NOT as content to memorize verbatim. Extract the
      underlying CONCEPTS, principles, definitions, and mechanisms being taught through the
      examples. Do NOT generate cards that restate the example questions. Generate
      concept-focused cards that a student would benefit from regardless of having seen the
      specific examples.
    problem_enumeration: |-
      You receive cleaned markdown from a textbook chapter (problems + solutions). List every
      numbered problem with its canonical book ID, subtype, and statement. Subtypes: theory_problem,
      multiple_choice, matching, true_false, completion. Preserve the book's numbering exactly
      (e.g. '1.7'). For Multiple-Choice items without book-level IDs, synthesize 'MC-{n}'.
      Do not invent problems. Do not skip problems. Do not generate solutions.
    problem_pairing: |-
      You receive a list of enumerated problems (each with id and statement) and a set of text
      spans from the document's review_exercises pages that did NOT match any explicit
      "Solution N.M" marker via regex. For each problem still missing a solution, find the span
      whose content answers it and return a ProblemLocation entry with role=solution.
      Match by content (the solution should derive or compute what the problem asks for), not
      by position. If no span matches a problem, omit it from your output — do NOT fabricate
      a solution. The pipeline's coverage audit will surface the gap.
    problem_card_gen: |-
      You receive one problem (statement + solution, with cross-references already inlined) and a
      CardPlan describing exactly how many cards to emit. Generate exactly the cards specified
      with the requested card_subtype values in order.
      Each card must be self-contained: every referenced equation, theorem, or figure is already
      inlined in the statement/solution text — do NOT add bare references like "see equation (1.2)".
      Carry book-numbering as a label on the front ("Problem 1.7: ...") and as a tag (see required tags).
      Respect the 500-char limit on every back text EXCEPT full_solution cards (which use
      LongFormCardContent and have no length cap).
      For full_solution cards, populate provenance_entries with one ProblemProvenance whose spans
      annotate the card.back.text: each span has origin: copy (with source_ref) or origin: generated.
      Spans must concatenate (in order) to the back.text exactly.
    card_plan_classifier: |-
      You receive one problem unit. Decide n_cards (1-5), which subproblem labels to expand,
      whether to include an overview card, and whether to include a full_solution card with
      gap-filling. Default to the heuristic in the prompt unless ambiguity is high.
```

### `scripts/schaum_chapter_pack.py` (NEW)

**Purpose:** Preprocessing helper for Schaum's-style books. Takes a cleaned PDF + chapter page range + answer-key page range, produces a per-chapter PDF with the answer key appended.

**Functions:**

- `pack_chapter(source_pdf: Path, chapter_pages: tuple[int, int], answer_key_pages: tuple[int, int], output_pdf: Path) -> None`:
  - Use `qpdf source_pdf --pages . {a}-{b} -- /tmp/range_chapter.pdf`
  - Use `qpdf source_pdf --pages . {c}-{d} -- /tmp/range_answers.pdf`
  - Use `pdfunite /tmp/range_chapter.pdf /tmp/range_answers.pdf {output_pdf}`
  - Clean up tmp files.
- `main()`: argparse entry point. Args: `--source`, `--chapter-pages "8-18"`, `--answer-key-pages "328-336"`, `--output`.

**Skeleton:**

```python
"""
scripts/schaum_chapter_pack.py
[[scripts.schaum_chapter_pack]]
https://github.com/Mjvolk3/Swanki/tree/main/scripts/schaum_chapter_pack.py

Preprocess a Schaum's-style book by chopping one chapter's pages and the back-of-book
answer key region, concatenating into a single PDF for solution_manual mode.

Usage:
    python scripts/schaum_chapter_pack.py \
        --source /scratch/alcamoSchaumsOutlineMicrobiology2010_clean.pdf \
        --chapter-pages 8-18 \
        --answer-key-pages 328-336 \
        --output /scratch/alcamo_CH01_packed.pdf
"""

import argparse
import subprocess
import tempfile
from pathlib import Path


def pack_chapter(
    source_pdf: Path,
    chapter_pages: tuple[int, int],
    answer_key_pages: tuple[int, int],
    output_pdf: Path,
) -> None:
    """Chop chapter pages and answer-key region, concatenate into one PDF."""
    with tempfile.TemporaryDirectory() as tmpdir:
        chapter_pdf = Path(tmpdir) / "chapter.pdf"
        answers_pdf = Path(tmpdir) / "answers.pdf"
        subprocess.run(
            ["qpdf", "--warning-exit-0", str(source_pdf),
             "--pages", ".", f"{chapter_pages[0]}-{chapter_pages[1]}",
             "--", str(chapter_pdf)],
            check=True,
        )
        subprocess.run(
            ["qpdf", "--warning-exit-0", str(source_pdf),
             "--pages", ".", f"{answer_key_pages[0]}-{answer_key_pages[1]}",
             "--", str(answers_pdf)],
            check=True,
        )
        subprocess.run(
            ["pdfunite", str(chapter_pdf), str(answers_pdf), str(output_pdf)],
            check=True,
        )


def _parse_range(spec: str) -> tuple[int, int]:
    a, b = spec.split("-")
    return int(a), int(b)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--chapter-pages", required=True, type=_parse_range)
    parser.add_argument("--answer-key-pages", required=True, type=_parse_range)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    pack_chapter(args.source, args.chapter_pages, args.answer_key_pages, args.output)
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
```

### `tests/test_problem_set.py` (NEW)

**Test cases:**

- `test_enumerate_problems_theory_problem` — fixture has three numbered problems `1.1`, `1.2`, `1.3`; assert all three IDs returned with correct statement/solution split.
- `test_enumerate_problems_multiple_choice` — fixture has `Multiple Choice` section with 5 items + back-of-book answers; assert IDs `MC-1`..`MC-5` returned with letter answers paired.
- `test_pair_problems_with_back_of_book_key` — fixture has appended `Chapter 1 / Multiple Choice / 1. c 2. c ...` block; assert solutions populated correctly.
- `test_resolve_references_inlines_equation` — `ProblemUnit` references `equation (1.2)`; supplied `ChapterIndex` has eq 1.2; assert text rewritten to include `$<latex>$`.
- `test_resolve_references_attaches_figure` — references `Figure 1.4`; assert `referenced_figures` populated.
- `test_resolve_references_unresolved_logs_warning` — references nonexistent `equation (9.9)`; assert warning logged, text unchanged.
- `test_classify_card_plan_short_problem` — `char_count=500` → `n_cards=1`.
- `test_classify_card_plan_long_problem` — `char_count=5000` → `n_cards=2, include_overview=True`.
- `test_classify_card_plan_with_parts` — 3 parts → `n_cards=4, include_main=True, subproblem_labels=["a","b","c"]`.
- `test_classify_card_plan_caps_subproblems_at_3` — 5 parts → `subproblem_labels` truncated to 3.
- `test_audit_coverage_part1_passes_when_all_paired` — 3 enumerated, 3 pairings with one solution each, 3 main cards with matching tags; assert no raise.
- `test_audit_coverage_part1_raises_when_pairing_dropped` — pass `pairings` with only 2 of 3 problem IDs; assert `CoverageError(missing={"3.1"})` raised.
- `test_audit_coverage_part2_raises_on_unsolved_default` — pairing for `1.1` has empty `solutions`; assert `CoverageError(unsolved={"1.1"})` raised when `allow_unsolved=False`.
- `test_audit_coverage_part2_passes_with_allow_unsolved` — same fixture with `allow_unsolved=True`; assert no raise.
- `test_audit_coverage_part3_raises_on_duplicate_main_card` — 1 enumerated problem, 2 `problem_main` cards both tagged `key.problem.1.1`; assert `CoverageError(duplicated={"1.1"})` raised.
- `test_audit_coverage_part3_raises_on_extra_card` — 0 problems enumerated, 1 main card tagged `key.problem.9.9`; assert `CoverageError(extra={"9.9"})` raised.
- `test_audit_coverage_problem_tag_rejects_malformed` — main card tagged `key.problem.1.1.extra`; `ProblemTag.parse` returns None; the tag is ignored; if no other main card covers `1.1`, raise `CoverageError(missing={"1.1"})`.
- `test_problem_tag_round_trip` — `ProblemTag(citation_key="bishop2024", problem_id="1.7").render()` returns `"bishop2024.problem.1.7"`; `ProblemTag.parse(rendered, "bishop2024")` returns the same model; `parse("bogus", ...)` returns None.
- `test_pair_adjacent_inline_solutions` — Schaum's-style fixture with inline `1.1` Q&A; assert `PairingResult.method == "regex"` and every pairing has exactly one solution location on the same page as the statement.
- `test_pair_far_apart_via_solution_marker` — Bishop-style fixture: problems on pages 1-2, `## Solution 1.7` heading on page 5 with 3 paragraphs; assert pairing links problem `1.7` to the page-5 solution span.
- `test_pair_back_of_book_mc_answers` — Schaum's-style fixture: `Multiple Choice` stems on page 2, `Chapter 1 / Multiple Choice / 1. c 2. c ...` block on page 8; assert each MC pairing carries a `ProblemLocation(role="solution")` pointing to page 8 with the letter answer expanded to the full choice text.
- `test_pair_llm_fallback_invoked_for_unmatched` — fixture has problems and worked solutions but NO explicit `Solution N.M` markers; mock `problem_pairing_agent.run_sync` to return one `ProblemLocation` per problem; assert it's called and result.method == `"mixed"`.
- `test_pair_unsolved_recorded_not_raised` — fixture problem `2.1` has no matching solution span anywhere; assert `PairingResult.pairings` includes problem `2.1` with empty `solutions`, and audit (with default `allow_unsolved=False`) hard-fails with `unsolved={"2.1"}` on `CoverageError`.
- `test_pair_unpaired_solutions_logged` — fixture has a `## Solution 9.9` block but no problem `9.9` enumerated; assert that span goes into `PairingResult.unpaired_solutions` and a WARNING is logged.
- `test_enumerate_problems_llm_fallback_invoked_on_regex_miss` — fixture with no `N.M` numbering; mock `problem_enumeration_agent.run_sync` and assert it's called.
- `test_multi_chapter_problem_id_collision` — two `ProblemUnit` instances both with `problem_id="1.1"` but different `chapter` fields; assert coverage audit treats them as distinct (audit groups by (chapter, problem_id)).
- `test_full_solution_card_markdown_round_trip` — construct a `FullSolutionCard` with 3000-char back; call `to_md`; pass through `AnkiProcessor.extract_cards`/`prepare_for_anki`; assert no truncation and valid HTML output.
- `test_run_problem_set_end_to_end_smoke` (integration, `@pytest.mark.integration`) — small Schaum's fixture, mocked `problem_card_gen_agent.run_sync` returning hand-crafted cards, assert pipeline produces a `.apkg` containing problem-set cards and (when full-solution cards are present) `provenance.yaml`.

**Markers:** Mostly unit tests (no marker). The end-to-end smoke test is `@pytest.mark.integration`. No `@pytest.mark.llm` markers — all LLM calls are mocked.

**Fixtures:** Add `tests/fixtures/problem_set/` (NEW directory; `tests/fixtures/` does not currently exist, must be created at the same time):

- `schaum_ch01_clean.md` — sketch:
  ```markdown
  # CHAPTER 1 / Introduction to Microbiology

  ## Theory and Problems

  1.1  What is microbiology?
  Microbiology is the study of microorganisms — bacteria, viruses, fungi, and protozoa.

  1.2  Who first observed microorganisms?
  Anton van Leeuwenhoek made systematic observations starting in the 1670s using single-lens microscopes of his own design.

  1.3  What is the germ theory of disease?
  The germ theory of disease, developed by Louis Pasteur and Robert Koch, holds that specific microorganisms cause specific diseases.

  ## Multiple Choice

  1. Among microorganisms studied in microbiology are
  (a) elephants
  (b) trees
  (c) viruses and bacteria
  (d) crystals

  2. The first scientist to observe microorganisms was
  (a) Robert Koch
  (b) Louis Pasteur
  (c) Anton van Leeuwenhoek
  (d) James Watson

  ## Answers to Review Questions

  ### Chapter 1

  Multiple Choice
  1. c 2. c
  ```

- `bishop_ch01_clean.md` — short fixture with one numbered problem referencing equation `(1.2)` from a (mock) prior chapter:
  ```markdown
  # Chapter 1 / Linear Models

  ## 1.7  Show that the squared-error loss reduces to MSE.

  Using equation (1.2), the per-sample loss is $\ell_i = (y_i - \hat{y}_i)^2$. Summing
  and dividing by N yields the mean squared error.
  ```

- `prior_chapter_index.yaml`:
  ```yaml
  chapter_id: bishop2024_CH00
  equations:
    - id: "1.2"
      latex: "y = w^T x + b"
      page_idx: 5
      display: true
  figures: []
  theorems: []
  ```

### `tests/test_chapter_index.py` (NEW)

**Test cases:**

- `test_build_chapter_index_extracts_tagged_equations` — fixture markdown has `$$ y = mx + b $$ \n (1.2)`; assert one equation with id="1.2".
- `test_build_chapter_index_extracts_theorem` — fixture has `Theorem 2.4: For all real x, ...`; assert one theorem with id="2.4", kind="theorem".
- `test_build_chapter_index_extracts_figure` — fixture has `![Cell diagram](images/cell.png)\n\nFigure 1.4: A representation of...`; assert one figure with id="1.4", image_path="images/cell.png".
- `test_chapter_index_round_trip_yaml` — build → write → load → assert equal.

**Markers:** none (pure unit tests).

### `tests/test_problem_set_models.py` (NEW)

**Test cases:**

- `test_card_plan_consistency_validator_passes` — `CardPlan(n_cards=4, include_main=True, subproblem_labels=["a","b","c"])` constructs cleanly.
- `test_card_plan_consistency_validator_fails` — `CardPlan(n_cards=5, include_main=True, subproblem_labels=["a"])` raises ValueError.
- `test_card_plan_n_cards_max_5` — `CardPlan(n_cards=6, ...)` raises.
- `test_problem_unit_round_trip` — construct, dump, validate; identity.
- `test_provenance_log_yaml_serialization` — round-trip via `yaml.safe_dump`/`yaml.safe_load`.

### `tests/test_models_validation.py` (MODIFY)

**Current state:** Existing tests for `CardContent`, `PlainCard`, `ImageCardContent`, `CardGenerationResponse`. (Note: file is `tests/test_models_validation.py`, NOT `test_card_models.py` — verify path before opening.)

**Changes:** Add tests for the new types:

- `test_long_form_card_content_uncapped` — construct with 2000-char text; assert no validation error.
- `test_long_form_card_content_validates_braces` — text with unbalanced braces auto-fixed (validates that the shared `_validate_card_text` helper still applies the auto-fix).
- `test_full_solution_card_construction` — front 500-char + back 2000-char + tags; constructs cleanly; `card_subtype == "full_solution"`.
- `test_plain_card_card_subtype_default` — `PlainCard(...)` defaults to `card_subtype="regular"`.
- `test_plain_card_card_subtype_problem_main` — explicit `card_subtype="problem_main"` accepted.
- `test_card_generation_response_accepts_full_solution_card` — `CardGenerationResponse(cards=[FullSolutionCard(...)])` constructs cleanly.

### `tests/test_main_cards_image_remap.py` (NEW)

**Test cases:**

- `test_filtered_page_idx_translates_to_original` — given `cleaned_files=[a,b,c,d,e]` and `page_labels` marking pages [0, 2, 4] as `main_content` and [1, 3] as `review_exercises`, assert `_generate_main_cards`'s segment-to-page map translates filtered indices `[0, 1, 2]` back to original indices `[0, 2, 4]`.
- `test_segment_spanning_filtered_pages_maps_to_correct_original_pages` — fabricate three short main_content pages and one long page so a single char segment spans two filtered pages; assert it maps to the correct two original page indices (skipping the review_exercises pages between them).
- `test_image_summary_lookup_succeeds_after_remap` — mock `image_summaries[page_idx]` for original indices [0, 2, 4]; run `_generate_main_cards` over filtered files; assert image-card interleaving accesses the correct image summaries (no IndexError, no wrong-image attachment).

**Markers:** none (pure unit tests).

### `tests/test_pipeline_mode.py` (MODIFY)

**Current state:** Tests for `mode=full` vs `mode=audio_only` dispatch.

**Changes:** Add tests for `mode=solution_manual`:

- `test_mode_solution_manual_dispatch` — config with `mode=solution_manual` calls `run_solution_manual_override` (mocked); the section classifier is NOT invoked; `_generate_cards_for_segment` is NOT called.
- `test_mode_full_classifier_dispatch` — config with `mode=full` calls `classify_sections` and routes both `main_content` (via `_generate_main_cards`) and `review_exercises` (via `run_problem_set_for_section`) sections; mock both helpers.
- `test_mode_solution_manual_writes_chapter_index_in_full_mode` — `mode=full` run writes `chapter-index.yaml` to output dir.
- `test_apkg_filename_helper_default` — `Pipeline._apkg_filename()` returns `"<key>.apkg"` when `apkg_filename_suffix=""`.
- `test_apkg_filename_helper_with_suffix` — returns `"<key>-problem-set.apkg"` when suffix set.

### Dendron notes (NEW)

- `notes/swanki.pipeline.problem_set.md`
- `notes/swanki.pipeline.chapter_index.md`
- `notes/swanki.models.problem_set.md`
- `notes/scripts.schaum_chapter_pack.md`

Each should follow the existing dendron-note pattern (frontmatter with id/title/desc/timestamps), include a one-paragraph module description, and have a dated section recording the initial implementation.

## Edge Cases

1. **Regex enumeration fails entirely.** Some chapters may not use `N.M` numbering (e.g., a chapter with only end-of-chapter exercises). `enumerate_problems` falls back to `problem_enumeration_agent` for full LLM-driven extraction. Result must still validate against `ProblemUnit` schema.
2. **Empty chapter index.** `build_chapter_index` returns `ChapterIndex(equations=[], figures=[], theorems=[])` for chapters without numbered items. `resolve_references` gracefully no-ops.
3. **Reference to a chapter that wasn't supplied.** `equation (5.3)` referenced from Ch7 work, but no `ch5_chapter-index.yaml` provided. Resolver logs warning, leaves text unchanged. Coverage audit still passes (the *problem* is covered; the *reference* is just unresolved). User must supply more indexes or accept the warning.
4. **Solution genuinely missing for a problem.** A Schaum's MC item with no back-of-book answer entry, or a Bishop problem the worked-solutions PDF doesn't cover. `pair_problems_across_pages` leaves the pairing's `solutions` empty. The audit's Part 2 then hard-fails the run unless the user explicitly sets `pipeline.solution_manual.allow_unsolved=True`. With the flag set, unsolved problems still get a `problem_main` card carrying just the question; the audit logs but does not raise. Default is False — zero-tolerance.
5. **Card subtype mismatch in LLM output.** LLM emits a `card_subtype="subproblem"` card without matching the planned subproblem labels. Pydantic validation passes (subtype is just an enum), but coverage logic checks the parent problem ID via tags — extra subproblem cards don't break coverage as long as the main card is present.
6. **Long-text full-solution card breaks audio.** Text > 5000 chars chunks into 5+ TTS calls. Existing `chunk_text`/`combine_audio` handles this; only concern is processing time. Acceptable for v1.
7. **Same problem ID appears in multiple chapters.** Schaum's reuses `1.1` across chapters. The `ProblemUnit.chapter` field disambiguates; coverage audit groups by `(chapter, problem_id)` not just `problem_id`. Tags include `#chapter-{chapter}` for downstream filtering.
8. **MC stem with multi-line choices.** Some MC questions span multiple lines per choice. Regex for `\([a-d]\)\s+(.+)` is greedy enough to capture multi-line; manual review on first run.
9. **Underline-based True/False (Phase 2).** Mathpix may not preserve `\underline{...}`. Phase 2 will need either an OCR mode flag or LLM inference comparing the original statement to the answer-key correction word.
10. **APKG suffix collides with existing output.** If user already has `<key>.apkg` and now generates `<key>-problem-set.apkg`, both coexist. The auto-increment logic (lines 233-240 of pipeline.py) only counters output *directories*, not files within. Acceptable: separate suffix avoids collision.
11. **Coverage audit blocks output for hours of work.** A failure mode: enumeration finds 40 problems, generation fails to produce cards for problem 23, coverage hard-fails after consuming all the LLM budget. Mitigation: log progress per problem, persist cards-so-far to disk, and let user inspect.
12. **Chapter-index emission accidentally runs in audio_only mode.** Audio-only doesn't need an index but emitting it is cheap and additive — the index is built from cleaned markdown which audio_only does produce. Decision: emit for both `full` and `audio_only` modes, skip only for `solution_manual` (which has no incoming chapter to index).

13. **Char chunking and page labels.** The existing pipeline cuts the document into ~6000-character chunks ("segments") for card generation. The classifier labels whole pages. To keep these compatible:
    - **Filter pages first, then chunk.** `_generate_main_cards` only sees pages labeled `main_content`. Each chunk is therefore made entirely from `main_content` text — no chunk mixes content kinds.
    - **Track original page numbers.** When we filter pages, page #2 in the filtered list might be page #5 in the original document. We pass an `original_page_indices` list alongside the filtered files so image lookups (`image_summaries[page_idx]`) use the right page number. Tested by `test_main_cards_image_remap`.
    - **Limit: a transition mid-page gets misrouted.** If a single PDF page starts with `main_content` text and a `## Multiple Choice` heading appears halfway down, the page gets one label and the other ~half page of text is sent to the wrong pipeline. Schaum's Ch1 has all transitions on page breaks (pages 8-15 are theory-problems, 16-18 are MC review, 328-336 are answer key) so this isn't hit. When a chapter does hit it: the user can either hand-edit `section-classification.yaml` and re-run with `classification_override`, or rely on the LLM fallback classifier. A future improvement is to label *heading regions* inside a page rather than whole pages; recorded as a known limit, not blocking for v1.

## Verification

After each file is implemented:

1. **Unit tests:** `pytest tests/test_problem_set.py tests/test_chapter_index.py tests/test_problem_set_models.py tests/test_card_models.py tests/test_pipeline_mode.py -xvs`
2. **Type check:** `mypy swanki/pipeline/problem_set.py swanki/pipeline/chapter_index.py swanki/models/problem_set.py swanki/models/cards.py swanki/pipeline/pipeline.py`
3. **Lint:** `ruff check swanki/pipeline/problem_set.py swanki/pipeline/chapter_index.py swanki/models/problem_set.py swanki/models/cards.py swanki/pipeline/pipeline.py scripts/schaum_chapter_pack.py`
4. **Integration smoke test (manual):**
   - `python scripts/schaum_chapter_pack.py --source /scratch/alcamoSchaumsOutlineMicrobiology2010_clean.pdf --chapter-pages 8-18 --answer-key-pages 328-336 --output /scratch/alcamo_CH01_packed.pdf`
   - Add a `.sh` runner: `swanki pdf_path=/scratch/alcamo_CH01_packed.pdf citation_key=alcamoSchaumsOutlineMicrobiology2010 +content_key=alcamoSchaumsOutlineMicrobiology2010_CH01 mode=solution_manual pipeline=solution_manual output=problem_set audio=none anki=default pipeline.processing.confirm_before_generation=false`
   - Inspect: `swanki-out/alcamoSchaumsOutlineMicrobiology2010_CH01/cards-plain.md` should contain ~30 problem cards (15 theory + 15 MC review), each with `#problem-set` tag and book numbering label. `<key>-problem-set.apkg` should exist. `provenance.yaml` should be empty (Phase 1 disables full_solution cards).
5. **Bishop end-to-end (manual, after Phase 1):** repeat with a Bishop chapter PDF + handwritten solutions PDF concatenated. Confirm cross-chapter references inline correctly when prior `chapter-index.yaml` is supplied.

## Execution

To implement, start a new Claude Code session in a worktree:

```
/setup-worktree solution-manual-mode
```

Then in the worktree:

```
/read-codebase
```

Then:

```
Implement the plan at notes/plan.solution-manual-mode-for-problem-set-pdfs.2026.04.25.md.
Read the plan first, then implement each file specification in dependency order. The order below
respects: cards.py types must exist before models/problem_set.py (which imports them), which must
exist before llm/agents.py (which imports response types), which must exist before
pipeline/problem_set.py (which imports the agents):

 1. swanki/models/cards.py (MODIFY) — factor _validate_card_text + _clean_card_tags helpers, add LongFormCardContent, FullSolutionCard, card_subtype field on PlainCard, widen CardGenerationResponse to PlainCard | FullSolutionCard
 2. swanki/models/sections.py (NEW) — ContentSection, ClassificationResult, SectionKind
 3. swanki/models/problem_set.py (NEW) — problem/plan/provenance models AND the three pydantic-ai response wrappers (ProblemEnumerationResponse, CardPlanResponse, ProblemCardBatchResponse)
 4. swanki/pipeline/chapter_index.py (NEW)
 5. swanki/llm/agents.py (MODIFY) — add five agents (section_classifier, problem_enumeration, problem_pairing, card_plan_classifier, problem_card_gen) importing response types from models/
 6. swanki/audio/card.py (MODIFY) — widen card-typed signatures to AnyCard = PlainCard | FullSolutionCard
 7. swanki/audio/lecture.py (MODIFY) — accept optional source_text param for filtered audio
 8. swanki/audio/reading.py (MODIFY) — same source_text param
 9. swanki/pipeline/section_classifier.py (NEW) — heading-first + LLM-fallback classifier with overlap density and Q-A pairing
10. swanki/pipeline/problem_set.py (NEW) — per-section + override entry points, depends on 1-9
11. swanki/models/__init__.py (MODIFY) — re-export new public types
12. swanki/conf/pipeline/solution_manual.yaml (NEW) — shared settings block for classifier + problem-set knobs
13. swanki/conf/refinement/solution_manual.yaml (NEW)
14. swanki/conf/prompts/solution_manual.yaml (NEW) — keys nested under prompts.solution_manual.* (now includes section_classifier and main_with_overlap_instruction)
15. swanki/conf/output/default.yaml (MODIFY — add apkg_filename_suffix)
16. swanki/conf/output/problem_set.yaml (NEW)
17. swanki/conf/config.yaml (MODIFY — comment update only)
18. swanki/pipeline/pipeline.py (MODIFY) — classifier dispatch in mode=full, _generate_main_cards helper extraction with overlap-density modulation, _apkg_filename helper, generate_outputs and generate_audio signature widening (with main_content_text), chapter-index emission, mode=solution_manual override path
19. swanki/__main__.py (MODIFY) — help text update
20. scripts/schaum_chapter_pack.py (NEW)
21. tests/fixtures/problem_set/ (NEW directory) — add schaum_ch01_clean.md, bishop_ch01_clean.md, prior_chapter_index.yaml per the fixture sketches
22. tests/test_problem_set_models.py (NEW) — covers ProblemUnit, CardPlan, ProvenanceLog, ProblemLocation, ProblemPairing, PairingResult
23. tests/test_sections_models.py (NEW) — covers PageLabel, ContentSection, ClassificationResult, sections_from_page_labels
24. tests/test_chapter_index.py (NEW)
25. tests/test_section_classifier.py (NEW) — heading-first cases, overlap-density cases, LLM-fallback mock
26. tests/test_problem_set.py (NEW)
27. tests/test_main_cards_image_remap.py (NEW) — page-idx remapping correctness for char-segmentation under classifier filtering
28. tests/test_models_validation.py (MODIFY — add tests for LongFormCardContent, FullSolutionCard, widened CardGenerationResponse, card_subtype default)
29. tests/test_pipeline_mode.py (MODIFY) — add classifier-dispatch tests + mode=solution_manual override tests + audio source masking tests
30. notes/swanki.pipeline.problem_set.md, notes/swanki.pipeline.chapter_index.md, notes/swanki.pipeline.section_classifier.md, notes/swanki.models.problem_set.md, notes/swanki.models.sections.md, notes/scripts.schaum_chapter_pack.md (NEW dendron notes)

After each logical unit, run verification (pytest + mypy + ruff for that file). Run /update-notes -> /stage -> /commit after each unit. Do not skip the chapter-index emission in mode=full — it is the source of cross-reference resolution for solution_manual mode.

When all files are complete, run the integration smoke test from the Verification section above.
```

