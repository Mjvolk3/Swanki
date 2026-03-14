---
id: 2qciti203tek3df5peklgpu
title: Test_audio_reading
desc: ''
updated: 1773321066457
created: 1773321066457
---

## 2026.03.12 - Update mocks for pydantic-ai migration

Updated test mocks from patching `OpenAI` client to patching `swanki.audio.reading.text_agent.run_sync`. Removed `openai_client` parameter from test function calls.

## 2026.03.13 - Update mocks for section-aware assembly

Replaced `combine_audio` mock with `combine_audio_with_section_pauses` mock to match the new section-aware assembly flow in `reading.py`.
