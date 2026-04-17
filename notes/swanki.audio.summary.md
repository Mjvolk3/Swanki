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
- **Proportional length cap**: Summary word limit now scales with source length (20%, floor 200, cap 800) instead of fixed 1200 words. Prompt reinforces "shorter than lecture" constraint. Prevents summary from exceeding lecture length on short papers.
- **Paragraph-only chunking for Fish Speech**: Switches to `chunk_text_paragraphs()` with 2000 char max when using Fish Speech. Section pauses increased to 3s.

## 2026.04.15 - Parallel chunk dispatch across Fish Speech servers

Summary audio now flattens chunks across all sections into one job list and dispatches via `tts_chunks_parallel()` for Fish Speech, regrouping paths by section index afterwards. Mirrors lecture and reading so summary generation also benefits from multi-server parallelism.

## 2026.04.16 - Summary chunks retained in `summary_chunks/` with manifest

Summary audio chunks now live under `summary_chunks/` and are kept after combination, paired with a `chunk_manifest.json` so individual chunks can be re-TTS'd and restitched via `restitch_from_chunks()`. Mirrors lecture and reading.

- Each chunk gets `append_chunk_pause(text, provider)` before TTS so direct concatenation (no crossfade) sounds seamless.
- Bookends are written into `summary_chunks/`, co-located with the chunks they bracket.
- `combine_audio_with_section_pauses()` is invoked with `chunk_crossfade_ms=0` explicitly. The cleanup `unlink()` block is gone.

## 2026.04.17 - Target 3-10 minute audio with explicit floor/ceiling; raise max_tokens for reasoning models

Previous summary cap was 200-800 words (aim 20% of source), which produced 1-5 minute narrations — too thin for the summary to stand on its own. Bumped target to **500-1650 words** (3-10 min at ~165 wpm with the 1.1x speed multiplier), with explicit floor and ceiling in the prompt. Also bumped `max_tokens` because gpt-5 reasoning models were exhausting the old budget before emitting any output.

- **Explicit floor and ceiling in prompt**: "TARGET LENGTH: between {floor} and {ceiling} words (aim near {word_cap}). Below the floor feels thin; above the ceiling stops being a summary." Matches the symmetric bounds approach now used in `swanki.audio.lecture`.
- **Soft aim scales with source**: `word_cap = clamp(source_words * 0.35, 500, 1650)` — longer source papers get a summary closer to the ceiling, shorter ones stay near the floor.
- **`max_tokens = max(word_cap * 4, 4000)`**: Previous `max(word_cap * 2, 1000)` was causing `Model token limit (1776) exceeded before any response was generated` on gpt-5 reasoning models, which consume budget on hidden reasoning tokens. Bumped multiplier to 4x and floor to 4000.
- **Educational-context preamble**: Prepended to the system prompt (same text as lecture/reading) to help safety filters clear on biosecurity-adjacent content.
- **`model: str` required**: No more hardcoded `gpt-5-mini` fallback — caller must pass the configured LLM.
