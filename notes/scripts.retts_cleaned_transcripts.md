---
id: vluui7fdqox6n9427ilkfrj
title: Retts_cleaned_transcripts
desc: ''
updated: 1776884689459
created: 1776884689459
---

## 2026.04.22 - Re-TTS lecture audio from a hand-fixed transcript, skipping the LLM

One-off fix path for when an existing lecture transcript is structurally correct but the audio is wrong (or when the transcript itself was manually edited to remove a defect and we just want the MP3 regenerated without re-running the expensive LLM generation + critique + refine loop).

- Reads a `*_fixed_transcript.md` produced by hand from the corresponding `*_transcript.md`.
- Strips the `**Generated Transcript:**` frontmatter marker so only the spoken content reaches TTS.
- Runs the same pipeline tail as `generate_lecture_audio`: `clean_markdown_for_tts` → `add_tts_pauses` → `split_transcript_by_sections` → `chunk_text_paragraphs` → `tts_chunks_parallel` → `combine_audio_with_section_pauses` with bookends.
- Writes the audio to the canonical `{prefix}-lecture-audio.mp3` path so downstream `sync_to_zotero` finds it via its glob pattern.
- Also writes the `_transcript.md` and `_transcript_cleaned_markdown.md` companion files that the main pipeline normally produces, so the lecture-transcript directory looks like a fresh run.

Created for the 2026-04-22 duplicate-opener fix on thornburg (3111w) and zvyagin (3757w) where the refine loop had regenerated a second full lecture spliced onto the first. The code-side guard (`_strip_duplicate_openers` in `swanki.audio.lecture`) now prevents this going forward; this script remains useful for any future transcript-edited-then-rerender case.