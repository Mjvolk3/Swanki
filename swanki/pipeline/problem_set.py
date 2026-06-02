"""
swanki/pipeline/problem_set.py
[[swanki.pipeline.problem_set]]
https://github.com/Mjvolk3/Swanki/tree/main/swanki/pipeline/problem_set.py
Test file: tests/test_problem_set.py

Solution-manual mode: enumerate problems, pair statements with solutions,
resolve cross-chapter references, generate cards per problem, audit coverage.
Used by mode=solution_manual (whole-document override) and by classifier-driven
mode=full routing (per-section).
"""

import logging
import re
from collections import Counter
from pathlib import Path
from typing import Any, Literal

import yaml

from ..llm.agents import (
    get_model_string,
    problem_card_gen_agent,
    problem_enumeration_agent,
    problem_pairing_agent,
)
from ..models.cards import PlainCard
from ..models.document import DocumentSummary
from ..models.problem_set import (
    CardPlan,
    PairingResult,
    ProblemCardBatchResponse,
    ProblemEnumerationResponse,
    ProblemLocation,
    ProblemPairing,
    ProblemPairingResponse,
    ProblemProvenance,
    ProblemTag,
    ProblemUnit,
    ProvenanceLog,
)
from .chapter_index import (
    ChapterIndex,
    build_chapter_index,
    load_chapter_index,
)

logger = logging.getLogger(__name__)


class CoverageError(RuntimeError):
    """Raised when problem-set coverage is incomplete.

    Carries diagnostic sets so callers can surface specific problem IDs.
    """

    def __init__(
        self,
        missing: set[str] | None = None,
        extra: set[str] | None = None,
        unsolved: set[str] | None = None,
        duplicated: set[str] | None = None,
    ) -> None:
        self.missing = missing or set()
        self.extra = extra or set()
        self.unsolved = unsolved or set()
        self.duplicated = duplicated or set()
        parts: list[str] = []
        if self.missing:
            parts.append(
                f"{len(self.missing)} problems missing from cards: {sorted(self.missing)}"
            )
        if self.extra:
            parts.append(
                f"{len(self.extra)} unexpected card IDs: {sorted(self.extra)}"
            )
        if self.unsolved:
            parts.append(
                f"{len(self.unsolved)} problems with no solution: {sorted(self.unsolved)}"
            )
        if self.duplicated:
            parts.append(
                f"{len(self.duplicated)} problems with duplicate main cards: "
                f"{sorted(self.duplicated)}"
            )
        super().__init__("Coverage audit failed: " + "; ".join(parts))


# Theory-problem anchor (`N.M`). The lookahead terminates on the next N.M, on
# any review-section divider (so the last theory problem doesn't slurp the MC
# section into its solution body), or on the back-of-book chapter header.
_THEORY_PROBLEM = re.compile(
    r"^([0-9]+)\.([0-9]+)\b\s+(.+?)"
    r"(?=^[0-9]+\.[0-9]+\b|^##\s+REVIEW QUESTIONS|"
    r"^Multiple Choice\.|^Matching\.|^True/False\.|^Completion\.|"
    r"^##\s*Chapter\s+\d|\Z)",
    re.MULTILINE | re.DOTALL,
)
# Stage-2 markers
_SOLUTION_MARKER = re.compile(
    r"^Solution\s+([0-9]+)\.([0-9]+)\b\s*[:.]?\s*(.+?)(?=^Solution\s+[0-9]+\.[0-9]+|\Z)",
    re.MULTILINE | re.DOTALL,
)
_MC_ANSWER_PAIR = re.compile(r"([0-9]+)\.\s*([a-z])\b")
# T/F answer is `T`, `F`, or a multi-word replacement phrase.
_TF_ANSWER_SPLIT = re.compile(
    r"(\d+)\.\s+(T|F|.+?)(?=\s+\d+\.\s|\s*\Z)",
    re.DOTALL,
)
# Completion answer is one or more words. Optional whitespace around the period
# absorbs OCR drift like `4 . hydrogen bonds`.
_CMP_ANSWER_SPLIT = re.compile(
    r"(\d+)\s*\.\s+(.+?)(?=\s+\d+\s*\.|\s*\Z)",
    re.DOTALL,
)

# Visible fill-in-the-blank rendered on Completion card fronts. Mathpix's blank
# token (`$\_\_\_\_$`) is normalized to this run of underscores; bump the length
# here to make the blank larger on every Completion card.
_COMPLETION_BLANK = "________"

# In-chapter review-section dividers. Schaum's writes them inline as
# "Multiple Choice. Select ...", "Matching. Match ...", "True/False. For each
# ...", "Completion. Fill in the blanks ...". Drop the verb requirement —
# Bishop and other authors vary, but the trailing `.` is canonical.
_MC_SECTION = re.compile(r"^Multiple Choice\.\s+\S", re.MULTILINE)
_MATCHING_SECTION = re.compile(r"^Matching\.\s+\S", re.MULTILINE)
_TF_SECTION = re.compile(r"^True/False\.\s+\S", re.MULTILINE)
_COMPLETION_SECTION = re.compile(r"^Completion\.\s+\S", re.MULTILINE)
# Combined boundary for terminating a section span (any other divider OR back
# of book).
# The back-of-book anchors (`Answers`, `Chapter N`) carry the same Mathpix-`##`
# vs MinerU-`#` header-level split as the `_BACK_*` partition patterns, so they
# accept `#{1,3}`. The bare-text in-chapter dividers (`Multiple Choice.` etc.)
# are OCR-agnostic and untouched.
_SECTION_OR_BACK_OF_BOOK = re.compile(
    r"^(?:Multiple Choice\.\s+\S|Matching\.\s+\S|True/False\.\s+\S|"
    r"Completion\.\s+\S|#{1,3}\s+Answers|#{1,3}\s+Chapter\s+\d)",
    re.MULTILINE,
)

# Per-subtype enumeration patterns.
# MC: number + stem on one line, then 2-5 lettered choice lines. MULTILINE only
# (NOT DOTALL — DOTALL was tested and reduced matches from 15 to 1 because the
# choice quantifier eats newlines greedily).
_MC_ITEM = re.compile(
    r"^(\d+)\.\s+(.+?)\n((?:\([a-z]\)\s+.+?\n){2,5})",
    re.MULTILINE,
)
# Matching / True-False items: optional `$\_\_\_\_$` blank-token prefix
# (Mathpix's rendering of an answer-blank), then `\d+. statement` running until
# the next item, an `^##` block header, or end-of-section. Note the blank
# token is alternating backslash-underscore pairs, hence `(?:\\_)+` not `\\_+`.
_MATCHING_ITEM = re.compile(
    r"^(?:\$(?:\\_)+\$\s+)?(\d+)\.\s+(.+?)"
    r"(?=^(?:\$(?:\\_)+\$\s+)?\d+\.\s|^##|\Z)",
    re.MULTILINE | re.DOTALL,
)
_TF_ITEM = _MATCHING_ITEM  # same shape — number + statement + blank-token prefix
# Completion items must contain a blank token to be enumerated; numbered prose
# without a blank is correctly skipped.
_COMPLETION_ITEM = re.compile(
    r"^(\d+)\.\s+(.+?\$(?:\\_)+\$.+?)(?=^\d+\.\s|^##|\Z)",
    re.MULTILINE | re.DOTALL,
)
# Column B option lines: `(letter) text`.
_COLUMN_B_OPTION = re.compile(r"^\(([a-z])\)\s+(.+)$", re.MULTILINE)

# Back-of-book partition. The header anchor is `#{1,3}` because Mathpix emits
# the back-of-book titles as H2 (`## Chapter 1`) while MinerU emits them as H1
# (`# Chapter 1`); H3 is cheap defensive headroom. A real header anchor is
# required — the section words also appear as in-chapter dividers
# (`Multiple Choice.` with a period) and inside answer-body prose — so bare-text
# matching is deliberately rejected.
_BACK_CHAPTER_HEADER = re.compile(r"^#{1,3}\s+Chapter\s+(\d+)\s*$", re.MULTILINE)
_BACK_SECTION_HEADER = re.compile(
    r"^#{1,3}\s+(Multiple Choice|Matching|True/False|Completion)\s*$",
    re.MULTILINE,
)

# Forward chapter detection (in-chapter heading, e.g. `# CHAPTER 1` or
# `## Chapter 1`).
_FORWARD_CHAPTER_HEADER = re.compile(
    r"^#{1,2}\s*(?:CHAPTER|Chapter)\s+(\d+)\b", re.MULTILINE
)

# Reference-resolution patterns
_REF_EQUATION = re.compile(r"equation\s*\(([0-9]+\.[0-9]+)\)", re.IGNORECASE)
_REF_FIGURE = re.compile(r"Figure\s+([0-9]+\.[0-9]+)", re.IGNORECASE)
_REF_THEOREM = re.compile(r"Theorem\s+([0-9]+\.[0-9]+)", re.IGNORECASE)

# Per-subtype system-prompt key dispatch.
_PROMPT_KEY_BY_SUBTYPE: dict[str, str] = {
    "theory_problem": "problem_card_gen",
    "multiple_choice": "problem_card_gen_multiple_choice",
    "matching": "problem_card_gen_matching",
    "true_false": "problem_card_gen_true_false",
    "completion": "problem_card_gen_completion",
}


def _detect_chapter(full_text: str, chapter_id: str | None) -> str:
    """Resolve the in-chapter chapter number for subtype-prefixed problem IDs.

    Tries the explicit ``chapter_id`` arg first (e.g. ``"alcamo2010_CH01"`` →
    ``"1"``; the leading zero is stripped). Falls back to scanning the cleaned
    markdown for a forward chapter heading (``# CHAPTER N`` /
    ``## Chapter N``). Returns ``"unknown"`` if neither succeeds.
    """
    if chapter_id:
        m = re.search(r"_CH0?(\d+)", chapter_id)
        if m is not None:
            return m.group(1)
    m = _FORWARD_CHAPTER_HEADER.search(full_text)
    if m is not None:
        return m.group(1)
    return "unknown"


def _section_spans(
    full_text: str, start_pattern: re.Pattern[str]
) -> list[tuple[int, int]]:
    """Locate EVERY in-chapter occurrence of a review-section's char span.

    A chapter can carry the same section type more than once (e.g. two Matching
    sets each numbered 1-10). Returns one ``(start, end)`` per occurrence of
    ``start_pattern``; each span ends at the next review-section divider OR the
    back-of-book block, whichever comes first. Returns ``[]`` when absent.
    """
    spans: list[tuple[int, int]] = []
    for m in start_pattern.finditer(full_text):
        nxt = _SECTION_OR_BACK_OF_BOOK.search(full_text, m.end())
        end = nxt.start() if nxt is not None else len(full_text)
        spans.append((m.start(), end))
    return spans


def _problem_id(prefix: str, chapter: str, occ: int, n_occ: int, item: str) -> str:
    """Build an occurrence-aware problem ID.

    When a section type appears exactly once in a chapter (``n_occ == 1``) the
    occurrence segment is suppressed so the ID stays ``MAT-CH3-7`` — zero
    regression for every chapter that already worked. When it appears more than
    once, the 1-based occurrence index is inserted: ``MAT-CH3-2-7``.
    """
    if n_occ <= 1:
        return f"{prefix}-CH{chapter}-{item}"
    return f"{prefix}-CH{chapter}-{occ}-{item}"


def _candidate_ids(
    prefix: str, chapter: str, occ: int, n_occ: int, item: str
) -> list[str]:
    """Back-of-book candidate IDs for the k-th section's k-th body.

    Tries, in order:
      1. the occurrence-aware ID (``MAT-CH3-2-7``) — the forward shape when the
         section repeats in the chapter;
      2. the bare chapter ID (``MAT-CH3-7``) — the forward shape when the
         section appears once;
      3. the legacy no-chapter fallback (``MAT-7``).

    Both the occurrence and bare chapter forms are emitted regardless of
    ``n_occ`` because the forward enumeration's occurrence count can diverge
    from the back-of-book's: the answer key may print one Matching set while the
    chapter poses two (real Alcamo CH03). The k-th body must still pair with the
    k-th forward set. The form natural to *this* body's occurrence count is
    tried first so it also becomes the label of an unpaired entry.
    """
    natural = _problem_id(prefix, chapter, occ, n_occ, item)
    occurrence = f"{prefix}-CH{chapter}-{occ}-{item}"
    bare_chapter = f"{prefix}-CH{chapter}-{item}"
    ordered = [natural, occurrence, bare_chapter, f"{prefix}-{item}"]
    seen: set[str] = set()
    return [c for c in ordered if not (c in seen or seen.add(c))]


def _set_label(occ: int, n_occ: int) -> str:
    """Visible-label disambiguator for a repeated same-type section.

    Returns ``" (set 2)"`` for the 2nd occurrence of a section type, ``""`` when
    the type appears once (the common case). The printed item number is kept
    separately, so the rendered front reads e.g. ``Matching (set 2) 7:``.
    """
    return "" if n_occ <= 1 else f" (set {occ})"


def _enumerate_multiple_choice(full_text: str, chapter: str) -> list[ProblemUnit]:
    """Enumerate Multiple Choice items across ALL of the chapter's MC sections."""
    spans = _section_spans(full_text, _MC_SECTION)
    n_occ = len(spans)
    out: list[ProblemUnit] = []
    for occ, (start, end) in enumerate(spans, start=1):
        section_text = full_text[start:end]
        set_label = _set_label(occ, n_occ)
        for m in _MC_ITEM.finditer(section_text):
            item_num = m.group(1)
            stem = m.group(2).strip()
            choices_block = m.group(3).rstrip()
            statement = (
                f"{item_num}.{set_label} {stem}\n{choices_block}".strip()
                if set_label
                else f"{item_num}. {stem}\n{choices_block}".strip()
            )
            out.append(
                ProblemUnit(
                    problem_id=_problem_id(
                        "MC", chapter, occ, n_occ, item_num
                    ),
                    subtype="multiple_choice",
                    chapter=chapter,
                    statement=statement,
                    solution=None,
                    char_count=len(statement),
                )
            )
    return out


def _enumerate_matching(full_text: str, chapter: str) -> list[ProblemUnit]:
    """Enumerate Matching Column-A items, embedding the full Column B options
    list in each statement so cards are self-contained.
    """
    spans = _section_spans(full_text, _MATCHING_SECTION)
    n_occ = len(spans)
    column_b = _extract_column_b(full_text, chapter)
    options_text = "\n".join(f"({letter}) {text}" for letter, text in column_b.items())

    out: list[ProblemUnit] = []
    for occ, (start, end) in enumerate(spans, start=1):
        section_text = full_text[start:end]
        set_label = _set_label(occ, n_occ)
        for m in _MATCHING_ITEM.finditer(section_text):
            item_num = m.group(1)
            stmt_body = m.group(2).strip()
            # Filter: skip the column-B option lines (they match
            # `\(letter\) text`, not `\d+. text`) and any item whose body
            # starts with a `Column` header (defensive guard against the
            # section header bleeding into a previous item's body).
            if re.match(r"^#{1,3}\s+Column", stmt_body):
                continue
            label = f"{item_num}.{set_label}"
            statement = (
                f"{label} {stmt_body}\n\nOptions:\n{options_text}"
                if options_text
                else f"{label} {stmt_body}"
            )
            out.append(
                ProblemUnit(
                    problem_id=_problem_id(
                        "MAT", chapter, occ, n_occ, item_num
                    ),
                    subtype="matching",
                    chapter=chapter,
                    statement=statement,
                    solution=None,
                    char_count=len(statement),
                )
            )
    return out


def _enumerate_true_false(full_text: str, chapter: str) -> list[ProblemUnit]:
    """Enumerate True/False statements. The originally-underlined word is NOT
    preserved in Mathpix OCR; the card front carries the prose verbatim and the
    back will be ``T`` or the corrected word. The card-gen prompt infers which
    word changed by comparing the back-of-book correction to the statement —
    no front-of-card "originally underlined" framing because Mathpix drops the
    underline markup.
    """
    spans = _section_spans(full_text, _TF_SECTION)
    n_occ = len(spans)
    out: list[ProblemUnit] = []
    for occ, (start, end) in enumerate(spans, start=1):
        section_text = full_text[start:end]
        set_label = _set_label(occ, n_occ)
        for m in _TF_ITEM.finditer(section_text):
            item_num = m.group(1)
            stmt_body = m.group(2).strip()
            statement = f"{item_num}.{set_label} True or false: {stmt_body}"
            out.append(
                ProblemUnit(
                    problem_id=_problem_id(
                        "TF", chapter, occ, n_occ, item_num
                    ),
                    subtype="true_false",
                    chapter=chapter,
                    statement=statement,
                    solution=None,
                    char_count=len(statement),
                )
            )
    return out


def _enumerate_completion(full_text: str, chapter: str) -> list[ProblemUnit]:
    r"""Enumerate Completion fill-in-blank items. Items must contain a
    ``$\_\_\_\_$`` blank token (Mathpix rendering) to be enumerated.
    """
    spans = _section_spans(full_text, _COMPLETION_SECTION)
    n_occ = len(spans)
    out: list[ProblemUnit] = []
    for occ, (start, end) in enumerate(spans, start=1):
        section_text = full_text[start:end]
        set_label = _set_label(occ, n_occ)
        for m in _COMPLETION_ITEM.finditer(section_text):
            item_num = m.group(1)
            body = m.group(2).strip()
            readable = body.replace("$\\_\\_\\_\\_$", _COMPLETION_BLANK)
            statement = f"{item_num}.{set_label} Fill in the blank: {readable}"
            out.append(
                ProblemUnit(
                    problem_id=_problem_id(
                        "CMP", chapter, occ, n_occ, item_num
                    ),
                    subtype="completion",
                    chapter=chapter,
                    statement=statement,
                    solution=None,
                    char_count=len(statement),
                )
            )
    return out


def _extract_column_b(full_text: str, chapter: str) -> dict[str, str]:
    """Find the in-chapter ``## Column B`` block for the given chapter and
    parse its ``(letter) option`` lines into a letter→text dict. Returns ``{}``
    if Column B is absent (chapter has no Matching section).

    Constrains the search to text BEFORE the back-of-book block (delimited by
    ``## Answers to Review Questions``) so the chapter-heading lookup doesn't
    accidentally land on the back-of-book ``## Chapter N`` header.
    """
    answers_re = re.compile(r"^##\s+Answers", re.MULTILINE)
    am = answers_re.search(full_text)
    forward_end = am.start() if am is not None else len(full_text)

    chapter_start = 0
    chapter_end = forward_end
    chapter_re = re.compile(
        rf"^#{{1,2}}\s*(?:CHAPTER|Chapter)\s+{chapter}\b", re.MULTILINE
    )
    cm = chapter_re.search(full_text, 0, forward_end)
    if cm is not None:
        chapter_start = cm.end()
        next_chapter_re = re.compile(
            r"^#{1,2}\s*(?:CHAPTER|Chapter)\s+\d", re.MULTILINE
        )
        nxt = next_chapter_re.search(full_text, chapter_start + 1, forward_end)
        if nxt is not None:
            chapter_end = nxt.start()

    column_b_re = re.compile(r"^#{1,3}\s+Column B\s*$", re.MULTILINE)
    cb = column_b_re.search(full_text, chapter_start, chapter_end)
    if cb is None:
        return {}
    options: dict[str, str] = {}
    for opt in _COLUMN_B_OPTION.finditer(full_text, cb.end(), chapter_end):
        letter = opt.group(1)
        text = opt.group(2).strip()
        options[letter] = text
    return options


# A standalone line inside an answer body that is purely a page number or a
# residual header. MinerU can spill a section's answer run across a page break,
# injecting a bare page-number line or a running-header line mid-run (O1). Such
# lines are stripped before the per-subtype answer tokenizers run so the body
# reads as one contiguous answer sequence.
_BODY_NOISE_LINE = re.compile(
    r"^(?:\d+|#{1,6}\s+.*|Answers to Review Questions)\s*$",
    re.MULTILINE,
)


def _strip_body_noise(body: str) -> str:
    """Remove standalone page-number / header-only lines from a section body.

    A section's answer run can be split mid-sequence by an injected page-number
    token or a running-header line (the O1 page-spill artifact). The answer
    tokenizers assume a contiguous run, so drop those standalone noise lines and
    rejoin the surviving answer fragments with single spaces.
    """
    kept = [
        line.strip()
        for line in body.splitlines()
        if line.strip() and not _BODY_NOISE_LINE.fullmatch(line.strip())
    ]
    return " ".join(kept)


def _merge_consecutive_chapters(
    matches: list[re.Match[str]],
) -> list[tuple[str, int, int]]:
    """Collapse consecutive same-number chapter headers into one span (O2).

    MinerU may stamp ``# Chapter N`` as a running header atop every page in a
    chapter's answer region, so ``_BACK_CHAPTER_HEADER`` matches the same number
    repeatedly. Merge a run of identical-numbered headers into a single span
    spanning from the first header's body start to the next *different* chapter.

    Returns:
        ``(chapter_num, body_start, header_start)`` tuples — ``body_start`` is
        where the first header's body begins; ``header_start`` is the char index
        of the first header (used to compute the previous span's end).
    """
    merged: list[tuple[str, int, int]] = []
    for m in matches:
        chapter_num = m.group(1)
        if merged and merged[-1][0] == chapter_num:
            continue
        merged.append((chapter_num, m.end(), m.start()))
    return merged


def _partition_back_of_book(full_text: str) -> dict[str, dict[str, list[str]]]:
    """Walk the back-of-book block, returning ``{chapter: {section: [body]}}``.

    Pass 1: locate every ``#{1,3} Chapter N`` boundary, merging consecutive
    same-number matches into one span (MinerU running-header dup, O2).
    Pass 2: within each chapter span, scan ``#{1,3} (Multiple Choice|...)``
    boundaries; each section type maps to a LIST of bodies, one per occurrence,
    so a chapter with two Matching sets keeps both (the k-th forward section
    pairs with the k-th body). Each body has page-spill noise stripped (O1).
    """
    chapter_matches = list(_BACK_CHAPTER_HEADER.finditer(full_text))
    if not chapter_matches:
        return {}
    merged = _merge_consecutive_chapters(chapter_matches)
    out: dict[str, dict[str, list[str]]] = {}
    for i, (chapter_num, chapter_start, _header_start) in enumerate(merged):
        chapter_end = (
            merged[i + 1][2] if i + 1 < len(merged) else len(full_text)
        )
        sections: dict[str, list[str]] = {}
        section_matches = list(
            _BACK_SECTION_HEADER.finditer(full_text, chapter_start, chapter_end)
        )
        for j, sm in enumerate(section_matches):
            section_name = sm.group(1)
            body_start = sm.end()
            body_end = (
                section_matches[j + 1].start()
                if j + 1 < len(section_matches)
                else chapter_end
            )
            body = _strip_body_noise(full_text[body_start:body_end])
            sections.setdefault(section_name, []).append(body)
        if sections:
            out[chapter_num] = sections
    return out


def _try_pair_or_unpaired(
    pairings_by_id: dict[str, ProblemPairing],
    unpaired_solutions: list[ProblemLocation],
    candidate_ids: list[str],
    text: str,
    role: Literal["statement", "solution"],
    page_idx: int,
) -> bool:
    """Try each candidate ID; append to the first matching pairing OR to
    ``unpaired_solutions`` when none match. Returns True if paired.

    Critical: never drops a parsed answer on the floor. Without this, a
    back-of-book answer for a missing-from-OCR item would silently vanish; the
    audit relies on ``unpaired_solutions`` to surface that gap.
    """
    for cid in candidate_ids:
        pair = pairings_by_id.get(cid)
        if pair is not None:
            pair.solutions.append(
                ProblemLocation(
                    problem_id=cid,
                    role=role,
                    page_idx=page_idx,
                    start_char=0,
                    end_char=len(text),
                    text=text,
                )
            )
            return True
    unpaired_solutions.append(
        ProblemLocation(
            problem_id=candidate_ids[0],
            role=role,
            page_idx=page_idx,
            start_char=0,
            end_char=len(text),
            text=text,
        )
    )
    return False


_EXERCISES_HEADING = re.compile(
    r"^#{1,3}\s+Exercises\b", re.MULTILINE | re.IGNORECASE
)
# Bishop-style worked solutions in a separate manual start with a bare
# ``N.M`` followed by an English word — NO difficulty marker like ``(?)``,
# ``($\star$)``, ``(* *)`` (those mark problem statements). MinerU strips
# the ``Solutions N.M-N.K / Chapter N <Title>`` running header, so we
# detect the boundary by this body-shape signal rather than a heading.
_SOLUTION_BODY_START = re.compile(
    r"^\d+\.\d+\s+(?![\(\$])[A-Za-z]",
    re.MULTILINE,
)


def _partition_statement_solution_regions(
    full_text: str,
) -> tuple[str, str | None]:
    """Split a packed-document into (statements_region, solutions_region).

    Bishop-style packed PDFs concatenate the book chapter (ending with a
    ``# Exercises`` section whose problems carry difficulty markers like
    ``(?)``, ``($\\star$)``, ``(* *)``) and a slice of the separate solution
    manual whose worked solutions are numbered as bare ``N.M`` followed by
    plain English text. The boundary is the first such bare ``N.M ...``
    line that appears AFTER the ``Exercises`` heading.

    When the chapter has no ``Exercises`` heading, or no solution-body line
    is found after it (Schaum's: inline Q&A, no separate solution span),
    return ``(full_text, None)`` so callers fall back to the legacy
    single-region path.
    """
    ex = _EXERCISES_HEADING.search(full_text)
    if ex is None:
        return full_text, None
    sol = _SOLUTION_BODY_START.search(full_text, ex.end())
    if sol is None:
        return full_text, None
    return full_text[: sol.start()], full_text[sol.start():]


def enumerate_problems(
    clean_md_files: list[Path], chapter_id: str | None = None
) -> list[ProblemUnit]:
    """Regex-first problem enumeration. Returns list of ProblemUnits.

    Theory-problems (``N.M`` numbering) are enumerated first. Then four
    review-subtype enumerators (Multiple Choice, Matching, True/False,
    Completion) run, each anchored on its inline section divider. Returns
    empty list if no items match.

    For Bishop-style packed PDFs (chapter Exercises + separate-manual
    solutions concatenated), only the statements region is scanned for
    theory-problems — bare ``N.M`` worked-solution bodies on the right of
    ``_partition_statement_solution_regions`` would otherwise be enumerated
    as duplicate "statements".

    Args:
        clean_md_files: Per-page cleaned markdown files.
        chapter_id: Optional chapter identifier (e.g. ``"alcamo2010_CH01"``).

    Returns:
        List of enumerated ProblemUnits, in document order (theory then
        review-subtypes).
    """
    problems: list[ProblemUnit] = []
    full_text = "\n\n".join(f.read_text() for f in clean_md_files)
    statements_text, _solutions_region = _partition_statement_solution_regions(
        full_text
    )

    for m in _THEORY_PROBLEM.finditer(statements_text):
        chap, num, body = m.group(1), m.group(2), m.group(3).strip()
        # First paragraph = statement; rest = solution.
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

    chapter_num = _detect_chapter(full_text, chapter_id)
    problems.extend(_enumerate_multiple_choice(full_text, chapter_num))
    problems.extend(_enumerate_matching(full_text, chapter_num))
    problems.extend(_enumerate_true_false(full_text, chapter_num))
    problems.extend(_enumerate_completion(full_text, chapter_num))

    return problems


def pair_problems_across_pages(
    problems: list[ProblemUnit],
    clean_md_files: list[Path],
    config: dict[str, Any],
) -> PairingResult:
    """Build PairingResult by Stage 0 (init) → 1 (adjacent) → 2 (regex).

    Stage 3 (LLM fallback) is wired but disabled when every problem already has
    a solution after Stages 1-2. v1 in this implementation skips Stage 3
    entirely; LLM-based pairing is reserved for future iteration once we have
    real Bishop fixtures with no explicit `Solution N.M` markers.

    Args:
        problems: Enumerated problems.
        clean_md_files: All cleaned per-page markdown files.
        config: Hydra config dict (used for prompts and model selection).

    Returns:
        PairingResult with one ProblemPairing per enumerated problem (Stage 0
        guarantee).
    """
    # Stage 0: one ProblemPairing per problem with empty solutions.
    pairings = [
        ProblemPairing(
            problem_id=p.problem_id,
            statement=ProblemLocation(
                problem_id=p.problem_id,
                role="statement",
                page_idx=p.page_span[0] if p.page_span else 0,
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
    used_regex = False

    full_text = "\n\n".join(f.read_text() for f in clean_md_files)

    # Stage 1: adjacent pairing — if the ProblemUnit already has an inline
    # solution, lift it into the pairing.
    for problem in problems:
        if problem.solution:
            pair = pairings_by_id[problem.problem_id]
            pair.solutions.append(
                ProblemLocation(
                    problem_id=problem.problem_id,
                    role="solution",
                    page_idx=problem.page_span[0] if problem.page_span else 0,
                    start_char=0,
                    end_char=len(problem.solution),
                    text=problem.solution,
                )
            )

    # Stage 2: regex pairing on explicit `Solution N.M` markers.
    for m in _SOLUTION_MARKER.finditer(full_text):
        pid = f"{m.group(1)}.{m.group(2)}"
        body = m.group(3).strip()
        pair = pairings_by_id.get(pid)
        loc = ProblemLocation(
            problem_id=pid,
            role="solution",
            page_idx=0,  # full-text scan loses page info; refine when needed
            start_char=m.start(),
            end_char=m.end(),
            text=body,
        )
        if pair is not None:
            pair.solutions.append(loc)
            used_regex = True
        else:
            unpaired_solutions.append(loc)

    # Stage 2b/2c/2d/2e: back-of-book partition + per-subtype loop. Replaces
    # the legacy single-regex approach (which required immediate adjacency
    # between `## Chapter N` and `## Multiple Choice` and never matched the
    # actual Mathpix output where Matching / True/False / Completion blocks
    # sit between them).
    back_of_book = _partition_back_of_book(full_text)
    for chapter_num, sections in back_of_book.items():
        for section_name, bodies in sections.items():
            n_occ = len(bodies)
            for occ, body in enumerate(bodies, start=1):
                if section_name == "Multiple Choice":
                    for m in _MC_ANSWER_PAIR.finditer(body):
                        mc_num, letter = m.group(1), m.group(2)
                        if _try_pair_or_unpaired(
                            pairings_by_id,
                            unpaired_solutions,
                            candidate_ids=_candidate_ids(
                                "MC", chapter_num, occ, n_occ, mc_num
                            ),
                            text=f"({letter})",
                            role="solution",
                            page_idx=0,
                        ):
                            used_regex = True
                elif section_name == "Matching":
                    column_b = _extract_column_b(full_text, chapter_num)
                    for m in _MC_ANSWER_PAIR.finditer(body):
                        mat_num, letter = m.group(1), m.group(2)
                        option_text = column_b.get(letter)
                        text = (
                            f"({letter}) {option_text}"
                            if option_text
                            else f"({letter})"
                        )
                        if _try_pair_or_unpaired(
                            pairings_by_id,
                            unpaired_solutions,
                            candidate_ids=_candidate_ids(
                                "MAT", chapter_num, occ, n_occ, mat_num
                            ),
                            text=text,
                            role="solution",
                            page_idx=0,
                        ):
                            used_regex = True
                elif section_name == "True/False":
                    for m in _TF_ANSWER_SPLIT.finditer(body):
                        tf_num = m.group(1)
                        raw_answer = m.group(2).strip()
                        if raw_answer == "T":
                            text = "True."
                        elif raw_answer == "F":
                            text = "False."
                        else:
                            text = (
                                "False — replace underlined word with: "
                                f"{raw_answer}"
                            )
                        if _try_pair_or_unpaired(
                            pairings_by_id,
                            unpaired_solutions,
                            candidate_ids=_candidate_ids(
                                "TF", chapter_num, occ, n_occ, tf_num
                            ),
                            text=text,
                            role="solution",
                            page_idx=0,
                        ):
                            used_regex = True
                elif section_name == "Completion":
                    for m in _CMP_ANSWER_SPLIT.finditer(body):
                        cmp_num = m.group(1)
                        answer = m.group(2).strip()
                        if _try_pair_or_unpaired(
                            pairings_by_id,
                            unpaired_solutions,
                            candidate_ids=_candidate_ids(
                                "CMP", chapter_num, occ, n_occ, cmp_num
                            ),
                            text=answer,
                            role="solution",
                            page_idx=0,
                        ):
                            used_regex = True

    # Stage 3: LLM content-pairing for problems still without a solution.
    # Bishop-style separate solution manuals carry no `Solution N.M` markers,
    # so Stages 1-2 never bridge the statement → solution gap; the agent
    # matches by content. Omits unmatchable problems (per prompt contract);
    # `audit_coverage` + `allow_unsolved` enforce the gap.
    used_llm = False
    sm_config = config.get("pipeline", {}).get("solution_manual", {})
    if sm_config.get("stage3_enabled", True):
        unpaired = [p for p in pairings if not p.solutions]
        _, solutions_region = _partition_statement_solution_regions(full_text)
        if unpaired and solutions_region:
            prompts_root = config.get("prompts", {}).get("prompts", {})
            sm_prompts = prompts_root.get("solution_manual", {})
            system_prompt = sm_prompts.get("problem_pairing", "")
            problems_block = "\n".join(
                f"- {p.problem_id}: {p.statement.text[:300]}" for p in unpaired
            )
            user_prompt = (
                "Unpaired problems (id: statement excerpt):\n"
                f"{problems_block}\n\n"
                "Solutions region (worked solutions, numbered as bare `N.M`):\n"
                f"{solutions_region}"
            )
            models_config = config.get("models", {}).get("models", {}).get("llm", {})
            result = problem_pairing_agent.run_sync(
                user_prompt,
                instructions=system_prompt,
                model=get_model_string(models_config),
            )
            response: ProblemPairingResponse = result.output
            for loc in response.solutions:
                pair = pairings_by_id.get(loc.problem_id)
                if pair is not None:
                    pair.solutions.append(loc)
                    used_llm = True

    method: Literal["regex", "llm", "mixed"] = (
        "mixed" if used_llm and used_regex
        else "llm" if used_llm
        else "regex"
    )

    return PairingResult(
        pairings=pairings,
        unpaired_solutions=unpaired_solutions,
        method=method,
        confidence=1.0,
    )


def resolve_references(
    problem: ProblemUnit,
    current_index: ChapterIndex,
    prior_indexes: list[ChapterIndex],
) -> ProblemUnit:
    """Inline equation/theorem text and collect figure refs for image attachment.

    Mutates ``problem.statement``, ``problem.solution``, and
    ``problem.referenced_figures`` in place.
    """
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
            logger.warning(
                f"Unresolved equation reference ({eq_id}) in problem {problem.problem_id}"
            )
            return m.group(0)

        def _repl_thm(m: re.Match) -> str:
            t_id = m.group(1)
            t = theorems.get(t_id)
            if t:
                stmt_short = t.statement[:200]
                return f"Theorem {t_id} ({t.kind}): {stmt_short}"
            logger.warning(
                f"Unresolved theorem reference {t_id} in problem {problem.problem_id}"
            )
            return m.group(0)

        text = _REF_EQUATION.sub(_repl_eq, text)
        text = _REF_THEOREM.sub(_repl_thm, text)
        return text

    problem.statement = _inline(problem.statement)
    if problem.solution:
        problem.solution = _inline(problem.solution)

    # Collect figure refs for image attachment on cards.
    for text in [problem.statement, problem.solution or ""]:
        for m in _REF_FIGURE.finditer(text):
            fig_id = m.group(1)
            fig = figures.get(fig_id)
            if fig and fig.image_path not in problem.referenced_figures:
                problem.referenced_figures.append(fig.image_path)

    problem.char_count = len(problem.statement) + len(problem.solution or "")
    return problem


def classify_card_plan(problem: ProblemUnit, sm_config: dict[str, Any]) -> CardPlan:
    """Heuristic-only card-plan classification (no LLM call in v1).

    Args:
        problem: Resolved problem with char_count populated.
        sm_config: solution_manual config block.

    Returns:
        CardPlan respecting the ≤5 card cap.
    """
    long_threshold = sm_config.get("long_problem_chars", 4000)

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


def _format_problem_card_prompt(
    problem: ProblemUnit,
    plan: CardPlan,
    doc_summary: DocumentSummary,
    citation_key: str,
) -> str:
    """Build the user prompt for problem_card_gen_agent."""
    required_tags = [
        "problem-set",
        f"chapter-{problem.chapter or 'unknown'}",
        ProblemTag(
            citation_key=citation_key, problem_id=problem.problem_id
        ).render(),
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


def generate_cards_for_problem(
    problem: ProblemUnit,
    plan: CardPlan,
    doc_summary: DocumentSummary,
    citation_key: str,
    config: dict[str, Any],
) -> tuple[list[PlainCard], ProblemProvenance | None]:
    """Single-problem card generation via problem_card_gen_agent.

    Honors ``enable_full_solution_cards`` flag — if False, downgrades the plan
    before constructing the prompt.
    """
    sm_config = config.get("pipeline", {}).get("solution_manual", {})

    if not sm_config.get("enable_full_solution_cards", False) and plan.include_full_solution:
        plan = plan.model_copy(
            update={
                "include_full_solution": False,
                "n_cards": plan.n_cards - 1,
            }
        )
        logger.info(
            f"enable_full_solution_cards=False; downgrading plan for problem {problem.problem_id}"
        )

    prompts_root = config.get("prompts", {}).get("prompts", {})
    sm_prompts = prompts_root.get("solution_manual", {})
    prompt_key = _PROMPT_KEY_BY_SUBTYPE.get(problem.subtype, "problem_card_gen")
    system_prompt = sm_prompts.get(prompt_key, sm_prompts.get("problem_card_gen", ""))
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

    # Stamp card_subtype from the plan, in order. The LLM can omit the field
    # (it defaults to "regular" on PlainCard) and we need the audit to find
    # the right subtypes — code knows the plan, so trust the plan, not the LLM.
    expected_subtypes: list[str] = []
    if plan.include_main:
        expected_subtypes.append("problem_main")
    expected_subtypes.extend(["subproblem"] * len(plan.subproblem_labels))
    if plan.include_overview:
        expected_subtypes.append("problem_overview")
    if plan.include_full_solution:
        expected_subtypes.append("full_solution")

    for card, subtype in zip(response.cards, expected_subtypes, strict=False):
        card.card_subtype = subtype  # type: ignore[assignment]

    # Stamp the canonical problem tag too — required by audit Part 3.
    canonical_tag = ProblemTag(
        citation_key=citation_key, problem_id=problem.problem_id
    ).render()
    for card in response.cards:
        if canonical_tag not in card.tags:
            card.tags.append(canonical_tag)

    # Attach figure images to card backs (problem_main / problem_overview).
    for card in response.cards:
        if problem.referenced_figures and card.back.image_path is None:
            card.back.image_path = problem.referenced_figures[0]

    provenance = (
        response.provenance_entries[0] if response.provenance_entries else None
    )
    return response.cards, provenance


def audit_coverage(
    problems: list[ProblemUnit],
    pairings: PairingResult,
    cards: list[PlainCard],
    citation_key: str,
    allow_unsolved: bool = False,
) -> None:
    """Three-part hard-fail coverage audit.

    Part 1: every enumerated problem appears in pairings.
    Part 2: every pairing has at least one solution unless allow_unsolved.
    Part 3: every paired problem has exactly one ``card_subtype="problem_main"``
    card (parsed via :class:`ProblemTag`).
    """
    enumerated_ids = {p.problem_id for p in problems}
    paired_ids = {p.problem_id for p in pairings.pairings}

    # Part 1: pairings cover all enumerated problems.
    missing_from_pairings = enumerated_ids - paired_ids
    if missing_from_pairings:
        raise CoverageError(missing=missing_from_pairings)

    # Part 2: each pairing has at least one solution.
    unsolved = {p.problem_id for p in pairings.pairings if not p.solutions}
    if unsolved and not allow_unsolved:
        raise CoverageError(unsolved=unsolved)
    if unsolved and allow_unsolved:
        logger.warning(
            f"allow_unsolved=True; {len(unsolved)} problems have no paired solution: {sorted(unsolved)}"
        )

    # Part 3: exactly one problem_main card per paired problem.
    main_card_counts: Counter[str] = Counter()
    for card in cards:
        if card.card_subtype != "problem_main":
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


def run_solution_manual_override(
    pipeline: Any,
    cleaned_files: list[Path],
    doc_summary: DocumentSummary,
    strict: bool = True,
) -> tuple[list[PlainCard], ProvenanceLog]:
    """Whole-document problem-set runner.

    Used by ``mode=solution_manual`` (explicit override) AND by ``mode=full``
    classifier dispatch when feeding a per-section file subset.

    Args:
        pipeline: The :class:`Pipeline` instance (passes config + state).
        cleaned_files: Per-page cleaned markdown (whole doc OR a section's pages).
        doc_summary: DocumentSummary from the existing summary stage.
        strict: When True (default, mode=solution_manual contract), raise if no
            problems are enumerated. When False (mode=full per-section call),
            warn and return empty results — a section may genuinely lack
            ``N.M``-numbered theory-problems (e.g. Schaum's MC review which
            uses ``1.`` / ``2.`` / ... numbering).

    Returns:
        ``(all_cards, provenance_log)``.
    """
    config = pipeline.config
    sm_config = config.get("pipeline", {}).get("solution_manual", {})
    chapter_id = pipeline.audio_prefix
    citation_key = pipeline.citation_key

    # Load prior chapter indexes for cross-reference resolution.
    prior_indexes: list[ChapterIndex] = []
    for path_str in sm_config.get("chapter_indexes", []) or []:
        prior_indexes.append(load_chapter_index(Path(path_str)))

    # Build current chapter's index from the cleaned markdown.
    current_index = build_chapter_index(cleaned_files, chapter_id=chapter_id)

    # Enumerate → pair → resolve refs → plan → generate.
    problems = enumerate_problems(cleaned_files, chapter_id=chapter_id)
    if not problems:
        if strict:
            raise RuntimeError(
                "No problems enumerated. Verify the input PDF contains numbered "
                "items in any of: theory-problems (N.M), Multiple Choice "
                "(1./2./...), Matching (Column A items), True/False (numbered "
                "statements), or Completion (numbered fill-in-blank items)."
            )
        logger.warning(
            "No numbered problems found in the supplied files; "
            "skipping problem-set pipeline for this section."
        )
        return [], ProvenanceLog(chapter_id=chapter_id)

    pairings = pair_problems_across_pages(problems, cleaned_files, config)
    problems = [
        resolve_references(p, current_index, prior_indexes) for p in problems
    ]
    plans = [classify_card_plan(p, sm_config) for p in problems]

    all_cards: list[PlainCard] = []
    provenance_entries: list[ProblemProvenance] = []
    for problem, plan in zip(problems, plans, strict=True):
        cards, prov = generate_cards_for_problem(
            problem, plan, doc_summary, citation_key, config
        )
        all_cards.extend(cards)
        if prov is not None:
            provenance_entries.append(prov)

    # Persist diagnostic artifacts BEFORE the audit so we have something to
    # inspect when audit fails. Cards aren't yet rendered to .apkg-bound
    # markdown; this is a debug dump of the LLM output.
    output_base = pipeline.output_base
    pairing_path = output_base / "problem-pairings.yaml"
    pairing_path.write_text(
        yaml.safe_dump(pairings.model_dump(), sort_keys=False)
    )
    logger.info(f"Wrote pairing artifact: {pairing_path}")

    debug_path = output_base / "cards-debug.yaml"
    problem_subtype_counts = Counter(p.subtype for p in problems)
    debug_path.write_text(
        yaml.safe_dump(
            {
                "n_cards": len(all_cards),
                "subtype_counts": dict(Counter(c.card_subtype for c in all_cards)),
                "problem_subtype_counts": dict(problem_subtype_counts),
                "cards": [
                    {
                        "front": c.front.text[:200],
                        "back": c.back.text[:200],
                        "tags": list(c.tags),
                        "card_subtype": c.card_subtype,
                    }
                    for c in all_cards
                ],
            },
            sort_keys=False,
        )
    )
    logger.info(f"Wrote cards debug artifact: {debug_path}")

    audit_coverage(
        problems,
        pairings,
        all_cards,
        citation_key,
        allow_unsolved=sm_config.get("allow_unsolved", False),
    )

    provenance_log = ProvenanceLog(
        chapter_id=chapter_id, entries=provenance_entries
    )

    return all_cards, provenance_log
