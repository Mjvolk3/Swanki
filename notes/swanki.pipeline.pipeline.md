---
id: gc296t2rsgc6sx28n224rgq
title: Pipeline
desc: ''
updated: 1773270048272
created: 1773013975831
---

## 2026.03.08 - Integrate ApkgExporter for direct .apkg output

Wire the new `ApkgExporter` into the pipeline so that `.apkg` files are generated alongside markdown card output when `create_anki_deck` is configured. The exporter runs after plain card writing (step 8) and again after audio generation (step 9b) to produce a final deck with audio URIs. This removes the dependency on a running AnkiConnect instance for basic deck creation.

## 2026.03.10 - Update audio imports to new swanki.audio package

Redirect audio function imports from `..utils.audio` to `..audio` following the refactor of the monolithic audio module into a standalone package.

## 2026.03.11 - Add audio_only mode to skip card generation

Enable users to produce audio outputs (lecture, summary, reading) without running the expensive card generation pipeline. This is Step 1 of the major refactor sequence ([[plan.major-refactor-sequence.plan-0]]).

- `process_full()` reads `config["mode"]` (default `"full"`). When `"audio_only"`, stages 5.5-8 (estimate, confirm, card gen, output write) are skipped; shared stages (PDF split, markdown, images, summary) and audio still run.
- `generate_audio()` guards complementary audio with `if not cards:` -- logs a warning and skips since complementary audio requires cards.
- The "write cards with audio" block at the end of `generate_audio()` also checks `and cards` to avoid writing an empty file.
- A warning is logged when `mode=audio_only` with no audio types enabled.

## 2026.03.11 - Add character-based segmentation mode for card generation

Introduce a unified "segment" abstraction so card generation operates on segments rather than pages. This is Step 3 of the major refactor sequence ([[plan.major-refactor-sequence.plan-0]]).

- New segmentation stage in `process_full()` inside the `mode == "full"` branch. When `segmentation: char`, pages are recombined and re-split into uniform character-length segments; when `segmentation: page` (default), behavior is unchanged.
- Card generation loop rewritten for document-order interleaving: text cards per segment, then image cards for the pages covered by that segment, with dedup via `last_image_page` tracking.
- Renamed `_generate_cards_for_page_with_context` to `_generate_cards_for_segment` to reflect the unified concept.
- Deleted `generate_cards_with_context()` (~333 lines of dead code never called by `process_full()`).
- Config key renames: `num_cards_per_page` to `cards_per_segment`, `cloze_cards_per_page` to `cloze_per_segment`. Dead `chunk_size`/`overlap` params removed.
- `estimate_card_count` updated to accept segment files and use segment terminology.

## 2026.03.11 - Read SI boundary metadata for lecture generation

Before calling `generate_lecture_audio()`, read `{citation_key}_meta.json` from the PDF directory to get `si_start_page`. Pass it as a kwarg so lectures can treat main paper and SI content separately. Falls back to `None` (today's behavior) when the file is absent. Part of Step 4 ([[plan.major-refactor-sequence.plan-0]]).

## 2026.03.12 - Migrate from instructor/OpenAI to pydantic-ai agents

Replaced all instructor and direct OpenAI calls with pydantic-ai agents from `swanki.llm.agents`. This is the largest file in the migration (Step 5 of [[plan.major-refactor-sequence.plan-0]]).

- Removed `self.instructor = instructor.patch(OpenAI())` from `__init__` and `OpenAI(api_key=...)` from `generate_audio()`.
- Removed `instructor`, `openai`, and `tenacity` imports.
- `generate_document_summary` uses `document_summary_agent.run_sync()` with `output_type=DocumentSummary`.
- Card generation (4 call sites: regular, cloze, 2x image) uses `card_gen_agent.run_sync()` with `output_type=CardGenerationResponse`. Tenacity retry wrappers replaced by agent `retries=3`.
- Self-critic loop: `_evaluate_cards` uses `card_feedback_agent`, `_refine_cards` uses `card_gen_agent`, `_generate_audio_feedback` uses `audio_feedback_agent`.
- `_refine_audio_transcript` uses shared `text_agent` (previously `response_model=None`).
- `ImageProcessor` initialized with `model: str` instead of `self.instructor`.
- Audio generation functions called without `openai_client` parameter.
