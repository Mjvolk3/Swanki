---
id: uaasvt8tg6kra7ik9p2azdh
title: __main__
desc: ''
updated: 1781029355357
created: 1781029355357
---

## 2026.06.09 - CLI: python -m swanki.abs

Mirrors the `python -m swanki.delivery` precedent. `refresh` defaults to
non-blocking (cron parity; `--wait` blocks for the delivery path), `refresh
--target KEY --output-dir DIR` runs the always-blocking targeted refresh,
`bookmarks` lists, and `clear-bookmarks --citation-key K [--window S E]...
[--yes]` is dry-run unless `--yes`. The `scripts/abs_refresh.sh` shim execs
`refresh "$@"`, so the cron line and the four legacy publish scripts keep
working unchanged.
