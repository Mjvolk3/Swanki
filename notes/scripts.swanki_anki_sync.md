---
id: swk22ankisync27a5wrk60
title: Swanki_anki_sync
desc: Push latest .apkg per Zotero item to AnkiConnect, then trigger one AnkiWeb sync
updated: 1779865320957
created: 1779865320957
---

## 2026.05.27 - Anki side of the "sync to swanki servers" shortcut

Mirror of [[scripts.swanki_abs_sync]] for the AnkiConnect side. Reads the same `infra/abs/projections.yml`, queries Zotero for fox-tagged items (the marker `sync_to_zotero` already sets on successful upload), resolves the newest `.apkg` per chapter via [[scripts._swanki_zotero_artifacts]]'s `latest_apkgs`, downloads each to an absolute path under `SWANKI_ANKI_STAGE` (default `/scratch/Swanki_Anki_Stage`), and POSTs `importPackage` to AnkiConnect. After all imports across all projections complete, POSTs a single `sync`.

Why this shape:

- Zotero remains the single source of truth ([[scripts.publish_regen_to_abs]] 2026-04-22). The new script reads but never writes Zotero -- the upstream `sync_to_zotero` writes; this layer is purely a "publish from Zotero to my servers" step.
- AnkiConnect calls use absolute paths under `/scratch` (already in the Flatpak Anki `--filesystem=/scratch:ro` allowlist per [[anki.headless-sync]]). Empirical: 2026-05-26 smoke test confirmed absolute paths work; no copy-into-`collection.media` gymnastics needed.
- Single batch `sync` at end of run, not one per item. One AnkiWeb round-trip per shell invocation -- matches "sync to swanki servers" as one event.
- Per-projection `push_anki: bool` toggle (default `True`) in projections.yml. Set `push_anki: false` to skip a projection's apkgs while still letting its audio flow through `swanki_abs_sync.py`.
- Skip-and-report failure semantics. Per-item status lines (`+`, `[dry-run]`, `!`); exit non-zero only when AnkiConnect itself is unreachable (caught at startup `version` ping).
- Fail-fast HTTP. Single unconditional POST per call; non-2xx surfaces as `requests.HTTPError`; non-null `error` field surfaces as `RuntimeError` with the addon's message. Only narrow `try/except` is around `zot.file(att["key"])` -- mirrors the existing precedent at `swanki_abs_sync.py:208-217` (stale Zotero attachment metadata pointing at a missing file).

Pydantic models cover the AnkiConnect wire shapes (`AnkiConnectRequest`, `AnkiConnectResponse`, `ImportPackageParams`) so validation gives clear errors. Projection config is read as a plain dict to match `swanki_abs_sync.py`'s style.

Pyzotero timeout patch (`_pyz.DEFAULT_TIMEOUT = 180`) applied at module load before any other Zotero client is constructed -- same as [[scripts.publish_regen_to_abs]] -- because apkg downloads for chapter-heavy books exceed the pyzotero 30s default. Out of scope: pinning pyzotero in `pyproject.toml`.

CLI surface (argparse, mirroring `swanki_abs_sync.py`):

- Optional positional `projections_path` (defaults to `~/Documents/projects/infra/abs/projections.yml`).
- `--projection NAME` limits to one projection.
- `--dry-run` prints the resolved plan and skips downloads + POSTs (except the startup `version` ping).

Prereqs (out of scope; documented in [[anki.headless-sync]]):

- Headless Anki + AnkiConnect on this host (systemd user unit `anki-headless.service`).
- AnkiConnect reachable at `http://127.0.0.1:8765` (env `ANKI_HOST` / `ANKI_PORT` override).
- Flatpak Anki has the staging directory in its `--filesystem` allowlist.
- Minimum AnkiConnect API version: 6.

Tests: `tests/test_swanki_anki_sync.py` covers `_latest_artifact` grouping (zips and apkgs), `ankiconnect_call` response shape + error path, `verify_ankiconnect` min-version check, `push_projection` skip / dry-run / real-run / stale-attachment paths. 16 tests, all mocked (pyzotero MagicMock + `requests.post` patch).

## 2026.06.04 - Shim over swanki.delivery AnkiConnect primitives

[[swanki.delivery]]. The AnkiConnect client (`ankiconnect_call`,
`verify_ankiconnect`, the request/response + importPackage models) moved to the
canonical `swanki/delivery/targets/anki.py` (`AnkiTarget`). This script keeps
its walk-all manual "push to anki" command (Sync Terminology) but imports those
primitives so the queue's per-item delivery and this command share one
implementation. AnkiConnect-primitive tests moved to `tests/test_delivery_anki.py`;
the push-projection tests here now patch `swanki.delivery.targets.anki.requests`.
