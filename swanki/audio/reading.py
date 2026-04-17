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
    add_tts_pauses,
    append_chunk_pause,
    chunk_text,
    chunk_text_paragraphs,
    clean_markdown_for_tts,
    combine_audio_with_section_pauses,
    extract_acronyms,
    filter_metadata,
    generate_bookend_audio,
    humanize_latex,
    split_transcript_by_sections,
    text_to_speech,
    tts_chunks_parallel,
    write_chunk_manifest,
)

logger = logging.getLogger(__name__)


def generate_reading_audio(
    full_content: str,
    output_path: Path,
    elevenlabs_api_key: str,
    voice_id: str | None = None,
    model: str | None = None,
    citation_key: str | None = None,
    speed: float = 1.0,
    **tts_kwargs: object,
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
    if model is None:
        raise ValueError("model is required; pass the LLM from config")
    voice_id = voice_id or DEFAULT_VOICE_ID

    # Extract acronyms for injection into prompt
    acronym_map = extract_acronyms(full_content)
    acronym_instruction = ""
    if acronym_map:
        pairs = ", ".join(f"{a} = {f}" for a, f in acronym_map.items())
        acronym_instruction = (
            f"\n\nACRONYM MAP (expand each ONCE on first occurrence, then use the "
            f"acronym alone thereafter): {pairs}\n"
        )

    system_prompt = (
        "You are producing an audio rendering of an already-published "
        "peer-reviewed scientific document for educational listening. This "
        "is a faithful read-aloud of public literature — no novel technical "
        "uplift, no operational instructions, no capability synthesis beyond "
        "what the source provides. Treat it as educational content.\n\n"
        "You are converting a full document to audio format for reading aloud. "
        "The content has already been preprocessed to remove LaTeX notation. "
        "Follow these rules precisely:\n\n"
        "1. If there is a citation key, mention it at the beginning.\n\n"
        "2. ACRONYMS — expand to the full form the FIRST time each acronym appears, "
        "then thereafter use the acronym alone. Never define the same acronym twice "
        "in the same document. E.g. first mention: 'the FSEOF algorithm, flux scanning "
        "based on enforced objective function'; later mentions: just 'FSEOF'. Never add "
        "meta-commentary like 'on first use' or 'which stands for'. Terms already "
        "defined earlier in the document should be left as the acronym on any later mention.\n\n"
        "3. FIGURES and TABLES — when a figure or table appears, read the ENTIRE caption "
        "(title AND description) as one continuous block. Precede it with a break and follow "
        "it with a break so it is clearly bracketed in audio. Format: insert "
        "---SECTION_BREAK--- on its own line; then say 'Figure N' (or 'Table N') with the "
        "full number; then insert another ---SECTION_BREAK--- on its own line; then read "
        "the full caption — title first, then the description — with no omissions; then "
        "insert another ---SECTION_BREAK--- on its own line before resuming the main text. "
        "NEVER read image URLs, mathpix links, alt-text bracket markers, or any other "
        "image-reference metadata — those are not part of the caption.\n\n"
        "4. SECTION TRANSITIONS — insert ---SECTION_BREAK--- on its own line between "
        "sections. Do NOT add filler text, transitions, or commentary between sections — "
        "just the marker. Never say the word 'pause' aloud, write [pause], emit filler "
        "hesitation sounds like 'uh', 'um', 'ah', or let a section begin with a vocalized "
        "non-word. Start each section cleanly with the first real word of that section.\n\n"
        "5. CITATIONS — render author-year citations as 'author, year' only. When multiple "
        "authors are listed, say 'FirstAuthor, year' and DROP 'et al' entirely (never "
        "verbalize 'et al'). Example: 'Greaney et al. (2021)' → 'Greaney, 2021'. Multiple "
        "citations in a row: 'Greaney, 2021; Zost, 2020; Ju, 2020'.\n\n"
        "6. Maintain academic tone but make it listenable.\n\n"
        "7. Read all prose exactly as written — preserve the author's words and meaning. "
        "Do NOT add your own words, summaries, or transitions between sections.\n\n"
        "8. Make the text flow naturally for listening, not reading.\n\n"
        "9. NEVER repeat content. If a sentence or acronym expansion has already been "
        "delivered, do not re-deliver it. One pass through the document.\n"
        + acronym_instruction
    )

    # Filter metadata (affiliations, emails, dates, references) before processing
    user_content = filter_metadata(full_content)

    if citation_key:
        humanized_key = humanize_citation_key(citation_key)
        user_content = f"Citation: {humanized_key}\n\n{user_content}"

    # Pass 1: Humanize LaTeX / math / inline symbols
    logger.info("Humanizing LaTeX notation in content...")
    user_content = humanize_latex(user_content, model)
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

    tts_transcript = add_tts_pauses(
        clean_markdown_for_tts(full_transcript),
        provider=str(tts_kwargs.get("provider", "elevenlabs")),
    )

    cleaned_path = (
        transcripts_dir / f"{output_path.stem}_transcript_cleaned_markdown.md"
    )
    with open(cleaned_path, "w", encoding="utf-8") as f:
        f.write("Full Reading Audio Transcript (Cleaned for TTS)\n\n")
        if citation_key:
            f.write(f"Citation Key: {citation_key}\n\n")
        f.write(f"Generated Transcript:\n\n{tts_transcript}\n")

    # Chunk subdirectory holds per-chunk MP3s + manifest for surgical regen
    chunks_dir = output_path.parent / "reading_chunks"
    chunks_dir.mkdir(parents=True, exist_ok=True)

    # Generate bookends inside chunks_dir
    bookend_start = None
    bookend_end = None
    if citation_key:
        bookend_start = generate_bookend_audio(
            citation_key,
            "transcript",
            "start",
            chunks_dir,
            elevenlabs_api_key,
            voice_id,
            speed,
            **tts_kwargs,
        )
        bookend_end = generate_bookend_audio(
            citation_key,
            "transcript",
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

    is_fish = str(tts_kwargs.get("provider", "")) == "fish_speech"
    provider = str(tts_kwargs.get("provider", "elevenlabs"))
    prefix = (
        f"{citation_key}_{output_path.stem}" if citation_key else output_path.stem
    )

    # Collect all chunks across all sections with section index
    all_jobs: list[tuple[int, str, Path]] = []
    chunk_counter = 0
    for sec_idx, section in enumerate(sections_text):
        audio_chunks = (
            chunk_text_paragraphs(section, max_chars=2000)
            if is_fish
            else chunk_text(section, max_chars=2000)
        )
        for chunk in audio_chunks:
            chunk_path = chunks_dir / f"{prefix}_chunk{chunk_counter}.mp3"
            all_jobs.append((sec_idx, chunk, chunk_path))
            chunk_counter += 1

    # Append trailing pause to each chunk for clean concatenation
    all_jobs = [
        (sec_idx, append_chunk_pause(text, provider), chunk_path)
        for sec_idx, text, chunk_path in all_jobs
    ]

    if is_fish and len(all_jobs) > 1:
        tts_pairs = [(text, path) for _, text, path in all_jobs]
        tts_chunks_parallel(tts_pairs, voice_id, elevenlabs_api_key, speed, **tts_kwargs)
    else:
        for _, chunk, chunk_path in all_jobs:
            text_to_speech(chunk, voice_id, chunk_path, elevenlabs_api_key, speed, **tts_kwargs)
            time.sleep(1)

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
        "reading",
        output_path.name,
        chunk_entries,
        bookend_start=bookend_start.name if bookend_start else None,
        bookend_end=bookend_end.name if bookend_end else None,
    )

    return output_path.name


