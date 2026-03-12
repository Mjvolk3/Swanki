---
id: 3efb827648a14ff3aac6e6a
title: Summary
desc: ''
updated: 1773142603440
created: 1773142603440
---

## 2026.03.10 - Document summary narration with SSML pauses

Extracted from monolithic audio module. Generates narration-style audio from document summaries with citation announcements, SSML `<break>` tags for pauses, and cleaned markdown transcripts saved alongside the audio.

## 2026.03.12 - Migrate from OpenAI client to pydantic-ai agents

Replaced direct `OpenAI` client call with shared `text_agent` from `swanki.llm.agents`. Removed `openai_client` parameter from `generate_summary_audio` -- now accepts `model: str` in pydantic-ai format. Manual retry loop replaced by agent-level `retries=3`. Part of Step 5 ([[plan.major-refactor-sequence.plan-0]]).
