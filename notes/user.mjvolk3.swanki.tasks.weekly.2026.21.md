---
id: 0oyvzrrhyn7gldfv2y805jn
title: '21'
desc: ''
updated: 1779569241493
created: 1779569241493
---

## 2026.05.22

- [x] Replaced the reading-completeness paper-level 0.95 hard-fail with per-chunk completeness retry + verbatim-input fallback in both passes -- catches catastrophic chunk collapse surgically (Hamming Ch1's 0.0075 ratio, qiu-class summarization drops) while letting natural variance (image-URL stripping, "et al" drops) flow through; singh validated the new code in production at 86.6% paper-level coverage with zero Pass-2 fallbacks [[swanki.audio.reading#20260522---per-chunk-completeness-retry-replaces-the-paper-level-hard-fail-floor]]
- [x] Added `_humanize_chunk_with_completeness` Pass-1 helper with floor 0.5 and 3-attempt retry; lifted `text_agent` to module-level in `_common.py` for consistent mock-patching across audio modules [[swanki.audio._common#20260522---humanize_latex-self-heals-chunk-level-collapse]]
- [x] Replaced the prior single guard-tripping test with 8 targeted tests covering per-chunk happy-path, exhausted-retry fallback, "retry succeeds on attempt 2", and floor-constant sanity guards for both passes; 149/149 reading + common tests green [[tests.test_audio_reading#20260522---cover-per-chunk-completeness-retry--fallback-paths]]

## 2026.05.23

- [x] Verified all 5 successful iCBF rest-batch papers (zhang, alenezi, smith, aygun, singh) landed in ABS with full Summary/Reading/Lecture trios; 13/16 iCBF total in ABS; remaining 3 (qiu, qu, swanson) ready for cleanup pass [[swanki.audio.reading#20260522---per-chunk-completeness-retry-replaces-the-paper-level-hard-fail-floor]]

## 2026.05.24

- [x] Lifted the lecture-only `_gen_with_safety_retry` into a generic `with_safety_retry(agent, ...)` in a new `swanki/llm/safety.py` module that works with any pydantic-ai Agent (text or structured-output) and reuses one canonical `EDU_CONTEXT_PREAMBLE` and `SAFETY_REFUSAL_MARKERS` tuple across lecture + card paths [[swanki.llm.safety#20260524---generalized-biosec-refusal-retry-wrapper]]
- [x] Wrapped all 6 `card_gen_agent` / `card_feedback_agent` call sites in `pipeline.py` (regular cards, cloze cards, 2× image cards, self-refine feedback, self-refine output) with the biosec-refusal retry; unblocks the iCBF `qu` (CRISPR) and `swanson` (RBD) failures where a single biosec-refused LLM call killed the run despite OCR + image-summaries + segment-classification all having completed [[swanki.pipeline.pipeline#20260524---wrap-all-6-card_gen_agent--card_feedback_agent-calls-with-the-biosec-refusal-retry]]
- [x] Refactored `lecture.py`'s `_gen_with_safety_retry` to be a thin wrapper around the shared helper, preserving its "return empty string on terminal failure" contract while removing the now-duplicate local constants [[swanki.audio.lecture#20260524---_gen_with_safety_retry-becomes-a-thin-wrapper-over-the-shared-helper]]
- [x] Added 8 tests covering happy path, retry on both `SAFETY_REFUSAL_MARKERS`, exhaustion-then-raise, non-safety pass-through, `model_settings` forwarding, and constants sanity; full audio + safety suite 30/30 green [[tests.test_llm_safety#20260524---coverage-for-the-generic-biosec-refusal-retry-wrapper]]
