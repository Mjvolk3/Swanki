"""Main processing pipeline for Swanki.

This module contains the Pipeline class which orchestrates the entire
workflow of converting PDFs to Anki flashcards. It coordinates all
processing steps including PDF conversion, markdown cleaning, image
processing, card generation, audio creation, and Anki integration.

The pipeline is configuration-driven using Hydra configs and supports
various processing options and output formats.

Classes
-------
Pipeline
    Main orchestrator for PDF to Anki card conversion

Examples
--------
>>> from swanki import Pipeline, ConfigGenerator
>>> from pathlib import Path
>>>
>>> # Generate configuration
>>> config_gen = ConfigGenerator()
>>> config = config_gen.generate(
...     pdf_path="paper.pdf",
...     output_dir="output",
...     deck_name="MyDeck"
... )
>>>
>>> # Create and run pipeline
>>> pipeline = Pipeline(config)
>>> outputs = pipeline.process_full(
...     pdf_path=Path("paper.pdf"),
...     citation_key="Smith2023"
... )
"""

from pathlib import Path
from typing import Dict, Any, List, Optional
from omegaconf import DictConfig
import instructor
from openai import OpenAI
import os
import random
import subprocess
import logging
import re
from dotenv import load_dotenv
from tenacity import Retrying, stop_after_attempt, wait_exponential, retry_if_exception_type
from pydantic import ValidationError

logger = logging.getLogger(__name__)

from ..models import (
    DocumentSummary,
    CardGenerationResponse,
    ImageSummary,
    ProcessingState,
    PlainCard,
    CardFeedback,
    AudioTranscriptFeedback,
    RefinementHistory,
    EnhancedCardGenerationResponse,
)

# Import new processing modules
from ..processing import (
    PDFProcessor,
    MarkdownConverter,
    MarkdownCleaner,
    ImageProcessor,
    AnkiProcessor,
)

# Import audio utilities
from ..utils.audio import (
    generate_card_audio,
    generate_summary_audio,
    generate_reading_audio,
    generate_lecture_audio,
)

# Import content utilities
from ..utils.content import (
    extract_images_from_markdown,
    detect_math_content,
    generate_image_card_prompts,
)


class Pipeline:
    """Main processing pipeline with configuration-driven workflow.

    Orchestrates the complete PDF to Anki card conversion process,
    managing all intermediate steps and outputs. Supports various
    configuration options for customizing the processing behavior.

    Parameters
    ----------
    config : Dict[str, Any]
        Hydra configuration dictionary containing all processing options

    Attributes
    ----------
    config : Dict[str, Any]
        Configuration dictionary
    instructor : instructor.Instructor
        Patched OpenAI client for structured outputs
    state : ProcessingState or None
        Current processing state tracker
    data_dir : Path
        Base directory for output data
    output_base : Path
        Current output directory for this run
    citation_key : str
        Citation key for the current document

    Methods
    -------
    process_full(pdf_path, citation_key)
        Run the complete processing pipeline
    split_pdf(pdf_path)
        Split PDF into individual pages
    convert_to_markdown(pages)
        Convert PDF pages to markdown
    clean_markdown(markdown_files)
        Clean and format markdown files
    process_images(markdown_files)
        Extract and summarize images
    generate_document_summary(markdown_files, image_summaries)
        Generate comprehensive document summary
    generate_cards_with_window(markdown_files, doc_summary, window_size, skip, num_cards)
        Generate cards using sliding window
    generate_image_cards(markdown_files, doc_summary, ...)
        Generate cards from images
    generate_outputs(cards, summary, output_dir)
        Generate output files in various formats
    generate_audio(cards, summary, outputs, cleaned_files, image_summaries)
        Generate audio files for cards and content
    send_to_anki(cards, outputs, anki_config)
        Send cards to Anki via AnkiConnect

    Examples
    --------
    >>> config = {
    ...     'pipeline': {'processing': {'window_size': 2}},
    ...     'audio': {'audio': {'generate_complementary': True}},
    ...     'anki': {'anki': {'enabled': True, 'auto_send': True}}
    ... }
    >>> pipeline = Pipeline(config)
    >>> outputs = pipeline.process_full(
    ...     pdf_path=Path("research_paper.pdf"),
    ...     citation_key="Johnson2024"
    ... )
    """

    def __init__(self, config: Dict[str, Any]):
        """Initialize the pipeline with configuration.

        Parameters
        ----------
        config : Dict[str, Any]
            Hydra configuration dictionary with processing options

        Notes
        -----
        Loads environment variables including SWANKI_DATA for output directory.
        Initializes OpenAI client with instructor for structured outputs.
        """
        self.config = config
        self.instructor = instructor.patch(OpenAI())
        self.state = None

        # Load environment variables
        load_dotenv()
        self.data_dir = Path(os.getenv("SWANKI_DATA", "swanki-out"))

    def process_full(
        self, pdf_path: Path, citation_key: str, output_dir: str = None
    ) -> Dict[str, Path]:
        """Process PDF through the complete pipeline.

        Executes all processing steps from PDF to final outputs, including
        splitting, conversion, cleaning, card generation, audio creation,
        and optional Anki integration.

        Parameters
        ----------
        pdf_path : Path
            Path to the input PDF file
        citation_key : str
            Citation key for naming outputs and referencing
        output_dir : str, optional
            Name for the output directory. If not provided, uses citation_key

        Returns
        -------
        Dict[str, Path]
            Dictionary mapping output types to file paths:
            - 'cards_plain': Plain markdown cards
            - 'cards_audio': Cards with audio links (if enabled)
            - 'summary': Document summary

        Raises
        ------
        RuntimeError
            If PDF conversion fails or no markdown content generated

        Examples
        --------
        >>> pipeline = Pipeline(config)
        >>> outputs = pipeline.process_full(
        ...     pdf_path=Path("/docs/paper.pdf"),
        ...     citation_key="Einstein1905"
        ... )
        >>> print(outputs['cards_plain'])
        PosixPath('swanki-out/Einstein1905/cards-plain.md')
        """

        # Initialize state
        self.state = ProcessingState(
            pdf_path=pdf_path, citation_key=citation_key, current_stage="initialization"
        )

        # Create output directory based on output_dir or citation key with auto-increment if exists
        base_name = (
            output_dir
            if output_dir
            else (citation_key if citation_key else "swanki-out")
        )
        output_path = self.data_dir / base_name

        # Store base_name for audio file naming
        self.audio_prefix = base_name

        # If directory exists, append a number
        if output_path.exists():
            counter = 0
            while True:
                numbered_dir = self.data_dir / f"{base_name}_{counter}"
                if not numbered_dir.exists():
                    output_path = numbered_dir
                    break
                counter += 1

        self.output_base = output_path
        self.output_base.mkdir(parents=True, exist_ok=True)

        # 1. Split PDF based on config
        self.state.current_stage = "pdf_split"
        pages = self.split_pdf(pdf_path)

        # 2. Convert to markdown
        self.state.current_stage = "markdown_conversion"
        markdown_files = self.convert_to_markdown(pages)

        # Check if conversion was successful - fail fast if not
        if not markdown_files:
            raise RuntimeError(
                "PDF to markdown conversion failed. Cannot proceed without markdown content."
            )

        # 3. Clean markdown
        self.state.current_stage = "markdown_cleaning"
        cleaned_files = self.clean_markdown(markdown_files)

        # 4. Process images
        self.state.current_stage = "image_processing"
        image_summaries = self.process_images(cleaned_files)

        # 5. Generate document summary (EARLY!)
        self.state.current_stage = "summary_generation"
        doc_summary = self.generate_document_summary(cleaned_files, image_summaries)
        self.state.document_summary = doc_summary

        # 6. Generate cards with sliding window
        self.state.current_stage = "card_generation"
        pipeline_config = self.config.get("pipeline", {})
        processing_config = pipeline_config.get("processing", {})
        all_cards = self.generate_cards_with_window(
            cleaned_files,
            doc_summary,
            window_size=processing_config.get("window_size", 2),
            skip=processing_config.get("skip", 1),
            num_cards=processing_config.get("num_cards_per_page", 3),
        )

        # 6.5. Generate image cards if enabled
        image_config = processing_config.get("image_cards", {})
        if image_config.get("enabled", True):
            self.state.current_stage = "image_card_generation"
            image_cards = self.generate_image_cards(
                cleaned_files,
                doc_summary,
                cards_per_image=image_config.get("cards_per_image", 3),
                image_on_front=image_config.get("image_on_front", True),
                image_on_back=image_config.get("image_on_back", True),
                require_math=image_config.get("require_math_content", False),
                placement_strategy=image_config.get("placement_strategy", "smart"),
                front_back_ratio=image_config.get("front_back_ratio", 0.5),
                image_summaries=image_summaries,
            )
            all_cards.extend(image_cards)

        # 7. Store citation key for later use
        self.citation_key = citation_key

        self.state.cards_generated = len(all_cards)

        # 8. Generate outputs based on config
        self.state.current_stage = "output_generation"
        outputs = self.generate_outputs(all_cards, doc_summary, self.output_base)

        # 9. Generate audio if configured
        audio_config = self.config.get("audio", {}).get("audio", {})
        if any(
            [
                audio_config.get("generate_complementary", False),
                audio_config.get("generate_summary", False),
                audio_config.get("generate_reading", False),
                audio_config.get("generate_lecture", False),
            ]
        ):
            self.state.current_stage = "audio_generation"
            self.generate_audio(
                all_cards, doc_summary, outputs, cleaned_files, image_summaries
            )

        # 10. Send to Anki if configured
        anki_config = self.config.get("anki", {}).get("anki", {})
        if anki_config.get("enabled", False) and anki_config.get("auto_send", False):
            self.state.current_stage = "anki_sending"
            self.send_to_anki(all_cards, outputs, anki_config)

        self.state.outputs = outputs
        return outputs

    def split_pdf(self, pdf_path: Path) -> List[Path]:
        """Split PDF into individual pages.

        Uses PDFProcessor to split a multi-page PDF into separate
        single-page PDF files for easier processing.

        Parameters
        ----------
        pdf_path : Path
            Path to the input PDF file

        Returns
        -------
        List[Path]
            List of paths to individual page PDFs

        See Also
        --------
        PDFProcessor : Handles PDF splitting operations
        """
        pdf_processor = PDFProcessor(self.output_base)
        pdf_files = pdf_processor.split_pdf(pdf_path)
        return pdf_files

    def convert_to_markdown(self, pages: List[Path]) -> List[Path]:
        """Convert PDF pages to markdown format.

        Converts individual PDF pages to markdown using the Mathpix
        service. Handles conversion errors gracefully and logs progress.

        Parameters
        ----------
        pages : List[Path]
            List of single-page PDF files to convert

        Returns
        -------
        List[Path]
            List of paths to generated markdown files

        Raises
        ------
        RuntimeError
            If no pages could be converted successfully

        Notes
        -----
        Uses os.system for better TTY handling with the mpx command.
        Creates output in 'md-singles' subdirectory.
        """

        # Create output directory
        md_singles_dir = self.output_base / "md-singles"
        md_singles_dir.mkdir(parents=True, exist_ok=True)

        markdown_files = []

        logger.info(f"Converting {len(pages)} PDF pages to markdown")

        # Convert each page individually (like the legacy approach)
        for page_pdf in pages:
            # Create corresponding markdown filename
            md_filename = page_pdf.stem + ".md"  # page-1.pdf -> page-1.md
            md_path = md_singles_dir / md_filename

            # Use os.system approach which handles clearLine errors better
            cmd = f"mpx convert '{page_pdf}' '{md_path}'"

            logger.debug(f"Converting {page_pdf.name} to {md_path.name}")

            try:
                # Use os.system - it handles TTY issues better than subprocess
                exit_code = os.system(cmd)

                if exit_code == 0 and md_path.exists() and md_path.stat().st_size > 0:
                    logger.debug(f"Successfully converted {page_pdf.name}")
                    markdown_files.append(md_path)
                else:
                    logger.warning(
                        f"Failed to convert {page_pdf.name} - exit code: {exit_code}"
                    )

            except Exception as e:
                logger.error(f"Error converting {page_pdf.name}: {e}")

        if not markdown_files:
            raise RuntimeError("Failed to convert any PDF pages to markdown.")

        logger.info(f"Successfully converted {len(markdown_files)} pages to markdown")
        return sorted(markdown_files)

    def clean_markdown(self, markdown_files: List[Path]) -> List[Path]:
        """Clean and standardize markdown files.

        Applies various cleaning operations to markdown files including
        removing artifacts, fixing formatting, and standardizing structure.

        Parameters
        ----------
        markdown_files : List[Path]
            List of markdown files to clean

        Returns
        -------
        List[Path]
            List of paths to cleaned markdown files

        See Also
        --------
        MarkdownCleaner : Handles markdown cleaning operations
        """
        cleaner = MarkdownCleaner(self.output_base)
        cleaned_files = cleaner.clean_all_markdown_files()
        return cleaned_files

    def process_images(self, markdown_files: List[Path]) -> List[ImageSummary]:
        """Extract and summarize images from markdown.

        Processes all images found in markdown files, generating
        AI-powered summaries and extracting relevant metadata.

        Parameters
        ----------
        markdown_files : List[Path]
            List of markdown files to process

        Returns
        -------
        List[ImageSummary]
            List of image summaries with metadata

        See Also
        --------
        ImageProcessor : Handles image extraction and summarization
        ImageSummary : Data model for image information
        """
        # Initialize processor with OpenAI client if available
        processor = ImageProcessor(self.output_base, self.instructor)

        # Process all images
        image_infos = processor.process_all_images()

        # Convert to ImageSummary objects
        image_summaries = []
        for idx, info in enumerate(image_infos):
            if "summary" in info:
                image_summary = ImageSummary(
                    image_url=info["url"],
                    summary=info["summary"],
                    alt_text=info.get("alt_text", ""),
                    page_idx=idx,
                    context=info.get("context", ""),
                )
                image_summaries.append(image_summary)

        return image_summaries

    def generate_document_summary(
        self, markdown_files: List[Path], image_summaries: List[ImageSummary]
    ) -> DocumentSummary:
        """Generate comprehensive document summary.

        Creates a structured summary of the entire document including
        title, authors, key contributions, methodology, and definitions
        of acronyms and technical terms.

        Parameters
        ----------
        markdown_files : List[Path]
            List of cleaned markdown files
        image_summaries : List[ImageSummary]
            List of image summaries to include

        Returns
        -------
        DocumentSummary
            Structured document summary with metadata

        Notes
        -----
        Uses configured prompts and LLM model for generation.
        Summary must be 200-500 words as validated by DocumentSummary.

        See Also
        --------
        DocumentSummary : Data model for document summaries
        """
        # Combine all markdown content
        combined_content = "\\n\\n".join([f.read_text() for f in markdown_files])

        # Format image summaries
        image_summary_text = "\\n".join(
            [f"Image {img.page_idx}: {img.summary}" for img in image_summaries]
        )

        # Get prompts from config (note the nested structure)
        prompts_config = self.config.get("prompts", {}).get("prompts", {})
        summary_prompts = prompts_config.get("summary", {})
        system_prompt = summary_prompts.get(
            "system",
            "You are an expert at creating concise, informative summaries of academic documents.",
        )
        user_prompt = summary_prompts.get(
            "document_summary",
            """Create a comprehensive summary of this document.
Focus on:
1. Main thesis and key contributions
2. All acronyms and their full forms
3. Technical terms that need clear definitions
4. Methodology and approach
5. Key findings

Document content:
{content}

Image summaries:
{image_summaries}""",
        )

        # Generate summary using instructor
        models_config = self.config.get("models", {}).get("models", {})
        llm_config = models_config.get("llm", {})
        response = self.instructor.chat.completions.create(
            model=llm_config.get("model", "gpt-4"),
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": user_prompt.format(
                        content=combined_content, image_summaries=image_summary_text
                    ),
                },
            ],
            response_model=DocumentSummary,
            max_retries=llm_config.get("max_retries", 3),
        )

        return response

    def generate_cards_with_window(
        self,
        markdown_files: List[Path],
        doc_summary: DocumentSummary,
        window_size: int,
        skip: int,
        num_cards: int,
    ) -> List[PlainCard]:
        """Generate flashcards using sliding window approach.

        Processes markdown files in overlapping windows to generate
        cards with better context. This helps create more coherent
        cards that can reference content across page boundaries.

        Parameters
        ----------
        markdown_files : List[Path]
            List of markdown files to process
        doc_summary : DocumentSummary
            Document summary for context
        window_size : int
            Number of files to process together
        skip : int
            Number of files to skip between windows
        num_cards : int
            Number of cards to generate per page

        Returns
        -------
        List[PlainCard]
            Generated flashcards

        Examples
        --------
        >>> # Process files in groups of 2, moving 1 file at a time
        >>> cards = pipeline.generate_cards_with_window(
        ...     markdown_files=files,
        ...     doc_summary=summary,
        ...     window_size=2,
        ...     skip=1,
        ...     num_cards=3
        ... )

        Notes
        -----
        The sliding window approach ensures cards can reference
        content that spans multiple pages, improving coherence.
        """
        all_cards = []
        
        # Handle case where window_size is larger than available files
        if window_size > len(markdown_files):
            logger.warning(f"Window size ({window_size}) is larger than number of files ({len(markdown_files)}). Using all available files.")
            window_size = len(markdown_files)
        
        # Ensure we generate at least one window
        num_windows = max(1, (len(markdown_files) - window_size) // skip + 1)
        
        for i in range(0, len(markdown_files) - window_size + 1, skip):
            window_files = markdown_files[i : i + window_size]

            # Combine content from window
            combined_content = "\\n\\n".join([f.read_text() for f in window_files])

            # Get config values
            prompts_config = self.config.get("prompts", {}).get("prompts", {})
            cards_prompts = prompts_config.get("cards", {})
            models_config = self.config.get("models", {}).get("models", {})
            llm_config = models_config.get("llm", {})
            processing_config = self.config.get("pipeline", {}).get("processing", {})

            # Generate cards for this window
            # Debug: Log the actual prompt being sent
            actual_prompt = cards_prompts.get(
                "generate_cards",
                "Create {num_cards} flashcards from this content.",
            ).replace('{num_cards}', str(num_cards * len(window_files))
            ).replace('{num_cloze}', str(processing_config.get("cloze_cards_per_page", 2) * len(window_files))
            ).replace('{title}', doc_summary.title
            ).replace('{acronyms}', str(doc_summary.acronyms)
            ).replace('{technical_terms}', str(doc_summary.technical_terms)
            ).replace('{content}', combined_content)
            
            # Debug logging removed for cleaner output
            logger.debug(f"Requesting {num_cards * len(window_files)} regular cards and {processing_config.get('cloze_cards_per_page', 2) * len(window_files)} cloze cards")
            
            # Generate regular cards first
            regular_prompt = f"""Generate EXACTLY {num_cards * len(window_files)} regular Q&A flashcards from this content.

Context from document summary:
Title: {doc_summary.title}
Acronyms: {doc_summary.acronyms}
Technical terms: {doc_summary.technical_terms}

Content:
{combined_content}

FORMAT RULES:
1. Use ## for the question (front of card)
2. Answer goes on the next line (back of card)
3. Tags go as a single bullet: - #tag1, #tag2, #tag3
4. NO CLOZE CARDS - only regular Q&A format
5. NEVER use generic tags like #equation, #definition - use conceptual tags like #causal-inference.dag

CRITICAL REQUIREMENTS:
1. Cards MUST be self-contained - students won't have access to the paper, figures, or other references
2. NEVER reference external content: "According to [12]", "As shown in Figure 3", "The paper states"
3. NEVER say "in the context of the document" or "as described in the document"
4. NEVER ask about specific authors: "What is Lachapelle et al.'s method?" - ask about the METHOD itself
5. NEVER ask "What does X stand for?" - ask what X IS or HOW it works instead
6. Each card tests ONE concept and includes all context needed to understand it
7. PRIORITIZE creating cards for EVERY mathematical equation, formula, or algorithm in the content
8. Use LaTeX with $ for inline math, $$ for display math
9. NEVER use LaTeX tables (\\\\begin{{tabular}})
10. For EVERY math symbol (h, F, g_j, etc.), define what it represents IN THE CARD

EQUATION PRIORITY:
- Create AT LEAST one card for EVERY equation in the content
- For key equations (like $X = (I - W^T)$, $E[X_j | X_{{pa(j)}}] = g_j(f_j(X))$), create multiple cards:
  * One asking what the equation represents
  * One asking about specific components/terms
  * One about its significance or application
- Even simple equations deserve cards (e.g., "What does $h(W) = 0$ represent in DAG optimization?")

Generate {num_cards * len(window_files)} regular Q&A cards now."""

            # Configure retries for validation errors
            regular_response = self.instructor.chat.completions.create(
                model=llm_config.get("model", "gpt-4"),
                messages=[
                    {
                        "role": "system",
                        "content": "Generate ONLY regular Q&A flashcards. Do NOT create any cloze deletion cards."
                    },
                    {
                        "role": "user",
                        "content": regular_prompt
                    }
                ],
                response_model=CardGenerationResponse,
                max_retries=Retrying(
                    stop=stop_after_attempt(3),
                    wait=wait_exponential(multiplier=1, min=4, max=10),
                    reraise=True
                ),
            )
            
            # Generate cloze cards separately
            cloze_count = processing_config.get("cloze_cards_per_page", 2) * len(window_files)
            cloze_prompt = f"""Generate EXACTLY {cloze_count} cloze deletion flashcards from this content.

Content:
{combined_content}

FORMAT: Each card MUST use {{{{c1::hidden text}}}} syntax for cloze deletions.

CRITICAL RULES:
1. Cards MUST be self-contained - no references to "the paper", figures, or external content
2. For equations: Hide PARTS of equations, not entire equations
3. Hide meaningful concepts, not arbitrary numbers or references
4. EVERY card MUST have AT LEAST 2 meaningful tags on the "- #tag1, #tag2" line
5. PRIORITIZE equations - create cloze cards for key mathematical expressions
6. MATH IN CLOZE: When hiding parts of math expressions, the ENTIRE math notation must stay together
   - WRONG: "In {{{{c1::$E[X_j$}}}} | {{{{c2::$X_{{pa(j)}}]$}}}}" (splits the equation)
   - WRONG: "The model {{{{c1::$E[X_j | X_{{}}}} {{{{c2::pa}}}} {{{{c3::(j)}}}}$" (splits subscript)
   - RIGHT: "In the model $E[X_j | {{{{c1::X_{{pa(j)}}}}}}] = {{{{c2::g_j(f_j(X))}}}}$"
   - RIGHT: "The equation {{{{c1::$E[X_j | X_{{pa(j)}}] = g_j(f_j(X))$}}}} represents conditional expectation"

EQUATION FOCUS:
- For EVERY major equation, create at least one cloze card
- Hide key variables, operators, or results in equations
- Keep mathematical notation intact - don't split subscripts, superscripts, or operators
- Examples: 
  * "The transformation uses {{c1::$h(W) = 0$}} to ensure {{c2::acyclicity}}"
  * "The model $E[X_j | X_{{pa(j)}}] = {{{{c1::g_j(f_j(X))}}}}$ represents {{{{c2::conditional expectation}}}}"

GOOD Examples:
## The {{{{c1::Pythagorean theorem}}}} states that {{{{c2::$a^2 + b^2 = c^2$}}}} for right triangles.

- #mathematics.geometry, #theorems.pythagorean

## In gradient descent, the update rule is $\\theta = \\theta - {{{{c1::α}}}} {{{{c2::∇L(θ)}}}}$ where {{{{c3::α is the learning rate}}}}.

- #optimization.gradient-descent, #machine-learning.algorithms

BAD Examples (AVOID):
- "The original method uses {{{{c1::algorithm X}}}}" (What original method? AND missing tags!)
- "{{{{c1::$E[X|Y] = g(f(X))$}}}}" (Don't hide entire equations AND missing tags!)
- "In the context of the document, {{{{c1::h(W) = 0}}}} ensures acyclicity" (Remove "in the context"!)
- "{{{{c1::NAS}}}} is used for model optimization" (Undefined acronym!)
- Tags: #equation, #definition (Generic tags - use conceptual ones!)

REMEMBER: EVERY cloze card MUST have tags just like regular cards!
Generate {cloze_count} cloze cards now. Focus on key definitions, formulas, and facts."""

            # Configure retries for validation errors
            cloze_response = self.instructor.chat.completions.create(
                model=llm_config.get("model", "gpt-4"),
                messages=[
                    {
                        "role": "system",
                        "content": "Generate ONLY cloze deletion flashcards using {{c1::text}} syntax. Ensure that when including math equations in cloze cards, the ENTIRE equation must be inside the cloze markers. Example: {{c1:\\(E = mc^2\\)}} not just {{c1:E}}."
                    },
                    {
                        "role": "user",
                        "content": cloze_prompt
                    }
                ],
                response_model=CardGenerationResponse,
                max_retries=Retrying(
                    stop=stop_after_attempt(3),
                    wait=wait_exponential(multiplier=1, min=4, max=10),
                    reraise=True
                ),
            )
            
            # Apply self-refine if enabled
            refinement_config = self.config.get("refinement", {}).get("refinement", {})
            if refinement_config.get("enabled", False):
                logger.info("Applying self-refine to improve card quality...")
                
                # Refine regular cards
                if regular_response.cards and "regular" in refinement_config.get("content_types", ["regular", "cloze"]):
                    regular_response = self._self_refine_cards(
                        regular_response,
                        doc_summary,
                        "regular"
                    )
                
                # Refine cloze cards
                if cloze_response.cards and "cloze" in refinement_config.get("content_types", ["regular", "cloze"]):
                    cloze_response = self._self_refine_cards(
                        cloze_response,
                        doc_summary,
                        "cloze"
                    )
            
            # Combine responses
            response = CardGenerationResponse(
                cards=regular_response.cards + cloze_response.cards,
                skipped_sections=regular_response.skipped_sections + cloze_response.skipped_sections
            )

            # Debug: Check what cards were generated
            regular_cards = [c for c in response.cards if "{{c" not in c.front.text]
            cloze_cards = [c for c in response.cards if "{{c" in c.front.text]
            logger.debug(f"Generated: {len(regular_cards)} regular cards, {len(cloze_cards)} cloze cards")
            
            # Check for math content
            math_cards = [c for c in response.cards if "$" in c.front.text or "$" in c.back.text]
            logger.debug(f"Math cards: {len(math_cards)}")
            
            # Check for references
            ref_cards = [c for c in response.cards if any(ref in c.front.text.lower() or ref in c.back.text.lower() 
                                                          for ref in ["ref.", "reference", "according to", "["])]
            if ref_cards:
                logger.debug(f"{len(ref_cards)} cards contain references that should have been removed")
            
            # Add the cards from the combined response
            all_cards.extend(response.cards)

        return all_cards

    def generate_image_cards(
        self,
        markdown_files: List[Path],
        doc_summary: DocumentSummary,
        cards_per_image: int = 3,
        image_on_front: bool = True,
        image_on_back: bool = True,
        require_math: bool = False,
        placement_strategy: str = "smart",
        front_back_ratio: float = 0.5,
        image_summaries: Optional[List[ImageSummary]] = None,
    ) -> List[PlainCard]:
        """Generate flashcards from document images.

        Creates cards that test understanding of visual content like
        figures, graphs, and diagrams. Supports various strategies
        for placing images on card fronts or backs.

        Parameters
        ----------
        markdown_files : List[Path]
            Markdown files containing image references
        doc_summary : DocumentSummary
            Document summary for context
        cards_per_image : int, optional
            Number of cards to generate per image (default is 3)
        image_on_front : bool, optional
            Allow images on card fronts (default is True)
        image_on_back : bool, optional
            Allow images on card backs (default is True)
        require_math : bool, optional
            Only process images with math content (default is False)
        placement_strategy : {'smart', 'alternate', 'random', 'prefer_front', 'prefer_back'}, optional
            Strategy for image placement (default is 'smart')
        front_back_ratio : float, optional
            Ratio for random placement strategy (default is 0.5)

        Returns
        -------
        List[PlainCard]
            Generated image-based flashcards

        Notes
        -----
        Image placement strategies:
        - 'smart': Place on front if question references the image
        - 'alternate': Alternate between front and back
        - 'random': Random placement with specified ratio
        - 'prefer_front': Always place on front
        - 'prefer_back': Always place on back

        Images are never placed on both sides of the same card.

        Examples
        --------
        >>> # Generate 2 cards per image, smart placement
        >>> image_cards = pipeline.generate_image_cards(
        ...     markdown_files=files,
        ...     doc_summary=summary,
        ...     cards_per_image=2,
        ...     placement_strategy='smart'
        ... )
        """
        image_cards = []

        for file_path in markdown_files:
            content = file_path.read_text()

            # Extract images from this file
            images = extract_images_from_markdown(content, file_path.parent)

            for image_info in images:
                # Check if math content is required and present
                if require_math and not detect_math_content(image_info["context"]):
                    continue

                logger.debug(f"Generating {cards_per_image} cards for image: {image_info['path']}")

                # Get surrounding content (more context around the image)
                file_content = content

                # Generate prompts for image cards
                prompts_config = self.config.get("prompts", {}).get("prompts", {})
                cards_prompts = prompts_config.get("cards", {})
                models_config = self.config.get("models", {}).get("models", {})
                llm_config = models_config.get("llm", {})

                # Find matching image summary if available
                image_summary_text = None
                if image_summaries:
                    # Try to match by URL/path
                    for img_summary in image_summaries:
                        # Check if paths match (handle different path formats)
                        if (image_info['path'] in img_summary.image_url or 
                            img_summary.image_url in image_info['path'] or
                            Path(image_info['path']).name == Path(img_summary.image_url).name):
                            image_summary_text = img_summary.summary
                            logger.debug(f"Found image summary for {image_info['path']}: {image_summary_text[:50]}...")
                            break
                    
                    if not image_summary_text:
                        logger.debug(f"No matching image summary found for {image_info['path']}")
                        logger.debug(f"  Available summaries: {[img.image_url for img in image_summaries]}")
                
                # Create a specialized prompt for image cards
                image_prompt = f"""Create {cards_per_image} educational flashcards based on this image and its context.

Image Information:
- Path: {image_info['path']}
- Alt text: {image_info['alt']}
- Context: {image_info['context']}
{f'- Image Description: {image_summary_text}' if image_summary_text else ''}

Document Summary Context:
- Title: {doc_summary.title}
- Acronyms: {doc_summary.acronyms}
- Technical terms: {doc_summary.technical_terms}

Full content from this page:
{file_content}

CRITICAL RULES:
- DO NOT include ![Image](...) markdown in your response - the image will be added automatically
- DO NOT put image links in the question or answer text
- Just write the question and answer text referring to "the image" or "this figure"

Requirements:
- Each card should test UNDERSTANDING of concepts, not just ask to describe the image
- Questions should focus on WHY, HOW, or WHAT implications the image shows
- BAD: "How are X and Y represented in this image?" (just asks for description)
- GOOD: "What relationship does the image show between X and Y?" (tests understanding)
- GOOD: "Why does the pathway split into two branches in the diagram?" (tests conceptual understanding)
- Cards can reference specific parts of the image (e.g., "What does the upper pathway represent?")
- Include mathematical notation if present in the image
- Make questions test conceptual understanding, not just visual identification
- {'Image can appear on front or back of card as appropriate' if image_on_front and image_on_back else 'Image should appear on front of card' if image_on_front else 'Image should appear on back of card' if image_on_back else 'No image placement preference'}

FORMAT RULES:
1. Use ## for the question (front of card) - NO IMAGE MARKDOWN
2. Answer goes on the next line (back of card) - NO IMAGE MARKDOWN
3. Tags go as a single bullet: - #tag1, #tag2, #tag3
4. Use period-delimited tags from broad to narrow (e.g., #biology.cell-biology, #machine-learning.neural-networks)
5. DO NOT include figure/image tags like #figures, #diagrams, #graphs - the card already has an image
6. NEVER include ![Image](...) in your text - images are handled separately

Example card for an image:
## What relationship between learning rate and convergence is shown in this graph?

The graph demonstrates that smaller learning rates lead to slower but more stable convergence, while larger learning rates can cause oscillations or divergence. The optimal learning rate (shown in green) balances speed and stability.

- #optimization.learning-rate, #machine-learning.training, #convergence-analysis"""

                # Generate cards using instructor
                try:
                    response = self.instructor.chat.completions.create(
                        model=llm_config.get("model", "gpt-4"),
                        messages=[
                            {
                                "role": "system",
                                "content": cards_prompts.get(
                                    "system",
                                    "You are an expert at creating educational flashcards that test understanding of visual content.",
                                ),
                            },
                            {"role": "user", "content": image_prompt},
                        ],
                        response_model=CardGenerationResponse,
                        max_retries=llm_config.get("max_retries", 3),
                    )

                    # Apply self-refine if enabled for image cards
                    refinement_config = self.config.get("refinement", {}).get("refinement", {})
                    if refinement_config.get("enabled", False) and "image" in refinement_config.get("content_types", ["regular", "cloze", "image"]):
                        logger.info(f"Applying self-refine to image cards for {image_info['path']}...")
                        response = self._self_refine_cards(
                            response,
                            doc_summary,
                            "image"
                        )

                    # Add image paths to the generated cards
                    for idx, card in enumerate(response.cards):
                        # Clean up any image markdown that might have slipped through
                        # Remove ![Image](...) patterns from both front and back text
                        import re
                        image_pattern = r'!\[.*?\]\([^)]+\)'
                        card.front.text = re.sub(image_pattern, '', card.front.text).strip()
                        card.back.text = re.sub(image_pattern, '', card.back.text).strip()
                        
                        # Decide where to place the image based on config
                        if image_on_front and not image_on_back:
                            card.front.image_path = image_info["original_path"]
                            if image_summary_text:
                                card.front.image_summary = image_summary_text
                        elif image_on_back and not image_on_front:
                            card.back.image_path = image_info["original_path"]
                            if image_summary_text:
                                card.back.image_summary = image_summary_text
                            else:
                                logger.error(f"No image summary found for {image_info['path']}")
                        elif image_on_front and image_on_back:
                            # Both allowed, but NEVER put the same image on both sides
                            place_on_front = False

                            if placement_strategy == "smart":
                                # Place on front if question references the image
                                place_on_front = any(
                                    word in card.front.text.lower()
                                    for word in [
                                        "figure",
                                        "image",
                                        "graph",
                                        "chart",
                                        "diagram",
                                        "show",
                                        "illustrate",
                                        "depict",
                                        "visual",
                                    ]
                                )
                            elif placement_strategy == "alternate":
                                # Alternate between front and back
                                place_on_front = idx % 2 == 0
                            elif placement_strategy == "random":
                                # Random with specified ratio
                                place_on_front = random.random() < front_back_ratio
                            elif placement_strategy == "prefer_front":
                                place_on_front = True
                            elif placement_strategy == "prefer_back":
                                place_on_front = False

                            # Place image on ONLY ONE side
                            if place_on_front:
                                card.front.image_path = image_info["original_path"]
                                if image_summary_text:
                                    card.front.image_summary = image_summary_text
                                # Explicitly ensure IMAGE is not on the back (but keep summary for audio)
                                card.back.image_path = None
                                # Don't clear back.image_summary - we might need it for audio
                            else:
                                card.back.image_path = image_info["original_path"]
                                if image_summary_text:
                                    card.back.image_summary = image_summary_text
                                else:
                                    # If no summary was found, log error
                                    logger.error(f"No image summary found for {image_info['path']}")
                                # Explicitly ensure IMAGE is not on the front
                                card.front.image_path = None

                    image_cards.extend(response.cards)

                    # Debug output for image placement
                    front_count = sum(
                        1 for card in response.cards if card.front.image_path
                    )
                    back_count = sum(
                        1 for card in response.cards if card.back.image_path
                    )
                    logger.debug(f"Generated {len(response.cards)} cards for image {image_info['path']}")
                    logger.debug(f"  Image placement - Front: {front_count}, Back: {back_count} (strategy: {placement_strategy})")

                except Exception as e:
                    logger.error(f"Error generating cards for image {image_info['path']}: {e}")
                    continue

        return image_cards

    def generate_outputs(
        self, cards: List[PlainCard], summary: DocumentSummary, output_dir: Path
    ) -> Dict[str, Path]:
        """Generate output files in configured formats.

        Creates various output files including plain cards, cards with
        audio links, and document summary based on configuration.

        Parameters
        ----------
        cards : List[PlainCard]
            Generated flashcards
        summary : DocumentSummary
            Document summary
        output_dir : Path
            Directory for output files

        Returns
        -------
        Dict[str, Path]
            Mapping of output types to file paths:
            - 'cards_plain': Plain markdown cards
            - 'cards_audio': Cards with audio (if enabled)
            - 'summary': Document summary

        Notes
        -----
        Audio card output is only generated if complementary audio
        generation is enabled in configuration.
        """
        outputs = {}

        # Get output config
        output_config = self.config.get("output", {}).get("output", {})
        formats = output_config.get("formats", {})
        tag_format = output_config.get("tag_format", "slugified")

        # Plain cards (no audio)
        plain_path = output_dir / formats.get("cards_plain", "cards-plain.md")
        with open(plain_path, "w") as f:
            for card in cards:
                f.write(
                    card.to_md(
                        include_audio=False,
                        citation_key=self.citation_key,
                        tag_format=tag_format,
                    )
                )
        outputs["cards_plain"] = plain_path

        # Note: Cards with audio will be written after audio generation
        # This ensures the audio URIs are properly set on the cards
        # See generate_audio method for audio card generation

        # Document summary
        summary_path = output_dir / formats.get("summary", "document-summary.md")
        with open(summary_path, "w") as f:
            f.write(f"# {summary.title}\\n\\n")
            f.write(f"**Authors:** {', '.join(summary.authors)}\\n\\n")
            f.write(f"## Summary\\n\\n{summary.summary}\\n\\n")
            f.write(f"## Key Contributions\\n\\n")
            for contrib in summary.key_contributions:
                f.write(f"- {contrib}\\n")
            f.write(f"\\n## Acronyms\\n\\n")
            for acronym, definition in summary.acronyms.items():
                f.write(f"- **{acronym}**: {definition}\\n")
        outputs["summary"] = summary_path

        return outputs

    def generate_audio(
        self,
        cards: List[PlainCard],
        summary: DocumentSummary,
        outputs: Dict[str, Path],
        cleaned_files: List[Path],
        image_summaries: List[ImageSummary],
    ):
        """Generate audio files for various content types.

        Creates audio files based on configuration including card audio,
        summary narration, full document reading, and educational lectures.

        Parameters
        ----------
        cards : List[PlainCard]
            Flashcards for audio generation
        summary : DocumentSummary
            Document summary for narration
        outputs : Dict[str, Path]
            Output file paths
        cleaned_files : List[Path]
            Cleaned markdown files for reading
        image_summaries : List[ImageSummary]
            Image summaries for lecture content

        Raises
        ------
        RuntimeError
            If required API keys are not set in environment

        Notes
        -----
        Requires ELEVEN_LABS_API_KEY and OPENAI_API_KEY environment
        variables. Generates different audio types based on config:
        - Complementary: Front/back audio for each card
        - Summary: Narration of document summary
        - Reading: Full document text-to-speech
        - Lecture: Educational presentation style

        See Also
        --------
        utils.audio : Audio generation utility functions
        """
        audio_config = self.config.get("audio", {}).get("audio", {})

        # Get API keys
        elevenlabs_api_key = os.getenv("ELEVEN_LABS_API_KEY")
        if not elevenlabs_api_key:
            raise RuntimeError("ELEVEN_LABS_API_KEY not set in environment.")

        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            raise RuntimeError("OPENAI_API_KEY not set in environment.")
        openai_client = OpenAI(api_key=openai_api_key)

        # Get model config
        models_config = self.config.get("models", {}).get("models", {})
        llm_config = models_config.get("llm", {})
        model = llm_config.get("model", "gpt-4o")
        voice_id = audio_config.get("voice_id")

        # Generate complementary audio (card audio)
        if audio_config.get("generate_complementary", False):
            logger.info("Generating complementary audio...")
            audio_dir = self.output_base / "gen-md-complementary-audio"
            audio_dir.mkdir(exist_ok=True)

            for i, card in enumerate(cards):
                # Use consistent card numbering instead of misleading page numbers
                # This ensures audio files match the card order
                card_base = f"card"

                # Get complementary audio speed from config
                complementary_speed = audio_config.get("complementary_speed", 1.0)
                # Get force regenerate option from config
                force_regenerate_citation = audio_config.get("force_regenerate_citation", False)

                front_filename, back_filename = generate_card_audio(
                    card=card,
                    card_index=i + 1,
                    page_base=card_base,
                    audio_dir=audio_dir,
                    openai_client=openai_client,
                    elevenlabs_api_key=elevenlabs_api_key,
                    voice_id=voice_id,
                    model=model,
                    citation_key=self.citation_key,
                    speed=complementary_speed,
                    force_regenerate_citation=force_regenerate_citation,
                )
                
                # Set audio URIs on the card for robust pairing
                if front_filename:
                    # Use relative path from output directory
                    card.audio_front_uri = f"gen-md-complementary-audio/{front_filename}"
                if back_filename:
                    card.audio_back_uri = f"gen-md-complementary-audio/{back_filename}"

                # Validate audio transcript matches card content
                if not card.validate_audio_match():
                    print(f"WARNING: Audio transcript mismatch for card {i+1}")
                
                if back_filename:
                    print(
                        f"Generated audio for card {i+1}: {front_filename}, {back_filename}"
                    )
                else:
                    print(
                        f"Generated audio for card {i+1}: {front_filename} (front only)"
                    )

        # Generate summary audio
        if audio_config.get("generate_summary", False):
            logger.info("Generating summary audio...")
            summary_text = f"{summary.summary}\n\nKey Contributions:\n" + "\n".join(
                [f"- {contrib}" for contrib in summary.key_contributions]
            )
            summary_audio_path = (
                self.output_base / f"{self.audio_prefix}-summary-audio.mp3"
            )

            # Get summary audio speed from config
            summary_speed = audio_config.get("summary_speed", 1.0)

            generate_summary_audio(
                summary_text=summary_text,
                output_path=summary_audio_path,
                openai_client=openai_client,
                elevenlabs_api_key=elevenlabs_api_key,
                voice_id=voice_id,
                model=model,
                citation_key=self.citation_key,
                speed=summary_speed,
            )
            print(f"Generated summary audio: {summary_audio_path.name}")

        # Generate reading audio (full document)
        if audio_config.get("generate_reading", False):
            logger.info("Generating reading audio...")
            # Combine all cleaned markdown content
            full_content = "\n\n".join([f.read_text() for f in cleaned_files])
            reading_audio_path = (
                self.output_base / f"{self.audio_prefix}-reading-audio.mp3"
            )

            # Get reading audio speed from config
            reading_speed = audio_config.get("reading_speed", 1.0)

            generate_reading_audio(
                full_content=full_content,
                output_path=reading_audio_path,
                openai_client=openai_client,
                elevenlabs_api_key=elevenlabs_api_key,
                voice_id=voice_id,
                model=model,
                citation_key=self.citation_key,
                speed=reading_speed,
            )
            print(f"Generated reading audio: {reading_audio_path.name}")

        # Generate lecture audio (educational style)
        if audio_config.get("generate_lecture", False):
            logger.info("Generating lecture audio...")
            lecture_audio_path = (
                self.output_base / f"{self.audio_prefix}-lecture-audio.mp3"
            )

            # Get lecture prompt configuration
            prompts_config = self.config.get("prompts", {}).get("prompts", {})
            audio_prompts = prompts_config.get("audio", {})
            lecture_prompt_config = {
                "lecture_system": audio_prompts.get("lecture_system"),
                "lecture_generation": audio_prompts.get("lecture_generation"),
            }

            # Extract image summaries as strings
            image_summary_strings = [img.summary for img in image_summaries]

            # Get lecture audio speed from config (defaults to same as summary)
            lecture_speed = audio_config.get(
                "lecture_speed", audio_config.get("summary_speed", 1.0)
            )

            generate_lecture_audio(
                markdown_files=cleaned_files,
                image_summaries=image_summary_strings,
                output_path=lecture_audio_path,
                openai_client=openai_client,
                elevenlabs_api_key=elevenlabs_api_key,
                voice_id=voice_id,
                model=model,
                citation_key=self.citation_key,
                lecture_prompt_config=lecture_prompt_config,
                speed=lecture_speed,
            )
            print(f"Generated lecture audio: {lecture_audio_path.name}")
        
        # After all audio generation is complete, write cards with audio links
        if audio_config.get("generate_complementary", False):
            # Get output config
            output_config = self.config.get("output", {}).get("output", {})
            formats = output_config.get("formats", {})
            tag_format = output_config.get("tag_format", "slugified")
            
            # Write cards with audio using the URIs stored in each card
            audio_path = self.output_base / formats.get("cards_audio", "cards-with-audio.md")
            with open(audio_path, "w") as f:
                for card in cards:
                    f.write(
                        card.to_md(
                            include_audio=True,
                            citation_key=self.citation_key,
                            tag_format=tag_format,
                        )
                    )
            outputs["cards_audio"] = audio_path
            logger.debug(f"Written cards with audio: {audio_path.name}")
            
            # Create a summary of audio transcripts for debugging
            transcripts_dir = self.output_base / "audio-transcripts"
            if transcripts_dir.exists():
                summary_path = transcripts_dir / "transcript-summary.md"
                with open(summary_path, "w") as f:
                    f.write("# Audio Transcript Summary\n\n")
                    f.write(f"Generated transcripts for {len(cards)} cards\n\n")
                    
                    # Count cards with images
                    cards_with_images = sum(1 for card in cards if card.front.image_path or card.back.image_path)
                    cards_with_summaries = sum(1 for card in cards if card.front.image_summary or card.back.image_summary)
                    
                    f.write(f"- Total cards: {len(cards)}\n")
                    f.write(f"- Cards with images: {cards_with_images}\n")
                    f.write(f"- Cards with image summaries: {cards_with_summaries}\n\n")
                    
                    # List any cards missing summaries
                    missing_summaries = [
                        card for card in cards 
                        if (card.front.image_path or card.back.image_path) 
                        and not (card.front.image_summary or card.back.image_summary)
                    ]
                    
                    if missing_summaries:
                        f.write(f"## Cards Missing Image Summaries ({len(missing_summaries)} cards)\n\n")
                        for card in missing_summaries:
                            f.write(f"- Card ID: {card.card_id}\n")
                            f.write(f"  - Front image: {card.front.image_path}\n")
                            f.write(f"  - Back image: {card.back.image_path}\n")
                            f.write(f"  - Front text preview: {card.front.text[:50]}...\n\n")
                    
                    f.write("\n## Transcript Files Generated\n\n")
                    transcript_files = sorted(transcripts_dir.glob("*.md"))
                    # Exclude the summary file itself
                    transcript_files = [f for f in transcript_files if f.name != "transcript-summary.md"]
                    for tf in transcript_files:
                        f.write(f"- {tf.name}\n")
                
                print(f"Written transcript summary: {summary_path.name}")

    def format_deck_name(self, template: str, deck_name: str) -> str:
        """Format deck name template with variables.

        Replaces template variables in deck name with actual values.

        Parameters
        ----------
        template : str
            Deck name template (e.g., '{deck_name}_cards')
        deck_name : str
            Deck name to substitute (output_dir if specified, otherwise citation_key)

        Returns
        -------
        str
            Formatted deck name

        Examples
        --------
        >>> pipeline.format_deck_name("{deck_name}_2024", "Smith")
        'Smith_2024'
        """
        # Support template variables
        variables = {
            "deck_name": deck_name or "default",
            "citation_key": self.citation_key
            or "default",  # Still support citation_key for backward compatibility
        }

        # Replace template variables
        formatted = template
        for var, value in variables.items():
            formatted = formatted.replace(f"{{{var}}}", value)

        return formatted

    def prepare_anki_file(
        self,
        cards: List[PlainCard],
        deck_name: str,
        output_path: Path,
        include_audio: bool = True,
    ) -> Path:
        """Prepare markdown file for Anki import.

        Creates a properly formatted markdown file with deck header
        required by the Anki markdown importer.

        Parameters
        ----------
        cards : List[PlainCard]
            Cards to include
        deck_name : str
            Name of the Anki deck
        output_path : Path
            Base output file path
        include_audio : bool, optional
            Whether to include audio links (default is True)

        Returns
        -------
        Path
            Path to prepared Anki file

        Notes
        -----
        Adds '# DeckName' header required by md_to_anki.py.
        Preserves exact card formatting from original output.
        """
        anki_file = output_path.parent / f"anki-{output_path.name}"

        # First, read the existing output file to use its exact format
        # This ensures we preserve the exact card format that was generated
        with open(output_path, "r") as f:
            content = f.read()

        with open(anki_file, "w") as f:
            # Write deck name header (required by md_to_anki.py)
            f.write(f"# {deck_name}\n\n")

            # Write the rest of the content as-is
            # This preserves the exact tag format from the original file
            f.write(content)

        return anki_file

    def send_to_anki(
        self,
        cards: List[PlainCard],
        outputs: Dict[str, Path],
        anki_config: Dict[str, Any],
    ):
        """Send generated cards to Anki via AnkiConnect.

        Uploads cards to Anki using the AnkiConnect API, supporting
        deck creation, card updates, and media file uploads.

        Parameters
        ----------
        cards : List[PlainCard]
            Flashcards to send
        outputs : Dict[str, Path]
            Output file paths
        anki_config : Dict[str, Any]
            Anki configuration options:
            - deck_name: Template for deck name (supports {citation_key})
            - card_format: 'plain' or 'with_audio'
            - update_existing: Update existing cards
            - media_upload: Upload media files
            - sync_after: Sync after upload
            - host: AnkiConnect host
            - port: AnkiConnect port

        Raises
        ------
        Exception
            If connection to Anki fails or upload errors occur

        Notes
        -----
        Requires Anki to be running with AnkiConnect addon installed.
        Creates deck if it doesn't exist. Handles both new cards and
        updates to existing cards based on configuration.

        See Also
        --------
        AnkiProcessor : Handles AnkiConnect communication
        """
        try:
            # Format deck name with template variables
            # Use output_dir (stored in audio_prefix) if it was specified, otherwise use citation_key
            deck_template = anki_config.get("deck_name", "{deck_name}")
            # Use audio_prefix which contains output_dir if specified, otherwise citation_key
            deck_name_value = (
                self.audio_prefix
                if hasattr(self, "audio_prefix")
                else self.citation_key
            )
            deck_name = self.format_deck_name(deck_template, deck_name_value)

            logger.info(f"Sending cards to Anki deck: {deck_name}")

            # Choose which output file to use as base
            # Important: Only use audio cards if they actually exist
            card_format = anki_config.get("card_format", "with_audio")
            if card_format == "with_audio" and "cards_audio" in outputs:
                base_file = outputs["cards_audio"]
            else:
                # Fall back to plain cards if audio cards don't exist or not requested
                base_file = outputs["cards_plain"]

            # Prepare Anki file with proper deck header
            # Only include audio if it was actually generated
            use_audio = card_format == "with_audio" and "cards_audio" in outputs
            anki_file = self.prepare_anki_file(
                cards, deck_name, base_file, include_audio=use_audio
            )

            # Initialize AnkiProcessor
            host = anki_config.get("host", "127.0.0.1")
            port = anki_config.get("port", 8765)
            anki_processor = AnkiProcessor(host, port)

            # Send cards to Anki
            cards_added, cards_updated = anki_processor.send_cards_from_file(
                file_path=anki_file,
                deck_name=deck_name,
                update_existing=anki_config.get("update_existing", True),
                upload_media=anki_config.get("media_upload", True),
                sync_after=anki_config.get("sync_after", False),
            )

            logger.info(
                f"Successfully sent to Anki deck '{deck_name}': {cards_added} added, {cards_updated} updated"
            )

        except Exception as e:
            logger.error(f"Failed to send cards to Anki: {e}")
            raise

    def _self_refine_cards(
        self,
        response: CardGenerationResponse,
        doc_summary: DocumentSummary,
        card_type: str
    ) -> CardGenerationResponse:
        """Apply self-refine pattern to improve card quality.
        
        Iteratively generates feedback and refines cards until they meet
        quality standards or reach maximum iterations.
        
        Parameters
        ----------
        response : CardGenerationResponse
            Initial card generation response
        doc_summary : DocumentSummary
            Document summary for context
        card_type : str
            Type of cards ('regular', 'cloze', or 'image')
            
        Returns
        -------
        CardGenerationResponse
            Refined cards response
        """
        refinement_config = self.config.get("refinement", {}).get("refinement", {})
        max_iterations = refinement_config.get("max_iterations", 3)
        
        # Track refinement history
        history = RefinementHistory()
        
        for iteration in range(max_iterations):
            # Generate feedback
            feedback = self._generate_card_feedback(
                response.cards,
                doc_summary,
                card_type
            )
            
            # Check if cards are good enough
            if feedback.done:
                logger.info(f"{card_type.capitalize()} cards passed quality check after {iteration} iterations")
                break
            
            # Log feedback
            logger.info(f"Iteration {iteration + 1} feedback for {card_type} cards:")
            for issue in feedback.feedback:
                logger.info(f"  - {issue}")
            
            # Refine cards based on feedback
            refined_response = self._refine_cards(
                response,
                feedback,
                doc_summary,
                card_type
            )
            
            # Save to history
            history.add_iteration(response.cards, feedback, refined_response.cards)
            
            # Update response for next iteration
            response = refined_response
            
        return response
    
    def _generate_card_feedback(
        self,
        cards: List[PlainCard],
        doc_summary: DocumentSummary,
        card_type: str
    ) -> CardFeedback:
        """Generate quality feedback for cards.
        
        Parameters
        ----------
        cards : List[PlainCard]
            Cards to evaluate
        doc_summary : DocumentSummary
            Document context
        card_type : str
            Type of cards being evaluated
            
        Returns
        -------
        CardFeedback
            Structured feedback about card quality
        """
        refinement_config = self.config.get("refinement", {}).get("refinement", {})
        feedback_prompts = refinement_config.get("feedback_prompts", {})
        
        # Format cards for evaluation
        cards_text = self._format_cards_for_feedback(cards)
        
        # Get appropriate feedback prompt
        feedback_prompt = feedback_prompts.get(f"{card_type}_cards", "")
        
        # Get LLM config
        models_config = self.config.get("models", {}).get("models", {})
        llm_config = models_config.get("llm", {})
        
        system_prompt = f"""You are an expert flashcard quality evaluator.
Check for these issues in {card_type} cards:
1. External references ([1], "According to X", "Figure 3")
2. Insufficient context ("this", "the model")
3. Generic tags (#equation vs #calculus.derivatives)
4. Rote memorization ("What does X stand for?")
5. Math formatting issues
6. Cloze problems (multiple deletions, split equations)
7. Undefined acronyms
8. Author-centric questions

If ALL cards are high quality, set done=True.
Otherwise provide specific, actionable feedback."""
        
        return self.instructor.chat.completions.create(
            model=llm_config.get("model", "gpt-4"),
            response_model=CardFeedback,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": f"""
Document context:
Title: {doc_summary.title}
Acronyms: {doc_summary.acronyms}
Technical terms: {doc_summary.technical_terms}

Cards to evaluate:
{cards_text}

{feedback_prompt}
"""
                }
            ],
            max_retries=Retrying(
                stop=stop_after_attempt(2),
                wait=wait_exponential(multiplier=1, min=2, max=5)
            )
        )
    
    def _refine_cards(
        self,
        response: CardGenerationResponse,
        feedback: CardFeedback,
        doc_summary: DocumentSummary,
        card_type: str
    ) -> CardGenerationResponse:
        """Refine cards based on feedback.
        
        Parameters
        ----------
        response : CardGenerationResponse
            Original cards
        feedback : CardFeedback
            Feedback to address
        doc_summary : DocumentSummary
            Document context
        card_type : str
            Type of cards
            
        Returns
        -------
        CardGenerationResponse
            Refined cards
        """
        refinement_config = self.config.get("refinement", {}).get("refinement", {})
        refinement_prompts = refinement_config.get("refinement_prompts", {})
        
        # Format cards and feedback
        cards_text = self._format_cards_for_feedback(response.cards)
        feedback_text = "\n".join([f"- {f}" for f in feedback.feedback])
        
        # Get refinement prompt
        refinement_prompt = refinement_prompts.get(f"{card_type}_cards", "")
        
        # Get LLM config
        models_config = self.config.get("models", {}).get("models", {})
        llm_config = models_config.get("llm", {})
        
        return self.instructor.chat.completions.create(
            model=llm_config.get("model", "gpt-4"),
            response_model=CardGenerationResponse,
            messages=[
                {
                    "role": "system",
                    "content": f"""You are an expert flashcard creator.
Refine the {card_type} cards to address ALL feedback issues.
Maintain the same number and types of cards."""
                },
                {
                    "role": "user",
                    "content": f"""
Original cards:
{cards_text}

Feedback to address:
{feedback_text}

Document context:
Title: {doc_summary.title}
Acronyms: {doc_summary.acronyms}
Technical terms: {doc_summary.technical_terms}

{refinement_prompt}

Generate {len(response.cards)} improved {card_type} cards addressing all feedback.
"""
                }
            ],
            max_retries=Retrying(
                stop=stop_after_attempt(2),
                wait=wait_exponential(multiplier=1, min=2, max=5)
            )
        )
    
    def _format_cards_for_feedback(self, cards: List[PlainCard]) -> str:
        """Format cards for feedback evaluation.
        
        Parameters
        ----------
        cards : List[PlainCard]
            Cards to format
            
        Returns
        -------
        str
            Formatted card text
        """
        formatted = []
        for i, card in enumerate(cards):
            formatted.append(f"Card {i + 1}:")
            formatted.append(f"Front: {card.front.text}")
            if not ("{{c" in card.front.text):  # Regular card
                formatted.append(f"Back: {card.back.text}")
            formatted.append(f"Tags: {', '.join(card.tags)}")
            formatted.append("")  # Empty line between cards
        
        return "\n".join(formatted)
    
    def _self_refine_audio_transcript(
        self,
        transcript: str,
        card_type: str,
        doc_summary: DocumentSummary
    ) -> str:
        """Apply self-refine to audio transcripts.
        
        Parameters
        ----------
        transcript : str
            Original audio transcript
        card_type : str
            Type of card ('regular', 'cloze', etc.)
        doc_summary : DocumentSummary
            Document context
            
        Returns
        -------
        str
            Refined transcript suitable for TTS
        """
        refinement_config = self.config.get("refinement", {}).get("refinement", {})
        
        if not refinement_config.get("include_audio", False):
            return transcript
        
        max_iterations = refinement_config.get("max_iterations", 3)
        
        for iteration in range(max_iterations):
            # Generate feedback for transcript
            feedback = self._generate_audio_feedback(transcript, card_type, doc_summary)
            
            if feedback.done:
                logger.info(f"Audio transcript passed quality check after {iteration} iterations")
                break
            
            # Refine transcript
            transcript = self._refine_audio_transcript(
                transcript,
                feedback,
                card_type,
                doc_summary
            )
        
        return transcript
    
    def _generate_audio_feedback(
        self,
        transcript: str,
        card_type: str,
        doc_summary: DocumentSummary
    ) -> AudioTranscriptFeedback:
        """Generate feedback for audio transcript.
        
        Parameters
        ----------
        transcript : str
            Transcript to evaluate
        card_type : str
            Type of content
        doc_summary : DocumentSummary
            Document context
            
        Returns
        -------
        AudioTranscriptFeedback
            Feedback about transcript quality
        """
        refinement_config = self.config.get("refinement", {}).get("refinement", {})
        feedback_prompts = refinement_config.get("feedback_prompts", {})
        
        # Get LLM config
        models_config = self.config.get("models", {}).get("models", {})
        llm_config = models_config.get("llm", {})
        
        return self.instructor.chat.completions.create(
            model=llm_config.get("model", "gpt-4"),
            response_model=AudioTranscriptFeedback,
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert in audio transcript quality for text-to-speech."
                },
                {
                    "role": "user",
                    "content": f"""
Transcript to evaluate:
{transcript}

Card type: {card_type}
Citation key: {doc_summary.citation_key if hasattr(doc_summary, 'citation_key') else 'Unknown'}
Acronyms in document: {doc_summary.acronyms}

{feedback_prompts.get(f'{card_type}_audio', feedback_prompts.get('audio_transcript', ''))}
"""
                }
            ]
        )
    
    def _refine_audio_transcript(
        self,
        transcript: str,
        feedback: AudioTranscriptFeedback,
        card_type: str,
        doc_summary: DocumentSummary
    ) -> str:
        """Refine audio transcript based on feedback.
        
        Parameters
        ----------
        transcript : str
            Original transcript
        feedback : AudioTranscriptFeedback
            Feedback to address
        card_type : str
            Type of content
        doc_summary : DocumentSummary
            Document context
            
        Returns
        -------
        str
            Refined transcript
        """
        refinement_config = self.config.get("refinement", {}).get("refinement", {})
        refinement_prompts = refinement_config.get("refinement_prompts", {})
        
        # Get LLM config
        models_config = self.config.get("models", {}).get("models", {})
        llm_config = models_config.get("llm", {})
        
        feedback_text = "\n".join([f"- {f}" for f in feedback.feedback])
        
        messages = [
            {
                "role": "system",
                "content": "You are an expert at creating clear audio transcripts for text-to-speech."
            },
            {
                "role": "user",
                "content": f"""
Original transcript:
{transcript}

Issues to fix:
{feedback_text}

Context:
- Card type: {card_type}
- Document acronyms: {doc_summary.acronyms}

{refinement_prompts.get(f'{card_type}_audio', refinement_prompts.get('audio_transcript', ''))}

Rewrite the transcript addressing all issues.
"""
            }
        ]
        
        response = self.instructor.chat.completions.create(
            model=llm_config.get("model", "gpt-4"),
            messages=messages,
            response_model=None  # Just get raw text response
        )
        
        return response.choices[0].message.content
