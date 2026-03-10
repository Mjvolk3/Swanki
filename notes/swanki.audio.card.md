---
id: eec275051e774ac494ab386
title: Card
desc: ''
updated: 1773142603440
created: 1773142603440
---

## 2026.03.10 - Flashcard audio generation with cloze handling and citation prefixing

Extracted from monolithic audio module. Handles cloze masking (`_replace_all_cloze_with_blank` for front, `_remove_cloze_markers` for back), image summary integration, LLM-based transcript generation via detailed system prompts (`_build_transcript_system_prompt`), citation humanization, and multi-chunk TTS with combination.
