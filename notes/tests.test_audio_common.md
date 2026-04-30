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
