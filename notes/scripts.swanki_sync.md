---
id: swk22sync27a5wrkpln60
title: Swanki_sync
desc: One-shot "sync to swanki servers" shortcut -- runs ABS audio refresh and Anki deck push back-to-back
updated: 1779865320957
created: 1779865320957
---

## 2026.05.27 - The user-facing shorthand for the "sync to swanki servers" shortcut

Single shell command that pushes the latest artifacts from Zotero (the source of truth) to the user's two self-hosted destinations:

1. ABS audio refresh -- `bash scripts/abs_refresh.sh` (existing). The audio path is gated per-projection by `push_audio:` in `infra/abs/projections.yml`.
2. Anki deck push -- `python scripts/swanki_anki_sync.py "$@"`. The anki path is gated per-projection by `push_anki:` in the same yaml.

Why a shell wrapper:

- The user phrased the request as "shorthand like sync to swanki servers". A shell script with `"$@"` forwarding to the Python step is the simplest match -- per-projection flags (`--projection NAME`, `--dry-run`) propagate to `swanki_anki_sync.py` without extra plumbing.
- `abs_refresh.sh` does not accept those flags (it runs its full 7-step pipeline unconditionally and uses its own `flock` for concurrency). The wrapper handles this by skipping `abs_refresh.sh` when `--dry-run` is in args, since the audio path has no dry mode.
- Resolves the Swanki repo root via `git -C "$(dirname "$(readlink -f "$0")")" rev-parse --show-toplevel`. Same pattern used in the dotfiles repo (see [[gilahyper]] / CLAUDE.md "Managing my dotfiles"). Lets the script work from any worktree and survive symlinks.

Out of scope:

- No `flock` on the wrapper itself. AnkiConnect serializes requests internally; double-invoke worst case is one importPackage waits then succeeds. `abs_refresh.sh` already has its own lock.
- Wrapper does not orchestrate sync_to_zotero (upstream; runs from the pipeline when `zotero.sync=true`). This layer is strictly "publish from Zotero to my servers".

Prereq: headless Anki + AnkiConnect on this host -- see [[anki.headless-sync]].
