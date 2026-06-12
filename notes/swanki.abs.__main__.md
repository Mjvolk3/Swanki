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

## 2026.06.12 - add-bookmark subcommand

`python -m swanki.abs add-bookmark --content-key KEY --time MM:SS --note TEXT
[--audio-type lecture]` — file-local time (also accepts plain seconds or
HH:MM:SS via `parse_clock_time`), shifted to item-global by
[[swanki.abs.bookmarks]] `add_bookmark`; note lands `🦢 swanki:`-prefixed.
