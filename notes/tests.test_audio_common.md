---
id: ndyydakbszf4csxvpkepy71
title: Test_audio_common
desc: ''
updated: 1773463874748
created: 1773463874748
---

## 2026.03.13 - Tests for section-aware audio infrastructure

Added 14 tests covering the new infrastructure functions: `generate_silence` (duration accuracy), `split_transcript_by_sections` (basic split, empty-between, no-marker, custom marker), `combine_audio_with_section_pauses` (basic sections, bookends, empty), and `extract_acronyms` (parenthetical, reverse pattern, multiple, empty, all-caps skip).

## 2026.04.26 - Tests for Fish Speech Unicode punctuation folding

Three tests for the new `_normalize_fish_speech_punct` helper in `swanki/audio/_common.py`: em-dash and en-dash mapping to comma+space and ASCII hyphen, curly quotes and ellipsis folding, and an ASCII-only passthrough check.

## 2026.05.14 - Coverage for new TTS-prep helpers + previously-untested combine params

Two formerly-broken assertions corrected (`test_append_chunk_pause_fish_speech`, `test_append_chunk_pause_strips_trailing_whitespace`): they expected `[long pause]` but production has emitted `[pause]` since 2026-04-26 (Fish renders `[long pause]` as audible breath/sigh — the test was the stale side, not the production code).

24 new test functions covering the Hamming bookmark plan's deterministic helpers and the previously-uncovered `combine_audio_with_section_pauses` parameters:

- `strip_forbidden_fish_tags` (5): sigh removal, allowed-tag preservation, idempotency, case insensitivity, full-constant sweep.
- `expand_acronyms_for_tts` (6): SAR -> S-A-R, allowlist skip, camelcase lower-prefix skip, camelcase lower-suffix skip, lowercase no-op, single-letter skip.
- `apply_pronunciation_overrides` (3): whole-word match, substring rejection ("Indecisively" untouched), empty-dict no-op.
- `strip_chapter_filename_slug` (3): basic match, no-match no-change, leading-zero drop ("07" -> "7").
- `detect_repeated_phrases` (4): "his last observation he said" surfaces, stopword-chatter filter ("the way that you can"), no-repetition empty list, below-threshold not flagged.
- `chunk_text_paragraphs` (3): 700-char cap respected, oversize-paragraph sentence-fallback, packs under budget.
- `combine_audio_with_section_pauses` (4): chunk_pause inserts silence (700 ms gap measurable), zero chunk_pause is a no-op, gain_match shifts mean dBFS toward target, chunk_tail_trim_ms=0 doesn't trim. The combine tests require ffmpeg in PATH (pydub dependency); they fail cleanly on machines without ffmpeg same as the existing combine_audio tests do.
