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