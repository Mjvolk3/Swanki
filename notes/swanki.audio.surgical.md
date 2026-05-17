---
id: cjm6hohfkys8uk61mlv9ys7
title: Surgical
desc: ''
updated: 1779043919197
created: 1779043919197
---

## 2026.05.17 - Reusable surgical single-chunk re-TTS + restitch

Generalizes the one-off `scripts/regen_campagne_lecture_chunks.py` pattern
into a reusable, importable helper so any future audio-quality fix can be
applied to existing renders without a full pipeline regeneration. Built to
service the Hamming Ch1 two-track plan
[[plan.hamming-chapter-1-audio-two-track-fixes.2026.05.17]] but deliberately
paper-agnostic.

`regenerate_and_restitch(manifest_path, chunk_edits, *, audio_type=None,
output_path=None, speed=1.1, tts_kwargs=None, section_pause_ms=None)`:

- `chunk_edits` maps a chunk `index` to replacement text, or to `None` to
  re-render the chunk's existing manifest text unchanged. The first form is
  for content fixes (hand-corrected text); the second for upstream
  code-level fixes where re-rendering the same text now yields correct
  audio.
- A non-None edit is persisted back into `manifest["chunks"][i]["text"]`
  and the manifest is rewritten, so the recorded transcript stays truthful
  and a later restitch stays correct. `restitch_from_chunks` concatenates
  chunk *files* (not text), so the audio change comes from re-TTS writing
  the chunk mp3; the manifest text is the record.
- Fails loud (CLAUDE.md fast-fail) on: wrong `audio_type` (indices are
  local per audio type -- a lecture vs reading mix-up is a silent
  data-corruption risk), a missing `postprocessor` block (restitch could
  not reproduce the original silence/gain), or an unknown chunk index.

`fish_speech_healthy(server_url)` is a cheap HTTP pre-flight; Fish has no
retry and a single failed chunk aborts a batch, so callers probe before any
re-TTS. Exported from `swanki.audio` for ergonomic import.
