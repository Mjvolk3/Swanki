"""
swanki/presentation/slide_generator.py
[[swanki.presentation.slide_generator]]
https://github.com/Mjvolk3/swanki/tree/main/swanki/presentation/slide_generator.py
Test file: tests/swanki/presentation/test_slide_generator.py

LLM-driven slide content generation using instructor for structured output.
"""

import instructor
from openai import OpenAI

from swanki.presentation.models import Presentation, PresentationSpec

SYSTEM_PROMPT = """\
You are an expert academic presenter creating a Reveal.js slide presentation \
from a research paper. Your output must be a structured Presentation object.

Guidelines:
- Create clear, concise slides suitable for an academic audience.
- Each slide should have a focused title (max 80 chars) and markdown content.
- Use LaTeX math notation ($...$ for inline, $$...$$ for display) where appropriate.
- Reference figures by their label in the figures list. The renderer will embed them.
- Keep bullet points concise -- no more than 4-5 per slide.
- Speaker notes should add context beyond what's on the slide.
- For figure-heavy slides, keep text minimal to avoid clutter.
- The first slide should use layout "title".
- Use layout "figure-full" for slides where a figure is the main content.
- Use layout "content" for text-heavy slides.
- You may create mermaid diagrams for concepts that benefit from visual explanation.
- Do not include figures that are not in the available figures list.
"""

USER_PROMPT_TEMPLATE = """\
Create a presentation for the following paper.

## User Instructions
{instructions}

## Slide Count
Between {slide_count_min} and {slide_count_max} slides.

## Document Summary
{doc_summary}

## Available Figures (by page number)
{image_summaries}

Create the presentation now. Include all figures listed above unless the user \
instructions say otherwise. Place each figure on the slide where its content \
is most relevant.
"""


class SlideGenerator:
    """Generate structured presentation content via LLM.

    Args:
        model: OpenAI model name to use.
    """

    def __init__(self, model: str = "gpt-4o") -> None:
        """Initialize with LLM model name."""
        self.model = model
        self.client = instructor.patch(OpenAI())

    def generate(
        self,
        spec: PresentationSpec,
        doc_summary_text: str,
        image_summaries: dict[str, str],
    ) -> Presentation:
        """Generate a structured presentation from paper data.

        Args:
            spec: User specification with instructions and constraints.
            doc_summary_text: Full document summary markdown text.
            image_summaries: Mapping of "page-N" to image description text.

        Returns:
            Structured Presentation with slides, figures, and diagrams.
        """
        image_summary_lines = []
        for key, desc in sorted(image_summaries.items()):
            page_num = key.split("-")[1].split("_")[0] if "-" in key else key
            image_summary_lines.append(f"- Page {page_num}: {desc[:500]}")
        image_summary_text = "\n".join(image_summary_lines)

        user_prompt = USER_PROMPT_TEMPLATE.format(
            instructions=spec.instructions or "Academic lit review style.",
            slide_count_min=spec.slide_count_min,
            slide_count_max=spec.slide_count_max,
            doc_summary=doc_summary_text,
            image_summaries=image_summary_text,
        )

        response: Presentation = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            response_model=Presentation,
            max_retries=3,
        )
        return response
