---
id: l2ht1mry2lnq5h6pxszowe6
title: Delivery
desc: ''
updated: 1780593069361
created: 1780593069361
---

## 2026.06.04 - Configurable delivery subsystem (source x target)

Plan: [[plan.delivery-subsystem-source-target-sync.2026.06.04]]. Replaces the
ad-hoc post-pipeline delivery scripts + the queue's exit-code-only DONE with a
real subsystem under `swanki/delivery/`.

**Two axes.**

- **SyncSource** (`source.py`) = where canonical artifacts come from.
  `LocalSource` globs the on-disk pipeline output dir (`*.apkg` + the
  `-{summary,reading,lecture}-audio.mp3` set) — the default, no network
  round-trip. `ZoteroSource` downloads the newest attachments via the hardened
  client. `ArtifactSet` is the frozen result both yield.
- **SyncTarget** (`targets/`) = per server. `ZoteroBackupTarget` wraps
  `sync_to_zotero` (still the sole fox-tag writer + commit-hash embedder).
  `AnkiTarget` is the canonical AnkiConnect client (importPackage per apkg +
  one final sync), per-item not library-wide. `AbsTarget` shells out to
  `scripts/abs_refresh.sh --wait`.

**Orchestration** (`orchestrator.py` + `__main__.py`). `deliver()` runs the
enabled targets in the fixed order Zotero -> Anki -> ABS, writing a per-target
`.delivery.json` marker (`markers.py`) after each success. An already-done
target is skipped, so a crashed re-drain resumes from the first unmarked target
instead of re-pushing — DONE is a verifiable, crash-resumable state. ABS is
**debounced**: per job it is only marked `deferred`; the queue fires one
`finalize-abs` refresh after the pending queue empties.

**Why `local` default.** Verified Zotero flakiness (502/504, and pyzotero's
30s per-call read timeout that overrides any client-level timeout — see
[[swanki.sync.zotero_client]]) plus the upload-then-redownload round trip make
Zotero a poor delivery *source*. `local` reads the bytes the pipeline just
wrote; Zotero stays the backup/provenance sink (written first, every run).

**Config** (`conf/delivery/{default,zotero_source}.yaml`, registered in
`config.yaml` defaults). Source selection + per-target enable toggles. The ABS
routing data file (`infra/abs/projections.yml`) is consumed by the refresh, not
duplicated into Hydra.

**Deviations from the plan, with rationale.**

- *Pipeline left unchanged.* The plan floated calling `deliver()` in-pipeline
  for the Zotero backup. Instead all delivery orchestration lives in the queue +
  `python -m swanki.delivery`, so ordering, markers, and the ABS debounce sit in
  one place; the queue now passes `zotero=default` (delivery owns the Zotero
  upload) rather than `zotero=sync`. The pipeline's `zotero=sync` path remains
  the standalone/manual backup. Avoids double-upload.
- *Only `swanki_anki_sync.py` became a shim.* `_swanki_zotero_artifacts.py` is
  now a re-export of `swanki/delivery/artifacts.py`, and `swanki_anki_sync.py`
  imports the canonical AnkiConnect primitives from `AnkiTarget` (keeping its
  walk-all manual command + tests). `swanki_abs_sync.py` and `abs_refresh.sh`
  stay canonical (the AbsTarget shells out to the proven refresh) rather than
  re-importing their extract logic — lower risk to the live cron. Fully gutting
  these into shims is the remaining migration step.
- *Delivery failure -> `undelivered/`, not `failed/`.* Generation is expensive;
  conflating a delivery flake with a generation failure would force a
  regenerate on retry. `undelivered/` keeps artifacts + `.delivery.json` on disk
  so a re-run resumes delivery without regenerating.

## 2026.06.09 - AbsTarget calls the module instead of subprocessing bash

`swanki/delivery/targets/abs.py` stops shelling out to
`scripts/abs_refresh.sh --wait` and calls
`swanki.abs.refresh.full_refresh(wait=True)` directly
([[swanki.abs.refresh]]), completing the absorption its stub docstring
promised. Interface unchanged (`name`, `refresh(dry_run=...)`, blocking
default), so the orchestrator, `python -m swanki.delivery finalize-abs`, and
the SLURM finalizer are untouched; `repo_dir` is retained in the signature for
compatibility but unused.
