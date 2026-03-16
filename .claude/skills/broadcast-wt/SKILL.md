---
name: broadcast-wt
description: Broadcast recent main-branch changes to a worktree by rebasing. Takes branch name as argument.
---

# Broadcast to Worktree

Rebase a worktree branch onto main so it picks up recent changes. This is the inverse of merge-worktree -- instead of landing a branch, you're syncing it forward.

**Usage:** `/broadcast-wt <branch-name>`

If no branch name is given, list active worktrees and ask the user to pick one.

## Prerequisites

You MUST be running from the main repo, NOT from inside a worktree. If the current working directory is a worktree, tell the user to switch to the main repo window.

## Step 1: Validate

1. Run `git worktree list` to confirm the branch exists as a worktree. **Parse the worktree path from this output** -- do not hardcode paths. The output format is `<path> <hash> [<branch>]`.
2. If the branch arg doesn't match any worktree, show the list and stop.
3. Check for uncommitted changes in the worktree:
   ```bash
   git -C <worktree-path> status --short
   ```
   If there are uncommitted changes, warn the user and stop. They need to commit or stash first.

## Step 2: Show what will be broadcast

Show the user the commits on main that the worktree branch doesn't have yet:

```bash
git log --oneline $(git -C <worktree-path> rev-parse HEAD)..main
```

If empty, inform the user the worktree is already up to date and stop.

## Step 3: Rebase worktree onto main

```bash
git -C <worktree-path> rebase main
```

If the rebase has conflicts, inform the user and stop. Do NOT force anything. Tell them to resolve conflicts in the worktree directory and run `git rebase --continue`.

## Step 4: Verify

Run these checks:

```bash
git -C <worktree-path> log --oneline -5
```

Print a summary:

```
Broadcast to: <branch>
Commits applied: <count>
Worktree: <worktree-path>
Status: up to date with main
```

## Important Rules

- NEVER force-push from this skill -- the user may or may not want to push the rebased branch
- If rebase conflicts occur, stop immediately and report -- do not try to auto-resolve
- The user's tool approval prompts are the gates -- do NOT ask extra confirmation questions
