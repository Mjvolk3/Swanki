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
from openai import OpenAI

from ..models.cards import LectureTranscriptFeedback
from ..utils.formatting import humanize_citation_key
from ._common import (
    DEFAULT_VOICE_ID,
    chunk_text,
    clean_markdown_for_tts,
    combine_audio,
    text_to_speech,
)

logger = logging.getLogger(__name__)


def critique_transcript_chunks(
    transcript: str,
    critique_prompt: str,
    instructor_client: OpenAI,
    model: str = "gpt-5",
    chunk_size: int = 8000,
    max_chunks: int = 5,
    max_retries: int = 3,
) -> LectureTranscriptFeedback:
    """Critique transcript by sampling multiple chunks for comprehensive feedback.

    Args:
        transcript: Full transcript to critique.
        critique_prompt: Prompt template with {transcript} and {position} placeholders.
        instructor_client: OpenAI client patched with instructor.
        model: Model to use for critique.
        chunk_size: Characters per chunk.
        max_chunks: Maximum chunks to sample.
        max_retries: Retries per chunk.

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
            critique = instructor_client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert educational content reviewer.",
                    },
                    {
                        "role": "user",
                        "content": critique_prompt.format(
                            transcript=chunk_escaped,
                            position=f"Characters {start_pos}-{start_pos + len(chunk)}",
                        ),
                    },
                ],
                response_model=LectureTranscriptFeedback,
                max_retries=max_retries,
            )

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
    openai_client: OpenAI,
    instructor_client: OpenAI,
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
        openai_client: Regular OpenAI client for generation.
        instructor_client: Instructor-patched client for validation.
        model: Model for generation and critique.
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

        response = openai_client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            max_completion_tokens=max_completion_tokens,
        )

        chunk_transcript = (
            response.choices[0].message.content.strip()
            if response.choices[0].message.content
            else ""
        )
        finish_reason = response.choices[0].finish_reason

        logger.info(
            f"Section '{section_title}' response: "
            f"content_length={len(chunk_transcript)}, "
            f"finish_reason={finish_reason}, "
            f"max_completion_tokens={max_completion_tokens}"
        )

        if not chunk_transcript:
            logger.error(
                f"Section '{section_title}' returned EMPTY content! "
                f"finish_reason={finish_reason}, "
                f"has_refusal={hasattr(response.choices[0].message, 'refusal') and response.choices[0].message.refusal is not None}"
            )
            if (
                hasattr(response.choices[0].message, "refusal")
                and response.choices[0].message.refusal
            ):
                logger.error(f"Refusal reason: {response.choices[0].message.refusal}")

        # Immediate critique
        try:
            chunk_escaped = chunk_transcript.replace("{", "{{").replace("}", "}}")

            critique = instructor_client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert educational content reviewer.",
                    },
                    {
                        "role": "user",
                        "content": critique_prompt.format(
                            transcript=chunk_escaped,
                        ),
                    },
                ],
                response_model=LectureTranscriptFeedback,
                max_retries=2,
            )

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
    openai_client: OpenAI,
    elevenlabs_api_key: str,
    voice_id: str | None = None,
    model: str = "gpt-5-mini",
    citation_key: str | None = None,
    lecture_prompt_config: dict | None = None,
    speed: float = 1.0,
    si_start_page: int | None = None,
) -> str:
    """Generate an educational lecture from document content.

    Args:
        markdown_files: Cleaned markdown file paths in order.
        image_summaries: Image summary strings to embed.
        output_path: Path for the output MP3 file.
        openai_client: OpenAI client for transcript generation.
        elevenlabs_api_key: ElevenLabs API key.
        voice_id: Voice ID (defaults to DEFAULT_VOICE_ID).
        model: OpenAI model to use.
        citation_key: Citation key to include in lecture.
        lecture_prompt_config: Custom prompt config with 'lecture_system'
            and 'lecture_prefix' keys.
        speed: Audio playback speed multiplier.
        si_start_page: Page index where SI begins in markdown_files.
            When set, main paper and SI are processed separately.

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
    full_system_prompt = f"{system_instructions}\n\nCitation: {humanized_key}"

    # Append SI instructions when SI is present
    if si_start_page is not None:
        si_prompt = si_instructions or _DEFAULT_LECTURE_SI_INSTRUCTIONS
        full_system_prompt += f"\n\n{si_prompt}"

    # Chunk main content only by semantic structure
    semantic_chunks = chunk_by_headers(cleaned_content, max_tokens_per_chunk=15000)

    # Build SI index once (empty if no SI)
    si_index = build_si_index(si_content) if si_content else {}
    if si_index:
        logger.info(f"SI index: {len(si_index)} entries: {list(si_index.keys())}")

    logger.info(f"Split content into {len(semantic_chunks)} semantic sections")
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

        lecture_transcript = None
        for attempt in range(max_retries):
            try:
                response = openai_client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": full_system_prompt},
                        {"role": "user", "content": user_message},
                    ],
                    max_completion_tokens=10000,
                )

                if (
                    response.choices
                    and len(response.choices) > 0
                    and response.choices[0].message.content
                ):
                    lecture_transcript = response.choices[0].message.content.strip()
                    if lecture_transcript:
                        break
                    else:
                        logger.warning(
                            f"Attempt {attempt + 1}: Returned empty lecture transcript"
                        )
                else:
                    logger.warning(
                        f"Attempt {attempt + 1}: Returned malformed response for lecture"
                    )

            except Exception as e:
                logger.warning(
                    f"Attempt {attempt + 1}: Error generating lecture transcript: {e}"
                )

            if attempt < max_retries - 1:
                time.sleep(2**attempt)

        if not lecture_transcript:
            logger.error(
                f"Failed to generate lecture transcript after {max_retries} attempts, using original"
            )
            lecture_transcript = section_content

        full_transcript = lecture_transcript
    else:
        # Multi-section generation
        logger.info("Using multi-section generation with per-section validation")
        accumulated_transcript = ""

        total_source_words = len(cleaned_content.split())
        cumulative_output_words = 0

        import instructor

        instructor_client = instructor.from_openai(openai_client)

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
                openai_client=openai_client,
                instructor_client=instructor_client,
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
    full_transcript = _refine_transcript(
        full_transcript,
        full_system_prompt,
        openai_client,
        model,
        citation_key,
        transcripts_dir,
        output_path,
        max_retries,
        enc,
        source_words=len(cleaned_content.split()),
    )

    # Save final transcript
    transcript_path = transcripts_dir / f"{output_path.stem}_transcript.md"
    with open(transcript_path, "w", encoding="utf-8") as f:
        f.write("# Lecture Audio Transcript\n\n")
        if citation_key:
            f.write(f"**Citation Key:** {citation_key}\n\n")
        f.write(f"**Generated Transcript:**\n\n{full_transcript}\n")

    tts_transcript = clean_markdown_for_tts(full_transcript)

    cleaned_path = (
        transcripts_dir / f"{output_path.stem}_transcript_cleaned_markdown.md"
    )
    with open(cleaned_path, "w", encoding="utf-8") as f:
        f.write("Lecture Audio Transcript (Cleaned for TTS)\n\n")
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

    if len(chunk_paths) == 1:
        chunk_paths[0].rename(output_path)
    else:
        combine_audio(chunk_paths, output_path)
        for p in chunk_paths:
            p.unlink()

    return output_path.name


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------

_DEFAULT_LECTURE_SYSTEM_PROMPT = """You are an expert educator creating an audio lecture from academic content.

YOUR TASK:
Transform the provided academic text into an engaging, conversational audio lecture.

CRITICAL OUTPUT RULES:
1. NO LISTS: Never use numbered lists (1., 2., 3.) or bullet points (-)
   - Convert to flowing narrative: "The main types include X, which does A, Y, which does B, and Z, which does C"

2. NO LATEX: Convert ALL LaTeX to natural language
   - Tables: Summarize with a few examples, don't read every row
   - Math: Convert to spoken form (e.g., "x squared" not "x^2")
   - Figures: Describe narratively

3. SKIP METADATA: Completely omit any remaining:
   - References sections
   - "Competing interests"
   - Author affiliations
   - Email addresses
   - "Published online" dates

4. CONVERSATIONAL TONE:
   - Write as if explaining to a curious student
   - Use transitions: "Let's turn to...", "This connects to...", "The key insight here is..."
   - Vary sentence structure for natural rhythm
   - Ask rhetorical questions to engage: "Why does this matter? Because..."

5. CONCLUDE WITH SUMMARY:
   - End with 3-5 main takeaways
   - Brief, clear recap
   - No new information

6. TARGET LENGTH:
   - Aim for roughly 40-60% of source manuscript length
   - Let the content drive section lengths
   - Be selective: key concepts only, skip exhaustive details
   - Focus on WHY and HOW, not just WHAT"""


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


_CRITIQUE_PROMPT = """Review this section of a lecture transcript for quality issues:

Position: {position}

CRITICAL CHECKS:
1. LIST DETECTION: Does it use numbered lists (1., 2., 3.) or bullet points (- )?
   - Count occurrences of list patterns
   - Flag sections that read like enumerated items

2. LATEX DETECTION: Does it contain raw LaTeX commands?
   - Check for: \\begin{{tabular}}, \\begin{{table}}, \\hline, \\multirow, \\captionsetup, \\caption, \\footnotetext, \\footnote, etc.
   - LaTeX math symbols: $10 \\%$, $\\boldsymbol{{\\alpha}}$, etc.
   - LaTeX MUST be converted to natural spoken language
   - Tables should be brief highlights with 2-3 examples, NEVER read row-by-row
   - Footnotes should be integrated inline naturally

3. CITATIONS: Does it include author citations or references?
   - Check for: "(Author et al., YEAR)", "Smith and Jones (2020)", "Fernandez-Martinez and Rout, 2009"
   - ALL citations must be removed and replaced with "Research has shown..." or similar

4. METADATA SECTIONS: Are any of these present?
   - "Further Reading" sections (MUST be removed)
   - "References" or "Bibliography" sections (MUST be removed)
   - Author affiliations or emails (MUST be removed)
   - "Competing interests" or "Acknowledgments" (MUST be removed)

5. LENGTH CHECK:
   - Estimate word count
   - Is it roughly 50% of typical source length?
   - Too detailed or encyclopedic?

6. CONVERSATIONAL FLOW:
   - Does it sound natural when read aloud?
   - Are there choppy, disconnected statements?
   - Good use of transitions between ideas?
   - Complete, flowing sentences?

7. FIGURE/TABLE INTEGRATION:
   - Figures should start with "In the text, an image shows..." or "Looking at a diagram, we can see..."
   - Tables should be summarized with key highlights, not listed exhaustively
   - Are descriptions natural and narrative?

8. SUMMARY:
   - Does it end with a clear summary of 3-5 main takeaways?
   - Missing or weak conclusion?

Return structured feedback with:
- feedback: List of specific issues with position info
- done: True if this section passes ALL checks, False if any issues found

Transcript section to review:
{transcript}"""


_REFINEMENT_TEMPLATE = Template("""Revise this lecture transcript to fix the issues identified:

ISSUES IDENTIFIED:
$critique

REVISION INSTRUCTIONS:
1. Convert ALL lists to flowing narrative prose
2. Convert ALL LaTeX to natural spoken language
3. Remove ALL citations and references
4. Remove metadata sections completely
5. Improve figure/table integration
6. Add or strengthen the concluding summary
7. Improve conversational flow
8. Reduce length if too detailed (aim for ~50% of original source)

ORIGINAL TRANSCRIPT:
$transcript

PROVIDE THE COMPLETE REVISED TRANSCRIPT:""")


def _refine_transcript(
    full_transcript: str,
    full_system_prompt: str,
    openai_client: OpenAI,
    model: str,
    citation_key: str | None,
    transcripts_dir: Path,
    output_path: Path,
    max_retries: int,
    enc: tiktoken.Encoding,
    source_words: int = 0,
) -> str:
    """Run iterative critique-and-refine loop on the transcript."""
    import instructor

    instructor_client = instructor.patch(openai_client)

    max_iterations = 3
    current_transcript = full_transcript
    critique_feedback = None

    # Length ratio check before critique loop
    if source_words > 0:
        ratio = len(current_transcript.split()) / source_words
        if ratio > 0.7:
            logger.warning(
                f"Transcript is {ratio:.0%} of source length — injecting length-reduction feedback"
            )
        elif ratio < 0.3:
            logger.warning(
                f"Transcript is only {ratio:.0%} of source length — potential under-development"
            )

    for iteration in range(max_iterations):
        logger.info(f"Lecture critique iteration {iteration + 1}/{max_iterations}")

        transcript_escaped = current_transcript.replace("{", "{{").replace("}", "}}")

        try:
            critique_feedback = instructor_client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert educational content reviewer.",
                    },
                    {
                        "role": "user",
                        "content": _CRITIQUE_PROMPT.format(
                            transcript=transcript_escaped,
                            position="Full document",
                        ),
                    },
                ],
                response_model=LectureTranscriptFeedback,
                max_retries=max_retries,
            )
        except Exception as e:
            logger.warning(f"Error critiquing full transcript: {e}")
            logger.info("Falling back to chunked critique...")
            critique_feedback = critique_transcript_chunks(
                transcript=current_transcript,
                critique_prompt=_CRITIQUE_PROMPT,
                instructor_client=instructor_client,
                model=model,
                chunk_size=8000,
                max_chunks=10,
                max_retries=max_retries,
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
                    if ratio > 0.7:
                        feedback_items.append(
                            f"LENGTH: Transcript is {ratio:.0%} of source. "
                            "Cut to 40-60% by removing redundancy and excessive detail."
                        )
                feedback_text = "\n".join(f"- {issue}" for issue in feedback_items)

                refinement_prompt = _REFINEMENT_TEMPLATE.substitute(
                    critique=feedback_text,
                    transcript=chunk,
                )

                refined_chunk = None

                for attempt in range(max_retries):
                    try:
                        refinement = openai_client.chat.completions.create(
                            model=model,
                            messages=[
                                {"role": "system", "content": full_system_prompt},
                                {"role": "user", "content": refinement_prompt},
                            ],
                            max_completion_tokens=max_output_tokens,
                        )

                        if (
                            refinement.choices
                            and len(refinement.choices) > 0
                            and refinement.choices[0].message.content
                        ):
                            refined_chunk = refinement.choices[
                                0
                            ].message.content.strip()
                            if refined_chunk:
                                break
                        else:
                            logger.warning(
                                f"Attempt {attempt + 1}: Empty refinement response"
                            )

                    except Exception as e:
                        logger.warning(
                            f"Attempt {attempt + 1}: Error during refinement: {e}"
                        )

                    if attempt < max_retries - 1:
                        time.sleep(2**attempt)

                if not refined_chunk:
                    logger.error("Failed to refine chunk, using original")
                    refined_chunk = chunk

                refined_chunks.append(refined_chunk)

            current_transcript = "\n\n".join(refined_chunks)
            logger.info("Lecture transcript refinement complete")

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
