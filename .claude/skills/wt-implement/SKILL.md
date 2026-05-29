---
name: wt-implement
description: Implement an instruction file (plan note, scratch note, .claude/plans/ file) in an isolated git worktree. Creates branch, sets up env, executes the instructions, runs verification, rebases onto main, and optionally merges.
---

# Worktree Implement

Take an instruction file and execute it in an isolated git worktree. The instruction file can be a plan note, scratch note, `.claude/plans/` file, or any markdown with implementation specs.

**Usage:** `/wt-implement <freeform text>`

The argument is freeform -- may contain file paths, dendron fnames, natural language, or a mix. Examples:

```
/wt-implement notes/plan.fix-audio-cloze-handling.2026.04.02.md
/wt-implement plan.fix-audio-cloze-handling.2026.04.02
/wt-implement the audio cloze plan and merge when done
/wt-implement .claude/plans/abc123.md merge after
```

---

## Phase 1: Parse Input and Setup

### Step 1: Find the instruction file

Extract the instruction file from the freeform input. Try these strategies in order:

1. **Literal file path**: if the input contains a token ending in `.md` that exists on disk, use it
2. **Dendron fname**: if a token looks like a dot-delimited dendron path (e.g. `plan.fix-audio.2026.04.02`), resolve to `notes/<fname>.md`
3. **Keyword search**: if neither above matches, glob `notes/plan.*.md` and `.claude/plans/*.md` for filenames containing the key words from the input. Present matches and let the user pick.
4. **Give up**: if no file found, ask the user to provide a path.

Also extract modifiers from the natural language:
- **"merge when done"** / **"merge after"** / **"to completion"**: auto-merge the PR after creation
- **"no merge"** / **"just PR"**: stop at PR creation (this is the default)

### Step 2: Read the instruction file

Read the file in full. Understand:
- What files need to be created or modified
- What verification steps are specified
- Any execution order requirements

### Step 3: Derive branch name

Extract a slug from the instruction filename:
- Strip `notes/`, `plan.`, `.claude/plans/`, date suffixes, `.md`
- Truncate to 50 chars
- Prefix with `plan/`

Examples:
- `notes/plan.fix-audio-cloze-handling.2026.04.02.md` -> `plan/fix-audio-cloze-handling`
- `notes/scratch.2026.04.02.config-overhaul.md` -> `plan/config-overhaul`

### Step 4: Create worktree

Check if it already exists first:

```bash
git worktree list
```

If not, create it:

```bash
git worktree add ~/projects/Swanki.worktrees/plan/<slug> -b plan/<slug>
```

### Step 5: Setup worktree

```bash
cd ~/projects/Swanki.worktrees/plan/<slug>
bash scripts/setup-worktree.sh
```

Then validate:
- `.env` sources cleanly in bash
- `import swanki` works from the worktree

### Step 6: cd into worktree

```bash
cd ~/projects/Swanki.worktrees/plan/<slug>
```

**CRITICAL:** ALL subsequent file edits happen in the worktree, not the main repo. Verify `pwd` shows the worktree path before making any edits.

---

## Phase 2: Implement

### Step 7: Load context

Re-read the instruction file from the worktree. For each file referenced in the specs:
- Read its current state in the worktree
- Read any additional context files mentioned

### Step 8: Execute file specifications

Work through each file spec in order. For each:

1. Read the current file
2. Apply changes per the spec (Edit for modifications, Write for new files, `dendron-cli` for new notes)
3. Verify syntax after each edit

**Rules:**
- Follow specs exactly -- no extra scope
- If a spec has a "Not fixing" or "Out of scope" section, respect it

### Step 9: Run verification

Execute whatever verification the instruction file specifies. Common pattern (use the swanki conda env -- on gilahyper this is `~/miniconda3/envs/swanki/bin/python`; on Mac the env is also named `swanki`):

1. **Tests**: `~/miniconda3/envs/swanki/bin/python -m pytest <files> -xvs`
2. **Type check**: `~/miniconda3/envs/swanki/bin/python -m mypy <files>`
3. **Lint**: `~/miniconda3/envs/swanki/bin/python -m ruff check <files>`
4. **Import check**: `~/miniconda3/envs/swanki/bin/python -c "from swanki.<module> import <thing>"`

If `~/miniconda3` does not exist (older Mac layouts may use `~/opt/miniconda3`), fall back to `conda run -n swanki python -m ...`. Do NOT hardcode `/Users/...` paths.

If any check fails, fix and re-run. Do not proceed until all pass.

---

## Phase 3: Finalize

### Step 10: Update notes and commit

Run the standard pipeline:
1. `/update-notes` -- update dendron module notes + weekly task note
2. `/stage` -- interactive staging
3. `/commit` -- commit with descriptive message

---

## Phase 4: Land on Main

### Step 11: Rebase onto main with retry

Use `git -C "$WT"` so cwd never matters; `$WT` is the worktree path from Step 6.

```bash
git -C "$WT" fetch origin main
git -C "$WT" rebase origin/main
```

**Retry logic** (for when multiple worktrees are merging concurrently):

If rebase fails with conflicts:

1. `git -C "$WT" rebase --abort`
2. Wait 10 seconds
3. `git -C "$WT" fetch origin main`
4. Retry `git -C "$WT" rebase origin/main`
5. If conflicts again, attempt resolution:
   - Weekly notes (`tasks.weekly.*.md`): auto-resolved by `.gitattributes` `merge=union`
   - `__init__.py`: keep both sides (additive)
   - Other files: inform user and stop
6. Max 3 attempts before stopping

### Step 12: Push and create PR

```bash
git -C "$WT" push -u origin plan/<slug>
```

Create PR (cd is fine here -- `gh` needs the branch context):

```bash
cd "$WT" && gh pr create --title "<concise title from instruction file>" --body "$(cat <<'EOF'
## Summary
<key changes as bullets>

## Instruction file
<dendron link or path to the instruction file>

## Verification
- Tests: PASS
- Mypy: PASS
- Ruff: PASS

Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

### Step 13: Merge (if requested)

Only if the user said "merge when done" / "to completion" / similar. Discover `$MAIN` from `git -C "$WT" worktree list` so every command targets the right repo (cwd is irrelevant):

1. `gh pr merge <number> --merge` (not squash)
2. `git -C "$MAIN" pull --ff-only origin main` -- **must use `-C "$MAIN"`**; running this in the worktree silently advances the branch instead of main
3. **Verify** the branch's top commit is now in main's log: `git -C "$MAIN" log --oneline -5`. If it is not, stop -- the merge did not land
4. `git -C "$MAIN" worktree remove --force "$WT"`
5. `git -C "$MAIN" branch -d plan/<slug>` (use `-D` if `-d` fails on hash mismatch -- PR is merged)
6. `gh api repos/Mjvolk3/Swanki/git/refs/heads/plan/<slug> --method DELETE`

Before merging, **main must be clean** (`git -C "$MAIN" status --short` empty). If not, stop and tell the user to commit or discard main-side WIP. No stashing.

If NOT merging, report the PR URL and stop.

---

## Important Rules

- ALL edits in the worktree directory, never main repo
- Follow the instruction file exactly -- no extra scope
- Respect "Not fixing" / "Out of scope" sections
- Run the instruction file's verification, not a generic test suite
- Rebase retry logic is essential for concurrent workflows
- Do NOT ask extra approval questions -- tool approval prompts are the gates
- If the instruction file has no explicit verification steps, default to: mypy + ruff on changed `.py` files
