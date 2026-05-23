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
