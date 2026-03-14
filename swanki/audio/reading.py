"""
swanki/audio/reading.py
[[swanki.audio.reading]]
https://github.com/Mjvolk3/Swanki/tree/main/swanki/audio/reading.py

Full document reading with two-pass LLM processing (LaTeX humanization + audio optimization).
"""

import logging
import time
from pathlib import Path

import tiktoken

from ..llm.agents import text_agent
from ..utils.formatting import humanize_citation_key
from ._common import (
    DEFAULT_VOICE_ID,
    chunk_text,
    clean_markdown_for_tts,
    combine_audio_with_section_pauses,
    extract_acronyms,
    filter_metadata,
    generate_bookend_audio,
    split_transcript_by_sections,
    text_to_speech,
)

logger = logging.getLogger(__name__)


def generate_reading_audio(
    full_content: str,
    output_path: Path,
    elevenlabs_api_key: str,
    voice_id: str | None = None,
    model: str = "openai:gpt-5-mini",
    citation_key: str | None = None,
    speed: float = 1.0,
) -> str:
    """Generate complete audio narration of a document.

    Uses two-pass LLM processing: (1) LaTeX humanization, (2) audio
    optimization. Audio chunks are limited to 2000 chars for quality.
    Sections are separated by real silence and bookended with citation
    key announcements.

    Args:
        full_content: The full document content.
        output_path: Path for the output MP3 file.
        elevenlabs_api_key: ElevenLabs API key.
        voice_id: Voice ID (defaults to DEFAULT_VOICE_ID).
        model: pydantic-ai model string (e.g. ``"openai:gpt-5-mini"``).
        citation_key: Citation key to announce at the beginning.
        speed: Audio playback speed multiplier.

    Returns:
        Filename of the generated audio file.
    """
    voice_id = voice_id or DEFAULT_VOICE_ID

    # Extract acronyms for injection into prompt
    acronym_map = extract_acronyms(full_content)
    acronym_instruction = ""
    if acronym_map:
        pairs = ", ".join(f"{a} = {f}" for a, f in acronym_map.items())
        acronym_instruction = f"\n\n8. Expand these acronyms on first use: {pairs}\n"

    system_prompt = (
        "You are converting a full document to audio format for reading aloud. "
        "The content has already been preprocessed to remove LaTeX notation. "
        "Follow these rules precisely:\n\n"
        "1. If there is a citation key, mention it at the beginning\n\n"
        "2. When an acronym appears, read it naturally with its full form, e.g. "
        "'the FSEOF algorithm, flux scanning based on enforced objective function' "
        "-- never add meta-commentary like 'on first use' or 'which stands for'\n\n"
        "3. When encountering a figure, insert ---SECTION_BREAK--- on its own line, "
        "then say 'Figure X' (using the figure number), then insert another "
        "---SECTION_BREAK--- on its own line, then read the figure description\n\n"
        "4. Between sections, insert ---SECTION_BREAK--- on its own line. Do NOT add "
        "any filler text, transitions, or commentary between sections -- just the marker. "
        "Never say the word 'pause' aloud or write [pause]\n\n"
        "5. Maintain academic tone but make it listenable\n\n"
        "6. Read all prose exactly as written - preserve the author's words and meaning. "
        "Do NOT add your own words, summaries, or transitions between sections\n\n"
        "7. Make the text flow naturally for listening, not reading\n"
        + acronym_instruction
    )

    # Filter metadata (affiliations, emails, dates, references) before processing
    user_content = filter_metadata(full_content)

    if citation_key:
        humanized_key = humanize_citation_key(citation_key)
        user_content = f"Citation: {humanized_key}\n\n{user_content}"

    # Pass 1: Humanize LaTeX notation
    logger.info("Humanizing LaTeX notation in content...")
    user_content = _humanize_latex(user_content, model)
    logger.info("LaTeX humanization complete")

    # Pass 2: Generate reading transcript
    enc = tiktoken.get_encoding("cl100k_base")
    tokens = enc.encode(user_content)
    max_chunk = 3000
    transcript_chunks: list[str] = []

    for start in range(0, len(tokens), max_chunk):
        chunk = enc.decode(tokens[start : start + max_chunk])

        try:
            result = text_agent.run_sync(
                chunk,
                instructions=system_prompt,
                model=model,
                model_settings={"max_tokens": 8000},
            )
            chunk_transcript = result.output.strip()
        except Exception as e:
            logger.warning(f"Error generating reading transcript: {e}")
            chunk_transcript = ""

        if not chunk_transcript:
            logger.error("Failed to generate reading transcript, using original")
            chunk_transcript = chunk

        transcript_chunks.append(chunk_transcript)

    full_transcript = "\n\n".join(transcript_chunks)

    # Save transcripts
    transcripts_dir = output_path.parent / "full_read"
    transcripts_dir.mkdir(parents=True, exist_ok=True)
    transcript_path = transcripts_dir / f"{output_path.stem}_transcript.md"
    with open(transcript_path, "w", encoding="utf-8") as f:
        f.write("# Full Reading Audio Transcript\n\n")
        if citation_key:
            f.write(f"**Citation Key:** {citation_key}\n\n")
        f.write(f"**Generated Transcript:**\n\n{full_transcript}\n")

    tts_transcript = clean_markdown_for_tts(full_transcript)

    cleaned_path = (
        transcripts_dir / f"{output_path.stem}_transcript_cleaned_markdown.md"
    )
    with open(cleaned_path, "w", encoding="utf-8") as f:
        f.write("Full Reading Audio Transcript (Cleaned for TTS)\n\n")
        if citation_key:
            f.write(f"Citation Key: {citation_key}\n\n")
        f.write(f"Generated Transcript:\n\n{tts_transcript}\n")

    # Generate bookends
    bookend_start = None
    bookend_end = None
    if citation_key:
        bookend_start = generate_bookend_audio(
            citation_key,
            "transcript",
            "start",
            output_path.parent,
            elevenlabs_api_key,
            voice_id,
            speed,
        )
        bookend_end = generate_bookend_audio(
            citation_key,
            "transcript",
            "end",
            output_path.parent,
            elevenlabs_api_key,
            voice_id,
            speed,
        )

    # Section-aware audio assembly
    sections_text = split_transcript_by_sections(tts_transcript)
    if not sections_text:
        sections_text = [tts_transcript]

    all_section_chunks: list[list[Path]] = []
    chunk_counter = 0

    for sec_idx, section in enumerate(sections_text):
        audio_chunks = chunk_text(section, max_chars=2000)
        section_paths: list[Path] = []

        for chunk in audio_chunks:
            prefix = (
                f"{citation_key}_{output_path.stem}"
                if citation_key
                else output_path.stem
            )
            chunk_path = output_path.parent / f"{prefix}_chunk{chunk_counter}.mp3"
            text_to_speech(chunk, voice_id, chunk_path, elevenlabs_api_key, speed)
            section_paths.append(chunk_path)
            chunk_counter += 1
            time.sleep(1)

        all_section_chunks.append(section_paths)

    combine_audio_with_section_pauses(
        all_section_chunks,
        output_path,
        bookend_start=bookend_start,
        bookend_end=bookend_end,
    )

    # Clean up chunk files
    for section_paths in all_section_chunks:
        for p in section_paths:
            p.unlink()

    return output_path.name


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------

_LATEX_SYSTEM_PROMPT = """You are a LaTeX-to-text converter for academic audio transcripts.

YOUR ONLY JOB: Convert ALL LaTeX notation to natural readable text.

CRITICAL RULES:
1. Convert EVERY LaTeX expression to spoken form
2. Remove ALL dollar signs ($), backslashes (\\), and curly braces ({})
3. NEVER output any LaTeX syntax in your response

CONVERSIONS (apply ALL of these):

Greek Letters (always convert):
- $\\alpha$ -> alpha, $\\beta$ -> beta, $\\gamma$ -> gamma
- $\\delta$ -> delta, $\\epsilon$ -> epsilon, $\\zeta$ -> zeta
- $\\eta$ -> eta, $\\theta$ -> theta, $\\iota$ -> iota
- $\\kappa$ -> kappa, $\\lambda$ -> lambda, $\\mu$ -> mu
- $\\nu$ -> nu, $\\xi$ -> xi, $\\pi$ -> pi
- $\\rho$ -> rho, $\\sigma$ -> sigma, $\\tau$ -> tau
- $\\upsilon$ -> upsilon, $\\phi$ -> phi, $\\chi$ -> chi
- $\\psi$ -> psi, $\\omega$ -> omega

Math Formatting (remove markup):
- $\\mathbf{a}$ -> a (remove bold)
- $\\mathit{x}$ -> x (remove italic)
- $S$ -> S (remove dollar signs from single letters)
- $x_i$ -> x sub i
- $x^2$ -> x squared
- $x^{-1}$ -> x to the negative 1
- $10^{-3}$ -> 10 to the negative 3

Fractions:
- $\\frac{1}{2}$ -> one half
- $\\frac{a}{b}$ -> a over b

Special Cases:
- $\\zeta \\upsilon \\mu \\iota$ -> zeta upsilon mu iota
- $a$ and $\\alpha$ -> a and alpha
- $\\mathbf{a}$ and $\\alpha$ -> a and alpha

DO NOT change any other text - only convert LaTeX. Preserve all prose exactly."""


def _humanize_latex(content: str, model: str) -> str:
    """Convert all LaTeX notation to natural readable text using LLM.

    Args:
        content: Content with LaTeX notation.
        model: pydantic-ai model string.

    Returns:
        Content with all LaTeX converted to natural language.
    """
    enc = tiktoken.get_encoding("cl100k_base")
    tokens = enc.encode(content)
    max_chunk = 8000
    humanized_chunks: list[str] = []

    for start in range(0, len(tokens), max_chunk):
        chunk = enc.decode(tokens[start : start + max_chunk])

        try:
            result = text_agent.run_sync(
                chunk,
                instructions=_LATEX_SYSTEM_PROMPT,
                model=model,
                model_settings={"max_tokens": 10000},
            )
            humanized_chunk = result.output.strip()
        except Exception as e:
            logger.warning(f"Error in LaTeX humanization: {e}")
            humanized_chunk = ""

        if not humanized_chunk:
            logger.error("LaTeX humanization failed, using original chunk")
            humanized_chunk = chunk

        humanized_chunks.append(humanized_chunk)

    return "\n\n".join(humanized_chunks)
