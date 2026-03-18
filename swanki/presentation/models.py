"""
swanki/presentation/models.py
[[swanki.presentation.models]]
https://github.com/Mjvolk3/swanki/tree/main/swanki/presentation/models.py
Test file: tests/swanki/presentation/test_models.py

Pydantic models for structured presentation generation from academic papers.
"""

from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field, field_validator


class FigureRef(BaseModel):
    """Reference to a figure extracted from the source PDF.

    Attributes:
        source_page: 1-based PDF page number containing the figure.
        crop_bbox: Normalized (x0, y0, x1, y1) crop box for sub-figure
            extraction. Values in [0, 1]. None for full page.
        caption: Caption text to display under the figure.
        label: Short label for referencing, e.g. "fig1", "figs2".
    """

    source_page: int = Field(description="1-based PDF page number")
    crop_bbox: list[float] | None = Field(
        None,
        description="Normalized [x0, y0, x1, y1] crop box (4 floats in 0-1), None for full page",
    )
    caption: str = Field(description="Figure caption")
    label: str = Field(description="Short label like 'fig1' or 'figs2'")


class MermaidDiagram(BaseModel):
    """A mermaid diagram to render in a slide.

    Attributes:
        code: Mermaid diagram source code.
        caption: Caption for the diagram.
    """

    code: str = Field(description="Mermaid diagram source code")
    caption: str = Field(description="Diagram caption")


class Slide(BaseModel):
    """A single presentation slide.

    Attributes:
        title: Slide title (max 80 chars).
        content: Markdown body content.
        speaker_notes: Speaker notes (reveal.js only).
        figures: Figures to include on this slide.
        mermaid_diagrams: Mermaid diagrams to render.
        layout: Slide layout type.
    """

    title: str = Field(max_length=80, description="Slide title")
    content: str = Field(description="Markdown body content")
    speaker_notes: str = Field(default="", description="Speaker notes")
    figures: list[FigureRef] = Field(
        default_factory=list, description="Figures to include"
    )
    mermaid_diagrams: list[MermaidDiagram] = Field(
        default_factory=list, description="Mermaid diagrams to render"
    )
    layout: Literal[
        "title", "content", "two-column", "figure-full", "section-break"
    ] = Field(default="content", description="Slide layout type")


class PresentationSpec(BaseModel):
    """User specification for presentation generation.

    Attributes:
        citation_key: Zotero citation key identifying the paper.
        instructions: Free-text user instructions for the LLM.
        slide_count_min: Minimum number of slides.
        slide_count_max: Maximum number of slides.
        include_all_main_figures: Whether to include all main-text figures.
        custom_images: Paths to additional images to include.
    """

    citation_key: str = Field(description="Zotero citation key")
    instructions: str = Field(default="", description="Free-text instructions")
    slide_count_min: int = Field(default=10, description="Minimum slide count")
    slide_count_max: int = Field(default=14, description="Maximum slide count")
    include_all_main_figures: bool = Field(
        default=True, description="Include all main-text figures"
    )
    custom_images: list[Path] = Field(
        default_factory=list, description="Paths to custom images"
    )


class Presentation(BaseModel):
    """Complete structured presentation output from the LLM.

    Attributes:
        title: Presentation title.
        subtitle: Optional subtitle.
        authors: List of author names.
        date: Presentation date string.
        slides: Ordered list of slides.
    """

    title: str = Field(description="Presentation title")
    subtitle: str = Field(default="", description="Optional subtitle")
    authors: list[str] = Field(description="Author names")
    date: str = Field(default="", description="Date string")
    slides: list[Slide] = Field(description="Ordered list of slides")

    @field_validator("slides")
    @classmethod
    def validate_slide_count(cls, v: list[Slide]) -> list[Slide]:
        """Validate at least one slide exists."""
        if len(v) == 0:
            raise ValueError("Presentation must have at least one slide")
        return v
