"""
swanki/pipeline/section_classifier.py
[[swanki.pipeline.section_classifier]]
https://github.com/Mjvolk3/Swanki/tree/main/swanki/pipeline/section_classifier.py
Test file: tests/test_section_classifier.py

Section classification for content-aware routing in mode=full. Identify
main_content vs review_exercises (vs front/back matter) sections, compute
overlap density, pair questions with answer-key blocks across distance.

Heading-driven first; LLM fallback (section_classifier_agent) when
confidence is below threshold. Result persisted to
<output_dir>/section-classification.yaml for introspection. To override,
hand-edit the YAML and pass pipeline.solution_manual.classification_override.
"""

import logging
import re
from pathlib import Path
from typing import Any

import yaml

from ..llm.agents import get_model_string, section_classifier_agent
from ..models.sections import (
    ClassificationResult,
    PageLabel,
    SectionKind,
)

logger = logging.getLogger(__name__)


# Heading-driven anchors. Schaum's-style chapters open with `## Theory and
# Problems`; review sections use the canonical Schaum's labels. Bishop and
# similar use `## Exercises` / `## Problems`.
_THEORY_HEADING = re.compile(
    r"^##\s+Theory and Problems\b", re.MULTILINE
)
_REVIEW_HEADINGS = re.compile(
    r"^#{1,3}\s+(Multiple Choice|Matching|True/False|Completion|Review Questions|Problems|Exercises|Practice Problems)\b",
    re.MULTILINE,
)
# Schaum's inline form: "Multiple Choice. Select the letter..." — these are
# section dividers in the chapter body that Mathpix doesn't promote to `##`.
_REVIEW_INLINE = re.compile(
    r"^(Multiple Choice|Matching|True/False|Completion)\.\s+(?:[A-Z]|For each|Pick|Select|Match|Fill|Write)",
    re.MULTILINE,
)
# Anchored to a markdown heading so a prose mention ("a preface to the topic")
# never trips the front-matter flip — only a real section title does.
_FRONT_MATTER = re.compile(
    r"^#{1,6}\s+(Preface|Table of Contents|Copyright|Dedication)\b",
    re.IGNORECASE | re.MULTILINE,
)
_CHAPTER_HEADER = re.compile(
    r"^#\s+(?:CHAPTER|Chapter)\s+\d+", re.MULTILINE
)
# Back-of-book answer block markers — `Chapter N` followed by an answer
# subheading. We re-classify these from back_matter -> review_exercises.
_BACK_OF_BOOK_BLOCK = re.compile(
    r"^Chapter\s+(\d+)\s*\n+\s*(Multiple Choice|Matching|True/False|Completion)",
    re.MULTILINE,
)
# Anchored to a markdown heading: the bare `\b...\b` form matched these words
# mid-prose (e.g. "index registers", "original references"), flipping a content
# page to back_matter and — because the kind is sticky — cascading the drop
# across the rest of the chapter. Real back-matter is always a promoted heading
# ("## References", "# Bibliography"). A positional guard in _heading_classify
# additionally requires the match to fall in the document tail.
_BACK_MATTER = re.compile(
    r"^#{1,6}\s+(Index|Glossary|Bibliography|References)\b",
    re.IGNORECASE | re.MULTILINE,
)

# Per-page problem-shape density: count `^N.M ` starters and `^(a)/(b)/...` MC
# items. Heuristic — tuned so a page with ~5 numbered problems hits ~0.5.
_PROBLEM_STARTER = re.compile(r"^\d+\.\d+\s+\S", re.MULTILINE)
_MC_ITEM_LINE = re.compile(r"^\d+\.\s+\S", re.MULTILINE)


def classify_sections(
    clean_md_files: list[Path],
    config: dict[str, Any],
    output_dir: Path | None = None,
) -> ClassificationResult:
    """Classify pages into PageLabels with heading-first + LLM fallback.

    If ``pipeline.solution_manual.classification_override`` is set in config,
    load and return that YAML directly (skips classification entirely). The
    introspection / manual-correction path: edit the persisted YAML, point
    this knob at it, re-run.

    Args:
        clean_md_files: Per-page cleaned markdown.
        config: Hydra config dict.
        output_dir: When provided, persist the result to
            ``<output_dir>/section-classification.yaml``.

    Returns:
        Populated ClassificationResult.
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
    """Pure heading-driven classification. One PageLabel per page."""
    page_labels: list[PageLabel] = []
    texts = [f.read_text() for f in clean_md_files]
    total = len(texts)
    current_kind: SectionKind = "main_content"
    current_anchor: str | None = None

    for i, text in enumerate(texts):
        # Check for transitions on this page. Order matters: review_exercises
        # wins over generic main_content; matter only matches on dedicated
        # boundary words and is downgraded if other content is also present.
        anchor_changed = False

        # Check for chapter header — resets to main_content from front_matter.
        if _CHAPTER_HEADER.search(text):
            current_kind = "main_content"
            current_anchor = "# CHAPTER ..."
            anchor_changed = True

        # Theory and Problems block — explicit main_content with overlap_density signal.
        if _THEORY_HEADING.search(text):
            current_kind = "main_content"
            current_anchor = "## Theory and Problems"
            anchor_changed = True

        # Review headings — start a review_exercises section. Match either the
        # markdown-promoted form (`## Multiple Choice`) or Schaum's inline form
        # ("Multiple Choice. Select the letter..."). Inline form is common in
        # mid-chapter section dividers that Mathpix doesn't promote to headers.
        review_match = _REVIEW_HEADINGS.search(text) or _REVIEW_INLINE.search(text)
        if review_match:
            current_kind = "review_exercises"
            current_anchor = f"## {review_match.group(1)}"
            anchor_changed = True

        # Back-matter heuristic: flip to back_matter only when the page has a
        # back-matter heading, no other content cues, AND sits in the document
        # tail (last ~20% of pages). The tail guard stops a stray real heading
        # mid-document from starting a back_matter run; the pairing pass below
        # still flips genuine answer-key pages back to review_exercises, and a
        # true tail heading still cascades through a multi-page back-matter run.
        if (
            _BACK_MATTER.search(text)
            and not review_match
            and not _CHAPTER_HEADER.search(text)
            and i >= int(total * 0.8)
        ):
            current_kind = "back_matter"
            current_anchor = "back_matter (heuristic)"
            anchor_changed = True

        # Front-matter heuristic — first few pages with Preface/TOC text and
        # no chapter header.
        if (
            i < 5
            and _FRONT_MATTER.search(text)
            and not _CHAPTER_HEADER.search(text)
            and not _THEORY_HEADING.search(text)
        ):
            current_kind = "front_matter"
            current_anchor = "front_matter (heuristic)"
            anchor_changed = True

        density = (
            _compute_overlap_density(text)
            if current_kind == "main_content"
            else (1.0 if current_kind == "review_exercises" else 0.0)
        )
        # Heading-anchored pages get high confidence; inherited classification
        # (no anchor on this page) gets moderate confidence.
        confidence = 1.0 if anchor_changed else 0.7

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
    """Estimate problem-shape density of a main_content page.

    Density = ``min(1.0, n_problem_starters * 50 / total_chars)``.
    Tuned so 20 problems in 5000 chars ≈ 0.5.
    """
    n_problem_starters = len(_PROBLEM_STARTER.findall(section_text))
    n_chars = max(1, len(section_text))
    return min(1.0, (n_problem_starters * 50) / n_chars)


def _pair_answer_keys(
    page_labels: list[PageLabel], texts: list[str]
) -> list[PageLabel]:
    r"""Re-classify back-matter pages that contain an answer-key block.

    Walks each back_matter page; if it carries a ``^Chapter N\nMultiple Choice``
    pattern, find the earliest review_exercises page in chapter N and link
    them via paired_answer_page. Then flip the back-matter page's kind to
    review_exercises so the problem-set pipeline picks it up.
    """
    # Locate the first review-exercises page per chapter for pairing lookup.
    review_pages_by_chapter: dict[str, int] = {}
    for label in page_labels:
        if label.kind != "review_exercises":
            continue
        # Try to read chapter number from the heading_anchor or first text line.
        text = texts[label.page_idx]
        chap_match = re.search(r"CHAPTER\s+(\d+)", text)
        if chap_match:
            chapter = chap_match.group(1)
            review_pages_by_chapter.setdefault(chapter, label.page_idx)

    for label in page_labels:
        if label.kind != "back_matter":
            continue
        text = texts[label.page_idx]
        block = _BACK_OF_BOOK_BLOCK.search(text)
        if not block:
            continue
        chapter = block.group(1)
        question_page = review_pages_by_chapter.get(chapter)
        if question_page is not None:
            label.paired_answer_page = question_page
        # Flip to review_exercises so the problem-set pipeline picks it up.
        label.kind = "review_exercises"
        label.overlap_density = 1.0
        label.note = "re-classified from back_matter to review_exercises after pairing"

    return page_labels


def _llm_classify(
    clean_md_files: list[Path], config: dict[str, Any]
) -> ClassificationResult:
    """Fallback: ask section_classifier_agent to produce ClassificationResult.

    Sends the first ~1500 chars of each page (a sample) along with the schema
    description from the prompt config. Used when the heading-driven pass has
    low confidence.
    """
    prompts_root = config.get("prompts", {}).get("prompts", {})
    sm_prompts = prompts_root.get("solution_manual", {})
    system_prompt = sm_prompts.get("section_classifier", "")
    sample = "\n\n--- PAGE ---\n\n".join(
        f.read_text()[:1500] for f in clean_md_files
    )
    models_config = config.get("models", {}).get("models", {}).get("llm", {})
    result = section_classifier_agent.run_sync(
        sample,
        instructions=system_prompt,
        model=get_model_string(models_config),
    )
    return result.output


# A page whose text ends with sentence-terminal punctuation (or a closing
# bracket/quote following it) finished its sentence; the next page starts a
# new one. Any other ending — a word, comma, em-dash, digit — is a sentence
# continuing across the page break.
_SENTENCE_TERMINAL_RE = re.compile(r"""[.!?:;)\]}"”’'](?:["”’')\]}]*)\s*$""")


def join_pages(texts: list[str]) -> str:
    """Concatenate page texts, gluing mid-sentence page breaks.

    Pages are normally joined with a blank line so ``add_tts_pauses`` renders a
    natural inter-page ``[pause]``. But ``clean-md-singles`` pages routinely end
    mid-sentence (e.g. page 4 ends "...fields of knowledge when", page 5 opens
    "they arise..."). A blank-line join there injects an audible ``[pause]``
    in the middle of a sentence. When the preceding page does not end a
    sentence, join with a single space instead so the sentence is spoken
    continuously; the blank-line join (and its pause) is kept only between
    pages that actually end a sentence.
    """
    out = ""
    for text in texts:
        text = text.strip()
        if not text:
            continue
        if not out:
            out = text
        elif _SENTENCE_TERMINAL_RE.search(out):
            out += "\n\n" + text
        else:
            out += " " + text
    return out


def merge_main_content(
    clean_md_files: list[Path], page_labels: list[PageLabel]
) -> str:
    """Concatenate only pages labeled main_content.

    Used by both segmentation (so the segmenter never sees problem-set content)
    and audio source masking (so lecture/reading aren't built from review
    exercises).
    """
    return join_pages(
        [
            clean_md_files[p.page_idx].read_text()
            for p in page_labels
            if p.kind == "main_content"
        ]
    )


def filter_files_by_kind(
    clean_md_files: list[Path],
    page_labels: list[PageLabel],
    kind: SectionKind,
) -> list[Path]:
    """Return cleaned-md files whose pages carry the given kind."""
    return [
        clean_md_files[p.page_idx] for p in page_labels if p.kind == kind
    ]


def original_page_indices(
    page_labels: list[PageLabel], kind: SectionKind
) -> list[int]:
    """Return original page indices (in document order) for pages of the given kind.

    Used to translate filtered-page indices back to original ones for image
    summary lookup in the main-content card-gen path.
    """
    return [p.page_idx for p in page_labels if p.kind == kind]
