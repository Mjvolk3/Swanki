---
id: 0hhtv1ncuqnn55asyj6hehm
title: Helpers
desc: ''
updated: 1773261708937
created: 1773261708937
---

## 2026.03.11 - New config utility module

Created to replace the 1354-line `ConfigGenerator` with four focused functions: `package_defaults_path()` returns the `swanki/conf/` location, `user_config_dir()` returns `~/.swanki/`, `init_user_config()` copies package defaults to the user dir for editing, and `show_config_info()` produces a human-readable summary of all active config locations and files.
