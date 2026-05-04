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


# Regex anchors. Schaum's `1.1`, `1.2`, ... start lines; the first paragraph
# after the ID is the statement, the rest until the next ID is the solution.
_THEORY_PROBLEM = re.compile(
    r"^([0-9]+)\.([0-9]+)\b\s+(.+?)(?=^[0-9]+\.[0-9]+\b|\Z)",
    re.MULTILINE | re.DOTALL,
)
# Stage-2 markers
_SOLUTION_MARKER = re.compile(
    r"^Solution\s+([0-9]+)\.([0-9]+)\b\s*[:.]?\s*(.+?)(?=^Solution\s+[0-9]+\.[0-9]+|\Z)",
    re.MULTILINE | re.DOTALL,
)
_MC_ANSWER_BLOCK = re.compile(
    r"^Chapter\s+([0-9]+)\s*\n+\s*Multiple Choice\s*\n+\s*((?:[0-9]+\.\s*[a-z]\s*)+)",
    re.MULTILINE,
)
_MC_ANSWER_PAIR = re.compile(r"([0-9]+)\.\s*([a-z])\b")

# Reference-resolution patterns
_REF_EQUATION = re.compile(r"equation\s*\(([0-9]+\.[0-9]+)\)", re.IGNORECASE)
_REF_FIGURE = re.compile(r"Figure\s+([0-9]+\.[0-9]+)", re.IGNORECASE)
_REF_THEOREM = re.compile(r"Theorem\s+([0-9]+\.[0-9]+)", re.IGNORECASE)


def enumerate_problems(
    clean_md_files: list[Path], chapter_id: str | None = None
) -> list[ProblemUnit]:
    """Regex-first problem enumeration. Returns list of ProblemUnits.

    Schaum's `N.M` numbering produces theory_problem subtypes with the answer
    paragraph paired inline. Returns empty list if no problems found; callers
    can decide to fall back to LLM enumeration.

    Args:
        clean_md_files: Per-page cleaned markdown files.
        chapter_id: Optional chapter identifier (e.g. ``"alcamo2010_CH01"``).

    Returns:
        List of enumerated ProblemUnits, in document order.
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

    # Stage 2b: back-of-book MC answer blocks.
    for m in _MC_ANSWER_BLOCK.finditer(full_text):
        chapter_num = m.group(1)
        for pair_match in _MC_ANSWER_PAIR.finditer(m.group(2)):
            mc_num, letter = pair_match.group(1), pair_match.group(2)
            # Two possible IDs: the chapter-prefixed MC-CHN-n form, or bare MC-n.
            for candidate_id in (f"MC-CH{chapter_num}-{mc_num}", f"MC-{mc_num}"):
                pair = pairings_by_id.get(candidate_id)
                if pair is not None:
                    pair.solutions.append(
                        ProblemLocation(
                            problem_id=candidate_id,
                            role="solution",
                            page_idx=0,
                            start_char=pair_match.start(),
                            end_char=pair_match.end(),
                            text=f"({letter})",
                        )
                    )
                    used_regex = True
                    break

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
                "problems matching the regex N.M (e.g. '1.1', '2.7')."
            )
        logger.warning(
            "No N.M-numbered problems found in the supplied files; "
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
    debug_path.write_text(
        yaml.safe_dump(
            {
                "n_cards": len(all_cards),
                "subtype_counts": dict(Counter(c.card_subtype for c in all_cards)),
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
