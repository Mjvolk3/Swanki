---
id: elm2rqdc1dwpvyotv9wnkdk
title: Generator
desc: ''
updated: 1773243582455
created: 1773243582455
---

## 2026.03.11 - Add mode key and lecture_only audio preset

Added `mode: full` to the generated `config.yaml` so users can override to `audio_only` to skip card generation. Added `lecture_only.yaml` audio preset (lecture only, no complementary/summary/reading) for the common use case of producing just a lecture from a paper.

### Deleted in config refactor (Step 2)

File deleted as part of the three-tier config refactor. The 1354 lines of runtime YAML generation are replaced by static YAML files in `swanki/conf/` shipped with the package. See [[swanki.config.helpers]] and [[swanki.config.hydra_plugins]] for the replacements.
