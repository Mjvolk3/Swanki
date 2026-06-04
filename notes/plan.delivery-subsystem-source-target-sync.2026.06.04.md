---
id: j1h07nusqk6oxl7a63b4s9o
title: '04'
desc: ''
updated: 1780590929892
created: 1780590929892
---

## Context

Today "delivery" — getting generated artifacts from a finished pipeline run onto
the user's self-hosted endpoints — is a pile of loosely-coupled shell + Python
scripts glued by convention, not a subsystem. `sync_to_zotero`
(`swanki/sync/zotero.py`) runs at pipeline end and is the only step the queue
knows about; everything after (Anki, ABS) is invoked by hand via
`scripts/swanki_sync.sh`. This produces three concrete failures the user hit:

1. **Queue DONE lies.** `scripts/swanki_queue.sh` marks a job `done/` on swanki
   exit 0, which only guarantees the Zotero backup. The contract (per auto-memory
   "Queue DONE = fully delivered") is Zotero backup -> headless Anki -> ABS, in
   order. A job can be DONE yet never reach Anki or ABS.
2. **Anki push walks the whole library.** `scripts/swanki_anki_sync.py` re-pushes
   every fox-tagged Zotero item on every run — O(library), slow, and couples a
   per-job delivery to global state.
3. **ABS refresh is per-invocation and Zotero-flaky.** It both round-trips through
   Zotero (upload then re-download) and inherits pyzotero's short read timeout with
   no retry, so a single 502/504 aborts delivery.

This plan builds a real, configurable delivery subsystem (`swanki/delivery/`) with
two orthogonal axes — **SyncSource** (where canonical artifacts come from:
`local` on-disk `SWANKI_DATA` output, or `zotero`) and **SyncTarget** (per server:
`anki`, `abs`) — driven by a Hydra config group. It absorbs the proven logic of
the stable scripts rather than rewriting it, hardens the Zotero client, and fixes
the queue DONE semantics. No kanban issues are tracked for this work.

## Relevant Files

| path | action | purpose | stance |
| --- | --- | --- | --- |
| `swanki/delivery/__init__.py` | NEW | export `SyncSource`, `SyncTarget`, `deliver()` orchestrator | n-a |
| `swanki/delivery/source.py` | NEW | `LocalSource` / `ZoteroSource` resolvers yielding canonical apkg+zip set for a key | n-a |
| `swanki/delivery/targets/anki.py` | NEW | Anki target: per-item importPackage + single final sync (absorbs `swanki_anki_sync.py`) | n-a |
| `swanki/delivery/targets/abs.py` | NEW | ABS target: 7-step scan + projections (absorbs `abs_refresh.sh` + `swanki_abs_sync.py`) | n-a |
| `swanki/delivery/zotero_target.py` | NEW | thin wrapper marking the Zotero backup as a target (delegates to `sync_to_zotero`) | n-a |
| `swanki/delivery/markers.py` | NEW | read/write `.delivery.json` per-target markers for crash-consistent re-drain | n-a |
| `swanki/delivery/orchestrator.py` | NEW | run targets in order Zotero->Anki->ABS, honor enable flags, ABS debounce hook | n-a |
| `swanki/conf/delivery/default.yaml` | NEW | `source: local`, all targets enabled, retry knobs | n-a |
| `swanki/conf/delivery/zotero_source.yaml` | NEW | variant: `source: zotero` for users without on-disk data | n-a |
| `swanki/conf/config.yaml` | MODIFY | register `delivery: default` in the defaults list | stable |
| `swanki/sync/zotero.py` | MODIFY | harden: explicit `httpx.Client` timeout + call-site retry wrapper; stays sole fox-tag writer | stable |
| `swanki/sync/__init__.py` | MODIFY | re-export hardened client helper if shared with delivery | stable |
| `swanki/pipeline/pipeline.py` | MODIFY | call `deliver()` (Zotero backup) at pipeline end behind config, replacing bare `sync_to_zotero` | stable |
| `scripts/swanki_queue.sh` | MODIFY | DONE = delivered Zotero->Anki->ABS; per-item Anki; ABS debounced once at drain end | in-flux |
| `scripts/swanki_anki_sync.py` | MODIFY | becomes thin shim -> `swanki.delivery` anki target (keeps Sync Terminology + tests) | stable |
| `scripts/abs_refresh.sh` | MODIFY | becomes thin shim -> ABS target; preserves `flock -n` (cron) vs `--wait` (delivery) | stable |
| `scripts/swanki_abs_sync.py` | MODIFY | logic absorbed by ABS target; file kept as shim | stable |
| `scripts/swanki_sync.sh` | MODIFY | thin shim chaining the subsystem (`--projection`/`--dry-run` forwarded) | stable |
| `scripts/_swanki_zotero_artifacts.py` | REFERENCE | reuse newest-per-content-prefix + `_chapter_base` logic from local source | stable |
| `scripts/swanki_enqueue.sh` | REFERENCE | job spec writer; unchanged but informs source key derivation | provisional |
| `~/Documents/projects/infra/abs/projections.yml` | REFERENCE | ABS target's DATA file (per-projection push_audio/push_anki); consumed, not duplicated into Hydra | undocumented |
| `tests/test_delivery_source.py` | NEW | local-source globbing + newest-per-prefix selection | n-a |
| `tests/test_delivery_anki.py` | NEW | migrated 16 assertions from `test_swanki_anki_sync.py` (importPackage-per-item, single sync, v6) | n-a |
| `tests/test_delivery_markers.py` | NEW | `.delivery.json` round-trip + resume-on-redrain | n-a |
| `tests/test_zotero_retry.py` | NEW | retry on 502/504/timeout, 404 skips, exhausts after 3 | n-a |
| `tests/test_swanki_anki_sync.py` | MODIFY | repoint at shim or migrate assertions; keep green | stable |

## Key Design Decisions

1. **Default source = `local` on gilahyper; `zotero` selectable.**
   *Why:* the deliberation verified Zotero API flakiness, and `local` avoids the
   upload-then-redownload round trip — the artifacts already sit at
   `$SWANKI_DATA/<key>/<content_key>` the moment the pipeline finishes. Zotero
   stays the backup/provenance sink and is still written every run; it is just not
   the primary read channel. *Rejected:* zotero-default (Scout-leaning) — adds a
   network dependency to the happy path and makes delivery fail when Zotero is down
   even though the bytes are local.

2. **Build the real subsystem, not a thin wrapper.**
   *Why:* the user's explicit ask is two orthogonal axes (source x target) with
   per-target enable and retry — a feature a shell wrapper cannot express cleanly.
   *Rejected:* Scout B's minimal-diff "just fix the queue hook" — it leaves the
   walk-all Anki push and per-job ABS refresh untouched, i.e. fixes one of three
   failures.

3. **Absorb proven script logic; do not rewrite from scratch; keep scripts as
   shims.** *Why:* `swanki_anki_sync.py`, `abs_refresh.sh`, `swanki_abs_sync.py`,
   `swanki_sync.sh`, `_swanki_zotero_artifacts.py` are STABLE — they carry paired
   dendron notes with documented invariants (2026-04 to 05-27) and a 16-test pin.
   Their behavior is correct; only the *orchestration* around them is broken.
   Lifting their bodies into `swanki/delivery/` and leaving the scripts as thin
   shims preserves the Sync Terminology shortcuts, the cron entrypoint, and the
   existing tests. *Rejected:* deleting the scripts — breaks "land on abs" /
   "push to anki" muscle memory and the cron job, for no gain.

4. **Zotero hardening via explicit `httpx.Client` + call-site retry, NOT the
   `DEFAULT_TIMEOUT` poke.** *Why:* pyzotero 1.11.0 is entirely httpx-based
   (established by the deliberation's verification); the existing
   `pyzotero._client.DEFAULT_TIMEOUT = 180` poke is read at client construction and
   is ineffective unless the bound name is mutated before the client is built — a
   fragile internal. Constructing the client with
   `httpx.Client(timeout=httpx.Timeout(180, connect=60))` and wrapping
   `items()/children()/file()` with a retry decorator that catches **httpx**
   exceptions (not `requests.exceptions`) is robust and explicit. **This lands
   first**, independently, so the existing scripts benefit immediately. *Rejected:*
   keeping the poke — silently no-ops on current pyzotero.

5. **Queue DONE = delivered to all enabled targets in order, recorded by
   per-target markers.** *Why:* exit-0 only proves Zotero. Emitting a
   `.delivery.json` per content key ({zotero, anki, abs} timestamps) makes DONE a
   verifiable state and lets a re-drain after a crash resume mid-delivery instead of
   re-pushing. *Rejected:* a single boolean DONE — loses which target succeeded,
   forcing full re-delivery on any partial failure.

6. **ABS refresh debounced once at end-of-drain, not per job.**
   *Why:* the ABS scan is a library-wide operation; running it per job is
   redundant and slow. The queue collects "ABS dirty" across drained jobs and fires
   one `--wait` refresh at the end. *Rejected:* per-job refresh (status quo).

7. **projections.yml stays the ABS target's DATA file.**
   *Why:* it is hand-tuned per-projection routing (push_audio/push_anki), already
   the right shape, and lives outside the repo at
   `~/Documents/projects/infra/abs/projections.yml`. Duplicating it into Hydra would
   create two sources of truth. Hydra configures *source selection + target enable +
   retry*; projections.yml configures *which projection gets what*. *Rejected:*
   migrating projections into the Hydra group.

## Approach

### Contracts

Two small structures. `SyncSource` is a Protocol with one method:
`resolve(key, content_key) -> ArtifactSet`, where `ArtifactSet` is a frozen
dataclass `{apkgs: list[Path], zips: list[Path], key, content_key}`. Two
implementations: `LocalSource` and `ZoteroSource`. `SyncTarget` is a Protocol:
`push(artifacts, *, dry_run) -> TargetResult` plus a `name` ("anki"|"abs"|
"zotero") and an `enabled` flag read from Hydra. Keeping these as Protocols (not a
`_target_` registry) matches the existing plain-nested-dict Hydra style — no
instantiation magic.

### LocalSource

Globs `$SWANKI_DATA/<key>/<content_key>/` for `*.apkg` and audio `*.zip`, then
reuses the **newest-per-content-prefix** selection from
`scripts/_swanki_zotero_artifacts.py` (`latest_apkgs`/`latest_zips` +
`_chapter_base` truncation) so multi-chapter directories pick one current artifact
per chapter base, not every historical timestamped file. This is the same dedupe
the Zotero pruner already trusts; lifting it into a shared helper avoids divergence.
ZoteroSource keeps the existing download-newest-attachment behavior for users
without on-disk data.

### Anki target

Absorbs `swanki_anki_sync.py`: assert AnkiConnect `version >= 6` (fail loud — the
addon is archived, so a silent skip would hide breakage), then
`importPackage` **per resolved apkg for this item only** (the per-item fix —
no library walk), then a **single** final `sync` action. The 16 assertions in
`tests/test_swanki_anki_sync.py` (importPackage-per-apkg, one final sync, v6 gate)
migrate verbatim into `tests/test_delivery_anki.py`.

### ABS target

Absorbs the 7-step `abs_refresh.sh` pipeline (Zotero->ABS folder sync via
`swanki_abs_sync.py` reading projections.yml, stale-chapter clean, chapter-title
set, library scan) and `swanki_abs_sync.py`'s per-projection push_audio/push_anki
routing. Critically it preserves the **lock distinction**: cron uses `flock -n`
(skip if busy), delivery-driven refresh uses `--wait` (block until the lock frees)
so a drain never silently no-ops its ABS step. Debounce lives in the orchestrator,
not here — the target stays a pure "do one refresh" unit.

### Zotero hardening (lands first)

Independent first PR. Replace the ineffective `DEFAULT_TIMEOUT` poke with an
explicit client and a retry wrapper:

```python
client = httpx.Client(timeout=httpx.Timeout(180.0, connect=60.0))
# wrap items()/children()/file(): 3 tries, exp backoff + jitter,
# retry on httpx.TimeoutException + 502/503/504; 404 -> skip, do not retry
```

`sync_to_zotero` keeps its 600s upload timeout patch and remains the **sole**
fox-tag writer (idempotent append on success) — the delivery layer never touches
the tag.

### Queue DONE rework

`swanki_queue.sh` after a swanki exit 0 invokes `python -m swanki.delivery` for the
job's key, which runs targets in order **Zotero backup -> Anki -> ABS** and writes
`.delivery.json` markers (one per target with a timestamp) into the job's output
dir. The job moves to `done/` only when all *enabled* targets are marked; partial
failure goes to `failed/` with the marker showing exactly which target stuck, so a
re-drain resumes from the unmarked target. ABS is **not** run per job here — the
orchestrator records "ABS dirty" and the drainer fires one debounced ABS refresh
after the pending queue empties.

### Execution order

1. Zotero hardening (`swanki/sync/zotero.py` + `test_zotero_retry.py`) — isolated,
   immediately useful.
2. `swanki/delivery/` package: source resolvers, anki + abs + zotero targets,
   markers, orchestrator; register `delivery` group in `config.yaml` defaults.
3. Rewire `pipeline.py` to call `deliver()` for the Zotero backup target.
4. Rework `swanki_queue.sh` DONE + ABS debounce.
5. Convert `swanki_anki_sync.py` / `abs_refresh.sh` / `swanki_abs_sync.py` /
   `swanki_sync.sh` to shims; migrate/repoint tests.

## Gotchas

1. **pyzotero is httpx, not requests.** Retry/except clauses must catch
   `httpx.TimeoutException` / `httpx.HTTPStatusError`, never
   `requests.exceptions.*` — the latter would never fire. (Established by the
   deliberation's verification of pyzotero 1.11.0.)
2. **Zotero 404 must skip, not retry.** A missing item/attachment is terminal —
   retrying wastes the backoff budget and masks the real "artifact absent"
   condition. Only 502/503/504 + timeouts retry.
3. **`abs_refresh.sh` `flock -n` silently skips.** The cron path is correct to skip
   when busy, but the delivery path must use `--wait` or a contended drain will mark
   ABS delivered without doing anything. Keep both modes (Decision/ABS target).
4. **Lockfile in `/tmp` is lost on reboot.** `flock /tmp/abs-refresh.lock` is fine
   for mutual exclusion but do not treat lock presence as durable delivery state —
   that is what `.delivery.json` is for.
5. **Queue crash-consistency.** If the drainer dies mid-delivery, exit code is
   unreliable; recovery reads `.delivery.json` and re-runs only unmarked targets.
   Markers are the source of truth, not the `done/`/`failed/` directory move.
6. **Flatpak `--filesystem` allowlist.** Headless Anki runs `--filesystem=/scratch:ro`
   — apkgs handed to `importPackage` must resolve under `/scratch` (where
   `SWANKI_DATA` lives on gilahyper). A staged copy outside the allowlist would
   import-fail with an opaque error.
7. **AnkiConnect addon is archived.** Assert `version >= 6` and fail loud; do not
   degrade to a skip — a silent skip would let DONE be marked with no Anki push.
8. **import + sync is non-atomic.** `importPackage` per item then one `sync`: if
   sync fails after imports succeed, the Anki marker must NOT be written, so re-drain
   re-syncs (importPackage is idempotent on identical apkg).
9. **Local-source newest-by-mtime ambiguity.** Two artifacts for the same chapter
    base with near-equal mtimes can tie; reuse `_chapter_base` truncation +
    timestamp-in-filename ordering (the existing pruner logic), not raw `st_mtime`,
    to pick deterministically.
10. **New Hydra group must be in `config.yaml` defaults.** Adding
    `swanki/conf/delivery/*.yaml` without the `delivery: default` line in the
    defaults list makes composition fail at startup — easy to miss.
11. **Commit hash before Zotero sync.** `sync_to_zotero` embeds the git HEAD short
    hash as artifact provenance (auto-memory rule). The Zotero backup target must
    run after the final commit/rebase, or re-sync; the delivery ordering
    (Zotero first) must not front-run the commit step.
12. **Staging dir cleanup.** If any target copies into a temp staging dir, clean it
    on both success and failure so re-drains do not accumulate or read stale stages.
13. **projections.yml lives outside the repo.** At
    `~/Documents/projects/infra/abs/projections.yml`; the ABS target must resolve it
    by the documented home-relative path (as `swanki_abs_sync.py` does), not a
    repo-relative one.

## Verification

- **pytest:** `tests/test_delivery_source.py`, `tests/test_delivery_anki.py`
  (migrated 16 assertions: importPackage-per-item, single final sync, v6 gate),
  `tests/test_delivery_markers.py` (round-trip + resume), `tests/test_zotero_retry.py`
  (502/504/timeout retry, 404 skip, exhaust-after-3). Existing
  `tests/test_swanki_anki_sync.py`, `tests/test_zotero_prune.py`,
  `tests/test_abs_bookmarks.py` stay green (shims).
- **mypy** + **ruff** on `swanki/delivery/**` and modified files.
- **Config composition:** `~/opt/miniconda3/envs/swanki/bin/Swanki swanki --cfg=job`
  resolves with the new `delivery` group present and `source: local`.
- **Manual smoke (dry-run):** deliver an already-generated chapter (e.g. Kuchel
  CH01) via `source=local` to anki + abs targets with `--dry-run`; confirm the
  local source globs `$SWANKI_DATA/<key>/<content_key>` and resolves one apkg + one
  zip per chapter base, no Zotero round trip. Then a live run: verify three
  `.delivery.json` markers appear in order, and a single ABS refresh fires after the
  (single-job) queue drains, not per job.
