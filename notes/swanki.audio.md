---
id: l3xpmitxe3jxwj0bwoyjbff
title: Audio
desc: ''
updated: 1773143237832
created: 1773143237832
---

## 2026.03.10 - Extract audio package from monolithic utils/audio.py

Refactored the 2918-line `swanki/utils/audio.py` into a standalone `swanki/audio/` package to improve maintainability and enable independent testing. The package exposes four public functions via `__init__.py`: `generate_card_audio`, `generate_lecture_audio`, `generate_reading_audio`, `generate_summary_audio`. Internal modules are `_common.py` (shared TTS, chunking, metadata filtering), `card.py`, `summary.py`, `reading.py`, and `lecture.py`.
