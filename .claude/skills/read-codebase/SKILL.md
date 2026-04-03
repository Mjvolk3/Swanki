---
name: read-codebase
description: Load source files (Python, Bash) and their paired dendron notes into context. Reads source + note together so code and its design history are adjacent. Covers swanki/, scripts/, and tests/. Supports module prefix filtering.
---

# Read Codebase + Notes

Load source files and their paired dendron notes into context. Each source file is read immediately followed by its dendron note, so the code and its design rationale are adjacent in context.

Covers these source directories:
- `swanki/` -- main Python package
- `scripts/` -- project shell scripts
- `tests/` -- test files

## Arguments

- **No arguments**: load the full codebase (all directories) and all paired notes
- **Module prefix** (e.g., `/read-codebase audio` or `/read-codebase anki`): load only files under `swanki/<prefix>/`
- **`scripts`**: load only `scripts/*.sh` and `scripts/*.py` with their paired notes
- **Multiple prefixes** (e.g., `/read-codebase audio anki`): load files under each prefix
- **`with-tests`**: also read the paired test file for each source file (default: on when filtering, off for full codebase)
- **`no-tests`**: skip test files even when filtering
- **`notes-only`**: read only the dendron notes (skip source files). Useful for reviewing design history.
- **`with-config`**: also read config files (pyproject.toml, CI workflows, etc.)

## Step 1: Determine scope

Based on arguments, build the list of source file glob patterns:

### Python package (swanki/)

| Argument           | Glob pattern                     |
|--------------------|----------------------------------|
| *(none)*           | `swanki/**/*.py`                 |
| `audio`            | `swanki/audio/**/*.py`           |
| `anki`             | `swanki/anki/**/*.py`            |
| `config`           | `swanki/config.py`               |
| Any other prefix   | `swanki/<prefix>/**/*.py` or `swanki/<prefix>.py` |

Also always include root-level modules when loading the full codebase:
- `swanki/__init__.py`
- `swanki/__main__.py`
- `swanki/config.py`
- Other root-level `.py` files

### Project scripts (scripts/)

When loading the full codebase (no arguments) or when `scripts` is an explicit argument:
- `scripts/*.sh`
- `scripts/*.py`

## Step 2: Glob for source files

Use the Glob tool to find all matching Python files. Exclude `__pycache__`, `.egg-info`, and worktree directories.

## Step 3: Compute paired file paths

For each source file, derive:

1. **Dendron note path**: convert path separators to dots, drop the file extension, prepend `notes/`, append `.md`.

   | Source file                  | Dendron note                       |
   |------------------------------|------------------------------------|
   | `swanki/audio/card.py`       | `notes/swanki.audio.card.md`       |
   | `swanki/config.py`           | `notes/swanki.config.md`           |
   | `scripts/setup-worktree.sh`  | `notes/scripts.setup-worktree.md`  |

2. **Test file path** (when `with-tests`): mirror the source path under `tests/` with `test_` prefix on the filename.
   - `swanki/audio/card.py` -> `tests/swanki/audio/test_card.py` or `tests/test_audio_card.py`

## Step 4: Read files in grouped batches

Read files in **parallel batches** (maximize parallel Read calls). Within each batch, group by module -- source file first, then its note, then its test file.

**Reading order per module:**
1. Source file (`swanki/audio/card.py`)
2. Paired dendron note (`notes/swanki.audio.card.md`) -- skip silently if it does not exist
3. Paired test file -- only if `with-tests`, skip silently if it does not exist

**Batch strategy:**
- Read up to 8 files in parallel per batch
- Process in order: root modules first, then subpackages alphabetically, then scripts
- Within each group, alphabetical order

**If `notes-only`:** skip source and test files, only read dendron notes that exist.

## Step 5: Read config files (if `with-config`)

When `with-config` is specified, also read:
- `pyproject.toml`
- `.pre-commit-config.yaml`
- `.github/workflows/*.yml`

## Step 6: Print summary

After all reads complete, print a compact summary:

```
Loaded N source files, M dendron notes, K test files
  Package: swanki/ (X files)
  Scripts: scripts/ (Y files)
  Notes:   notes/*.md (M files, P missing)
  Tests:   tests/ (K files, skipped | included)
  Config:  pyproject.toml, ... (if with-config)
```

Report any source files that lack a paired dendron note (these are candidates for `/update-notes`).

## Important Rules

- Read source + note together (adjacent in context) so the "what" and "why" are paired
- Skip silently when a note or test file does not exist -- do NOT error
- When loading the full codebase without `with-tests`, skip test files to conserve context
- When filtering to a subpackage, include tests by default (smaller scope, tests are more relevant)
- Use parallel Read calls aggressively -- 8+ files per batch
- Do NOT read files under `docs/_build/`, `*.egg-info/`, `__pycache__/`, or `.worktrees/`
- Do NOT ask extra approval questions -- tool approval prompts are the gates

## Example Invocations

- `/read-codebase` -- full codebase (package + scripts) + all paired notes (no tests)
- `/read-codebase audio` -- audio subpackage + notes + tests
- `/read-codebase audio anki` -- two subpackages + notes + tests
- `/read-codebase scripts` -- just scripts + paired notes
- `/read-codebase notes-only` -- just the dendron notes (design history review)
- `/read-codebase with-config` -- full codebase + notes + config files
- `/read-codebase audio no-tests` -- audio source + notes, skip tests
