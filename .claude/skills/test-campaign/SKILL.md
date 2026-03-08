---
name: test-campaign
description: Run a test coverage campaign — baseline coverage, identify gaps, write meaningful tests, verify improvement, write a dated report. Accepts optional target files/modules; defaults to open-ended full-codebase campaign.
---

# Test Campaign

Drive a focused test coverage campaign: baseline, gap analysis, test writing, verification, and a dated report.

## Workflow

```
/test-campaign [targets] -> baseline coverage -> gap analysis -> write tests -> update dendron notes -> final coverage -> write report -> stage
```

## Arguments

- **No args**: Open-ended campaign. Analyze full `swanki/` codebase, prioritize modules by coverage gap (lowest first).
- **With file/module args** (e.g., `/test-campaign swanki/processing/pdf_processor.py swanki/models/cards.py`): Targeted campaign — coverage still runs for the full package, but test writing is scoped to the specified modules.
- **With prose args** (e.g., `/test-campaign "focus on card generation and PDF processing"`): Interpret intent and scope accordingly.

## Step 1: Baseline Coverage

Run unit tests with coverage (excludes integration/llm markers by default):

```bash
/Users/michaelvolk/miniconda3/bin/python -m pytest tests/ --cov=swanki --cov-report=term-missing -q -m "not llm and not integration"
```

Parse output to build a coverage table: module, statements, missing lines, branch %, overall %. Record **baseline total %** for the report.

## Step 2: Identify Gaps

Build a prioritized gap list sorted by coverage % ascending (0% first).

**Deprioritize or skip** (document why in report):

- Modules that require a live LLM call — mark paths as `@pytest.mark.llm` candidates.
- Modules requiring external services (Anki, Zotero, Elevenlabs) — flag coverage ceiling in report.
- `__init__.py` re-export files with no logic.

If args were provided, highlight those modules at the top of the gap list.

## Step 3: Write Tests

For each priority module, write tests in the matching file under `tests/`:

| Source                              | Test file                           |
|-------------------------------------|-------------------------------------|
| `swanki/processing/pdf_processor.py` | `tests/test_pdf_processor.py`      |
| `swanki/models/cards.py`           | `tests/test_cards.py`               |
| `swanki/pipeline/pipeline.py`      | `tests/test_pipeline.py`            |

**Test quality rules:**

- Test logical behaviors, not lines. One test can and should make multiple assertions if they belong to the same workflow — avoid splitting a single operation into many tiny tests.
- Prefer few, well-structured tests with broad coverage per test over many narrow tests.
- Mock only at system boundaries (subprocess, HTTP requests, filesystem when testing logic above it). Never mock everything inside the function under test.
- Never write tests that only verify pydantic parses a field or other third-party library behavior. Every test must exercise project logic.
- Use `tmp_path` (pytest fixture) for all filesystem tests — never write to real project directories.
- Use `unittest.mock.patch` for subprocess calls, HTTP calls, and other I/O boundaries.
- Mark tests correctly: `@pytest.mark.integration` for external services, `@pytest.mark.llm` for LLM calls.

**After writing tests for a module**, spot-check by running coverage for that module:

```bash
/Users/michaelvolk/miniconda3/bin/python -m pytest tests/test_<module>.py --cov=swanki.<dotted_module> --cov-report=term-missing -q
```

Verify improvement before moving to the next module.

## Step 3b: Update Dendron Notes for Test Files

After writing tests for each module, update (or create) the corresponding dendron note for each new/modified test file.

Map test files to notes the same way as source files:

`tests/test_pdf_processor.py` -> `notes/tests.test_pdf_processor.md`

If the note doesn't exist, create it:

```bash
dendron-cli note write --fname "tests.test_pdf_processor"
```

Append a dated section explaining **why** these tests were written from the intentional stance:

- What behavior is being protected against regression?
- What edge cases were found worth guarding?
- Any surprising behaviors discovered while writing tests?
- Why certain paths were deliberately left untested?

Keep it concise — 2-4 sentences per module. The diff shows *what* was added; the note captures *why*.

This can be batched across a wave of modules rather than done one-by-one.

## Step 4: Final Coverage Run

After all tests are written, run the full suite:

```bash
/Users/michaelvolk/miniconda3/bin/python -m pytest tests/ --cov=swanki --cov-report=term-missing -q -m "not llm and not integration"
```

Record **final total %** and per-module deltas.

## Step 5: Write Campaign Report

Create a dendron note for the report:

```bash
dendron-cli note write --fname "test-campaign.YYYY.MM.DD"
```

Append after frontmatter:

```markdown
## YYYY.MM.DD - Test Campaign Report

### Summary

| Metric            | Value |
|-------------------|-------|
| Baseline coverage | XX%   |
| Final coverage    | YY%   |
| New test functions | N    |
| Modules improved  | list  |
| Ceiling modules   | list  |

### Coverage Delta by Module

| Module                  | Before | After | Notes                   |
|-------------------------|--------|-------|-------------------------|
| processing/pdf_processor | 0%    | 85%   |                         |
| utils/audio.py          | 0%     | 0%    | Elevenlabs API - future |

### Test Quality Notes

- What kinds of tests were written (unit, mocked boundary, etc.)
- Any bugs or edge cases discovered during testing
- Modules excluded and why

### Next Campaign Targets

- What remains and why it was deferred
```

## Step 6: Stage

Stage all new/modified test files, dendron notes, and the report:

```bash
git add tests/... notes/tests.*.md notes/test-campaign.YYYY.MM.DD.md
```

Print a summary of staged files.

## Important Rules

- Never write tests that only test library internals or pydantic parsing.
- No mock-everything tests — if every call is mocked, the test verifies nothing.
- 100% coverage is not the goal — meaningful coverage of real behavior with minimal test count is. Document ceilings honestly.
- No Unicode emojis in report or dendron notes.
- Do NOT ask extra approval questions — tool approval prompts are the gates.

## Example Invocations

- `/test-campaign` — open-ended full campaign
- `/test-campaign swanki/processing/pdf_processor.py` — targeted: PDF processor only
- `/test-campaign swanki/models/` — all models submodule
- `/test-campaign "focus on card generation and markdown processing"`
- "run a test campaign on the processing module"
- "check coverage and improve tests for pipeline.py"
