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
from openai import OpenAI

from ..utils.formatting import humanize_citation_key
from ._common import (
    DEFAULT_VOICE_ID,
    chunk_text,
    clean_markdown_for_tts,
    combine_audio,
    text_to_speech,
)

logger = logging.getLogger(__name__)


def generate_reading_audio(
    full_content: str,
    output_path: Path,
    openai_client: OpenAI,
    elevenlabs_api_key: str,
    voice_id: str | None = None,
    model: str = "gpt-5-mini",
    citation_key: str | None = None,
    speed: float = 1.0,
) -> str:
    """Generate complete audio narration of a document.

    Uses two-pass LLM processing: (1) LaTeX humanization, (2) audio
    optimization. Audio chunks are limited to 2000 chars for quality.

    Args:
        full_content: The full document content.
        output_path: Path for the output MP3 file.
        openai_client: OpenAI client for transcript generation.
        elevenlabs_api_key: ElevenLabs API key.
        voice_id: Voice ID (defaults to DEFAULT_VOICE_ID).
        model: OpenAI model to use.
        citation_key: Citation key to announce at the beginning.
        speed: Audio playback speed multiplier.

    Returns:
        Filename of the generated audio file.
    """
    voice_id = voice_id or DEFAULT_VOICE_ID

    system_prompt = (
        "You are converting a full document to audio format for reading aloud. "
        "The content has already been preprocessed to remove LaTeX notation. "
        "Follow these rules precisely:\n\n"
        "1. If there is a citation key, mention it at the beginning\n\n"
        "2. When an acronym appears, read it naturally with its full form, e.g. "
        "'the FSEOF algorithm, flux scanning based on enforced objective function' "
        "-- never add meta-commentary like 'on first use' or 'which stands for'\n\n"
        "3. Skip any remaining image references, URLs, or figure/table blocks entirely\n\n"
        '4. Between sections, insert a <break time="2.0s" /> tag for a pause, then '
        "start with a brief transition -- never say the word 'pause' aloud or write [pause]\n\n"
        "5. Maintain academic tone but make it listenable\n\n"
        "6. Read all prose exactly as written - preserve the author's words and meaning\n\n"
        "7. Make the text flow naturally for listening, not reading\n"
    )

    user_content = full_content
    if citation_key:
        humanized_key = humanize_citation_key(citation_key)
        user_content = f"Citation: {humanized_key}\n\n{full_content}"

    # Pass 1: Humanize LaTeX notation
    logger.info("Humanizing LaTeX notation in content...")
    user_content = _humanize_latex(user_content, openai_client, model)
    logger.info("LaTeX humanization complete")

    # Pass 2: Generate reading transcript
    enc = tiktoken.get_encoding("cl100k_base")
    tokens = enc.encode(user_content)
    max_chunk = 3000
    transcript_chunks: list[str] = []

    for start in range(0, len(tokens), max_chunk):
        chunk = enc.decode(tokens[start : start + max_chunk])

        chunk_transcript = None
        max_retries = 3

        for attempt in range(max_retries):
            try:
                response = openai_client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": chunk},
                    ],
                    max_completion_tokens=8000,
                )

                if (
                    response.choices
                    and len(response.choices) > 0
                    and response.choices[0].message.content
                ):
                    chunk_transcript = response.choices[0].message.content.strip()
                    if chunk_transcript:
                        break
                    else:
                        logger.warning(
                            f"Attempt {attempt + 1}: GPT-5 returned empty reading transcript for chunk"
                        )
                else:
                    logger.warning(
                        f"Attempt {attempt + 1}: GPT-5 returned malformed response for reading. "
                        f"Response details: choices={len(response.choices) if response.choices else 0}, "
                        f"has_content={bool(response.choices and response.choices[0].message.content) if response.choices else False}, "
                        f"finish_reason={response.choices[0].finish_reason if response.choices and len(response.choices) > 0 else 'N/A'}"
                    )

            except Exception as e:
                logger.warning(
                    f"Attempt {attempt + 1}: Error generating reading transcript: {e}"
                )

            if attempt < max_retries - 1:
                time.sleep(2**attempt)

        if not chunk_transcript:
            logger.error(
                f"Failed to generate reading transcript after {max_retries} attempts, using original"
            )
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

    # Generate audio
    audio_chunks = chunk_text(tts_transcript, max_chars=2000)
    chunk_paths: list[Path] = []

    for i, chunk in enumerate(audio_chunks):
        prefix = (
            f"{citation_key}_{output_path.stem}" if citation_key else output_path.stem
        )
        chunk_path = output_path.parent / f"{prefix}_chunk{i}.mp3"
        text_to_speech(chunk, voice_id, chunk_path, elevenlabs_api_key, speed)
        chunk_paths.append(chunk_path)
        time.sleep(1)

    combine_audio(chunk_paths, output_path)

    for p in chunk_paths:
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


def _humanize_latex(content: str, openai_client: OpenAI, model: str) -> str:
    """Convert all LaTeX notation to natural readable text using LLM.

    Args:
        content: Content with LaTeX notation.
        openai_client: OpenAI client for conversion.
        model: OpenAI model to use.

    Returns:
        Content with all LaTeX converted to natural language.
    """
    enc = tiktoken.get_encoding("cl100k_base")
    tokens = enc.encode(content)
    max_chunk = 8000
    humanized_chunks: list[str] = []

    for start in range(0, len(tokens), max_chunk):
        chunk = enc.decode(tokens[start : start + max_chunk])

        max_retries = 3
        humanized_chunk = None

        for attempt in range(max_retries):
            try:
                response = openai_client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": _LATEX_SYSTEM_PROMPT},
                        {"role": "user", "content": chunk},
                    ],
                    max_completion_tokens=10000,
                )

                if (
                    response.choices
                    and len(response.choices) > 0
                    and response.choices[0].message.content
                ):
                    humanized_chunk = response.choices[0].message.content.strip()
                    if humanized_chunk:
                        break
                    else:
                        logger.warning(
                            f"Attempt {attempt + 1}: LaTeX humanization returned empty"
                        )
                else:
                    logger.warning(
                        f"Attempt {attempt + 1}: LaTeX humanization returned malformed response"
                    )

            except Exception as e:
                logger.warning(
                    f"Attempt {attempt + 1}: Error in LaTeX humanization: {e}"
                )

            if attempt < max_retries - 1:
                time.sleep(2**attempt)

        if not humanized_chunk:
            logger.error(
                f"LaTeX humanization failed after {max_retries} attempts, using original chunk"
            )
            humanized_chunk = chunk

        humanized_chunks.append(humanized_chunk)

    return "\n\n".join(humanized_chunks)
