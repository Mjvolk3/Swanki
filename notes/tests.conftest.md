---
id: kkfmyahi8bcy8v1miumnnhs
title: Conftest
desc: ''
updated: 1773321064301
created: 1773321064301
---

## 2026.03.12 - Remove mock_openai_client fixture for pydantic-ai migration

Removed the `mock_openai_client` pytest fixture that patched `openai.OpenAI`. No longer needed since all LLM calls now go through pydantic-ai agents which are mocked at the agent level in individual test files.
