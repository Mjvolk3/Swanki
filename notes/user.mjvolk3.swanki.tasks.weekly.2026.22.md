---
id: swk22wk5planservsync27a
title: '22'
desc: ''
updated: 1779864732867
created: 1779864732867
---

## 2026.05.27

- [ ] Add `bash scripts/swanki_sync.sh` shorthand that pushes latest .apkg per Zotero item via AnkiConnect and runs `abs_refresh.sh` for audio, gated by per-projection `push_audio` / `push_anki` toggles in `infra/abs/projections.yml` [[plan.swanki-servers-sync-shortcut.2026.05.27]]

## 2026.05.29

- [x] Add an Anki `Feedback` field round-tripped via `<!-- user-feedback: -->` markdown markers for review-time triage, with a one-shot AnkiConnect migration for existing collections [[swanki.processing.apkg_exporter]]
- [x] Add solution-manual Stage 3 LLM content-pairing for Bishop-style separate-manual PDFs (statement/solution region split + content-match agent) [[swanki.pipeline.problem_set]]
- [ ] Add a pipeline-wide `verbalize_bit_strings` TTS scrubber so binary codewords read digit-by-digit (not as cardinals), then run the Hamming ch1-10 annotation review (ch1-9 surgical, ch10 full regen) [[plan.bit-string-verbalizer-hamming-annotations.2026.05.29]]

## 2026.05.30

- [x] Fix mid-sentence page-seam pauses: `join_pages` glues pages that end without sentence-terminal punctuation instead of letting `add_tts_pauses` drop a `[pause]` mid-sentence (resolves the Hamming Ch1 p4→p5 orange ABS comment; 4 of 8 Ch1 pages were affected) [[swanki.pipeline.section_classifier]]
- [x] Built swanki-native `comment_edit.py` (`edit_chunk` + `chunk_edit_agent` + extracted `preprocess_for_tts` + `_edits/` audit trail) so reviewer comments drive precise chunk re-TTS through the preprocessor; audio-fix skill now calls it [[plan.swanki-comment-driven-chunk-edits.2026.05.30]]
- [x] Shipped `bash scripts/swanki_sync.sh` shorthand — runs `abs_refresh.sh` for audio and POSTs `importPackage` + final `sync` to AnkiConnect for the newest .apkg per fox-tagged Zotero item; both halves gated by per-projection `push_audio` / `push_anki` (default True) and share a new `_latest_artifact` helper [[plan.swanki-servers-sync-shortcut.2026.05.27]]
- [x] Split the single bookend pause into asymmetric `bookend_start/end/trailing_pause_ms` global knobs (fast front, ~2s break + trailing silence; persisted to manifest on restitch) and refined the book_voice lecture prompt for a stronger post-example conceptual takeaway [[plan.audio-bookend-pauses-conceptual-prompt.2026.05.30]]
