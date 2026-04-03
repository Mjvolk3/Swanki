---
name: update-src-notes
description: Update dendron module notes for changed source files (Python, Bash, etc.). Checks staged files first, then falls back to modified (unstaged) files. Appends dated sections and stages updated notes.
---

# Update Source Notes

Update dendron module notes for source files that have changed. Module notes are staged when done.

## Workflow

```
(edit source) -> /update-src-notes -> /update-tasks-weekly -> /stage -> /commit
```

Or use `/update-notes` (meta-skill) which runs this + `/update-tasks-weekly` in one command.

## Arguments

This skill accepts **optional file path arguments**. Behavior depends on whether arguments are provided:

- **With arguments** (e.g., `/update-src-notes swanki/config.py scripts/setup-worktree.sh`): update only the specified files. Uses `git diff HEAD -- <file>` to get the diff (covers both staged and unstaged changes). If a file has no diff against HEAD (e.g., new untracked file), read the full file content instead.
- **No arguments**: auto-discover changed source files (see Step 1 for the staged-then-modified fallback).

If no files are found (no args, nothing staged, nothing modified), inform the user and stop.

## Step 1: Determine target source files

- **If arguments provided**: use the listed file paths directly. Verify each file exists.
- **If no arguments**, use a two-tier discovery:
  1. **First, check staged files**: run `git diff --cached --name-only` to get staged source files (`.py`, `.sh`, etc.).
  2. **If nothing is staged**, fall back to **modified (unstaged) files**: run `git diff --name-only` to get unstaged modified source files.

Report which tier was used (staged vs. modified) so the user knows.

If the resulting list is empty after both tiers, inform the user and stop. Do not proceed to later steps.

## Step 2: Map files to dendron notes

For each target source file, derive the dendron note path by converting path separators to dots and dropping the file extension:

| Source file                     | Dendron note                          |
|---------------------------------|---------------------------------------|
| `swanki/config.py`             | `notes/swanki.config.md`             |
| `swanki/audio/card.py`         | `notes/swanki.audio.card.md`         |
| `scripts/setup-worktree.sh`    | `notes/scripts.setup-worktree.md`    |

**Rules:**

- Any source file can be synced -- package modules, scripts, shell scripts, etc.
- Convert path separators to dots, keep hyphens as-is, and drop the extension
- The dendron note is `notes/<dendron_path>.md`
- If the note file does not exist, **create it** with `dendron-cli note write` (see Step 2b).

## Step 2b: Create missing notes

For each target file whose dendron note does **not** exist, create it:

```bash
dendron-cli note write --fname "<dendron_path>"
```

This creates the note with proper dendron frontmatter.

**Important:** `dendron-cli` creates notes that end with `---\n` and **no trailing blank line**. When editing these newly created notes, match on the unique `created:` timestamp line + `---` rather than trying to match `---` followed by a blank line.

Track which notes were newly created for the summary in Step 5.

## Step 3: Update each module note

For each module note that exists:

1. **Read the note** to understand its current content.
2. **Read the diff** for the corresponding source file:
   - If running with **explicit file arguments**: `git diff HEAD -- <source_file>` (covers staged + unstaged). If this returns empty (new untracked file), read the full file content instead.
   - If discovered from **staged files** (tier 1): `git diff --cached -- <source_file>`
   - If discovered from **modified files** (tier 2): `git diff -- <source_file>`
3. **Check for an existing H2 section with today's date** (pattern: `## YYYY.MM.DD`).

### If today's date section already exists

- Read the existing section content.
- Compare it against the diff. If the diff introduces changes not covered by the existing section, **append** new subsections or bullet points to the existing dated section. Do not duplicate information already present.
- If the existing section already covers the diff, do nothing.

### If no section for today's date exists

- **Append** a new H2 section at the bottom of the file with this format:

```markdown
## YYYY.MM.DD - Brief Title

One-paragraph summary describing what changed and why.

### Subsection (optional)

- Bullet points with specifics
- Code snippets in fenced blocks where helpful
```

**Writing guidelines (intentional stance -- "why the change, for what"):**

- Lead with **purpose**, not mechanics. The diff shows *what* changed; the note should capture *why*.
- The brief title should name the intent
- The summary paragraph should be 1-3 sentences explaining motivation and impact
- Use bullet points sparingly for multi-part changes
- No Unicode emojis (breaks xelatex PDF export)

## Step 4: Stage updated module notes

Run `git add <note_path>` for each module note that was modified in Step 3.

## Step 5: Print summary

```
Source: staged files (or: modified files -- nothing was staged)

Created notes:
  - swanki.audio.card (new)

Updated module notes:
  - swanki.config (updated existing 2026.02.11 section)
  - swanki.audio.card (added new 2026.02.11 section)

All module notes staged.
```

## Important Rules

- Create missing dendron notes with `dendron-cli note write` -- never with the Write tool.
- NEVER modify dendron YAML frontmatter (the `---` block at the top of notes).
- NEVER remove or rewrite existing dated sections -- only append to them or add new ones.
- Preserve the existing style and structure of each note.
- No Unicode emojis in any markdown content.
- Do NOT ask extra approval questions -- tool approval prompts are the gates.

## Example Invocations

- `/update-src-notes` -- auto-discover: staged files first, then modified files
- `/update-src-notes swanki/config.py` -- update a Python module
- `/update-src-notes scripts/setup-worktree.sh` -- update a bash script
- `/update-src-notes swanki/config.py swanki/audio/card.py` -- update multiple files
