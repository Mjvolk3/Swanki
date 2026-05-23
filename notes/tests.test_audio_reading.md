---
id: 2qciti203tek3df5peklgpu
title: Test_audio_reading
desc: ''
updated: 1773321066457
created: 1773321066457
---

## 2026.03.12 - Update mocks for pydantic-ai migration

Updated test mocks from patching `OpenAI` client to patching `swanki.audio.reading.text_agent.run_sync`. Removed `openai_client` parameter from test function calls.

## 2026.03.13 - Update mocks for section-aware assembly

Replaced `combine_audio` mock with `combine_audio_with_section_pauses` mock to match the new section-aware assembly flow in `reading.py`.

## 2026.05.22 - Cover per-chunk completeness retry + fallback paths

Anchors the per-chunk self-healing landed in [[swanki.audio.reading]] and
[[swanki.audio._common]] (both 2026.05.22). The prior single
`test_reading_coverage_dropped_paragraph_trips_guard` test asserted the
paper-level hard-fail floor, which no longer exists -- now there are 8
targeted tests covering the new behavior:

- **`reading_coverage_ratio` as a pure diagnostic** -- four tests confirm
  the function reports passthrough / expansion / drop / empty-source
  ratios without raising. Replaces the prior "trips guard" assertion that
  was bound to the removed `_READING_COVERAGE_MIN_RATIO` constant.
- **`_humanize_chunk_with_completeness` (Pass-1)** -- three tests:
  happy-path single-shot success, three-attempt exhaustion -> raw-input
  fallback, and a "retry succeeds on attempt 2" path that asserts the
  helper returns the second result and stops retrying.
- **`_pass2_chunk_with_completeness` (Pass-2)** -- two tests mirroring
  the happy-path and exhaustion cases, plus assertion that the returned
  `fell_back` flag is `True` only when the input is returned verbatim.
- **Floor-constant sanity guards** -- one test per pass asserts the
  module-level floor stays within a sane band (0.1-0.7 for Pass-1, 0.7-0.95
  for Pass-2) so a future tweak that ratchets the floor outside its
  design intent is caught immediately.
- **`test_generate_reading_audio_mocked`** updated to mock both
  `swanki.audio.reading.text_agent` and `swanki.audio._common.text_agent`
  with a long-enough output to clear the per-chunk floor on the first
  attempt -- exercises the new helpers transparently through the
  end-to-end flow.

149/149 tests in `tests/test_audio_reading.py` + `tests/test_audio_common.py`
pass under the new code.
