---
id: scr1swankijob0sbatchserverless
title: Swanki Job (sbatch)
desc: ''
updated: 1780790000000
created: 1780790000000
---

`scripts/swanki_job.sbatch` -- the per-paper SLURM job for the serverless-Fish
model. One `--gres=gpu:1` allocation owns a single GPU end to end.

## 2026.06.06 - created

Submitted by [[scripts.swanki_enqueue]] (`SWANKI_QUEUE_EXECUTOR=slurm`) or the
[[scripts.swanki_queue]] slurm bridge, which export the inputs as `SWANKI_JOB_*`
and `sbatch --export=ALL`. Flow: derive a free host port (apptainer shares the
host network -- no `-p` map -- so concurrent jobs must not collide) -> bring up
Fish from the baked `.sif` via `apptainer --nv` on the allocated GPU, with a
`trap` that stops the instance on EXIT -> wait on `/v1/health` -> export
`SWANKI_FISH_PORTS=<port>` -> `conda activate swanki` (native; MinerU's
`swanki-mineru` sibling stays resolvable) -> `swanki ...` with gilahyper defaults
-> locate the newest output dir (mtime) -> deliver.

Delivery honors "DONE = delivered" ([[feedback_queue_done_means_delivered]]): an
AnkiConnect health-check defers (exit 75, artifacts kept, resumable) if Anki is
down; otherwise `deliver --targets zotero` (parallel-safe) then
`flock deliver --targets anki` (one headless Anki cannot serve concurrent
import+sync, so ONLY this phase is serialized across the node), then touch
`abs-dirty` for the singleton finalizer ([[scripts.swanki_finalize_abs]]). The
delivery Python module is unchanged; only the call site moved here from the
drainer. Full design: [[plan.slurm-native-serverless-fish.2026.06.06]];
cutover: [[runbook.slurm-cutover]].

## 2026.06.07 - First live cutover: four bugs found and fixed

The serverless path went live (Docker Fish decommissioned, drainer disabled) and
the first real runs surfaced four issues, all now fixed:

- **Fish interpreter** (`9fb2179`): `apptainer exec ... python` fails -- the
  image's venv is not on `PATH` once the entrypoint is bypassed. Call the venv
  binary directly: `/app/.venv/bin/python` (override `SWANKI_FISH_PYTHON`).
- **Un-baked image writes** (`3935542`): the read-only `.sif` needs
  `--writable-tmpfs` so the image's runtime writes land in an ephemeral overlay
  (`SWANKI_FISH_WRITABLE=0` once deps are baked at build time). Cold start ~64s.
- **Generation-only** (`4533c9c`): `SWANKI_JOB_DELIVER=0` stops after generation,
  skipping the card-oriented Zotero+Anki delivery. Needed for `mode=audio_only`
  (no apkg) and for parallel runs over a shared Zotero item (concurrent backups
  race); push audio to ABS separately.
- **Orphaned-Fish GPU leak** (`8a1416d`, the important one): Fish was an
  `apptainer instance` (daemon). On `scancel`/SIGKILL the `EXIT` trap never fires,
  so the daemon kept ~22GB of VRAM; the next job on that "free" card OOM'd
  (job 853: "44GB used, this process 6.9GB"). Now Fish runs as a background CHILD
  (`apptainer exec ... &`) in the job's cgroup, so SLURM cgroup-kill reaps it on
  any termination; trap also catches TERM/INT.

Confirmed NOT a problem: GPU pinning. Two concurrent jobs get distinct physical
GPUs (cgroup-isolated, local index 0 each), and `apptainer --nv` honors the
cgroup -- the OOMs were leaked memory, not pile-up. See [[runbook.slurm-cutover]].
