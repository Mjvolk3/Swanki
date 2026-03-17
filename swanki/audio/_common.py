"""
swanki/audio/_common.py
[[swanki.audio._common]]
https://github.com/Mjvolk3/Swanki/tree/main/swanki/audio/_common.py

Shared TTS utilities: chunking, speech synthesis, audio combination, and metadata filtering.
"""

import logging
import re
from collections.abc import Sequence
from pathlib import Path
from typing import Literal

import httpx
from elevenlabs import ElevenLabs, VoiceSettings
from pydub import AudioSegment

logger = logging.getLogger(__name__)

DEFAULT_VOICE_ID = "7p1Ofvcwsv7UBPoFNcpI"
DEFAULT_TTS_MODEL = "eleven_flash_v2_5"
LECTURE_TTS_MODEL = "eleven_multilingual_v2"


def clean_markdown_for_tts(text: str) -> str:
    """Remove markdown formatting that interferes with TTS.

    Strips headers, bold, italics, links, inline code, horizontal rules,
    and blockquote markers while preserving the underlying text content.

    Args:
        text: Markdown text to clean.

    Returns:
        Plain text suitable for TTS.
    """
    cleaned = text
    cleaned = re.sub(r"^#{1,6}\s+", "", cleaned, flags=re.MULTILINE)
    cleaned = re.sub(r"\*\*(.*?)\*\*", r"\1", cleaned)
    cleaned = re.sub(r"\*(.*?)\*", r"\1", cleaned)
    cleaned = re.sub(r"\[(.*?)\]\(.*?\)", r"\1", cleaned)
    cleaned = re.sub(r"`([^`]+)`", r"\1", cleaned)
    cleaned = re.sub(r"^[\-\*\_]{3,}\s*$", "", cleaned, flags=re.MULTILINE)
    cleaned = re.sub(r"^>\s+", "", cleaned, flags=re.MULTILINE)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    return cleaned.strip()


def add_tts_pauses(text: str) -> str:
    """Insert SSML break tags for natural TTS pacing.

    Adds ``<break>`` tags at paragraph boundaries and after
    section transition sentences. Works with ElevenLabs v2 models
    which support ``<break time="X.Xs" />``.

    Args:
        text: Cleaned transcript text (already TTS-ready).

    Returns:
        Text with SSML break tags inserted.
    """
    # Add short pause between paragraphs (0.7s — noticeable but not jarring)
    text = re.sub(r"\n\n+", '\n\n<break time="0.7s" />\n\n', text)

    # Add pause after colon at end of a line (often introduces a list or concept)
    text = re.sub(r":\s*\n", ':\n<break time="0.4s" />\n', text)

    # Collapse any double breaks that got stacked
    text = re.sub(
        r'(<break time="[^"]*" />\s*){2,}',
        '<break time="0.7s" />\n\n',
        text,
    )

    return text


def chunk_text(text: str, max_chars: int = 3000) -> list[str]:
    """Split text into chunks at paragraph and sentence boundaries.

    Args:
        text: Text to split into chunks.
        max_chars: Maximum characters per chunk.

    Returns:
        List of text chunks.
    """
    paragraphs = text.split("\n\n")
    chunks: list[str] = []
    current = ""

    for p in paragraphs:
        if len(current) + len(p) + 2 <= max_chars:
            current = (current + "\n\n" + p).strip()
        else:
            if current:
                chunks.append(current)
            if len(p) <= max_chars:
                current = p
            else:
                sentences = re.split(r"(?<=[.!?]) +", p)
                part = ""
                for s in sentences:
                    if len(part) + len(s) + 1 <= max_chars:
                        part = (part + " " + s).strip()
                    else:
                        chunks.append(part)
                        part = s
                if part:
                    chunks.append(part)
                current = ""

    if current:
        chunks.append(current)

    return chunks


def chunk_text_paragraphs(text: str, max_chars: int = 4500) -> list[str]:
    """Split text at paragraph boundaries only — never mid-sentence.

    Designed for lecture TTS where prosody continuity within paragraphs
    is critical. Each paragraph stays intact; only paragraph breaks are
    used as split points. Uses a larger default max_chars to keep
    coherent passages together.

    Args:
        text: Text to split into chunks.
        max_chars: Maximum characters per chunk.

    Returns:
        List of text chunks, each containing one or more full paragraphs.
    """
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks: list[str] = []
    current = ""

    for p in paragraphs:
        if not current:
            current = p
        elif len(current) + len(p) + 2 <= max_chars:
            current = current + "\n\n" + p
        else:
            chunks.append(current)
            current = p

    if current:
        chunks.append(current)

    return chunks


def text_to_speech(
    text: str,
    voice_id: str,
    output_path: Path,
    api_key: str,
    speed: float = 1.0,
    tts_model: str = DEFAULT_TTS_MODEL,
) -> None:
    """Convert text to speech via ElevenLabs and save as MP3.

    Args:
        text: Text to convert to speech.
        voice_id: ElevenLabs voice ID.
        output_path: Path for the output MP3 file.
        api_key: ElevenLabs API key.
        speed: Playback speed multiplier (uses FFmpeg atempo).
        tts_model: ElevenLabs model ID. Defaults to flash_v2_5 (cheap, fast).
            Use LECTURE_TTS_MODEL for premium quality.
    """
    httpx_client = httpx.Client(timeout=httpx.Timeout(300.0, connect=60.0))

    client = ElevenLabs(api_key=api_key, httpx_client=httpx_client)

    settings = VoiceSettings(
        stability=0.5,
        similarity_boost=0.75,
        style=0.2,
        use_speaker_boost=True,
    )

    stream = client.text_to_speech.convert(
        text=text,
        voice_id=voice_id,
        model_id=tts_model,
        output_format="mp3_44100_192",
        voice_settings=settings,
    )

    data: bytes = b"".join(stream) if hasattr(stream, "__iter__") else stream  # type: ignore[arg-type]

    if speed != 1.0:
        temp_path = output_path.with_suffix(".temp.mp3")
        with open(temp_path, "wb") as f:
            f.write(data)

        audio = AudioSegment.from_mp3(temp_path)

        atempo_filters: list[str] = []
        remaining_speed = speed

        # FFmpeg atempo only accepts 0.5-2.0; chain filters for wider range
        while remaining_speed < 0.5 or remaining_speed > 2.0:
            if remaining_speed < 0.5:
                atempo_filters.append("atempo=0.5")
                remaining_speed = remaining_speed / 0.5
            else:
                atempo_filters.append("atempo=2.0")
                remaining_speed = remaining_speed / 2.0

        if remaining_speed != 1.0:
            atempo_filters.append(f"atempo={remaining_speed}")

        if atempo_filters:
            filter_chain = ",".join(atempo_filters)
            full_filter_chain = f"{filter_chain},apad=pad_dur=0.1"
            audio.export(
                output_path,
                format="mp3",
                parameters=[
                    "-filter:a",
                    full_filter_chain,
                    "-avoid_negative_ts",
                    "make_zero",
                    "-loglevel",
                    "error",
                ],
            )
        else:
            audio.export(output_path, format="mp3")

        temp_path.unlink()
    else:
        with open(output_path, "wb") as f:
            f.write(data)


def combine_audio(
    files: list[Path],
    output: Path,
    crossfade_ms: int = 200,
    first_crossfade_ms: int | None = None,
) -> None:
    """Combine multiple MP3 files into one with crossfade transitions.

    Args:
        files: MP3 files to combine in order.
        output: Path for the combined output file.
        crossfade_ms: Crossfade duration in milliseconds.
        first_crossfade_ms: Override crossfade for the first transition.
    """
    if not files:
        logger.error("No audio files provided to combine_audio")
        return

    segments = [AudioSegment.from_mp3(str(f)) for f in files]
    if not segments:
        logger.error("No audio segments could be loaded")
        return

    combined = segments[0]

    for i, seg in enumerate(segments[1:]):
        fade_duration = (
            first_crossfade_ms
            if i == 0 and first_crossfade_ms is not None
            else crossfade_ms
        )
        combined = combined.append(seg, crossfade=fade_duration)

    combined.export(str(output), format="mp3", bitrate="192k")


def validate_audio_file(
    audio_path: Path,
    min_size: int = 1024,
    expected_content: str = "",
) -> bool:
    """Check that an audio file exists, has reasonable size, and is loadable.

    Args:
        audio_path: Path to the audio file.
        min_size: Minimum file size in bytes.
        expected_content: Label for log messages.

    Returns:
        True if the file passes all checks.
    """
    if not audio_path.exists():
        logger.warning(f"Audio file does not exist: {audio_path}")
        return False

    file_size = audio_path.stat().st_size
    if file_size < min_size:
        logger.warning(f"Audio file too small ({file_size} bytes): {audio_path}")
        return False

    try:
        audio = AudioSegment.from_mp3(str(audio_path))
        duration_ms = len(audio)

        if duration_ms < 500:
            logger.warning(
                f"Audio too short ({duration_ms}ms) for content '{expected_content}': {audio_path}"
            )
            return False

        if duration_ms > 10000:
            logger.warning(
                f"Audio too long ({duration_ms}ms) for citation '{expected_content}': {audio_path}"
            )
            return False

        logger.debug(
            f"Audio validation passed: {audio_path} ({duration_ms}ms, {file_size} bytes)"
        )
        return True

    except Exception as e:
        logger.error(f"Failed to load audio file {audio_path}: {e}")
        return False


def filter_metadata(content: str) -> str:
    """Remove academic paper metadata (authors, affiliations, references).

    Filters section-level blocks (References, Acknowledgments, Author info)
    and individual lines (emails, affiliations, postal addresses).

    Args:
        content: Raw markdown content from an academic paper.

    Returns:
        Content with metadata removed.
    """
    lines = content.split("\n")
    filtered_lines: list[str] = []
    skip_mode = False

    skip_patterns = [
        r"^##?\s*References?\s*$",
        r"^##?\s*Competing\s+interests?\s*$",
        r"^##?\s*Author\s+",
        r"^##?\s*Acknowledg(?:e)?ments?\s*$",
        r"^\\author\{",
        r"^\s*e-mail:",
        r"Published online:",
        r"https://doi\.org/",
        r"^\\title\{",
        r"^\\end\{document\}",
        r"^\s*\d+\.\s+[A-Z][a-z]+,\s+[A-Z]\.",
    ]

    inline_skip_patterns = [
        r"^\s*\$?\^?\{?[0-9]+\}?\$?\s*Department of",
        r"^\s*\*?\s*[A-Z][a-z]+ [A-Z]\. [A-Z][a-z]+\s+\(",
        r"\S+@\S+\.\S+",
        r"^\s*(?:Department|School|Institute|Faculty|Center|Centre)\s+of\b",
        r"^\s*(?:University|College|Laboratory|Lab)\s+of\b",
        r"^\s*\d{1,3}\s+[A-Z][a-z]+\s+(?:Street|Avenue|Road|Boulevard|Drive)",
        r"^\s*(?:Received|Accepted|Revised|Published)\s*:?\s*\d",
        r"^\s*(?:Correspondence|Corresponding author)",
    ]

    for line in lines:
        if any(re.search(pattern, line, re.IGNORECASE) for pattern in skip_patterns):
            skip_mode = True
            continue

        if line.strip().startswith("\\bibitem") or line.strip().startswith(
            "\\begin{thebibliography}"
        ):
            skip_mode = True
            continue

        if line.startswith("##") and skip_mode:
            if not any(
                re.search(pattern, line, re.IGNORECASE) for pattern in skip_patterns
            ):
                skip_mode = False

        if not skip_mode:
            if not any(re.search(p, line) for p in inline_skip_patterns):
                filtered_lines.append(line)

    return "\n".join(filtered_lines)


# ---------------------------------------------------------------------------
# Section-aware audio infrastructure
# ---------------------------------------------------------------------------

SECTION_BREAK_MARKER = "---SECTION_BREAK---"


def generate_silence(duration_ms: int, output_path: Path) -> Path:
    """Create a silent MP3 file.

    Args:
        duration_ms: Duration of silence in milliseconds.
        output_path: Path for the output MP3 file.

    Returns:
        The output path.
    """
    AudioSegment.silent(duration=duration_ms).export(str(output_path), format="mp3")
    return output_path


def split_transcript_by_sections(
    transcript: str, marker: str = SECTION_BREAK_MARKER
) -> list[str]:
    """Split transcript text on a marker, stripping whitespace and filtering empties.

    Args:
        transcript: Transcript text with section break markers.
        marker: The marker string to split on.

    Returns:
        List of non-empty section strings.
    """
    return [s.strip() for s in transcript.split(marker) if s.strip()]


def combine_audio_with_section_pauses(
    sections: Sequence[list[Path]],
    output: Path,
    section_pause_ms: int = 2000,
    chunk_crossfade_ms: int = 200,
    bookend_start: Path | None = None,
    bookend_end: Path | None = None,
    bookend_pause_ms: int = 500,
) -> None:
    """Combine audio chunks grouped by section with real silence between sections.

    Args:
        sections: List of chunk-path lists, one list per section.
        output: Path for the combined output file.
        section_pause_ms: Silence duration between sections.
        chunk_crossfade_ms: Crossfade duration between chunks within a section.
        bookend_start: Optional start bookend audio file.
        bookend_end: Optional end bookend audio file.
        bookend_pause_ms: Silence after start bookend / before end bookend.
    """
    if not sections:
        logger.error("No sections provided to combine_audio_with_section_pauses")
        return

    combined: AudioSegment | None = None

    # Start bookend
    if bookend_start and bookend_start.exists():
        combined = AudioSegment.from_mp3(str(bookend_start))
        combined += AudioSegment.silent(duration=bookend_pause_ms)

    for sec_idx, section_chunks in enumerate(sections):
        if not section_chunks:
            continue

        # Build section audio from chunks with crossfade
        section_audio = AudioSegment.from_mp3(str(section_chunks[0]))
        for chunk_path in section_chunks[1:]:
            section_audio = section_audio.append(
                AudioSegment.from_mp3(str(chunk_path)), crossfade=chunk_crossfade_ms
            )

        # Append section with silence gap (except before first section)
        if combined is None:
            combined = section_audio
        else:
            combined += AudioSegment.silent(duration=section_pause_ms)
            combined += section_audio

    if combined is None:
        logger.error("No audio content to combine")
        return

    # End bookend
    if bookend_end and bookend_end.exists():
        combined += AudioSegment.silent(duration=bookend_pause_ms)
        combined += AudioSegment.from_mp3(str(bookend_end))

    combined.export(str(output), format="mp3", bitrate="192k")


def generate_bookend_audio(
    citation_key: str,
    audio_type: Literal["transcript", "summary", "lecture"],
    position: Literal["start", "end"],
    output_dir: Path,
    elevenlabs_api_key: str,
    voice_id: str,
    speed: float = 1.0,
    paper_title: str | None = None,
) -> Path:
    """Generate a short bookend announcement audio clip.

    Args:
        citation_key: Raw citation key (will be humanized).
        audio_type: Type of audio being bookended.
        position: Whether this is a start or end bookend.
        output_dir: Directory to cache the bookend file.
        elevenlabs_api_key: ElevenLabs API key.
        voice_id: ElevenLabs voice ID.
        speed: Playback speed multiplier.
        paper_title: Paper title for lecture start bookends.

    Returns:
        Path to the generated bookend MP3.
    """
    from ..utils.formatting import humanize_citation_key

    humanized = humanize_citation_key(citation_key)
    cache_path = output_dir / f"{citation_key}_{audio_type}_{position}.mp3"

    if audio_type == "lecture":
        if position == "start":
            title_part = f" We are covering: {paper_title}." if paper_title else ""
            text = f"Today's lecture is posted as: {humanized}.{title_part}"
        else:
            text = f"And with that we conclude: {humanized}."
    else:
        label = position.upper()
        text = f"{label}: {humanized}."

    output_dir.mkdir(parents=True, exist_ok=True)
    text_to_speech(text, voice_id, cache_path, elevenlabs_api_key, speed)
    return cache_path


def extract_acronyms(text: str) -> dict[str, str]:
    """Extract acronym definitions from text.

    Scans for patterns like ``ACRONYM (Full Form)`` and ``Full Form (ACRONYM)``.

    Args:
        text: Source text to scan.

    Returns:
        Dict mapping acronym to its expansion, e.g. ``{"FSEOF": "flux scanning..."}``.
    """
    acronyms: dict[str, str] = {}

    # Pattern 1: ACRONYM (Full Form)  e.g. "FSEOF (flux scanning based on ...)"
    for m in re.finditer(r"\b([A-Z]{2,})\s*\(([^)]{5,})\)", text):
        acr, full = m.group(1), m.group(2).strip()
        # Skip if the "full form" is all-caps (not really an expansion)
        if not full.isupper():
            acronyms[acr] = full

    # Pattern 2: Full Form (ACRONYM)  e.g. "flux scanning ... (FSEOF)"
    for m in re.finditer(r"([A-Za-z][^(]{4,}?)\s*\(([A-Z]{2,})\)", text):
        full, acr = m.group(1).strip(), m.group(2)
        if acr not in acronyms and not full.isupper():
            acronyms[acr] = full

    return acronyms
