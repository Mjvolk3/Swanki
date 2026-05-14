"""
swanki/audio/card.py
[[swanki.audio.card]]
https://github.com/Mjvolk3/Swanki/tree/main/swanki/audio/card.py

Flashcard audio generation with cloze handling, image descriptions, and citation prefixing.
"""

import json
import logging
import re
import time
from pathlib import Path

import tiktoken

from ..llm.agents import text_agent
from ..models.cards import PlainCard
from ..utils.formatting import humanize_citation_key
from ._common import (
    DEFAULT_VOICE_ID,
    append_chunk_pause,
    apply_pronunciation_overrides,
    chunk_text,
    combine_audio,
    expand_acronyms_for_tts,
    strip_chapter_filename_slug,
    strip_forbidden_fish_tags,
    text_to_speech,
    validate_audio_file,
)

logger = logging.getLogger(__name__)


def _preprocess_for_tts(text: str, tts_kwargs: dict) -> str:
    """Apply Fish-Speech-aware TTS preprocessing to a single text fragment.

    Centralizes the deterministic scrubber chain so card.py's five
    text_to_speech call sites all run the same passes in the same order.
    Pure no-op for elevenlabs (the fish-only steps are gated by provider).

    Order matches lecture.py / summary.py / reading.py: slug-strip ->
    acronym letter-by-letter (fish only) -> pronunciation overrides ->
    forbidden-tag scrub (fish only). Card transcripts skip
    clean_markdown_for_tts and add_tts_pauses entirely (cards are short and
    arrive already TTS-shaped); this helper picks up the remaining scrubbers.

    Args:
        text: Card transcript fragment about to be sent to text_to_speech.
        tts_kwargs: Provider config dict; reads optional ``preprocessor``
            sub-tree for per-paper pronunciations and acronym allowlist.

    Returns:
        Preprocessed text safe for the provider's TTS endpoint.
    """
    is_fish = str(tts_kwargs.get("provider", "")) == "fish_speech"
    _prep_raw = tts_kwargs.get("preprocessor")
    prep_cfg: dict = _prep_raw if isinstance(_prep_raw, dict) else {}
    out = strip_chapter_filename_slug(text)
    if is_fish and prep_cfg.get("acronym_letter_by_letter", True):
        allowlist = set(prep_cfg.get("acronym_allowlist", []))
        out = expand_acronyms_for_tts(out, allowlist=allowlist)
    pronunciations = prep_cfg.get("pronunciations", {}) or {}
    if pronunciations:
        out = apply_pronunciation_overrides(out, pronunciations)
    if is_fish and prep_cfg.get("strip_forbidden_tags", True):
        out = strip_forbidden_fish_tags(out)
    return out


def generate_card_transcript(
    card: PlainCard,
    is_front: bool,
    model: str | None = None,
    citation_key: str | None = None,
    humanized_citation: str | None = None,
) -> str:
    """Generate an audio-optimized transcript for one side of a card.

    Handles cloze masking, image summary integration, math-to-speech
    conversion, and citation prefixing.

    Args:
        card: The card to generate transcript for.
        is_front: Whether this is the front (True) or back (False).
        model: pydantic-ai model string (e.g. ``"openai:gpt-5-mini"``).
        citation_key: Raw citation key to include in front transcript.
        humanized_citation: Pre-humanized citation for consistency.

    Returns:
        Transcript text optimized for TTS.
    """
    if model is None:
        raise ValueError("model is required; pass the LLM from config")
    is_cloze = "{{c" in card.front.text

    # Get the appropriate text WITHOUT citation first
    if is_front:
        content = card.front.text

        # For cloze cards on front, replace cloze markers with "blank"
        if is_cloze:
            content = _replace_all_cloze_with_blank(content)

        # Remove any existing citation to work with clean content
        if citation_key and content.startswith(f"@{citation_key}: "):
            content = content[len(f"@{citation_key}: ") :]
        elif humanized_citation and content.startswith(f"{humanized_citation}: "):
            content = content[len(f"{humanized_citation}: ") :]
    else:
        # For back of card
        if is_cloze:
            # Read the FULL front text with cloze markers removed to reveal hidden text
            content = card.front.text

            # Filter tags from back text
            if card.back.text:
                back_lines = card.back.text.split("\n")
                filtered_back = []
                for line in back_lines:
                    if not (
                        line.strip().startswith("#") or line.strip().startswith("- #")
                    ):
                        filtered_back.append(line)
                non_tag_back = "\n".join(filtered_back).strip()
                if non_tag_back:
                    logger.warning(
                        f"Cloze card {card.card_id} has non-tag content in back: {non_tag_back[:50]}..."
                    )

            # Remove cloze markers to reveal hidden text
            content = re.sub(
                r"\{\{c\d+::(.+?)\}\}(?!\})",
                _remove_cloze_markers,
                content,
                flags=re.DOTALL,
            )

            if "blank" in content.lower():
                logger.warning(
                    f"'blank' found in cloze back content after processing: {content[:100]}..."
                )

            # Remove existing citation
            if citation_key and content.startswith(f"@{citation_key}: "):
                content = content[len(f"@{citation_key}: ") :]
            elif humanized_citation and content.startswith(f"{humanized_citation}: "):
                content = content[len(f"{humanized_citation}: ") :]
        else:
            # Regular card - use the back text without tags
            content = card.back.text
            lines = content.split("\n")
            filtered_lines = []
            for line in lines:
                if not (line.strip().startswith("#") or line.strip().startswith("- #")):
                    filtered_lines.append(line)
            content = "\n".join(filtered_lines).strip()

    # Gather image summary for this side
    image_summary_for_audio = ""

    logger.debug(f"Card {card.card_id} - Audio generation debug:")
    logger.debug(f"  Is front: {is_front}")
    logger.debug(f"  Front image path: {card.front.image_path}")
    logger.debug(f"  Back image path: {card.back.image_path}")
    logger.debug(f"  Front image summary: {card.front.image_summary}")
    logger.debug(f"  Back image summary: {card.back.image_summary}")

    if is_front:
        if card.front.image_path and card.front.image_summary:
            image_summary_for_audio = card.front.image_summary
            logger.debug("  Using front image summary for front audio")
        elif card.front.image_path and not card.front.image_summary:
            logger.error(
                f"Card {card.card_id} has front image but no image summary for audio"
            )
    else:
        if card.back.image_path and card.back.image_summary:
            image_summary_for_audio = card.back.image_summary
            logger.debug("  Using back image summary for back audio")
        elif card.back.image_path and not card.back.image_summary:
            logger.error(
                f"Card {card.card_id} has back image but no image summary for audio"
            )

    # Add citation prefix
    if (is_front or (not is_front and is_cloze)) and (
        citation_key or humanized_citation
    ):
        citation_prefix = (
            humanized_citation if humanized_citation else f"@{citation_key}"
        )
        content = f"{citation_prefix}: {content.strip()}"

    # Append image summary after main content
    if image_summary_for_audio:
        content = f"{content.strip()}. Image description: {image_summary_for_audio}"
        logger.debug(
            f"Card {card.card_id}: Added image summary AFTER content for audio"
        )

    # Pre-process: humanize LaTeX before transcript generation
    # This dedicated pass converts all math to spoken form so the transcript
    # LLM doesn't have to handle LaTeX conversion AND audio optimization.
    if "$" in content or "\\" in content:
        from ._common import humanize_latex

        logger.info(f"Card {card.card_id} - Humanizing LaTeX before transcript generation")
        content = humanize_latex(content, model)

    # Build system prompt
    system_content = _build_transcript_system_prompt(
        is_front, is_cloze, bool(image_summary_for_audio)
    )

    # Process through LLM in chunks
    enc = tiktoken.get_encoding("cl100k_base")
    tokens = enc.encode(content)
    max_chunk = 3000
    out_chunks: list[str] = []

    logger.info(f"Card {card.card_id} - Sending to LLM:")
    logger.info(f"  Content length: {len(content)} chars")
    logger.info(f"  Content preview: {content[:300]}...")
    logger.info(
        f"  Contains 'Image description:': {'Yes' if 'Image description:' in content else 'No'}"
    )

    for start in range(0, len(tokens), max_chunk):
        chunk = enc.decode(tokens[start : start + max_chunk])
        logger.info(
            f"  Processing chunk {start // max_chunk + 1}, length: {len(chunk)}"
        )

        try:
            result = text_agent.run_sync(
                chunk,
                instructions=system_content,
                model=model,
                model_settings={"max_tokens": 2000},
            )
            response_content = result.output.strip()
        except Exception as e:
            logger.warning(f"  Error calling LLM: {e}")
            response_content = ""

        if not response_content:
            logger.error("  Failed to get response from LLM")
            response_content = chunk

        out_chunks.append(response_content)

        logger.info(f"  LLM response length: {len(response_content)} chars")
        logger.info(
            f"  Response includes image desc: {'Yes' if 'image' in response_content.lower() else 'No'}"
        )

    transcript = "\n\n".join(out_chunks)
    transcript = re.sub(r"(Question|Answer|Guidance):\s*", "", transcript)
    return transcript


def generate_citation_audio(
    citation_key: str,
    output_path: Path,
    elevenlabs_api_key: str,
    voice_id: str | None = None,
    model: str | None = None,
    speed: float = 1.0,
    use_cache: bool = True,
    max_retries: int = 3,
    min_file_size: int = 1024,
    force_regenerate: bool = False,
    citation_speed_override: float | None = None,
    **tts_kwargs: object,
) -> Path:
    """Generate reusable audio for a citation key with validation and caching.

    Args:
        citation_key: The citation key to convert to audio.
        output_path: Path for the output MP3 file.
        elevenlabs_api_key: ElevenLabs API key.
        voice_id: Voice ID (defaults to DEFAULT_VOICE_ID).
        model: pydantic-ai model string.
        speed: Audio playback speed multiplier.
        use_cache: Whether to reuse existing file if valid.
        max_retries: Maximum retry attempts.
        min_file_size: Minimum valid file size in bytes.
        force_regenerate: Force regeneration even if cached.
        citation_speed_override: Override speed for citation audio only.

    Returns:
        Path to the generated audio file.

    Raises:
        RuntimeError: If audio generation fails after all retries.
    """
    if model is None:
        raise ValueError("model is required; pass the LLM from config")
    voice_id = voice_id or DEFAULT_VOICE_ID

    humanized = _humanize_citation(citation_key, model, max_retries)

    logger.debug(f"Citation audio generation: '{citation_key}' -> '{humanized}'")

    # Check cache
    if use_cache and not force_regenerate and output_path.exists():
        if validate_audio_file(output_path, min_file_size, humanized):
            logger.info(f"Using cached citation audio: {output_path}")
            return output_path
        else:
            logger.warning(
                f"Cached citation audio failed validation, regenerating: {output_path}"
            )
            output_path.unlink()

    citation_text = f"{humanized}:"

    last_error = None
    for attempt in range(max_retries):
        try:
            logger.debug(
                f"Generating citation audio (attempt {attempt + 1}/{max_retries})"
            )

            citation_speed = (
                citation_speed_override
                if citation_speed_override is not None
                else speed
            )
            text_to_speech(
                text=_preprocess_for_tts(citation_text, tts_kwargs),
                voice_id=voice_id,
                output_path=output_path,
                api_key=elevenlabs_api_key,
                speed=citation_speed,
                **tts_kwargs,
            )

            if validate_audio_file(output_path, min_file_size, humanized):
                logger.debug(f"Successfully generated citation audio: {output_path}")
                return output_path
            else:
                logger.warning(
                    f"Generated audio failed validation (attempt {attempt + 1})"
                )
                if output_path.exists():
                    output_path.unlink()

        except Exception as e:
            last_error = e
            logger.error(
                f"Error generating citation audio (attempt {attempt + 1}): {e}"
            )
            if output_path.exists():
                output_path.unlink()

        if attempt < max_retries - 1:
            wait_time = 2**attempt
            logger.info(f"Waiting {wait_time} seconds before retry...")
            time.sleep(wait_time)

    error_msg = f"Failed to generate valid citation audio after {max_retries} attempts"
    if last_error:
        error_msg += f": {last_error}"
    raise RuntimeError(error_msg)


def generate_card_audio(
    card: PlainCard,
    card_index: int,
    page_base: str,
    audio_dir: Path,
    elevenlabs_api_key: str,
    voice_id: str | None = None,
    model: str | None = None,
    citation_key: str | None = None,
    speed: float = 1.0,
    force_regenerate_citation: bool = False,
    **tts_kwargs: object,
) -> tuple[str, str | None]:
    """Generate audio files for both sides of a flashcard.

    Creates front and back MP3 files. Citation audio is generated once
    and prepended to each front. Cloze cards mask hidden text on front
    and reveal on back.

    Args:
        card: The card to generate audio for.
        card_index: 1-based index for naming.
        page_base: Base name for the page (e.g., "page-1").
        audio_dir: Directory to save audio files.
        elevenlabs_api_key: ElevenLabs API key.
        voice_id: Voice ID (defaults to DEFAULT_VOICE_ID).
        model: pydantic-ai model string (e.g. ``"openai:gpt-5-mini"``).
        citation_key: Citation key for file naming and content.
        speed: Audio playback speed multiplier.
        force_regenerate_citation: Force regeneration of citation audio.

    Returns:
        Tuple of (front_filename, back_filename). Back may be None.
    """
    if model is None:
        raise ValueError("model is required; pass the LLM from config")
    voice_id = voice_id or DEFAULT_VOICE_ID

    humanized_citation = humanize_citation_key(citation_key) if citation_key else None

    if humanized_citation:
        logger.debug(
            f"Card {card.card_id} - Using humanized citation: '{humanized_citation}' (from '{citation_key}')"
        )

    # Generate transcripts without citation (added separately as audio)
    front_transcript = generate_card_transcript(
        card,
        is_front=True,
        model=model,
        citation_key=None,
        humanized_citation=None,
    )

    back_transcript = generate_card_transcript(
        card,
        is_front=False,
        model=model,
        citation_key=None,
        humanized_citation=None,
    )

    card.audio_front_transcript = front_transcript
    card.audio_back_transcript = back_transcript

    card_uuid = card.card_id or str(card_index)

    if citation_key:
        front_filename = f"{citation_key}_{card_uuid}_front.mp3"
        back_filename = f"{citation_key}_{card_uuid}_back.mp3"
    else:
        front_filename = f"{card_uuid}_front.mp3"
        back_filename = f"{card_uuid}_back.mp3"

    front_path = audio_dir / front_filename
    back_path = audio_dir / back_filename

    # Save transcripts for debugging
    _save_card_transcripts(
        card,
        card_index,
        card_uuid,
        citation_key,
        front_transcript,
        back_transcript,
        humanized_citation,
        audio_dir,
    )

    # Generate citation audio
    citation_audio_path = None
    if citation_key and humanized_citation:
        citation_audio_path = audio_dir / f"{citation_key}_citation.mp3"
        try:
            citation_audio_path = generate_citation_audio(
                citation_key=citation_key,
                output_path=citation_audio_path,
                elevenlabs_api_key=elevenlabs_api_key,
                voice_id=voice_id,
                model=model,
                speed=speed,
                use_cache=True,
                force_regenerate=force_regenerate_citation,
                **tts_kwargs,
            )
        except RuntimeError as e:
            logger.error(
                f"Failed to generate citation audio for card {card.card_id}: {e}"
            )
            citation_audio_path = None
            logger.warning(f"Proceeding without citation audio for card {card.card_id}")

    provider = str(tts_kwargs.get("provider", "elevenlabs"))
    chunks_subdir = audio_dir / "card_chunks"

    front_manifest_chunks: list[dict] = []
    back_manifest_chunks: list[dict] = []

    # Generate front audio
    front_chunks = chunk_text(front_transcript)
    needs_combination = citation_audio_path is not None or len(front_chunks) > 1

    if not needs_combination:
        text_to_speech(
            _preprocess_for_tts(front_chunks[0], tts_kwargs),
            voice_id, front_path, elevenlabs_api_key, speed, **tts_kwargs
        )
    else:
        chunks_subdir.mkdir(parents=True, exist_ok=True)
        chunk_paths: list[Path] = []

        if citation_audio_path and citation_audio_path.exists():
            chunk_paths.append(citation_audio_path)
            front_manifest_chunks.append(
                {
                    "index": 0,
                    "type": "citation",
                    "file": citation_audio_path.name,
                }
            )

        for i, chunk in enumerate(front_chunks):
            prefix = f"{citation_key}_{page_base}" if citation_key else page_base
            chunk_path = chunks_subdir / f"{prefix}_{card_index}_front_chunk{i}.mp3"
            paused_chunk = append_chunk_pause(chunk, provider)
            text_to_speech(
                _preprocess_for_tts(paused_chunk, tts_kwargs),
                voice_id, chunk_path, elevenlabs_api_key, speed, **tts_kwargs
            )
            chunk_paths.append(chunk_path)
            front_manifest_chunks.append(
                {
                    "index": len(front_manifest_chunks),
                    "type": "tts",
                    "text": paused_chunk,
                    "file": chunk_path.name,
                }
            )
            time.sleep(1)

        combine_audio(chunk_paths, front_path, crossfade_ms=0)

    # Generate back audio
    if back_transcript:
        time.sleep(1)

        back_chunks = chunk_text(back_transcript)
        if len(back_chunks) == 1:
            text_to_speech(
                _preprocess_for_tts(back_chunks[0], tts_kwargs),
                voice_id, back_path, elevenlabs_api_key, speed, **tts_kwargs
            )
        else:
            chunks_subdir.mkdir(parents=True, exist_ok=True)
            chunk_paths = []
            for i, chunk in enumerate(back_chunks):
                prefix = f"{citation_key}_{page_base}" if citation_key else page_base
                chunk_path = chunks_subdir / f"{prefix}_{card_index}_back_chunk{i}.mp3"
                paused_chunk = append_chunk_pause(chunk, provider)
                text_to_speech(
                    _preprocess_for_tts(paused_chunk, tts_kwargs),
                    voice_id, chunk_path, elevenlabs_api_key, speed, **tts_kwargs
                )
                chunk_paths.append(chunk_path)
                back_manifest_chunks.append(
                    {
                        "index": i,
                        "type": "tts",
                        "text": paused_chunk,
                        "file": chunk_path.name,
                    }
                )
                time.sleep(1)

            combine_audio(chunk_paths, back_path, crossfade_ms=0)

        # Write per-card manifest (one file per card avoids parallel-write races)
        if front_manifest_chunks or back_manifest_chunks:
            chunks_subdir.mkdir(parents=True, exist_ok=True)
            citation_audio_rel = (
                f"../{citation_audio_path.name}"
                if citation_audio_path and citation_audio_path.exists()
                else None
            )
            manifest = {
                "audio_type": "card",
                "card_id": card_uuid,
                "card_index": card_index,
                "front_file": front_filename,
                "back_file": back_filename,
                "citation_audio": citation_audio_rel,
                "sides": {
                    "front": {"chunks": front_manifest_chunks},
                    "back": {"chunks": back_manifest_chunks},
                },
            }
            manifest_path = chunks_subdir / f"{card_uuid}_manifest.json"
            manifest_path.write_text(json.dumps(manifest, indent=2))

        return front_filename, back_filename
    else:
        if front_manifest_chunks:
            chunks_subdir.mkdir(parents=True, exist_ok=True)
            citation_audio_rel = (
                f"../{citation_audio_path.name}"
                if citation_audio_path and citation_audio_path.exists()
                else None
            )
            manifest = {
                "audio_type": "card",
                "card_id": card_uuid,
                "card_index": card_index,
                "front_file": front_filename,
                "back_file": None,
                "citation_audio": citation_audio_rel,
                "sides": {
                    "front": {"chunks": front_manifest_chunks},
                },
            }
            manifest_path = chunks_subdir / f"{card_uuid}_manifest.json"
            manifest_path.write_text(json.dumps(manifest, indent=2))
        return front_filename, None


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------


def _replace_all_cloze_with_blank(text: str) -> str:
    """Replace all cloze deletions with 'blank', handling nested braces."""
    result = text
    while "{{c" in result:
        start = result.find("{{c")
        if start == -1:
            break

        colon_pos = result.find("::", start)
        if colon_pos == -1:
            break

        pos = colon_pos + 2
        brace_count = 2

        while pos < len(result) and brace_count > 0:
            if result[pos] == "{":
                brace_count += 1
            elif result[pos] == "}":
                brace_count -= 1
            pos += 1

        if brace_count == 0:
            result = result[:start] + "blank" + result[pos:]
        else:
            break

    return result


def _remove_cloze_markers(match: re.Match[str]) -> str:  # type: ignore[type-arg]
    """Remove cloze markers from a regex match, handling nested braces."""
    cloze_content = match.group(1)
    brace_count = 0
    complete_content = cloze_content
    remaining = match.string[match.end() :]

    for char in cloze_content:
        if char == "{":
            brace_count += 1
        elif char == "}":
            brace_count -= 1

    if brace_count > 0:
        for i, char in enumerate(remaining):
            complete_content += char
            if char == "{":
                brace_count += 1
            elif char == "}":
                brace_count -= 1
                if brace_count == -2:
                    complete_content = complete_content[:-1]
                    break

    return complete_content


def _humanize_citation(
    citation_key: str, model: str | None = None, max_retries: int = 3
) -> str:
    """Convert a citation key to natural speech via LLM."""
    if model is None:
        raise ValueError("model is required; pass the LLM from config")
    system_prompt = (
        "Convert citation keys to natural speech for text-to-speech. "
        "Make it flow naturally as if speaking. Add appropriate pauses with commas. "
        "Keep it concise but clear. Do not add extra words like 'from' or 'by'. "
        "Return ONLY the converted text, no explanation."
    )

    user_prompt = (
        f"Convert this citation key to natural speech: {citation_key}\n\n"
        "Examples:\n"
        "smithMachineLearning2023 -> Smith, Machine Learning, 2023\n"
        "bishopDeepLearningFoundations2024_deep-learning-revolution -> "
        "Bishop, Deep Learning Foundations, 2024, deep learning revolution\n"
        "johnsonEtAl2022 -> Johnson et al, 2022\n"
        "feldmannYeastMolecularCell2012 -> Feldmann, Yeast Molecular Cell, 2012"
    )

    try:
        result = text_agent.run_sync(
            user_prompt,
            instructions=system_prompt,
            model=model,
            model_settings={"max_tokens": 100},
        )
        humanized = result.output.strip()
        if humanized:
            logger.debug(
                f"Successfully humanized citation: '{citation_key}' -> '{humanized}'"
            )
            return humanized
    except Exception as e:
        logger.warning(f"Error generating citation: {e}")

    logger.error("Failed to humanize citation, using fallback")
    humanized = re.sub(r"([a-z])([A-Z])", r"\1 \2", citation_key)
    humanized = humanized.replace("_", ", ").replace("-", " ")
    return humanized


def _save_card_transcripts(
    card: PlainCard,
    card_index: int,
    card_uuid: str,
    citation_key: str | None,
    front_transcript: str,
    back_transcript: str,
    humanized_citation: str | None,
    audio_dir: Path,
) -> None:
    """Save card transcripts to markdown files for debugging."""
    transcripts_dir = audio_dir.parent / "complementary_transcripts"
    transcripts_dir.mkdir(parents=True, exist_ok=True)

    # Save front transcript
    front_transcript_filename = (
        f"{citation_key}_{card_uuid}_front.md"
        if citation_key
        else f"{card_uuid}_front.md"
    )
    front_transcript_path = transcripts_dir / front_transcript_filename
    with open(front_transcript_path, "w", encoding="utf-8") as f:
        f.write(f"# Card {card_index} - Front Transcript\n\n")
        f.write(f"**Card ID:** {card_uuid}\n\n")
        f.write(f"**Original Text:**\n{card.front.text}\n\n")
        if card.front.image_path:
            f.write(f"**Image Path:** {card.front.image_path}\n\n")
        if card.front.image_summary:
            f.write(f"**Image Summary:** {card.front.image_summary}\n\n")

        f.write("**Image Summary Debug:**\n")
        f.write(f"- Has image on front: {card.front.image_path is not None}\n")
        f.write(f"- Has image on back: {card.back.image_path is not None}\n")
        f.write(
            f"- Front image summary: {'Yes' if card.front.image_summary else 'No'}\n"
        )
        f.write(f"- Back image summary: {'Yes' if card.back.image_summary else 'No'}\n")
        f.write(
            f"- Image summary included in transcript: {'Yes' if any(phrase in front_transcript for phrase in ['Image description:', 'image description:']) else 'No'}\n\n"
        )

        f.write(f"**Generated Transcript:**\n{front_transcript}\n")

        if humanized_citation:
            f.write(f"\n**Citation Added:** {humanized_citation}\n")

    # Save back transcript
    if back_transcript:
        back_transcript_filename = (
            f"{citation_key}_{card_uuid}_back.md"
            if citation_key
            else f"{card_uuid}_back.md"
        )
        back_transcript_path = transcripts_dir / back_transcript_filename
        with open(back_transcript_path, "w", encoding="utf-8") as f:
            f.write(f"# Card {card_index} - Back Transcript\n\n")
            f.write(f"**Card ID:** {card_uuid}\n\n")
            f.write(
                f"**Original Text:**\n{card.back.text if '{{c' not in card.front.text else card.front.text}\n\n"
            )
            if card.back.image_path:
                f.write(f"**Image Path:** {card.back.image_path}\n\n")
            if card.back.image_summary:
                f.write(f"**Image Summary:** {card.back.image_summary}\n\n")
            f.write(f"**Generated Transcript:**\n{back_transcript}\n")


_MATH_RULES = (
    "For mathematical expressions, convert LaTeX notation to speakable form:\n"
    "- Fractions: \\frac{a}{b} as 'a over b', \\frac{1}{2} as 'one half'\n"
    "- Summations: \\sum_{i=1}^n as 'sum from i equals 1 to n'\n"
    "- Products: \\prod_{i=1}^n as 'product from i equals 1 to n'\n"
    "- Integrals: \\int_a^b as 'integral from a to b'\n"
    "- Bold symbols: \\mathbf{w} as 'vector w' or 'bold w'\n"
    "- Functions: f(x, y) as 'f of x and y'\n"
    "- Curly braces: \\{...\\} as 'the quantity...'\n"
    "- Square brackets: [a, b] as 'the interval from a to b'\n"
    "- Subscripts: X_j as 'X sub j', X_{parent} as 'X sub parent', X_i as 'X sub i'\n"
    "- Superscripts: X^2 as 'X squared', X^n as 'X to the n', X^{-1} as 'X inverse'\n"
    "- E[X | Y] as 'expected value of X given Y'\n"
    "- E(w) as 'E of w' (error function notation)\n"
    "- X^T as 'X transpose'\n"
    "- (I - W^T) as 'I minus W transpose'\n"
    "- g_j(f_j(X)) as 'g sub j of f sub j of X'\n"
    "- \\mid or | as 'given' in conditional expressions\n"
    "- \\text{} contents should be read normally\n"
    "- Matrix notation: X_1 to X_6 as 'X one to X six'\n"
    "- Greek letters: \\alpha as 'alpha', \\beta as 'beta', \\mathbf{w} as 'bold omega', etc.\n"
)


def _build_transcript_system_prompt(
    is_front: bool,
    is_cloze: bool,
    has_image: bool,
) -> str:
    """Build the system prompt for card transcript generation."""
    if is_front:
        if is_cloze:
            if has_image:
                image_instructions = (
                    "3. If the content includes 'Image description:' at the end, you MUST read it\n"
                    "   - Image description ALWAYS comes AFTER the main content\n"
                    "   - Read the image description exactly as provided\n"
                    "   - Only convert LaTeX/math notation to speakable form if present\n"
                    "4. Read ALL content in order: main cloze text first, then image description (if present)\n"
                    "5. The image description is crucial for audio-only learners - never skip it\n"
                    "6. CRITICAL: Image cards should NEVER be cloze cards (this is validated elsewhere)\n"
                )
            else:
                image_instructions = (
                    "3. This card has NO IMAGE - do not generate, imagine, or describe any images\n"
                    "4. Only read the text content provided - nothing more\n"
                )

            return (
                "Read this text exactly as written for audio. "
                "CRITICAL INSTRUCTIONS:\n"
                "1. Say 'blank' exactly where it appears in the text\n"
                "2. Do NOT try to figure out what the blank should be\n"
                f"{image_instructions}\n"
                "FORBIDDEN: Do NOT paraphrase, expand, elaborate, or explain the content\n\n"
                f"{_MATH_RULES}\n"
                "Remember: Include ALL content exactly as provided, especially image descriptions"
            )
        else:
            if has_image:
                image_instructions = (
                    "3. 'Image description:' ALWAYS appears at the end - read it exactly as provided:\n"
                    "   - Read the image description verbatim\n"
                    "   - Only convert LaTeX/math notation to speakable form if present\n"
                    "4. DO NOT answer the question or provide explanations\n"
                    "5. DO NOT skip the image description - it's crucial for audio-only learners\n"
                    "6. NEVER read tags (lines starting with # or - #)\n\n"
                    "Example structure: [Question as written]. [Image description as provided]\n"
                )
            else:
                image_instructions = (
                    "3. This card has NO IMAGE - do not generate, imagine, or describe any images\n"
                    "4. DO NOT answer the question or provide explanations\n"
                    "5. NEVER read tags (lines starting with # or - #)\n\n"
                    "Example structure: [Question as written]\n"
                )

            return (
                "Read this flashcard QUESTION exactly as written for audio. "
                "CRITICAL INSTRUCTIONS:\n"
                "1. This is the FRONT of a flashcard - read ALL content IN THE EXACT ORDER PROVIDED\n"
                "2. DO NOT rearrange the content - read it exactly as given\n"
                f"{image_instructions}\n"
                "FORBIDDEN: Do NOT paraphrase, expand, answer, explain, or elaborate on the question\n\n"
                "For mathematical expressions, convert LaTeX notation to speakable form:\n"
                "- Subscripts: X_j as 'X sub j', X_{parent} as 'X sub parent', X_i as 'X sub i'\n"
                "- Superscripts: X^2 as 'X squared', X^n as 'X to the n'\n"
                "- E[X | Y] as 'expected value of X given Y'\n"
                "- X^{-1} as 'X inverse' not 'X to the power of minus one'\n"
                "- X^T as 'X transpose'\n"
                "- (I - W^T) as 'I minus W transpose'\n"
                "- (I - W^T)^{-1} as 'the inverse of I minus W transpose'\n"
                "- f_2((I - W^T)^{-1}) as 'f two of the inverse of I minus W transpose'\n"
                "- g_j(f_j(X)) as 'g sub j of f sub j of X'\n"
                "- F(W) as 'F of W'\n"
                "- \\mid or | as 'given' in conditional expressions\n"
                "- \\text{} contents should be read normally\n"
                "- Matrix notation: X_1 to X_6 as 'X one to X six'\n"
                "- \\sum as 'sum', \\prod as 'product', \\int as 'integral'\n"
                "- Greek letters: \\alpha as 'alpha', \\beta as 'beta', etc.\n"
                "- Parentheses in math: \\(F(W)\\) as 'F of W'\n\n"
                "Remember: This is a QUESTION only - read it verbatim, do not provide the answer!"
            )
    else:
        # Back of card
        if is_cloze:
            return (
                "Read this complete text exactly as written for audio. "
                "This is the ANSWER that reveals what was hidden in the blanks. "
                "IMPORTANT: The text has already been processed to remove cloze markers. "
                "Do NOT say 'blank' - read all the words that are present. "
                "Read it as a complete statement with all words revealed.\n\n"
                "FORBIDDEN: Do NOT paraphrase, expand, elaborate, or explain the content\n\n"
                "CRITICAL: Convert ALL mathematical notation to spoken form:\n"
                "- \\(F(W)\\) -> 'F of W'\n"
                "- \\(h(W)=0\\) -> 'h of W equals zero'\n"
                "- \\(E[X_j \\mid X_{pa(j)}]\\) -> 'expected value of X sub j given X sub parent of j'\n"
                "- \\(g_j(f_j(X))\\) -> 'g sub j of f sub j of X'\n"
                "- \\(\\mathbb{E}[X_j \\mid X_{pa(j)}]\\) -> 'expected value of X sub j given X sub parent of j'\n"
                "- Any expression like \\(...\\) or $...$ MUST be converted to words\n"
                "- NEVER output raw LaTeX like '\\(F(W)\\)' - always convert to words\n\n"
                "General rules:\n"
                "- Subscripts: X_j as 'X sub j'\n"
                "- Superscripts: X^2 as 'X squared', X^{-1} as 'X inverse'\n"
                "- Greek letters: \\alpha as 'alpha', \\beta as 'beta', etc.\n"
            )
        else:
            if has_image:
                image_instructions = (
                    "3. 'Image description:' ALWAYS appears at the end - read it exactly as provided:\n"
                    "   - Read the image description verbatim\n"
                    "   - Only convert LaTeX/math notation to speakable form if present\n"
                    "4. CRITICAL: NEVER read tags (lines starting with # or - #)\n"
                )
            else:
                image_instructions = (
                    "3. This card has NO IMAGE - do not generate, imagine, or describe any images\n"
                    "4. CRITICAL: NEVER read tags (lines starting with # or - #)\n"
                )

            return (
                "Read this answer exactly as written for audio. "
                "CRITICAL INSTRUCTIONS:\n"
                "1. Read ALL content IN THE EXACT ORDER PROVIDED\n"
                "2. DO NOT rearrange the content - read it exactly as given\n"
                f"{image_instructions}\n"
                "FORBIDDEN: Do NOT paraphrase, expand, elaborate, or explain the content\n\n"
                f"{_MATH_RULES}"
            )
