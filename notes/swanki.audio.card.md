---
id: eec275051e774ac494ab386
title: Card
desc: ''
updated: 1773142603440
created: 1773142603440
---

## 2026.03.10 - Flashcard audio generation with cloze handling and citation prefixing

Extracted from monolithic audio module. Handles cloze masking (`_replace_all_cloze_with_blank` for front, `_remove_cloze_markers` for back), image summary integration, LLM-based transcript generation via detailed system prompts (`_build_transcript_system_prompt`), citation humanization, and multi-chunk TTS with combination.

## 2026.03.12 - Migrate from OpenAI client to pydantic-ai agents

Replaced direct `OpenAI` client calls with shared `text_agent` from `swanki.llm.agents`. Removed `client: OpenAI` and `openai_client` parameters from `generate_card_transcript`, `generate_citation_audio`, and `generate_card_audio` -- all now accept a `model: str` parameter in pydantic-ai format (e.g. `"openai:gpt-5-mini"`). Manual retry loops replaced by agent-level `retries=3`. Fixed hardcoded `"gpt-4o-mini"` in `_humanize_citation` to use the configured model string. Part of Step 5 ([[plan.major-refactor-sequence.plan-0]]).

## 2026.03.12 - Add card_id fallback for audio filename generation

`card_uuid` now falls back to `str(card_index)` when `card.card_id` is `None`, preventing blank filenames in audio output. This handles cards generated before UUID assignment.

## 2026.04.03 - Two-pass LaTeX humanization and Fish Speech tts_kwargs passthrough

Added a dedicated LaTeX humanization pass before card transcript generation to prevent raw LaTeX from reaching TTS. Previously the LLM had to simultaneously convert LaTeX AND optimize text for audio in a single pass, causing frequent failures where math notation was read aloud verbatim.

- **Two-pass approach**: If card content contains `$` or `\`, `humanize_latex()` from `_common.py` runs first with a focused LLM prompt that only converts LaTeX to spoken form. The transcript LLM then works with already-clean text.
- **tts_kwargs passthrough**: `generate_card_audio()`, `generate_citation_audio()`, and all internal `text_to_speech()` calls now accept and forward `**tts_kwargs` for Fish Speech provider support.
