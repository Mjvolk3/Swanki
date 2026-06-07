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

- [x] Shipped the configurable delivery subsystem `swanki/delivery/` (SyncSource local|zotero crossed with SyncTarget zotero/anki/abs, Hydra `delivery` group), a hardened Zotero client (lifted pyzotero per-call read timeout + 5xx/timeout retry with 404-skip), and a queue rework where DONE means delivered Zotero->Anki->ABS with per-target `.delivery.json` markers, per-item Anki push, and an ABS refresh debounced once at drain-end. [[plan.delivery-subsystem-source-target-sync.2026.06.04]]

## 2026.06.05

- [x] Fixed reasoning-model token-exhaustion crashes: bumped image-summary `max_tokens` 1024->8000 (hard crash at `process_images` on Kuchel CH05) and table-summary 256->4000 defensively, since `gpt-5.5` reasoning tokens count against `max_tokens` and exhaust tiny budgets before any visible output (commit 2b40e42) [[swanki.processing.image_processor]]
- [x] Re-applied the Zotero sync-log pagination fix on current main: `_find_or_create_sync_note` now lookups via `zot.everything(zot.children(parent_key))` so an existing "Swanki Sync Log" note that fell off page 1 is found instead of duplicated (was 85 dupes on one item); `#34`'s client refactor had made the original PR #25 conflict and left the bug live, so #25 closed as superseded; added `tests/test_zotero_sync_note.py` regression [[swanki.sync.zotero]]
- [x] Documented the six precise ch1-3 Hamming lecture edits (World War Two x2, two prosody re-rolls, the "physically" skip, the Socrates ending) applied via `edit_chunk` and published to ABS as `20260602T1434-ef69683`, plus the verbalizer Roman-numeral root-cause fix (PR #31, `2c6392d`); ch1-3 ABS bookmarks now need clear+re-mark [[swanki.audio.hamming-comments-runbook.2026.05.29]]

## 2026.06.06

- [x] Shipped smarter lecture TTS chunking: `chunk_text_paragraphs` gains a fish-opt-in balanced path (`soft_max_chars`/`min_sentences_per_chunk`) that even-splits over-soft paragraphs and merges lone single-sentence chunks, plus a config-gated per-chunk onset fade in `_load`; non-fish stays byte-identical and shipped-code A/B over Hamming CH01-10 hits mean 515->423 / stdev 146->95 / single-sentence 13->1 (CH04 5->0) [[plan.smarter-lecture-tts-chunking.2026.06.06]]
- [ ] Migrate generation onto SLURM with serverless per-job Fish: each paper = one `sbatch --gres=gpu:1` job that brings up apptainer Fish on its allocated GPU, runs OCR+cards+TTS pinned to that one GPU, delivers Zotero->Anki->ABS at end-of-job then tears Fish down; `swanki_enqueue.sh` becomes a thin sbatch-renderer with `--dependency` chaining (linear/parallel via QOS `GrpTRES`); core fixes (`mineru.py` ambient `CUDA_VISIBLE_DEVICES`, `_common.py` single Fish port) ship now, the live cutover is a user-run runbook [[plan.slurm-native-serverless-fish.2026.06.06]]
- [x] Shipped the binary-codeword TTS scope fix (PR #39, merged): trimmed the self-contradictory `10` example from the BINARY CODEWORDS rule at all four prompt sites, added the scoped rule to book_voice.yaml + summary.py (which had none), demoted `verbalize_bit_strings` to per-paper opt-in (default-off across the four call sites + fish_speech.yaml mirror), and added a CH10 opt-in regression fixture + prompt-example guard; 135 tests pass and a CH10 raw-vs-scrubbed diff confirmed the LLM already emits word-form codewords so default-off has zero CH10 regression [[plan.scope-binary-codeword-tts.2026.06.06]]

## 2026.06.07

- [x] Fixed the SLURM serverless-Fish reference-port bug (PR #38 regression): `ensure_fish_speech_reference` now resolves `server_url` through `_discover_fish_speech_servers` so the `/v1/references/*` calls honor the per-job `SWANKI_FISH_PORTS` dynamic port instead of dialing 8080 and getting connection-refused before any TTS; local 8080 runs unchanged. Validated by CH01 SLURM canary (job 851: COMPLETED, 27-chunk lecture). Per-job Fish runs uncompiled at ~3.6 tok/s (~1.3h/chapter); `SWANKI_FISH_COMPILE=1` under test for the fan-out [[swanki.audio._common]]
