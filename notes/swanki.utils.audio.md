---
id: 2ma58ujmncg9t2nk07zjz0u
title: Audio
desc: ''
updated: 1773015371940
created: 1773015371940
---

## 2026.03.08 - Fix TTS reading quality: acronyms, metadata filtering, and section pauses

Address three issues observed during paper readings. The LLM was adding meta-commentary when expanding acronyms ("on first use"), reading author emails and affiliations extracted from PDF typesetting, and literally saying "pause" between sections instead of inserting silence.

- Reworded acronym prompt rules in both summary and full-reading system prompts to read acronyms naturally with their full form, prohibiting phrases like "on first use" or "which stands for"
- Replaced vague "add natural pauses" instructions with ElevenLabs `<break time="x.xs" />` SSML tags (1.0s between summary points, 2.0s between reading sections) -- supported on `eleven_multilingual_v2`
- Expanded `filter_metadata()` with inline patterns for email addresses, department/university affiliations, postal addresses, submission/publication dates, and correspondence lines
- Added acknowledgments to section-level skip patterns
- Updated `default.yaml` transcript_cleaning prompt to match

## 2026.03.10 - Retire monolithic audio module in favor of swanki.audio package

The single 2918-line `swanki/utils/audio.py` was split into a dedicated `swanki/audio/` package with five focused modules: `_common.py` (shared TTS utilities), `card.py` (flashcard audio), `summary.py` (document summary narration), `reading.py` (full document reading), and `lecture.py` (educational lecture generation). This file is now deleted; all imports redirect through `swanki.audio`.
