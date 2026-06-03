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
    _partition_back_of_book,
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


# ── OCR-agnostic back-of-book partition (MinerU `#` vs Mathpix `##`) ─────


class TestPartitionOcrAgnostic:
    def test_mineru_hash_partitions(self) -> None:
        """MinerU emits the back-of-book titles as H1 (`# Chapter 1`); the
        loosened `#{1,3}` anchor must partition it just like Mathpix `##`.
        """
        text = (FIXTURE_DIR / "schaum_mineru_back_of_book.md").read_text()
        part = _partition_back_of_book(text)
        assert part["1"]["Multiple Choice"][0].startswith("1. c 2. c 3. a")
        assert part["1"]["Matching"][0] == "1. c 2. d 3. e 4. c 5. b 6. a 7. b 8. e 9. c 10. a"
        assert part["2"]["Completion"][0].startswith("1. elements 2. nitrogen")

    def test_mineru_and_mathpix_produce_same_bodies(self) -> None:
        """The CH01 Matching answer body is identical whether the headers came
        from MinerU (`#`) or Mathpix (`##`) — only the anchor differs.
        """
        mineru = _partition_back_of_book(
            (FIXTURE_DIR / "schaum_mineru_back_of_book.md").read_text()
        )
        mathpix = _partition_back_of_book(
            (FIXTURE_DIR / "schaum_ch01_back_of_book.md").read_text()
        )
        assert mineru["1"]["Matching"][0] == mathpix["1"]["Matching"][0]
        assert (
            mineru["1"]["Multiple Choice"][0]
            == mathpix["1"]["Multiple Choice"][0]
        )


class TestTwoMatchingSections:
    FIXTURE = FIXTURE_DIR / "schaum_two_matching.md"

    def test_enumerates_both_sets(self) -> None:
        problems = enumerate_problems([self.FIXTURE], "alcamo2010_CH03")
        mat = [p for p in problems if p.subtype == "matching"]
        assert len(mat) == 20
        assert [p.problem_id for p in mat] == (
            [f"MAT-CH3-1-{n}" for n in range(1, 11)]
            + [f"MAT-CH3-2-{n}" for n in range(1, 11)]
        )

    def test_partition_holds_two_bodies(self) -> None:
        part = _partition_back_of_book(self.FIXTURE.read_text())
        assert len(part["3"]["Matching"]) == 2

    def test_kth_set_pairs_with_kth_body(self) -> None:
        problems = enumerate_problems([self.FIXTURE], "alcamo2010_CH03")
        result = pair_problems_across_pages(problems, [self.FIXTURE], {})
        # Set 1 body: 1->c (Viruses); set 2 body: 1->e (Cyanobacteria).
        s1 = next(p for p in result.pairings if p.problem_id == "MAT-CH3-1-1")
        s2 = next(p for p in result.pairings if p.problem_id == "MAT-CH3-2-1")
        assert s1.solutions[0].text == "(c) Viruses"
        assert s2.solutions[0].text == "(e) Cyanobacteria"
        assert not result.unpaired_solutions

    def test_set_two_label_disambiguates_but_keeps_item_number(self) -> None:
        problems = enumerate_problems([self.FIXTURE], "alcamo2010_CH03")
        s2_7 = next(p for p in problems if p.problem_id == "MAT-CH3-2-7")
        head = s2_7.statement.splitlines()[0]
        assert head.startswith("7. (set 2)")


class TestPageSpillBody:
    def test_spill_body_tokenizes_full_run(self) -> None:
        """A Completion answer run split by a stray page-number line AND a
        MinerU running-header `# Chapter 2` dup must still tokenize 1-15.
        """
        fixture = FIXTURE_DIR / "schaum_page_spill.md"
        part = _partition_back_of_book(fixture.read_text())
        # O2: the duplicated `# Chapter 2` header collapses into one span.
        assert list(part.keys()) == ["2"]
        body = part["2"]["Completion"][0]
        # O1: the stray `328` page number and residual header are stripped, so
        # the body is one contiguous run carrying both halves of the split.
        assert "10. amino acids" in body
        assert "11. peptide bond" in body
        assert "15. uracil" in body
        assert "328" not in body
        assert "Chapter" not in body

    def test_spill_pairs_all_fifteen(self) -> None:
        fixture = FIXTURE_DIR / "schaum_page_spill.md"
        # Synthesize a matching forward Completion section so the back-of-book
        # answers have problems to pair against.
        problems = enumerate_problems([fixture], "alcamo2010_CH02")
        result = pair_problems_across_pages(problems, [fixture], {})
        # The 15 answers must not silently vanish: they pair OR go unpaired.
        cmp_unpaired = [
            u.problem_id
            for u in result.unpaired_solutions
            if u.problem_id.startswith("CMP-")
        ]
        assert len(cmp_unpaired) == 15


class TestOrphanPreFirstChapterSpill:
    """A prior chapter's answer-key tail spills onto the top of the target
    chapter's answer page as headerless `# Completion` / `# Matching` blocks
    BEFORE the first `# Chapter N` header (real Alcamo CH05, book page 329).

    The forward section span must terminate at that orphan boundary so the
    orphan `N.` answer lines are NOT mis-enumerated as forward Matching items,
    and the back-of-book partition must discard the orphan (it precedes
    `# Chapter 4`). Target chapter 5 carries TWO Matching sets; the real
    `MAT-CH5-2-1` must pair to `(d)`, not be stolen by the orphan.
    """

    FIXTURE = FIXTURE_DIR / "schaum_orphan_spill.md"

    def test_orphan_discarded_from_partition(self) -> None:
        part = _partition_back_of_book(self.FIXTURE.read_text())
        # Only real chapter headers; the orphan pre-Chapter-4 spill is dropped.
        assert sorted(part.keys()) == ["4", "5", "6"]

    def test_no_duplicate_matching_ids(self) -> None:
        problems = enumerate_problems([self.FIXTURE], "alcamo2010_CH05")
        mat_ids = [p.problem_id for p in problems if p.subtype == "matching"]
        # Exactly the two clean sets, 1-10 each, no orphan-injected dups.
        assert mat_ids == (
            [f"MAT-CH5-1-{n}" for n in range(1, 11)]
            + [f"MAT-CH5-2-{n}" for n in range(1, 11)]
        )
        assert len(mat_ids) == len(set(mat_ids))

    def test_set_two_item_one_pairs_to_d(self) -> None:
        problems = enumerate_problems([self.FIXTURE], "alcamo2010_CH05")
        result = pair_problems_across_pages(problems, [self.FIXTURE], {})
        s2_1 = [
            p for p in result.pairings if p.problem_id == "MAT-CH5-2-1"
        ]
        assert len(s2_1) == 1
        assert len(s2_1[0].solutions) == 1
        assert s2_1[0].solutions[0].text == "(d) Thermophile"

    def test_every_matching_item_single_solution(self) -> None:
        problems = enumerate_problems([self.FIXTURE], "alcamo2010_CH05")
        result = pair_problems_across_pages(problems, [self.FIXTURE], {})
        mat = [
            p for p in result.pairings if p.problem_id.startswith("MAT-CH5")
        ]
        assert len(mat) == 20
        assert all(len(p.solutions) == 1 for p in mat)

    def test_orphan_completion_answers_not_enumerated(self) -> None:
        # The orphan Ch3 `# Completion` line (nanometer, mycoplasmas, …) must
        # never reach a Chapter-5 Matching statement.
        problems = enumerate_problems([self.FIXTURE], "alcamo2010_CH05")
        assert not any(
            "nanometer" in p.statement for p in problems
        )


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
