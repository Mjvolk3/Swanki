---
id: 0ddcdd33da14487abaca264
title: _common
desc: ''
updated: 1773142603440
created: 1773142603440
---

## 2026.03.10 - Shared TTS utilities extracted from monolithic audio module

Houses the cross-cutting audio helpers that all generation modules depend on: `chunk_text` (paragraph/sentence boundary splitting), `clean_markdown_for_tts` (strip formatting), `text_to_speech` (ElevenLabs API with FFmpeg speed adjustment), `combine_audio` (pydub crossfade merging), `validate_audio_file` (size and duration checks), and `filter_metadata` (academic metadata stripping).

## 2026.03.12 - Add explicit type annotation for TTS stream result

Added `data: bytes` annotation with `# type: ignore[arg-type]` to the `text_to_speech` stream join to satisfy mypy. The ElevenLabs SDK returns a union type that mypy cannot narrow through `hasattr`.

## 2026.03.13 - Section-aware audio infrastructure for quality improvements

Added five new functions to support real silence between sections, bookend announcements, and reliable acronym expansion across all audio types. Motivated by listening to the merzbacher paper's generated audio and identifying quality gaps: SSML `<break>` tags were unreliable, no start/end announcements existed, and acronyms were inconsistently expanded.

- `generate_silence(duration_ms, output_path)`: creates silent MP3 via pydub
- `split_transcript_by_sections(transcript, marker)`: splits on `---SECTION_BREAK---` markers
- `combine_audio_with_section_pauses(sections, output, ...)`: assembles section-grouped chunks with real silence gaps and optional bookend clips
- `generate_bookend_audio(citation_key, audio_type, position, ...)`: generates cached START/END TTS clips with humanized citation key; lecture variant includes paper title
- `extract_acronyms(text)`: regex extraction of `ACRONYM (Full Form)` and reverse patterns for injection into LLM prompts

## 2026.03.15 - TTS model tiering, paragraph chunking, and SSML pause injection

Three changes to reduce ElevenLabs costs and improve audio prosody.

- **TTS model tiering**: Added `DEFAULT_TTS_MODEL = "eleven_flash_v2_5"` and `LECTURE_TTS_MODEL = "eleven_multilingual_v2"`. The `text_to_speech()` function now accepts a `tts_model` parameter (defaults to flash). Reading, summary, cards, and bookends use the cheaper flash model (0.5x credits, 40k char limit); lecture explicitly passes the premium multilingual model for quality. Previously everything used `eleven_multilingual_v2` at 1 credit/char.
- **Paragraph-only chunking**: New `chunk_text_paragraphs()` splits only at paragraph boundaries, never mid-sentence. Used for lecture TTS to avoid prosody-breaking mid-sentence splits. Default max 4500 chars (vs 2000-3000 for `chunk_text`).
- **SSML pause injection**: New `add_tts_pauses()` inserts `<break time="0.7s" />` between paragraphs and `<break time="0.4s" />` after line-ending colons. ElevenLabs v2 models interpret these as natural AI-modeled pauses (not raw silence). Replaces the old approach of writing "[pause]" or "Pause." in transcripts, which the TTS model read aloud.

## 2026.04.03 - Fish Speech provider integration, LaTeX humanization, provider-aware pauses

Added self-hosted Fish Speech S2 Pro as an alternative TTS provider, eliminating ElevenLabs API dependency for audio generation. The core `text_to_speech()` function now dispatches to `_tts_elevenlabs()` or `_tts_fish_speech()` based on a `provider` key in `**tts_kwargs`, keeping all 10+ existing call sites unchanged.

- **Provider dispatch**: Refactored `text_to_speech()` to accept `**tts_kwargs` and route to private backend functions. `_tts_fish_speech()` POSTs to the Fish Speech `/v1/tts` endpoint with optional `reference_id` for voice cloning. Extracted speed adjustment into shared `_apply_speed()` helper.
- **SSML stripping**: `_strip_ssml()` removes ElevenLabs `<break>` tags before sending text to Fish Speech, which uses its own inline `[tag]` syntax.
- **Reference voice management**: `ensure_fish_speech_reference()` registers a WAV clip with the Fish Speech server via `/v1/references/add` (multipart upload), checking `/v1/references/list` first to avoid duplicates.
- **Provider-aware pauses**: `add_tts_pauses()` now accepts a `provider` parameter -- inserts SSML `<break>` tags for ElevenLabs, `[pause]`/`[short pause]` for Fish Speech.
- **LaTeX humanization**: New public `humanize_latex()` function with a dedicated `_LATEX_SYSTEM_PROMPT` that focuses the LLM solely on converting LaTeX to spoken form. Two-pass approach: humanize first, then generate transcript. Moved from reading.py-only to shared utility so card.py can use it.
- **Server discovery with fallback**: `_find_fish_speech_server()` scans ports 8080-8083 for an available Fish Speech server, falling back to wait-and-retry if all are busy. Enables multi-server parallel paper processing.
- **Audio truncation fix**: Reverted `chunk_length` to 200 (safe default), bumped `max_new_tokens` to 4096 for headroom. Timeout increased from 300s to 600s.
- **Richer inline pauses**: Fish Speech path now adds `[short pause]` after sentence-ending periods, not just paragraph breaks. Stacked tags are collapsed.

## 2026.04.15 - Multi-server Fish Speech parallelism

Scale Fish Speech audio generation across multiple GPU server instances by distributing chunks round-robin. A single paper's audio chunks now process concurrently instead of serially, cutting wall time roughly in proportion to the number of healthy servers.

- **Server discovery with caching**: `_discover_fish_speech_servers()` health-checks all `_FISH_SPEECH_PORTS` once and caches the healthy list. Re-discovers when the cached count is below the configured port count so late-starting servers get picked up.
- **Round-robin picker**: `_pick_fish_speech_server()` replaces the old "find one and wait" logic with a thread-safe global counter that hands out servers in rotation.
- **Parallel batch helper**: New `tts_chunks_parallel()` accepts `(text, output_path)` pairs and runs them through a `ThreadPoolExecutor` sized to the number of healthy servers. Falls back to sequential when only one server is available or only one chunk is queued.
- **Longer client timeout**: `_tts_fish_speech()` httpx client timeout bumped from 600s to 1800s to tolerate large chunks on slower GPUs.
- **Sentence-fallback chunking**: `chunk_text_paragraphs()` now pre-splits any single paragraph that exceeds `max_chars` at sentence boundaries, so no chunk ever exceeds the limit. Previously oversized paragraphs were emitted as-is, which Fish Speech would truncate.

## 2026.04.16 - Pause-based chunk transitions and chunk retention for surgical regeneration

Replaced 200ms cross-fade between TTS chunks with direct concatenation, letting Fish Speech `[long pause]` and ElevenLabs `<break>` tags supply transitions naturally. Crossfade was clipping sentence endings and the timbre mismatch across independently-synthesized chunks was audible. At the same time, chunk files are now retained instead of being deleted, so re-running TTS on a single bad chunk and restitching is possible without regenerating the whole audio.

- **Crossfade defaults flipped to 0**: `combine_audio()` and `combine_audio_with_section_pauses()` now default `crossfade_ms` / `chunk_crossfade_ms` to `0` instead of `200`. Existing call sites pass `chunk_crossfade_ms=0` explicitly so behavior is independent of the default.
- **`append_chunk_pause(text, provider)`**: Idempotent helper that appends `[long pause]` (Fish Speech) or `<break time="1.0s" />` (ElevenLabs) to the end of a chunk's text. The ElevenLabs idempotency check looks for any trailing self-closing SSML tag (`/>`), which is intentional -- we do not stack any trailing SSML.
- **`write_chunk_manifest(chunks_dir, audio_type, output_file, chunks, ...)`**: Writes `chunk_manifest.json` next to the chunk files. Records audio type, output filename, optional bookend filenames, and per-chunk index/section/text/file. Drives the surgical-regen workflow.
- **`restitch_from_chunks(manifest_path, output_path, ...)`**: Reads the manifest, groups chunk paths by section, and calls `combine_audio_with_section_pauses` to reassemble final audio. Asserts each chunk file exists before assembly so a missing chunk fails fast.

## 2026.04.17 - Expanded humanization prompt for ASCII math, units, inequalities, and stray dollars

`_LATEX_SYSTEM_PROMPT` now covers the full span of inline notation that reaches TTS, not just `$...$` delimited LaTeX. Orange annotations on the zvyagin paper's reading audio showed recurring failures on bare unicode Greek (e.g. "p_θ"), inequalities read as "greater than" when "more than" is more natural, unit abbreviations ("12 h" → "12 hours"), version numbers ("NCCL 2.10.3"), approximation tildes, and stray dollar signs leaking through from mathpix output. Card audio was already using this prompt; reading now shares it too (see `swanki.audio.reading`).

- **Stray-dollar rule**: Explicit instruction to delete any bare `$` not clearly delimiting a math expression, so the TTS never says "dollar" unless prose is about currency.
- **Inequalities**: `>` → "more than" (not "greater than"), `<` → "less than", `≥`/`≤` → "at least"/"at most".
- **Units**: numeric-adjacent `h`/`s`/`min`/`ms`/`bp`/`kb`/`Mb`/`GB`/`TB` expand to full words; acronym units like `CPU`/`GPU` stay as acronyms.
- **Version numbers**: `NCCL 2.10.3` → "N C C L version 2.10.3" — prefix "version" and keep the dotted sequence intact.
- **Bare Greek in prose**: covers the common case where a figure caption or inline math loses its delimiters after markdown conversion, leaving unicode Greek letters floating in prose.
