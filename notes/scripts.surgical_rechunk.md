---
id: mf0kkpjm1hjdig7w5kvodnu
title: Surgical_rechunk
desc: ''
updated: 1779043925716
created: 1779043925716
---

## 2026.05.17 - Thin CLI over the surgical helper

Generic command-line front end to
[[swanki.audio.surgical]] `regenerate_and_restitch`. Re-TTS the named chunk
indices using their EXISTING manifest text, then restitch -- the reusable
case after an upstream code fix (e.g. the RC1 sentinel mask) where
re-rendering the same text now produces correct audio. Every other chunk
file is reused untouched.

Args: `--manifest-path --audio-type --chunk-indices --reference-id
[--server-url --speed --temperature --section-pause-ms --output-path]`.
Fish Speech is health-checked first; a down server exits non-zero before
any partial work. For *content* edits (hand-corrected chunk text) callers
import `regenerate_and_restitch` directly with an explicit edits map
instead -- see [[scripts.fix_hamming_ch1_reading]].
