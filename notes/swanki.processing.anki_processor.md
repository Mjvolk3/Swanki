---
id: qytur9zpslhrjz64krmav08
title: Anki Processor
desc: ''
updated: 1773013975831
created: 1773013975831
---

## 2026.03.08 - Extract card-processing functions to module level

Lift card parsing, formatting, and extraction logic out of `AnkiProcessor` methods into standalone module-level functions (`parse_tags`, `split_front_back`, `extract_cards`, `format_card_html`, `format_cloze_html`, etc.). This enables `ApkgExporter` to reuse the same parsing and HTML formatting without depending on AnkiConnect. The `AnkiProcessor` methods now delegate to these functions, preserving backward compatibility.

## 2026.03.12 - Type annotation modernization and ruff formatting

Replaced `typing` generics (`List`, `Dict`, `Tuple`, `Set`, `Optional`) with Python 3.10+ builtins (`list`, `dict`, `tuple`, `set`, `X | None`). Removed unused `json` import. Applied ruff formatting: double quotes, Google-style docstring headers (`Returns:` instead of `Returns`), line wrapping.

## 2026.05.19 - user-feedback marker extraction + Feedback field on AnkiConnect notes

`extract_cards()` now strips a single-line `<!-- user-feedback: TEXT -->` marker out of every card body before any other parsing and surfaces the captured text as the `user_feedback` key on the returned dict (empty string when absent). Done with a precompiled `USER_FEEDBACK_RE`, in a pre-pass before tag stripping, because the tag-strip loop only pops trailing `#`/`- #`/blank lines and would otherwise stop at the comment. The marker matches the format emitted by [[swanki.models.cards]] `PlainCard.to_md()`.

`AnkiProcessor.send_cards_from_file()` reads `card.get("user_feedback", "")` and passes it through to AnkiConnect's `addNote` as a third field — `Feedback` — on both Basic and Cloze model notes. Existing collections need `scripts/anki_add_feedback_field.py` run once first, or AnkiConnect rejects the addNote with an unknown-field error.

Why a comment marker and not an extra `%` block: the existing two-block `%` separator splits front from back. Adding a third block would have meant a more invasive parser change and a less-readable source markdown. HTML comments are inert in Markdown→HTML conversion AND we strip them at extract time, so they never reach `prepare_for_anki` content paths. Round-trip is trivial regex on one line.

## 2026.05.29 - Feedback-field plumbing finalized as WIP

WIP checkpoint for the marker plumbing above. `extract_cards` strips the `USER_FEEDBACK_RE` line in a pre-pass and surfaces `user_feedback` (empty when absent) on the dict; `AnkiProcessor` writes it to the `Feedback` field on both Cloze (`{Text, Back Extra, Feedback}`) and Basic (`{Front, Back, Feedback}`). Mirrors the .apkg path in [[swanki.processing.apkg_exporter]] and the emitter in [[swanki.models.cards]]. Pre-existing collections must run [[scripts.anki_add_feedback_field]] once (`modelFieldAdd` at ord 2) or AnkiConnect rejects the unknown field; round-trip covered in [[tests.test_models_validation]].
