---
id: trv85xwl57ta7f7wgyxluxu
title: Swanki Servers Sync Shortcut
desc: 'One-shot user shortcut that pushes latest .apkg per Zotero item to headless Anki + runs the ABS audio refresh, both reading Zotero as source of truth'
updated: 1779863773822
created: 1779863773822
---

## Context

The headless Anki desktop on gilahyper (see [[anki.headless-sync]]) is now running and accepting AnkiConnect calls on `127.0.0.1:8765`. A smoke test confirmed that `importPackage` with an absolute `.apkg` path under `/scratch` succeeds (Flatpak Anki was granted `--filesystem=/scratch:ro`), and a subsequent `sync` call uploads to AnkiWeb such that the Mac desktop pulls it on the next sync.

Today the audio side already has a single command: `bash scripts/abs_refresh.sh` reads Zotero (the source of truth), runs `swanki_abs_sync.py` to pull the latest mp3 zip per item, then mirrors collections, enriches metadata, cleans stale chapters, sets chapter titles, and forces an ABS rescan. The Anki side has no equivalent — generated `.apkg` files land in Zotero via `swanki/sync/zotero.py` but never reach a running Anki client, so the user has to sideload manually.

This PR adds the missing half. New `scripts/swanki_anki_sync.py` mirrors `scripts/swanki_abs_sync.py`: it reads the same `infra/abs/projections.yml`, queries Zotero for fox-emoji-tagged items (the marker `sync_to_zotero` already sets on successful upload), resolves the latest `.apkg` per item, POSTs `importPackage` to AnkiConnect with an absolute path, and POSTs a single `sync` at the end. New `scripts/swanki_sync.sh` is the user-facing shorthand — it chains `swanki_abs_sync.py` (audio) and `swanki_anki_sync.py` (cards) so one command refreshes both surfaces. Zotero stays the source of truth; nothing in `swanki/`, `sync_to_zotero.py`, or the headless Anki setup notes changes. The manual sideload affordance is unchanged. This layer is purely additive for users running their own ABS + headless Anki.

## Relevant Files

| Path | Tag | Purpose | Classification |
|---|---|---|---|
| `scripts/swanki_abs_sync.py` | MODIFY | Extract `latest_zips` into shared helper; otherwise untouched. | stable |
| `scripts/abs_refresh.sh` | REFERENCE | Existing audio refresh pipeline; called by the new shell shortcut. | stable |
| `scripts/publish_regen_to_abs.sh` | REFERENCE | Sibling one-shot script; pattern source for the wrapper layout. | stable |
| `swanki/sync/zotero.py` | REFERENCE | Defines the apkg-naming + fox-tag conventions the new script depends on. | stable |
| `swanki/pipeline/pipeline.py` | REFERENCE | Generator of the `.apkg` files this PR consumes; not edited. | stable |
| `infra/abs/projections.yml` | MODIFY | Add `push_audio` / `push_anki` per-projection toggles. | stable (no paired note; infra config) |
| `scripts/_swanki_zotero_artifacts.py` | NEW | Shared module: `_latest_artifact(zot, item_key, suffix)` plus `latest_zips` / `latest_apkgs` thin wrappers. | n/a (new) |
| `scripts/swanki_anki_sync.py` | NEW | Mirror of `swanki_abs_sync.py` for the AnkiConnect side. | n/a (new) |
| `scripts/swanki_sync.sh` | NEW | User-facing shorthand wrapping `abs_refresh.sh` + `swanki_anki_sync.py`. | n/a (new) |
| `notes/scripts.swanki_anki_sync.md` | NEW | Paired dendron note for the new Python script. | n/a (new) |
| `notes/scripts.swanki_sync.md` | NEW | Paired dendron note for the new shell wrapper. | n/a (new) |
| `notes/scripts._swanki_zotero_artifacts.md` | NEW | Paired dendron note for the shared artifact helper. | n/a (new) |
| `tests/test_swanki_anki_sync.py` | NEW | Unit tests with mocked pyzotero + mocked AnkiConnect HTTP. | n/a (new) |

Paired-note check: `swanki_abs_sync.md`, `abs_refresh.md`, `swanki.sync.zotero.md`, `publish_regen_to_abs.md` are all stable with dated entries documenting current invariants; `latest_zips`'s evolution ("single newest" → "newest per prefix") is explicit in `swanki_abs_sync.md`'s 2026.04.26 entry. `infra/abs/projections.yml` has no paired dendron note (infra-side config) but the schema has not shifted since 2026.04.20.

## Key Design Decisions

1. **Absolute paths for `importPackage`, no copy-into-`collection.media`.** Empirical evidence from yesterday's smoke test trumps stale AnkiConnect docs — a Zotero-zip-extracted `.apkg` sitting under `/scratch` imported cleanly. Copying into `~/.var/app/.../collection.media/` would double disk footprint and add a brittle Flatpak path.
2. **Flatpak filesystem grant is a prerequisite, not in-scope.** The override `--filesystem=/scratch:ro` (and equivalent for the projection's download root) is already in place per `notes/anki.headless-sync.md`. The new script's frontmatter docstring + paired note flag the dependency; we do NOT auto-detect or auto-fix it.
3. **`scripts/swanki_anki_sync.py` mirrors `scripts/swanki_abs_sync.py` 1:1.** Same projection-config loader, same Zotero pagination, same fox-tag filter, same per-projection invocation. Reviewer reads one file and understands both.
4. **`_latest_artifact` factored into a new shared module, `scripts/_swanki_zotero_artifacts.py`.** Both `latest_zips` and a new `latest_apkgs` become thin wrappers around `_latest_artifact(zot, item_key, suffix)`. Rejected: importing `latest_zips` directly from `swanki_abs_sync` into `swanki_anki_sync` — would create a non-obvious dependency between two peer "sync" scripts and resist independent testing.
5. **Pydantic models for projection-config entries and AnkiConnect request/response shapes.** `ProjectionConfig`, `AnkiConnectRequest[T]`, `AnkiConnectResponse[T]`, `ImportPackageParams`, `SyncParams`. Plain functions everywhere else.
6. **Fail-fast HTTP, no `try/except`.** Single unconditional `requests.post` to AnkiConnect's `version` action at script start; let exceptions propagate. Matches `sync_to_zotero`'s fail-fast asserts (`assert api_key`, `assert library_id`). Sole exception: `swanki_abs_sync.py:208-217` already wraps `zot.file(att["key"])` because Zotero attachment metadata can lag behind storage — we mirror that one narrow `try/except` only when reading Zotero file bytes for the same reason.
7. **No `flock` for v1.** Interactive CLI, not cron. AnkiConnect serializes incoming requests internally. `abs_refresh.sh` keeps its existing flock (it's cron-eligible); the new wrapper does not add one.
8. **Skip-and-report failure semantics.** Per-item status lines: `+ <citation_key>: imported deck.apkg`, `- <citation_key>: no apkg attached`, `! <citation_key>: importPackage failed (...)`. Exit 0 if every attempted import either succeeded or had nothing to import. Exit non-zero ONLY if AnkiConnect itself is unreachable (caught at the startup `version` ping).
9. **Latest tie-breaker = embedded `\d{8}T\d{4}` timestamp.** Same as `latest_zips` (`ZIP_PATTERN` in `swanki_abs_sync.py:39-41`). There is no mtime tiebreaker in the existing code and we will not add one — the filename timestamp IS the sort key. Apkg pattern: `^(?P<key>.+)-(?P<ts>\d{8}T\d{4})-(?P<hash>[a-f0-9]+)\.apkg$`, copied verbatim from the zip regex with the extension swapped, because `swanki/sync/zotero.py:29` writes apkgs with the same shape (`{stem}-{timestamp}-{commit}.apkg`).
10. **Filter on fox-emoji tag, same as `swanki_abs_sync.py`.** Only items the user has marked as Swanki-uploaded participate. Group-library projections (`mv-ll`) inherit the same filter.
11. **Single batch `sync` at the end of all imports.** One AnkiWeb round-trip per shell invocation, not one per item. Matches user expectation ("sync to swanki servers" — one event).
12. **Shorthand is a shell script (`scripts/swanki_sync.sh`), not a Makefile target.** The user phrased the request as "shorthand like sync to swanki servers"; a shell script with `$@` forwarding is the simplest match and lets per-projection flags propagate to both Python scripts.
13. **`--projection NAME` and `--dry-run` flags on the Python script.** argparse, mirroring how `swanki_abs_sync.py` already accepts an optional positional projections path. `--dry-run` prints the resolved per-projection plan (item key, apkg filename, absolute path) without calling AnkiConnect — supports the verification smoke test.
14. **Per-projection toggles default both ON.** Existing projections in `infra/abs/projections.yml` get `push_audio: true, push_anki: true` applied implicitly when keys are absent. New projections opt-out explicitly. Avoids breaking the existing `michaelvolk` / `mv-ll` projections on first deploy.
15. **No `pyzotero` version pin in this PR.** Pinning pyzotero is a separate housekeeping concern; if `_client.DEFAULT_TIMEOUT = 180` mutation (see `publish_regen_to_abs.sh:21-23`) becomes load-bearing for the new script, lift it the same way — but don't introduce a pin under cover of this work.

## Approach

The whole change is `scripts/` + `notes/` + `tests/` + one config file. No edits to `swanki/`, no edits to `sync_to_zotero`, no edits to the headless-Anki systemd unit or Flatpak override. The data flow once everything lands:

1. User runs `bash scripts/swanki_sync.sh [--projection NAME] [--dry-run]` on gilahyper.
2. The wrapper invokes `scripts/abs_refresh.sh` (existing — pulls audio zips from Zotero, syncs ABS collections, enriches metadata, cleans stale chapters, sets chapter titles, triggers ABS rescan).
3. The wrapper invokes `scripts/swanki_anki_sync.py` with the same flags. This script reads `infra/abs/projections.yml`, pings AnkiConnect once for version compat, then for each projection where `push_anki` is truthy walks fox-tagged Zotero items, resolves `latest_apkgs`, downloads each to an absolute path under the staging dir, and POSTs `importPackage`.
4. After all imports across all projections complete, the script POSTs a single `sync` to push to AnkiWeb.
5. The Mac's next `Sync` click pulls the new decks.

**Shared artifact helper.** `scripts/_swanki_zotero_artifacts.py` exports a generic `_latest_artifact(zot, item_key, suffix)` that walks `zot.children(item_key)`, filters attachments whose `filename` matches `^(?P<key>.+)-(?P<ts>\d{8}T\d{4})-(?P<hash>[a-f0-9]+){suffix}$`, groups by the `key` capture, and keeps the newest timestamp per group. `latest_zips` and `latest_apkgs` are one-line wrappers that pass `suffix=r"\.zip"` / `r"\.apkg"`. `scripts/swanki_abs_sync.py` imports both from the new module and deletes its local definitions; the legacy `latest_zip` (single newest, kept for back-compat per `swanki_abs_sync.md` 2026.04.26) becomes a thin wrapper over `latest_zips`. Since `scripts/` is not a package, the import resolves via the script's directory being on `sys.path` when invoked as `python scripts/swanki_abs_sync.py` from the repo root — same convention as the sibling scripts.

**`swanki_anki_sync.py` structure.** Single-file script, frontmatter docstring per the project Python format rule:

- Pydantic models at top (subset of the yaml + AnkiConnect wire shapes): `ProjectionConfig` with `push_audio: bool = True, push_anki: bool = True` plus the `zotero` sub-block; `AnkiConnectRequest` (`action`, `version: int = 6`, `params`); generic `AnkiConnectResponse[T]` with `result: T | None`, `error: str | None`; `ImportPackageParams` (`path: str`, `deleteExisting: bool = False`).
- `ankiconnect_call(action, params)` — builds the request body, `requests.post(url, json=..., timeout=300)`, `r.raise_for_status()`, validates against `AnkiConnectResponse`, returns the unwrapped `result`. On `error != None`, prints and returns `None` (skip-and-report); on connect failure, the exception propagates (fail-fast).
- `verify_ankiconnect()` — calls `ankiconnect_call("version", {})` and asserts the returned int is the minimum compatible version (6, per AnkiConnect docs and the smoke test). Run once at startup.
- `push_projection(name, cfg, api_key, dry_run)` — analog of `sync_projection` in `swanki_abs_sync.py`. Loads the Zotero client, iterates `fetch_items(zot, tag)` (reused via `from swanki_abs_sync import fetch_items, citation_key, resolve_library`), calls `latest_apkgs(zot, item['key'])`, downloads each via `zot.file(att['key'])` to a stable absolute path under `$SWANKI_ANKI_STAGE` (default `~/Documents/projects/Swanki_Anki_Stage/<projection>/`), and POSTs `importPackage` per apkg. In `--dry-run` mode, prints the resolved plan and skips download + POST.
- `main()` — argparse for `--projection NAME` (defaults to all enabled), `--dry-run`, and an optional positional projections-yaml path. Loads projections, filters by `cfg.get("push_anki", True)` and the `--projection` flag, calls `verify_ankiconnect()` once, then `push_projection(...)` per name, then a single `ankiconnect_call("sync", {})` at the end.

The Zotero attachment fetch is the one place we permit a narrow `try/except` — matching `swanki_abs_sync.py:208-217`, where stale attachment metadata pointing at a missing file already causes `zot.file(att["key"])` to throw. Skip-and-report; do not let one stale attachment kill the whole projection.

**`swanki_sync.sh` structure.** Mirrors `publish_regen_to_abs.sh` layout — `set -euo pipefail`, source the conda env + `.env`, then sequentially call `bash scripts/abs_refresh.sh` (NOT `swanki_abs_sync.py` directly — reusing the wrapper gets the user the same library scan / metadata enrichment / chapter cleanup that hourly cron gets) followed by `python scripts/swanki_anki_sync.py`, with `"$@"` forwarded to both. The per-projection `push_audio: bool` flag is read by `swanki_abs_sync.py`'s `sync_projection` (early-return on `not cfg.get("push_audio", True)`); the symmetric `push_anki` flag is read by `swanki_anki_sync.py`. Both default to `True`.

**Projection config extension.** Add two sibling keys per projection in `infra/abs/projections.yml`: `push_audio: true` and `push_anki: true` alongside the existing `zotero` block. Absent keys default to `True` (via the Pydantic field defaults) so existing deployments don't break.

**Migration in `swanki_abs_sync.py`.** Delete `latest_zips` / `latest_zip` (`scripts/swanki_abs_sync.py:103-136`) and the `ZIP_PATTERN` constant (`scripts/swanki_abs_sync.py:39-41`, moves into `_swanki_zotero_artifacts.py` as an internal regex factory); add `from _swanki_zotero_artifacts import latest_zips, latest_zip`; add a `push_audio` early-return at the top of `sync_projection`. No behavior change for the existing michaelvolk / mv-ll projections — both inherit `push_audio: true` as the default.

## Gotchas

1. **AnkiConnect addon is archived upstream.** The addon (Anki ID 2055492159, installed per `notes/anki.headless-sync.md`) still works against modern Anki 25.x but no longer receives updates. Document the version pin in the new script's frontmatter docstring (minimum compatible: AnkiConnect API version 6). If the version ping at startup returns `< 6`, fail loudly.
2. **pyzotero default read timeout is 30s.** `publish_regen_to_abs.sh:21-23` already mutates `pyzotero._client.DEFAULT_TIMEOUT = 180` for the search path. The new script's `zot.file(att["key"])` call downloads the apkg bytes — for any apkg over ~5MB on a slow link, the 30s default may bite. Apply the same `_client.DEFAULT_TIMEOUT = 180` mutation at the top of `swanki_anki_sync.py` before importing the Zotero functions from `swanki_abs_sync.py`. (Don't bother pinning pyzotero in this PR — see decision 15.)
3. **`.apkg` filename pattern must use the same `\d{8}T\d{4}-[a-f0-9]+` regex as zips.** `swanki/sync/zotero.py:29` writes apkgs as `{stem}-{timestamp}-{commit}.apkg` where `stem` itself may contain `-problem-set` or `-vocab` (per `output.apkg_filename_suffix`). The shared `_latest_artifact` regex must NOT anchor on a specific stem shape — the `(?P<key>.+)` capture is greedy and lets the apkg `key` group equal `bishop2024_CH01-problem-set` or `ManPrep1000GREwords-vocab` interchangeably. Mirror the zip pattern exactly.
4. **Book-chapter grouping is NOT done by the apkg side.** Books generate one apkg per chapter (e.g. `bishop2024_CH01_intro-...apkg` and `bishop2024_CH02_revolution-...apkg`), all attached to the same Zotero parent. `_latest_artifact` already groups by the `key` capture (the prefix before the timestamp), so each chapter resolves to its own newest apkg — multiple imports per Zotero item is the expected case. Do not strip `_CH##_` like the audio side does (the audio side groups for ABS book-of-chapters UX; Anki has no equivalent grouping).
5. **Empty projections must not abort the sync.** A projection that returns zero fox-tagged items prints `0 item(s) matched` and moves on, like `swanki_abs_sync.py` already does. Do not raise.
6. **Single `sync` at the end blocks for AnkiWeb upload.** Empirical: yesterday's smoke test showed the `sync` call blocks long enough for the upload to be in flight, and the response is `{"result": null, "error": null}`. The Mac sync that follows immediately sees the new deck. Do not add a manual sleep; AnkiConnect's response signals completion.
7. **Apkg staging directory must be absolute when passed to AnkiConnect.** AnkiConnect resolves paths against the Anki process's CWD (typically the Flatpak sandbox root); passing a relative path silently fails. The script's `Path(...).resolve()` produces the absolute form before building `ImportPackageParams`.
8. **The Flatpak sandbox needs read access to wherever the apkgs land.** `notes/anki.headless-sync.md` documents `--filesystem=/scratch:ro`. If `SWANKI_ANKI_STAGE` defaults to `~/Documents/projects/Swanki_Anki_Stage/`, the Flatpak override needs `--filesystem=$HOME/Documents/projects/Swanki_Anki_Stage:ro` too. Cleanest sidestep: default the stage dir to a path already in the sandbox (under `/scratch`), and document the override extension in the paired note.
9. **GUID stability across re-imports.** Per `notes/anki.headless-sync.md`, AnkiConnect's `importPackage` merges by note GUID — re-importing the same apkg updates existing notes rather than creating duplicates. The Swanki apkg exporter must keep GUIDs stable across regen cycles for the same content_key (it does, via the `apkg_exporter` module). If a future schema change breaks GUID stability, the operator can pass `deleteExisting: true` in `ImportPackageParams`, but that wipes review history on gilahyper — only the Mac's local schedule survives (round-trip via AnkiWeb sync). Default `deleteExisting: false`.
10. **`abs_refresh.sh` exits non-zero on flock contention with code 0 (per its own logic).** If a cron-driven `abs_refresh.sh` is mid-run when the user invokes `swanki_sync.sh`, the wrapped call returns 0 immediately ("another abs_refresh in progress — skipping"). The Anki side then runs against potentially-stale audio state on ABS — but that's fine because the two sides are independent. Do not gate `swanki_anki_sync.py` on `abs_refresh.sh`'s exit status beyond the `set -e` baseline; a non-zero from `abs_refresh.sh` (true failure, not skip) does abort the wrapper, which is the desired behavior.
11. **Per-item Zotero file download is sequential.** Each `zot.file(att["key"])` is a separate HTTP round-trip to api.zotero.org; for a projection with 30 fox-tagged items each carrying one apkg, expect 30 sequential downloads. The user's library size makes this O(seconds-to-minutes); no need to parallelize in v1, but the script's progress logging should print per-item start/finish so a long run is visible from the terminal.

## Verification

- Unit tests live in `tests/test_swanki_anki_sync.py` with mocked `pyzotero.zotero.Zotero` and a mocked `requests.post`:
  - `_latest_artifact` returns the newest apkg per `key` prefix given three fake apkgs across two prefixes at three different timestamps.
  - `_latest_artifact` returns the chapter-level newest for book apkgs (two chapters, one apkg each at different timestamps) — both retained.
  - `_latest_artifact` returns `[]` for an item with zero matching attachments.
  - `_latest_artifact` ignores attachments whose filename doesn't match the suffix (e.g. zips when called with `.apkg`).
  - `ankiconnect_call` validates response shape and raises on non-200; on `error != None` returns `None` and logs to stderr.
  - `push_projection` skips items with no apkg and reports the skip; calls `importPackage` once per resolved apkg with an absolute path.
  - `push_projection` honors `push_anki: false` (the calling `main` filters before invocation; assert the filter logic separately).
  - `--dry-run` does not call `requests.post` for `importPackage` or `sync` — only the startup `version` ping.
- Lint passes: `ruff check scripts/_swanki_zotero_artifacts.py scripts/swanki_anki_sync.py tests/test_swanki_anki_sync.py`. Confirms frontmatter docstring, Google-style docstrings, no `try/except` outside the one Zotero file-fetch site.
- Type check passes: `mypy scripts/_swanki_zotero_artifacts.py scripts/swanki_anki_sync.py` clean. Pydantic models give the AnkiConnect call shapes static types.
- Manual smoke test (the verification gate):
  - Pick one fox-tagged Zotero item with one apkg attached (e.g. the `ManPrep1000GREwords` test item used during the headless-sync setup).
  - `bash scripts/swanki_sync.sh --projection michaelvolk --dry-run` — verify printed plan lists the expected apkg filename and an absolute path under the stage dir; confirm no AnkiConnect POSTs landed (check Anki logs).
  - `bash scripts/swanki_sync.sh --projection michaelvolk` — verify ABS refresh ran (existing behavior), the apkg downloaded, `importPackage` returned `{"result": true, "error": null}`, and the final `sync` returned `{"result": null, "error": null}`.
  - Click Sync on the Mac Anki desktop and confirm the deck appears.
- Regression: `bash scripts/abs_refresh.sh` standalone still works exactly as before — the only `swanki_abs_sync.py` change is the import line, the constant deletion, the local-function deletion, and the `push_audio` early-return guard; functional behavior on the existing projections (both default `push_audio: true`) is unchanged.
- Any existing tests covering `latest_zips` / `ZIP_PATTERN` must be re-pointed at the new shared module.

