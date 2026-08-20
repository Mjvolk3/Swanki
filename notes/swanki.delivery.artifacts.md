---
id: y5xkew19psckx3cbn44a2y7
title: Artifacts
desc: ''
updated: 1785208677586
created: 1785208677586
---

## 2026.08.20 - `zips_by_prefix`: newest-per-prefix is not enough for audio

`latest_zips` answers "the current artifact per chapter", which is right for
the Anki target (the newest `.apkg` IS the current deck) and wrong for the ABS
audio sync. A cards-only re-run -- correctness gate, no TTS -- emits a zip
holding just the `.apkg`, and being newest it outranks the older bundle that
carries the mp3s, so the audio silently disappears for any consumer building
from scratch. See [[swanki.abs.sync]] for the failure it caused on `mv-rp`.

`zips_by_prefix` returns **every** zip per prefix, newest timestamp first, and
leaves the stopping rule to the caller. `latest_zips` is unchanged and still
what the Anki path uses -- the two questions are genuinely different, so this
adds a function rather than changing the existing one.
