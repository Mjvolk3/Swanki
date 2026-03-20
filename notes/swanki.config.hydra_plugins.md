---
id: 2vqo4jhq2v0qrr8z2ws7aj7
title: Hydra_plugins
desc: ''
updated: 1773261709967
created: 1773261709967
---

## 2026.03.11 - New three-tier Hydra SearchPathPlugin

Created `SwankiSearchPathPlugin` implementing git-config-style three-tier resolution: package defaults (`pkg://swanki/conf`), global user prefs (`~/.swanki/`), and local project overrides (`.swanki/` in cwd). Registered via `pyproject.toml` entry point under `hydra_plugins`. CLI overrides sit above all three tiers.
