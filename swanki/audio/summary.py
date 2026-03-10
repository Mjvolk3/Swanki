"""
swanki/audio/summary.py
[[swanki.audio.summary]]
https://github.com/Mjvolk3/Swanki/tree/main/swanki/audio/summary.py

Document summary narration with citation announcements and SSML pauses.
"""

import logging
import time
from pathlib import Path

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


def generate_summary_audio(
    summary_text: str,
    output_path: Path,
    openai_client: OpenAI,
    elevenlabs_api_key: str,
    voice_id: str | None = None,
    model: str = "gpt-5-mini",
    citation_key: str | None = None,
    speed: float = 1.0,
) -> str:
    """Generate narration-style audio for a document summary.

    Args:
        summary_text: The summary text to convert to audio.
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
        "You are converting a document summary to audio format. "
        "Follow these rules precisely:\n"
        "1. If there is a citation key, mention it at the beginning\n"
        "2. Speak in a clear, academic tone suitable for summarization\n"
        "3. Convert any math notation to spoken form\n"
        "4. Read acronyms naturally with their full form, e.g. 'the FSEOF algorithm, "
        "flux scanning based on enforced objective function' -- never add phrases like "
        "'on first use' or 'which stands for'\n"
        '5. To add pauses between main points, insert a <break time="1.0s" /> tag '
        "(up to 3s) -- never say the word 'pause' aloud or write [pause]\n"
        "6. Keep the content informative but accessible\n"
        "7. Never include phrases like 'Summary:' or 'This document...'\n"
    )

    user_content = summary_text
    if citation_key:
        humanized_key = humanize_citation_key(citation_key)
        user_content = f"Citation: {humanized_key}\n\n{summary_text}"

    transcript = None
    max_retries = 3

    for attempt in range(max_retries):
        try:
            response = openai_client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_content},
                ],
                max_completion_tokens=1500,
            )

            if (
                response.choices
                and len(response.choices) > 0
                and response.choices[0].message.content
            ):
                transcript = response.choices[0].message.content.strip()
                if transcript:
                    break
                else:
                    logger.warning(
                        f"Attempt {attempt + 1}: GPT-5 returned empty summary transcript"
                    )
            else:
                logger.warning(
                    f"Attempt {attempt + 1}: GPT-5 returned malformed response for summary"
                )

        except Exception as e:
            logger.warning(
                f"Attempt {attempt + 1}: Error generating summary transcript: {e}"
            )

        if attempt < max_retries - 1:
            time.sleep(2**attempt)

    if not transcript:
        logger.error(
            f"Failed to generate transcript after {max_retries} attempts, using original text"
        )
        transcript = user_content

    # Save transcript with markdown for human reading/editing
    transcripts_dir = output_path.parent / "summary_transcript"
    transcripts_dir.mkdir(parents=True, exist_ok=True)
    transcript_path = transcripts_dir / f"{output_path.stem}_transcript.md"
    with open(transcript_path, "w", encoding="utf-8") as f:
        f.write("# Summary Audio Transcript\n\n")
        if citation_key:
            f.write(f"**Citation Key:** {citation_key}\n\n")
        f.write(f"**Generated Transcript:**\n\n{transcript}\n")

    # Create TTS-clean version
    tts_transcript = clean_markdown_for_tts(transcript)

    cleaned_path = (
        transcripts_dir / f"{output_path.stem}_transcript_cleaned_markdown.md"
    )
    with open(cleaned_path, "w", encoding="utf-8") as f:
        f.write("Summary Audio Transcript (Cleaned for TTS)\n\n")
        if citation_key:
            f.write(f"Citation Key: {citation_key}\n\n")
        f.write(f"Generated Transcript:\n\n{tts_transcript}\n")

    # Generate audio
    chunks = chunk_text(tts_transcript)

    if not chunks:
        logger.error(
            f"No chunks generated from transcript. Transcript length: {len(transcript)}"
        )
        logger.debug(f"Transcript content: {transcript[:200]}...")
        return output_path.name

    if len(chunks) == 1:
        text_to_speech(chunks[0], voice_id, output_path, elevenlabs_api_key, speed)
    else:
        chunk_paths: list[Path] = []
        for i, chunk in enumerate(chunks):
            prefix = (
                f"{citation_key}_{output_path.stem}"
                if citation_key
                else output_path.stem
            )
            chunk_path = output_path.parent / f"{prefix}_chunk{i}.mp3"
            text_to_speech(chunk, voice_id, chunk_path, elevenlabs_api_key, speed)
            chunk_paths.append(chunk_path)
            time.sleep(1)

        combine_audio(chunk_paths, output_path)
        for p in chunk_paths:
            p.unlink()

    return output_path.name
