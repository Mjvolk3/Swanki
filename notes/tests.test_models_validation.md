---
id: pot4qumfvclwjw4rqo229km
title: Test_models_validation
desc: ''
updated: 1780075592768
created: 1780075592768
---

## 2026.05.29 - PlainCard.user_feedback round-trip coverage

New `TestPlainCardUserFeedback` class locks the data plumbing for the Anki review-time triage channel (see [[swanki.models.cards]]). Intent: prove the marker is invisible by default and never bleeds into card content, so the field can ship silently.

- `test_default_is_empty_string` — `user_feedback` defaults to `""`.
- `test_to_md_omits_marker_when_empty` — no `<!-- user-feedback:` marker emitted when the field is empty.
- `test_to_md_emits_marker_when_set` — marker is emitted and ordered BEFORE the tag line (asserts `marker_idx < tag_idx`).
- `test_extract_cards_round_trip` — drives `to_md()` -> [[swanki.processing.anki_processor]] `extract_cards()`, asserts `user_feedback` survives and the marker is stripped from both front and back content.

