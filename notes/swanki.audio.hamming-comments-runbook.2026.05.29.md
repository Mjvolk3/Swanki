---
id: hamming-comments-runbook-20260529
title: Hamming Comment Runbook (Round 2, 2026-05-29)
desc: 13 ABS Lecture bookmarks (2026-05-24..26) against the 2026-05-19 audio, triaged
updated: 1780000000000
created: 1780000000000
---

# Hamming ABS comments — Round 2 (2026-05-24 to 05-26)

Snapshot of the 13 live ABS bookmarks on the Hamming **Lecture** item
(`3d4a9ce9-a8d4-4a3d-ad48-a911672408a5`), left while listening to the
2026-05-19 audio. Round 1 (45 bookmarks, Apr 27 - May 20) was addressed by the
05-19 regen and archived in [[swanki.audio.hamming-bookmarks-archive.2026.05.21]].
Bookmark `time` lags the issue by minutes; chapter mapped via lecture-concat
boundaries (ch3@21.0m, ch4@34.3m, ch5@53.9m, ch6@65.6m, ch7@76.0m, ch9@103.6m,
ch10@115.1m). Plan: [[plan.bit-string-verbalizer-hamming-annotations.2026.05.29]].

**Decision: ch10 = full audio regen; everything else = surgical / config.**

| time | ch | comment | disposition |
|---|---|---|---|
| 29.1m | 03 | "How is light a human dimension? probably regenerate from text to audio" | surgical — transcript edit + re-TTS |
| 53.6m | 04→05 | larger pause after "this concludes the lecture" bookend, across all lectures | bookend pause config (all lectures) + re-stitch |
| 62.7m | 05 | Jack Kane anecdotes split across the lecture, disorganized/wasteful | surgical — transcript edit (or accept if it mirrors source) |
| 65.6m | 06 | want ~2s gap on bookend back-end so autoplay sounds like a distinct break | bookend gap config + re-stitch |
| 75.9m | 06→07 | small gap before the bookend to make the ending clear | bookend gap config + re-stitch |
| 104.0m | 09 | "dimensional space" jammed together on first reading in the body | surgical — re-TTS (spacing) |
| 112.3m | 09 | theory-vs-practice first example needs a bit more depth | surgical — transcript edit + re-TTS |
| 118.7m | 10 | "the 111 sounds like it's repeated, confusing" | ch10 regen (verbalizer: 111 -> one-one-one) |
| 120.0m | 10 | "says zero but sounds like Jairo" | ch10 regen; add "zero" pronunciation override only if it persists |
| 125.2m | 10 | TTS spamming the word "100" nearly 100+ times | ch10 regen (verbalizer: 100 -> one-zero-zero) |
| 126.8m | 10 | "100 spamming finally stopped here" | ch10 regen (same fix) |
| 127.4m | 10 | "in the exact symbols I utter" ends as a question with up-tone | ch10 regen (prosody re-roll) |
| 128.0m | 10 | overall: some examples confusing; want conceptual points after examples stronger | ch10 regen (transcript critic/refine pass) |

## Execution status (2026-05-29)

- [x] Verbalizer merged to `main` (PR #18, merge `0b6c68b`).
- [ ] ch10 full audio regen (`mode=audio_only audio=all models=fish_speech_hamming`), verify codewords read digit-by-digit, publish to ABS.
- [ ] Bookend pause/gap config change + re-stitch all lecture chapters (53.6m / 65.6m / 75.9m).
- [ ] Surgical fixes: ch3 (29.1m), ch5 (62.7m), ch9 (104.0m, 112.3m).
- [ ] After all land + re-listen: clear + re-mark ABS bookmarks (do NOT clear before — ch3/5/9 comments are still the task list).

## 2026.05.30 - Bookend pauses + conceptual prompt landed (structural batch)

The bookend pause/gap cluster (53.6m, 65.6m, 75.9m) and the conceptual-strength
comment (128.0m) are addressed by code in
[[plan.audio-bookend-pauses-conceptual-prompt.2026.05.30]] (asymmetric
`bookend_start/end/trailing_pause_ms` global knobs + a book_voice lecture-prompt
refinement). Post-merge runbook to land them on ABS:

1. Re-stitch all 10 Hamming chapters with the new pauses (pure pydub, no Fish
   needed; `scripts/regen_hamming_bookends_ch1_10.py` now passes+persists
   300/2000/1500). This rewrites each chunk_timeline + persists the keys into
   each manifest.
2. Commit, then `sync_to_zotero` per chapter, then `bash scripts/abs_refresh.sh`.
3. Clear+re-mark ABS bookmarks (all chapter offsets shift). The ch1-9 comment
   task list above survives on content-match, not offsets.
4. The conceptual-prompt refinement only affects a FRESH lecture transcript
   regen (not a re-stitch); ch10 already regenerated 2026-05-29 before this
   prompt change, so a fresh ch10 lecture regen would be needed to pick it up
   (optional / judged by listening).

Then the precise per-chunk fixes (ch3 29.1m, ch9 104.0m/112.3m) via
[[swanki.audio.comment_edit]] `edit_chunk` -- each re-stitches its chapter and
inherits the persisted bookend pauses from the manifest.
