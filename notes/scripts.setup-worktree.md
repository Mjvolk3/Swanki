---
id: qi0yyuthuv3whf32uyvleee
title: Setup Worktree
desc: ''
updated: 1773237976374
created: 1773237976374
---

One-command setup for new git worktrees. Run from inside the worktree directory after `git worktree add`.

## Usage

```bash
git worktree add ../Swanki.worktrees/<branch> -b <branch>
cd ../Swanki.worktrees/<branch>
bash scripts/setup-worktree.sh
```

## What it does

1. **`.env` copy** -- copies `.env` from main repo, rewrites `WORKSPACE_DIR` and `ASSET_IMAGES_DIR` to point into the worktree. `SWANKI_DATA` stays unchanged (shared sibling directory).
2. **Conda check** -- verifies the `swanki` conda environment exists.
3. **`.env.vscode`** -- sets `PYTHONPATH` so VS Code resolves imports from the worktree, not the main repo.
4. **Claude Code memory symlink** -- symlinks `~/.claude/projects/<encoded-worktree>/memory/` to the main repo's memory directory so all worktrees share the same `MEMORY.md`.
5. **Pre-commit hooks** -- runs `pre-commit install` in the worktree.
