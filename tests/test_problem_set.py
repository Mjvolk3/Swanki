"""
tests/test_problem_set.py
[[tests.test_problem_set]]
https://github.com/Mjvolk3/Swanki/tree/main/tests/test_problem_set.py

Unit tests for the multi-subtype enumerators (Multiple Choice, Matching,
True/False, Completion) and back-of-book pairing branches in
swanki.pipeline.problem_set, anchored on real Schaum's CH01 OCR fixtures.
"""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from swanki.models.cards import CardContent, PlainCard
from swanki.models.document import DocumentSummary
from swanki.models.problem_set import (
    PairingResult,
    ProblemCardBatchResponse,
    ProblemLocation,
    ProblemPairing,
    ProblemTag,
    ProblemUnit,
)
from swanki.pipeline.problem_set import (
    CoverageError,
    _enumerate_completion,
    _enumerate_matching,
    _enumerate_multiple_choice,
    _enumerate_true_false,
    audit_coverage,
    enumerate_problems,
    generate_cards_for_problem,
    pair_problems_across_pages,
)

FIXTURE_DIR = Path(__file__).parent / "fixtures" / "problem_set"


def _make_card(tag: str, subtype: str = "problem_main") -> PlainCard:
    return PlainCard(
        front=CardContent(text="Q"),
        back=CardContent(text="A"),
        tags=[tag],
        card_subtype=subtype,  # type: ignore[arg-type]
    )


# ── Enumerator tests ────────────────────────────────────────────────────


class TestEnumerateMultipleChoice:
    def test_finds_all_15(self) -> None:
        text = (FIXTURE_DIR / "schaum_ch01_mc_section.md").read_text()
        problems = _enumerate_multiple_choice(text, "1")
        assert len(problems) == 15
        assert [p.problem_id for p in problems] == [
            f"MC-CH1-{n}" for n in range(1, 16)
        ]

    def test_each_item_carries_all_choices(self) -> None:
        text = (FIXTURE_DIR / "schaum_ch01_mc_section.md").read_text()
        problems = _enumerate_multiple_choice(text, "1")
        for p in problems:
            assert "(a)" in p.statement
            assert "(b)" in p.statement
            assert "(c)" in p.statement
            assert "(d)" in p.statement
            assert p.subtype == "multiple_choice"
            assert p.chapter == "1"

    def test_returns_empty_for_section_absent(self) -> None:
        assert _enumerate_multiple_choice("nothing here", "1") == []


class TestEnumerateMatching:
    def test_skips_missing_item5(self) -> None:
        text = (FIXTURE_DIR / "schaum_ch01_matching_section.md").read_text()
        problems = _enumerate_matching(text, "1")
        ids = [p.problem_id for p in problems]
        assert "MAT-CH1-5" not in ids
        assert ids == [
            "MAT-CH1-1",
            "MAT-CH1-2",
            "MAT-CH1-3",
            "MAT-CH1-4",
            "MAT-CH1-6",
            "MAT-CH1-7",
            "MAT-CH1-8",
            "MAT-CH1-9",
            "MAT-CH1-10",
        ]

    def test_includes_full_column_b_options(self) -> None:
        text = (FIXTURE_DIR / "schaum_ch01_matching_section.md").read_text()
        problems = _enumerate_matching(text, "1")
        first = problems[0]
        for letter in ("a", "b", "c", "d", "e"):
            assert f"({letter})" in first.statement
        assert "Bacteria" in first.statement
        assert "Cyanobacteria" in first.statement


class TestEnumerateTrueFalse:
    def test_finds_all_15(self) -> None:
        text = (FIXTURE_DIR / "schaum_ch01_true_false_section.md").read_text()
        problems = _enumerate_true_false(text, "1")
        assert len(problems) == 15
        assert [p.problem_id for p in problems] == [
            f"TF-CH1-{n}" for n in range(1, 16)
        ]

    def test_strips_blank_marker_from_statement(self) -> None:
        text = (FIXTURE_DIR / "schaum_ch01_true_false_section.md").read_text()
        problems = _enumerate_true_false(text, "1")
        for p in problems:
            assert "$\\_\\_\\_\\_$" not in p.statement
            assert p.statement.startswith(f"{p.problem_id.split('-')[-1]}. True or false:")
            # The "originally underlined term" framing was dropped — Mathpix
            # strips the underline markup so the front cannot reference it.
            assert "originally underlined" not in p.statement


class TestEnumerateCompletion:
    def test_finds_all_15_with_blank_token(self) -> None:
        text = (FIXTURE_DIR / "schaum_ch02_completion_section.md").read_text()
        problems = _enumerate_completion(text, "2")
        assert len(problems) == 15
        for p in problems:
            assert p.statement.startswith(p.problem_id.split("-")[-1] + ". Fill in the blank:")
            assert "____" in p.statement

    def test_skips_numbered_prose_without_blank(self) -> None:
        # No blank token → not enumerated as Completion.
        synth = (
            "Completion. Fill in the blanks below.\n\n"
            "1. The capital of France is Paris.\n"
            "2. Two plus two is four.\n"
        )
        assert _enumerate_completion(synth, "1") == []

    def test_returns_empty_when_section_absent(self) -> None:
        assert _enumerate_completion("nothing here", "1") == []


# ── Pairing tests ───────────────────────────────────────────────────────


def _full_section_subset_files() -> list[Path]:
    """Pages 8-12 of the real Schaum's CH01 OCR — the review-section span the
    classifier routes to ``review_exercises``.
    """
    src = Path(
        "/scratch/projects/torchcell-scratch/Swanki_Data/"
        "alcamoSchaumsOutlineMicrobiology2010_CH01_6/clean-md-singles"
    )
    if not src.exists():
        pytest.skip(f"Source OCR not available at {src}")
    return sorted(src.glob("page-*.md"), key=lambda p: int(p.stem.split("-")[1]))[7:]


class TestPairingBackOfBook:
    def test_mc_pairs_resolve_with_markdown_chapter_header(self) -> None:
        files = _full_section_subset_files()
        problems = enumerate_problems(
            files, "alcamoSchaumsOutlineMicrobiology2010_CH01_6"
        )
        result = pair_problems_across_pages(problems, files, {})
        mc_pairs = [p for p in result.pairings if p.problem_id.startswith("MC-CH1-")]
        assert len(mc_pairs) == 15
        for p in mc_pairs:
            assert len(p.solutions) == 1, f"{p.problem_id} should have 1 solution"

    def test_matching_solutions_carry_full_column_b_text(self) -> None:
        files = _full_section_subset_files()
        problems = enumerate_problems(
            files, "alcamoSchaumsOutlineMicrobiology2010_CH01_6"
        )
        result = pair_problems_across_pages(problems, files, {})
        mat1 = next(p for p in result.pairings if p.problem_id == "MAT-CH1-1")
        # Back-of-book says item 1 → c. Column B (c) = Viruses. Pair text
        # should NOT be just "(c)" — must include the option text.
        assert mat1.solutions[0].text == "(c) Viruses"

    def test_true_false_handles_letter_and_replacement_word(self) -> None:
        files = _full_section_subset_files()
        problems = enumerate_problems(
            files, "alcamoSchaumsOutlineMicrobiology2010_CH01_6"
        )
        result = pair_problems_across_pages(problems, files, {})
        # TF-CH1-1 answer is "diatoms" (replacement word).
        tf1 = next(p for p in result.pairings if p.problem_id == "TF-CH1-1")
        assert "diatoms" in tf1.solutions[0].text
        assert tf1.solutions[0].text.startswith("False —")
        # TF-CH1-2 answer is "T" (single letter, true).
        tf2 = next(p for p in result.pairings if p.problem_id == "TF-CH1-2")
        assert tf2.solutions[0].text == "True."

    def test_unpaired_back_of_book_answer_for_missing_matching_item5(
        self,
    ) -> None:
        """OCR drops Column A item 5 — the back-of-book entry for item 5 must
        land in unpaired_solutions (not be silently dropped on the floor like
        the legacy Stage 2b).
        """
        files = _full_section_subset_files()
        problems = enumerate_problems(
            files, "alcamoSchaumsOutlineMicrobiology2010_CH01_6"
        )
        result = pair_problems_across_pages(problems, files, {})
        unpaired_ids = [u.problem_id for u in result.unpaired_solutions]
        assert "MAT-CH1-5" in unpaired_ids


class TestPairingCompletionMultiWord:
    def test_completion_handles_multi_word_answers(self) -> None:
        fpath = FIXTURE_DIR / "schaum_ch02_completion_section.md"
        problems = enumerate_problems([fpath], "fixture_CH02")
        result = pair_problems_across_pages(problems, [fpath], {})
        cmp3 = next(p for p in result.pairings if p.problem_id == "CMP-CH2-3")
        assert cmp3.solutions[0].text == "organic compounds"
        cmp9 = next(p for p in result.pairings if p.problem_id == "CMP-CH2-9")
        assert cmp9.solutions[0].text == "dehydration synthesis"


# ── Audit tests ─────────────────────────────────────────────────────────


def _build_audit_inputs(
    citation_key: str = "alcamo2010",
) -> tuple[list[ProblemUnit], PairingResult, list[PlainCard]]:
    """Construct enumerated problems + paired solutions + matching cards for
    the audit. Mirrors the real CH01 review-section shape: 30 theory + 15 MC +
    9 Matching (item 5 missing) + 15 T/F = 69 problems.
    """
    problems: list[ProblemUnit] = []
    pairings: list[ProblemPairing] = []

    def _add(pid: str, subtype: str, chapter: str) -> None:
        problems.append(
            ProblemUnit(
                problem_id=pid,
                subtype=subtype,  # type: ignore[arg-type]
                chapter=chapter,
                statement="Q",
                solution="A",
                char_count=2,
            )
        )
        pairings.append(
            ProblemPairing(
                problem_id=pid,
                statement=ProblemLocation(
                    problem_id=pid, role="statement", page_idx=0,
                    start_char=0, end_char=1, text="Q",
                ),
                solutions=[
                    ProblemLocation(
                        problem_id=pid, role="solution", page_idx=0,
                        start_char=0, end_char=1, text="A",
                    )
                ],
            )
        )

    for n in range(1, 31):
        _add(f"1.{n}", "theory_problem", "1")
    for n in range(1, 16):
        _add(f"MC-CH1-{n}", "multiple_choice", "1")
    for n in (1, 2, 3, 4, 6, 7, 8, 9, 10):  # item 5 missing
        _add(f"MAT-CH1-{n}", "matching", "1")
    for n in range(1, 16):
        _add(f"TF-CH1-{n}", "true_false", "1")

    pairing_result = PairingResult(
        pairings=pairings, unpaired_solutions=[], method="regex", confidence=1.0
    )
    cards = [
        _make_card(
            tag=ProblemTag(citation_key=citation_key, problem_id=p.problem_id).render()
        )
        for p in problems
    ]
    return problems, pairing_result, cards


class TestAuditCoverage:
    def test_all_subtypes_pass(self) -> None:
        problems, pairings, cards = _build_audit_inputs()
        # Should not raise.
        audit_coverage(problems, pairings, cards, "alcamo2010", allow_unsolved=False)

    def test_unpaired_mc_raises(self) -> None:
        problems, pairings, cards = _build_audit_inputs()
        # Drop the solution from MC-CH1-7.
        target = next(p for p in pairings.pairings if p.problem_id == "MC-CH1-7")
        target.solutions = []
        with pytest.raises(CoverageError) as exc:
            audit_coverage(problems, pairings, cards, "alcamo2010", allow_unsolved=False)
        assert "MC-CH1-7" in exc.value.unsolved

    def test_missing_main_card_raises(self) -> None:
        problems, pairings, cards = _build_audit_inputs()
        # Remove TF-CH1-3's card.
        cards = [
            c
            for c in cards
            if "alcamo2010.problem.TF-CH1-3" not in c.tags
        ]
        with pytest.raises(CoverageError) as exc:
            audit_coverage(problems, pairings, cards, "alcamo2010", allow_unsolved=False)
        assert "TF-CH1-3" in exc.value.missing


# ── Subtype-aware prompt dispatch ──────────────────────────────────────


class TestPromptDispatch:
    @pytest.mark.parametrize(
        ("subtype", "expected_key_fragment"),
        [
            ("theory_problem", "Carry book-numbering as a label"),
            ("multiple_choice", "ONE multiple-choice problem"),
            ("matching", "ONE Matching item"),
            ("true_false", "ONE True/False statement"),
            ("completion", "ONE Completion item"),
        ],
    )
    def test_dispatch_loads_subtype_specific_system_prompt(
        self, subtype: str, expected_key_fragment: str
    ) -> None:
        # Build the real prompts dict and a stub config.
        from omegaconf import OmegaConf

        prompt_path = (
            Path(__file__).parent.parent
            / "swanki"
            / "conf"
            / "prompts"
            / "solution_manual.yaml"
        )
        prompts_data = OmegaConf.to_container(
            OmegaConf.load(prompt_path), resolve=True
        )
        config = {
            "prompts": {"prompts": prompts_data["prompts"]},
            "models": {"models": {"llm": {}}},
            "pipeline": {"solution_manual": {"enable_full_solution_cards": False}},
        }

        problem = ProblemUnit(
            problem_id="MC-CH1-7" if subtype != "theory_problem" else "1.7",
            subtype=subtype,  # type: ignore[arg-type]
            chapter="1",
            statement="Q",
            solution="A",
            char_count=2,
        )
        from swanki.models.problem_set import CardPlan

        plan = CardPlan(n_cards=1, include_main=True)
        doc_summary = DocumentSummary(
            title="t",
            authors=["a"],
            main_topic="m",
            key_contributions=["k"],
            methodology="meth",
            summary=" ".join(["word"] * 120),
            acronyms={},
            technical_terms={},
        )

        captured: dict[str, str] = {}

        def fake_run_sync(user_prompt: str, **kwargs: object) -> object:
            captured["instructions"] = str(kwargs.get("instructions", ""))
            mock_result = MagicMock()
            mock_result.output = ProblemCardBatchResponse(
                cards=[
                    PlainCard(
                        front=CardContent(text="Q"),
                        back=CardContent(text="A"),
                        tags=["problem-set"],
                    )
                ],
                provenance_entries=[],
            )
            return mock_result

        with patch(
            "swanki.pipeline.problem_set.problem_card_gen_agent.run_sync",
            side_effect=fake_run_sync,
        ):
            generate_cards_for_problem(
                problem, plan, doc_summary, "alcamo2010", config
            )

        assert expected_key_fragment in captured["instructions"], (
            f"Subtype {subtype} did not load the expected system prompt. "
            f"Got: {captured['instructions'][:200]!r}"
        )
