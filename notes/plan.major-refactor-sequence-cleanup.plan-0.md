---
id: thkvv3m6kiriqmq7gz0jhzo
title: Plan 0
desc: ''
updated: 1773323828273
created: 1773323173835
---
Pre-API Hardening Plan for `major-refactor`

## Context

The 5-step major refactor is functionally complete (audio decoupling, config, segmentation, lecture transcripts, pydantic-ai migration). Before spending money on real LLM API calls, we need to catch as many issues as possible with static analysis, type checking, and unit tests. The goal is zero surprises when we first hit the API.

**Current state:** 92 tests pass, 2 test files are broken (scaffold + removed method), ruff has 490 errors (mostly legacy), `ImageSummary` model silently drops `alt_text`/`context` fields, and `__init__.py` eagerly imports 16 legacy functions pulling in old OpenAI deps.

---

## Step 1: Green test suite — fix broken tests

Delete `tests/test_first_module.py` (scaffold importing nonexistent `my_package`).

Delete `tests/test_anki_processor_tables.py` — all 4 tests call `_parse_cards_from_markdown` which no longer exists on `AnkiProcessor`. The table conversion functionality these tested may be re-covered later; for now they are dead code producing false failures.

**Verify:** `pytest tests/ -x` → all green (92 pass today + 0 broken).

**Files:**

- `tests/test_first_module.py` — delete
- `tests/test_anki_processor_tables.py` — delete

---

## Step 2: Ruff auto-fix + format

Run `ruff check --fix swanki/ tests/` then `ruff format swanki/ tests/`. This clears ~370 of 490 errors (import sorting, type annotation modernization, docstring colons).

Then manually fix the ~28 remaining errors in **modern modules only** (skip `legacy/`):

- `D100`/`D104`: Add missing module/package docstrings to `__version__.py`, `__init__.py` files
- `UP035`: Change `from typing import List, Dict, Optional` → `list`, `dict`, `| None` in `swanki/models/document.py` and similar
- `D301`: Add raw string prefix to docstrings with escape sequences

**Skip:** All ~92 remaining errors in `swanki/legacy/` — not in the active pipeline path.

**Verify:** `ruff check swanki/ --exclude legacy/ tests/` → 0 errors.

**Files:**

- All `swanki/**/*.py` (auto-fix)
- `swanki/models/document.py`, `swanki/models/cards.py` — manual UP035 fixes
- `swanki/__version__.py` — add module docstring

---

## Step 3: Fix `ImageSummary` silent data loss

`pipeline.py:579-605` passes `alt_text=` and `context=` to `ImageSummary(...)`, but the model has no such fields. Pydantic v2 silently ignores them → data lost.

**Fix:** Add the missing fields to `ImageSummary` in `swanki/models/document.py`:

```python
alt_text: str = Field("", description="Alt text for the image")
context: str = Field("", description="Surrounding text context")
```

Also add `model_config = ConfigDict(extra="forbid")` to all Pydantic output models (`ImageSummary`, `DocumentSummary`, `CardGenerationResponse`, `CardFeedback`, `AudioTranscriptFeedback`, `LectureTranscriptFeedback`). This turns future silent drops into immediate errors.

**Verify:** `pytest tests/ -x` still green; no `extra="forbid"` violations.

**Files:**

- `swanki/models/document.py` — add fields + `extra="forbid"`
- `swanki/models/cards.py` — add `extra="forbid"`
- `swanki/models/audio.py` — add `extra="forbid"`

---

## Step 4: Clean up `swanki/__init__.py` legacy imports

Remove all 16 legacy re-exports. Keep only `Pipeline`. Anyone using legacy code can import from `swanki.legacy.*` directly.

This eliminates eager imports of `openai`, `tiktoken`, and other heavy legacy deps on every `import swanki`.

**Files:**

- `swanki/__init__.py`

---

## Step 5: Tighten mypy on modern modules

Current `pyproject.toml` disables 11 error codes for `swanki.audio.*`, `swanki.pipeline.*`, `swanki.models.*`. Re-enable the three most dangerous ones that cause runtime crashes:

- `attr-defined` — accessing nonexistent attributes
- `call-arg` — wrong arguments to functions
- `arg-type` — wrong types passed

Fix the actual type errors that surface. Leave `no-any-return`, `type-arg`, `no-untyped-def` suppressed for now.

**Do NOT touch** `swanki/legacy/` mypy config.

**Verify:** `mypy swanki/ --exclude legacy` with tightened config → 0 errors on re-enabled codes.

**Files:**

- `pyproject.toml` — narrow mypy overrides
- Various files in `swanki/audio/`, `swanki/pipeline/`, `swanki/models/` — fix type annotations

---

## Step 6: Add targeted unit tests for API-adjacent code

Write tests that verify wiring between config → agents → pipeline WITHOUT calling APIs:

1. **`tests/test_agents.py` (new):** Test `get_model_string()` with default config, anthropic config, missing keys, edge cases. Verify agent `run_sync` receives correct kwargs by mocking.

2. **`tests/test_models_validation.py` (new):** Round-trip test for each output model — construct valid instance, serialize, deserialize. Tests field constraints (summary word count validators, `max_length=5` on contributions) to catch validation failures before they waste API tokens.

3. **`tests/test_config_resolution.py` (new):** Hydra composition smoke test — load `default.yaml` and `anthropic.yaml`, verify `models.llm.provider` and `models.llm.model` resolve correctly.

4. **Extend `tests/test_pipeline_mode.py`:** Add a test that verifies `get_model_string` is called and config values propagate into agent calls during `process_full()`.

**Files:**

- `tests/test_agents.py` — new
- `tests/test_models_validation.py` — new
- `tests/test_config_resolution.py` — new
- `tests/test_pipeline_mode.py` — extend

---

## Step 7: Minimal `@pytest.mark.llm` smoke test

Create a single cheap API test that validates the full chain:

- Use a 1-page test PDF fixture (or pre-baked minimal markdown)
- `audio=none` (skip ElevenLabs costs)
- `cards_per_segment=1`, `cloze_per_segment=0`
- Assert outputs dict has expected keys and files exist
- Cost: ~1-2 API calls, < $0.10

Mark with `@pytest.mark.llm` so it's skipped by default, run explicitly with `pytest --llm`.

**Files:**

- `tests/fixtures/` — new directory with minimal test PDF
- `tests/test_smoke_llm.py` — new

---

## What to skip

- **Legacy code cleanup** (31 files, 250 ruff errors) — not in active pipeline path
- **`requires-python` fix** (`>=3.13` vs actual 3.11) — cosmetic, not blocking
- **Rewriting try/except blocks** — existing ones in `pipeline.py` are at external boundaries (API calls, file I/O), arguably appropriate. Flag but don't rewrite pre-testing.
- **Full mypy strict compliance** — diminishing returns; focus on the 3 most dangerous error codes

---

## Verification (end-to-end)

After all steps:

1. `ruff check swanki/ --exclude legacy/ tests/` → 0 errors
2. `ruff format --check swanki/ tests/` → no changes needed
3. `mypy swanki/ --exclude legacy` → 0 errors on re-enabled codes
4. `pytest tests/ -x` → all green (unit tests)
5. `pytest tests/ -x --llm` → smoke test passes (1 real API call)
