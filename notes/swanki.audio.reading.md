---
id: adeac28210904270923c96e
title: Reading
desc: ''
updated: 1773142603440
created: 1773142603440
---

## 2026.03.10 - Full document reading with two-pass LLM processing

Extracted from monolithic audio module. Uses a two-pass approach: (1) `_humanize_latex` converts all LaTeX to natural text in 8000-token chunks, (2) LLM generates reading-optimized transcript in 3000-token chunks. Audio is chunked at a stricter 2000-char limit for quality.

## 2026.03.12 - Migrate from OpenAI client to pydantic-ai agents

Replaced direct `OpenAI` client calls with shared `text_agent` from `swanki.llm.agents` in both `generate_reading_audio` and `_humanize_latex`. Removed `openai_client` parameter -- functions now accept `model: str` in pydantic-ai format. Manual retry loops replaced by agent-level `retries=3`. Part of Step 5 ([[plan.major-refactor-sequence.plan-0]]).

## 2026.03.13 - Section-aware assembly, metadata filtering, no-filler pauses, bookends, acronyms

Addresses issues heard in merzbacher paper audio: university addresses and dates read aloud, filler text between sections instead of silence, no bookend announcements, and inconsistent acronym expansion.

- **Metadata filtering**: `filter_metadata()` now applied to content before LLM processing, stripping affiliations, emails, "Received/Accepted/Published" dates, and references
- **No-filler section breaks**: Replaced SSML `<break time="2.0s"/>` with `---SECTION_BREAK---` markers; prompt explicitly forbids filler text or transitions between sections
- **Figure handling**: New prompt instruction to announce figures with pause/`Figure X`/pause/description pattern instead of skipping them
- **Section-aware assembly**: Replaced flat `combine_audio` with `combine_audio_with_section_pauses` for real silence between sections
- **Bookends**: Generates START/END citation key announcements via `generate_bookend_audio`
- **Acronyms**: `extract_acronyms()` scans source text and injects definitions into the LLM prompt

## 2026.03.15 - Flash TTS model and SSML pause injection

Switched from `eleven_multilingual_v2` (1 credit/char) to `eleven_flash_v2_5` (0.5x credits, 40k char limit) for reading audio -- quality is sufficient for straight readings and costs half as much. Added `add_tts_pauses()` after `clean_markdown_for_tts()` to insert SSML `<break>` tags at paragraph boundaries for natural pacing.

## 2026.04.03 - Fish Speech tts_kwargs passthrough and provider-aware pauses

Added `**tts_kwargs` parameter to `generate_reading_audio()` for Fish Speech provider support. All `text_to_speech()`, `generate_bookend_audio()`, and `add_tts_pauses()` calls now forward provider info. Pause insertion uses `[pause]`/`[short pause]` tags for Fish Speech instead of SSML `<break>`.
- **Paragraph-only chunking for Fish Speech**: Switches to `chunk_text_paragraphs()` with 2000 char max when using Fish Speech to avoid mid-sentence audio truncation. Section pauses increased to 3s.

## 2026.04.15 - Parallel chunk dispatch across Fish Speech servers

Reading audio now flattens chunks across all sections into one job list and dispatches via `tts_chunks_parallel()` when Fish Speech is the provider, then regroups paths by section index for the section-paused combine step. Same pattern as lecture/summary so a multi-server deployment processes a paper's audio concurrently.

## 2026.04.16 - Reading chunks retained in `reading_chunks/` with manifest

Reading audio chunks now live under `reading_chunks/` and are kept after combination, paired with a `chunk_manifest.json` so a single bad chunk can be re-TTS'd and the reading restitched via `restitch_from_chunks()`. Same shape as lecture and summary -- consistency of the chunks-plus-manifest layout across audio types is the point.

- Each chunk gets `append_chunk_pause(text, provider)` before TTS so direct concatenation (no crossfade) sounds seamless.
- Bookends are written into `reading_chunks/`, co-located with the chunks they bracket.
- `combine_audio_with_section_pauses()` is invoked with `chunk_crossfade_ms=0` explicitly. The cleanup `unlink()` block is gone.
