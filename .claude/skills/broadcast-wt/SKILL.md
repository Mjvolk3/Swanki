---
name: broadcast-wt
description: Broadcast recent main-branch changes to a worktree by rebasing. Takes branch name as argument.
---

# Broadcast to Worktree

Rebase a worktree branch onto main so it picks up recent changes. This is the inverse of merge-worktree -- instead of landing a branch, you're syncing it forward.

**Usage:** `/broadcast-wt <branch-name>`

If no branch name is given, list active worktrees and ask the user to pick one.

## Path convention

Every git command targets its repo explicitly with `git -C <path>`. Parse both paths from `git worktree list` (the `[main]` entry and the `[<branch>]` entry) -- never hardcode and never depend on cwd.

```bash
git worktree list
MAIN="<main-repo-path-from-worktree-list>"
WT="<worktree-path-from-worktree-list>"
```

## Step 1: Validate

1. Run `git -C "$MAIN" worktree list` to confirm the branch exists as a worktree. Format: `<path> <hash> [<branch>]`.
2. If the branch arg doesn't match any worktree, show the list and stop.
3. Check for uncommitted changes in the worktree:
   ```bash
   git -C "$WT" status --short
   ```
   If there are uncommitted changes, warn the user and stop. They need to **commit or discard** first -- not stash. Stashing on shared `.git` is fragile and accumulates a graveyard of un-popped stashes.
4. Check that main is clean before broadcasting **from** main. If `git -C "$MAIN" status --short` is non-empty, stop and tell the user to commit or discard the main-side WIP first -- broadcasting a moving main target is unsafe.

## Step 2: Show what will be broadcast

Show the user the commits on main that the worktree branch doesn't have yet:

```bash
git -C "$MAIN" log --oneline $(git -C "$WT" rev-parse HEAD)..main
```

If empty, inform the user the worktree is already up to date and stop.

## Step 3: Rebase worktree onto main

```bash
git -C "$WT" rebase main
```

If the rebase has conflicts, inform the user and stop. Do NOT force anything. Tell them to resolve conflicts in the worktree directory and run `git rebase --continue`.

## Step 4: Verify

```bash
git -C "$WT" log --oneline -5
```

Print a summary:

```
Broadcast to: <branch>
Commits applied: <count>
Worktree: <worktree-path>
Status: up to date with main
```

## Important Rules

- **Every git command uses `git -C "$MAIN"` or `git -C "$WT"`.** Never depend on cwd.
- **Both main and worktree must be clean.** No stashing -- commit or discard WIP first.
- NEVER force-push from this skill -- the user may or may not want to push the rebased branch.
- If rebase conflicts occur, stop immediately and report -- do not try to auto-resolve.
- The user's tool approval prompts are the gates -- do NOT ask extra confirmation questions.
