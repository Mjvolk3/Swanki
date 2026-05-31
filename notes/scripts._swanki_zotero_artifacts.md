---
id: zot22art27wkrly5pqxh02a
title: _swanki_zotero_artifacts
desc: Shared "newest artifact per content-prefix" lookup over Zotero child attachments
updated: 1779865320957
created: 1779865320957
---

## 2026.05.27 - Extracted from swanki_abs_sync.py for reuse by the anki sync side

`sync_to_zotero` (swanki/sync/zotero.py:29) uploads Swanki outputs as timestamped attachments shaped `<prefix>-<YYYYMMDDThhmm>-<commit>.<ext>`. A single Zotero item (paper or multi-chapter book) accumulates several of these over re-runs. Both `swanki_abs_sync.py` (zips) and the new `swanki_anki_sync.py` (apkgs) need to resolve the newest attachment per chapter prefix, so the implementation lives here once.

`_latest_artifact(zot, item_key, pattern)` walks `zot.children(item_key)`, filters attachments whose `filename` matches `pattern` (a compiled regex from `_artifact_pattern(suffix)` with named groups `key`, `ts`, `hash`), groups by the `key` capture, and keeps the newest `ts` per group. `latest_zips`, `latest_zip` (back-compat single-newest wrapper), and `latest_apkgs` are thin wrappers passing `.zip` / `.apkg` patterns.

Decisions retained from the previous `latest_zips` in [[scripts.swanki_abs_sync]]:

- Group by the `key` capture (the prefix before the timestamp). For books with `_CH##_<slug>` chapters, each chapter is its own prefix and resolves to its own newest attachment -- exactly the behavior books need.
- Timestamp `\d{8}T\d{4}` is the sole tie-breaker. There is no mtime fallback; the filename timestamp IS the sort key.
- `latest_zip` (singular) preserved only as a back-compat wrapper. New callers should use the plural form.

Not a package -- `scripts/` is on `sys.path[0]` when scripts are invoked from the repo root (`python scripts/foo.py`), so siblings import directly: `from _swanki_zotero_artifacts import latest_apkgs`. Tests import via an explicit `sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))` in `tests/test_swanki_anki_sync.py`.
