## Dendron Paths

Example:
[[Paper|Paper]] exists here `/Swanki/notes/Paper.md`

Example

![](./assets/images/fix_cloze.md.issue-with-cloze-card-no-data-in-extra.png) exists here `Swanki/notes/assets/images/fix_cloze.md.issue-with-cloze-card-no-data-in-extra.png`

## Coding Advice

- Don't be superfluous
- Don't use try except blocks - fail fast minimize other types of exception coding like by using excessive conditionals

## Python File Format

Every `.py` file starts with a single frontmatter docstring. The module description (if any) goes in the same block -- never a separate docstring.

```python
"""
swanki/audio/card.py
[[swanki.audio.card]]
https://github.com/Mjvolk3/Swanki/tree/main/swanki/audio/card.py
Test file: tests/test_audio_card.py

Flashcard audio generation with cloze handling and citation prefixing.
"""
```

Use **Google-style docstrings** for functions and classes (`Args:`, `Returns:`, `Raises:`). Ruff enforces `convention = "google"`. Keep docstrings concise -- no verbose parameter descriptions that duplicate type annotations. Pydantic models use `Field(description="...")` instead of docstrings for fields.

## Pydantic Models

- We want to use pydantic models to structure output as much as possible as opposed to controlling output by changing prompts.

## Files

- Tests should go in `tests/`

## Code Execution

- ~/opt/miniconda3/envs/swanki/bin/Swanki python script.py

## Weekly Notes

- When checking off a task in the weekly note, always add a one-sentence summary before the `[[link]]`. Never leave a checked item as just a bare link.

## Git Worktrees

We develop on multiple branches simultaneously using git worktrees. Each worktree lives at `~/projects/Swanki.worktrees/<branch>/` alongside the main repo at `~/projects/Swanki/`. Active worktrees and their tasks are tracked in weekly notes (e.g., `notes/user.mjvolk3.swanki.tasks.weekly.2026.10.md`).

**Shared data.** `SWANKI_DATA` points to the sibling `Swanki_Data/` directory and is the same across all worktrees (no per-worktree copy needed). Only repo-internal paths (`WORKSPACE_DIR`, `ASSET_IMAGES_DIR`) get rewritten by the setup script.

**Shared auto memory.** `scripts/setup-worktree.sh` symlinks each worktree's Claude Code auto memory directory to the main repo's memory directory (`~/.claude/projects/.../memory/`). This means all worktrees and the main repo read and write the same `MEMORY.md` and topic files. When writing to auto memory, be aware that another Claude Code agent in a different worktree may be doing the same -- keep writes additive, don't overwrite entire files, and use topic-specific files to reduce conflicts.

**Concurrent agents.** Multiple Claude Code sessions may be active across worktrees at the same time, each working on a different branch/feature. Do not assume you are the only agent running. This is especially relevant for auto memory writes and any shared resources.

### Worktree Merge Workflow

When a worktree branch is ready to land:

1. **Single branch:** rebase onto main, push, open PR, merge, then clean up.
2. **Batch (multiple independent branches):** merge sequentially -- rebase first branch onto main, merge its PR, update main, rebase next branch, repeat. Each feature gets its own clean merge with linear history. Do NOT use integration branches.

After merging:

```bash
git worktree remove --force ~/projects/Swanki.worktrees/<branch>
git branch -d <branch>
gh api repos/Mjvolk3/Swanki/git/refs/heads/<branch> --method DELETE
```

**Weekly note conflicts:** `.gitattributes` sets `merge=union` on `notes/user.mjvolk3.swanki.tasks.weekly.*.md`, so git automatically keeps lines from both sides. No manual resolution needed for this file.

**Other conflict files** (e.g. `__init__.py`): resolve manually -- all additions are additive, so keep both sides.

## Finding Rationale for Changes

To understand why a code change was made, check the dendron module note (`notes/swanki.<module>.md`). Each dated section documents what changed and why. This is the primary source of decision history for the codebase.

## Change Log

- This is automatically updated. Don't edit it directly.
