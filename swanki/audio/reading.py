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
from ..llm.safety import with_safety_retry
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
    filter_metadata,
    generate_bookend_audio,
    humanize_latex,
    split_transcript_by_sections,
    strip_chapter_filename_slug,
    strip_forbidden_fish_tags,
    text_to_speech,
    tts_chunks_parallel,
    write_chunk_manifest,
)

logger = logging.getLogger(__name__)

# Pass-2 (audio-optimization) per-chunk completeness floor. Pass-2 only ever
# expands -- acronym first-use, citation rendering as "author, year",
# SECTION_BREAK markers -- and drops only image URLs and "et al", together a
# few percent. A chunk that comes back below 0.85 has lost prose. Catches the
# qiu-class "summarization tendency" failure surgically (per-chunk retry +
# verbatim fallback) instead of failing the whole paper.
_PASS2_CHUNK_MIN_RATIO = 0.85

# Per-chunk LLM retry budget before falling back to the humanized input.
_CHUNK_RETRY_ATTEMPTS = 3


def reading_coverage_ratio(source: str, transcript: str) -> float:
    """Token-count ratio of the final transcript to the pre-humanize source.

    Diagnostic only -- the per-chunk completeness checks in Pass-1
    (`_humanize_chunk_with_completeness`) and Pass-2
    (`_pass2_chunk_with_completeness`) self-heal silent omissions before they
    reach the final transcript, so this is logged for telemetry rather than
    used as a hard-fail gate. Compares against the pre-humanize reference (post
    filter_metadata, before Pass-1) so equation/symbol rewrites are not
    miscounted as deletions.

    Args:
        source: Pre-humanize reference text.
        transcript: Concatenated final Pass-2 output.

    Returns:
        Ratio of transcript tokens to source tokens; 1.0 if source is empty.
    """
    enc = tiktoken.get_encoding("cl100k_base")
    src_tokens = len(enc.encode(source))
    if not src_tokens:
        return 1.0
    return len(enc.encode(transcript)) / src_tokens


def _pass2_chunk_with_completeness(
    chunk: str, system_prompt: str, model: str
) -> tuple[str, bool]:
    """Pass-2 transcript generation with per-chunk completeness retry.

    Pass-2 is instructed to read prose verbatim and only expand (acronym
    first-use, citation rendering, SECTION_BREAK markers). A chunk below
    `_PASS2_CHUNK_MIN_RATIO` means the LLM omitted prose -- the qiu-class
    failure where rules #8 ("flow naturally") and #9 ("never repeat") get
    interpreted as license to summarize. Retries with a stricter "deliver
    every sentence verbatim" addendum; if all attempts stay below the floor,
    returns the humanized input chunk verbatim so no source content is lost.

    Args:
        chunk: One Pass-2 input chunk (post-humanize).
        system_prompt: Pass-2 system prompt.
        model: pydantic-ai model string.

    Returns:
        Tuple of ``(transcript, fell_back)``. ``fell_back`` is True iff every
        retry stayed below the completeness floor and the humanized input was
        returned verbatim.
    """
    enc = tiktoken.get_encoding("cl100k_base")
    input_tokens = len(enc.encode(chunk))
    best_output = ""
    best_ratio = 0.0

    for attempt in range(_CHUNK_RETRY_ATTEMPTS):
        instructions = system_prompt
        if attempt > 0:
            instructions = (
                system_prompt
                + "\n\nRETRY -- A previous attempt omitted source prose. "
                "Deliver every sentence of this chunk verbatim. Do not skip, "
                "summarize, or condense even sentences that feel repetitive. "
                "Rule #9 (no repetition) applies only WITHIN this chunk; do "
                "not assume earlier chunks already covered anything."
            )
        # Biosec-refusal-aware: same content that triggers gpt-5.5's safety
        # guard in document_summary / card-gen can refuse here too. Wrap with
        # the educational-context preamble retry; re-raises after the 3 inner
        # preamble attempts so the chunk-level token-ratio fallback below
        # only engages on legit short outputs, not biosec refusals (those
        # mean the content is unrenderable, not under-tokenized).
        result = with_safety_retry(
            text_agent,
            chunk,
            instructions=instructions,
            model=model,
            model_settings={"max_tokens": 8000},
            label="reading Pass-2 chunk",
        )
        candidate = result.output.strip()
        candidate_ratio = (
            len(enc.encode(candidate)) / input_tokens if input_tokens else 1.0
        )
        if candidate_ratio > best_ratio:
            best_output = candidate
            best_ratio = candidate_ratio
        if candidate_ratio >= _PASS2_CHUNK_MIN_RATIO:
            return best_output, False
        logger.warning(
            "Pass-2 chunk attempt %d ratio %.3f < %.2f; retrying",
            attempt + 1,
            candidate_ratio,
            _PASS2_CHUNK_MIN_RATIO,
        )

    logger.error(
        "Pass-2 chunk exhausted %d retries (best ratio %.3f < %.2f); "
        "falling back to humanized input verbatim to preserve content",
        _CHUNK_RETRY_ATTEMPTS,
        best_ratio,
        _PASS2_CHUNK_MIN_RATIO,
    )
    return chunk, True


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
        "Do NOT add your own words, summaries, or transitions between sections. Every "
        "sentence in the input must appear in the output; if a sentence feels redundant "
        "or off-topic, include it verbatim anyway. Omission of any sentence is a failure.\n\n"
        "8. The source is already prose; do NOT smooth, condense, or rephrase to make it "
        "'flow better'. Render exactly what is written — only the rule-2/3/5 transformations "
        "(acronyms, figure markers, citations) change wording. Apostrophes, contractions, "
        "and natural prose carry the flow; you do not need to add anything.\n\n"
        "9. WITHIN THIS CHUNK ONLY: do not duplicate a sentence that already appears "
        "literally in this chunk's input. Do NOT assume earlier chunks already covered "
        "anything — you cannot see them. If the input contains it, render it; deduplication "
        "across the document is handled elsewhere.\n"
        + acronym_instruction
    )

    # RC3: optional per-paper prosody addendum, appended verbatim. Carried in
    # the preprocessor sub-tree so no pipeline plumbing is needed and papers
    # without the key are unaffected. Reading-only — does not touch the
    # lecture critic/refiner first-person book-voice whitelist.
    _prep_for_prompt = tts_kwargs.get("preprocessor")
    if isinstance(_prep_for_prompt, dict):
        addendum = str(_prep_for_prompt.get("system_prompt_addendum", "")).strip()
        if addendum:
            system_prompt = f"{system_prompt}\n\n{addendum}"

    # Filter metadata (affiliations, emails, dates, references) before processing
    user_content = filter_metadata(full_content)

    if citation_key:
        humanized_key = humanize_citation_key(citation_key)
        user_content = f"Citation: {humanized_key}\n\n{user_content}"

    # Stable pre-humanize reference for the completeness guard. Captured
    # BEFORE Pass 1 so a humanize_latex collapse (which would otherwise
    # truncate both sides of the coverage ratio equally and pass) is caught:
    # humanize only expands prose, so the final transcript must still cover
    # this baseline.
    coverage_reference = user_content

    # Pass 1: Humanize LaTeX / math / inline symbols
    logger.info("Humanizing LaTeX notation in content...")
    user_content = humanize_latex(user_content, model)
    logger.info("LaTeX humanization complete")

    # Pass 2: Generate reading transcript with per-chunk completeness retry.
    # Each chunk is verified against `_PASS2_CHUNK_MIN_RATIO` and retried with
    # a stricter "deliver every sentence verbatim" addendum; chunks that
    # exhaust retries fall back to the humanized input so no source prose is
    # lost. Replaces the prior paper-level hard-fail guard with surgical
    # per-chunk self-healing.
    enc = tiktoken.get_encoding("cl100k_base")
    tokens = enc.encode(user_content)
    max_chunk = 3000
    transcript_chunks: list[str] = []
    pass2_fallbacks = 0

    for start in range(0, len(tokens), max_chunk):
        chunk = enc.decode(tokens[start : start + max_chunk])
        chunk_transcript, fell_back = _pass2_chunk_with_completeness(
            chunk, system_prompt, model
        )
        if fell_back:
            pass2_fallbacks += 1
        transcript_chunks.append(chunk_transcript)

    full_transcript = "\n\n".join(transcript_chunks)

    # Telemetry: final paper-level coverage + fallback count. Diagnostic only;
    # the per-chunk retry+fallback above already prevents silent omissions
    # from reaching this point, so the prior paper-level hard-fail guard is
    # gone (readings have no paper-level floor -- small natural variation
    # from image-URL stripping and "et al" drops flows through).
    coverage = reading_coverage_ratio(coverage_reference, full_transcript)
    logger.info(
        "Reading transcript complete for %s: %.1f%% paper-level coverage; "
        "Pass-2 chunk fallbacks: %d",
        citation_key or output_path.stem,
        coverage * 100,
        pass2_fallbacks,
    )

    # Save transcripts
    transcripts_dir = output_path.parent / "full_read"
    transcripts_dir.mkdir(parents=True, exist_ok=True)
    transcript_path = transcripts_dir / f"{output_path.stem}_transcript.md"
    with open(transcript_path, "w", encoding="utf-8") as f:
        f.write("# Full Reading Audio Transcript\n\n")
        if citation_key:
            f.write(f"**Citation Key:** {citation_key}\n\n")
        f.write(f"**Generated Transcript:**\n\n{full_transcript}\n")

    # Pre-TTS scrubber pipeline (mirrors lecture.py flow). Same order, same
    # rationale: clean markdown, slug-strip safety net, acronym rewrite,
    # pronunciation overrides, forbidden-tag scrub. Fish-only steps gated by
    # preprocessor flags.
    is_fish_for_prep = str(tts_kwargs.get("provider", "")) == "fish_speech"
    _prep_raw = tts_kwargs.get("preprocessor")
    prep_cfg: dict = _prep_raw if isinstance(_prep_raw, dict) else {}
    cleaned = clean_markdown_for_tts(full_transcript)
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
    # YAML-driven chunking (models.tts.chunking.max_chars) overrides the
    # legacy 2000-char hardcoded cap. Fish ships max_chars=700 so quality
    # doesn't decay past ~700 chars per chunk (Theme 4 from the Hamming
    # bookmark plan).
    _chunk_raw = tts_kwargs.get("chunking")
    chunking_cfg: dict = _chunk_raw if isinstance(_chunk_raw, dict) else {}
    chunk_max_chars = int(chunking_cfg.get("max_chars", 2000 if is_fish else 4500))

    # Each job carries a per-chunk boundary type ("paragraph" | "sentence")
    # so combine_audio_with_section_pauses can size the inter-chunk silence
    # for the kind of source-text break it spans. chunk_text() (non-fish path)
    # doesn't expose boundaries; default those to "paragraph".
    all_jobs: list[tuple[int, str, Path, str]] = []
    chunk_counter = 0
    for sec_idx, section in enumerate(sections_text):
        if is_fish:
            audio_chunks = chunk_text_paragraphs(section, max_chars=chunk_max_chars)
        else:
            audio_chunks = [(c, "paragraph") for c in chunk_text(section, max_chars=chunk_max_chars)]
        for chunk_text_, boundary in audio_chunks:
            chunk_path = chunks_dir / f"{prefix}_chunk{chunk_counter}.mp3"
            all_jobs.append((sec_idx, chunk_text_, chunk_path, boundary))
            chunk_counter += 1

    # Append trailing pause to each chunk for clean concatenation
    all_jobs = [
        (sec_idx, append_chunk_pause(text, provider), chunk_path, boundary)
        for sec_idx, text, chunk_path, boundary in all_jobs
    ]

    if is_fish and len(all_jobs) > 1:
        tts_pairs = [(text, path) for _, text, path, _ in all_jobs]
        tts_chunks_parallel(tts_pairs, voice_id, elevenlabs_api_key, speed, **tts_kwargs)
    else:
        for _, chunk, chunk_path, _b in all_jobs:
            text_to_speech(chunk, voice_id, chunk_path, elevenlabs_api_key, speed, **tts_kwargs)
            time.sleep(1)

    all_section_chunks: list[list[Path]] = [[] for _ in sections_text]
    all_section_boundaries: list[list[str]] = [[] for _ in sections_text]
    for sec_idx, _, chunk_path, boundary in all_jobs:
        all_section_chunks[sec_idx].append(chunk_path)
        all_section_boundaries[sec_idx].append(boundary)

    # YAML-driven postprocessor knobs (models.tts.postprocessor.*) bring
    # reading audio in line with lecture: gain match, inter-chunk silence,
    # tail trim, crossfade. Fall-through defaults preserve prior behavior
    # when no sub-tree is provided.
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
        "reading",
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


