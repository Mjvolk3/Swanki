---
name: update-notes
description: "Meta-skill: update dendron module notes for changed source files, then update the weekly task note. Combines /update-src-notes + /update-tasks-weekly into one command. Run before /stage and /commit."
---

# Update Notes

Meta-skill that updates both **source module notes** and the **weekly task note** in one command. Replaces the old two-step `/update-src-notes` -> `/update-tasks-weekly` sequence.

## Workflow

```
(edit source) -> /update-notes -> /stage -> /commit
```

For fine-grained control, the individual skills are still available:

```
(edit source) -> /update-src-notes -> /update-tasks-weekly -> /stage -> /commit
```

## Arguments

This skill accepts **optional file path arguments**, passed through to the source notes step:

- **With arguments** (e.g., `/update-notes swanki/config.py scripts/setup-worktree.sh`): update only the specified files.
- **No arguments**: auto-discover changed source files (staged first, then modified).

If no files are found (no args, nothing staged, nothing modified), inform the user and stop.

---

# Part 1: Update Source Module Notes

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
- Convert path separators to dots, keep hyphens as-is, and drop the extension: `scripts/setup-worktree.sh` > `scripts.setup-worktree`
- The dendron note is `notes/<dendron_path>.md`
- If the note file does not exist, **create it** with `dendron-cli note write` (see Step 2b).

## Step 2b: Create missing notes

For each target file whose dendron note does **not** exist, create it:

```bash
dendron-cli note write --fname "<dendron_path>"
```

For example, `swanki/audio/card.py` with no note:

```bash
dendron-cli note write --fname "swanki.audio.card"
```

This creates `notes/swanki.audio.card.md` with proper dendron frontmatter. The note is then treated as an existing note in Step 3 (it will get a dated section appended).

**Important:** `dendron-cli` creates notes that end with `---\n` and **no trailing blank line**. When editing these newly created notes, match on the unique `created:` timestamp line + `---` rather than trying to match `---` followed by a blank line.

Track which notes were newly created for the summary.

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

- **Append** a new H2 section at the bottom of the file (before any trailing blank lines) with this format:

```markdown
## YYYY.MM.DD - Brief Title

One-paragraph summary describing what changed and why.

### Subsection (optional)

- Bullet points with specifics
- Code snippets in fenced blocks where helpful
```

**Writing guidelines (intentional stance -- "why the change, for what"):**

- Lead with **purpose**, not mechanics. Ask: "why does this change exist? what does it enable?" The diff already shows *what* changed; the note should capture *why*.
- The brief title should name the intent (e.g., "Decouple audio generation from card rendering", not "Remove generate_audio function")
- The summary paragraph should be 1-3 sentences explaining motivation and impact. Keep it brief.
- Use bullet points sparingly for multi-part changes. Omit trivial details (import reordering, lint fixes) unless they reflect a deliberate decision.
- Include short code snippets only when they clarify a new interface or configuration.
- Follow the note's existing style and level of detail.
- No Unicode emojis (breaks xelatex PDF export).

## Step 4: Stage updated module notes

Run `git add <note_path>` for each module note that was modified in Step 3.

**Keep track of the list of updated modules** -- this feeds into Part 2 for the weekly bullets.

---

# Part 2: Update Weekly Task Note

## Step 5: Find the weekly note

The weekly task note lives at `notes/user.mjvolk3.swanki.tasks.weekly.YYYY.WW.md` where `WW` is the ISO week number. Find the current one by globbing `notes/user.mjvolk3.swanki.tasks.weekly.2026.*.md`.

### Worktree Detection

**If the working directory path contains `.worktrees/`**, you are in a git worktree. Worktrees write to a **child note** of the main weekly note to avoid merge conflicts.

**Detection steps:**

1. Check if `pwd` contains `.worktrees/`. If not, use the main weekly note as normal.
2. If in a worktree, find the worktree-specific child note:
   - Read the main weekly note
   - Search for a line containing the worktree branch name (from `git branch --show-current`) and a `[[...]]` dendron link
   - Extract the linked dendron path -- that is the target note for all updates
3. If no matching line exists in the main weekly, inform the user and stop.

## Step 6: Add weekly entries

1. **Read the current weekly note** to understand existing tasks and structure.
2. **Find today's date section** (`## YYYY.MM.DD`). Create it if it doesn't exist (append below the last dated section -- chronological order, newer at bottom).
3. **For each module updated in Part 1**, add a one-line bullet entry:
   - The one-sentence description is the most important part. It should tell the reader the point of the work without having to open the linked note.
   - Link to the relevant note using dendron wiki-link syntax: `[[dendron.path]]` (no aliases)
   - Do not duplicate entries that already exist for the same module under today's date

### Section Anchor Links

When a module note has multiple dated sections, link to the specific section rather than the whole note. Dendron anchor syntax: `[[note.path#anchor-slug]]`.

**CRITICAL: Always verify the H2 header exists before computing an anchor.**

Step 1 -- list actual H2 headers in the target note:

```bash
grep -n "^## " notes/swanki.some_module.md
```

Only use headers that appear in that output.

Step 2 -- compute the anchor from the exact header text using the Python one-liner:

```bash
python3 -c "import re,sys; h=sys.argv[1]; t=re.sub(r'^#+\s*','',h).lower(); t=re.sub(r'[^\w\s-]','',t); print(t.replace(' ','-'))" "## 2026.02.15 - Brief Title Here"
```

### Task Entry Format

```markdown
- [x] One-sentence explainer of completed work [[dendron.path.to.note]]
- [ ] One-sentence explainer of pending task [[dendron.path.to.note]]
```

## Step 7: Format validation and task reordering

Before staging the weekly note, scan the entire file for format violations and reorder tasks.

**Task reordering (mandatory):**

Within each date section (`## YYYY.MM.DD`), sort bullets so completed tasks (`- [x]`) appear **above** pending tasks (`- [ ]`). Preserve relative order within each group (completed items keep their original order among themselves, same for pending items). This applies every time the weekly note is touched -- not just when marking tasks done.

**Check for and fix:**

- H3 or deeper headings (`###`, `####`) under date sections -- flatten into bullets
- Horizontal rules (`***`, `---` used as separators, not frontmatter) -- remove
- Prose paragraphs between bullets -- condense into bullet items
- Nested sub-lists -- flatten to one level
- Date headers that aren't `YYYY.MM.DD` format -- replace with actual date
- `#future` tags placed inline in H2 headers -- move to own line below heading
- Multi-sentence bullets -- condense to one sentence with dendron link for details

## Step 8: Stage weekly note

Run `git add <weekly-note-path>`.

---

# Part 3: Combined Summary

## Step 9: Print summary

```
Source: staged files (or: modified files -- nothing was staged)

Created notes:
  - swanki.audio.card (new)

Updated source notes:
  - swanki.config (added 2026.03.19 section)
  - swanki.audio.tts (updated existing 2026.03.19 section)

Updated weekly note:
  - Added 2 entries under ## 2026.03.19

All notes staged. Run /stage -> /commit to finalize.
```

---

## Important Rules

- Create missing dendron notes with `dendron-cli note write` -- never with the Write tool.
- NEVER modify dendron YAML frontmatter (the `---` block at the top of notes).
- NEVER remove or rewrite existing dated sections -- only append to them or add new ones.
- Preserve the existing style and structure of each note.
- No Unicode emojis in any markdown content.
- Do NOT ask extra approval questions -- tool approval prompts are the gates.

## Example Invocations

- `/update-notes` -- auto-discover: staged files first, then modified files. Updates both module notes and weekly.
- `/update-notes swanki/config.py` -- update module note for config.py, then add weekly entry
- `/update-notes scripts/setup-worktree.sh` -- update a bash script note + weekly entry
- `/update-notes swanki/config.py swanki/audio/card.py` -- update multiple files + weekly
- "update notes for changed files"
