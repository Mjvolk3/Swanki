---
name: mypy
description: Run mypy on staged or specified Python files and fix errors following the project's type-checking strategy.
---

# Mypy Fixer

Run mypy in strict mode on staged or specified Python files, then fix errors following the project's type-checking strategy.

## Workflow

```
(edit python) -> /mypy -> /update-py-notes -> /commit
```

## Arguments

- **With arguments** (e.g., `/mypy swanki/config.py`): run mypy on the specified files only.
- **No arguments**: run mypy on all staged `.py` files under `swanki/`. If nothing is staged, run on the entire `swanki/` directory.

## Step 1: Determine target files

- **If arguments provided**: use the listed file paths directly.
- **If no arguments**: run `git diff --cached --name-only -- 'swanki/*.py'` to get staged `.py` files. If none, target `swanki/` as a whole.

## Step 2: Run mypy

```bash
/Users/michaelvolk/miniconda3/bin/python -m mypy --strict --show-error-codes <files_or_dir>
```

If mypy passes clean, inform the user and stop.

## Step 3: Fix errors by type

For each error, apply the appropriate strategy:

### `[import-untyped]` and `[import-not-found]`

1. Check if a `types-{package}` stub package exists (e.g., `types-requests` for `requests`).
2. If stubs exist: add the package to dev dependencies and install it.
3. If no stubs exist: add `# type: ignore[import-untyped]` to the specific import line.
4. Never set `ignore_missing_imports = true` globally or per-module in `pyproject.toml`.

### `[no-untyped-def]`

Add return type annotations to the function. Use `-> None` for functions that don't return, specific types otherwise.

### `[union-attr]` and `[attr-defined]`

Add `assert x is not None` guards or `if x is not None:` checks before the attribute access. Prefer assertions for values that must not be None at that point in the logic. Prefer conditionals when None is a valid state that needs handling.

### `[type-arg]`

Add explicit type parameters to generic types (e.g., `dict[str, Any]` instead of bare `dict`).

### `[arg-type]`

Fix argument type mismatches by casting, narrowing, or correcting the call.

### `[untyped-decorator]`

For framework decorators that mypy cannot type, add `# type: ignore[misc]` with a comment explaining why (framework limitation). For custom decorators, add proper type annotations.

### All other errors

Fix the code. Never add blanket `# type: ignore` without a specific error code. Only ignore known mypy false positives (with the specific error code).

## Step 4: Re-run mypy

Run mypy again to verify all fixes. If new errors appear, fix them. Repeat until clean.

## Step 5: Stage fixed files

Run `git add <fixed_files>` for all files that were modified during fixing.

## Important Rules

- NEVER set `ignore_missing_imports = true` globally or per-module
- NEVER add bare `# type: ignore` without a specific error code
- Always prefer installing typed stubs over ignoring import errors
- Per-line `# type: ignore[error-code]` for untyped third-party imports only when no stubs exist
- Strict mode globally for source code under `swanki/`
- Do NOT ask extra approval questions -- tool approval prompts are the gates

## Example Invocations

- `/mypy` -- check all staged Python files (or entire swanki/)
- `/mypy swanki/config.py` -- check a specific file
- `/mypy swanki/processing/pdf_processor.py swanki/models/cards.py` -- check multiple files
- "run mypy on the processing module"
- "fix type errors in pipeline.py"
