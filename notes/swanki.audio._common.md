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
