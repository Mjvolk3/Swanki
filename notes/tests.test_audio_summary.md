---
id: poue4s2owdmfgk5g8onkhsz
title: Test_audio_summary
desc: ''
updated: 1773321067535
created: 1773321067535
---

## 2026.03.12 - Update mocks for pydantic-ai migration

Updated test mocks from patching `OpenAI` client to patching `swanki.audio.summary.text_agent.run_sync`. Removed `openai_client` parameter from test function calls.

## 2026.03.13 - Update mocks for section-aware assembly and bookends

Replaced `combine_audio` mock with `combine_audio_with_section_pauses` mock. Added `generate_bookend_audio` mock in the citation key test to prevent real TTS API calls.
