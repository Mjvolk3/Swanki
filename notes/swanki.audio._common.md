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
