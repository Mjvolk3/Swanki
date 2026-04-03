---
name: setup-worktree
description: Create a new git worktree or ensure an existing one is properly configured. Wraps scripts/setup-worktree.sh with validation.
---

# Setup Worktree

Create a new git worktree or ensure an existing one is properly configured. This skill wraps `scripts/setup-worktree.sh` with additional validation.

**Usage:**
- `/setup-worktree <branch-name>` -- create new worktree and set it up
- `/setup-worktree` -- set up the current worktree (if already inside one)

## Step 1: Determine worktree path

**If a branch name is provided:**

Check if the worktree already exists:
```bash
git worktree list
```

If it exists, use its path. If not, create it:
```bash
git worktree add ~/projects/Swanki.worktrees/<branch> -b <branch>
```

Worktree naming convention:
- `feat/<name>` branch -> `~/projects/Swanki.worktrees/feat/<name>/`
- `fix/<name>` branch -> `~/projects/Swanki.worktrees/fix/<name>/`
- `plan/<name>` branch -> `~/projects/Swanki.worktrees/plan/<name>/`

**If no argument and we're already in a worktree** (path contains `.worktrees/`):

Use the current directory.

**If no argument and we're in the main repo:**

Inform the user and stop -- need a branch name.

## Step 2: Run the bash setup script

```bash
cd <worktree_path>
bash scripts/setup-worktree.sh
```

This handles:
- `.env` copy from main with path overrides
- VS Code config verification
- Claude Code auto memory symlink
- pre-commit hooks

## Step 3: Validate .env sources cleanly

Test that `.env` is syntactically valid for bash sourcing:

```bash
bash -c 'set -a; source <worktree_path>/.env 2>&1; echo "EXIT: $?"'
```

If the exit code is non-zero, fix lines that bash interprets as commands.

## Step 4: Verify import works

Test that the package imports cleanly from the worktree:

```bash
PYTHONPATH=<worktree_path> /Users/michaelvolk/miniconda3/bin/python -c "import swanki; print(swanki.__file__)"
```

The output path should point to the worktree, not the main repo.

## Step 5: Report

```
Worktree setup complete: <worktree_path>
  Branch: <branch_name>
  .env:   OK (sourced cleanly) | FIXED (N lines corrected)
  Import: swanki loads from <path>
  Memory: symlinked to main repo
```

## Important Rules

- ALWAYS run this skill when creating a new worktree or first working with one
- The bash script (`scripts/setup-worktree.sh`) is the foundation -- run it first, then layer on validation
- If the worktree is behind main, suggest rebasing AFTER setup
