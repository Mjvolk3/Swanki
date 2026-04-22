---
id: 5919f28fc4494149b81400c
title: Lecture
desc: ''
updated: 1773142603440
created: 1773142603440
---

## 2026.03.10 - Educational lecture generation with semantic chunking and self-refinement

Extracted from monolithic audio module. Implements `chunk_by_headers` for semantic section splitting, `generate_and_validate_chunk` with per-section LLM critique, and an iterative refinement loop (`_refine_transcript`) targeting 50% of source length. Uses `instructor` for structured `LectureTranscriptFeedback` responses.

## 2026.03.11 - Lecture transcript refactor (Step 4)

Major overhaul addressing two problems: false mid-lecture conclusions when SI pages follow the main paper, and broken per-section word budgets causing excessively long lectures. Part of ([[plan.major-refactor-sequence.plan-0]]).

- **Length control refactor**: Removed `section_budget_words` / `section_max_words` params from `generate_and_validate_chunk()`. Critique prompt now checks quality only (LaTeX, citations, lists, tone). Length enforcement moved to `_refine_transcript()` via source-word ratio — injects length-reduction feedback when ratio > 0.7, logs warning when < 0.3. System prompt target changed to "40-60% of source manuscript length".
- **Broadened `chunk_by_headers()`**: Now matches unnumbered headers (`## Methods`, `## Results`) in addition to numbered (`## 1.0 Introduction`). Uses two regex patterns tried in order: numbered first, unnumbered fallback. Requires h2+ to avoid matching h1 titles.
- **SI splitting**: `generate_lecture_audio()` accepts `si_start_page` to split `markdown_files` into main and SI. Main content is chunked; SI is indexed separately.
- **SI indexing**: New `build_si_index()` parses SI content at markers (Extended Data Fig, Supplementary Fig, Table S, Methods headers) into a `dict[str, str]`. New `extract_relevant_si()` scans each main section for SI references and returns matched snippets with fuzzy key normalization.
- **SI enrichment**: Per-section SI snippets passed to `generate_and_validate_chunk()` via `si_reference_content` param, appended to user message. Single-pass path passes truncated SI directly. SI instructions appended to system prompt.
- **SI balance constraint**: When SI content is provided, critique prompt includes an SI BALANCE CHECK requiring at least 50% main paper coverage.

## 2026.03.12 - Migrate from instructor/OpenAI to pydantic-ai agents

Replaced dual-client pattern (`instructor.from_openai()` + `instructor.patch()`) with `lecture_critic_agent` and shared `text_agent` from `swanki.llm.agents`. Removed `openai_client` and `instructor_client` parameters from all functions. Three structured call sites now use `lecture_critic_agent.run_sync()` for critique and `text_agent.run_sync()` for generation/refinement. Critique-regenerate loop preserved identically. Part of Step 5 ([[plan.major-refactor-sequence.plan-0]]).

## 2026.03.13 - Lecture structure enforcement, analogy rule, section-aware assembly, bookends, acronyms

Addresses quality issues identified from listening to merzbacher paper lecture: meandering structure, over-analogizing, no section pauses, no bookend announcements.

- **Structure enforcement**: System prompt now mandates labeled sections (Introduction, 2-4 Results/Discussion, Conclusion and Future Directions) separated by `---SECTION_BREAK---` markers
- **Analogy rule**: New rule 7 -- "Use analogies to illuminate, not replace. Every analogy must be followed by the precise technical statement"
- **Section-aware assembly**: Replaced flat `combine_audio` with `combine_audio_with_section_pauses` for real silence between lecture sections
- **Bookends**: Generates lecture-specific bookends ("Today's lecture is posted as: ..." / "And with that we conclude: ...") via new `paper_title` parameter
- **Acronyms**: `extract_acronyms()` scans source content and injects definitions into the system prompt

## 2026.03.15 - Great Courses style overhaul, methods/SI classification, length caps, prosody improvements

Major lecture quality pass driven by listening to thornburg (39 min, repetitive methods sections) and docter (lecture longer than reading). Four areas of change.

- **System prompt rewrite**: Replaced generic educator prompt with Great Courses-style instructions. Influences: Sagan, Feynman, Lane. Mandatory opening roadmap ("Today we'll cover three things..."), spoken section transitions (no markdown headers), author-faithful tone (modest, never overselling), ban on meta-commentary ("in the text, an image shows", "for audio purposes"). Length target tightened from 40-60% to 25-35% of source.
- **Methods/SI section classification**: New `_PREAMBLE_HEADERS` and `_METHODS_SI_HEADERS` regex patterns. After `chunk_by_headers()`, sections are classified into main (drives lecture structure) vs methods/SI (enrichment only). Uses positional cascade: once a methods header (e.g., "KEY RESOURCES TABLE") is seen, all subsequent sections are methods/SI. Methods/SI content is indexed via `build_si_index()` and passed to main sections as enrichment context through the existing `extract_relevant_si()` pipeline. For thornburg: 67 sections reduced to 12 main + 55 enrichment.
- **Hard length cap**: `_refine_transcript()` now truncates at `min(source_words, 4500)` after refinement, finding the last sentence boundary. Prevents lectures from exceeding ~30 minutes regardless of refinement loop outcome.
- **Prosody**: Paragraph-only TTS chunking via `chunk_text_paragraphs()` (4500 char max, never mid-sentence). 3-second section pauses (up from 2s). SSML `<break>` tags injected via `add_tts_pauses()`. Premium `eleven_multilingual_v2` model for lecture TTS; all other audio types use cheaper `eleven_flash_v2_5`.

## 2026.04.03 - Fish Speech prosody tags and tts_kwargs passthrough

Added Fish Speech inline prosody tag support for lecture audio generation, producing more expressive and natural-sounding lectures when using the self-hosted TTS provider.

- **Prosody tag instructions**: When `provider=fish_speech`, appends `_FISH_SPEECH_TAG_INSTRUCTIONS` to the lecture system prompt. Instructs the LLM to insert `[pause]`, `[short pause]`, `[emphasis]`, `[excited]`, and `[inhale]` tags sparingly (1-3 per section) for natural pacing and emphasis. ElevenLabs path is unchanged.
- **Provider-aware pauses**: `add_tts_pauses()` call now passes the provider so post-processing uses `[pause]` tags instead of SSML `<break>` for Fish Speech.
- **tts_kwargs passthrough**: `generate_lecture_audio()`, bookend calls, and all `text_to_speech()` calls forward `**tts_kwargs`.
- **Critic accepts Fish Speech tags**: `_CRITIQUE_PROMPT_FISH_SPEECH` variant adds an exception so `[pause]`, `[emphasis]`, etc. are not flagged as meta-commentary. Threaded through `_refine_transcript()` via `critique_prompt` parameter.
- **Paragraph-only chunking for Fish Speech**: Uses `chunk_text_paragraphs()` with 2000 char max (vs 4500 for ElevenLabs) to avoid mid-sentence truncation. Longer section pauses (4s vs 3s).

## 2026.04.15 - Parallel chunk dispatch across Fish Speech servers

Lecture audio now collects every chunk across every section into a single job list before TTS, then dispatches the whole batch through `tts_chunks_parallel()` for Fish Speech (or sequentially for ElevenLabs). Eliminates the per-section serial bottleneck so a multi-server setup actually saturates all GPUs for a single lecture.

- Job list is `(section_idx, text, chunk_path)` so chunks can be regrouped back into per-section lists after parallel TTS for the existing `combine_audio_with_section_pauses()` path.
- ElevenLabs path stays sequential with the original `time.sleep(1)` rate-limiter.

## 2026.04.16 - Lecture chunks retained in `lecture_chunks/` with manifest

Lecture audio chunks now live under `lecture_chunks/` next to the final MP3 instead of at the parent path, and they are no longer deleted after combination. A `chunk_manifest.json` records every chunk's section, text, and filename plus the bookend filenames, enabling surgical re-TTS of one bad chunk followed by `restitch_from_chunks()` to rebuild the lecture without regenerating everything.

- `append_chunk_pause(text, provider)` is applied to every chunk before TTS dispatch so direct concatenation (no crossfade) sounds seamless. Provider-aware: Fish Speech gets `[long pause]`, ElevenLabs gets `<break time="1.0s" />`.
- Bookend audio is also written into `lecture_chunks/`, keeping all per-lecture audio assets co-located for restitch.
- `combine_audio_with_section_pauses()` is now invoked with `chunk_crossfade_ms=0` explicitly. The cleanup `unlink()` block is gone.

## 2026.04.17 - Educational-context preambles, symmetric length bounds, and model required

Two problems surfaced when regenerating the zvyagin (SARS-CoV-2 GenSLMs) lecture: (1) OpenAI's safety filter blocked `gpt-5.2` on biosecurity-adjacent content — the full-doc critique got 400s and fell back to weak chunked critique, letting the lecture stay at 48% of source well above the 25-35% target; (2) when the filter did NOT fire, the length loop overshot the other way and trimmed to 7% of source because the refinement was cut-only with no symmetric expand branch. Both are addressed here; `gpt-5.4` also behaves better on this content and is the practical fix for (1).

- **Educational-context preamble**: Prepended to `_DEFAULT_LECTURE_SYSTEM_PROMPT`, `_REFINEMENT_TEMPLATE`, `_CRITIQUE_PROMPT`, and the inline section-level critique inside `generate_and_validate_chunk`. Text frames the lecture as a "peer-reviewed educational summary of already-published methods — no novel technical uplift, no operational instructions, no capability synthesis beyond what the paper itself provides". Helped safety-filter false-positives clear on 5.4 (still not enough for 5.2 on genomics content; model upgrade is the real fix).
- **Symmetric length refinement**: `_refine_transcript` now forces `critique_feedback.done = False` when the ratio is outside `[0.20, 0.45]`, keeping the loop alive. Injects `LENGTH: EXPAND` feedback when ratio < 20% (mirror of the existing `LENGTH: CUT` at > 45%). Stops the asymmetric cut-only behavior that drove v2 to 7% of source.
- **`model: str` required**: `critique_transcript_chunks` and `generate_lecture_audio` no longer default to `openai:gpt-5-mini`. Matches card/reading/summary — config LLM must be passed explicitly; `ValueError` if left `None`.

## 2026.04.22 - Word-count budget, chunk-aware refinement, duplicate-opener guard

The ratio-of-source budget was producing too-short lectures for small papers (merzbacher 8 min, tazza 9 min) and too-long ones for dense books (would exceed 30 min cap). Switched to an absolute word-count band centered on 30% of source, with explicit floor and ceiling. Independently, the refine loop was regenerating full lectures when a tail chunk got `LENGTH: EXPAND` feedback — the model took the full system prompt's "OPENING → BODY → CLOSING" structure literally and appended a second intro + roadmap, guillotined at the hard cap. Fixed at two layers: tightened prompts so refinement cannot add new openings, and a post-refine `_strip_duplicate_openers()` guard catches any that slip through.

### Word-count budget

- New module constants: `PLANNING_WPM = 130` (measured fish_speech@1.1x rate), `LECTURE_SOURCE_RATIO = 0.30`, `LECTURE_WORD_FLOOR = 1500` (~11.5 min), `LECTURE_WORD_CAP = 3900` (30 min hard cap).
- `_compute_lecture_target_words(source_words)` returns `(target, floor, ceiling)` where target = `clamp(source * 0.30, 1500, 3900)` and the band is `[0.85·target, 1.15·target]` clamped to the same limits.
- `_DEFAULT_LECTURE_SYSTEM_PROMPT` LENGTH rule rewritten with `${target_floor}`, `${target_ceiling}`, `${target_words}` Template placeholders; injected via `Template(system_instructions).safe_substitute(...)` at call time.
- `_refine_transcript` length checks switched from ratio bands (`0.20-0.45`) to absolute word-count bands. Same shape: force `done = False` and inject `LENGTH: EXPAND`/`CUT` feedback when outside band.
- Hard truncation at the end of the refine loop now caps at `LECTURE_WORD_CAP` regardless of source word count (was `min(source_words, 4500)`).

### Chunk-aware refinement

- New `_REFINE_SYSTEM_PROMPT`: explicit "you are editing a chunk of an existing lecture; do NOT add new intros/roadmaps/closings". Used as `instructions` for refinement calls instead of `full_system_prompt` (which mandated the full lecture arc).
- `_REFINEMENT_TEMPLATE` reworded: headline says "revise ONLY the chunk below", adds a HARD CONSTRAINTS block listing forbidden additions (opening hook, roadmap, closing summary, paper topic framing), and the closing instruction says "PROVIDE THE REVISED CHUNK (same scope, same position in the lecture)" instead of "PROVIDE THE COMPLETE REVISED TRANSCRIPT".
- `_CRITIQUE_PROMPT` LENGTH item (#3) simplified — code enforces the band now, critic focuses on style/substance.

### Duplicate-opener guard

- New `_strip_duplicate_openers(transcript)` helper, invoked right after `_refine_transcript` returns. Scans for multiple occurrences of `"Today we'll cover"` (both straight and smart apostrophe variants).
- Two modes: if the second occurrence is followed by a `---SECTION_BREAK---` and substantial content (>100 words) after it, excise just the restart block (last-period-before-duplicate to end-of-trailing-break), preserving downstream body sections. Otherwise the restart runs to end-of-transcript → truncate at the last sentence boundary before the duplicate.
- Discovered because thornburg v2 and zvyagin v6 both produced transcripts ending with a second opening hook + roadmap + body; bookmark from Prologue pinpointed "At the conclusion it's talking about what we are going to do as if back to the introduction". Transcripts for both papers were hand-fixed and re-TTS'd via `scripts/retts_cleaned_transcripts.py`.
