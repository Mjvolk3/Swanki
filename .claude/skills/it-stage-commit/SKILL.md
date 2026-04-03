---
name: it-stage-commit
description: Iteratively stage and commit related blocks of code + notes + weekly. Enforces the commit trio rule across multiple logical groups.
---

# Iterative Stage and Commit

Stage and commit changes in logical blocks, one commit per block. Each commit pairs source files with their dendron notes and the weekly task note -- enforcing the commit trio rule. Designed for sessions where multiple independent features were implemented on `main` concurrently.

## When to Use

- After `/update-notes` has already run (which covers both source notes and weekly)
- When `git status` shows changes spanning multiple unrelated features/modules
- When working on `main` with multiple Claude Code editors producing independent changes

## Workflow

```
/update-notes -> /it-stage-commit
```

This skill replaces the separate `/stage` -> `/commit` steps with a single iterative loop.

## Step 1: Survey all changes

Run `git status` (never `-uall`) to get the full picture. Categorize every changed/untracked file.

If there are no changes, inform the user and stop.

## Step 2: Detect logical blocks

Group related files into commit blocks. Each block should be a coherent, self-contained change that makes sense as a single commit.

### Block formation rules

1. **Anchor on source files.** Each block starts from one or more related `.py` (or `.sh`) source files that form a logical unit (e.g., all files for one module, one refactor, one feature).

2. **Pull in paired files.** For each source file in a block, include:
   - Its dendron note (`notes/<dendron-path>.md`)
   - Its test file (`tests/.../<test_file>.py`) and test dendron note
   - Any new data files created for that feature

3. **Weekly note goes in the FIRST block only.** The weekly note (`notes/user.mjvolk3.swanki.tasks.weekly.*.md`) is staged with the first commit block. Subsequent blocks do not re-stage it.

4. **Non-Python files** (skills, configs, CLAUDE.md, etc.) form their own block(s) or attach to the most related code block.

5. **A file appears in exactly one block.** No duplication.

### Disambiguation

When changes span many features, use these signals to separate blocks:
- **Different subpackages** = different blocks (e.g., `audio/` vs `anki/`)
- **Related changes** stay together (e.g., `card.py` + `test_card.py` + `swanki.card.md` = one block)

## Step 3: Present blocks and proceed

Display all detected blocks with numbered labels and file lists, then proceed directly to committing. Do NOT ask for confirmation -- the tool approval prompts on each `git commit` are the only gates needed.

```
Detected commit blocks:

[1] Audio card generation refactor (5 files)
    swanki/audio/card.py
    tests/test_audio_card.py
    notes/swanki.audio.card.md
    ...

[2] Config model updates (4 files)
    swanki/config.py
    ...

Proceeding with 2 blocks...
```

## Step 4: Iterative stage-commit loop

For each confirmed block, in order:

### 4a. Stage

- `git add <files>` for all files in the block (explicit paths, never `git add -A`)
- `git rm` for deleted files
- Never stage `.env`, credentials, or secrets

### 4b. Verify staged

- `git diff --cached --name-status` to confirm what's staged

### 4c. Commit

- Check recent commit style: `git log -3 --oneline`
- Draft a commit message:
  - Summary line under 70 characters (use conventional commit prefix: `feat:`, `fix:`, `refactor:`, `test:`, `docs:`, `chore:`)
  - Bulleted list of changes (max 10 bullets)
  - Co-authored-by line
- Run the commit. The user's tool approval prompt is the gate.

### 4d. Verify and continue

- `git status` to confirm success
- Report: "Committed block [N]. M blocks remaining."
- Proceed to next block

## Step 5: Final summary

After all blocks are committed, print:

```
Committed 2 blocks:
  abc1234 feat: refactor audio card generation with cloze handling
  def5678 fix: update config model defaults

All changes committed. N files across M commits.
```

## Important Rules

- NEVER run `git add -A` or `git add .`
- NEVER stage `.env`, credentials, or secrets -- warn the user
- NEVER amend commits unless explicitly requested
- NEVER skip hooks or use `--no-verify`
- NEVER commit without the co-authored-by line
- DO NOT push unless explicitly asked
- The weekly note appears in the FIRST block only
- Each file appears in exactly one block
- Do NOT ask extra approval questions beyond block confirmation -- tool approval prompts are the gates
- If a pre-commit hook fails, fix the issue and create a NEW commit (never amend)
- `__init__.py` changes that register a new module go with that module's block

## Example Invocations

- `/it-stage-commit` -- detect blocks, confirm, commit iteratively
- "iteratively stage and commit my changes"
- "commit changes in logical blocks"
