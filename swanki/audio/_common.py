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
        # Inject [short pause] every 3 sentences inside continuous prose so
        # long single paragraphs (which Fish S2-Pro otherwise speaks without
        # noticeable breath) still get lecture cadence. Newlines are not used
        # by S2-Pro for pacing — every pause is tag-driven.
        _sent_counter = [0]

        def _inject_pause(_match: re.Match) -> str:
            _sent_counter[0] += 1
            if _sent_counter[0] % 3 == 0:
                return " [short pause] "
            return ""

        text = re.sub(r"(?<=[.!?])(?=\s+[A-Z])", _inject_pause, text)
        # Collapse stacked tags
        text = re.sub(r"(\[pause\]\s*){2,}", "[pause]\n\n", text)
        text = re.sub(r"(\[short pause\]\s*){2,}", "[short pause] ", text)
    else:
        text = re.sub(r"\n\n+", '\n\n<break time="0.7s" />\n\n', text)
        text = re.sub(r":\s*\n", ':\n<break time="0.4s" />\n', text)
        text = re.sub(
            r'(<break time="[^"]*" />\s*){2,}',
            '<break time="0.7s" />\n\n',
            text,
        )

    return text


_CHUNK_BOUNDARY_PAUSE_RE = re.compile(
    r"(\s*\[(?:pause|short pause|long pause)\])+\s*$"
)
_CHUNK_LEADING_PAUSE_RE = re.compile(
    r"^(\s*\[(?:pause|short pause|long pause)\])+\s*"
)


def strip_chunk_boundary_pause_tags(text: str) -> str:
    """Strip ``[pause]`` / ``[short pause]`` / ``[long pause]`` from chunk ends.

    Pause tags at chunk boundaries cause audible stutter when Fish renders the
    token immediately before (or after) the deterministic inter-chunk silence
    supplied by :func:`combine_audio_with_section_pauses` (``chunk_pause_ms``).
    Pause tags should appear MID-chunk only -- where they signal complex-
    sentence comprehension breaks or dramatic effect. Mid-chunk tags are
    preserved.

    Idempotent. Operates only on text that begins or ends with a (possibly
    stacked) sequence of pause tags; mid-chunk content is untouched.

    Args:
        text: Chunk text bound for TTS.

    Returns:
        Text with leading and trailing pause tags removed (and surrounding
        whitespace trimmed).
    """
    text = _CHUNK_LEADING_PAUSE_RE.sub("", text)
    text = _CHUNK_BOUNDARY_PAUSE_RE.sub("", text)
    return text.strip()


def append_chunk_pause(text: str, provider: str = "elevenlabs") -> str:
    """Prepare a chunk's tail for TTS provider-specific concatenation.

    For Fish Speech: STRIP any trailing ``[pause]`` / ``[short pause]`` /
    ``[long pause]`` tag (and any leading one). Inter-chunk silence is supplied
    deterministically by :func:`combine_audio_with_section_pauses` via
    ``chunk_pause_ms``; the trailing pause tags previously emitted here caused
    audible stutter at chunk boundaries (Fish renders the token, then the
    silence plays, producing a perceptible double-beat). Pause tags belong
    MID-chunk only -- for complex-sentence comprehension breaks or dramatic
    effect.

    For ElevenLabs: APPEND a self-closing ``<break time="1.0s" />`` SSML tag.
    ElevenLabs does NOT receive deterministic inter-chunk silence at
    concatenation time, so the SSML break is the pause mechanism. Idempotent:
    skips when a ``/>``-terminated tag is already present.

    Args:
        text: Chunk text.
        provider: TTS provider name (``"fish_speech"`` or ``"elevenlabs"``).

    Returns:
        Provider-appropriate chunk-tail text.
    """
    if provider == "fish_speech":
        return strip_chunk_boundary_pause_tags(text)
    text = text.rstrip()
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


def chunk_text_paragraphs(
    text: str, max_chars: int = 4500
) -> list[tuple[str, str]]:
    """Split text at paragraph boundaries, falling back to sentences.

    Designed for lecture TTS where prosody continuity within paragraphs is
    critical. Splits preferentially at paragraph breaks. Any single paragraph
    that exceeds ``max_chars`` is further split at sentence boundaries so no
    chunk is ever larger than ``max_chars``.

    Args:
        text: Text to split into chunks.
        max_chars: Maximum characters per chunk.

    Returns:
        List of ``(chunk_text, boundary_type)`` tuples. ``boundary_type``
        describes the source-text relationship between THIS chunk and the
        PREVIOUS chunk -- either ``"paragraph"`` (this chunk starts at a
        paragraph break in the source) or ``"sentence"`` (this chunk starts
        at a sentence break inside an over-budget paragraph that was
        subdivided). The first chunk's boundary is always ``"paragraph"`` --
        it has no predecessor within the section, and the outer combine
        helper handles the section-level gap separately. Callers pass these
        boundary types to :func:`combine_audio_with_section_pauses` so each
        inter-chunk silence can be sized for the kind of break it spans.
    """
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]

    # First-level split: each item is either a whole paragraph or a sentence-
    # bounded sub-paragraph (when the source paragraph exceeds max_chars).
    # Each item carries its boundary type relative to the PREVIOUS item.
    items: list[tuple[str, str]] = []
    for p in paragraphs:
        if len(p) <= max_chars:
            items.append((p, "paragraph"))
            continue
        # Split at sentence boundaries (period/!/? followed by space)
        sentences = re.split(r"(?<=[.!?])\s+", p)
        first_sub = True
        current_sent = ""
        for s in sentences:
            if not current_sent:
                current_sent = s
            elif len(current_sent) + len(s) + 1 <= max_chars:
                current_sent = current_sent + " " + s
            else:
                items.append(
                    (current_sent, "paragraph" if first_sub else "sentence")
                )
                first_sub = False
                current_sent = s
        if current_sent:
            items.append(
                (current_sent, "paragraph" if first_sub else "sentence")
            )

    # Second-level split: greedy-pack items into chunks. The boundary
    # preceding each chunk is the boundary of its FIRST item -- once items
    # are joined inside a chunk with "\n\n", any internal paragraph breaks
    # are absorbed (no inter-chunk silence applies inside a chunk).
    chunks: list[tuple[str, str]] = []
    current_text = ""
    current_boundary = "paragraph"
    for item_text, item_boundary in items:
        if not current_text:
            current_text = item_text
            current_boundary = item_boundary
        elif len(current_text) + len(item_text) + 2 <= max_chars:
            current_text = current_text + "\n\n" + item_text
        else:
            chunks.append((current_text, current_boundary))
            current_text = item_text
            current_boundary = item_boundary

    if current_text:
        chunks.append((current_text, current_boundary))

    return chunks


def _strip_ssml(text: str) -> str:
    """Remove SSML break tags that Fish Speech cannot handle."""
    return re.sub(r'<break[^>]*/?\s*>', '', text)


_FISH_SPEECH_PUNCT_MAP = {
    "\u2014": ", ",   # em dash → comma + space (reads as a natural pause)
    "\u2013": "-",    # en dash → ASCII hyphen
    "\u2212": "-",    # minus sign → ASCII hyphen
    "\u2018": "'",    # left single quote
    "\u2019": "'",    # right single quote / apostrophe
    "\u201A": "'",    # single low-9 quote
    "\u201B": "'",    # single high-reversed-9 quote
    "\u201C": '"',    # left double quote
    "\u201D": '"',    # right double quote
    "\u201E": '"',    # double low-9 quote
    "\u2026": "...",  # horizontal ellipsis
    "\u00A0": " ",    # non-breaking space
}


def _normalize_fish_speech_punct(text: str) -> str:
    """Fold Unicode punctuation into ASCII for Fish Speech TTS.

    Fish Speech's tokenizer garbles Unicode dashes, curly quotes, and
    ellipses rather than voicing them as pauses or apostrophes. Mapping
    each to an ASCII equivalent before synthesis removes the garble
    without changing perceived prosody.
    """
    for src, dst in _FISH_SPEECH_PUNCT_MAP.items():
        text = text.replace(src, dst)
    return text


# Single source of truth for tags Fish renders as audible breath / wrong
# register. Mirrored by the writer prompts in default.yaml / book_voice.yaml
# and by the lecture critic prompt; the deterministic stripper below is the
# safety net that catches LLM-emitted forbidden tags before TTS.
FISH_SPEECH_FORBIDDEN_TAGS: tuple[str, ...] = (
    "inhale", "exhale", "sigh", "clearing throat", "tsk", "panting", "moaning",
    "whisper", "soft tone", "shouting", "screaming",
    "sad", "depressed", "crying", "sobbing",
    "angry", "furious", "panicked", "anxious", "scared", "worried",
)

_FISH_SPEECH_FORBIDDEN_TAG_RE = re.compile(
    r"\[\s*(" + "|".join(re.escape(t) for t in FISH_SPEECH_FORBIDDEN_TAGS) + r")\s*\]",
    flags=re.IGNORECASE,
)


def strip_forbidden_fish_tags(text: str) -> str:
    """Strip Fish Speech bracket tags Fish renders as breath / wrong register.

    Idempotent. Logs each stripped tag at WARNING so prompt drift surfaces in
    the run log instead of disappearing silently into the audio.

    Args:
        text: Transcript bound for Fish Speech TTS.

    Returns:
        Text with forbidden tags removed and double spaces collapsed.
    """

    def _sub(m: re.Match) -> str:
        logger.warning(f"Stripped forbidden Fish Speech tag: {m.group(0)!r}")
        return ""

    cleaned = _FISH_SPEECH_FORBIDDEN_TAG_RE.sub(_sub, text)
    cleaned = re.sub(r"  +", " ", cleaned)
    cleaned = re.sub(r" +\n", "\n", cleaned)
    return cleaned


# Standalone uppercase token of length 2-6, not part of camelCase. Camel-case
# (myACRONYM, ACRONYMfoo) is excluded so identifiers in body prose aren't
# mangled into letter spellings.
_STANDALONE_ACRONYM_RE = re.compile(r"(?<![A-Za-z])([A-Z]{2,6})(?![A-Za-z])")


def expand_acronyms_for_tts(
    text: str, allowlist: set[str] | None = None
) -> str:
    """Rewrite standalone uppercase tokens as letter-by-letter for Fish Speech.

    Fish reads ``S-A-R`` cleanly as letters (per the existing
    `_FISH_SPEECH_PUNCT_MAP` design) but reads bare ``SAR`` as ``"say R"``.

    Args:
        text: Transcript bound for TTS.
        allowlist: Tokens to skip (already pronounceable, e.g. ``USA``,
            ``NASA``). When None, no tokens are skipped.

    Returns:
        Text with bare acronyms rewritten as ``S-A-R`` form.
    """
    skip = allowlist or set()

    def _sub(m: re.Match) -> str:
        tok = m.group(1)
        if tok in skip:
            return tok
        return "-".join(tok)

    return _STANDALONE_ACRONYM_RE.sub(_sub, text)


def apply_pronunciation_overrides(
    text: str, overrides: dict[str, str]
) -> str:
    """Whole-word case-sensitive substitutions applied before TTS.

    The override key wins over `expand_acronyms_for_tts`: callers should run
    overrides AFTER the acronym pass so a per-paper rewrite for a specific
    token (e.g. ``SAR -> "sar"``) preempts the generic ``S-A-R`` rewrite.

    Args:
        text: Transcript bound for TTS.
        overrides: Mapping of source token to replacement. Empty dict is a
            no-op.

    Returns:
        Text with overrides applied.
    """
    for src, dst in overrides.items():
        text = re.sub(rf"\b{re.escape(src)}\b", dst, text)
    return text


_REPEATED_PHRASE_WORD_RE = re.compile(r"[A-Za-z][A-Za-z'-]*")
_REPEATED_PHRASE_STOPWORDS = frozenset({
    "the", "a", "an", "of", "to", "and", "or", "but", "is", "are", "was",
    "were", "be", "been", "being", "in", "on", "at", "by", "for", "with",
    "that", "this", "it", "its", "as", "from", "we", "you", "i", "he", "she",
    "they", "them", "our",
})


def detect_repeated_phrases(
    transcript: str,
    n: int = 5,
    threshold: int = 3,
    min_distinct_content_words: int = 3,
) -> list[str]:
    """Find n-gram phrases repeated above ``threshold`` times.

    Used by the lecture refine loop as a deterministic guard against the
    "his last observation" failure mode the LLM critic missed (Theme 5).
    Filters chatter like "the way that you can" by requiring at least
    ``min_distinct_content_words`` non-stopword tokens per shingle.

    Args:
        transcript: Lecture transcript text (post-refine, pre-TTS).
        n: Phrase length in tokens.
        threshold: Minimum repetition count to flag.
        min_distinct_content_words: Drop n-grams that are mostly function
            words (avoids false positives on common phrasing).

    Returns:
        Repeated phrases in descending frequency order.
    """
    tokens = [t.lower() for t in _REPEATED_PHRASE_WORD_RE.findall(transcript)]
    if len(tokens) < n:
        return []
    counts: dict[tuple[str, ...], int] = {}
    for i in range(len(tokens) - n + 1):
        gram = tuple(tokens[i : i + n])
        content = sum(1 for t in gram if t not in _REPEATED_PHRASE_STOPWORDS)
        if content < min_distinct_content_words:
            continue
        counts[gram] = counts.get(gram, 0) + 1
    repeats = [(gram, c) for gram, c in counts.items() if c >= threshold]
    repeats.sort(key=lambda x: -x[1])
    return [" ".join(gram) for gram, _ in repeats]


# Citation-key chapter pattern: <base>_<NN>_<slug>. The leading-zero numeric
# segment is the chapter index; the slug uses hyphens and is humanized into
# spaces by humanize_chapter_slug() in swanki/utils/formatting.py. The match
# here is a fast deterministic pre-check used by the slug-stripper.
_CHAPTER_SLUG_PATTERN = re.compile(
    r"\b([A-Za-z][A-Za-z0-9]+)_(\d{1,3})_([a-z][a-z0-9-]+)\b"
)


def strip_chapter_filename_slug(text: str) -> str:
    """Replace raw ``<base>_<NN>_<slug>`` tokens with humanized chapter form.

    Catches Theme 8: the lecture writer occasionally interpolates the raw
    chapter content_key (e.g. ``hammingArtDoingScience2020_03_history-of-
    computers-hardware``) into transcript text. Without this stripper, Fish
    reads the underscored slug aloud verbatim — ``"zero three"`` and all.

    Replaces matches with ``Chapter <N>: <human slug>`` (slug hyphens become
    spaces). Fall-through routing: bookend templates should call
    ``swanki.utils.formatting.humanize_chapter_slug`` directly when they have
    the citation_key in hand; this function is the safety net for any leakage
    that escapes the templating layer.

    Args:
        text: Transcript text.

    Returns:
        Text with chapter-slug tokens replaced.
    """

    def _sub(m: re.Match) -> str:
        num = int(m.group(2))
        slug = m.group(3).replace("-", " ")
        return f"Chapter {num}: {slug}"

    return _CHAPTER_SLUG_PATTERN.sub(_sub, text)


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
    clean_text = _normalize_fish_speech_punct(clean_text)

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
    chunk_tail_trim_ms: int = 0,
    chunk_pause_ms: int = 0,
    gain_match_target_dbfs: float | None = None,
    chunk_boundaries: Sequence[list[str]] | None = None,
    chunk_pause_ms_by_boundary: dict[str, int] | None = None,
) -> None:
    """Combine audio chunks grouped by section with real silence between sections.

    Defaults to direct concatenation between chunks (``chunk_crossfade_ms=0``)
    so trailing pauses generated by the TTS provider supply natural transitions.

    Args:
        sections: List of chunk-path lists, one list per section.
        output: Path for the combined output file.
        section_pause_ms: Silence duration between sections.
        chunk_crossfade_ms: Crossfade duration between chunks within a section.
            Combines with ``chunk_pause_ms``: when both are set, the silence is
            inserted first and the next chunk crossfades into the trailing silence,
            smoothing the join without bleeding speech.
        bookend_start: Optional start bookend audio file.
        bookend_end: Optional end bookend audio file.
        bookend_pause_ms: Silence after start bookend / before end bookend.
        chunk_tail_trim_ms: Strip this many ms from the end of each chunk before
            concatenation. Used to clip Fish Speech tag-rendering artifacts
            (audible inhale/sigh that the [pause] tag renders as).
        chunk_pause_ms: Uniform fallback silence between chunks within a section.
            Used when ``chunk_boundaries`` + ``chunk_pause_ms_by_boundary`` are
            absent (legacy single-knob callers and elevenlabs).
        gain_match_target_dbfs: If set, each chunk + bookend is shifted by a
            single gain scalar so its mean dBFS lands at the target. Pure gain,
            no compression — preserves intra-chunk dynamics (Hamming's
            expressive emphasis stays loud relative to surrounding speech).
            Eliminates audible loudness jumps between consecutive chunks.
        chunk_boundaries: Per-chunk boundary types, parallel to ``sections``.
            Each inner list is ``[<boundary for chunks[0]>, <boundary for
            chunks[1]>, ...]``; values are ``"paragraph"`` or ``"sentence"``
            describing the source-text relationship between THIS chunk and the
            PREVIOUS chunk in the same section. The boundary preceding
            chunks[0] is irrelevant (no predecessor in section) and ignored.
            Sourced from :func:`chunk_text_paragraphs`.
        chunk_pause_ms_by_boundary: Boundary-type-keyed silence durations,
            e.g. ``{"paragraph": 1100, "sentence": 500}``. When provided
            together with ``chunk_boundaries``, supersedes ``chunk_pause_ms``
            -- each inter-chunk gap uses the duration matching the chunk's
            boundary type. Missing keys fall back to ``chunk_pause_ms``.
    """
    if not sections:
        logger.error("No sections provided to combine_audio_with_section_pauses")
        return

    def _gain_match(seg: AudioSegment) -> AudioSegment:
        if gain_match_target_dbfs is None:
            return seg
        # pydub returns -inf for silent segments; only normalize voiced audio
        if seg.dBFS == float("-inf"):
            return seg
        delta = gain_match_target_dbfs - seg.dBFS
        return seg + delta

    def _load(path: Path) -> AudioSegment:
        seg = AudioSegment.from_mp3(str(path))
        if chunk_tail_trim_ms > 0 and len(seg) > chunk_tail_trim_ms + 200:
            # Silence-aware trim: cut inside the trailing silence (NOT at its
            # leading edge). Cutting right at the speech-silence transition
            # makes the chunk-end sound clipped — the listener perceives the
            # last syllable as truncated. We keep ~150 ms of post-speech
            # silence as breathing room before the inter-chunk pause kicks in.
            from pydub.silence import detect_silence

            scan_window_ms = chunk_tail_trim_ms + 200
            scan = seg[-scan_window_ms:]
            silence_thresh = max(seg.dBFS - 16, -50.0)
            silences = detect_silence(
                scan, min_silence_len=80, silence_thresh=silence_thresh
            )
            # Trailing silence: a range whose end touches the end of the scan
            # window (within a small tolerance).
            trailing = [s for s in silences if s[1] >= scan_window_ms - 30]
            if trailing:
                silence_start_in_scan = trailing[-1][0]
                # 350 ms of post-speech silence buffer. Listener feedback on v8
                # (150 ms): still perceived as clipped at chunk boundaries even
                # though no speech was actually being cut. The buffer needs to
                # leave enough silence after the last syllable that the chunk
                # never feels truncated. With this width, only chunks with
                # genuinely long trailing silence get any trim at all.
                tail_buffer_ms = 350
                abs_cut = min(
                    len(seg)
                    - scan_window_ms
                    + silence_start_in_scan
                    + tail_buffer_ms,
                    len(seg),
                )
                seg = seg[:abs_cut]
            # else: chunk ends mid-speech — leave intact, no blind trim.
        return _gain_match(seg)

    combined: AudioSegment | None = None

    # Start bookend (also gain-matched so it doesn't punch over the chunk level)
    if bookend_start and bookend_start.exists():
        combined = _gain_match(AudioSegment.from_mp3(str(bookend_start)))
        combined += AudioSegment.silent(duration=bookend_pause_ms)

    # Capture as locals so mypy narrows away the Optional and the closure
    # below doesn't keep repeating the truthiness check.
    _bounds: Sequence[list[str]] | None = chunk_boundaries
    _pause_map: dict[str, int] | None = chunk_pause_ms_by_boundary
    use_per_boundary = bool(_bounds) and bool(_pause_map)

    def _gap_ms_for(sec_idx: int, chunk_idx: int) -> int:
        """Pick the right inter-chunk silence for the gap PRECEDING this chunk."""
        if use_per_boundary and _bounds is not None and _pause_map is not None:
            sec_bounds = _bounds[sec_idx] if sec_idx < len(_bounds) else []
            if chunk_idx < len(sec_bounds):
                btype = sec_bounds[chunk_idx]
                return int(_pause_map.get(btype, chunk_pause_ms))
        return chunk_pause_ms

    for sec_idx, section_chunks in enumerate(sections):
        if not section_chunks:
            continue

        # Build section audio from chunks: silence first, then crossfade-append.
        section_audio = _load(section_chunks[0])
        for chunk_idx_in_section, chunk_path in enumerate(section_chunks[1:], start=1):
            gap_ms = _gap_ms_for(sec_idx, chunk_idx_in_section)
            if gap_ms > 0:
                section_audio += AudioSegment.silent(duration=gap_ms)
            section_audio = section_audio.append(
                _load(chunk_path), crossfade=chunk_crossfade_ms
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
        combined += _gain_match(AudioSegment.from_mp3(str(bookend_end)))

    combined.export(str(output), format="mp3", bitrate="192k")


def write_chunk_manifest(
    chunks_dir: Path,
    audio_type: str,
    output_file: str,
    chunks: list[dict],
    bookend_start: str | None = None,
    bookend_end: str | None = None,
    postprocessor: dict | None = None,
) -> Path:
    """Write a chunk manifest JSON for surgical regeneration.

    Args:
        chunks_dir: Directory containing chunk files.
        audio_type: One of ``"lecture"``, ``"reading"``, ``"summary"``, ``"card"``.
        output_file: Filename of the combined output audio.
        chunks: List of dicts with keys ``index``, ``section``, ``text``, ``file``.
        bookend_start: Filename of start bookend, if any.
        bookend_end: Filename of end bookend, if any.
        postprocessor: Optional dict of the boundary-fix knobs that the
            original render passed to :func:`combine_audio_with_section_pauses`
            (``section_pause_ms``, ``chunk_pause_ms``, ``chunk_tail_trim_ms``,
            ``chunk_crossfade_ms``, ``gain_match_target_dbfs``,
            ``bookend_pause_ms``). Recorded in the manifest so a later
            ``restitch_from_chunks`` reproduces the original render exactly --
            without this, restitch defaults to zero inter-chunk silence and
            chunks crash into each other.

    Returns:
        Path to the written manifest file.
    """
    manifest = {
        "audio_type": audio_type,
        "output_file": output_file,
        "bookend_start": bookend_start,
        "bookend_end": bookend_end,
        "postprocessor": postprocessor or {},
        "chunks": chunks,
    }
    manifest_path = chunks_dir / "chunk_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2))
    logger.info(f"Wrote chunk manifest: {manifest_path} ({len(chunks)} chunks)")
    return manifest_path


def restitch_from_chunks(
    manifest_path: Path,
    output_path: Path,
    section_pause_ms: int | None = None,
    bookend_pause_ms: int | None = None,
) -> None:
    """Reassemble final audio from chunk files using a manifest.

    Reads the chunk manifest JSON, loads each chunk file, and combines them
    with the same boundary-fix knobs the original render used (recorded in
    ``manifest["postprocessor"]`` by :func:`write_chunk_manifest`). Used for
    surgical regeneration: re-TTS one chunk or regenerate bookends, then
    restitch without re-running the body LLM/TTS work.

    Args:
        manifest_path: Path to ``chunk_manifest.json``.
        output_path: Path for the reassembled output MP3.
        section_pause_ms: Override for ``section_pause_ms`` from manifest.
            When None, uses manifest value (or 2000 if manifest predates the
            postprocessor field).
        bookend_pause_ms: Override for ``bookend_pause_ms`` from manifest.
            When None, uses manifest value (or 500 fallback).
    """
    manifest = json.loads(manifest_path.read_text())
    chunks_dir = manifest_path.parent
    post = manifest.get("postprocessor") or {}

    sections: dict[int, list[Path]] = {}
    boundaries: dict[int, list[str]] = {}
    for chunk in manifest["chunks"]:
        sec = chunk["section"]
        if sec not in sections:
            sections[sec] = []
            boundaries[sec] = []
        chunk_path = chunks_dir / chunk["file"]
        assert chunk_path.exists(), f"Chunk file missing: {chunk_path}"
        sections[sec].append(chunk_path)
        # Default to "paragraph" for older manifests that don't carry boundary;
        # the boundary-keyed map's "paragraph" entry then determines silence.
        boundaries[sec].append(chunk.get("boundary", "paragraph"))

    sorted_keys = sorted(sections.keys())
    section_lists = [sections[k] for k in sorted_keys]
    boundary_lists = [boundaries[k] for k in sorted_keys]

    bookend_start = None
    bookend_end = None
    if manifest.get("bookend_start"):
        bookend_start = chunks_dir / manifest["bookend_start"]
    if manifest.get("bookend_end"):
        bookend_end = chunks_dir / manifest["bookend_end"]

    # Caller overrides win, then manifest, then sensible legacy defaults.
    eff_section_pause = (
        section_pause_ms
        if section_pause_ms is not None
        else int(post.get("section_pause_ms", 2000))
    )
    eff_bookend_pause = (
        bookend_pause_ms
        if bookend_pause_ms is not None
        else int(post.get("bookend_pause_ms", 500))
    )
    boundary_map = post.get("chunk_pause_ms_by_boundary") or None
    combine_audio_with_section_pauses(
        section_lists,
        output_path,
        section_pause_ms=eff_section_pause,
        chunk_crossfade_ms=int(post.get("chunk_crossfade_ms", 0)),
        bookend_start=bookend_start,
        bookend_end=bookend_end,
        bookend_pause_ms=eff_bookend_pause,
        chunk_tail_trim_ms=int(post.get("chunk_tail_trim_ms", 0)),
        chunk_boundaries=boundary_lists if boundary_map else None,
        chunk_pause_ms_by_boundary=boundary_map,
        chunk_pause_ms=int(post.get("chunk_pause_ms", 0)),
        gain_match_target_dbfs=post.get("gain_match_target_dbfs"),
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
    from ..utils.formatting import (
        chapter_number_spoken,
        humanize_citation_key,
        parse_chapter_key,
    )

    parsed_chapter = parse_chapter_key(citation_key)
    humanized_full = humanize_citation_key(citation_key)
    cache_path = output_dir / f"{citation_key}_{audio_type}_{position}.mp3"

    if audio_type == "lecture":
        if parsed_chapter is not None:
            # Book-chapter form (<base>_<NN>_<slug>): the listener wants the
            # exact slug read aloud (citation key + chapter number as written
            # + humanized title), bracketed by "this lecture is posted as" /
            # "this concludes" framing plus a "Let's begin chapter N, slug"
            # opener for orientation.
            base, num_str, slug = parsed_chapter
            base_humanized = humanize_citation_key(base)
            num_spoken = chapter_number_spoken(num_str)  # e.g. "01" -> "o one"
            n_word = chapter_number_spoken(str(int(num_str)))  # e.g. "01" -> "one"
            exact_reading = f"{base_humanized}, {num_spoken}, {slug}"
            if position == "start":
                text = (
                    f"This lecture is posted as: {exact_reading}. "
                    f"Let's begin chapter {n_word}, {slug}."
                )
            else:
                text = (
                    f"This concludes chapter {n_word}, {slug}, "
                    f"which is posted as: {exact_reading}."
                )
        else:
            # Non-chapter (regular paper) bookend retains the existing form.
            if position == "start":
                title_part = f" We are covering: {paper_title}." if paper_title else ""
                text = f"Today's lecture is posted as: {humanized_full}.{title_part}"
            else:
                text = f"And with that we conclude: {humanized_full}."
    else:
        label = position.upper()
        text = f"{label}: {humanized_full}."

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

_LATEX_SYSTEM_PROMPT = """You are a math/LaTeX/inline-notation → speech converter for academic audio transcripts.

YOUR ONLY JOB: Convert ALL math, LaTeX, inline symbols, unit abbreviations, bare Greek letters, and ASCII-math notation to natural readable text.

CRITICAL RULES:
1. Convert EVERY mathematical, symbolic, or unit expression to spoken form.
2. Remove ALL dollar signs ($), backslashes (\\), and curly braces ({}). A stray "$" MUST NEVER appear in the output — papers often have bare dollar signs from mathpix leakage; eliminate them entirely.
3. NEVER output any LaTeX syntax in your response.
4. Preserve all surrounding prose EXACTLY. Only transform the math/units/symbols.

CONVERSIONS (apply ALL of these):

Greek Letters — convert both delimited and BARE forms:
- $\\alpha$ -> alpha, $\\beta$ -> beta, $\\gamma$ -> gamma, $\\delta$ -> delta
- $\\epsilon$ -> epsilon, $\\zeta$ -> zeta, $\\eta$ -> eta, $\\theta$ -> theta
- $\\iota$ -> iota, $\\kappa$ -> kappa, $\\lambda$ -> lambda, $\\mu$ -> mu
- $\\nu$ -> nu, $\\xi$ -> xi, $\\pi$ -> pi, $\\rho$ -> rho
- $\\sigma$ -> sigma, $\\tau$ -> tau, $\\upsilon$ -> upsilon, $\\phi$ -> phi
- $\\chi$ -> chi, $\\psi$ -> psi, $\\omega$ -> omega
- Bare unicode Greek letters anywhere in prose convert too:
  "p_θ with weights, θ" -> "p sub theta with weights, theta"
  "μ represents the mixing constant" -> "mu represents the mixing constant"

Math Formatting (remove markup):
- $\\mathbf{a}$ -> a (remove bold);  $\\mathit{x}$ -> x (remove italic)
- $\\mathcal{O}(n)$ -> big O of n;  $\\mathcal{O}(64T)$ -> big O of 64 T
- $S$ -> S (remove dollar signs from single letters)
- $x_i$ -> x sub i;  $x^2$ -> x squared;  $x^{-1}$ -> x to the negative 1
- $10^{-3}$ -> 10 to the negative 3
- $p_\\theta$ -> p sub theta

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

Inequalities and comparison symbols (inline, NOT inside $ delimiters):
- "> 256" -> "more than 256"  (NOT "greater than")
- "< 29,000" -> "less than 29,000"
- "≥ 10" / ">= 10" -> "at least 10"
- "≤ 5" / "<= 5" -> "at most 5"
- "~9 h" / "∼9 h" / "approximately 9 h" -> "approximately 9 hours"
- "±" -> "plus or minus"
- "×" -> "times" (e.g. "10 ×" -> "10 times")
- "→" -> "to" or "becomes" depending on context

Unit abbreviations — expand to full words when adjacent to a number:
- "12 h" -> "12 hours";  "2 s" -> "2 seconds";  "5 min" -> "5 minutes"
- "3 ms" -> "3 milliseconds";  "10 μs" -> "10 microseconds"
- "500 bp" -> "500 base pairs";  "2 kb" -> "2 kilobases";  "1 Mb" -> "1 megabase"
- "16 GB" -> "16 gigabytes";  "40 TB" -> "40 terabytes"
- "5 CPUs" / "8 GPUs" stay as acronyms (already spoken-friendly as "C P Us" / "G P Us")
- "1%" / "1 %" -> "1 percent"

Version numbers / dotted sequences:
- "NCCL 2.10.3" -> "N C C L version 2.10.3" (keep the version number but prefix "version")
- "Python 3.12.1" -> "Python version 3.12.1"

Approximations and ranges:
- "~1.5 million" / "∼1.5 million" -> "approximately 1.5 million"
- "1–10" / "1-10" (as a numeric range) -> "one to ten"

STRAY-DOLLAR RULE: If you see a standalone "$" not clearly delimiting a math expression, DELETE it. Never say "dollar" unless the prose explicitly refers to currency.

Special Cases:
- $\\zeta \\upsilon \\mu \\iota$ -> zeta upsilon mu iota
- $a$ and $\\alpha$ -> a and alpha
- $\\mathbf{a}$ and $\\alpha$ -> a and alpha

DO NOT change any other text. Preserve prose exactly; only transform the math/units/symbols."""


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
