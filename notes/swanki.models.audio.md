---
id: f6m9pzjtkn9753biah5i38i
title: Audio
desc: ''
updated: 1773333550181
created: 1773333550181
---

## 2026.03.12 - Add strict model config

Added `model_config = ConfigDict(extra="forbid")` to `AudioTranscript` so unexpected fields raise validation errors instead of being silently ignored. Also applied ruff formatting and Google-style docstring headers.
