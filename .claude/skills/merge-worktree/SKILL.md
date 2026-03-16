---
name: merge-worktree
description: Merge a worktree branch to main via PR, then clean up worktree and branch. Takes branch name as argument.
---

# Merge Worktree

Merge a completed worktree branch into main via GitHub PR (for audit trail), then remove the worktree and delete the branch.

**Usage:** `/merge-worktree <branch-name>`

If no branch name is given, list active worktrees and ask the user to pick one.

## Prerequisites

You MUST be running from the main repo, NOT from inside a worktree. If the current working directory is a worktree, tell the user to switch to the main repo window.

## Step 1: Validate

1. Run `git worktree list` to confirm the branch exists as a worktree. **Parse the worktree path from this output** -- do not hardcode paths. The output format is `<path> <hash> [<branch>]`.
2. If the branch arg doesn't match any worktree, show the list and stop.
3. Check for uncommitted changes in the worktree:
   ```
   git -C <worktree-path> status --short
   ```
   If there are uncommitted changes, warn the user and stop. They need to commit or discard first.

## Step 2: Stash main repo changes

Check `git status --short` on main. If there are uncommitted changes, run `git stash` and note that we need to `git stash pop` at the end.

## Step 3: Rebase onto main

```bash
git -C ~/projects/Swanki.worktrees/<branch> rebase main
```

If the rebase has conflicts, inform the user and stop. Do NOT force anything.

## Step 4: Push branch

```bash
git -C ~/projects/Swanki.worktrees/<branch> push -u origin <branch>
```

If the branch was already pushed and needs a force push (due to rebase), use `--force-with-lease` (not `--force`).

## Step 5: Create PR

Run from the worktree directory so `gh` picks up the correct branch:

```bash
cd ~/projects/Swanki.worktrees/<branch> && gh pr create --title "<title>" --body "<body>"
```

- **Title:** Use the first commit's message if there's a single commit, or draft a concise summary if multiple commits.
- **Body:** Use this format:

```markdown
## Summary
<1-3 bullet points summarizing changes>

## Files changed
<short list of key files>
```

## Step 6: Merge PR (regular merge, NOT squash)

```bash
gh pr merge <pr-number> --merge
```

Use `--merge` (not `--squash`, not `--rebase`). This preserves commit hashes so local branch deletion works cleanly.

Do NOT pass `--delete-branch` -- we handle cleanup ourselves to avoid the worktree branch-switch bug.

## Step 7: Update local main

```bash
git pull --ff-only origin main
```

Use `--ff-only` since we just merged and there should be no divergence. If this fails, fall back to `git pull --rebase origin main`.

## Step 8: Clean up worktree and branches

Run these in order:

1. Remove the worktree:
   ```bash
   git worktree remove --force ~/projects/Swanki.worktrees/<branch>
   ```

2. Delete the local branch:
   ```bash
   git branch -d <branch>
   ```
   If `-d` fails (e.g., hash mismatch from GitHub merge strategy), use `-D` since we confirmed the PR is merged.

3. Delete the remote branch:
   ```bash
   gh api repos/Mjvolk3/Swanki/git/refs/heads/<branch> --method DELETE
   ```

## Step 9: Restore stashed changes

If we stashed in Step 2, run `git stash pop`.

## Step 10: Verify

Run `git worktree list` and `git log --oneline -3` to confirm clean state. Print a summary:

```
Merged: <branch> -> main (PR #<number>)
Cleaned up: worktree, local branch, remote branch
```

## Important Rules

- NEVER squash merge -- use regular merge to preserve commit hashes
- NEVER pass `--delete-branch` to `gh pr merge` (causes worktree branch-switch bug)
- NEVER force-push without `--force-with-lease`
- If anything fails, stop and report -- do not try to recover automatically
- The user's tool approval prompts are the gates -- do NOT ask extra confirmation questions
