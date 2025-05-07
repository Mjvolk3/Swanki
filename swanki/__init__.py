# swanki/__init__.py
from .mathpix import convert_pdf_to_markdown
from .clean_md import clean_markdown_files
from .split_pdf import split_pdf_into_pages
from .generate_cards import generate_text_cards
from .recombine_md import recombine_md_files
from .combine import combine_mds
from .token_count import count_tokens_in_md_file
from .image_summary_replace import process_images_summaries
from .generate_image_cards import generate_image_cards
from .generate_transcript import generate_transcript_input, generate_transcript
from .clean_transcript import clean_transcript
from .transcript_to_audio import generate_audio_from_transcript
from .generate_reading_transcript import clean_reading_transcript
from .generate_reading_transcript import generate_reading_transcript_input
from .generate_complementary_audio_transcript_gen_md import (
    generate_complementary_audio_transcript_plain_card,
)

from .generate_complementary_audio_transcript_image_cards import (
    generate_complementary_audio_transcript_image_card,
)
from .generate_complementary_audio_gen_md import generate_audio_from_transcripts
from .generate_cards_with_complementary_audio import enrich_gen_md
from .generate_image_cards_with_complementary_audio import enrich_image_cards

functions = [
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

__all__ = functions
