---
id: zj1izon72ef9qxd4jq477mp
title: __init__
desc: ''
updated: 1773261705807
created: 1773261705807
---

## 2026.03.11 - Remove ConfigGenerator export

Removed `ConfigGenerator` from the package's public API since `generator.py` was deleted in the config refactor. The `Pipeline` class remains the sole new-API export alongside legacy compatibility imports.

## 2026.03.12 - Remove legacy re-exports from top-level package

All legacy function re-exports (30+ symbols like `split_pdf_into_pages`, `convert_pdf_to_markdown`, etc.) moved out of `swanki/__init__.py` into `swanki/legacy/__init__.py`. The top-level package now exports only `Pipeline`, making the public API surface intentional and minimal. Legacy code remains importable via `swanki.legacy`.
