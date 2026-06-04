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

## 2026.05.31

- [x] Standardized table/figure audio landmarks: `markdown_cleaner` now emits deterministic `Figure:`/`Table:` landmarks (no number, full caption verbatim or a stashed placeholder), bracketed by real `---SECTION_BREAK---` silence; new `landmarks` helpers + `table_processor` + `TableSummary` model fill caption-less tables via a text LLM and caption-less figures from image summaries; table cells are never voiced (fixes the Hamming Ch1 numeric-grid leak); lecture `_embed_images` prose retired for consistency [[plan.reading-table-figure-landmarks.2026.05.31]]
- [x] Built swanki-native `comment_edit.py` (`edit_chunk` + `chunk_edit_agent` + extracted `preprocess_for_tts` + `_edits/` audit trail) so reviewer comments drive precise chunk re-TTS through the preprocessor; audio-fix skill now calls it [[plan.swanki-comment-driven-chunk-edits.2026.05.30]]
- [x] Shipped `bash scripts/swanki_sync.sh` shorthand — runs `abs_refresh.sh` for audio and POSTs `importPackage` + final `sync` to AnkiConnect for the newest .apkg per fox-tagged Zotero item; both halves gated by per-projection `push_audio` / `push_anki` (default True) and share a new `_latest_artifact` helper [[plan.swanki-servers-sync-shortcut.2026.05.27]]
- [x] Split the single bookend pause into asymmetric `bookend_start/end/trailing_pause_ms` global knobs (fast front, ~2s break + trailing silence; persisted to manifest on restitch) and refined the book_voice lecture prompt for a stronger post-example conceptual takeaway [[plan.audio-bookend-pauses-conceptual-prompt.2026.05.30]]

## 2026.06.01

- [x] Shipped the post-card-creation LLM correctness gate (factual-only, high-acceptance, on by default; keep/fix/quarantine with per-card JSON audit + reasons) at the `generate_outputs` chokepoint; merged PR #24 [[plan.post-creation-llm-card-correctness-gate.2026.06.01]]
- [x] Fixed CI package break: declared `audioop-lts` so `pydub` imports on Python 3.13 (stdlib `audioop` removed by PEP 594) and installed `ffmpeg` on the test runner; suite now collects and runs (0 -> 484 items, 262 passing) instead of erroring at import; merged PR #26 [[PR #26]]
- [ ] Fix section-classifier back-matter false-positive: anchor `_BACK_MATTER`/`_FRONT_MATTER` cues to markdown headings (not `\b...\b` prose) + positional guard so back_matter only starts in the last ~20% of pages; keeps stickiness/answer-key pairing intact. Fixes Hamming ch04 (was dropping 6 of 9 pages as back_matter on "index registers" -> 4 cards) then re-gens ch04 [[plan.section-classifier-back-matter-positional-guard.2026.06.01]]
- [ ] Built a fire-and-forget serial generation queue (`scripts/swanki_enqueue.sh` + `scripts/swanki_queue.sh` + `swanki-queue.service` systemd --user unit): drop many sources, drains one at a time so the single Fish server is never oversubscribed; concurrency + executor (local/noop/slurm-stub) knobs key off Fish capacity for the dual-purpose future [[scripts.swanki_queue]]
- [ ] Fix verbalizer misreading Roman numerals: `expand_acronyms_for_tts` letter-spelled `II`->`I-I` (Fish "one one") like an acronym; map unambiguous uppercase Roman numerals (II, III, VII…XX) to their cardinal word, excluding IV/VI (intravenous / vi-editor collisions → no regression). Fixes "World War II/III", "Part VII", etc. pipeline-wide [[plan.verbalizer-roman-numeral-guard.2026.06.02]]
- [x] Made Completion fill-in-the-blank cards' blank larger via a tunable `_COMPLETION_BLANK` constant (4 -> 8 underscores) in `problem_set.py` + matching prompt examples [[swanki.pipeline.problem_set]]
- [ ] Make Schaum's solution-manual parsing OCR-agnostic (loosen 3 `^##`-hardcoded back-of-book regexes to `^#{1,3}` so MinerU `#` headers parse — fixes the CoverageError on all 5 Alcamo chapters), repeated-same-named-section-aware (list-valued partition + occurrence-indexed IDs), and page-spill-tolerant; plus move PDF chop+concat into `swanki/pdf_prep.py` (pure-Python pypdf) [[plan.solution-manual-robust-parsing-pdf-prep.2026.06.02]]

## 2026.06.04

- [ ] Build a configurable delivery subsystem (`swanki/delivery/`): SyncSource (`local`|`zotero`, default local) x SyncTarget (`anki`, `abs`, plus Zotero backup) driven by a Hydra `delivery` config group; rework queue DONE to mean delivered in order Zotero->Anki->ABS with per-target `.delivery.json` markers, per-item Anki push, and ABS refresh debounced once at drain-end; harden the flaky Zotero client (explicit httpx timeout + 5xx/timeout retry, lands first); existing sync scripts become thin shims [[plan.delivery-subsystem-source-target-sync.2026.06.04]]
