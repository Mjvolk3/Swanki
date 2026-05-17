---
id: 1utzpk0ve4ilan4yiko9hi1
title: Fix_hamming_ch1_reading
desc: ''
updated: 1779043932231
created: 1779043932231
---

## 2026.05.17 - Track-B surgical repair of live Hamming Ch1 reading

Applies hand-corrected text to the 5 annotation-flagged chunks of the live
Ch1 reading manifest and restitches, leaving the other 53 chunk mp3s
byte-identical. Driven by the 6 orange Zotero annotations
([[plan.hamming-chapter-1-audio-two-track-fixes.2026.05.17]]):

- RC1 chunk0, chunk31: strip the spoken `---SECTION_B-R-E-A-K---` leak
  (the marker the acronym pass mangled before the splitter could remove
  it).
- RC2 chunk31: reinstate the page 4->5 bridge clause Pass-2 silently
  dropped ("they arise so you will not be left behind ... In the position
  I found myself in at the Laboratories ..."), verbatim from
  `clean-md-singles/page-5.md`.
- RC3 chunk37: add a trailing `[short pause]` so the "past was once the
  future" aphorism lands instead of being swallowed by the chunk join.
- RC4 chunk53, chunk54: re-render the computers-vs-humans advantages table
  reading each row across (label then description as one clause) with a
  light inter-row `[short pause]`, replacing the fragmented per-cell
  `[pause]` cadence; all ten rows retained.

Uses the cloned Hamming voice (`hamming-20260428T1135-science-vs-
engineering`) -- patched chunks must match the untouched ones. Fish
pre-flight aborts before any re-TTS if the server is down. Pairs with the
Zotero re-zip / fox tag + `abs_refresh.sh` republish so BookPlayer serves
the corrected audio.
