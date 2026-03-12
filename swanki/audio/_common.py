"""
swanki/audio/_common.py
[[swanki.audio._common]]
https://github.com/Mjvolk3/Swanki/tree/main/swanki/audio/_common.py

Shared TTS utilities: chunking, speech synthesis, audio combination, and metadata filtering.
"""

import logging
import re
from pathlib import Path

import httpx
from elevenlabs import ElevenLabs, VoiceSettings
from pydub import AudioSegment

logger = logging.getLogger(__name__)

DEFAULT_VOICE_ID = "7p1Ofvcwsv7UBPoFNcpI"


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


def text_to_speech(
    text: str,
    voice_id: str,
    output_path: Path,
    api_key: str,
    speed: float = 1.0,
) -> None:
    """Convert text to speech via ElevenLabs and save as MP3.

    Args:
        text: Text to convert to speech.
        voice_id: ElevenLabs voice ID.
        output_path: Path for the output MP3 file.
        api_key: ElevenLabs API key.
        speed: Playback speed multiplier (uses FFmpeg atempo).
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
        model_id="eleven_multilingual_v2",
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
