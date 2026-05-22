"""
swanki/models/problem_set.py
[[swanki.models.problem_set]]
https://github.com/Mjvolk3/Swanki/tree/main/swanki/models/problem_set.py
Test file: tests/test_problem_set_models.py

Pydantic models for solution-manual mode: problem units, card plans, provenance,
problem-solution pairing, the ProblemTag parser/renderer, and pydantic-ai
response wrappers (ProblemEnumerationResponse, CardPlanResponse,
ProblemCardBatchResponse, ProblemPairingResponse). Response types live here
(not pipeline/problem_set.py) to avoid a circular import with llm/agents.py.
"""

import re
from typing import Literal

from pydantic import BaseModel, Field, model_validator

from .cards import PlainCard

ProblemSubtype = Literal[
    "theory_problem", "multiple_choice", "matching", "true_false", "completion"
]
CardSubtype = Literal[
    "regular",
    "cloze",
    "image",
    "problem_main",
    "subproblem",
    "problem_overview",
    "full_solution",
    "definition_main",
    "definition_example",
    "definition_elaboration",
]


class ProblemPart(BaseModel):
    """One labeled sub-part of a multi-part problem (e.g. (a)/(b)/(c))."""

    label: str = Field(description="Part label like 'a', 'b', 'i'")
    statement: str
    solution: str | None = None


class ProblemUnit(BaseModel):
    """One numbered problem with its statement, optional solution, and parts."""

    problem_id: str = Field(description="Canonical book ID like '1.7' or 'MC-1'")
    subtype: ProblemSubtype
    chapter: str | None = None
    statement: str
    solution: str | None = None
    parts: list[ProblemPart] = Field(default_factory=list)
    referenced_figures: list[str] = Field(default_factory=list)
    referenced_equations: list[str] = Field(default_factory=list)
    page_span: tuple[int, int] | None = None
    char_count: int = 0


class CardPlan(BaseModel):
    """How many cards of which subtypes to emit for one problem."""

    n_cards: int = Field(ge=1, le=5)
    include_main: bool = True
    subproblem_labels: list[str] = Field(default_factory=list, max_length=3)
    include_overview: bool = False
    include_full_solution: bool = False

    @model_validator(mode="after")
    def check_n_cards_consistent(self) -> "CardPlan":
        expected = (
            int(self.include_main)
            + len(self.subproblem_labels)
            + int(self.include_overview)
            + int(self.include_full_solution)
        )
        if self.n_cards != expected:
            raise ValueError(
                f"n_cards={self.n_cards} inconsistent with flags (expected {expected})"
            )
        return self


class ProvenanceSpan(BaseModel):
    """One span in a full-solution card, marked as copy or LLM-generated."""

    text: str
    origin: Literal["copy", "generated"]
    source_ref: str | None = None


class ProblemProvenance(BaseModel):
    """Provenance for one problem's full_solution card."""

    problem_id: str
    spans: list[ProvenanceSpan]


class ProvenanceLog(BaseModel):
    """Top-level YAML artifact wrapping all problem provenance entries."""

    chapter_id: str | None = None
    entries: list[ProblemProvenance] = Field(default_factory=list)


class ProblemLocation(BaseModel):
    """Where a problem statement or solution lives in the document."""

    problem_id: str
    role: Literal["statement", "solution"]
    page_idx: int
    start_char: int = 0
    end_char: int = 0
    text: str


class ProblemPairing(BaseModel):
    """One problem with its statement and zero-or-more solution locations."""

    problem_id: str
    statement: ProblemLocation
    solutions: list[ProblemLocation] = Field(default_factory=list)


class PairingResult(BaseModel):
    """Top-level pairing artifact, persisted to <output_dir>/problem-pairings.yaml."""

    pairings: list[ProblemPairing]
    unpaired_solutions: list[ProblemLocation] = Field(default_factory=list)
    method: Literal["regex", "llm", "mixed"]
    confidence: float = Field(ge=0.0, le=1.0)


class ProblemEnumerationResponse(BaseModel):
    """Output of problem_enumeration_agent (LLM-fallback enumeration)."""

    problems: list[ProblemUnit]


class CardPlanResponse(BaseModel):
    """Output of card_plan_classifier_agent."""

    plan: CardPlan


class ProblemCardBatchResponse(BaseModel):
    """Output of problem_card_gen_agent for one problem's cards.

    Lives in models/ (not pipeline/) so llm/agents.py can import the response
    type without cycling through pipeline/problem_set.py. Phase 1 emits only
    PlainCard subtypes; FullSolutionCard support lands when LongFormCardContent
    is added.
    """

    cards: list[PlainCard]
    provenance_entries: list[ProblemProvenance] = Field(default_factory=list)


class ProblemPairingResponse(BaseModel):
    """Output of the Stage-3 LLM fallback in pair_problems_across_pages.

    The agent receives unpaired problems and unparsed review-exercises text;
    returns one ProblemLocation per match it finds. Omits problems it can't
    match (does NOT fabricate solutions).
    """

    solutions: list[ProblemLocation]


_PROBLEM_TAG_RE = re.compile(
    r"^([^.]+)\.problem\.([0-9]+\.[0-9]+|[A-Z]+(?:-CH\d+)?-\d+)$"
)


class ProblemTag(BaseModel):
    """Strongly-typed parser/renderer for the per-problem card tag.

    Replaces fragile str.startswith / str.removeprefix audit logic with a
    strict regex round-trip. ``parse`` returns None for malformed tags so
    downstream code can ignore non-problem tags cleanly.
    """

    citation_key: str
    problem_id: str

    def render(self) -> str:
        return f"{self.citation_key}.problem.{self.problem_id}"

    @classmethod
    def parse(cls, tag: str, citation_key: str) -> "ProblemTag | None":
        m = _PROBLEM_TAG_RE.match(tag)
        if m is None or m.group(1) != citation_key:
            return None
        return cls(citation_key=citation_key, problem_id=m.group(2))
