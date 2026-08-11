---
name: drain-merge-queue
description: Run the deterministic merge-queue drainer once (sweep free notes to main + land queued worktree branches). Normally triggered automatically by /enqueue-merge and a cron; use this only to force a drain by hand.
---

# Drain Merge Queue

Run the deterministic, **model-free** drainer (`scripts/drain_merge_queue.py`)
one time:

```bash
$HOME/miniconda3/envs/swanki/bin/python \
  $HOME/Documents/projects/Swanki/scripts/drain_merge_queue.py
```

That script self-guards with a non-blocking `flock` (at most one drainer runs at
a time), sweeps free notes to `main`, then claims and lands every queued branch
**worktree -> origin** (`rebase origin/main` -> `push HEAD:main` -> close PR ->
clean up worktree + branch). It is the **only** automated writer to `main`, and
it never touches local `main`, so a diverged local `main` cannot block a
landing. Free notes are standalone notes edited on `main` (weekly task notes and
the like -- not paired module/test/script notes, which travel with their source
through a worktree). It prints a one-line summary: what swept, what landed, what
blocked.

## You normally never call this by hand

The drainer is **event-driven**, not a poll:

- `/enqueue-merge` runs it right after adding a branch, so a landing fires the
  instant work arrives.
- A `*/2 * * * *` crontab entry (`scripts/crontab.txt`) runs it as a cheap,
  deterministic safety-net: it sweeps free notes the user edited on `main` and
  picks up any branch orphaned by a session that died mid-drain (the OS releases
  that session's `flock` on death, but its un-landed rows still need a drainer).

Both cost **zero tokens** -- the drainer is pure git/gh orchestration.

## When to use this skill

Only to **force a drain now** -- e.g. right after `merge_queue.py requeue`-ing a
branch you just fixed, or to flush the queue without waiting up to 2 min for the
cron. If a branch comes back `blocked`, fix it in its worktree and `requeue`.
