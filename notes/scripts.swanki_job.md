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
