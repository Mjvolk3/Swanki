---
id: gc296t2rsgc6sx28n224rgq
title: Pipeline
desc: ''
updated: 1773013975831
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
