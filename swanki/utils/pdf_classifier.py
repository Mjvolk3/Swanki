"""
swanki/utils/pdf_classifier.py
[[swanki.utils.pdf_classifier]]
https://github.com/Mjvolk3/Swanki/tree/main/swanki/utils/pdf_classifier.py

LLM-based PDF page classifier for smart cutting.
"""

import warnings
from pathlib import Path

from pydantic import BaseModel
from PyPDF2 import PdfReader


class PageLabel(BaseModel):
    """Single page classification with label and keep/cut decision."""

    page: int  # 1-indexed
    label: str  # "content" | "references" | "acknowledgments" | "author_info" | "supplementary"
    keep: bool  # educational value?


class PDFCutPlan(BaseModel):
    """LLM-generated plan for which PDF pages to keep or cut."""

    pages: list[PageLabel]
    keep_ranges: list[tuple[int, int]]  # 0-indexed [start, end) ranges to KEEP


SYSTEM_PROMPT = """\
You are a PDF page classifier. Given the first few lines of each page of an \
academic paper, classify every page and decide which to keep for educational \
flashcard generation.

KEEP (educational value):
- Content, Abstract, Introduction, Methods, Results, Discussion
- Supplementary Figures/Data, Extended Data, STAR Methods
- Tables, Figures, Equations

CUT (no educational value):
- References, Bibliography, Literature Cited
- Acknowledgments
- Author Information, Author Contributions
- Competing/Conflicts of Interest, Financial Interests/Disclosures
- Data Availability statements, Code Availability
- Declaration of Interests

Labels: "content", "references", "acknowledgments", "author_info", "supplementary"
- Use "content" for main body + methods + results + discussion
- Use "supplementary" for supplementary/extended data sections
- Use "references" for references/bibliography
- Use "acknowledgments" for acknowledgments
- Use "author_info" for author contributions, conflicts, data availability, etc.

Set keep=true for "content" and "supplementary", keep=false for the rest.

For keep_ranges, merge adjacent keep-pages into contiguous 0-indexed [start, end) \
ranges. Only include ranges where keep=true. Isolated cut-pages between two keep \
sections should produce two separate ranges (do NOT bridge over cut pages)."""


def _extract_page_previews(pdf_path: Path, max_lines: int = 5) -> list[str]:
    """Extract the first N lines of text from each page."""
    warnings.filterwarnings("ignore")
    reader = PdfReader(str(pdf_path), strict=False)
    previews = []
    for page in reader.pages:
        text = page.extract_text() or ""
        lines = [line.strip() for line in text.split("\n") if line.strip()][:max_lines]
        previews.append("\n".join(lines))
    return previews


def classify_pdf(pdf_path: Path) -> PDFCutPlan:
    """Classify each page of a PDF and return a cut plan."""
    previews = _extract_page_previews(pdf_path)

    user_msg = "Classify each page of this PDF:\n\n"
    for i, preview in enumerate(previews):
        user_msg += f"--- Page {i + 1} ---\n{preview}\n\n"

    from pydantic_ai import Agent

    pdf_cut_agent: Agent[None, PDFCutPlan] = Agent(output_type=PDFCutPlan, retries=3)
    result = pdf_cut_agent.run_sync(
        user_msg,
        instructions=SYSTEM_PROMPT,
        model="openai:gpt-5-nano",
    )
    return result.output  # type: ignore[no-any-return]
