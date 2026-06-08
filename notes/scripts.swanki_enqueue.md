---
id: scr1swankienqueue0dualbackend
title: Swanki Enqueue
desc: ''
updated: 1780790000000
created: 1780790000000
---

`scripts/swanki_enqueue.sh` -- enqueue one swanki generation job.

## 2026.06.06 - dual backend (legacy spec + SLURM submit)

Backend selected by `SWANKI_QUEUE_EXECUTOR` (same knob the drainer uses):
`local`/`noop` (default) writes a JSON spec to `$SWANKI_QUEUE_DIR/pending/` for
the bash drainer; `slurm` renders + submits [[scripts.swanki_job]] via
`sbatch --parsable --export=ALL` and prints the jobid on stdout for chaining. The
CLI (`--pdf/--key/--content-key/--voice/--author/--extra`) and gilahyper defaults
are unchanged; new flags `--after JOBID` (afterok), `--dependency SPEC` (raw), and
`--singleton` (linear) only apply to the slurm backend and are combined into one
comma-joined `--dependency`. Job inputs cross into the sbatch via exported
`SWANKI_JOB_*` env (avoids `--export` comma/space pitfalls with multi-token
`--extra` and spaced `--author`). `DRY_RUN=1` prints the submission instead of
running it. Linear/parallel is also a SLURM QOS `GrpTRES=gres/gpu=N` cap. Plan:
[[plan.slurm-native-serverless-fish.2026.06.06]]; cutover: [[runbook.slurm-cutover]].

## 2026.06.07 - SWANKI_SBATCH_EXTRA for dedicating N GPUs

Added a raw `sbatch`-flag passthrough so the operator can dedicate a fixed number
of GPUs to swanki (`8a1416d`): `export SWANKI_SBATCH_EXTRA="--qos=swanki
--account=swanki"` routes jobs through a QOS whose `GrpTRES=gres/gpu=N` caps swanki
at N concurrent GPUs, leaving 4-N free for other work. Word-split and appended to
the `sbatch` argv. Without it, swanki opportunistically uses every free GPU. The
QOS itself is created once via `sacctmgr` (see [[runbook.slurm-cutover]]); change N
anytime with `sacctmgr modify qos swanki set GrpTRES=gres/gpu=N`.
