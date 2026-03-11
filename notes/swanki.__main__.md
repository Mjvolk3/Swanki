---
id: p13m2d07as85clv11lsvtrl
title: __main__
desc: ''
updated: 1773243581415
created: 1773243581415
---

## 2026.03.11 - Add audio_only mode and lecture_only preset to CLI help

Updated help text to document the new `mode=<full|audio_only>` config option and the `lecture_only` audio preset, with an example showing lecture-only usage without card generation.

### Replaced ConfigGenerator with three-tier config system

Removed `ConfigGenerator.ensure_configs()` call from `@hydra.main` decorator. Hydra now discovers configs via the `SwankiSearchPathPlugin` (package defaults, `~/.swanki/`, `.swanki/`). Set `config_path=None` since the plugin handles search paths. Added `--show-defaults`, `--init-config`, and `--config-info` CLI flags. Updated help text with renamed audio presets and new config documentation.
