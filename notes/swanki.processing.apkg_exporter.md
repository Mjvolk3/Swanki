---
id: yo9ks4y8u3j0uhunotsxzcb
title: Apkg Exporter
desc: ''
updated: 1773144184343
created: 1773144184343
---

## 2026.05.05 - Per-card complementary audio not embedded in apkg

`_find_media` searched `base_dir` and its parents (up to 3 levels) but not immediate subdirectories. `prepare_for_anki` strips the directory prefix when converting `[audio-front](gen-md-complementary-audio/foo.mp3)` to `[sound:foo.mp3]`, so the apkg packager re-locates the file by basename alone. Per-card audio lives in `<output_dir>/gen-md-complementary-audio/`, which the original lookup never touched — every export quietly logged "0 media files" while the cards still carried `[sound:...]` references that pointed nowhere. Verified empirically against `_CH01_7`: 61 cards, 122 mp3s on disk, 0 in the apkg → re-export with the patched lookup gives 122 in the apkg and a 27 MB file.

Fix iterates `base_dir.iterdir()` between the direct-hit check and the parent-walk fallback. Two regression tests cover the new path: `test_find_media_searches_immediate_subdirectories` (direct unit test) and `test_media_bundling_resolves_subdirectory` (end-to-end apkg packaging via `[audio-front](subdir/...)` link form).

## 2026.05.19 - Feedback field on Basic + Cloze note types

Added a `Feedback` field at ord 2 to both `_basic_model_json` and `_cloze_model_json`. Templates (`qfmt`/`afmt`) were intentionally NOT changed — the field is silent in review so existing cards render identically; the field exists to be edited in the Anki note editor during review, then read out later by a daily AnkiConnect triage job (see [[swanki.models.cards]] for the deferred pipeline design).

`export_from_cards()` reads `card.get("user_feedback", "")` off the parsed card dict and writes it into the fields dict alongside Front/Back or Text/Back Extra. `_build_database()` now assembles a three-element `field_values` list per note (`\x1f`-joined), defaulting the third element to empty.

Model IDs are still derived from `BASIC_MODEL_SEED = "swanki-basic-v1"` and `CLOZE_MODEL_SEED = "swanki-cloze-v1"` — keeping seeds stable means the new exports re-use the same model ids that existing collections already carry, so once `scripts/anki_add_feedback_field.py` retrofits the field via `modelFieldAdd`, future imports drop in cleanly. Bumping the seeds would have orphaned scheduling history — explicitly avoided.

Tests covering the change: `test_basic_model_has_feedback_field`, `test_cloze_model_has_feedback_field`, `test_feedback_value_round_trips_into_flds`, `test_feedback_defaults_empty_when_absent`, `test_feedback_round_trips_through_markdown_file` in [[tests.test_apkg_exporter]].

## 2026.05.29 - Feedback field at ord 2 finalized in both genanki models

WIP checkpoint for the .apkg side of the review-time triage channel. `ApkgExporter` reads `card.get("user_feedback", "")`, adds `Feedback` to the per-card fields dict (alongside Front/Back or Text/Back Extra), and appends it as the 3rd `\x1f`-joined value (ord 2) in the genanki `flds` for both the Basic and Cloze models. Both model definitions (`_basic_model_json`, `_cloze_model_json`) register a `Feedback` field at ord 2; templates are untouched so cards render identically. Field names land as `[Front, Back, Feedback]` and `[Text, Back Extra, Feedback]`. Model seeds stay stable so migrated collections (via [[scripts.anki_add_feedback_field]]) re-use the same model ids. Mirrors [[swanki.processing.anki_processor]] and [[swanki.models.cards]]; tests in [[tests.test_apkg_exporter]].

