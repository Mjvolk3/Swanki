"""
tests/test_glossary.py
[[tests.test_glossary]]
https://github.com/Mjvolk3/Swanki/tree/main/tests/test_glossary.py

Unit tests for swanki.pipeline.glossary: enumeration (mocked agent), the
definition card plan, batched card generation (subtype + tag stamping, surplus
dropping), the coverage audit, and the mode=glossary pipeline dispatch branch.
LLM calls are mocked; no live API/OCR is exercised.
"""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from swanki.models.cards import CardContent, PlainCard
from swanki.models.glossary import (
    DefinitionCardBatchResponse,
    DefinitionCardPlan,
    GlossaryEnumerationResponse,
    GlossaryTag,
    GlossaryUnit,
)
from swanki.pipeline import Pipeline
from swanki.pipeline.glossary import (
    audit_coverage,
    classify_definition_plan,
    enumerate_glossary,
    generate_cards_for_terms,
)
from swanki.pipeline.problem_set import CoverageError


def _config(batch_size: int = 25, generate_example: bool = True) -> dict:
    return {
        "prompts": {
            "prompts": {
                "glossary": {
                    "definition_enumeration": "ENUM",
                    "definition_card_gen": "GEN",
                }
            }
        },
        "models": {"models": {"llm": {"provider": "openai", "model": "gpt-5"}}},
        "pipeline": {
            "glossary": {
                "batch_size": batch_size,
                "generate_example": generate_example,
                "long_entry_chars": 600,
            }
        },
    }


def _card(front: str, back: str) -> PlainCard:
    return PlainCard(
        front=CardContent(text=front),
        back=CardContent(text=back),
        tags=["seed"],
    )


def _definition_main_card(citation: str, slug: str) -> PlainCard:
    return PlainCard(
        front=CardContent(text="**x**"),
        back=CardContent(text="d"),
        tags=[GlossaryTag(citation_key=citation, term_slug=slug).render()],
        card_subtype="definition_main",  # type: ignore[arg-type]
    )


class TestEnumerateGlossary:
    def test_returns_units_and_sets_char_count(self) -> None:
        units = [
            GlossaryUnit(term="abase", definition="Degrade or humble."),
            GlossaryUnit(term="abate", definition="Reduce, diminish."),
        ]
        page = MagicMock()
        page.read_text.return_value = "wordlist page text"
        with patch("swanki.pipeline.glossary.glossary_enumeration_agent") as agent:
            agent.run_sync.return_value = MagicMock(
                output=GlossaryEnumerationResponse(units=units)
            )
            out = enumerate_glossary([page], _config())
        assert [u.term for u in out] == ["abase", "abate"]
        assert out[0].char_count == len("abase") + len("Degrade or humble.")


class TestClassifyDefinitionPlan:
    def test_short_entry_one_card(self) -> None:
        unit = GlossaryUnit(term="abase", definition="d", char_count=20)
        plan = classify_definition_plan(unit, {"long_entry_chars": 600})
        assert plan.n_cards == 1
        assert plan.include_main

    def test_long_entry_still_one_card_v1(self) -> None:
        unit = GlossaryUnit(term="abase", definition="d" * 5000, char_count=5000)
        plan = classify_definition_plan(unit, {"long_entry_chars": 600})
        assert plan.n_cards == 1


class TestGenerateCardsForTerms:
    def test_stamps_subtype_and_canonical_tag(self) -> None:
        units = [
            GlossaryUnit(term="abase", definition="Degrade.", char_count=20),
            GlossaryUnit(term="abate", definition="Reduce.", char_count=15),
        ]
        plans = [DefinitionCardPlan(n_cards=1, include_main=True) for _ in units]
        returned = DefinitionCardBatchResponse(
            cards=[
                _card("**abase**", "Degrade. *e.g.* He abased them."),
                _card("**abate**", "Reduce. *e.g.* The storm abated."),
            ]
        )
        with patch("swanki.pipeline.glossary.definition_card_gen_agent") as agent:
            agent.run_sync.return_value = MagicMock(output=returned)
            cards = generate_cards_for_terms(units, plans, "key2018", _config())
        assert len(cards) == 2
        for card, term in zip(cards, ["abase", "abate"]):
            assert card.card_subtype == "definition_main"
            assert f"key2018.glossary.{term}" in card.tags
            assert "vocabulary" in card.tags
            assert "gre" in card.tags

    def test_surplus_cards_dropped(self) -> None:
        units = [GlossaryUnit(term="abase", definition="d", char_count=5)]
        plans = [DefinitionCardPlan(n_cards=1, include_main=True)]
        returned = DefinitionCardBatchResponse(
            cards=[_card("**abase**", "d"), _card("**extra**", "x")]
        )
        with patch("swanki.pipeline.glossary.definition_card_gen_agent") as agent:
            agent.run_sync.return_value = MagicMock(output=returned)
            cards = generate_cards_for_terms(units, plans, "k", _config())
        assert len(cards) == 1
        assert "k.glossary.abase" in cards[0].tags

    def test_batches_by_batch_size(self) -> None:
        units = [
            GlossaryUnit(term="a", definition="d", char_count=5),
            GlossaryUnit(term="b", definition="d", char_count=5),
        ]
        plans = [DefinitionCardPlan(n_cards=1, include_main=True) for _ in units]
        with patch("swanki.pipeline.glossary.definition_card_gen_agent") as agent:
            agent.run_sync.side_effect = [
                MagicMock(
                    output=DefinitionCardBatchResponse(cards=[_card("**a**", "d")])
                ),
                MagicMock(
                    output=DefinitionCardBatchResponse(cards=[_card("**b**", "d")])
                ),
            ]
            cards = generate_cards_for_terms(units, plans, "k", _config(batch_size=1))
        assert agent.run_sync.call_count == 2
        assert len(cards) == 2


class TestAuditCoverage:
    def test_passes_when_one_card_per_term(self) -> None:
        units = [
            GlossaryUnit(term="abase", definition="d"),
            GlossaryUnit(term="abate", definition="d"),
        ]
        cards = [
            _definition_main_card("k", "abase"),
            _definition_main_card("k", "abate"),
        ]
        audit_coverage(units, cards, "k")  # must not raise

    def test_missing_raises(self) -> None:
        units = [
            GlossaryUnit(term="abase", definition="d"),
            GlossaryUnit(term="abate", definition="d"),
        ]
        cards = [_definition_main_card("k", "abase")]
        with pytest.raises(CoverageError):
            audit_coverage(units, cards, "k")

    def test_duplicate_raises(self) -> None:
        units = [GlossaryUnit(term="abase", definition="d")]
        cards = [
            _definition_main_card("k", "abase"),
            _definition_main_card("k", "abase"),
        ]
        with pytest.raises(CoverageError):
            audit_coverage(units, cards, "k")

    def test_extra_raises(self) -> None:
        units = [GlossaryUnit(term="abase", definition="d")]
        cards = [
            _definition_main_card("k", "abase"),
            _definition_main_card("k", "zzz"),
        ]
        with pytest.raises(CoverageError):
            audit_coverage(units, cards, "k")


class TestGlossaryDispatch:
    """mode=glossary routes the whole document through run_glossary_override."""

    @pytest.fixture()
    def base_config(self) -> dict:
        return {
            "mode": "glossary",
            "pipeline": {
                "processing": {"confirm_before_generation": False},
                "glossary": {},
            },
            "audio": {"audio": {}},
            "output": {"output": {"formats": {}, "create_anki_deck": False}},
            "anki": {"anki": {"enabled": False, "auto_send": False}},
            "models": {"models": {"llm": {"model": "gpt-5"}, "tts": {}}},
            "prompts": {"prompts": {"glossary": {}}},
            "refinement": {"refinement": {"enabled": False}},
            "zotero": {"zotero": {"sync": False}},
        }

    def test_dispatch_calls_override_and_generates_outputs(
        self, base_config, tmp_path
    ) -> None:
        p = Pipeline(base_config)
        p.split_pdf = MagicMock(return_value=[Path("/tmp/p1.pdf")])
        p.convert_to_markdown = MagicMock(return_value=[Path("/tmp/p1.md")])
        p.clean_markdown = MagicMock(return_value=[Path("/tmp/p1_clean.md")])
        p.process_images = MagicMock(return_value=[])
        p.generate_document_summary = MagicMock()
        p.generate_outputs = MagicMock(return_value=({}, []))
        p.generate_audio = MagicMock()
        p.data_dir = tmp_path

        with patch(
            "swanki.pipeline.glossary.run_glossary_override", return_value=[]
        ) as override:
            p.process_full(Path("/tmp/test.pdf"), "test2023")

        override.assert_called_once()
        p.generate_outputs.assert_called_once()
