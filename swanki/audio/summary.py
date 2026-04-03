"""
swanki/audio/summary.py
[[swanki.audio.summary]]
https://github.com/Mjvolk3/Swanki/tree/main/swanki/audio/summary.py

Document summary narration with section pauses, bookend announcements, and acronym expansion.
"""

import logging
import time
from pathlib import Path

from ..llm.agents import text_agent
from ..utils.formatting import humanize_citation_key
from ._common import (
    DEFAULT_VOICE_ID,
    add_tts_pauses,
    chunk_text,
    clean_markdown_for_tts,
    combine_audio_with_section_pauses,
    extract_acronyms,
    generate_bookend_audio,
    split_transcript_by_sections,
    text_to_speech,
)

logger = logging.getLogger(__name__)


def generate_summary_audio(
    summary_text: str,
    output_path: Path,
    elevenlabs_api_key: str,
    voice_id: str | None = None,
    model: str = "openai:gpt-5-mini",
    citation_key: str | None = None,
    speed: float = 1.0,
    **tts_kwargs: object,
) -> str:
    """Generate narration-style audio for a document summary.

    Args:
        summary_text: The summary text to convert to audio.
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
    acronym_map = extract_acronyms(summary_text)
    acronym_instruction = ""
    if acronym_map:
        pairs = ", ".join(f"{a} = {f}" for a, f in acronym_map.items())
        acronym_instruction = f"\n8. Expand these acronyms on first use: {pairs}\n"

    system_prompt = (
        "You are converting a document summary to audio format. "
        "Follow these rules precisely:\n"
        "1. If there is a citation key, mention it at the beginning\n"
        "2. Speak in a clear, academic tone suitable for summarization\n"
        "3. Convert any math notation to spoken form\n"
        "4. Read acronyms naturally with their full form, e.g. 'the FSEOF algorithm, "
        "flux scanning based on enforced objective function' -- never add phrases like "
        "'on first use' or 'which stands for'\n"
        "5. Between main points, insert ---SECTION_BREAK--- on its own line. "
        "Use paragraph breaks to create natural pacing.\n"
        "6. NEVER write [pause], [Pause], 'Pause.', or any pause instruction. "
        "NEVER try to spell out words letter by letter. "
        "Pauses are handled automatically by paragraph structure.\n"
        "7. Keep the content informative but accessible\n"
        "8. Never include phrases like 'Summary:' or 'This document...'\n"
        "9. STRICT LENGTH LIMIT: Keep under 1200 words total. The audio must be "
        "under 10 minutes. Be concise — hit the key points and move on.\n"
        + acronym_instruction
    )

    user_content = summary_text
    if citation_key:
        humanized_key = humanize_citation_key(citation_key)
        user_content = f"Citation: {humanized_key}\n\n{summary_text}"

    try:
        result = text_agent.run_sync(
            user_content,
            instructions=system_prompt,
            model=model,
            model_settings={"max_tokens": 1200},
        )
        transcript = result.output.strip()
    except Exception as e:
        logger.error(f"Failed to generate summary transcript: {e}")
        transcript = ""

    if not transcript:
        logger.error("Empty transcript, using original text")
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
    tts_transcript = add_tts_pauses(
        clean_markdown_for_tts(transcript),
        provider=str(tts_kwargs.get("provider", "elevenlabs")),
    )

    cleaned_path = (
        transcripts_dir / f"{output_path.stem}_transcript_cleaned_markdown.md"
    )
    with open(cleaned_path, "w", encoding="utf-8") as f:
        f.write("Summary Audio Transcript (Cleaned for TTS)\n\n")
        if citation_key:
            f.write(f"Citation Key: {citation_key}\n\n")
        f.write(f"Generated Transcript:\n\n{tts_transcript}\n")

    # Generate bookends
    bookend_start = None
    bookend_end = None
    if citation_key:
        bookend_start = generate_bookend_audio(
            citation_key,
            "summary",
            "start",
            output_path.parent,
            elevenlabs_api_key,
            voice_id,
            speed,
            **tts_kwargs,
        )
        bookend_end = generate_bookend_audio(
            citation_key,
            "summary",
            "end",
            output_path.parent,
            elevenlabs_api_key,
            voice_id,
            speed,
            **tts_kwargs,
        )

    # Section-aware audio assembly
    sections_text = split_transcript_by_sections(tts_transcript)
    if not sections_text:
        sections_text = [tts_transcript]

    if not sections_text or not any(s.strip() for s in sections_text):
        logger.error(
            f"No sections generated from transcript. Transcript length: {len(transcript)}"
        )
        return output_path.name

    all_section_chunks: list[list[Path]] = []
    chunk_counter = 0

    for section in sections_text:
        chunks = chunk_text(section)
        section_paths: list[Path] = []

        for chunk in chunks:
            prefix = (
                f"{citation_key}_{output_path.stem}"
                if citation_key
                else output_path.stem
            )
            chunk_path = output_path.parent / f"{prefix}_chunk{chunk_counter}.mp3"
            text_to_speech(chunk, voice_id, chunk_path, elevenlabs_api_key, speed, **tts_kwargs)
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

    # Clean up chunk and bookend files
    for section_paths in all_section_chunks:
        for p in section_paths:
            p.unlink()
    if bookend_start and bookend_start.exists():
        bookend_start.unlink()
    if bookend_end and bookend_end.exists():
        bookend_end.unlink()

    return output_path.name
