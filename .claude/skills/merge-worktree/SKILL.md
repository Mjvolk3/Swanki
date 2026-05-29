---
name: merge-worktree
description: Merge a worktree branch to main via PR, then clean up worktree and branch. Takes branch name as argument.
---

# Merge Worktree

Merge a completed worktree branch into main via GitHub PR (for audit trail), then remove the worktree and delete the branch.

**Usage:** `/merge-worktree <branch-name>`

If no branch name is given, list active worktrees and ask the user to pick one.

## Path convention (set first; then cwd never matters)

The recurring failure in this kind of skill is running a main-repo command **in the wrong directory**. If `git merge` or `git pull` executes inside the worktree -- because an earlier step did `cd <worktree>`, or because the steps were chained with `&&` on one line -- then `HEAD` there is the branch tip, so git prints `Already up to date` and **main never advances**. It is a silent no-op that looks like success.

To make that impossible, **every git command below targets its repo explicitly with `git -C <path>`, so the current working directory is irrelevant.** Discover and set these once at the start (then reuse verbatim):

```bash
# Parse from `git worktree list` -- never hardcode
git worktree list
# MAIN is the entry whose branch is `[main]`; WT is the entry whose branch is `[<branch>]`.
MAIN="<main-repo-path-from-worktree-list>"
WT="<worktree-path-from-worktree-list>"
```

- Main-repo operations (status check, push, pull, cleanup, verify) all use `git -C "$MAIN" ...`.
- Worktree operations (rebase, push branch, PR create) use `git -C "$WT" ...` or `cd "$WT" && gh ...`.
- **Never chain `cd "$WT"` with a main-repo git command on the same `&&` line.**

## Serialize -- never run concurrently

Do NOT start this skill while another `/merge-worktree` (or any landing/push that touches main) is in flight in another session or worktree. All worktrees share one `.git` -- parallel runs corrupt each other. Before starting, confirm no other landing is active. One landing at a time.

## Step 1: Validate

1. Run `git -C "$MAIN" worktree list` to confirm the branch exists as a worktree. **Parse paths from this output** -- do not hardcode. Format: `<path> <hash> [<branch>]`.
2. If the branch arg doesn't match any worktree, show the list and stop.
3. Check for uncommitted changes in the worktree:
   ```bash
   git -C "$WT" status --short
   ```
   If there are uncommitted changes, warn the user and stop. They need to commit or discard first.

## Step 2: Main must be clean

Check `git -C "$MAIN" status --short`. If there are any uncommitted changes (tracked or untracked) -- **stop and report**. Do NOT stash. The user must commit, discard, or move the WIP onto a branch first.

Print the dirty paths and the explicit choices:

```text
Main is dirty -- merge-worktree refuses to run.
Uncommitted paths:
  <paths>
Options:
  - Commit on main (if the changes belong there)
  - git restore --staged --worktree -- <paths>  (discard)
  - Move WIP to a branch:  git switch -c <branch>
Re-run /merge-worktree after main is clean.
```

This is by design: stashing on shared main is fragile (concurrent runs corrupt each other, popped stashes silently conflict with rebases, and a "graveyard" of un-popped stashes accumulates). Keeping main always-clean removes the entire failure class.

## Step 3: Rebase onto main

```bash
git -C "$WT" rebase main
```

If the rebase has conflicts, inform the user and stop. Do NOT force anything.

## Step 4: Push branch

```bash
git -C "$WT" push -u origin <branch>
```

If the branch was already pushed and needs a force push (due to rebase), use `--force-with-lease` (not `--force`).

## Step 5: Create PR

Run from the worktree directory so `gh` picks up the correct branch:

```bash
cd "$WT" && gh pr create --title "<title>" --body "<body>"
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
git -C "$MAIN" pull --ff-only origin main
```

Use `--ff-only` since we just merged and there should be no divergence. If this fails, fall back to `git -C "$MAIN" pull --rebase origin main`. **Note the `-C "$MAIN"`** -- never let this run in the worktree, where `git pull` would try to advance the branch, not main.

## Step 8: Clean up worktree and branches

Run these in order (each uses `-C "$MAIN"` so cwd is irrelevant):

1. Remove the worktree:
   ```bash
   git -C "$MAIN" worktree remove --force "$WT"
   ```

2. Delete the local branch:
   ```bash
   git -C "$MAIN" branch -d <branch>
   ```
   If `-d` fails (e.g., hash mismatch from GitHub merge strategy), use `-D` since we confirmed the PR is merged.

3. Delete the remote branch:
   ```bash
   gh api repos/Mjvolk3/Swanki/git/refs/heads/<branch> --method DELETE
   ```

## Step 9: Verify

```bash
git -C "$MAIN" worktree list
git -C "$MAIN" log --oneline -5
```

The branch's top commit MUST appear in main's log -- this is the final catch for a silent no-op merge. If it does not appear, the merge did not actually advance main; stop and report. Otherwise print the summary:

```text
Merged: <branch> -> main (PR #<number>)
Cleaned up: worktree, local branch, remote branch
```

## Important Rules

- **Every git command uses `git -C "$MAIN"` (main) or `git -C "$WT"` (worktree).** Never depend on cwd; never chain `cd "$WT"` with a main-repo git command on the same `&&` line.
- **Main must be clean.** No stashing. If main is dirty, bail and tell the user to commit/discard/branch the WIP first.
- **One landing at a time.** Do not run concurrently with other merge-worktree / push-to-main flows.
- NEVER squash merge -- use regular merge to preserve commit hashes.
- NEVER pass `--delete-branch` to `gh pr merge` (worktree branch-switch bug).
- NEVER force-push without `--force-with-lease`.
- If anything fails, stop and report -- do not try to recover automatically.
- The user's tool approval prompts are the gates -- do NOT ask extra confirmation questions.
