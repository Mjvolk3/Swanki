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

## 2026.06.08 - Layer 2: Fish restart-supervisor + crash capture

The client-side TTS retry (`0d95eaf`, `_tts_fish_speech`) re-discovers a healthy
server between attempts but was proven necessary-not-sufficient: when the in-job
Fish is hard-killed mid-generation (SIGKILL/SIGSEGV after dozens of chunks --
silent, no traceback, no CUDA OOM, no dmesg OOM-killer, VRAM flat ~23-25GB), the
single launched Fish stays dead, so the retry has nothing to reconnect to and the
job fails. The three LONGEST Hamming chapters (CH04/05/07) failed all three batch
runs; in the last batch all three died at the **same millisecond across three
different GPUs** while CH03 completed at that instant -- a shared/node-level kill
event, not per-job VRAM flakiness. Root cause still unknown; this makes the job
**survive** it.

Layer 2 wraps only the generation step (the supervisor is a generation-phase
concern; delivery 130-168 and the exit-75 Anki-deferred path are untouched):

- **`start_fish`** factors the original launch+health-wait into a function that
  reassigns the GLOBAL `fish_pid` and returns non-zero if Fish dies or never goes
  healthy. The initial launch and every respawn call it -- a respawned Fish is
  identical (same `.sif`, port, checkpoints, `apptainer exec` child not
  `instance`, preserving the `8a1416d` cgroup-reap guarantee).
- **Unified poll loop** backgrounds `swanki` and polls both PIDs from the one
  shell that owns `fish_pid` + the late-bound trap (no sidecar process, no PID
  file -- the trap re-reads the var at fire time so it always reaps the current
  Fish). swanki is checked FIRST so a completed run is never masked by a
  simultaneous Fish teardown. On Fish death: reap, capture a crash record,
  respawn same port, re-wait health, continue.
- **`capture_fish_crash`** appends a timestamped record (exit code, `dmesg`/
  `journalctl -k`/`/var/log/messages` tail, `nvidia-smi -q` Xid) to
  `$QUEUE_DIR/logs/swanki-job-$job-fish-crash.log` (/tmp fallback). Best-effort,
  always returns 0 -- instrumentation must never abort the job. This is the
  diagnostic that finally names the killer on the next occurrence.
- **Knobs:** `SWANKI_FISH_RESTART_ENABLED` (default 1; `=0` restores launch-once
  for crash-loop debugging), `SWANKI_FISH_MAX_RESTARTS` (default 3 respawns, then
  final crash capture + exit 1 so "DONE = delivered" holds),
  `SWANKI_FISH_RESPAWN_SETTLE` (default 5s, lets the socket release before
  re-binding the same port), `SWANKI_FISH_POLL_S` (default 3s). The sbatch also
  exports `SWANKI_FISH_TTS_ATTEMPTS=8` (up from the client default 4) so the
  client's 2/5/15/30s backoff outlasts a respawn's ~30-60s model reload.

**Load-bearing finding -- the voice reference survives a respawn for free.**
`ensure_fish_speech_reference` runs ONCE at TTS setup (`pipeline.py:2159`), not
per-TTS, and `_tts_fish_speech` keeps sending only `reference_id`. A respawned
Fish has empty in-memory reference state -- but Fish's `/v1/references/add`
persists the reference to `references/<id>/` ON DISK, and that dir is
bind-mounted from the host (`$FISH_REPO/references:/app/references`). On the cold
process, `load_by_id` re-reads and re-encodes the reference from that disk dir
(its in-memory cache miss just triggers a re-encode, not a failure). So the
supervisor needs NO re-registration logic and `_common.py` stays untouched (it is
in-flux from today and owns the HTTP boundary). The post-health cold re-encode on
the first post-respawn TTS fits inside the client's 1800s read timeout, so the
same `/v1/health` gate that the proven initial launch uses is sufficient on
respawn too.

Verified with a standalone control-flow harness (happy path, single-respawn
recovery, bound-exceeded -> exit 1 + final event, swanki-failure propagation,
respawn-unhealthy -> exit 1, /tmp fallback) -- no GPU needed; the real path is
the post-cutover re-queue of a LONGEST chapter. `git diff` confirms zero change
under `swanki/` (card/audio content untouched). Plan:
[[plan.fish-restart-supervisor-slurm-job.2026.06.08]].

## 2026.06.09 - Default slurm log path moved out of the repo root

Same change as [[scripts.swanki_audio_edit]]: the header `--output` fallback now
points at `/home/michaelvolk/.swanki-queue/logs/slurm-%j.log` so direct sbatch
submissions stop dumping logs into the repo root; enqueue-driven submissions
already overrode it to the same dir.
