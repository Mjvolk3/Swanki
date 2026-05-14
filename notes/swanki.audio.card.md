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

## 2026.04.16 - Card chunks retained in `card_chunks/` with per-card manifest

Per-card front/back chunks now live under `audio_dir/card_chunks/` and are kept after combination. Each card writes its own `{card_uuid}_manifest.json` so re-TTS of one chunk and restitch is possible without regenerating other cards. Per-card filenames avoid the race condition that a shared manifest would have under the existing parallel card processing in `pipeline.py`.

- **Pause-before-concat**: `append_chunk_pause(text, provider)` is applied to every TTS chunk before dispatch, so the front (citation prepended + chunked transcript) and back combine cleanly with `combine_audio(..., crossfade_ms=0)`. Citation audio is treated as a pre-existing file (`type: "citation"` in the manifest) and not given an appended pause.
- **Manifest shape**: `{card_id, card_index, front_file, back_file, citation_audio, sides: {front: {chunks: [...]}, back: {chunks: [...]}}}`. The `citation_audio` field is a relative path (`../{citation_key}_citation.mp3`) since the citation audio stays in `audio_dir` (shared, pre-generated once before the parallel card loop).
- **Cleanup removed**: The `.unlink()` calls on chunk files at the end of front and back generation are gone. Single-chunk single-side cards (no citation) still write directly to the final path with no chunks subdir.

## 2026.04.17 - Drop hardcoded model defaults; model required from caller

Removed `model: str = "openai:gpt-5-mini"` defaults from `generate_card_transcript`, `generate_citation_audio`, `generate_card_audio`, and `_humanize_citation`. The pipeline was already passing the config-resolved model (`gpt-5.2` / `gpt-5.4`) to every call site, so the hardcoded defaults were unreachable in production and acted as a footgun for direct callers (e.g. one-off regen scripts) that silently downgraded to `gpt-5-mini`. All four signatures now take `model: str | None = None` and raise `ValueError` early if left unset, so the LLM config is always the single source of truth.

## 2026.05.14 - Add _preprocess_for_tts helper and wire into all 5 text_to_speech sites

Card audio bypasses `clean_markdown_for_tts` and `add_tts_pauses` (cards are short and arrive already TTS-shaped) so the pre-TTS scrubber pipeline didn't naturally land here. Added `_preprocess_for_tts(text, tts_kwargs)` helper at module level that runs the same scrubber chain as lecture/summary/reading: `strip_chapter_filename_slug` -> `expand_acronyms_for_tts` (fish only) -> `apply_pronunciation_overrides` -> `strip_forbidden_fish_tags` (fish only).

All 5 `text_to_speech` call sites now wrap their text arg with this helper:
- `generate_citation_audio` line 332 (citation announcement)
- `generate_card_audio` line 493 (single-chunk front)
- `generate_card_audio` line 514 (multi-chunk front loop)
- `generate_card_audio` line 536 (single-chunk back)
- `generate_card_audio` line 546 (multi-chunk back loop)

No chunker change (cards use `chunk_text` and stay short). No combine change (cards use `combine_audio` not `combine_audio_with_section_pauses`). The today's chunk-boundary pause-tag strip from `append_chunk_pause` already applies to cards since they call that function.
