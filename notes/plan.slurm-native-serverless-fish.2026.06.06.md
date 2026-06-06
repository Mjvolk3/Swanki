---
id: iht7s0teac3ovgwytil5ama
title: '06'
desc: ''
updated: 1780784914102
created: 1780784914102
---

## Context

Today generation runs through a bash drain loop (`scripts/swanki_queue.sh`) fronted by
the `swanki-queue.service` systemd --user unit, with four long-lived Docker Fish-Speech
servers (one per GPU, ports 8080-8083) staying resident across all jobs. That model
couples *every* swanki run to a shared, always-on Fish fleet: the four servers are the
real concurrency limiter, GPU assignment is hand-pinned (MinerU steals GPU 3, Fish owns
0-3), and there is no scheduler — the drainer is a FIFO loop, so "linear vs parallel"
and "wait for the node" are not expressible.

This plan migrates generation onto **SLURM with serverless, per-job Fish**: each paper
becomes one `sbatch --gres=gpu:1 --partition=main --time=UNLIMITED` job that owns a
single GPU end to end. The job picks a free host port, brings up Fish *inside the job*
via `apptainer --nv` from a baked image (deps + model cache pre-loaded), exports
`SWANKI_FISH_PORTS=<that one port>`, runs native-conda swanki (MinerU OCR + card-gen +
Fish TTS all on the one allocated GPU = local index 0), runs delivery
(Zotero -> Anki -> ABS) as an end-of-job step, then tears Fish down. SLURM replaces the
drainer as scheduler: linear/parallel is QOS `GrpTRES=gres/gpu=N` plus
`--dependency=singleton`; the ABS debounce becomes a singleton finalizer job.

**Scope guardrail.** This PR lands the SLURM path **additively** on branch
`feat/slurm-native-queue` in an isolated worktree. The implementing agent does NOT run
real `sbatch`, does NOT build the `.sif`, does NOT mutate Docker, and does NOT touch the
live drainer or `swanki-queue.service` — those keep running. The live cutover is a
**USER-RUN runbook** (dendron note + script), not executed by the agent. Two core code
fixes ship now because they are pure improvements that also unblock the SLURM path:
`swanki/ocr/mineru.py` drops the hardcoded GPU "3" and honors the ambient
`CUDA_VISIBLE_DEVICES`; `swanki/audio/_common.py` honors a single-element
`SWANKI_FISH_PORTS`. Open issues `#21` and `#22` are orthogonal; rebase on latest main.

## Relevant Files

| Path | Action | Purpose | Stance |
|------|--------|---------|--------|
| `swanki/ocr/mineru.py` | MODIFY | Drop hardcoded `cuda_visible_devices="3"` (line 100); honor ambient `CUDA_VISIBLE_DEVICES` lazily | in-flux |
| `swanki/conf/ocr/mineru.yaml` | MODIFY | Remove `cuda_visible_devices:"3"` (line 7) GPU pin; fix stale `~/opt/miniconda3` `python_bin` (line 5) -> `~/miniconda3` | in-flux |
| `swanki/audio/_common.py` | MODIFY | `_FISH_SPEECH_PORTS` / `_discover_fish_speech_servers` honor a single-element `SWANKI_FISH_PORTS` (lines ~887-952) | in-flux |
| `scripts/swanki_enqueue.sh` | MODIFY | Becomes a thin `sbatch`-renderer; keep CLI + gilahyper defaults; add `--dependency`/`--after`; emit `sbatch --parsable` jobid | undocumented |
| `scripts/swanki_queue.sh` | MODIFY | Fill the `slurm` executor branch (line ~96) as a migration bridge; keep `local` drain working | in-flux |
| `scripts/swanki_dequeue.sh` | MODIFY | Re-point at `squeue`/`scontrol`/`scancel` for the SLURM path | undocumented |
| `Makefile` | MODIFY | Queue targets re-point at `squeue`/`scancel` | undocumented |
| `.claude/skills/swanki-queue/SKILL.md` | MODIFY | Skill inspects/edits via `squeue`/`scontrol` for SLURM jobs | undocumented |
| `scripts/swanki_job.sbatch` | NEW | Per-paper sbatch template: free-port -> apptainer Fish -> native swanki -> delivery -> teardown | n-a |
| `scripts/slurm_cutover.sh` | NEW | USER-RUN cutover/acceptance script (node resume, QOS, image build, decommission) | n-a |
| `notes/runbook.slurm-cutover.md` | NEW | USER-RUN dendron runbook for the live cutover | n-a |
| `tests/test_ocr_mineru_gpu_pin.py` | NEW | Unit test: mineru honors ambient `CUDA_VISIBLE_DEVICES`, no "3" leak | n-a |
| `tests/test_audio_fish_port_resolution.py` | NEW | Unit test: single-element `SWANKI_FISH_PORTS` discovery | n-a |
| `swanki/delivery/__main__.py` | REFERENCE | Delivery CLI (`deliver`/`finalize-abs`); module unchanged, only call site relocates | stable |
| `swanki/delivery/` (orchestrator/anki/abs) | REFERENCE | SyncSource x SyncTarget; AnkiTarget importPackage+sync; AbsTarget `abs_refresh.sh --wait` | stable |
| `~/Documents/projects/fish-speech/docker/Dockerfile` | MODIFY (runbook) | Bake deps + model cache into image so `apptainer --writable-tmpfs` needs no re-download | n-a |
| `~/Documents/projects/fish-speech/slurm/fish-speech-server.sbatch` | DELETE (runbook) | Standalone Docker-Fish sbatch (`docker run --gpus device=$FISH_GPU -p`) superseded by in-job apptainer | n-a |
| `swanki-queue.service` (systemd --user) | DELETE (runbook) | Drainer unit retired once SLURM is the scheduler | n-a |
| `tests/test_ocr_mineru_split.py`, `tests/test_ocr_dispatch.py` | REFERENCE | Existing OCR tests to keep green | stable |
| `tests/test_audio_common.py` | REFERENCE | Existing TTS discovery tests to keep green | stable |
| `tests/test_delivery_*.py` | REFERENCE | Existing delivery tests to keep green | stable |

## Key Design Decisions

1. **apptainer `--nv`, not Docker, for in-job Fish.** Docker on a SLURM compute node
   escapes the cgroup device constraint — `docker run --gpus` talks to the daemon, which
   is not inside the job's cgroup, so the job could see GPUs SLURM did not allocate.
   apptainer runs in the calling user's namespace inside the job's cgroup, so `--nv`
   exposes exactly the one device `--gres=gpu:1` granted. *Rejected: podman* — closer to
   rootless but not installed/validated on this node, and apptainer is the HPC-standard
   already present; no reason to add a second runtime.

2. **Host networking, free-port derivation.** Fish's `tools/api_server.py` accepts
   `--listen 0.0.0.0:PORT` (confirmed from live `ps`). apptainer uses **host
   networking** (no `-p` mapping like the old Docker sbatch), so the in-job server binds
   the host port directly. To avoid collisions when QOS permits multiple jobs per node,
   the job derives a candidate port from `$SLURM_JOB_ID`/`$SLURM_LOCALID`
   (e.g. `base + (SLURM_JOB_ID % range)`), then *confirms it is free* before binding.
   The single chosen port is exported as `SWANKI_FISH_PORTS=<port>` so swanki discovery
   targets exactly that server. *Why not the old `-p PORT:8080` map:* host networking is
   simpler under apptainer and removes the container-port indirection entirely.

3. **Delivery runs inside the job, not in a drainer.** `DONE` means delivered
   Zotero -> Anki -> ABS (`feedback_queue_done_means_delivered`, 2026-06-04). Under
   SLURM there is no post-loop drainer to host the delivery call, so the delivery
   *module* is unchanged but its *call site* relocates from `swanki_queue.sh:136-152`
   into the sbatch job as an end-of-job step. The job exits non-zero (or marks
   `undelivered/`) if delivery fails, preserving the "DONE = delivered" invariant.

4. **Lazy ambient `CUDA_VISIBLE_DEVICES`, not Hydra `oc.env` interpolation.** The job's
   cgroup renumbers the allocated GPU to local index 0, so a hardcoded "3" is
   out-of-range and crashes MinerU. Fix: `mineru.py` reads `CUDA_VISIBLE_DEVICES` from
   the ambient environment at call time and only sets a default if unset; the YAML pin
   is removed. *Rejected: `oc.env:CUDA_VISIBLE_DEVICES` in `mineru.yaml`* — `mineru.yaml`
   already carries a warning against compose-time `oc.env` (resolves at config-load, not
   at subprocess-launch, so it can capture the wrong/empty value); a lazy Python read is
   correct and testable.

5. **Native conda for swanki + MinerU; only Fish is containerized.** swanki and MinerU
   run in the job's native conda envs under `~/miniconda3` (swanki env + the
   `swanki-mineru` sibling), so the sibling-path lookup that resolves the MinerU
   interpreter stays intact and the `~/opt/miniconda3` gotcha is moot. Only Fish lives in
   the apptainer image. Also fixes the stale `~/opt/miniconda3` `python_bin` default in
   `mineru.yaml:5` to `~/miniconda3` per `reference_gilahyper_conda_paths`.

6. **Additive landing, no hot deletion.** The SLURM path ships alongside the running
   drainer + Docker Fish. `swanki_queue.sh`'s `slurm` executor branch becomes a working
   bridge, but the bash drain loop, `swanki-queue.service`, and the four Docker Fish
   servers are NOT deleted in this PR — their removal is a runbook step the user runs
   after the acceptance gate passes. *Rejected: keeping the drainer as the permanent
   scheduler* — it cannot express QOS concurrency or dependencies; SLURM is the point.

7. **`flock` on the Anki target only.** Card-gen and TTS are GPU-isolated per job and
   need no cross-job lock, but a single headless AnkiConnect on `127.0.0.1:8765` cannot
   take concurrent `importPackage`/`sync` calls. So the Anki delivery target takes an
   `flock` (serializing only Anki across parallel jobs). A pre-delivery health-check on
   `127.0.0.1:8765` **defers** (routes artifacts to `undelivered/`) rather than fails if
   Anki is down, so a transient Anki outage does not burn a completed generation.

8. **Linear vs parallel via QOS + singleton, ABS finalizer singleton.** Concurrency is a
   SLURM QOS `GrpTRES=gres/gpu=N` cap (N=1 forces serial like today; N>1 allows
   parallel). Ordering between specific jobs uses `--dependency` / `--after`. The ABS
   refresh debounce — previously the drainer's busy->idle finalize step — becomes a
   `--dependency=singleton` finalizer job so only one ABS refresh runs at a time after
   the batch drains.

9. **`--time=UNLIMITED`.** Explicit user choice; partition `main` is `MaxTime=INFINITE`
   on this private box. Kept as the template default; the runbook documents bounded
   wall-time (`--time=HH:MM:SS`) as an override for shared-fairness scenarios.

## Approach

Execution order, why-before-what:

**(i) Core code fixes + unit tests.** These are pure correctness wins independent of
SLURM and unblock per-job GPU isolation, so they land first.
- `swanki/ocr/mineru.py`: replace the `ocr_config.get("cuda_visible_devices","3")` at
  line 100 with a lazy read of the ambient `CUDA_VISIBLE_DEVICES` (only default if
  unset); the subprocess env (line 127) inherits it. `tests/test_ocr_mineru_gpu_pin.py`
  asserts no "3" leaks and an ambient value is honored.
- `swanki/conf/ocr/mineru.yaml`: drop the `cuda_visible_devices` key (line 7); fix
  `python_bin` (line 5) `~/opt/miniconda3` -> `~/miniconda3`.
- `swanki/audio/_common.py`: `_FISH_SPEECH_PORTS` and `_discover_fish_speech_servers`
  (lines ~887-952) already split `SWANKI_FISH_PORTS` on comma — confirm a single-element
  value (`"8123"`) yields a one-server list and discovery probes only that port.
  `tests/test_audio_fish_port_resolution.py` covers the single-port case.

**(ii) The sbatch job template** `scripts/swanki_job.sbatch`. Rendered per paper. Steps:
derive + confirm a free host port; launch Fish via `apptainer --nv` (host net) from the
baked image, backgrounded; poll `/v1/health` until ready; `export SWANKI_FISH_PORTS`;
run native-conda swanki with gilahyper defaults (`audio=all anki=default ocr=mineru
models=<voice> zotero=default`); run `python -m swanki.delivery deliver ...` (flock only
around the Anki phase, defer on Anki-down); `trap` Fish teardown on EXIT. Disambiguating
snippet:

```bash
# derive a candidate, confirm free, fall back by scanning upward
port=$(( 8100 + SLURM_JOB_ID % 400 ))
while ss -ltn "sport = :$port" | grep -q ":$port"; do port=$((port + 1)); done
apptainer instance start --nv "$FISH_SIF" fish_$SLURM_JOB_ID
apptainer exec instance://fish_$SLURM_JOB_ID \
  python tools/api_server.py --listen 0.0.0.0:"$port" &
trap 'apptainer instance stop fish_$SLURM_JOB_ID' EXIT
export SWANKI_FISH_PORTS="$port"
```

**(iii) `scripts/swanki_enqueue.sh` -> sbatch renderer.** Keep the CLI
(`--pdf`/`--key`/`--content-key`/`--voice`/`--author`/`--extra`) and gilahyper defaults;
render `swanki_job.sbatch` with those values; add `--dependency`/`--after` passthrough;
emit the `sbatch --parsable` jobid on stdout so callers can chain dependencies. Gate any
real `sbatch` behind `DRY_RUN` so the agent can render-and-inspect without submitting.

**(iv) Re-point queue tooling** at SLURM: `swanki_dequeue.sh`, the `Makefile` queue
targets, and the `swanki-queue` skill use `squeue`/`scontrol`/`scancel` instead of the
`~/.swanki-queue/pending` dir. `swanki_queue.sh`'s `slurm` executor branch (line ~96)
becomes a working bridge that shells out to the renderer.

**(v) Baked-image build recipe (described, not built).** Document a `Dockerfile` change
in `~/Documents/projects/fish-speech` to bake Python deps AND the model cache into the
image (so `apptainer --writable-tmpfs` never re-downloads at job start). The runbook
builds the `.sif` via `apptainer build ... docker-daemon://fish-speech-server:cuda`.

**(vi) USER-RUN runbook** `notes/runbook.slurm-cutover.md` + `scripts/slurm_cutover.sh`:
node resume (`systemctl restart slurmd` + `scontrol update ... state=resume`); create
`swanki` account + QOS `GrpTRES=gres/gpu=N` via `sacctmgr`; bake + build the Fish image;
cold-start measurement; decommission the four Docker Fish; retire
`swanki-queue.service`; acceptance test `srun --gres=gpu:1 nvidia-smi -L` == 1 GPU.

**Out of scope.** Preemption/requeue tuning is deferred. No hot deletion of live
services. No real `sbatch`/`.sif`/Docker mutation by the agent.

## Gotchas

1. **GPU index renumbering (HIGH).** Inside a 1-GPU cgroup the allocated card is local
   index 0; a hardcoded "3" is out of range and crashes MinerU. Sidestep: decision 4 —
   lazy ambient `CUDA_VISIBLE_DEVICES`, YAML pin removed.
2. **Fish static port scan (HIGH).** The `[8080,8081,8082,8083]` default would probe
   dead ports under serverless Fish. Sidestep: the job exports the single job-private
   port; `_common.py` honors a one-element `SWANKI_FISH_PORTS`.
3. **ffmpeg/ffprobe on PATH (MEDIUM).** `pydub` needs them; they resolve only when
   swanki runs under `conda activate swanki`. Sidestep: the sbatch template activates the
   conda env (not a bare `python`), per `reference_gilahyper_conda_paths`.
4. **Docker cgroup escape (HIGH).** `docker run --gpus` bypasses the job cgroup.
   Sidestep: `apptainer --nv` (decision 1).
5. **apptainer `--writable-tmpfs` re-download (MEDIUM).** A tmpfs overlay starts empty,
   so an un-baked image re-fetches deps/model every job = minutes of cold start.
   Sidestep: bake deps + model cache into the image (approach v).
6. **Concurrent AnkiConnect import/sync (MEDIUM).** One headless Anki cannot serve
   parallel `importPackage`/`sync`. Sidestep: `flock` on the Anki target only
   (decision 7).
7. **ABS refresh contention (MEDIUM).** Parallel jobs each triggering ABS would thrash.
   Sidestep: ABS stays `abs_refresh.sh --wait` inside the job, and the batch-level
   refresh is a `--dependency=singleton` finalizer; cron keeps using `-n`.
8. **Anki-down burns a generation (MEDIUM).** Sidestep: pre-delivery health-check on
   `127.0.0.1:8765` routes to `undelivered/` (re-runnable) instead of failing.
9. **output_dir lexicographic mis-order (MINOR).** The auto-increment can mis-sort, but
   the job knows its own output dir, so this is sidestepped for free; note only.
10. **Worktree shared `SWANKI_DATA` collision (MEDIUM).** All worktrees point at the same
    `Swanki_Data/`; concurrent jobs writing the same `<key>/<content_key>` collide.
    Sidestep: the content_key/output_dir is per-paper unique; do not run two jobs for the
    same key concurrently.
11. **Live-mutation guardrail (CRITICAL).** Agent must not run real `sbatch`, build a
    `.sif`, mutate Docker, or touch live services. Sidestep: every real action gated
    behind `DRY_RUN`; verification is `shellcheck` + `bash -n` + sample-render + pytest.
12. **Orthogonal open issues.** `#21`/`#22` are unrelated; rebase the worktree on latest
    main before opening the PR.

## Verification

**Agent-safe (run in the worktree, no live side effects):**
- `shellcheck scripts/swanki_job.sbatch scripts/swanki_enqueue.sh scripts/swanki_queue.sh
  scripts/swanki_dequeue.sh scripts/slurm_cutover.sh` — clean.
- `bash -n` on every modified/new shell script.
- **Sample render:** with `DRY_RUN=1`, run `swanki_enqueue.sh --pdf sample.pdf --key
  SAMPLE` and inspect the rendered `swanki_job.sbatch` — assert `--gres=gpu:1`,
  `--partition=main`, `--time=UNLIMITED`, the free-port + apptainer block, the
  `export SWANKI_FISH_PORTS`, the native-conda swanki invocation with gilahyper
  defaults, and the `python -m swanki.delivery` end-of-job step with Anki `flock`.
- `pytest` the existing suite (`test_ocr_mineru_split`, `test_ocr_dispatch`,
  `test_audio_common`, `test_delivery_*`) — all green — plus the two new unit tests
  (`test_ocr_mineru_gpu_pin`, `test_audio_fish_port_resolution`).

**USER-RUN manual acceptance gates (in the runbook, NOT run by the agent):**
- Node resume, then `srun --gres=gpu:1 nvidia-smi -L` shows **exactly one** GPU (the GRES
  isolation gate; not a code blocker — gres.conf already maps `gpu:rtx6000:4 ->
  /dev/nvidia[0-3]` and cgroup.conf has `ConstrainDevices=yes`).
- One end-to-end paper through `sbatch` (cold-start timing recorded).
- Cutover: decommission the four Docker Fish, retire `swanki-queue.service`, delete the
  standalone Fish sbatch.
