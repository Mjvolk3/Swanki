---
id: irezw5cmga8eba0djaoal52
title: Refresh
desc: ''
updated: 1781029348748
created: 1781029348748
---

## 2026.06.09 - Full refresh as module function + seconds-scale targeted refresh

`full_refresh(wait=...)` reproduces the 7 steps of the legacy
`scripts/abs_refresh.sh` pipeline in Python. The flock moved with it:
`fcntl.flock` on the SAME `/tmp/abs-refresh.lock` (same syscall as flock(1)),
so during the migration window an in-flight bash cron run and a module run
still exclude each other. `wait=False` = cron semantics (skip when contended);
`wait=True` = delivery semantics (block; queue DONE means delivered).
Environment-agnostic: bash drainer, SLURM finalizer, cron shim, and
interactive use call the same function.

- `targeted_refresh(citation_key=..., output_dir=...)` is the hot republish
  loop: the full refresh costs ~20 min (Zotero multi-projection repagination,
  not ABS), where drop -> scan affected libraries -> verify -> per-item
  chapter fix-up takes seconds. NOT scan-only: the republished file's new
  `-<TS>-<hash>` name leaves chapters pointing at a deleted file until
  `fix_item_chapters` runs.
- Routing is by existing group dir, fanned out across every push_audio
  projection that already carries the item (a republish always has a prior
  sync). A genuinely new item raises and goes through the full refresh.
- Verification polls the item until its audioFiles serve the new filenames
  (60s budget); a timeout raises rather than reporting false success.
