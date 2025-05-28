"""Swanki: Automated flashcard generation from academic PDFs.

Swanki is a Python package that transforms academic PDFs into Anki flashcards with
AI-generated content. It processes PDFs by extracting text and images, generating
summaries, creating question-answer pairs, and optionally adding audio narration.

The package provides both a modern pipeline-based API and legacy functions for
backward compatibility.

Main Components
---------------
Pipeline : class
    Main interface for processing PDFs through the complete workflow
ConfigGenerator : class
    Configuration management for the processing pipeline

Legacy Functions
----------------
The package maintains backward compatibility with legacy functions for:
- PDF processing (splitting, converting to markdown)
- Content generation (cards, transcripts, audio)
- Image processing (extraction, summarization)

Examples
--------
Basic usage with the modern API:

>>> from swanki import Pipeline, ConfigGenerator
>>> 
>>> # Generate configuration
>>> config_gen = ConfigGenerator()
>>> config = config_gen.generate(
...     pdf_path="paper.pdf",
...     output_dir="output",
...     deck_name="MyDeck"
... )
>>> 
>>> # Process PDF
>>> pipeline = Pipeline(config)
>>> pipeline.run()

Notes
-----
For new projects, use the Pipeline API. Legacy functions are maintained
for backward compatibility but may be deprecated in future versions.
"""

# New refactored components
from .config import ConfigGenerator
from .pipeline import Pipeline

# Legacy imports for backward compatibility
from .legacy.mathpix import convert_pdf_to_markdown
from .legacy.clean_md import clean_markdown_files
from .legacy.split_pdf import split_pdf_into_pages
from .legacy.generate_cards import generate_text_cards
from .legacy.recombine_md import recombine_md_files
from .legacy.combine import combine_mds
from .legacy.token_count import count_tokens_in_md_file
from .legacy.image_summary_replace import process_images_summaries
from .legacy.generate_image_cards import generate_image_cards
from .legacy.generate_transcript import generate_transcript_input, generate_transcript
from .legacy.clean_transcript import clean_transcript
from .legacy.transcript_to_audio import generate_audio_from_transcript
from .legacy.generate_reading_transcript import clean_reading_transcript
from .legacy.generate_reading_transcript import generate_reading_transcript_input
from .legacy.generate_complementary_audio_transcript_gen_md import (
    generate_complementary_audio_transcript_plain_card,
)

from .legacy.generate_complementary_audio_transcript_image_cards import (
    generate_complementary_audio_transcript_image_card,
)
from .legacy.generate_complementary_audio_gen_md import generate_audio_from_transcripts
from .legacy.generate_cards_with_complementary_audio import enrich_gen_md
from .legacy.generate_image_cards_with_complementary_audio import enrich_image_cards

# New exports
new_exports = [
    "ConfigGenerator",
    "Pipeline",
]

# Legacy exports for backward compatibility
legacy_exports = [
    "split_pdf_into_pages",
    "convert_pdf_to_markdown",
    "clean_markdown_files",
    "generate_text_cards",
    "recombine_md_files",
    "combine_mds",
    "count_tokens_in_md_file",
    "process_images_summaries",
    "generate_image_cards",
    "generate_transcript_input",
    "generate_transcript",
    "clean_transcript",
    "generate_audio_from_transcript",
    "clean_reading_transcript",
    "generate_reading_transcript_input",
    "generate_complementary_audio_transcript_plain_card",
    "generate_complementary_audio_transcript_image_card",
    "generate_audio_from_transcripts",
    "enrich_gen_md",
    "enrich_image_cards",
]

__all__ = new_exports + legacy_exports
