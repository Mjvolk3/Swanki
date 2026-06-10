---
name: swanki-queue
description: Inspect and edit the swanki generation queue — show status, slice/remove pending jobs, reorder, edit job specs, and prune or requeue failed jobs. Use when the user wants to view, edit, cancel, reprioritize, or clean up queued swanki jobs.
user_invocable: true
---

# swanki-queue — inspect & edit the generation queue

The queue is JSON spec files under `~/.swanki-queue/{pending,running,done,failed,cancelled}/`
(`$SWANKI_QUEUE_DIR` overrides the root). FIFO order is the **filename timestamp**;
the drainer (`swanki-queue.service`) claims the lexicographically-first `pending/`
spec by atomic `mv` into `running/`. All editing here operates on `pending/` —
**never** `running/` (claiming it is a race with the drainer).

Tools you drive:
- `scripts/swanki_dequeue.sh` — status / list / slice (see `--help`)
- `scripts/swanki_enqueue.sh` — add a job
- `make queue` / `make queue-list` — thin wrappers over `--status` / `--list`

## What to do

1. **Always start by showing state** so indices are fresh:
   `bash scripts/swanki_dequeue.sh --status`
   Indices shift after any removal — re-run before a second slice.

2. **Map the user's intent to one operation below.** For anything that removes or
   mutates specs, show the matched jobs (`--dry-run`) and confirm before acting,
   unless the user already named exact jobs or said to just do it.

### View
- Dashboard: `bash scripts/swanki_dequeue.sh --status`
- Just pending with indices: `bash scripts/swanki_dequeue.sh --list`

### Slice / cancel pending jobs
Pick the narrowest selector that matches the request:
- by position: `--index 3`, range `--index 2-4`, list `--index 1,4,5`
- by exact id: `--id <id>`
- all of a citation key: `--key <citation_key>`
- one chapter: `--content-key <key>_CH##_<slug>`
- everything: `--all`

Preview then act:
```bash
bash scripts/swanki_dequeue.sh --index 2-4 --dry-run   # confirm targets
bash scripts/swanki_dequeue.sh --index 2-4 --yes       # do it
```
Sliced specs move to `cancelled/` (recoverable). Add `--purge` only if the user
wants them gone permanently.

### Reorder / reprioritize
No flag for this — order is the filename. To **promote** a pending job to run next,
rename it to a timestamp earlier than the current head (keep the `-NNNN-key.json`
suffix). Read the current head filename first, then:
```bash
# bump <file> to the front (epoch 0 prefix sorts before any real timestamp)
mv ~/.swanki-queue/pending/<file> ~/.swanki-queue/pending/19700101T000000-0001-<key>.json
```
To **demote**, give it a later timestamp than the current tail. Confirm the new
order with `--list` afterward. Do not rename a `running/` spec.

### Edit a job's contents (voice, author, extra overrides, pdf path)
A spec is plain JSON. For a small field change, open it:
`code ~/.swanki-queue/pending/<file>.json`
Keys: `pdf`, `citation_key`, `content_key`, `voice`, `author`, `extra`, `enqueued`.
If the user would rather rebuild it, slice the old one and re-enqueue (below).

### Add a job
```bash
scripts/swanki_enqueue.sh --pdf PATH --key CITATION_KEY \
  [--content-key <key>_CH##_<slug>] [--voice fish_speech_<clone>] \
  [--author "Name"] [--extra "hydra.override=x"]
```

### Failed jobs
- Inspect why one died: read `~/.swanki-queue/logs/<id>.log`.
- Prune the failed archive: `bash scripts/swanki_dequeue.sh --state failed --all --purge`
  (or `make queue-clean-failed`).
- Requeue a failed job: re-run `swanki_enqueue.sh` with the same args (read them
  from the failed spec). swanki auto-increments `output_dir`, so a re-run is safe.

## Rules
- Touch `pending/` (and `failed/` only when explicitly cleaning up); never `running/`.
- Confirm before any destructive op unless the user named exact jobs or said go.
- Prefer the script's selectors over hand-`rm`; only hand-edit/rename for content
  edits and reordering, which the script intentionally does not do.
- After any change, re-run `--status` and report the new state.
