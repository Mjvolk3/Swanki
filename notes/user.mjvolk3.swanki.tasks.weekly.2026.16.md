---
id: ctvyty0ac2uwuefo2r5qtf9
title: '16'
desc: ''
updated: 1776292556935
created: 1776292556935
---

## 2026.04.15

- [x] Add nightly Zotero MP3 zip export script for BookPlayer import on M1 Mac [[scripts.zip_swanki_mp3s#2026-04-15---nightly-zotero-mp3-zip-export-for-bookplayer]]

## 2026.04.17

- [x] Expand LaTeX humanization prompt to cover ASCII math, inequalities, units, version numbers, and bare Greek — kills dollar-sign leakage and verbatim math in reading audio [[swanki.audio._common#20260417---expanded-humanization-prompt-for-ascii-math-units-inequalities-and-stray-dollars]]
- [x] Consolidate reading's humanizer with `_common` and rewrite its system prompt for figure-caption bracketing, acronym repeat-expansion ban, author-year citations without "et al", and no-filler section starts [[swanki.audio.reading#20260417---consolidate-humanization-caption-citation-acronym-and-transition-rules]]
- [x] Add educational-context preambles, symmetric length bounds (floor injection at <20% mirrors existing cut at >45%), and enforce required `model` parameter across lecture generation, refinement, and critique [[swanki.audio.lecture#20260417---educational-context-preambles-symmetric-length-bounds-and-model-required]]
- [x] Retarget summary audio to 3-10 minute band (500-1650 words) with explicit floor/ceiling prompt, bump `max_tokens` for gpt-5 reasoning overhead, and require `model` param [[swanki.audio.summary#20260417---target-3-10-minute-audio-with-explicit-floorceiling-raise-max_tokens-for-reasoning-models]]
- [x] Drop hardcoded `gpt-5-mini` default from all card audio functions so direct callers no longer silently downgrade from the configured LLM [[swanki.audio.card#20260417---drop-hardcoded-model-defaults-model-required-from-caller]]
- [x] Require `model` on `ImageProcessor.__init__` to match the config-is-source-of-truth discipline applied to all audio modules [[swanki.processing.image_processor#20260417---model-parameter-required-remove-hardcoded-gpt-4o-default]]
- [x] Fix Zotero item lookup (progressive-query search + native `citationKey` field) and tag the parent item with 🦊 after a successful Swanki upload [[swanki.sync.zotero#20260417---robust-citation-key-lookup-and-fox-emoji-tag-on-upload]]
