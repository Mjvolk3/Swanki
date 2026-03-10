---
id: c04cf4024e0c46188d356b1
title: Utils
desc: ''
updated: 1773142603440
created: 1773142603440
---

## 2026.03.10 - Remove audio re-exports after package extraction

Audio functions (`generate_card_audio`, `generate_summary_audio`, `generate_reading_audio`) are no longer re-exported from `swanki.utils`. They now live in the dedicated `swanki.audio` package. The utils `__init__` retains only formatting utilities.
