---
id: z5gciijdddthexkwing8l7d
title: Plan 0
desc: ''
updated: 1772073048734
created: 1772073048734
---

## Adapt iBioFoundry-AI Skills, Scripts, and VS Code Tasks to Swanki

### Overview

Port the following from iBioFoundry-AI to Swanki:

**Skills (dendron/notes workflow)**:

1. **`update-py-notes`** -- update dendron module notes for changed Python files
2. **`update-tasks-weekly`** -- update weekly task note with progress
3. **`pdf`** -- generate PDF from markdown note via pandoc
4. **`save-plan`** -- copy Claude Code plan into a Dendron note

**Skills (git workflow)**:

5. **`stage`** -- smart staging with auto-detected file blocks
6. **`commit`** -- commit staged changes with auto-generated bulleted message

**Skills (code quality)**:

7. **`ruff`** -- run ruff linter on staged/specified Python files (adapted for swanki env)

**Skills (utilities)**:

8. **`dendron-tree`** -- show dendron note hierarchy as a visual tree
9. **`gh-issue`** -- create GitHub issue from a dendron note

**Publish scripts and assets**:

10. **`export_pod_md.sh`** -- resolve `![[note]]` transclusions (not built into Dendron for local use)
11. **`bib_tex_pdf.sh`** -- update Swanki's version to match iBioFoundry-AI improvements (Lua filter, mermaid temp dir, SCRIPT_DIR-relative paths)
12. **`break-long-code.lua`** -- Lua filter for code block line wrapping

**VS Code tasks**:

13. **`Dendron: export pod md`** and **`Dendron: export pod md + pdf`**
14. **`dendron: tree`**

**Scripts**:

15. **`scripts/dendron-tree.sh`** -- backing script for dendron-tree skill and VS Code task

---

### Task 1: Create `.claude/skills/` directory structure

Swanki currently uses `.claude/commands/` (old format). Create the new skills directory:

```
.claude/skills/
  update-py-notes/SKILL.md
  update-tasks-weekly/SKILL.md
  pdf/SKILL.md
```

Existing `.claude/commands/` files (clean_pdf.md, etc.) can stay -- Claude Code supports both.

---

### Task 2: Adapt `update-py-notes` skill

**Source**: `iBioFoundry-AI/.claude/skills/update-py-notes/SKILL.md`

**Adaptations needed**:

- Change package name references: `ibiofoundry_ai/` -> `swanki/`
- Dendron note path mapping: `swanki/processing/pdf_processor.py` -> `notes/swanki.processing.pdf_processor.md`
- Same workflow: staged files -> modified files fallback
- Same writing guidelines (intentional stance, no emojis)
- `dendron-cli note write` for creating missing notes (same)
- `git add` for staging (same)

**No new scripts needed** -- this skill only uses git, dendron-cli, and Claude's Edit tool.

---

### Task 3: Adapt `update-tasks-weekly` skill

**Source**: `iBioFoundry-AI/.claude/skills/update-tasks-weekly/SKILL.md`

**Adaptations needed**:

- Weekly note path: `notes/user.Mjvolk3.iBioFoundry-AI.tasks.weekly.YYYY.WW.md` -> `notes/user.mjvolk3.swanki.tasks.weekly.YYYY.WW.md`
- Glob pattern for discovery: `notes/user.mjvolk3.swanki.tasks.weekly.2026.*.md`
- Linking rules: `[[swanki.module_name]]` instead of `[[ibiofoundry_ai.module_name]]`
- Remove worktree detection section (Swanki doesn't use worktrees currently)
- Remove Slack notification section (not used in Swanki)
- Keep: section anchor computation, date format, entry format, files-to-skip rules

**No new scripts needed**.

---

### Task 4: Adapt `pdf` skill

**Source**: `iBioFoundry-AI/.claude/skills/pdf/SKILL.md`

**Adaptations needed**:

- Script path: `notes/assets/publish/scripts/bib_tex_pdf.sh` (already exists in Swanki)
- Usage is identical: `bash notes/assets/publish/scripts/bib_tex_pdf.sh <input> . <output>`
- Same notes about mermaid-filter, emoji warnings, 120s timeout

**Minimal changes** -- mostly just copy the skill file.

---

### Task 5: Update `bib_tex_pdf.sh` in Swanki

**Source**: `iBioFoundry-AI/notes/assets/publish/scripts/bib_tex_pdf.sh`
**Target**: `Swanki/notes/assets/publish/scripts/bib_tex_pdf.sh`

The iBioFoundry-AI version has improvements over Swanki's current version:

- Uses `SCRIPT_DIR` to compute `NOTES_DIR` (more robust than `cd ./notes`)
- Creates mermaid temp directory for diagram images
- Sets Puppeteer config for headless Chrome
- Includes the Lua filter `-L assets/publish/filters/break-long-code.lua`
- Has `pdf_subdir` parameter (4th arg, defaults to `pdf-output`)
- Cleans up mermaid temp dir after

**Action**: Replace Swanki's `bib_tex_pdf.sh` with iBioFoundry-AI's version.

---

### Task 6: Copy `break-long-code.lua` filter

**Source**: `iBioFoundry-AI/notes/assets/publish/filters/break-long-code.lua`
**Target**: `Swanki/notes/assets/publish/filters/break-long-code.lua`

New file. Create `notes/assets/publish/filters/` directory and copy the Lua filter.

---

### Task 7: Copy `export_pod_md.sh` script

**Source**: `iBioFoundry-AI/notes/assets/publish/scripts/export_pod_md.sh`
**Target**: `Swanki/notes/assets/publish/scripts/export_pod_md.sh`

New file in Swanki. This script resolves `![[note]]` transclusions into flat markdown. It uses `SCRIPT_DIR` to find `NOTES_DIR` so it works without modification.

Also create the output directory: `notes/assets/export-pod-md/` (the script creates it via `mkdir -p` but good to have).

---

### Task 8: Add VS Code tasks for export pod

**Target**: `Swanki/swanki.code-workspace` tasks section

Add two new tasks:

```jsonc
{
    "label": "Dendron: export pod md",
    "type": "shell",
    "command": "bash ./notes/assets/publish/scripts/export_pod_md.sh ${file}",
    "problemMatcher": []
},
{
    "label": "Dendron: export pod md + pdf",
    "type": "shell",
    "command": "bash ./notes/assets/publish/scripts/export_pod_md.sh ${file} && ./notes/assets/publish/scripts/bib_tex_pdf.sh ./notes/assets/export-pod-md/${fileBasename} ./notes/assets/export-pod-md ${fileBasenameNoExtension} pdf-pod-output",
    "problemMatcher": []
}
```

These go in the `// Publish` section alongside the existing pandoc tasks.

Also create `notes/assets/pdf-pod-output/` directory for the combined export+pdf output.

---

### Task 9: Update `header-includes.tex` (optional)

**Source**: `iBioFoundry-AI/notes/assets/publish/tex-templates/header-includes.tex`
**Target**: `Swanki/notes/assets/publish/tex-templates/header-includes.tex`

The iBioFoundry-AI version adds:

- DejaVu Sans Mono for code blocks (Unicode box-drawing support)
- `fvextra` for line wrapping in code blocks
- Redirect `\begin{verbatim}` to fvextra's Verbatim
- Tone down red "alert/error" tokens from pandoc syntax highlighting

Compare Swanki's current version and update if it's missing these.

---

### Task 10: Adapt `stage` skill

**Source**: `iBioFoundry-AI/.claude/skills/stage/SKILL.md`

**Adaptations needed**:

- Change "Commit Trio" references: `ibiofoundry_ai/` -> `swanki/`
- Weekly note path: `notes/user.mjvolk3.swanki.tasks.weekly.*.md`
- Pre-stage reminders: reference `/update-py-notes` and `/mypy` (same tools apply)
- Remove docs update reminder (Swanki doesn't have Sphinx docs currently)
- Keep: block detection rules, multiSelect UX, `git add` explicit paths, never `git add -A`

**No new scripts needed**.

---

### Task 11: Adapt `commit` skill

**Source**: `iBioFoundry-AI/.claude/skills/commit/SKILL.md`

**Adaptations needed**:

- Remove Step 1.5 (Sphinx docs update) -- Swanki doesn't have this
- Remove `update-docs` skill reference
- Keep: check staged, match commit style from `git log`, bulleted message format, Co-Authored-By line, never amend, never skip hooks

**No new scripts needed**.

---

### Task 12: Adapt `ruff` skill

**Source**: `iBioFoundry-AI/.claude/skills/ruff/SKILL.md`

**Adaptations needed**:

- Python env path: `~/miniconda3/envs/ibf/bin/python` -> `/Users/michaelvolk/opt/miniconda3/envs/swanki/bin/python`
- Package name: `ibiofoundry_ai/` -> `swanki/`
- Per-file ignores: adapt to Swanki's `pyproject.toml` ruff config (read it during execution)
- Docstring frontmatter pattern: update GitHub URL to Swanki repo
- Keep: workflow order, auto-fix strategy, stage fixed files

**No new scripts needed**. Check `Swanki/pyproject.toml` for existing ruff config.

---

### Task 13: Adapt `save-plan` skill

**Source**: `iBioFoundry-AI/.claude/skills/save-plan/SKILL.md`

**Adaptations needed**:

- Example dendron paths: `ibiofoundry_ai.tools.python_exec.plan-0` -> `swanki.processing.image_processor.plan-0`
- Everything else is generic (reads `.claude/plans/`, uses `dendron-cli note write`, `git add`)

**No new scripts needed**.

---

### Task 14: Adapt `dendron-tree` skill and copy backing script

**Source skill**: `iBioFoundry-AI/.claude/skills/dendron-tree/SKILL.md`
**Source script**: `iBioFoundry-AI/scripts/dendron-tree.sh`

**Target skill**: `Swanki/.claude/skills/dendron-tree/SKILL.md`
**Target script**: `Swanki/scripts/dendron-tree.sh`

The script is generic (uses `notes/*.md` glob, no project-specific paths). Copy as-is.

The skill just calls `bash scripts/dendron-tree.sh $ARGUMENTS`. Copy as-is.

Create `Swanki/scripts/` directory if it doesn't exist.

---

### Task 15: Adapt `gh-issue` skill

**Source**: `iBioFoundry-AI/.claude/skills/gh-issue/SKILL.md`

**Adaptations needed**:

- Default repo target: `iBioFoundry/iBioFoundry-AI` -> appropriate Swanki repo (check `git remote -v`)
- Example invocations: update dendron note paths
- Keep: all formatting conventions, workflow, temp file preview, label inference

**No new scripts needed**.

---

### Task 16: Add VS Code task for `dendron: tree`

**Target**: `Swanki/swanki.code-workspace` tasks section

Add:

```jsonc
{
    "label": "dendron: tree",
    "type": "shell",
    "command": "bash scripts/dendron-tree.sh -L ${input:dendronTreeDepth}",
    "problemMatcher": []
}
```

Also add the `dendronTreeDepth` input (pickString 1-5) to the inputs array.

---

### Summary of files to create/modify

**New files to CREATE**:

| File                                            | Source                       |
| ----------------------------------------------- | ---------------------------- |
| `.claude/skills/update-py-notes/SKILL.md`       | Adapted from iBioFoundry-AI  |
| `.claude/skills/update-tasks-weekly/SKILL.md`   | Adapted from iBioFoundry-AI  |
| `.claude/skills/pdf/SKILL.md`                   | Adapted from iBioFoundry-AI  |
| `.claude/skills/save-plan/SKILL.md`             | Adapted from iBioFoundry-AI  |
| `.claude/skills/stage/SKILL.md`                 | Adapted from iBioFoundry-AI  |
| `.claude/skills/commit/SKILL.md`                | Adapted from iBioFoundry-AI  |
| `.claude/skills/ruff/SKILL.md`                  | Adapted from iBioFoundry-AI  |
| `.claude/skills/dendron-tree/SKILL.md`          | Copied from iBioFoundry-AI   |
| `.claude/skills/gh-issue/SKILL.md`              | Adapted from iBioFoundry-AI  |
| `notes/assets/publish/scripts/export_pod_md.sh` | Copied from iBioFoundry-AI   |
| `notes/assets/publish/filters/break-long-code.lua` | Copied from iBioFoundry-AI |
| `scripts/dendron-tree.sh`                       | Copied from iBioFoundry-AI   |

**Existing files to MODIFY**:

| File                                                | Change                                 |
| --------------------------------------------------- | -------------------------------------- |
| `notes/assets/publish/scripts/bib_tex_pdf.sh`      | Replace with iBioFoundry-AI version    |
| `notes/assets/publish/tex-templates/header-includes.tex` | Update with new LaTeX packages    |
| `swanki.code-workspace`                             | Add export pod + dendron tree tasks    |

**Directories to CREATE**:

- `.claude/skills/update-py-notes/`
- `.claude/skills/update-tasks-weekly/`
- `.claude/skills/pdf/`
- `.claude/skills/save-plan/`
- `.claude/skills/stage/`
- `.claude/skills/commit/`
- `.claude/skills/ruff/`
- `.claude/skills/dendron-tree/`
- `.claude/skills/gh-issue/`
- `notes/assets/publish/filters/`
- `notes/assets/export-pod-md/`
- `notes/assets/pdf-pod-output/`
- `scripts/`

---

### Execution order

**Phase 1: Publish infrastructure (no deps)**

1. Task 6: Copy `break-long-code.lua`
2. Task 7: Copy `export_pod_md.sh`
3. Task 9: Update `header-includes.tex`
4. Task 14 (script part): Copy `scripts/dendron-tree.sh`

**Phase 2: Update existing scripts (depends on Phase 1)**

5. Task 5: Update `bib_tex_pdf.sh` (depends on lua filter from Task 6)

**Phase 3: Skills (can all be done in parallel)**

6. Task 2: `update-py-notes` skill
7. Task 3: `update-tasks-weekly` skill
8. Task 4: `pdf` skill
9. Task 10: `stage` skill
10. Task 11: `commit` skill
11. Task 12: `ruff` skill
12. Task 13: `save-plan` skill
13. Task 14 (skill part): `dendron-tree` skill
14. Task 15: `gh-issue` skill

**Phase 4: VS Code workspace (depends on Phases 1-2)**

15. Task 8: Add export pod tasks to workspace
16. Task 16: Add dendron tree task to workspace

**Phase 5: Verify**

17. Task 1: Verify directory structure and all files created
