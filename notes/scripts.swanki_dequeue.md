---
id: xcha6u77n7vd22s5ieeybfv
title: Swanki_dequeue
desc: ''
updated: 1781052390918
created: 1781052390919
---

## 2026.06.09 - Queue slicing: the inverse of swanki_enqueue

New tool for editing the local generation queue without hand-deleting spec
files: list and slice pending jobs by 1-based FIFO index (single, range,
comma list), exact id, citation key, or content key, plus `--all` and a
`--status` dashboard (drainer systemd state, running, pending, archive
counts). Sliced specs MOVE to `cancelled/` (same archival pattern as `done/` /
`failed/`) so a mistaken slice is recoverable; `--purge` hard-deletes.
`--state failed` retargets the failed archive for pruning.

- `running/` is never touched -- claiming is an atomic-mv race with the
  drainer, and slicing there would corrupt an in-flight job.
- Indices reflect `--list` order and shift after any removal: list first,
  slice second. `--dry-run` previews; deletion prompts unless `--yes`.
- Surfaced two ways: `make queue` / `make queue-list` / `make queue-clean-failed`
  (new top-level Makefile of thin shortcuts) and the `/swanki-queue` Claude
  Code skill for conversational queue edits.
