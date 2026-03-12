---
id: yesph2herei6w3aa651imaf
title: Test_audio_card
desc: ''
updated: 1773321065386
created: 1773321065386
---

## 2026.03.12 - Update mocks for pydantic-ai migration

Updated test mocks from patching `OpenAI` client to patching `swanki.audio.card.text_agent.run_sync`. Mock return values now use pydantic-ai `RunResult`-style objects with `.output` attribute. Removed `openai_client` and `client` parameters from test function calls.
