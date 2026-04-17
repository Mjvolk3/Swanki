"""
swanki/audio/lecture.py
[[swanki.audio.lecture]]
https://github.com/Mjvolk3/Swanki/tree/main/swanki/audio/lecture.py

Educational lecture generation with semantic chunking, per-section validation,
and iterative self-refinement.
"""

import logging
import re
import time
from pathlib import Path
from string import Template

import tiktoken

from ..llm.agents import lecture_critic_agent, text_agent
from ..models.cards import LectureTranscriptFeedback
from ..utils.formatting import humanize_citation_key
from ._common import (
    DEFAULT_VOICE_ID,
    LECTURE_TTS_MODEL,
    add_tts_pauses,
    append_chunk_pause,
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


def critique_transcript_chunks(
    transcript: str,
    critique_prompt: str,
    model: str = "openai:gpt-5",
    chunk_size: int = 8000,
    max_chunks: int = 5,
) -> LectureTranscriptFeedback:
    """Critique transcript by sampling multiple chunks for comprehensive feedback.

    Args:
        transcript: Full transcript to critique.
        critique_prompt: Prompt template with {transcript} and {position} placeholders.
        model: pydantic-ai model string.
        chunk_size: Characters per chunk.
        max_chunks: Maximum chunks to sample.

    Returns:
        Combined feedback with done=False if any chunk has issues.
    """
    chunks = []
    for i in range(0, len(transcript), chunk_size):
        if len(chunks) >= max_chunks:
            break
        chunk = transcript[i : i + chunk_size]
        chunks.append((i, chunk))

    logger.info(f"Critiquing transcript in {len(chunks)} chunks...")

    all_feedback: list[str] = []
    all_done = True

    for start_pos, chunk in chunks:
        chunk_escaped = chunk.replace("{", "{{").replace("}", "}}")

        try:
            result = lecture_critic_agent.run_sync(
                critique_prompt.format(
                    transcript=chunk_escaped,
                    position=f"Characters {start_pos}-{start_pos + len(chunk)}",
                ),
                instructions="You are an expert educational content reviewer.",
                model=model,
            )
            critique = result.output

            if not critique.done:
                all_done = False
            all_feedback.extend(critique.feedback)

        except Exception as e:
            logger.warning(f"Error critiquing chunk at {start_pos}: {e}")
            all_done = False
            all_feedback.append(
                f"Chars {start_pos}-{start_pos + len(chunk)}: Failed to critique (error: {e!s})"
            )

    return LectureTranscriptFeedback(
        feedback=all_feedback,
        done=all_done,
        word_count=0,
        meets_length_target=all_done,
    )


def chunk_by_headers(
    content: str,
    max_tokens_per_chunk: int = 15000,
) -> list[tuple[str, str, int]]:
    """Chunk content by markdown headers, preserving semantic structure.

    Args:
        content: Markdown content to chunk.
        max_tokens_per_chunk: Maximum tokens per section before splitting.

    Returns:
        List of (section_title, section_content, token_count) tuples.
    """
    enc = tiktoken.get_encoding("cl100k_base")
    numbered_pattern = r"^(#{2,})\s+([0-9.]+)(?:\s*\\\\)?\s*(.*)$"
    unnumbered_pattern = r"^(#{2,})\s+([A-Z][A-Za-z\s,]+)$"

    chunks: list[tuple[str, str, int]] = []
    current_section: dict[str, str | int] = {
        "title": "",
        "content": "",
        "start_line": 0,
    }

    lines = content.split("\n")

    for line_idx, line in enumerate(lines):
        numbered = re.match(numbered_pattern, line, re.MULTILINE)
        unnumbered = (
            re.match(unnumbered_pattern, line, re.MULTILINE) if not numbered else None
        )
        match = numbered or unnumbered

        if match:
            if current_section["content"]:
                section_content = str(current_section["content"])
                token_count = len(enc.encode(section_content))

                if token_count > max_tokens_per_chunk:
                    subsections = _split_large_section(
                        section_content, max_tokens_per_chunk
                    )
                    for i, subsection in enumerate(subsections):
                        title = f"{current_section['title']} (part {i + 1})"
                        chunks.append((title, subsection, len(enc.encode(subsection))))
                else:
                    chunks.append(
                        (
                            str(current_section["title"]),
                            section_content,
                            token_count,
                        )
                    )

            if numbered:
                number = numbered.group(2)
                title = (
                    numbered.group(3).strip()
                    if numbered.group(3)
                    else f"Section {number}"
                )
                title = title or f"Section {number}"
            else:
                assert unnumbered is not None
                title = unnumbered.group(2).strip()

            current_section = {
                "title": title,
                "content": line + "\n",
                "start_line": line_idx,
            }
        else:
            current_section["content"] = str(current_section["content"]) + line + "\n"

    # Add final section
    if current_section["content"]:
        section_content = str(current_section["content"])
        token_count = len(enc.encode(section_content))
        if token_count > max_tokens_per_chunk:
            subsections = _split_large_section(section_content, max_tokens_per_chunk)
            for i, subsection in enumerate(subsections):
                title = f"{current_section['title']} (part {i + 1})"
                chunks.append((title, subsection, len(enc.encode(subsection))))
        else:
            chunks.append((str(current_section["title"]), section_content, token_count))

    return chunks


def generate_and_validate_chunk(
    content_chunk: str,
    section_title: str,
    previous_context: str,
    system_prompt: str,
    citation_key: str,
    model: str,
    max_retries: int = 2,
    si_reference_content: str | None = None,
) -> str:
    """Generate a section transcript with immediate self-criticism validation.

    Args:
        content_chunk: Section content to generate lecture from.
        section_title: Title of this section.
        previous_context: Context from previous section.
        system_prompt: System prompt with lecture instructions.
        citation_key: Humanized citation key.
        model: pydantic-ai model string.
        max_retries: Maximum retry attempts.
        si_reference_content: Relevant SI content for this section.

    Returns:
        Validated lecture transcript for this section.
    """
    critique_prompt = """Review this lecture transcript section for quality issues.

Check for:
1. Raw LaTeX (\\begin{{tabular}}, \\hline, $symbols$, etc.) - Should be converted to natural language
2. Author citations ((Author, 2020)) - Should be removed or replaced with "Research shows..."
3. References/Further Reading sections - Should be omitted
4. Lists (numbered or bulleted) - Should be converted to flowing narrative
5. Cross-references ("see Figure X", "Table Y") - Should be removed or integrated naturally
6. Conversational tone maintained throughout

Transcript to review:
{transcript}

If issues found, list them specifically. Set done=False if refinement needed, done=True if acceptable."""

    if si_reference_content:
        critique_prompt += """

SI BALANCE CHECK:
- At least 50% of the section must cover main paper content.
- At most 50% may be SI enrichment.
- If SI dominates, set done=False and si_balance=False with feedback:
  "SI content dominates this section — rebalance toward main paper."
"""

    chunk_transcript = ""

    for attempt in range(max_retries):
        if previous_context:
            user_message = (
                f"Continue your lecture on {citation_key}.\n\n"
                f"Previously, you covered:\n---\n{previous_context}\n---\n\n"
                f"Now present this section: {section_title}\n\n"
                "Maintain the same conversational style - no LaTeX, no citations, flowing narrative only.\n\n"
                f"Content:\n{content_chunk}"
            )
        else:
            user_message = (
                f"Begin your lecture on {citation_key}.\n\n"
                f"Present this section: {section_title}\n\n"
                f"Content:\n{content_chunk}"
            )

        if si_reference_content:
            user_message += (
                "\n\n---\nRELEVANT SUPPLEMENTARY INFORMATION (use to enrich your discussion, "
                "but keep the main paper as the primary focus):\n"
                f"{si_reference_content}"
            )

        max_completion_tokens = 10000

        try:
            gen_result = text_agent.run_sync(
                user_message,
                instructions=system_prompt,
                model=model,
                model_settings={"max_tokens": max_completion_tokens},
            )
            chunk_transcript = gen_result.output.strip()
        except Exception as e:
            logger.error(f"Section '{section_title}' generation failed: {e}")
            chunk_transcript = ""

        logger.info(
            f"Section '{section_title}' response: "
            f"content_length={len(chunk_transcript)}, "
            f"max_completion_tokens={max_completion_tokens}"
        )

        if not chunk_transcript:
            logger.error(f"Section '{section_title}' returned EMPTY content!")

        # Immediate critique
        try:
            chunk_escaped = chunk_transcript.replace("{", "{{").replace("}", "}}")

            critique_result = lecture_critic_agent.run_sync(
                critique_prompt.format(
                    transcript=chunk_escaped,
                ),
                instructions="You are an expert educational content reviewer.",
                model=model,
            )
            critique = critique_result.output

            if critique.done:
                logger.info(f"Section '{section_title}' passed validation")
                return chunk_transcript
            else:
                logger.warning(
                    f"Section '{section_title}' needs refinement (attempt {attempt + 1}): {critique.feedback}"
                )
                if attempt == max_retries - 1:
                    logger.warning(f"Accepting section after {max_retries} attempts")
                    return chunk_transcript

        except Exception as e:
            logger.warning(f"Critique failed for section '{section_title}': {e}")
            return chunk_transcript

    return chunk_transcript


def generate_lecture_audio(
    markdown_files: list[Path],
    image_summaries: list[str],
    output_path: Path,
    elevenlabs_api_key: str,
    voice_id: str | None = None,
    model: str = "openai:gpt-5-mini",
    citation_key: str | None = None,
    lecture_prompt_config: dict | None = None,
    speed: float = 1.0,
    si_start_page: int | None = None,
    paper_title: str | None = None,
    **tts_kwargs: object,
) -> str:
    """Generate an educational lecture from document content.

    Args:
        markdown_files: Cleaned markdown file paths in order.
        image_summaries: Image summary strings to embed.
        output_path: Path for the output MP3 file.
        elevenlabs_api_key: ElevenLabs API key.
        voice_id: Voice ID (defaults to DEFAULT_VOICE_ID).
        model: pydantic-ai model string (e.g. ``"openai:gpt-5-mini"``).
        citation_key: Citation key to include in lecture.
        lecture_prompt_config: Custom prompt config with 'lecture_system'
            and 'lecture_prefix' keys.
        speed: Audio playback speed multiplier.
        si_start_page: Page index where SI begins in markdown_files.
            When set, main paper and SI are processed separately.
        paper_title: Paper title for lecture bookend announcements.

    Returns:
        Filename of the generated audio file.
    """
    voice_id = voice_id or DEFAULT_VOICE_ID

    # Guard: si_start_page out of bounds
    if si_start_page is not None and si_start_page >= len(markdown_files):
        logger.warning(
            f"si_start_page={si_start_page} >= {len(markdown_files)} files, "
            "falling back to no-SI mode"
        )
        si_start_page = None

    # Split files into main and SI when boundary is known
    if si_start_page is not None:
        main_files = markdown_files[:si_start_page]
        si_files = markdown_files[si_start_page:]
        logger.info(f"SI split: {len(main_files)} main pages, {len(si_files)} SI pages")
    else:
        main_files = markdown_files
        si_files = []

    # Prepare content with embedded image summaries
    image_idx = 0

    def _embed_images(files: list[Path]) -> str:
        nonlocal image_idx
        result = ""
        for md_file in files:
            content = md_file.read_text()
            while "![" in content and image_idx < len(image_summaries):
                img_start = content.find("![")
                img_end = content.find(")", img_start)
                if img_end > img_start:
                    alt_start = content.find("[", img_start) + 1
                    alt_end = content.find("]", alt_start)
                    alt_text = content[alt_start:alt_end] if alt_end > alt_start else ""
                    summary = image_summaries[image_idx]
                    if alt_text:
                        integrated_summary = f"Looking at {alt_text.lower()}, we can see {summary[0].lower()}{summary[1:]}"
                    else:
                        integrated_summary = (
                            f"The visual here shows {summary[0].lower()}{summary[1:]}"
                        )
                    before = content[:img_start]
                    after = content[img_end + 1 :]
                    content = f"{before}{integrated_summary}{after}"
                    image_idx += 1
                else:
                    break
            result += content + "\n\n"
        return result

    main_content = _embed_images(main_files)
    si_content = _embed_images(si_files) if si_files else ""

    cleaned_content = main_content
    logger.info(f"Main content length: {len(main_content)} characters")
    if si_content:
        logger.info(f"SI content length: {len(si_content)} characters")

    # Extract acronyms for injection into prompt
    acronym_map = extract_acronyms(main_content)
    acronym_instruction = ""
    if acronym_map:
        pairs = ", ".join(f"{a} = {f}" for a, f in acronym_map.items())
        acronym_instruction = (
            f"\n\n9. ACRONYM EXPANSION: Expand these acronyms on first use: {pairs}"
        )

    # Get instructions
    if lecture_prompt_config:
        system_instructions = lecture_prompt_config.get("lecture_system", "")
        content_prefix = lecture_prompt_config.get("lecture_prefix", "")
        si_instructions = lecture_prompt_config.get("lecture_si_instructions", "")
    else:
        system_instructions = _DEFAULT_LECTURE_SYSTEM_PROMPT
        content_prefix = "Begin your lecture on"
        si_instructions = ""

    humanized_key = (
        humanize_citation_key(citation_key) if citation_key else "this academic work"
    )
    full_system_prompt = (
        f"{system_instructions}{acronym_instruction}\n\nCitation: {humanized_key}"
    )

    # Add Fish Speech inline tag instructions for richer prosody
    if str(tts_kwargs.get("provider", "")) == "fish_speech":
        full_system_prompt += f"\n\n{_FISH_SPEECH_TAG_INSTRUCTIONS}"

    # Append SI instructions when SI is present (either from _meta.json or inline)
    # (SI instructions added after classification below if methods/SI sections found)
    if si_start_page is not None:
        si_prompt = si_instructions or _DEFAULT_LECTURE_SI_INSTRUCTIONS
        full_system_prompt += f"\n\n{si_prompt}"

    # Chunk all content by semantic structure, then classify
    all_chunks = chunk_by_headers(cleaned_content, max_tokens_per_chunk=15000)

    si_index: dict[str, str] = {}

    # Classify sections into three buckets:
    # 1. Preamble (Authors, Highlights, etc.) → skip, no cascade
    # 2. Methods/SI (KEY RESOURCES, METHOD DETAILS, etc.) → enrichment + cascade
    #    Once a methods/SI header is seen, everything after is also methods/SI
    #    (subsections like "ODE", "DNA Replication" follow "METHOD DETAILS")
    # 3. Main content → drives the lecture structure
    main_chunks: list[tuple[str, str, int]] = []
    methods_si_chunks: list[tuple[str, str, int]] = []
    in_methods_si = False
    for title, content, tokens in all_chunks:
        stripped = title.strip()
        if _PREAMBLE_HEADERS.match(stripped):
            methods_si_chunks.append((title, content, tokens))
        elif _METHODS_SI_HEADERS.match(stripped):
            in_methods_si = True
            methods_si_chunks.append((title, content, tokens))
        elif in_methods_si:
            methods_si_chunks.append((title, content, tokens))
        else:
            main_chunks.append((title, content, tokens))

    if methods_si_chunks:
        logger.info(
            f"Classified {len(main_chunks)} main sections, "
            f"{len(methods_si_chunks)} methods/SI sections (available as enrichment)"
        )
        for title, _, tokens in methods_si_chunks:
            logger.info(f"  [enrichment] '{title}' ({tokens} tokens)")

        # Build SI index from inline methods/SI sections for enrichment
        # Only if no page-level SI index already exists from _meta.json
        methods_si_text = "\n\n".join(c for _, c, _ in methods_si_chunks)
        if not si_index:
            si_index = build_si_index(methods_si_text)
            # If build_si_index found no markers, index the whole pool as one entry
            if not si_index and methods_si_text.strip():
                si_index = {"methods_si_pool": methods_si_text}
                logger.info("Indexed methods/SI as single enrichment pool")

    # Build SI index from page-level split (if available and not already built)
    if not si_index and si_content:
        si_index = build_si_index(si_content)
    if si_index:
        logger.info(f"SI index: {len(si_index)} entries: {list(si_index.keys())}")

    # Inject SI enrichment instructions if we have enrichment material
    # (from either inline classification or page-level split)
    if si_index and si_start_page is None and methods_si_chunks:
        si_prompt = si_instructions or _DEFAULT_LECTURE_SI_INSTRUCTIONS
        full_system_prompt += f"\n\n{si_prompt}"

    semantic_chunks = main_chunks

    logger.info(f"Lecture will cover {len(semantic_chunks)} main sections")
    for i, (title, _, tokens) in enumerate(semantic_chunks):
        logger.info(f"  Section {i + 1}: '{title}' ({tokens} tokens)")

    transcript_chunks: list[str] = []
    max_retries = 3

    enc = tiktoken.get_encoding("cl100k_base")
    if len(semantic_chunks) == 1 and semantic_chunks[0][2] < 20000:
        # Single-pass for short documents
        logger.info("Using single-pass generation (short document)")

        section_title, section_content, _ = semantic_chunks[0]
        user_message = (
            f"{content_prefix}: {humanized_key}\n\nContent:\n{section_content}"
        )
        if si_content:
            user_message += (
                "\n\n---\nSUPPLEMENTARY INFORMATION (use to enrich, "
                "but keep main paper as primary focus):\n"
                f"{si_content[:3000]}"
            )

        try:
            gen_result = text_agent.run_sync(
                user_message,
                instructions=full_system_prompt,
                model=model,
                model_settings={"max_tokens": 10000},
            )
            lecture_transcript = gen_result.output.strip()
        except Exception as e:
            logger.error(f"Error generating lecture transcript: {e}")
            lecture_transcript = ""

        if not lecture_transcript:
            logger.error("Failed to generate lecture transcript, using original")
            lecture_transcript = section_content

        full_transcript = lecture_transcript
    else:
        # Multi-section generation
        logger.info("Using multi-section generation with per-section validation")
        accumulated_transcript = ""

        total_source_words = len(cleaned_content.split())
        cumulative_output_words = 0

        for section_idx, (section_title, section_content, _) in enumerate(
            semantic_chunks
        ):
            section_source_words = len(section_content.split())

            logger.info(
                f"Generating section {section_idx + 1}/{len(semantic_chunks)}: {section_title}"
            )
            logger.info(f"  Source: {section_source_words} words")

            previous_context = (
                _extract_context(accumulated_transcript, max_tokens=300)
                if section_idx > 0
                else ""
            )

            si_ref = (
                extract_relevant_si(section_content, si_index) if si_index else None
            )

            chunk_transcript = generate_and_validate_chunk(
                content_chunk=section_content,
                section_title=section_title,
                previous_context=previous_context,
                system_prompt=full_system_prompt,
                citation_key=humanized_key,
                model=model,
                max_retries=2,
                si_reference_content=si_ref,
            )

            section_actual_words = len(chunk_transcript.split())
            cumulative_output_words += section_actual_words

            logger.info(f"  Generated: {section_actual_words} words")
            logger.info(
                f"  Cumulative: {cumulative_output_words}/{total_source_words} source words"
            )

            accumulated_transcript += "\n\n" + chunk_transcript
            transcript_chunks.append(chunk_transcript)

        full_transcript = "\n\n".join(transcript_chunks)

    # Prepare transcript directory
    transcripts_dir = output_path.parent / "lecture_transcript"
    transcripts_dir.mkdir(parents=True, exist_ok=True)

    # Safety check: empty transcript
    if not full_transcript or len(full_transcript.strip()) == 0:
        logger.error("Empty transcript generated - cannot proceed with critique")

        critique_path = transcripts_dir / f"{output_path.stem}_critique.md"
        with open(critique_path, "w", encoding="utf-8") as f:
            f.write("# Lecture Transcript Critique\n\n")
            if citation_key:
                f.write(f"**Citation Key:** {citation_key}\n\n")
            f.write(
                "**Status:** ERROR\n\nUnable to critique - empty transcript generated.\n"
            )

        transcript_path = transcripts_dir / f"{output_path.stem}_transcript.md"
        with open(transcript_path, "w", encoding="utf-8") as f:
            f.write("# Lecture Audio Transcript\n\n")
            if citation_key:
                f.write(f"**Citation Key:** {citation_key}\n\n")
            f.write(f"**Generated Transcript:**\n\n{full_transcript}\n")

        logger.error("No audio files to combine")
        return output_path.name

    # Self-refine loop
    critique_prompt = _CRITIQUE_PROMPT
    if str(tts_kwargs.get("provider", "")) == "fish_speech":
        critique_prompt = _CRITIQUE_PROMPT_FISH_SPEECH

    full_transcript = _refine_transcript(
        full_transcript,
        full_system_prompt,
        model,
        citation_key,
        transcripts_dir,
        output_path,
        max_retries,
        enc,
        source_words=len(cleaned_content.split()),
        critique_prompt=critique_prompt,
    )

    # Save final transcript
    transcript_path = transcripts_dir / f"{output_path.stem}_transcript.md"
    with open(transcript_path, "w", encoding="utf-8") as f:
        f.write("# Lecture Audio Transcript\n\n")
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
        f.write("Lecture Audio Transcript (Cleaned for TTS)\n\n")
        if citation_key:
            f.write(f"Citation Key: {citation_key}\n\n")
        f.write(f"Generated Transcript:\n\n{tts_transcript}\n")

    # Chunk subdirectory holds per-chunk MP3s + manifest for surgical regen
    chunks_dir = output_path.parent / "lecture_chunks"
    chunks_dir.mkdir(parents=True, exist_ok=True)

    # Generate bookends inside chunks_dir
    bookend_start = None
    bookend_end = None
    if citation_key:
        bookend_start = generate_bookend_audio(
            citation_key,
            "lecture",
            "start",
            chunks_dir,
            elevenlabs_api_key,
            voice_id,
            speed,
            paper_title=paper_title,
            **tts_kwargs,
        )
        bookend_end = generate_bookend_audio(
            citation_key,
            "lecture",
            "end",
            chunks_dir,
            elevenlabs_api_key,
            voice_id,
            speed,
            **tts_kwargs,
        )

    # Section-aware audio assembly — paragraph-only chunking for lecture prosody
    sections_text = split_transcript_by_sections(tts_transcript)
    if not sections_text:
        sections_text = [tts_transcript]

    chunk_counter = 0

    is_fish = str(tts_kwargs.get("provider", "")) == "fish_speech"
    provider = str(tts_kwargs.get("provider", "elevenlabs"))
    prefix = (
        f"{citation_key}_{output_path.stem}" if citation_key else output_path.stem
    )

    # Collect all chunks across all sections with section index
    all_jobs: list[tuple[int, str, Path]] = []
    for sec_idx, section in enumerate(sections_text):
        audio_chunks = chunk_text_paragraphs(
            section, max_chars=2000 if is_fish else 4500
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
        tts_chunks_parallel(
            tts_pairs, voice_id, elevenlabs_api_key, speed,
            tts_model=LECTURE_TTS_MODEL, **tts_kwargs,
        )
    else:
        for _, chunk, chunk_path in all_jobs:
            text_to_speech(
                chunk, voice_id, chunk_path, elevenlabs_api_key, speed,
                tts_model=LECTURE_TTS_MODEL, **tts_kwargs,
            )
            time.sleep(1)

    all_section_chunks: list[list[Path]] = [[] for _ in sections_text]
    for sec_idx, _, chunk_path in all_jobs:
        all_section_chunks[sec_idx].append(chunk_path)

    # Lecture uses longer section pauses for distinct section separation
    lecture_pause = 4000 if is_fish else 3000
    combine_audio_with_section_pauses(
        all_section_chunks,
        output_path,
        section_pause_ms=lecture_pause,
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
        "lecture",
        output_path.name,
        chunk_entries,
        bookend_start=bookend_start.name if bookend_start else None,
        bookend_end=bookend_end.name if bookend_end else None,
    )

    return output_path.name


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------

_DEFAULT_LECTURE_SYSTEM_PROMPT = """You are a world-class science lecturer in the style of The Great Courses series. Your influences include writers like Carl Sagan, Richard Feynman, and Nick Lane — people who make deep science vivid without dumbing it down. You speak with authority, warmth, and intellectual modesty.

YOUR TASK:
Transform the provided academic text into a polished audio lecture — the kind a listener would choose over a podcast.

STRUCTURE:
Every lecture follows this arc, with ---SECTION_BREAK--- on its own line between each part:

1. OPENING (1-2 paragraphs): State the big question this work addresses. Why should anyone care? Set the intellectual stage. End with a brief roadmap: "Today we'll cover three things: first..., then..., and finally..."

2. BODY (2-4 sections): Each section tells one part of the story. Open each section with a spoken transition that names what's coming — not a bare heading, but a sentence: "Now let's turn to how the authors actually solved this problem." Then dive into the narrative.

3. CLOSING (1 paragraph): A single crisp summary of 3-5 takeaways woven into flowing prose. No new information. End with an intellectually honest forward-looking sentence.

CRITICAL OUTPUT RULES:

1. LENGTH — STRICTLY 25-35% of source manuscript word count.
   - This is a LECTURE, not a second reading of the paper.
   - Cover the key ideas, skip exhaustive details. Be selective and confident.
   - If the source is 5000 words, your lecture is 1250-1750 words. No more.
   - NEVER repeat or re-explain a concept you've already covered.
   - One pass through the material. No "let's revisit" or "as we said earlier."

2. NO META-COMMENTARY — Never mention the format or medium.
   - FORBIDDEN phrases: "for audio purposes", "in the text, an image shows",
     "the source material", "this lecture", "in our discussion", "as we noted"
   - When describing a figure or result, just describe it directly:
     WRONG: "In the text, an image shows a pathway diagram..."
     RIGHT: "The pathway branches at glucose-6-phosphate, where..."
   - The listener knows this is a lecture. Never remind them.

3. NO LISTS — Convert to flowing narrative prose.

4. NO LATEX — Convert ALL math to natural spoken form.

5. SKIP METADATA — Omit references, acknowledgments, affiliations, emails.

6. TONE — Authoritative but modest, like a tenured professor who loves the subject.
   - Adopt the authors' own level of confidence. If they hedge, you hedge.
   - Never oversell: "trivially easy", "obviously", "simply" are banned.
   - Express genuine intellectual excitement where the science warrants it.
   - Use analogies to illuminate, then immediately give the precise technical statement.
   - Vary sentence length. Short sentences for emphasis. Longer ones for flow.

7. SECTION TRANSITIONS — No markdown headers. Use spoken transitions:
   - "Now, the question becomes..." / "This brings us to..." / "Let's turn to..."
   - After the transition sentence, pause: insert ---SECTION_BREAK--- on its own line.
   - Then continue with the body of that section.

8. SECTION BREAKS — Insert ---SECTION_BREAK--- between sections.
   - This creates real silence in the final audio.
   - Place the break AFTER the transition sentence that introduces the next topic."""


_FISH_SPEECH_TAG_INSTRUCTIONS = """SPEECH PROSODY TAGS:
You are generating text for Fish Speech TTS, which supports inline [tag] markers.
Use these tags sparingly but deliberately to make the lecture sound natural and engaging.

Available tags and when to use them:
- [pause] — Between major ideas or after a key takeaway. Gives the listener a beat.
- [short pause] — After a colon, before a list-as-prose, or between related ideas.
- [emphasis] — Before a key term's first introduction or a surprising result.
- [excited] — When describing a genuine breakthrough or elegant insight (use rarely).
- [inhale] — Before a long complex sentence to sound natural (use very sparingly).

Do NOT overuse tags. A lecture with a tag every sentence sounds robotic.
Aim for 1-3 tags per section. Let punctuation and sentence structure do most of the work.

Example:
"This brings us to the central insight. [pause] [emphasis] The acyclicity constraint
can be written as a smooth, differentiable function. That single move transforms an
NP-hard combinatorial search into something gradient descent can handle. [short pause]
And that changes everything."
"""


def _split_large_section(content: str, max_tokens: int) -> list[str]:
    """Split a large section at paragraph boundaries to stay under token limit."""
    enc = tiktoken.get_encoding("cl100k_base")

    paragraphs = content.split("\n\n")
    chunks: list[str] = []
    current_chunk = ""

    for para in paragraphs:
        test_chunk = current_chunk + "\n\n" + para if current_chunk else para
        if len(enc.encode(test_chunk)) > max_tokens and current_chunk:
            chunks.append(current_chunk)
            current_chunk = para
        else:
            current_chunk = test_chunk

    if current_chunk:
        chunks.append(current_chunk)

    return chunks


def _extract_context(transcript: str, max_tokens: int = 300) -> str:
    """Extract last N tokens from transcript for section continuity."""
    if not transcript:
        return ""

    enc = tiktoken.get_encoding("cl100k_base")
    tokens = enc.encode(transcript)

    if len(tokens) <= max_tokens:
        return transcript

    return enc.decode(tokens[-max_tokens:]).strip()


# Preamble sections to SKIP (don't trigger positional cascade)
_PREAMBLE_HEADERS = re.compile(
    r"(?i)^("
    r"AUTHORS?$"
    r"|CORRESPONDENCE$"
    r"|GRAPHICAL\s+ABSTRACT$"
    r"|HIGHLIGHTS$"
    r"|IN\s+BRIEF$"
    r"|ARTICLE$"
    r"|DECLARATION\s+OF\s+INTERESTS?"
    r"|ACKNOWLEDGMENTS?"
    r")"
)

# Methods/SI sections — trigger positional cascade (everything after = methods/SI)
_METHODS_SI_HEADERS = re.compile(
    r"(?i)^("
    r"KEY\s+RESOURCES?"
    r"|EXPERIMENTAL\s+MODEL"
    r"|METHOD\s+DETAILS?"
    r"|STAR\s+METHODS?"
    r"|QUANTIFICATION\s+AND\s+STATISTICAL"
    r"|SUPPLEMENTA\w*\s+(?:FIGURES?|TABLES?|INFORMATION|DATA|MATERIALS?)"
    r"|RESOURCE\s+AVAILABILITY"
    r"|DATA\s+(?:AND\s+CODE\s+)?AVAILABILITY"
    r"|LEAD\s+CONTACT"
    r"|MATERIALS?\s+(?:AND\s+)?(?:METHODS?|AVAILABILITY)"
    r"|(?:SOFTWARE|DOCKER|APPTAINER|GPU)\s"
    r")"
)

_SI_MARKER_PATTERNS = [
    r"Extended Data Fig(?:ure)?\.?\s*\d+",
    r"Supplementary Fig(?:ure)?\.?\s*S?\d+",
    r"Figure S\d+",
    r"Table S\d+",
    r"Supplementary Table\s*S?\d+",
    r"#{2,}\s+(?:Methods|Data|Statistical Analysis|Experimental Procedures)",
]
_SI_MARKER_RE = re.compile(
    "|".join(f"({p})" for p in _SI_MARKER_PATTERNS), re.IGNORECASE
)

_SI_REF_PATTERNS = re.compile(
    r"(?:"
    r"Extended Data Fig(?:ure)?\.?\s*\d+"
    r"|Supplementary Fig(?:ure)?\.?\s*S?\d+"
    r"|Figure S\d+"
    r"|Table S\d+"
    r"|Supplementary Table\s*S?\d+"
    r")",
    re.IGNORECASE,
)

_DEFAULT_LECTURE_SI_INSTRUCTIONS = """\
SUPPLEMENTARY INFORMATION HANDLING:
- SI data enriches the main paper but should NOT dominate the lecture.
- Weave SI details naturally into the narrative where they add depth.
- At least 50% of each section must cover the main paper content.
- Reference SI as "additional experiments show..." or "further data confirms..." — avoid "Supplementary Figure S3" labels."""


def build_si_index(si_content: str) -> dict[str, str]:
    """Index SI content by marker (Extended Data Fig 1, Table S2, etc.).

    Args:
        si_content: Full SI markdown text.

    Returns:
        Dict mapping normalized marker key to the content following that marker
        until the next marker (or end of text).
    """
    if not si_content.strip():
        return {}

    splits: list[tuple[str, int]] = []
    for m in _SI_MARKER_RE.finditer(si_content):
        key = _normalize_si_key(m.group(0))
        splits.append((key, m.start()))

    if not splits:
        return {}

    index: dict[str, str] = {}
    for i, (key, start) in enumerate(splits):
        end = splits[i + 1][1] if i + 1 < len(splits) else len(si_content)
        index[key] = si_content[start:end]

    return index


def extract_relevant_si(
    section_content: str,
    si_index: dict[str, str],
    context_chars: int = 500,
) -> str | None:
    """Find SI references in a section and return matching SI snippets.

    Args:
        section_content: Main paper section text.
        si_index: Index built by build_si_index().
        context_chars: Max chars per matched snippet.

    Returns:
        Concatenated relevant SI snippets, or None if no references found.
    """
    if not si_index:
        return None

    refs = _SI_REF_PATTERNS.findall(section_content)
    if not refs:
        return None

    matched_snippets: list[str] = []
    seen_keys: set[str] = set()

    for ref in refs:
        norm = _normalize_si_key(ref)
        # Fuzzy match against index keys
        for key, content in si_index.items():
            if key in seen_keys:
                continue
            if _si_keys_match(norm, key):
                matched_snippets.append(content[:context_chars])
                seen_keys.add(key)

    return "\n\n".join(matched_snippets) if matched_snippets else None


def _normalize_si_key(raw: str) -> str:
    """Normalize SI marker to a canonical form for matching."""
    s = raw.strip()
    s = re.sub(r"Fig(?:ure)?\.?", "Figure", s, flags=re.IGNORECASE)
    s = re.sub(r"\s+", " ", s)
    s = s.rstrip(".:;,")
    return s.lower()


def _si_keys_match(a: str, b: str) -> bool:
    """Fuzzy match two normalized SI keys."""
    return a == b or a in b or b in a


_CRITIQUE_PROMPT = """Review this lecture transcript for quality issues. The gold standard is The Great Courses lecture series.

Position: {position}

CRITICAL CHECKS:

1. META-COMMENTARY: Flag ANY of these — they must be removed:
   - "In the text, an image shows..." / "the source material" / "for audio purposes"
   - "in our discussion" / "this lecture" / "as we noted" / "as mentioned earlier"
   - Any reference to the FORMAT or MEDIUM of the content

2. REPETITION: Does it re-explain concepts already covered?
   - Duplicate summaries or conclusions (only ONE closing allowed)
   - "As we discussed..." followed by re-stating what was already said
   - Concepts introduced twice with different wording

3. LENGTH: Target is 25-35% of source manuscript.
   - Estimate word count
   - Flag if over 40% — needs aggressive cutting

4. MARKDOWN HEADERS: Are there bare markdown headers (##, ###)?
   - These must be converted to spoken transitions
   - "## Concluding summary" → "Now let's draw this together."

5. LIST DETECTION: Numbered lists, bullet points, or list-like structure?

6. LATEX DETECTION: Raw LaTeX commands or math symbols?

7. CITATIONS: Author citations or references?

8. METADATA: References, acknowledgments, affiliations?

9. TONE:
   - Overselling? ("trivially easy", "obviously", "simply")
   - Salesman-like enthusiasm vs authoritative modesty?
   - Does it respect the authors' own level of confidence?

10. CONVERSATIONAL FLOW:
    - Natural when read aloud? Varied sentence lengths?
    - Choppy or disconnected statements?
    - Good transitions between sections?

11. SUMMARY:
    - Single clear closing paragraph with 3-5 takeaways?
    - Woven into prose, not list-like?

Return structured feedback with:
- feedback: List of specific issues with position info
- done: True if this section passes ALL checks, False if any issues found

Transcript section to review:
{transcript}"""


_CRITIQUE_PROMPT_FISH_SPEECH = _CRITIQUE_PROMPT.replace(
    "1. META-COMMENTARY: Flag ANY of these — they must be removed:\n"
    "   - \"In the text, an image shows...\" / \"the source material\" / \"for audio purposes\"\n"
    "   - \"in our discussion\" / \"this lecture\" / \"as we noted\" / \"as mentioned earlier\"\n"
    "   - Any reference to the FORMAT or MEDIUM of the content",
    "1. META-COMMENTARY: Flag ANY of these — they must be removed:\n"
    "   - \"In the text, an image shows...\" / \"the source material\" / \"for audio purposes\"\n"
    "   - \"in our discussion\" / \"this lecture\" / \"as we noted\" / \"as mentioned earlier\"\n"
    "   - Any reference to the FORMAT or MEDIUM of the content\n"
    "   EXCEPTION: Bracketed TTS prosody tags like [pause], [short pause], [emphasis],\n"
    "   [excited], [inhale] are VALID speech synthesis markers — do NOT flag them.",
)


_REFINEMENT_TEMPLATE = Template("""Revise this lecture transcript to fix the issues identified:

ISSUES IDENTIFIED:
$critique

REVISION INSTRUCTIONS:
1. Convert ALL lists to flowing narrative prose
2. Convert ALL LaTeX to natural spoken language
3. Remove ALL citations and references
4. Remove metadata sections completely
5. Remove ALL meta-commentary ("in the text, an image shows", "for audio purposes", "in our discussion")
6. Convert markdown headers to spoken transitions ("Now let's turn to...")
7. Remove duplicate summaries — keep ONE closing paragraph at the end
8. Remove ANY re-explanation of concepts already covered. One pass only.
9. TARGET LENGTH: 25-35% of source. Cut aggressively if over.
10. Maintain Great Courses lecture style: authoritative, modest, never salesman-like

ORIGINAL TRANSCRIPT:
$transcript

PROVIDE THE COMPLETE REVISED TRANSCRIPT:""")


def _refine_transcript(
    full_transcript: str,
    full_system_prompt: str,
    model: str,
    citation_key: str | None,
    transcripts_dir: Path,
    output_path: Path,
    max_retries: int,
    enc: tiktoken.Encoding,
    source_words: int = 0,
    critique_prompt: str = _CRITIQUE_PROMPT,
) -> str:
    """Run iterative critique-and-refine loop on the transcript."""
    max_iterations = 3
    current_transcript = full_transcript
    critique_feedback = None

    # Length ratio check before critique loop (target: 25-35% of source)
    if source_words > 0:
        ratio = len(current_transcript.split()) / source_words
        if ratio > 0.45:
            logger.warning(
                f"Transcript is {ratio:.0%} of source length (target 25-35%) — injecting length-reduction feedback"
            )
        elif ratio < 0.2:
            logger.warning(
                f"Transcript is only {ratio:.0%} of source length — potential under-development"
            )

    for iteration in range(max_iterations):
        logger.info(f"Lecture critique iteration {iteration + 1}/{max_iterations}")

        transcript_escaped = current_transcript.replace("{", "{{").replace("}", "}}")

        try:
            critique_result = lecture_critic_agent.run_sync(
                critique_prompt.format(
                    transcript=transcript_escaped,
                    position="Full document",
                ),
                instructions="You are an expert educational content reviewer.",
                model=model,
            )
            critique_feedback = critique_result.output
        except Exception as e:
            logger.warning(f"Error critiquing full transcript: {e}")
            logger.info("Falling back to chunked critique...")
            critique_feedback = critique_transcript_chunks(
                transcript=current_transcript,
                critique_prompt=critique_prompt,
                model=model,
                chunk_size=8000,
                max_chunks=10,
            )

        if critique_feedback.done:
            logger.info(
                f"Lecture transcript passed quality check after {iteration} iterations"
            )
            break

        logger.info(
            f"Iteration {iteration + 1} feedback ({len(critique_feedback.feedback)} issues):"
        )
        for issue in critique_feedback.feedback:
            logger.info(f"  - {issue}")

        if iteration < max_iterations - 1:
            logger.info("Refining lecture transcript based on critique...")

            refined_chunks: list[str] = []
            transcript_tokens = enc.encode(current_transcript)
            chunk_size = 8000

            current_tokens = len(transcript_tokens)
            max_output_tokens = min(current_tokens + 2000, 16000)

            for start in range(0, len(transcript_tokens), chunk_size):
                chunk = enc.decode(transcript_tokens[start : start + chunk_size])

                feedback_items = list(critique_feedback.feedback)
                if source_words > 0:
                    ratio = len(current_transcript.split()) / source_words
                    if ratio > 0.45:
                        feedback_items.append(
                            f"LENGTH: Transcript is {ratio:.0%} of source (target 25-35%). "
                            "Cut aggressively: remove repetition, re-explanations, "
                            "exhaustive details, and redundant summaries. One pass only."
                        )
                feedback_text = "\n".join(f"- {issue}" for issue in feedback_items)

                refinement_prompt = _REFINEMENT_TEMPLATE.substitute(
                    critique=feedback_text,
                    transcript=chunk,
                )

                try:
                    refine_result = text_agent.run_sync(
                        refinement_prompt,
                        instructions=full_system_prompt,
                        model=model,
                        model_settings={"max_tokens": max_output_tokens},
                    )
                    refined_chunk = refine_result.output.strip()
                except Exception as e:
                    logger.warning(f"Error during refinement: {e}")
                    refined_chunk = ""

                if not refined_chunk:
                    logger.error("Failed to refine chunk, using original")
                    refined_chunk = chunk

                refined_chunks.append(refined_chunk)

            current_transcript = "\n\n".join(refined_chunks)
            logger.info("Lecture transcript refinement complete")

    # Hard cap: never exceed source word count or ~30 min (~4500 words at TTS speed)
    max_lecture_words = min(source_words, 4500) if source_words > 0 else 4500
    current_words = len(current_transcript.split())
    if current_words > max_lecture_words:
        logger.warning(
            f"Lecture {current_words}w exceeds cap {max_lecture_words}w, truncating to last sentence"
        )
        words = current_transcript.split()
        truncated = " ".join(words[:max_lecture_words])
        last_period = truncated.rfind(".")
        if last_period > len(truncated) * 0.7:
            current_transcript = truncated[: last_period + 1]
        else:
            current_transcript = truncated

    # Save critique if issues remain
    if critique_feedback and not critique_feedback.done and critique_feedback.feedback:
        critique_path = transcripts_dir / f"{output_path.stem}_critique.md"
        with open(critique_path, "w", encoding="utf-8") as f:
            f.write("# Lecture Transcript Critique\n\n")
            if citation_key:
                f.write(f"**Citation Key:** {citation_key}\n\n")
            f.write(
                f"**Status:** NEEDS REFINEMENT (after {max_iterations} iterations)\n\n"
            )
            f.write("**Remaining Issues:**\n\n")
            for i, issue in enumerate(critique_feedback.feedback, 1):
                f.write(f"{i}. {issue}\n")
        logger.info(
            f"Critique file saved with {len(critique_feedback.feedback)} remaining issues after {max_iterations} iterations"
        )

    return current_transcript
