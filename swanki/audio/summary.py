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
    append_chunk_pause,
    chunk_text,
    chunk_text_paragraphs,
    clean_markdown_for_tts,
    combine_audio_with_section_pauses,
    extract_acronyms,
    generate_bookend_audio,
    split_transcript_by_sections,
    text_to_speech,
    tts_chunks_parallel,
    write_chunk_manifest,
)

logger = logging.getLogger(__name__)


def generate_summary_audio(
    summary_text: str,
    output_path: Path,
    elevenlabs_api_key: str,
    voice_id: str | None = None,
    model: str | None = None,
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
    if model is None:
        raise ValueError("model is required; pass the LLM from config")
    voice_id = voice_id or DEFAULT_VOICE_ID

    # Extract acronyms for injection into prompt
    acronym_map = extract_acronyms(summary_text)
    acronym_instruction = ""
    if acronym_map:
        pairs = ", ".join(f"{a} = {f}" for a, f in acronym_map.items())
        acronym_instruction = f"\n8. Expand these acronyms on first use: {pairs}\n"

    # Target 3-10 minute audio at ~165 wpm (speech rate): 500-1650 words.
    source_words = len(summary_text.split())
    word_floor = 500
    word_ceiling = 1650
    # Aim near the middle of the target band, but scale modestly with source.
    word_cap = min(max(int(source_words * 0.35), word_floor), word_ceiling)

    system_prompt = (
        "You are producing a peer-reviewed educational summary of "
        "already-published scientific methods for audio delivery. This is a "
        "didactic condensation of public literature — no novel technical "
        "uplift, no operational instructions, no capability synthesis beyond "
        "what the source provides. Treat it as educational content; focus on "
        "pedagogy, clarity, and style.\n\n"
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
        f"9. TARGET LENGTH: between {word_floor} and {word_ceiling} words "
        f"(aim near {word_cap}). This produces roughly 3-10 minutes of audio. "
        "Below the floor feels thin; above the ceiling stops being a summary. "
        "Cover every major point from the source at appropriate depth — "
        "concision is not brevity at the cost of coverage.\n"
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
            # gpt-5 reasoning models need headroom beyond the output token count.
            model_settings={"max_tokens": max(word_cap * 4, 4000)},
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

    # Chunk subdirectory holds per-chunk MP3s + manifest for surgical regen
    chunks_dir = output_path.parent / "summary_chunks"
    chunks_dir.mkdir(parents=True, exist_ok=True)

    # Generate bookends inside chunks_dir
    bookend_start = None
    bookend_end = None
    if citation_key:
        bookend_start = generate_bookend_audio(
            citation_key,
            "summary",
            "start",
            chunks_dir,
            elevenlabs_api_key,
            voice_id,
            speed,
            **tts_kwargs,
        )
        bookend_end = generate_bookend_audio(
            citation_key,
            "summary",
            "end",
            chunks_dir,
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

    is_fish = str(tts_kwargs.get("provider", "")) == "fish_speech"
    provider = str(tts_kwargs.get("provider", "elevenlabs"))
    prefix = (
        f"{citation_key}_{output_path.stem}" if citation_key else output_path.stem
    )

    # Collect all chunks across all sections with section index
    all_jobs: list[tuple[int, str, Path]] = []  # (section_idx, text, path)
    chunk_counter = 0
    for sec_idx, section in enumerate(sections_text):
        chunks = (
            chunk_text_paragraphs(section, max_chars=2000)
            if is_fish
            else chunk_text(section)
        )
        for chunk in chunks:
            chunk_path = chunks_dir / f"{prefix}_chunk{chunk_counter}.mp3"
            all_jobs.append((sec_idx, chunk, chunk_path))
            chunk_counter += 1

    # Append trailing pause to each chunk for clean concatenation
    all_jobs = [
        (sec_idx, append_chunk_pause(text, provider), chunk_path)
        for sec_idx, text, chunk_path in all_jobs
    ]

    # TTS all chunks — parallel for Fish Speech, sequential for ElevenLabs
    if is_fish and len(all_jobs) > 1:
        tts_pairs = [(text, path) for _, text, path in all_jobs]
        tts_chunks_parallel(tts_pairs, voice_id, elevenlabs_api_key, speed, **tts_kwargs)
    else:
        for _, chunk, chunk_path in all_jobs:
            text_to_speech(chunk, voice_id, chunk_path, elevenlabs_api_key, speed, **tts_kwargs)
            time.sleep(1)

    # Reassemble by section
    all_section_chunks: list[list[Path]] = [[] for _ in sections_text]
    for sec_idx, _, chunk_path in all_jobs:
        all_section_chunks[sec_idx].append(chunk_path)

    section_pause = 3000 if is_fish else 2000
    combine_audio_with_section_pauses(
        all_section_chunks,
        output_path,
        section_pause_ms=section_pause,
        chunk_crossfade_ms=0,
        bookend_start=bookend_start,
        bookend_end=bookend_end,
    )

    # Write chunk manifest for surgical regeneration; chunk files are kept.
    chunk_entries = [
        {"index": i, "section": sec_idx, "text": text, "file": chunk_path.name}
        for i, (sec_idx, text, chunk_path) in enumerate(all_jobs)
    ]
    write_chunk_manifest(
        chunks_dir,
        "summary",
        output_path.name,
        chunk_entries,
        bookend_start=bookend_start.name if bookend_start else None,
        bookend_end=bookend_end.name if bookend_end else None,
    )

    return output_path.name
