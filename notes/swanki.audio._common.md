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
