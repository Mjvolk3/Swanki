---
id: 2xs1u58eowzrh0fwng0forx
title: Swanki Queue
desc: ''
updated: 1780369521401
created: 1780369521401
---

## 2026.06.01 - Serial generation drain queue

Fire-and-forget queue for running many swanki sources without babysitting
blocking. `scripts/swanki_enqueue.sh` drops a JSON spec into
`~/.swanki-queue/pending/`; `scripts/swanki_queue.sh` (run by the
`swanki-queue.service` systemd --user unit) drains it one job at a time and
moves each spec to `done/` or `failed/` with a per-job log under `logs/`.

**Why serial, not SLURM/parallel.** The bottleneck is the single shared Fish
TTS server, not compute slots — one swanki run already saturates all its
workers, so parallelism only thrashes the GPU. SLURM's strengths (multi-node,
fair-share, preemption) are wasted on one box + one service. So the queue is a
serial drainer whose concurrency knob keys off **Fish capacity, not GPU
count**.

**Knobs (env, settable via `systemctl --user edit swanki-queue`):**

- `SWANKI_QUEUE_CONCURRENCY` (default 1) — in-flight jobs. Keep at 1 while one
  Fish server backs the box; raise only if Fish is scaled to serve more
  concurrent streams.
- `SWANKI_QUEUE_EXECUTOR` (`local` | `noop` | `slurm`) — `local` runs swanki
  directly; `noop` is a dry-run that logs the composed argv (handy to verify a
  job before committing GPU time); `slurm` is a forward-compat stub.
- `SWANKI_REPO`, `SWANKI_CONDA_SH`, `SWANKI_QUEUE_DIR`, `SWANKI_QUEUE_POLL`.

**Usage.**

```bash
# paper
scripts/swanki_enqueue.sh --pdf /path/paper.pdf --key smith2024
# book chapter (author voice + extra override)
scripts/swanki_enqueue.sh --pdf /path/ch01.pdf --key someBook2020 \
  --content-key someBook2020_CH01_intro --voice fish_speech_bechtel \
  --author "Jane Doe" --extra "pipeline.processing.cards_per_segment=4"
```

Each job runs `swanki pdf_path=… citation_key=… audio=all anki=default
ocr=mineru models=<voice> zotero=sync [content_key=… +output_dir=<key>/<ck>]
[+author=…] confirm_before_generation=false [extra]`. `zotero=sync` + the cron
`abs_refresh` land artifacts automatically; the Zotero item for `citation_key`
must already exist (else run with `--extra "zotero=default"` for local-only).

**Install (machine-level — references the main repo scripts path):**

```bash
mkdir -p ~/.config/systemd/user
ln -sf ~/Documents/projects/Swanki/scripts/swanki-queue.service \
       ~/.config/systemd/user/swanki-queue.service
systemctl --user daemon-reload
systemctl --user enable --now swanki-queue.service
```

Inspect: `systemctl --user status swanki-queue`, `journalctl --user -u
swanki-queue -f`, `tail -f ~/.swanki-queue/queue.log`, `ls
~/.swanki-queue/pending` (depth).

**Robustness.** A restart requeues any spec orphaned in `running/` (systemd
kills in-flight children); swanki auto-increments `output_dir`, so a re-run is
safe. FIFO by filename timestamp. Spec claim is an atomic `mv pending→running`.

**Dual-purpose future.** When the box runs Fish on half the GPUs and SLURM jobs
on the rest, the same spec/interface survives: either bump
`SWANKI_QUEUE_CONCURRENCY` to Fish's concurrent-stream capacity, or flip
`SWANKI_QUEUE_EXECUTOR=slurm` and implement the stub (submit `sbatch` with
`--dependency=singleton` or array `%N`, capped to Fish capacity). Truly
efficient GPU sharing — parallel OCR across SLURM GPUs while TTS serializes on
Fish, without a job holding a GPU idle during the long TTS wait — would need
the pipeline split into per-phase jobs (OCR/card job releases its GPU; a
GPU-less TTS job streams Fish). That refactor is deferred; the spec-file
interface survives it.
