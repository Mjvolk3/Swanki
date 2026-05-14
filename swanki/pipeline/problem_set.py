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
_SECTION_OR_BACK_OF_BOOK = re.compile(
    r"^(?:Multiple Choice\.\s+\S|Matching\.\s+\S|True/False\.\s+\S|"
    r"Completion\.\s+\S|##\s+Answers|##\s+Chapter\s+\d)",
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

# Back-of-book partition.
_BACK_CHAPTER_HEADER = re.compile(r"^##\s+Chapter\s+(\d+)\s*$", re.MULTILINE)
_BACK_SECTION_HEADER = re.compile(
    r"^##\s+(Multiple Choice|Matching|True/False|Completion)\s*$",
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


def _section_span(
    full_text: str, start_pattern: re.Pattern[str]
) -> tuple[int, int] | None:
    """Locate one in-chapter review-section's char span.

    Returns ``(start, end)`` for the first match of ``start_pattern``. The end
    is the start of the next review-section divider OR the back-of-book block,
    whichever comes first. Returns ``None`` if the section is absent.
    """
    m = start_pattern.search(full_text)
    if m is None:
        return None
    nxt = _SECTION_OR_BACK_OF_BOOK.search(full_text, m.end())
    end = nxt.start() if nxt is not None else len(full_text)
    return (m.start(), end)


def _enumerate_multiple_choice(full_text: str, chapter: str) -> list[ProblemUnit]:
    """Enumerate Multiple Choice items in the chapter's MC section."""
    span = _section_span(full_text, _MC_SECTION)
    if span is None:
        return []
    section_text = full_text[span[0] : span[1]]
    out: list[ProblemUnit] = []
    for m in _MC_ITEM.finditer(section_text):
        item_num = m.group(1)
        stem = m.group(2).strip()
        choices_block = m.group(3).rstrip()
        statement = f"{item_num}. {stem}\n{choices_block}".strip()
        out.append(
            ProblemUnit(
                problem_id=f"MC-CH{chapter}-{item_num}",
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
    span = _section_span(full_text, _MATCHING_SECTION)
    if span is None:
        return []
    section_text = full_text[span[0] : span[1]]
    column_b = _extract_column_b(full_text, chapter)
    options_text = "\n".join(f"({letter}) {text}" for letter, text in column_b.items())

    out: list[ProblemUnit] = []
    for m in _MATCHING_ITEM.finditer(section_text):
        item_num = m.group(1)
        stmt_body = m.group(2).strip()
        # Filter: skip the column-B option lines (they match `\(letter\) text`,
        # not `\d+. text`, so they wouldn't be captured by _MATCHING_ITEM
        # anyway) and any item whose body starts with `## Column` (defensive
        # guard against the section header bleeding into a previous item's
        # body — the lookahead already prevents this, but cheap to assert).
        if stmt_body.startswith("## Column"):
            continue
        statement = (
            f"{item_num}. {stmt_body}\n\nOptions:\n{options_text}"
            if options_text
            else f"{item_num}. {stmt_body}"
        )
        out.append(
            ProblemUnit(
                problem_id=f"MAT-CH{chapter}-{item_num}",
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
    span = _section_span(full_text, _TF_SECTION)
    if span is None:
        return []
    section_text = full_text[span[0] : span[1]]
    out: list[ProblemUnit] = []
    for m in _TF_ITEM.finditer(section_text):
        item_num = m.group(1)
        stmt_body = m.group(2).strip()
        statement = f"{item_num}. True or false: {stmt_body}"
        out.append(
            ProblemUnit(
                problem_id=f"TF-CH{chapter}-{item_num}",
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
    span = _section_span(full_text, _COMPLETION_SECTION)
    if span is None:
        return []
    section_text = full_text[span[0] : span[1]]
    out: list[ProblemUnit] = []
    for m in _COMPLETION_ITEM.finditer(section_text):
        item_num = m.group(1)
        body = m.group(2).strip()
        readable = body.replace("$\\_\\_\\_\\_$", "____")
        statement = f"{item_num}. Fill in the blank: {readable}"
        out.append(
            ProblemUnit(
                problem_id=f"CMP-CH{chapter}-{item_num}",
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

    column_b_re = re.compile(r"^##\s+Column B\s*$", re.MULTILINE)
    cb = column_b_re.search(full_text, chapter_start, chapter_end)
    if cb is None:
        return {}
    options: dict[str, str] = {}
    for opt in _COLUMN_B_OPTION.finditer(full_text, cb.end(), chapter_end):
        letter = opt.group(1)
        text = opt.group(2).strip()
        options[letter] = text
    return options


def _partition_back_of_book(full_text: str) -> dict[str, dict[str, str]]:
    """Walk the back-of-book block and return ``{chapter_num: {section: body}}``.

    Pass 1: locate every ``^## Chapter N$`` boundary and record start indexes.
    Pass 2: within each chapter span, scan ``^## (Multiple Choice|Matching|...)``
    boundaries and capture each section's body (text from the section header
    line's end to the next section header OR chapter header OR end-of-text).
    """
    chapter_matches = list(_BACK_CHAPTER_HEADER.finditer(full_text))
    if not chapter_matches:
        return {}
    out: dict[str, dict[str, str]] = {}
    for i, cm in enumerate(chapter_matches):
        chapter_num = cm.group(1)
        chapter_start = cm.end()
        chapter_end = (
            chapter_matches[i + 1].start()
            if i + 1 < len(chapter_matches)
            else len(full_text)
        )
        sections: dict[str, str] = {}
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
            body = full_text[body_start:body_end].strip()
            sections[section_name] = body
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


def enumerate_problems(
    clean_md_files: list[Path], chapter_id: str | None = None
) -> list[ProblemUnit]:
    """Regex-first problem enumeration. Returns list of ProblemUnits.

    Theory-problems (``N.M`` numbering) are enumerated first. Then four
    review-subtype enumerators (Multiple Choice, Matching, True/False,
    Completion) run, each anchored on its inline section divider. Returns
    empty list if no items match.

    Args:
        clean_md_files: Per-page cleaned markdown files.
        chapter_id: Optional chapter identifier (e.g. ``"alcamo2010_CH01"``).

    Returns:
        List of enumerated ProblemUnits, in document order (theory then
        review-subtypes).
    """
    problems: list[ProblemUnit] = []
    full_text = "\n\n".join(f.read_text() for f in clean_md_files)

    for m in _THEORY_PROBLEM.finditer(full_text):
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
        for section_name, body in sections.items():
            if section_name == "Multiple Choice":
                for m in _MC_ANSWER_PAIR.finditer(body):
                    mc_num, letter = m.group(1), m.group(2)
                    if _try_pair_or_unpaired(
                        pairings_by_id,
                        unpaired_solutions,
                        candidate_ids=[
                            f"MC-CH{chapter_num}-{mc_num}",
                            f"MC-{mc_num}",
                        ],
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
                        candidate_ids=[
                            f"MAT-CH{chapter_num}-{mat_num}",
                            f"MAT-{mat_num}",
                        ],
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
                        candidate_ids=[
                            f"TF-CH{chapter_num}-{tf_num}",
                            f"TF-{tf_num}",
                        ],
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
                        candidate_ids=[
                            f"CMP-CH{chapter_num}-{cmp_num}",
                            f"CMP-{cmp_num}",
                        ],
                        text=answer,
                        role="solution",
                        page_idx=0,
                    ):
                        used_regex = True

    method: Literal["regex", "llm", "mixed"] = "regex" if used_regex else "regex"

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
