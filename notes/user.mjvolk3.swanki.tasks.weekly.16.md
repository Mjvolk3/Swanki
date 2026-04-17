---
id: 3q5fy1xegyfyty5glti1765
title: '16'
desc: ''
updated: 1776290433298
created: 1776290419183
---
## 2026.04.15

- [x] Distribute Fish Speech audio across multiple GPU servers via round-robin discovery and a parallel chunk helper [[swanki.audio._common]]
- [x] Flatten lecture chunks into one job list and dispatch in parallel for Fish Speech [[swanki.audio.lecture]]
- [x] Flatten reading chunks into one job list and dispatch in parallel for Fish Speech [[swanki.audio.reading]]
- [x] Flatten summary chunks into one job list and dispatch in parallel for Fish Speech [[swanki.audio.summary]]
- [x] Add content_key to the pipeline and parallelize card audio across Fish Speech servers [[swanki.pipeline.pipeline]]
- [x] Bundle Zotero uploads into a single zip per run and harden item lookup plus upload timeouts [[swanki.sync.zotero]]
- [x] Forward content_key from the CLI into the pipeline [[swanki.__main__]]

## 2026.04.16

- [x] Replace 200ms chunk crossfade with direct concat and add `append_chunk_pause`, `write_chunk_manifest`, and `restitch_from_chunks` helpers [[swanki.audio._common]]
- [x] Retain lecture chunks under `lecture_chunks/` with manifest for surgical re-TTS [[swanki.audio.lecture]]
- [x] Retain reading chunks under `reading_chunks/` with manifest for surgical re-TTS [[swanki.audio.reading]]
- [x] Retain summary chunks under `summary_chunks/` with manifest for surgical re-TTS [[swanki.audio.summary]]
- [x] Retain card chunks under `card_chunks/` with per-card manifest to avoid parallel-write races [[swanki.audio.card]]
- [x] Re-export `restitch_from_chunks` from the audio package so callers can rebuild from a manifest [[swanki.audio.__init__]]
