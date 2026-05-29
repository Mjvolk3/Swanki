---
id: 13c0ujody47vxnxyll1mrwi
title: Anki_add_feedback_field
desc: ''
updated: 1780075599621
created: 1780075599621
---

## 2026.05.29 - One-shot migration to add the Feedback field to live note types

One-shot, idempotent migration that adds the `Feedback` field (ord 2, after Front/Back or Text/Back Extra) to the existing Swanki Basic and Cloze note types in a running Anki collection, via AnkiConnect (`modelFieldAdd`, default `127.0.0.1:8765`). Intent: align collections populated BEFORE the field existed with the new schema so newer `.apkg` imports — which now carry a third field — drop in cleanly instead of fighting a two-field model. Without it, importing on top of the old model is brittle.

- Idempotent: checks `modelFieldNames` first; reports `added` / `already_present` / `missing_model` per model and exits non-zero only when a requested model is absent.
- Run on the laptop — gilahyper has no Anki client (the `anki=default` rule).
- Pairs with the model-side change in [[swanki.processing.apkg_exporter]] and the round-trip plumbing in [[swanki.models.cards]] / [[swanki.processing.anki_processor]]. Model IDs are unchanged, so retrofitted collections keep their scheduling history.

