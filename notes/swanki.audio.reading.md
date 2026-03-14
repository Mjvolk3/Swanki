---
id: adeac28210904270923c96e
title: Reading
desc: ''
updated: 1773142603440
created: 1773142603440
---

## 2026.03.10 - Full document reading with two-pass LLM processing

Extracted from monolithic audio module. Uses a two-pass approach: (1) `_humanize_latex` converts all LaTeX to natural text in 8000-token chunks, (2) LLM generates reading-optimized transcript in 3000-token chunks. Audio is chunked at a stricter 2000-char limit for quality.

## 2026.03.12 - Migrate from OpenAI client to pydantic-ai agents

Replaced direct `OpenAI` client calls with shared `text_agent` from `swanki.llm.agents` in both `generate_reading_audio` and `_humanize_latex`. Removed `openai_client` parameter -- functions now accept `model: str` in pydantic-ai format. Manual retry loops replaced by agent-level `retries=3`. Part of Step 5 ([[plan.major-refactor-sequence.plan-0]]).

## 2026.03.13 - Section-aware assembly, metadata filtering, no-filler pauses, bookends, acronyms

Addresses issues heard in merzbacher paper audio: university addresses and dates read aloud, filler text between sections instead of silence, no bookend announcements, and inconsistent acronym expansion.

- **Metadata filtering**: `filter_metadata()` now applied to content before LLM processing, stripping affiliations, emails, "Received/Accepted/Published" dates, and references
- **No-filler section breaks**: Replaced SSML `<break time="2.0s"/>` with `---SECTION_BREAK---` markers; prompt explicitly forbids filler text or transitions between sections
- **Figure handling**: New prompt instruction to announce figures with pause/`Figure X`/pause/description pattern instead of skipping them
- **Section-aware assembly**: Replaced flat `combine_audio` with `combine_audio_with_section_pauses` for real silence between sections
- **Bookends**: Generates START/END citation key announcements via `generate_bookend_audio`
- **Acronyms**: `extract_acronyms()` scans source text and injects definitions into the LLM prompt
