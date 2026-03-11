---
id: zj1izon72ef9qxd4jq477mp
title: __init__
desc: ''
updated: 1773261705807
created: 1773261705807
---

## 2026.03.11 - Remove ConfigGenerator export

Removed `ConfigGenerator` from the package's public API since `generator.py` was deleted in the config refactor. The `Pipeline` class remains the sole new-API export alongside legacy compatibility imports.
