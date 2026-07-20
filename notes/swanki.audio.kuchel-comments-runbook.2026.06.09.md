---
id: s7ywviuh2s5s81w4xa405vr
title: 09
desc: ''
updated: 1781061062941
created: 1781061062941
---

## Kuchel CH01 lecture — precise number-reading edits (2026.06.09)

Source: ABS bookmarks on `kuchelSchaumOutlineBiochemistry2011` CH01 lecture (item
`7b7b2d9e`). Root cause: the pre-fix BINARY CODEWORDS prompt rule (the ambiguous `10`
example) made the lecture LLM write number ranges as digit-words in the prose itself —
NOT the regex scrubber (the stored chunk text had no bare `[01]` tokens). Fixed at the
pipeline level by PR #39; these surgical edits repair the already-rendered CH01 audio.

Dir: `kuchelSchaumOutlineBiochemistry2011_CH01_cell-ultrastructure_1/lecture_chunks`.
Applied via `edit_chunk(speech_only=True)` after a programmatic digit-swap on the stored
chunk text (verbatim re-TTS, no re-preprocess — `lecture.py` stores the exact TTS input,
so re-preprocessing would inject a spurious `[short pause]`). Speed auto-resolved to 1.0
via the new manifest/audio-type resolution (PR #43). Originals backed up to
`lecture_chunks/_pre_number_fix_backup.json`.

| Chunk | Bookmark | Fix                                                                                      |
|-------|----------|------------------------------------------------------------------------------------------|
| 1     | 1:08     | "one-zero to one-zero-zero micrometers" -> "10 to 100 micrometers"                       |
| 3     | (bonus)  | "one-zero to 15 percent" -> "10 to 15 percent"                                           |
| 22    | 13:39    | "one-zero percent" -> "10 percent"                                                       |
| 11    | 6:53     | speech-only re-roll (Fish said "zero" as "deero" reading 0.004) — stochastic, spot-check |

Published Zotero (source of truth) -> ABS via `sync_to_zotero` + `swanki.abs.targeted_refresh`.
ABS chunk times shifted, so CH01 bookmarks need clear + re-mark. See
[[swanki.audio.comment_edit]], [[plan.scope-binary-codeword-tts.2026.06.06]].

## Kuchel CH05 reading — number-verbalization fix (2026.06.10)

Scan of CH05 found the lecture and summary tracks CLEAN; the **reading** track had
**34 number-verbalization artifacts across 26 chunks** (same pre-PR#39 root cause, but
the reading rule's "10" example mangled this section's dense scientific notation,
figure/chapter refs, and data tables). All 34 were mis-verbalized numbers (no genuine
codewords — biochemistry), each a deterministic digit-word -> numeral swap:
`one-zero`->`10`, `one-one`->`11`, `one-zero-zero`->`100`, `one-one-zero`->`110`,
`one-zero-zero-zero`->`1000`. Examples: "around 10 to the 3 to 10 to the 12" (10^3-10^12),
"Fig. 5-11", "Chap. 11"/"Chap. 10", "L equals 1000", "2.0; 100" (table cell).

Dir: `kuchelSchaumOutlineBiochemistry2011_CH05_regulation-of-reaction-rates-enzymes_0/reading_chunks`.
One restitch of the 310-chunk reading manifest is ~122s, so 26 per-chunk `edit_chunk`
calls would be ~53 min of restitch waste; applied as a **batch** (`/tmp/ch05_numfix.py`)
that mirrors `edit_chunk`'s verbatim `speech_only` path (archive baseline + `_edits`
audit) but lifts restitch out of the loop: digit-swap the stored chunk text, verbatim
re-TTS each affected chunk (no re-preprocess), then a SINGLE `restitch_from_chunks`.
Speed auto-resolved to **1.2** (reading) via the manifest/audio-type fallback (PR #43).
Verified: 0 verbalized tokens remain; output mp3 + `chunk_timeline.json` regenerated.

Affected chunks (fix count): 2(2), 4, 9, 10, 48, 52, 53, 54(2), 56, 59(3), 62, 69, 140,
184, 189(2), 202, 203, 231, 240, 244, 250, 280(4), 281, 285, 298, 307.

Published Zotero -> ABS same as CH01. ABS chunk times shifted, so CH05 bookmarks need
clear + re-mark.

## Kuchel CH03 reading + lecture — number-verbalization fix (2026.07.20)

Same pre-PR#39 root cause found in **CH03** (`building-blocks-of-life`), which had
NEVER been remediated: audio rendered 2026-06-04, two days before PR#39 (3893cc9)
demoted `verbalize_bit_strings` to opt-in and de-fanged the "10" prompt example.
Scan: summary CLEAN; **reading 30 artifacts / 23 chunks**, **lecture 2 / 2 chunks**.
Four ABS bookmarks on the parent item (`7b7b2d9e`) flagged it: 1:08, 6:53 ("deero"
= Fish saying "zero" oddly, stochastic — not a number bug), 13:39, and 55:52 ("100
Dolphins red as binary").

Fix mirrors CH05: deterministic digit-word -> numeral swap on stored chunk text,
verbatim `speech_only` re-TTS per affected chunk (no re-preprocess), then ONE
`restitch_from_chunks` per track. Guard regex fixed vs CH05's: hyphen neighbours
are IN scope (`Fig. 3-one-zero` -> `Fig. 3-10`, `one-zero-methyl` -> `10-methyl`),
only letter-abutting runs rejected. Ran serverless on SLURM (job 972,
`--dependency=afterany:971`) to avoid the epilog cross-kill of the live pipeline's
Fish. Verified: 0 verbalized runs remain across all three tracks; baselines in
`{reading,lecture}_chunks/_edits/`. Speed auto-resolved 1.2 reading / 1.0 lecture.

Reading chunks fixed: 2(2), 3, 35, 37, 60, 62(2), 65, 79, 80, 93(2), 147, 157,
159, 160, 186, 215, 222, 260, 277, 278(4), 284, 297(2). Lecture: 1, 40.

Delivery (2026.07.20): commit -> `sync_to_zotero` (prunes prior attachments, re-tag
🦊) -> stamp local mp3s -> `swanki.abs.refresh.targeted_refresh` (windowed-wipes
stale ABS file). ALL four Kuchel ABS bookmarks cleared whole-item via
`scripts/abs_clear_bookmarks.py` (this also swept the stale CH01 bookmarks that
were never cleared after the 2026-06-09 fix).
