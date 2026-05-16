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
    apply_pronunciation_overrides,
    chunk_text,
    chunk_text_paragraphs,
    clean_markdown_for_tts,
    combine_audio_with_section_pauses,
    expand_acronyms_for_tts,
    extract_acronyms,
    generate_bookend_audio,
    split_transcript_by_sections,
    strip_chapter_filename_slug,
    strip_forbidden_fish_tags,
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

    # Target 4-5 minute audio at ~130 wpm (fish_speech@1.1x): 500-700 words.
    # Constant regardless of source length so summaries feel consistent.
    word_floor = 500
    word_ceiling = 700
    word_cap = 600

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
        f"(aim near {word_cap}). This produces roughly 4-5 minutes of audio "
        "and should stay constant regardless of source length. "
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

    # Pre-TTS scrubber pipeline (mirrors lecture.py flow). Order matters:
    # clean markdown first so scrubbers operate on prose, slug-strip before
    # acronym pass so uppercase chunks of a leaked content_key aren't misread,
    # pronunciation overrides AFTER the generic acronym rewrite so per-paper
    # tokens win, forbidden-tag scrubber LAST among deterministic stage so
    # any LLM-emitted [sigh] gets stripped before add_tts_pauses injects the
    # legitimate pause tags it needs to.
    is_fish_for_prep = str(tts_kwargs.get("provider", "")) == "fish_speech"
    _prep_raw = tts_kwargs.get("preprocessor")
    prep_cfg: dict = _prep_raw if isinstance(_prep_raw, dict) else {}
    cleaned = clean_markdown_for_tts(transcript)
    cleaned = strip_chapter_filename_slug(cleaned)
    if is_fish_for_prep and prep_cfg.get("acronym_letter_by_letter", True):
        allowlist = set(prep_cfg.get("acronym_allowlist", []))
        cleaned = expand_acronyms_for_tts(cleaned, allowlist=allowlist)
    pronunciations = prep_cfg.get("pronunciations", {}) or {}
    if pronunciations:
        cleaned = apply_pronunciation_overrides(cleaned, pronunciations)
    if is_fish_for_prep and prep_cfg.get("strip_forbidden_tags", True):
        cleaned = strip_forbidden_fish_tags(cleaned)
    tts_transcript = add_tts_pauses(
        cleaned,
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

    # YAML-driven chunking (models.tts.chunking.max_chars) overrides the
    # legacy hardcoded cap; fish_speech*.yaml ships max_chars=700 to keep
    # Fish quality from decaying past ~700 chars per chunk (Theme 4 from
    # the Hamming bookmark plan).
    _chunk_raw = tts_kwargs.get("chunking")
    chunking_cfg: dict = _chunk_raw if isinstance(_chunk_raw, dict) else {}
    chunk_max_chars = int(chunking_cfg.get("max_chars", 2000 if is_fish else 4500))

    # Collect all chunks across all sections with section index. Each job
    # carries (section_idx, text, path, boundary_type) where boundary_type
    # describes the gap PRECEDING this chunk in source-text terms
    # ("paragraph" | "sentence"). chunk_text() (non-fish) doesn't expose
    # boundaries; we default those to "paragraph".
    all_jobs: list[tuple[int, str, Path, str]] = []
    chunk_counter = 0
    for sec_idx, section in enumerate(sections_text):
        if is_fish:
            audio_chunks = chunk_text_paragraphs(section, max_chars=chunk_max_chars)
        else:
            audio_chunks = [(c, "paragraph") for c in chunk_text(section)]
        for chunk_text_, boundary in audio_chunks:
            chunk_path = chunks_dir / f"{prefix}_chunk{chunk_counter}.mp3"
            all_jobs.append((sec_idx, chunk_text_, chunk_path, boundary))
            chunk_counter += 1

    # Append trailing pause to each chunk for clean concatenation
    all_jobs = [
        (sec_idx, append_chunk_pause(text, provider), chunk_path, boundary)
        for sec_idx, text, chunk_path, boundary in all_jobs
    ]

    # TTS all chunks — parallel for Fish Speech, sequential for ElevenLabs
    if is_fish and len(all_jobs) > 1:
        tts_pairs = [(text, path) for _, text, path, _ in all_jobs]
        tts_chunks_parallel(tts_pairs, voice_id, elevenlabs_api_key, speed, **tts_kwargs)
    else:
        for _, chunk, chunk_path, _b in all_jobs:
            text_to_speech(chunk, voice_id, chunk_path, elevenlabs_api_key, speed, **tts_kwargs)
            time.sleep(1)

    # Reassemble by section
    all_section_chunks: list[list[Path]] = [[] for _ in sections_text]
    all_section_boundaries: list[list[str]] = [[] for _ in sections_text]
    for sec_idx, _, chunk_path, boundary in all_jobs:
        all_section_chunks[sec_idx].append(chunk_path)
        all_section_boundaries[sec_idx].append(boundary)

    # YAML-driven postprocessor knobs (models.tts.postprocessor.*) supply
    # the boundary-fix bundle (gain match, inter-chunk silence, tail trim,
    # crossfade). Fall-through defaults preserve prior behavior when the
    # sub-tree is absent. Summary previously had no boundary fixes — now
    # consistent with lecture for fish providers.
    _post_raw = tts_kwargs.get("postprocessor")
    post_cfg: dict = _post_raw if isinstance(_post_raw, dict) else {}
    section_pause = int(post_cfg.get("section_pause_ms", 3000 if is_fish else 2000))
    chunk_tail_trim_ms = int(post_cfg.get("chunk_tail_trim_ms", 250 if is_fish else 0))
    chunk_pause_ms = int(post_cfg.get("chunk_pause_ms", 700 if is_fish else 0))
    chunk_crossfade_ms = int(post_cfg.get("chunk_crossfade_ms", 50 if is_fish else 0))
    gain_match = post_cfg.get("gain_match_target_dbfs", -25.0 if is_fish else None)
    chunk_pause_map_default = (
        {"paragraph": 1100, "sentence": 500} if is_fish else None
    )
    chunk_pause_ms_by_boundary = post_cfg.get(
        "chunk_pause_ms_by_boundary", chunk_pause_map_default
    )
    combine_audio_with_section_pauses(
        all_section_chunks,
        output_path,
        section_pause_ms=section_pause,
        chunk_crossfade_ms=chunk_crossfade_ms,
        bookend_start=bookend_start,
        bookend_end=bookend_end,
        chunk_tail_trim_ms=chunk_tail_trim_ms,
        chunk_pause_ms=chunk_pause_ms,
        gain_match_target_dbfs=gain_match,
        chunk_boundaries=all_section_boundaries if chunk_pause_ms_by_boundary else None,
        chunk_pause_ms_by_boundary=chunk_pause_ms_by_boundary,
    )

    # Write chunk manifest for surgical regeneration; chunk files are kept.
    chunk_entries = [
        {
            "index": i,
            "section": sec_idx,
            "text": text,
            "file": chunk_path.name,
            "boundary": boundary,
        }
        for i, (sec_idx, text, chunk_path, boundary) in enumerate(all_jobs)
    ]
    write_chunk_manifest(
        chunks_dir,
        "summary",
        output_path.name,
        chunk_entries,
        bookend_start=bookend_start.name if bookend_start else None,
        bookend_end=bookend_end.name if bookend_end else None,
        postprocessor={
            "section_pause_ms": section_pause,
            "chunk_pause_ms": chunk_pause_ms,
            "chunk_tail_trim_ms": chunk_tail_trim_ms,
            "chunk_crossfade_ms": chunk_crossfade_ms,
            "gain_match_target_dbfs": gain_match,
            "chunk_pause_ms_by_boundary": chunk_pause_ms_by_boundary,
        },
    )

    return output_path.name
