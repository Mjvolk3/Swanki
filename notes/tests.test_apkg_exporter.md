---
id: 07ho156bt386mlc8geyn2zo
title: Test_apkg_exporter
desc: ''
updated: 1773333558047
created: 1773333558047
---

## 2026.03.12 - Remove unused imports and fix docstrings

Removed unused `os` and private helper imports (`_guid`, `_stable_id`). Fixed raw string docstrings for escape sequences. Capitalized docstring first words per convention.

## 2026.05.29 - Feedback-field export coverage

Tests locking the `Feedback` field on exported .apkg models (see [[swanki.processing.apkg_exporter]]). Intent: prove the field exists at ord 2 on both models and that supplied feedback survives into the genanki note row, so the review-time triage channel is durable across export.

- `test_basic_model_has_feedback_field` — Basic model `flds` names are `[Front, Back, Feedback]` with `Feedback` at ord 2.
- `test_cloze_model_has_feedback_field` — Cloze model `flds` names are `[Text, Back Extra, Feedback]`.
- `test_feedback_value_round_trips_into_flds` — a supplied `user_feedback` lands as the 3rd `\x1f`-separated fld value.
- `test_feedback_defaults_empty_when_absent` — cards without `user_feedback` still get an empty 3rd field, not a missing one.
- `test_feedback_round_trips_through_markdown_file` — full `to_md` marker -> `extract_cards` -> apkg path keeps the text intact.
