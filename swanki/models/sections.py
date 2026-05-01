"""
swanki/models/sections.py
[[swanki.models.sections]]
https://github.com/Mjvolk3/Swanki/tree/main/swanki/models/sections.py
Test file: tests/test_sections_models.py

Pydantic models for section classification used by the section-aware routing
layer in Pipeline.process_full. PageLabel is the source of truth (one entry
per PDF page); ContentSection is a derived view (run-length-encoded same-kind
spans). ClassificationResult bundles both plus method/confidence and is
persisted to <output_dir>/section-classification.yaml for introspection.
"""

from typing import Literal

from pydantic import BaseModel, Field, model_validator

SectionKind = Literal[
    "main_content", "review_exercises", "front_matter", "back_matter"
]


class PageLabel(BaseModel):
    """Per-page classification record.

    Source of truth for routing decisions. Persisted to
    section-classification.yaml so the user can hand-edit and re-run with
    pipeline.solution_manual.classification_override pointing at the edit.
    """

    page_idx: int
    kind: SectionKind
    heading_anchor: str | None = Field(
        default=None,
        description="Most recent markdown heading driving this page's classification.",
    )
    overlap_density: float = Field(
        ge=0.0,
        le=1.0,
        default=0.0,
        description="Per-page problem-shape density in [0,1]. 1.0 for review_exercises; 0.0 for matter; computed for main_content.",
    )
    confidence: float = Field(ge=0.0, le=1.0, default=1.0)
    paired_answer_page: int | None = Field(
        default=None,
        description="When set, this page contains answers paired with the question section that owns the linked page.",
    )
    note: str | None = Field(
        default=None, description="Freeform diagnostic (e.g. 're-classified after pairing')."
    )


class ContentSection(BaseModel):
    """Run-length-encoded view of consecutive same-kind PageLabels.

    Built by sections_from_page_labels(); consumed by routing logic in
    Pipeline.process_full when iterating sections to dispatch to main_content
    card-gen vs problem-set card-gen.
    """

    kind: SectionKind
    start_page: int
    end_page: int
    heading: str | None = None
    overlap_density: float = Field(ge=0.0, le=1.0, default=0.0)
    paired_answer_section: int | None = None


class ClassificationResult(BaseModel):
    """Top-level classifier output."""

    page_labels: list[PageLabel]
    sections: list[ContentSection] = Field(default_factory=list)
    confidence: float = Field(ge=0.0, le=1.0)
    method: Literal["heading", "llm", "mixed"]

    @model_validator(mode="after")
    def derive_sections_if_empty(self) -> "ClassificationResult":
        """Build sections from page_labels if not provided."""
        if not self.sections and self.page_labels:
            self.sections = sections_from_page_labels(self.page_labels)
        return self


def sections_from_page_labels(
    page_labels: list[PageLabel],
) -> list[ContentSection]:
    """Run-length-encode page labels into ContentSection ranges.

    Consecutive pages with the same kind merge into one section. Section-level
    overlap_density is the mean of constituent page densities. The heading
    anchor of the first page becomes the section heading.

    Args:
        page_labels: Per-page classification records, in document order.

    Returns:
        Derived list of ContentSection covering all pages.
    """
    if not page_labels:
        return []
    sections: list[ContentSection] = []
    cur_kind = page_labels[0].kind
    cur_start = 0
    cur_heading = page_labels[0].heading_anchor
    for i in range(1, len(page_labels) + 1):
        boundary = i == len(page_labels) or page_labels[i].kind != cur_kind
        if boundary:
            span = page_labels[cur_start:i]
            density = sum(p.overlap_density for p in span) / len(span)
            sections.append(
                ContentSection(
                    kind=cur_kind,
                    start_page=cur_start,
                    end_page=i - 1,
                    heading=cur_heading,
                    overlap_density=density,
                )
            )
            if i < len(page_labels):
                cur_kind = page_labels[i].kind
                cur_start = i
                cur_heading = page_labels[i].heading_anchor
    return sections
