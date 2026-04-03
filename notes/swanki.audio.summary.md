---
id: 3efb827648a14ff3aac6e6a
title: Summary
desc: ''
updated: 1773142603440
created: 1773142603440
---

## 2026.03.10 - Document summary narration with SSML pauses

Extracted from monolithic audio module. Generates narration-style audio from document summaries with citation announcements, SSML `<break>` tags for pauses, and cleaned markdown transcripts saved alongside the audio.

## 2026.03.12 - Migrate from OpenAI client to pydantic-ai agents

Replaced direct `OpenAI` client call with shared `text_agent` from `swanki.llm.agents`. Removed `openai_client` parameter from `generate_summary_audio` -- now accepts `model: str` in pydantic-ai format. Manual retry loop replaced by agent-level `retries=3`. Part of Step 5 ([[plan.major-refactor-sequence.plan-0]]).

## 2026.03.13 - Section-aware assembly, bookends, acronym injection

Replaced SSML `<break time="1.0s"/>` tags with `---SECTION_BREAK---` markers for real silence between summary points. Added START/END bookend announcements via `generate_bookend_audio`. Acronyms extracted from source text and injected into the LLM prompt for reliable first-use expansion.

## 2026.03.15 - Summary length cap, anti-pause prompt, flash TTS, SSML pauses

Four changes to improve summary audio quality and reduce costs.

- **Length cap**: Added "STRICT LENGTH LIMIT: Keep under 1200 words" instruction and reduced `max_tokens` from 1500 to 1200. Ensures summaries stay under 10 minutes.
- **Anti-pause/spelling prompt**: Explicitly bans `[pause]`, `[Pause]`, `Pause.` and letter-by-letter spelling in the system prompt. Old summaries literally said these words aloud.
- **Flash TTS model**: Now uses `eleven_flash_v2_5` (default) instead of `eleven_multilingual_v2` -- 0.5x credit cost.
- **SSML pauses**: `add_tts_pauses()` inserts `<break>` tags at paragraph boundaries for natural pacing, replacing the old approach of writing pause instructions in the transcript.

## 2026.04.03 - Fish Speech tts_kwargs passthrough and provider-aware pauses

Added `**tts_kwargs` parameter to `generate_summary_audio()` for Fish Speech provider support. All `text_to_speech()`, `generate_bookend_audio()`, and `add_tts_pauses()` calls now forward provider info. Pause insertion uses `[pause]`/`[short pause]` tags for Fish Speech instead of SSML `<break>`.
