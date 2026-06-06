---
id: rbk1slurmcutover0serverlessfsh
title: SLURM Cutover (serverless Fish)
desc: ''
updated: 1780790000000
created: 1780790000000
---

USER-RUN runbook to cut swanki generation over from the bash drainer + 4 Docker
Fish containers to SLURM-native, serverless per-job Fish. The implementing agent
does NOT run any of this; it ships the code + scripts only. Helper:
`scripts/slurm_cutover.sh` ([[scripts.slurm_cutover]]) prints every command
(dry-run) and runs them with `RUN=1`. Plan: [[plan.slurm-native-serverless-fish.2026.06.06]].

## Why

Today one swanki run already eats all 4 GPUs (TTS fans across fish-0..2, OCR on
GPU 3), the 4 Docker Fish servers hold ~19.6 GB each even when idle, and there is
no scheduler. Target: each paper is one `sbatch --gres=gpu:1` job that brings up
Fish in-job via apptainer on its one allocated GPU, runs OCR+cards+TTS there,
delivers Zotero -> Anki -> ABS, and tears Fish down. Idle swanki then uses zero
GPU, and SLURM (cgroup-enforced) keeps science and swanki off each other.

## Order matters

Docker Fish runs OUTSIDE SLURM, so SLURM cannot see the 19.6 GB it holds. If you
resume the node while Docker Fish is up, SLURM will schedule onto "free" GPUs that
Docker is actually using. So: resume + prove isolation + build image + prove one
paper works serverless, and ONLY THEN decommission Docker Fish + the drainer.

## Steps

1. Preflight (read-only): `sinfo -N -o "%N %t %G"` (node is `down*`),
   `grep -i ConstrainDevices /etc/slurm/cgroup.conf` (already `yes`),
   `cat /etc/slurm/gres.conf` (already maps `gpu:rtx6000:4 -> /dev/nvidia[0-3]`).
2. Resume the node [sudo]: `sudo systemctl restart slurmd` then
   `sudo scontrol update nodename=gilahyper state=resume`. The node has been
   `DOWN+NOT_RESPONDING` since the last reboot; this re-registers it.
3. ACCEPTANCE GATE (the GRES-isolation proof the old fish sbatch doubted):
   `srun --gres=gpu:1 --partition=main nvidia-smi -L` must list EXACTLY ONE GPU.
   If it shows all four, GRES/cgroup isolation is misconfigured -- stop and fix
   gres.conf/cgroup.conf before going further (the OCR/Fish pinning assumes the
   allocated GPU is local index 0).
4. swanki account + QOS [sudo] (the linear/parallel knob):
   `sudo sacctmgr -i add account swanki` ; `sudo sacctmgr -i add user $USER account=swanki` ;
   `sudo sacctmgr -i add qos swanki` ;
   `sudo sacctmgr -i modify qos swanki set GrpTRES=gres/gpu=1` (linear; set `=2`+
   for parallel). Submit swanki jobs under this QOS (`--qos=swanki`), science gets
   the other GPUs. Preemption is deferred (v1 = cap-to-N only).
5. Bake the Fish image. Edit `fish-speech/docker/Dockerfile` so `uv sync` AND the
   s2-pro model cache run at BUILD time (today they run at every container start,
   ~2 GB of wheels -- fatal for serverless). Then
   `docker build -t fish-speech-server:cuda -f docker/Dockerfile .` and
   `apptainer build fish-speech-server.sif docker-daemon://fish-speech-server:cuda`.
   The job uses `apptainer run/exec --nv` so it stays inside the SLURM cgroup
   (Docker would not). If the entrypoint still writes into the image at runtime,
   add `--writable-tmpfs` in `swanki_job.sbatch`.
6. Cold-start measurement: submit one paper and watch time-to-`/v1/health` in the
   job log: `SWANKI_QUEUE_EXECUTOR=slurm scripts/swanki_enqueue.sh --pdf P --key K`.
   Expect ~60-90 s once deps/model are baked. Tune `SWANKI_FISH_COMPILE` (0/1) and
   a persistent TorchInductor cache if needed.
7. End-to-end paper: confirm the job generates, delivers (Zotero backup, then Anki
   under the flock), and the artifacts land. ABS: submit the finalizer once after
   a batch: `sbatch scripts/swanki_finalize_abs.sbatch` (singleton; needs no GPU).
8. [DESTRUCTIVE] Decommission Docker Fish: `docker stop fish-0 fish-1 fish-2 fish-3`
   (frees the GPUs so SLURM's view is accurate). Do this only after step 7 passes.
9. [DESTRUCTIVE] Retire the drainer: `systemctl --user disable --now swanki-queue.service`.
   SLURM is the scheduler now; enqueue with `SWANKI_QUEUE_EXECUTOR=slurm`.

## Chaining and management (from a Claude Code session)

- Linear: `--singleton` (shared job-name) or QOS `GrpTRES=gres/gpu=1`.
- Parallel: no singleton; QOS `GrpTRES=gres/gpu=N`.
- Order: `scripts/swanki_enqueue.sh ... --after <jobid>` (afterok) or
  `--dependency afterany:101:102`; the script prints the new jobid on stdout.
- Watch/manage: `squeue --me`, `sacct -X`, `scontrol show job <id>`,
  `scontrol hold/release <id>`, `scancel <id>`.

## Deferred (not in this PR)

- `Makefile`, `scripts/swanki_dequeue.sh`, and the `swanki-queue` skill were
  untracked WIP at branch time, so re-pointing them from `~/.swanki-queue/pending`
  at `squeue`/`scontrol`/`scancel` is a follow-up once they are committed.
- Preemption (`PreemptType=preempt/qos`) so a science surge can reclaim swanki's
  GPU; v1 relies on the QOS GpuTRES cap instead.
