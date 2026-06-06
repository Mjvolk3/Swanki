---
id: scr1slurmcutover0userrunhelper
title: SLURM Cutover Script
desc: ''
updated: 1780790000000
created: 1780790000000
---

`scripts/slurm_cutover.sh` -- USER-RUN helper that drives the SLURM-native
cutover. Dry-run by default (prints each command); `RUN=1` executes.

## 2026.06.06 - created

A `step()` wrapper echoes each command and runs it only under `RUN=1`. Steps:
preflight (read-only) -> resume node `[sudo]` -> 1-GPU isolation acceptance
(`srun --gres=gpu:1 nvidia-smi -L`) -> swanki account + QOS `GrpTRES=gres/gpu=N`
`[sudo]` -> build baked Fish image + `apptainer build .sif` -> cold-start
measurement -> ABS singleton finalizer -> `[DESTRUCTIVE]` stop Docker Fish ->
`[DESTRUCTIVE]` disable `swanki-queue.service`. Never run by the implementing
agent. Narrative + rationale: [[runbook.slurm-cutover]];
plan: [[plan.slurm-native-serverless-fish.2026.06.06]].
