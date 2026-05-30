"""
swanki/models/glossary.py
[[swanki.models.glossary]]
https://github.com/Mjvolk3/Swanki/tree/main/swanki/models/glossary.py
Test file: tests/test_glossary_models.py

Pydantic models for glossary mode: the definition unit, the definition card
plan, the GlossaryTag parser/renderer, and pydantic-ai response wrappers
(GlossaryEnumerationResponse, DefinitionCardBatchResponse). Response types live
here (not pipeline/glossary.py) to avoid a circular import with llm/agents.py --
the same arrangement as models/problem_set.py.
"""

import re

from pydantic import BaseModel, Field, model_validator

from .cards import PlainCard


def slugify_term(term: str) -> str:
    """Slugify a headword for use in the per-term glossary tag.

    Lowercases, collapses every run of non-alphanumeric characters into a single
    hyphen, and trims leading/trailing hyphens.

    Args:
        term: The headword to slugify.

    Returns:
        A ``[a-z0-9-]+`` slug (possibly empty for all-symbol input).
    """
    return re.sub(r"[^a-z0-9]+", "-", term.strip().lower()).strip("-")


class GlossaryUnit(BaseModel):
    """One enumerated glossary entry: a term and its definition prose."""

    term: str = Field(description="The headword / vocabulary term")
    definition: str = Field(
        description="Full definition prose, including part-of-speech and senses"
    )
    char_count: int = 0


class DefinitionCardPlan(BaseModel):
    """How many cards of which kind to emit for one glossary unit.

    For GRE wordlists this is always one ``definition_main`` card. The shape
    mirrors :class:`swanki.models.problem_set.CardPlan` so future elaboration
    (encyclopedia long entries) can extend it without restructuring callers.
    """

    n_cards: int = Field(ge=1, le=5)
    include_main: bool = True

    @model_validator(mode="after")
    def check_n_cards_consistent(self) -> "DefinitionCardPlan":
        """Validate that n_cards matches the enabled card-kind flags."""
        expected = int(self.include_main)
        if self.n_cards != expected:
            raise ValueError(
                f"n_cards={self.n_cards} inconsistent with flags (expected {expected})"
            )
        return self


class GlossaryEnumerationResponse(BaseModel):
    """Output of glossary_enumeration_agent (LLM-assisted enumeration)."""

    units: list[GlossaryUnit]


class DefinitionCardBatchResponse(BaseModel):
    """Output of definition_card_gen_agent for one batch of terms.

    Lives in models/ (not pipeline/) so llm/agents.py can import the response
    type without cycling through pipeline/glossary.py.
    """

    cards: list[PlainCard]


_GLOSSARY_TAG_RE = re.compile(r"^([^.]+)\.glossary\.([a-z0-9-]+)$")


class GlossaryTag(BaseModel):
    """Strongly-typed parser/renderer for the per-term card tag.

    Mirrors :class:`swanki.models.problem_set.ProblemTag`: a strict regex
    round-trip so the coverage audit keys on a parsed term slug rather than
    fragile ``str.startswith`` logic. ``parse`` returns None for tags that are
    not glossary tags (or belong to another citation key) so callers can ignore
    them cleanly.
    """

    citation_key: str
    term_slug: str

    def render(self) -> str:
        """Render the canonical ``<citation_key>.glossary.<term_slug>`` tag."""
        return f"{self.citation_key}.glossary.{self.term_slug}"

    @classmethod
    def parse(cls, tag: str, citation_key: str) -> "GlossaryTag | None":
        """Parse a tag into a GlossaryTag, or None if it is not a glossary tag."""
        m = _GLOSSARY_TAG_RE.match(tag)
        if m is None or m.group(1) != citation_key:
            return None
        return cls(citation_key=citation_key, term_slug=m.group(2))
