---
id: v1u7g4yloox9zrk9jbe5vsv
title: '17'
desc: ''
updated: 1776884900886
created: 1776884900886
---

## 2026.04.22

- [x] Switched lecture length policy to an absolute word-count band (`clamp(src*0.30, 1500, 3900)` at ~130 wpm) and pinned the 30-min hard cap [[swanki.audio.lecture#20260422---word-count-budget-chunk-aware-refinement-duplicate-opener-guard]]
- [x] Made summary target a constant 500-700 words (~4-5 min) regardless of source length [[swanki.audio.summary#20260422---constant-4-5-minute-target-drop-source-scaled-cap]]
- [x] Added `_strip_duplicate_openers` post-refine guard plus a chunk-aware refinement prompt that forbids new intros/roadmaps/closings [[swanki.audio.lecture#20260422---word-count-budget-chunk-aware-refinement-duplicate-opener-guard]]
- [x] Re-TTS'd thornburg + zvyagin lectures from hand-cleaned transcripts to remove the duplicate-lecture defect before the code guard existed [[scripts.retts_cleaned_transcripts#20260422---re-tts-lecture-audio-from-a-hand-fixed-transcript-skipping-the-llm]]
- [x] Wrote `republish_fixed_lectures.sh` to orchestrate re-TTS → Zotero upload → ABS cleanup → abs_refresh as a single fix flow [[scripts.republish_fixed_lectures#20260422---orchestrate-the-duplicate-opener-fix-end-to-end]]
- [x] Wrote `publish_regen_to_abs.sh` as the Zotero-backed publish path for already-generated versioned audio [[scripts.publish_regen_to_abs#20260422---publish-already-generated-versioned-audio-via-the-zoteroabs-path]]
- [x] Added `abs_clean_stale_chapters.py` and wired it into `abs_refresh.sh` as step 5/6 so stale chapter JSON is cleared whenever a book's audioFiles no longer match its chapter titles [[scripts.abs_clean_stale_chapters#20260422---initial-version]] [[scripts.abs_refresh#20260422---added-stale-chapter-cleanup-as-step-56]]

## 2026.04.25

- [x] Fixed `swanki_abs_sync` so a republished paper's new mp3 evicts the prior `(key, audio_type)` file in the same dir, eliminating phantom ABS chapters from stacked timestamped versions [[scripts.swanki_abs_sync#20260425---replace-stale-per-paper-mp3s-on-republish]]
- [ ] Plan: solution-manual mode for problem-set PDFs (Schaum's, Bishop) — deterministic enumeration, problem-solution pairing, cross-chapter reference resolution, coverage audit, separate `<key>-problem-set.apkg` deck [[plan.solution-manual-mode-for-problem-set-pdfs.2026.04.25]]

## 2026.04.26

- [x] Inject `[short pause]` every third sentence inside continuous prose, switch chunk-end tag from `[long pause]` to `[pause]`, and add `chunk_tail_trim_ms` / `chunk_pause_ms` so Fish Speech lectures stop "blazing through" and chunk-boundary breath/sigh artifacts disappear [[swanki.audio._common#20260426---sentence-boundary-pacing-and-fish-speech-punctuationconcat-fixes]]
- [x] Fold Unicode em/en dashes, curly quotes, ellipsis, and NBSP to ASCII before sending text to Fish so its tokenizer no longer garbles or drops them [[swanki.audio._common#20260426---sentence-boundary-pacing-and-fish-speech-punctuationconcat-fixes]]
- [x] Wrap each lecture section's generation in a safety-refusal retry that prepends an explicit educational-context preamble, expand the critic's Fish-tag whitelist to a curated professorial vocabulary, and wire deterministic chunk gaps into the lecture combine path [[swanki.audio.lecture#20260426---safety-refusal-retry-fish-tag-whitelist-deterministic-chunk-gaps]]
- [x] Mirror the Fish-tag whitelist in `lecture_system` and add a faithfulness-to-source rule that forbids tangential public-health framing when the paper is a methods/compute paper (`swanki/conf/prompts/default.yaml`) [[swanki.audio.lecture#20260426---safety-refusal-retry-fish-tag-whitelist-deterministic-chunk-gaps]]
- [x] Refactor `latest_zip` into `latest_zips` so a single Zotero parent can carry one zip per chapter (group by name prefix, keep newest per group) and skip stale 404 attachments instead of aborting the whole projection [[scripts.swanki_abs_sync#20260426---per-chapter-zip-support-and-graceful-404-handling]]
- [x] Tests for `_normalize_fish_speech_punct` covering dash, quote/ellipsis, and ASCII-passthrough cases [[tests.test_audio_common#20260426---tests-for-fish-speech-unicode-punctuation-folding]]

## 2026.04.30

- [x] Apply Hamming-book boundary-fix bundle to lecture concatenation: chunk_pause 700 ms, section_pause 5 s, 50 ms crossfade, per-chunk gain match to -25 dBFS, silence-aware tail trim with 350 ms post-speech buffer [[swanki.audio.lecture#20260430---boundary-fix-bundle-and-first-person-book-voice-critic-patches]]
- [x] Replace blind tail trim with silence-aware trim, add `gain_match_target_dbfs` parameter, and let `chunk_pause_ms` + `chunk_crossfade_ms` stack so the inter-chunk silence and crossfade now compose instead of being mutually exclusive [[swanki.audio._common#20260430---silence-aware-trim-gain-match-and-crossfade-co-existence]]
- [x] Patch lecture critic + refiner to whitelist first-person speaker framings so the book-voice writer's author-voice phrasing survives the refine loop instead of being stripped as meta-commentary [[swanki.audio.lecture#20260430---boundary-fix-bundle-and-first-person-book-voice-critic-patches]]
- [x] Patch `abs_clean_stale_chapters` to accept prefix-match for human-readable chapter titles so cleaned slug titles survive cron cycles instead of being wiped on every refresh [[scripts.abs_clean_stale_chapters#20260430---allow-prefix-match-for-cleaned-chapter-titles]]
- [x] Bump page classifier from `gpt-5-nano` to `gpt-5.4-nano-2026-03-17` and the main LLM slot to `gpt-5.4-2026-03-05` across model configs [[swanki.utils.pdf_classifier#20260430---bump-page-classifier-model-to-gpt-54-nano]]
- [x] New `swanki.voice_clone` package with multi-clip-per-speaker layout for iterating on Fish Speech voice references without losing prior takes [[swanki.voice_clone.__init__#20260430---new-voice-clone-management-package]]
- [x] Pydantic schema and disk path helpers honoring `$SWANKI_MODELS` for the new voice-ref layout [[swanki.voice_clone.refs#20260430---schema--path-helpers-for-multi-clip-voice-references]]
- [x] DeepFilterNet wrapper for cleaning archival voice clips, with shims for torchaudio API removals so DFN runs on modern torch/torchaudio [[swanki.voice_clone.denoise#20260430---deepfilternet-wrapper-for-archival-voice-clone-references]]
- [x] CLI `clone_voice_from_youtube.py` for end-to-end YouTube voice cloning: yt-dlp clip extraction, denoise, register on Fish Speech, persist clip.json [[scripts.clone_voice_from_youtube#20260430---end-to-end-youtube-voice-cloning-cli]]

## 2026.05.14

- [x] Implemented Hamming lecture audio quality plan: tightened `chunk_text_paragraphs(max_chars=700)`, plumbed nested `models.tts.{preprocessor,chunking,postprocessor}` YAML through `swanki/pipeline/pipeline.py:1880-1925`, added deterministic TTS-prep scrubbers (forbidden-tag stripper, acronym letter-by-letter rewriter, pronunciation overrides, slug stripper) + n-gram repeated-phrase detector wired into the refine loop, extended `LectureTranscriptFeedback` with `bridge_quality` / `repeated_phrases` + a `@model_validator` that auto-flips `done`, added INTER-SECTION BRIDGES + INTRA-PASSAGE CONNECTIVES + SOURCE-TEXT CHRONOLOGY rules to `default.yaml` and `book_voice.yaml`, humanized chapter-slug bookend intros via new `humanize_chapter_slug`, fixed two stale `[long pause]` test assertions, and added 24+9 new unit tests across `tests/test_audio_common.py`, `tests/test_audio_lecture.py`, and the new `tests/test_utils_formatting.py` [[plan.hamming-lecture-audio-quality-fixes.2026.05.14]]
- [x] Added `scripts/abs_set_chapter_titles.py` to deterministically set ABS chapter titles to the canonical `<content_key>` form (e.g. `hammingArtDoingScience2020_03_history-of-computers-hardware`) after every refresh, eliminating the "Chapter 1"/"Chapter 2" UI fallback that ABS auto-numbers when chapters JSON is empty. Wired into `scripts/abs_refresh.sh` as step 6/7 between `abs_clean_stale_chapters` and the library scan; idempotent so re-renders don't churn titles. Backfilled the entire library on this run [[scripts.abs_set_chapter_titles#20260514---initial-deterministic-chapter-titles-after-every-refresh]] [[scripts.abs_refresh#20260514---add-abs_set_chapter_titles-as-step-67]]

- [x] Fixed Fish-Speech chunk-boundary stutter: `append_chunk_pause` for fish_speech now STRIPS trailing/leading `[pause]`/`[short pause]`/`[long pause]` tokens (via new `strip_chunk_boundary_pause_tags` helper) instead of appending one. Inter-chunk silence is supplied entirely by `combine_audio_with_section_pauses(chunk_pause_ms=700)`; the previous trailing tokens caused Fish to render the tag THEN play the silence, producing audible double-beat stutter at every chunk boundary. Mid-chunk pause tags (for complex-sentence comprehension breaks / dramatic effect) are preserved. ElevenLabs branch unchanged. Updated 2 tests + added 4 new ones [[swanki.audio._common#20260514---strip-chunk-boundary-pause-tags-instead-of-appending-one-fish-stutter-fix]]

- [x] Mirrored Hamming-PR audio fixes (chunker max_chars, pre-TTS scrubber pipeline, postprocessor knobs for gain match / inter-chunk silence / tail trim / crossfade) into `swanki/audio/summary.py` + `swanki/audio/reading.py`. Added `_preprocess_for_tts` helper in `swanki/audio/card.py` and wrapped all 5 `text_to_speech` text args so card audio also gets slug-strip + acronym letter-by-letter + pronunciation overrides + forbidden-tag scrub. All four audio types (lecture, summary, reading, card) now share the same Fish-Speech preprocessing + postprocessing baseline; defaults preserve elevenlabs behavior [[swanki.audio.summary#20260514---mirror-lecturepy-audio-fixes-for-consistency-across-types]] [[swanki.audio.reading#20260514---mirror-lecturepy-audio-fixes-for-consistency-across-types]] [[swanki.audio.card#20260514---add-_preprocess_for_tts-helper-and-wire-into-all-5-text_to_speech-sites]]
