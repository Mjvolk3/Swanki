"""
tests/test_glossary_models.py
[[tests.test_glossary_models]]
https://github.com/Mjvolk3/Swanki/tree/main/tests/test_glossary_models.py

Unit tests for swanki.models.glossary: slugify_term, DefinitionCardPlan
consistency validation, and the GlossaryTag parser/renderer round-trip.
"""

import pytest
from pydantic import ValidationError

from swanki.models.glossary import (
    DefinitionCardPlan,
    GlossaryTag,
    slugify_term,
)


class TestSlugifyTerm:
    def test_simple_word(self) -> None:
        assert slugify_term("abase") == "abase"

    def test_uppercase_and_whitespace(self) -> None:
        assert slugify_term("  Mixed Case  ") == "mixed-case"

    def test_punctuation_collapses_to_single_hyphen(self) -> None:
        assert slugify_term("e.g.") == "e-g"
        assert slugify_term("self-restraint") == "self-restraint"

    def test_parenthetical_pos(self) -> None:
        assert slugify_term("(verb)") == "verb"

    def test_digits_preserved(self) -> None:
        assert slugify_term("catch-22") == "catch-22"


class TestDefinitionCardPlan:
    def test_one_main_card_valid(self) -> None:
        plan = DefinitionCardPlan(n_cards=1, include_main=True)
        assert plan.n_cards == 1

    def test_n_cards_inconsistent_with_main_raises(self) -> None:
        with pytest.raises(ValidationError):
            DefinitionCardPlan(n_cards=2, include_main=True)

    def test_no_main_card_inconsistent_raises(self) -> None:
        # include_main=False expects 0 cards, but ge=1 forbids 0, so it raises.
        with pytest.raises(ValidationError):
            DefinitionCardPlan(n_cards=1, include_main=False)


class TestGlossaryTag:
    def test_render(self) -> None:
        tag = GlossaryTag(citation_key="ManPrep1000GREwords", term_slug="abase")
        assert tag.render() == "ManPrep1000GREwords.glossary.abase"

    def test_round_trip_simple(self) -> None:
        rendered = GlossaryTag(
            citation_key="ManPrep1000GREwords", term_slug="abase"
        ).render()
        parsed = GlossaryTag.parse(rendered, "ManPrep1000GREwords")
        assert parsed is not None
        assert parsed.term_slug == "abase"

    def test_round_trip_hyphenated_and_digits(self) -> None:
        for slug in ("self-restraint", "catch-22", "e-g"):
            rendered = GlossaryTag(citation_key="key2018", term_slug=slug).render()
            parsed = GlossaryTag.parse(rendered, "key2018")
            assert parsed is not None
            assert parsed.term_slug == slug

    def test_parse_wrong_citation_key_returns_none(self) -> None:
        rendered = GlossaryTag(citation_key="keyA", term_slug="abase").render()
        assert GlossaryTag.parse(rendered, "keyB") is None

    def test_parse_non_glossary_tag_returns_none(self) -> None:
        assert GlossaryTag.parse("key.problem.1.1", "key") is None
        assert GlossaryTag.parse("vocabulary", "key") is None
        assert GlossaryTag.parse("key.glossary.Has Spaces", "key") is None
