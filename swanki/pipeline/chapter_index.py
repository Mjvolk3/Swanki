"""
swanki/pipeline/chapter_index.py
[[swanki.pipeline.chapter_index]]
https://github.com/Mjvolk3/Swanki/tree/main/swanki/pipeline/chapter_index.py
Test file: tests/test_chapter_index.py

Build, persist, and load chapter-index.yaml: a structured artifact of numbered
equations, figures, and theorems extracted from a chapter's cleaned markdown.
Used by solution-manual mode to inline cross-chapter references onto cards.
"""

import re
from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, Field

# Equations: $$...$$ block with optional trailing (N.M) tag, OR \tag{N.M} inside.
_EQUATION_BLOCK = re.compile(r"\$\$([^$]+?)\$\$\s*(?:\(([0-9]+\.[0-9]+)\))?", re.DOTALL)
_EQUATION_INLINE_TAG = re.compile(r"\\tag\{([0-9]+\.[0-9]+)\}")
# Theorems: capture statement up to the next blank line or end-of-file.
_THEOREM = re.compile(
    r"^(Theorem|Lemma|Proposition|Definition|Corollary)\s+([0-9.]+)[\s.:]+(.+?)(?=\n\n|\Z)",
    re.MULTILINE | re.DOTALL,
)
# Figures: ![alt](url) immediately followed by "Fig N.M:" or "Figure N.M:" caption.
_FIGURE_BLOCK = re.compile(
    r"!\[([^\]]*)\]\(([^)]+)\)\s*\n+\s*(?:Fig\.|Figure)\s+([0-9]+\.[0-9]+)\s*[:|]\s*([^\n]+)",
    re.MULTILINE,
)


class NumberedEquation(BaseModel):
    """A numbered equation extracted from chapter markdown."""

    id: str
    latex: str
    page_idx: int
    display: bool = True


class NumberedFigure(BaseModel):
    """A numbered figure with caption + image path extracted from chapter markdown."""

    id: str
    caption: str
    image_path: str
    page_idx: int


class NumberedTheorem(BaseModel):
    """A numbered theorem-style statement (theorem/lemma/etc.)."""

    id: str
    kind: Literal["theorem", "lemma", "proposition", "definition", "corollary"]
    statement: str
    page_idx: int


class ChapterIndex(BaseModel):
    """All numbered items in one chapter, used for cross-reference resolution."""

    chapter_id: str
    equations: list[NumberedEquation] = Field(default_factory=list)
    figures: list[NumberedFigure] = Field(default_factory=list)
    theorems: list[NumberedTheorem] = Field(default_factory=list)


def build_chapter_index(
    clean_md_files: list[Path], chapter_id: str
) -> ChapterIndex:
    """Extract numbered equations, figures, and theorems from cleaned markdown.

    Args:
        clean_md_files: Per-page cleaned markdown (output of MarkdownCleaner).
        chapter_id: Identifier like 'bishop2024_CH01'.

    Returns:
        Populated ChapterIndex.
    """
    equations: list[NumberedEquation] = []
    figures: list[NumberedFigure] = []
    theorems: list[NumberedTheorem] = []

    for page_idx, md_file in enumerate(clean_md_files):
        text = md_file.read_text()

        for m in _EQUATION_BLOCK.finditer(text):
            latex = m.group(1).strip()
            eq_id = m.group(2)
            if eq_id is None:
                tag_match = _EQUATION_INLINE_TAG.search(latex)
                if tag_match:
                    eq_id = tag_match.group(1)
            if eq_id:
                equations.append(
                    NumberedEquation(id=eq_id, latex=latex, page_idx=page_idx)
                )

        for m in _THEOREM.finditer(text):
            kind_str = m.group(1).lower()
            theorems.append(
                NumberedTheorem(
                    id=m.group(2),
                    kind=kind_str,  # type: ignore[arg-type]
                    statement=m.group(3).strip(),
                    page_idx=page_idx,
                )
            )

        for m in _FIGURE_BLOCK.finditer(text):
            figures.append(
                NumberedFigure(
                    id=m.group(3),
                    caption=m.group(4).strip(),
                    image_path=m.group(2),
                    page_idx=page_idx,
                )
            )

    return ChapterIndex(
        chapter_id=chapter_id,
        equations=equations,
        figures=figures,
        theorems=theorems,
    )


def write_chapter_index(index: ChapterIndex, output_path: Path) -> None:
    """Persist chapter index as YAML."""
    output_path.write_text(
        yaml.safe_dump(index.model_dump(), sort_keys=False)
    )


def load_chapter_index(yaml_path: Path) -> ChapterIndex:
    """Load chapter index from YAML."""
    return ChapterIndex.model_validate(yaml.safe_load(yaml_path.read_text()))
