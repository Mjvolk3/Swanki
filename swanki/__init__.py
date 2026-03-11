"""
swanki/__init__.py
[[swanki]]
https://github.com/Mjvolk3/Swanki/tree/main/swanki/__init__.py
Test file: tests/test_swanki.py

Automated flashcard generation from academic PDFs.
"""

from .legacy.clean_md import clean_markdown_files as clean_markdown_files
from .legacy.clean_transcript import clean_transcript as clean_transcript
from .legacy.combine import combine_mds as combine_mds
from .legacy.generate_cards import generate_text_cards as generate_text_cards
from .legacy.generate_cards_with_complementary_audio import (
    enrich_gen_md as enrich_gen_md,
)
from .legacy.generate_complementary_audio_gen_md import (
    generate_audio_from_transcripts as generate_audio_from_transcripts,
)
from .legacy.generate_complementary_audio_transcript_gen_md import (
    generate_complementary_audio_transcript_plain_card as generate_complementary_audio_transcript_plain_card,
)
from .legacy.generate_complementary_audio_transcript_image_cards import (
    generate_complementary_audio_transcript_image_card as generate_complementary_audio_transcript_image_card,
)
from .legacy.generate_image_cards import generate_image_cards as generate_image_cards
from .legacy.generate_image_cards_with_complementary_audio import (
    enrich_image_cards as enrich_image_cards,
)
from .legacy.generate_reading_transcript import (
    clean_reading_transcript as clean_reading_transcript,
)
from .legacy.generate_reading_transcript import (
    generate_reading_transcript_input as generate_reading_transcript_input,
)
from .legacy.generate_transcript import (
    generate_transcript as generate_transcript,
)
from .legacy.generate_transcript import (
    generate_transcript_input as generate_transcript_input,
)
from .legacy.image_summary_replace import (
    process_images_summaries as process_images_summaries,
)
from .legacy.mathpix import convert_pdf_to_markdown as convert_pdf_to_markdown
from .legacy.recombine_md import recombine_md_files as recombine_md_files
from .legacy.split_pdf import split_pdf_into_pages as split_pdf_into_pages
from .legacy.token_count import count_tokens_in_md_file as count_tokens_in_md_file
from .legacy.transcript_to_audio import (
    generate_audio_from_transcript as generate_audio_from_transcript,
)
from .pipeline import Pipeline as Pipeline

__all__ = [
    "Pipeline",
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
