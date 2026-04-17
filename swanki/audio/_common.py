"""
swanki/audio/_common.py
[[swanki.audio._common]]
https://github.com/Mjvolk3/Swanki/tree/main/swanki/audio/_common.py

Shared TTS utilities: chunking, speech synthesis, audio combination, and metadata filtering.
"""

import json
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


def add_tts_pauses(text: str, provider: str = "elevenlabs") -> str:
    """Insert pause markers for natural TTS pacing.

    For ElevenLabs, inserts SSML ``<break>`` tags.
    For Fish Speech, inserts inline ``[pause]`` / ``[short pause]`` tags.

    Args:
        text: Cleaned transcript text (already TTS-ready).
        provider: TTS provider name.

    Returns:
        Text with pause markers inserted.
    """
    if provider == "fish_speech":
        text = re.sub(r"\n\n+", "\n\n[pause]\n\n", text)
        text = re.sub(r":\s*\n", ":\n[short pause]\n", text)
        # Add pause after sentences ending with period followed by newline
        text = re.sub(r"\.\s*\n", ".\n[short pause]\n", text)
        # Collapse stacked tags
        text = re.sub(r"(\[pause\]\s*){2,}", "[pause]\n\n", text)
        text = re.sub(r"(\[short pause\]\s*){2,}", "[short pause]\n", text)
    else:
        text = re.sub(r"\n\n+", '\n\n<break time="0.7s" />\n\n', text)
        text = re.sub(r":\s*\n", ':\n<break time="0.4s" />\n', text)
        text = re.sub(
            r'(<break time="[^"]*" />\s*){2,}',
            '<break time="0.7s" />\n\n',
            text,
        )

    return text


def append_chunk_pause(text: str, provider: str = "elevenlabs") -> str:
    """Append a trailing pause tag to a TTS chunk.

    Ensures each chunk's audio ends with a natural pause so direct
    concatenation of chunks sounds seamless. Idempotent: returns the
    text unchanged when a trailing pause tag is already present.

    Args:
        text: Chunk text to append a pause to.
        provider: TTS provider name (``"fish_speech"`` or ``"elevenlabs"``).

    Returns:
        Text with a trailing pause tag appended (or unchanged if already
        present).
    """
    text = text.rstrip()
    if provider == "fish_speech":
        if not text.endswith("[long pause]"):
            text += " [long pause]"
    else:
        # Any trailing self-closing SSML tag (commonly <break.../>) is treated
        # as an existing pause and not stacked. This is intentional.
        if not text.endswith("/>"):
            text += ' <break time="1.0s" />'
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
    """Split text at paragraph boundaries, falling back to sentences.

    Designed for lecture TTS where prosody continuity within paragraphs
    is critical. Splits preferentially at paragraph breaks. Any single
    paragraph that exceeds ``max_chars`` is further split at sentence
    boundaries so no chunk is ever larger than ``max_chars``.

    Args:
        text: Text to split into chunks.
        max_chars: Maximum characters per chunk.

    Returns:
        List of text chunks.
    """
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]

    # Pre-split any paragraph that is itself too large at sentence boundaries.
    split_paragraphs: list[str] = []
    for p in paragraphs:
        if len(p) <= max_chars:
            split_paragraphs.append(p)
            continue
        # Split at sentence boundaries (period/!/? followed by space)
        sentences = re.split(r"(?<=[.!?])\s+", p)
        current_sent = ""
        for s in sentences:
            if not current_sent:
                current_sent = s
            elif len(current_sent) + len(s) + 1 <= max_chars:
                current_sent = current_sent + " " + s
            else:
                split_paragraphs.append(current_sent)
                current_sent = s
        if current_sent:
            split_paragraphs.append(current_sent)

    chunks: list[str] = []
    current = ""

    for p in split_paragraphs:
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


def _strip_ssml(text: str) -> str:
    """Remove SSML break tags that Fish Speech cannot handle."""
    return re.sub(r'<break[^>]*/?\s*>', '', text)


def _apply_speed(data: bytes, output_path: Path, speed: float) -> None:
    """Write audio bytes to output_path, applying FFmpeg atempo if speed != 1.0."""
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


def _tts_elevenlabs(
    text: str,
    voice_id: str,
    output_path: Path,
    api_key: str,
    speed: float,
    tts_model: str,
) -> None:
    """ElevenLabs TTS backend."""
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
    _apply_speed(data, output_path, speed)


_FISH_SPEECH_PORTS = [8080, 8081, 8082, 8083]

# Thread-safe round-robin state for multi-server distribution
import threading as _threading

_server_lock = _threading.Lock()
_server_index = 0
_healthy_servers: list[str] = []
_servers_discovered = False


def _discover_fish_speech_servers(base_url: str, force: bool = False) -> list[str]:
    """Discover all healthy Fish Speech servers, with caching.

    Re-discovers if the cached list has fewer servers than available ports,
    allowing late-starting servers to be picked up.
    """
    global _healthy_servers, _servers_discovered

    if _servers_discovered and not force and len(_healthy_servers) >= len(_FISH_SPEECH_PORTS):
        return _healthy_servers

    from urllib.parse import urlparse

    parsed = urlparse(base_url)
    host = f"{parsed.scheme}://{parsed.hostname}"

    healthy: list[str] = []
    for port in _FISH_SPEECH_PORTS:
        url = f"{host}:{port}"
        try:
            r = httpx.get(f"{url}/v1/health", timeout=10.0)
            if r.status_code == 200:
                healthy.append(url)
        except httpx.HTTPError:
            continue

    if not healthy:
        healthy = [base_url]

    if not _servers_discovered or len(healthy) > len(_healthy_servers):
        logger.info(f"Discovered {len(healthy)} Fish Speech server(s): {healthy}")

    _healthy_servers = healthy
    _servers_discovered = True
    return healthy


def _pick_fish_speech_server(base_url: str) -> str:
    """Round-robin across healthy Fish Speech servers (thread-safe)."""
    global _server_index

    servers = _discover_fish_speech_servers(base_url)

    with _server_lock:
        server = servers[_server_index % len(servers)]
        _server_index += 1

    return server


def _tts_fish_speech(
    text: str,
    output_path: Path,
    server_url: str,
    reference_id: str | None,
    temperature: float,
    audio_format: str,
    speed: float,
) -> None:
    """Fish Speech S2 Pro TTS backend."""
    clean_text = _strip_ssml(text)

    payload: dict = {
        "text": clean_text,
        "format": audio_format,
        "temperature": temperature,
        "streaming": False,
        "chunk_length": 200,
        "max_new_tokens": 4096,
    }
    if reference_id:
        payload["reference_id"] = reference_id

    url = _pick_fish_speech_server(server_url)
    client = httpx.Client(timeout=httpx.Timeout(1800.0, connect=60.0))
    response = client.post(f"{url}/v1/tts", json=payload)
    assert response.status_code == 200, (
        f"Fish Speech TTS failed: {response.status_code} {response.text}"
    )

    _apply_speed(response.content, output_path, speed)


def ensure_fish_speech_reference(
    server_url: str,
    reference_id: str,
    audio_path: Path,
    text: str,
) -> None:
    """Register a voice reference with Fish Speech if not already present.

    Args:
        server_url: Fish Speech server URL.
        reference_id: Name to register the reference under.
        audio_path: Path to the reference WAV file.
        text: Transcription of the reference audio.
    """
    client = httpx.Client(timeout=httpx.Timeout(30.0, connect=10.0))

    # Check if already registered
    resp = client.get(
        f"{server_url}/v1/references/list",
        headers={"Accept": "application/json"},
    )
    assert resp.status_code == 200, f"Failed to list references: {resp.text}"
    data = resp.json()
    existing = data.get("reference_ids", [])
    if reference_id in existing:
        logger.info(f"Fish Speech reference '{reference_id}' already registered")
        return

    # Register new reference
    assert audio_path.exists(), f"Reference audio not found: {audio_path}"
    resp = client.post(
        f"{server_url}/v1/references/add",
        files={"audio": (audio_path.name, audio_path.read_bytes(), "audio/wav")},
        data={"id": reference_id, "text": text},
    )
    assert resp.status_code == 200, (
        f"Failed to register reference: {resp.status_code} {resp.text}"
    )
    logger.info(f"Registered Fish Speech reference '{reference_id}'")


def text_to_speech(
    text: str,
    voice_id: str,
    output_path: Path,
    api_key: str,
    speed: float = 1.0,
    tts_model: str = DEFAULT_TTS_MODEL,
    **tts_kwargs: object,
) -> None:
    """Convert text to speech and save as MP3.

    Dispatches to ElevenLabs or Fish Speech based on the ``provider`` key
    in *tts_kwargs*. When ``provider`` is absent or ``"elevenlabs"``, the
    positional *voice_id* / *api_key* / *tts_model* args are used. When
    ``provider`` is ``"fish_speech"``, the relevant kwargs are
    ``server_url``, ``reference_id``, ``temperature``, and ``format``.

    Args:
        text: Text to convert to speech.
        voice_id: ElevenLabs voice ID (ignored for fish_speech).
        output_path: Path for the output MP3 file.
        api_key: ElevenLabs API key (ignored for fish_speech).
        speed: Playback speed multiplier (uses FFmpeg atempo).
        tts_model: ElevenLabs model ID.
        **tts_kwargs: Provider-specific options (provider, server_url, etc.).
    """
    provider = str(tts_kwargs.get("provider", "elevenlabs"))

    if provider == "fish_speech":
        _tts_fish_speech(
            text=text,
            output_path=output_path,
            server_url=str(tts_kwargs.get("server_url", "http://localhost:8080")),
            reference_id=tts_kwargs.get("reference_id"),  # type: ignore[arg-type]
            temperature=float(tts_kwargs.get("temperature", 0.8)),
            audio_format=str(tts_kwargs.get("format", "mp3")),
            speed=speed,
        )
    else:
        _tts_elevenlabs(text, voice_id, output_path, api_key, speed, tts_model)


def tts_chunks_parallel(
    chunks: list[tuple[str, Path]],
    voice_id: str,
    api_key: str,
    speed: float = 1.0,
    tts_model: str = DEFAULT_TTS_MODEL,
    **tts_kwargs: object,
) -> list[Path]:
    """Process multiple TTS chunks in parallel across Fish Speech servers.

    Each chunk is sent to a different server via round-robin. Results are
    returned in the same order as the input chunks.

    Args:
        chunks: List of (text, output_path) pairs.
        voice_id: Voice ID (ignored for fish_speech).
        api_key: API key (ignored for fish_speech).
        speed: Playback speed multiplier.
        tts_model: TTS model ID.
        **tts_kwargs: Provider-specific options.

    Returns:
        List of output paths in input order.
    """
    from concurrent.futures import ThreadPoolExecutor

    num_servers = len(_discover_fish_speech_servers(
        str(tts_kwargs.get("server_url", "http://localhost:8080"))
    ))
    max_workers = min(len(chunks), num_servers)

    def _process(args: tuple[str, Path]) -> Path:
        text, output_path = args
        text_to_speech(text, voice_id, output_path, api_key, speed, tts_model, **tts_kwargs)
        return output_path

    if max_workers <= 1:
        return [_process(c) for c in chunks]

    logger.info(f"Processing {len(chunks)} TTS chunks in parallel across {max_workers} servers")
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        results = list(pool.map(_process, chunks))

    return results


def combine_audio(
    files: list[Path],
    output: Path,
    crossfade_ms: int = 0,
    first_crossfade_ms: int | None = None,
) -> None:
    """Combine multiple MP3 files into one with optional crossfade transitions.

    Defaults to direct concatenation (``crossfade_ms=0``) so chunk-level
    pauses generated by the TTS provider are preserved untouched.

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
    chunk_crossfade_ms: int = 0,
    bookend_start: Path | None = None,
    bookend_end: Path | None = None,
    bookend_pause_ms: int = 500,
) -> None:
    """Combine audio chunks grouped by section with real silence between sections.

    Defaults to direct concatenation between chunks (``chunk_crossfade_ms=0``)
    so trailing pauses generated by the TTS provider supply natural transitions.

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


def write_chunk_manifest(
    chunks_dir: Path,
    audio_type: str,
    output_file: str,
    chunks: list[dict],
    bookend_start: str | None = None,
    bookend_end: str | None = None,
) -> Path:
    """Write a chunk manifest JSON for surgical regeneration.

    Args:
        chunks_dir: Directory containing chunk files.
        audio_type: One of ``"lecture"``, ``"reading"``, ``"summary"``, ``"card"``.
        output_file: Filename of the combined output audio.
        chunks: List of dicts with keys ``index``, ``section``, ``text``, ``file``.
        bookend_start: Filename of start bookend, if any.
        bookend_end: Filename of end bookend, if any.

    Returns:
        Path to the written manifest file.
    """
    manifest = {
        "audio_type": audio_type,
        "output_file": output_file,
        "bookend_start": bookend_start,
        "bookend_end": bookend_end,
        "chunks": chunks,
    }
    manifest_path = chunks_dir / "chunk_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2))
    logger.info(f"Wrote chunk manifest: {manifest_path} ({len(chunks)} chunks)")
    return manifest_path


def restitch_from_chunks(
    manifest_path: Path,
    output_path: Path,
    section_pause_ms: int = 2000,
    bookend_pause_ms: int = 500,
) -> None:
    """Reassemble final audio from chunk files using a manifest.

    Reads the chunk manifest JSON, loads each chunk file, and combines
    them with section pauses. Used for surgical regeneration: re-TTS one
    chunk, then restitch.

    Args:
        manifest_path: Path to ``chunk_manifest.json``.
        output_path: Path for the reassembled output MP3.
        section_pause_ms: Silence between sections.
        bookend_pause_ms: Silence after start / before end bookend.
    """
    manifest = json.loads(manifest_path.read_text())
    chunks_dir = manifest_path.parent

    sections: dict[int, list[Path]] = {}
    for chunk in manifest["chunks"]:
        sec = chunk["section"]
        if sec not in sections:
            sections[sec] = []
        chunk_path = chunks_dir / chunk["file"]
        assert chunk_path.exists(), f"Chunk file missing: {chunk_path}"
        sections[sec].append(chunk_path)

    section_lists = [sections[k] for k in sorted(sections.keys())]

    bookend_start = None
    bookend_end = None
    if manifest.get("bookend_start"):
        bookend_start = chunks_dir / manifest["bookend_start"]
    if manifest.get("bookend_end"):
        bookend_end = chunks_dir / manifest["bookend_end"]

    combine_audio_with_section_pauses(
        section_lists,
        output_path,
        section_pause_ms=section_pause_ms,
        chunk_crossfade_ms=0,
        bookend_start=bookend_start,
        bookend_end=bookend_end,
        bookend_pause_ms=bookend_pause_ms,
    )
    logger.info(
        f"Restitched audio from {sum(len(s) for s in section_lists)} chunks -> {output_path}"
    )


def generate_bookend_audio(
    citation_key: str,
    audio_type: Literal["transcript", "summary", "lecture"],
    position: Literal["start", "end"],
    output_dir: Path,
    elevenlabs_api_key: str,
    voice_id: str,
    speed: float = 1.0,
    paper_title: str | None = None,
    **tts_kwargs: object,
) -> Path:
    """Generate a short bookend announcement audio clip.

    Args:
        citation_key: Raw citation key (will be humanized).
        audio_type: Type of audio being bookended.
        position: Whether this is a start or end bookend.
        output_dir: Directory to cache the bookend file.
        elevenlabs_api_key: ElevenLabs API key.
        voice_id: Voice ID.
        speed: Playback speed multiplier.
        paper_title: Paper title for lecture start bookends.
        **tts_kwargs: Provider-specific options passed to text_to_speech.

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
    text_to_speech(text, voice_id, cache_path, elevenlabs_api_key, speed, **tts_kwargs)
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


# ---------------------------------------------------------------------------
# LaTeX humanization for TTS
# ---------------------------------------------------------------------------

_LATEX_SYSTEM_PROMPT = """You are a LaTeX-to-text converter for academic audio transcripts.

YOUR ONLY JOB: Convert ALL LaTeX notation to natural readable text.

CRITICAL RULES:
1. Convert EVERY LaTeX expression to spoken form
2. Remove ALL dollar signs ($), backslashes (\\), and curly braces ({})
3. NEVER output any LaTeX syntax in your response

CONVERSIONS (apply ALL of these):

Greek Letters (always convert):
- $\\alpha$ -> alpha, $\\beta$ -> beta, $\\gamma$ -> gamma
- $\\delta$ -> delta, $\\epsilon$ -> epsilon, $\\zeta$ -> zeta
- $\\eta$ -> eta, $\\theta$ -> theta, $\\iota$ -> iota
- $\\kappa$ -> kappa, $\\lambda$ -> lambda, $\\mu$ -> mu
- $\\nu$ -> nu, $\\xi$ -> xi, $\\pi$ -> pi
- $\\rho$ -> rho, $\\sigma$ -> sigma, $\\tau$ -> tau
- $\\upsilon$ -> upsilon, $\\phi$ -> phi, $\\chi$ -> chi
- $\\psi$ -> psi, $\\omega$ -> omega

Math Formatting (remove markup):
- $\\mathbf{a}$ -> a (remove bold)
- $\\mathit{x}$ -> x (remove italic)
- $S$ -> S (remove dollar signs from single letters)
- $x_i$ -> x sub i
- $x^2$ -> x squared
- $x^{-1}$ -> x to the negative 1
- $10^{-3}$ -> 10 to the negative 3

Fractions:
- $\\frac{1}{2}$ -> one half
- $\\frac{a}{b}$ -> a over b

Operators:
- $\\sum_{i=1}^n$ -> sum from i equals 1 to n
- $\\prod_{i=1}^n$ -> product from i equals 1 to n
- $\\int_a^b$ -> integral from a to b

Delimiters:
- \\( ... \\) -> convert contents to words
- $ ... $ -> convert contents to words
- \\text{...} -> read contents normally
- E[X | Y] -> expected value of X given Y
- \\mid or | -> given (in conditional expressions)
- X^T -> X transpose

Special Cases:
- $\\zeta \\upsilon \\mu \\iota$ -> zeta upsilon mu iota
- $a$ and $\\alpha$ -> a and alpha
- $\\mathbf{a}$ and $\\alpha$ -> a and alpha

DO NOT change any other text - only convert LaTeX. Preserve all prose exactly."""


def humanize_latex(content: str, model: str) -> str:
    """Convert all LaTeX notation to natural readable text using LLM.

    Args:
        content: Content with LaTeX notation.
        model: pydantic-ai model string.

    Returns:
        Content with all LaTeX converted to natural language.
    """
    import tiktoken

    from ..llm.agents import text_agent

    enc = tiktoken.get_encoding("cl100k_base")
    tokens = enc.encode(content)
    max_chunk = 8000
    humanized_chunks: list[str] = []

    for start in range(0, len(tokens), max_chunk):
        chunk = enc.decode(tokens[start : start + max_chunk])

        result = text_agent.run_sync(
            chunk,
            instructions=_LATEX_SYSTEM_PROMPT,
            model=model,
            model_settings={"max_tokens": 10000},
        )
        humanized_chunk = result.output.strip()

        if not humanized_chunk:
            logger.error("LaTeX humanization failed, using original chunk")
            humanized_chunk = chunk

        humanized_chunks.append(humanized_chunk)

    return "\n\n".join(humanized_chunks)
