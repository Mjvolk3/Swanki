"""
tests/test_problem_set_models.py
[[tests.test_problem_set_models]]
https://github.com/Mjvolk3/Swanki/tree/main/tests/test_problem_set_models.py

Pydantic validation tests for swanki.models.problem_set: ProblemTag round-trip
across all chapter-prefixed forms (MC-CH1-7, MAT-CH1-3, TF-CH1-7, CMP-CH2-9),
plus ProblemUnit subtype Literal coverage.
"""

import pytest
from pydantic import ValidationError

from swanki.models.problem_set import ProblemTag, ProblemUnit


class TestProblemTagRoundTrip:
    def test_theory_problem_round_trip(self) -> None:
        tag = ProblemTag(citation_key="alcamo2010", problem_id="1.7")
        rendered = tag.render()
        assert rendered == "alcamo2010.problem.1.7"
        parsed = ProblemTag.parse(rendered, "alcamo2010")
        assert parsed is not None
        assert parsed.problem_id == "1.7"

    def test_multiple_choice_round_trip(self) -> None:
        tag = ProblemTag(citation_key="alcamo2010", problem_id="MC-CH1-7")
        rendered = tag.render()
        assert rendered == "alcamo2010.problem.MC-CH1-7"
        parsed = ProblemTag.parse(rendered, "alcamo2010")
        assert parsed is not None
        assert parsed.problem_id == "MC-CH1-7"

    def test_matching_round_trip(self) -> None:
        tag = ProblemTag(citation_key="alcamo2010", problem_id="MAT-CH1-3")
        rendered = tag.render()
        parsed = ProblemTag.parse(rendered, "alcamo2010")
        assert parsed is not None
        assert parsed.problem_id == "MAT-CH1-3"

    def test_true_false_round_trip(self) -> None:
        tag = ProblemTag(citation_key="alcamo2010", problem_id="TF-CH1-7")
        rendered = tag.render()
        parsed = ProblemTag.parse(rendered, "alcamo2010")
        assert parsed is not None
        assert parsed.problem_id == "TF-CH1-7"

    def test_completion_round_trip(self) -> None:
        tag = ProblemTag(citation_key="alcamo2010", problem_id="CMP-CH2-9")
        rendered = tag.render()
        parsed = ProblemTag.parse(rendered, "alcamo2010")
        assert parsed is not None
        assert parsed.problem_id == "CMP-CH2-9"

    def test_bare_subtype_form_still_accepted(self) -> None:
        """The legacy bare form (MC-1, MAT-3, TF-7, CMP-9) without a chapter
        prefix is the documented fallback when chapter context is unknown.
        """
        for pid in ("MC-1", "MAT-3", "TF-7", "CMP-9"):
            rendered = f"alcamo2010.problem.{pid}"
            parsed = ProblemTag.parse(rendered, "alcamo2010")
            assert parsed is not None, f"failed to parse bare form {pid}"
            assert parsed.problem_id == pid

    def test_parse_rejects_lowercase_prefix(self) -> None:
        assert ProblemTag.parse(
            "alcamo2010.problem.mc-CH1-7", "alcamo2010"
        ) is None

    def test_parse_rejects_wrong_citation_key(self) -> None:
        assert ProblemTag.parse(
            "alcamo2010.problem.MC-CH1-7", "bishop2017"
        ) is None

    def test_parse_rejects_malformed_tag(self) -> None:
        assert ProblemTag.parse("not.a.tag.shape", "alcamo2010") is None
        assert ProblemTag.parse("alcamo2010.notproblem.MC-CH1-7", "alcamo2010") is None


class TestProblemUnitSubtypeLiteral:
    @pytest.mark.parametrize(
        "subtype",
        ["theory_problem", "multiple_choice", "matching", "true_false", "completion"],
    )
    def test_accepts_all_five_subtypes(self, subtype: str) -> None:
        unit = ProblemUnit(
            problem_id="1.1",
            subtype=subtype,  # type: ignore[arg-type]
            statement="Q",
            char_count=1,
        )
        assert unit.subtype == subtype

    def test_rejects_invalid_subtype(self) -> None:
        with pytest.raises(ValidationError):
            ProblemUnit(
                problem_id="1.1",
                subtype="bogus",  # type: ignore[arg-type]
                statement="Q",
            )
