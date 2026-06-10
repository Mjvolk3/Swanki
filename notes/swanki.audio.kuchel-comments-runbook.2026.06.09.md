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

| Chunk | Bookmark | Fix |
| --- | --- | --- |
| 1  | 1:08  | "one-zero to one-zero-zero micrometers" -> "10 to 100 micrometers" |
| 3  | (bonus) | "one-zero to 15 percent" -> "10 to 15 percent" |
| 22 | 13:39 | "one-zero percent" -> "10 percent" |
| 11 | 6:53  | speech-only re-roll (Fish said "zero" as "deero" reading 0.004) — stochastic, spot-check |

Published Zotero (source of truth) -> ABS via `sync_to_zotero` + `swanki.abs.targeted_refresh`.
ABS chunk times shifted, so CH01 bookmarks need clear + re-mark. See
[[swanki.audio.comment_edit]], [[plan.scope-binary-codeword-tts.2026.06.06]].
