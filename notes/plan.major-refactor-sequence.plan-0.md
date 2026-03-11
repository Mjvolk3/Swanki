---
id: okjmzumd1mcqagpaadnjx1h
title: Plan 0
desc: ''
updated: 1773238019273
created: 1773197428520
---
Major Refactor Sequence — Master Plan

## Overview

Five interdependent refactors executed linearly on a single long-lived branch (`refactor/major-pipeline-overhaul`). One commit per completed step gives clean revert points. Each step builds on the prior — the ordering minimizes rework and conflict.

## Branch Strategy

```bash
git checkout -b refactor/major-pipeline-overhaul
# Step 1 → commit → Step 2 → commit → ... → Step 5 → commit → PR to main
```

## Execution Order

| Step | Plan                                           | Risk   | Key Touch Points                                                  |
|------|------------------------------------------------|--------|-------------------------------------------------------------------|
| 1    | [[plan.audio-decoupling-from-cards.plan-0]]    | Low    | `pipeline.py` (branching), config                                 |
| 2    | [[plan.config-refactor-less-clunky.plan-0]]    | Medium | Config system, `__main__.py`, delete `generator.py`               |
| 3    | [[plan.optional-create-cards-per-char.plan-0]] | Medium | New `segmenter.py`, `pipeline.py` (card gen loop), `swanki/conf/` |
| 4    | [[plan.lecture-transcript-refactor.plan-0]]    | Medium | `lecture.py`, `pipeline.py` (passthrough), `swanki/conf/prompts/` |
| 5    | [[plan.instructor-to-pydanticAI.plan-0]]       | High   | Every LLM call site, new `swanki/llm/` package                    |

## Why This Order

1. **Audio decoupling first** — smallest change (~30 lines), ships a user-requested feature (lecture-only mode), validates that audio is truly independent of cards
2. **Config refactor second** — eliminates the 1360-line `generator.py` before steps 3-5 would otherwise need to modify it. All subsequent config changes go directly to `swanki/conf/` package defaults
3. **Segmentation third** — modifies the card generation loop in `pipeline.py`. Doing this before the LLM migration (step 5) means we rearrange the loop with familiar instructor call patterns
4. **Lecture transcript fourth** — adds new functions to `lecture.py` using current instructor/OpenAI patterns. These get migrated to pydanticAI in step 5 along with everything else
5. **PydanticAI migration last** — touches every module. All structural refactors must be stable before swapping the LLM layer underneath them

## Dependency Graph

```
Step 1 (audio decoupling)
  │
  ├─→ Step 2 (config refactor)
  │     │
  │     ├─→ Step 3 (segmentation)
  │     │
  │     └─→ Step 4 (lecture transcript)
  │
  └─────────────────────────────→ Step 5 (pydanticAI)
                                    ↑ depends on ALL prior steps
```

Steps 3 and 4 are independent of each other (cards vs audio) but both depend on step 2. Either order works; segmentation first is preferred because it touches `pipeline.py`'s card generation loop which is also modified in step 5.

## Conflict Zones and Resolutions

### High severity

| Plans                 | File           | Conflict                                                                   | Resolution                                                                                          |
|-----------------------|----------------|----------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------|
| Segmentation + Config | `generator.py` | Segmentation would update it; config deletes it                            | Config runs first — segmentation skips all generator changes                                        |
| PydanticAI + Lecture  | `lecture.py`   | Both heavily modify — one changes call patterns, other changes what's sent | Lecture runs first with current patterns; pydanticAI migrates everything including new SI functions |

### Medium severity

| Plans                     | File          | Conflict                  | Resolution                                                                                         |
|---------------------------|---------------|---------------------------|----------------------------------------------------------------------------------------------------|
| PydanticAI + Segmentation | `pipeline.py` | Both modify card gen loop | Segmentation renames method and restructures loop first; pydanticAI then migrates the calls inside |

### Low/none

| Plans                      | Notes                                      |
|----------------------------|--------------------------------------------|
| Audio decoupling + Config  | Orthogonal — `mode` key migrates trivially |
| Audio decoupling + Lecture | Different stages in `process_full()`       |
| Segmentation + Lecture     | Cards vs audio — no overlap                |

## Per-Step Adjustments

Detailed adjustments are documented in each plan's "Sequencing Note" section. Summary:

### Step 1 adjustments: none

Audio decoupling plan is self-contained. Config goes to `.swanki_config/` (migrated in step 2).

### Step 2 adjustments

- Must carry forward `mode: full` key and `lecture_only.yaml` from step 1 into `swanki/conf/`

### Step 3 adjustments

- ~~All `generator.py` modifications~~ — **SKIP**. File no longer exists.
- All `.swanki_config/pipeline/*.yaml` → `swanki/conf/pipeline/*.yaml`
- Segmentation stage placed inside `mode == "full"` branch (audio-only doesn't need segments)

### Step 4 adjustments

- All `.swanki_config/prompts/*.yaml` → `swanki/conf/prompts/*.yaml`
- `si_start_page` passthrough in `pipeline.py` must be outside mode guard (lecture runs in both modes)
- New functions written with instructor/OpenAI patterns (migrated in step 5)

### Step 5 adjustments

- Model configs in `swanki/conf/models/` (not `.swanki_config/`)
- Card gen method is `_generate_cards_for_segment()` (renamed in step 3)
- `lecture.py` has additional functions from step 4 (`build_si_index`, `extract_relevant_si`, modified `generate_and_validate_chunk`) — all LLM calls in these must also be migrated
- `LectureTranscriptFeedback` has `si_balance` field from step 4
- **Critical**: self-critic and retry mechanisms (card feedback, lecture critique, audio validation) must be faithfully replicated. Consult local clones of both libraries as reference:
  - instructor: `/Users/michaelvolk/Documents/projects/instructor`
  - pydantic-ai: `/Users/michaelvolk/Documents/projects/pydantic-ai`
  - See "Migration Risk: Self-Critic and Retry Mechanisms" section in [[plan.instructor-to-pydanticAI.plan-0]] for details

## Quality Gates (applied to every step)

Every step must satisfy all of the following before committing:

### Code quality

- [ ] `ruff check` passes on all touched files
- [ ] `ruff format` passes on all touched files
- [ ] `mypy --strict` passes on all touched files (or module-level overrides documented)

### Documentation

- [ ] Google-style docstrings on all new/modified public functions and classes
- [ ] Frontmatter header block on every new `.py` file per project conventions
- [ ] `/update-py-notes` run for all touched `.py` files (dendron module notes)
- [ ] Sphinx docs updated for any public API changes, new modules, or new CLI flags

### Testing

- [ ] Unit tests written for all new functions (not just integration)
- [ ] Existing test suite passes: `python -m pytest tests/ -x`
- [ ] New tests pass: `python -m pytest tests/ -x --tb=short`
- [ ] Test coverage does not decrease (run `/test-campaign` if adding significant code)

### Git hygiene

- [ ] One commit per completed step with descriptive message
- [ ] No unrelated changes mixed in
- [ ] `/stage` and `/commit` workflow followed

## Step-by-Step Checklist

### Step 1: Audio Decoupling [[plan.audio-decoupling-from-cards.plan-0]]

- [x] Add `mode: full` to `.swanki_config/config.yaml`
- [x] Add `mode` branching in `process_full()`
- [x] Add cards guard in `generate_audio()`
- [x] Create `lecture_only.yaml` audio preset
- [x] Update `__main__.py` help text
- [x] Write unit tests for audio_only branch
- [x] Quality gates pass
- [ ] Commit: "Add audio_only mode to skip card generation"

### Step 2: Config Refactor [[plan.config-refactor-less-clunky.plan-0]]

- [ ] Create `swanki/conf/` with all YAML defaults (including `mode: full` from step 1)
- [ ] Rename audio presets to self-documenting names
- [ ] Implement `SwankiSearchPathPlugin` for three-tier resolution
- [ ] Register plugin via `pyproject.toml` entry point
- [ ] Update `@hydra.main(config_path=...)` in `__main__.py`
- [ ] Delete `swanki/config/generator.py` (1360 lines)
- [ ] Create `swanki/config/helpers.py`
- [ ] Add `--show-defaults`, `--init-config`, `--config-info` CLI flags
- [ ] Migrate `.swanki_config_custom/` contents to `~/.swanki/`
- [ ] Add `swanki/conf/**/*.yaml` to `pyproject.toml` package data
- [ ] Write unit tests for search path plugin, helpers
- [ ] Quality gates pass
- [ ] Commit: "Replace ConfigGenerator with three-tier config system"

### Step 3: Character Segmentation [[plan.optional-create-cards-per-char.plan-0]]

- [ ] Create `swanki/pipeline/segmenter.py` with all 4 functions
- [ ] Add segmentation stage in `process_full()` (inside `mode == "full"` branch)
- [ ] Delete `generate_cards_with_context` (dead code)
- [ ] Rename `_generate_cards_for_page_with_context` → `_generate_cards_for_segment`
- [ ] Update card gen loop with document-order interleaving
- [ ] Update `estimate_card_count` for segment awareness
- [ ] Rename config keys in `swanki/conf/pipeline/*.yaml`
- [ ] Remove dead `chunk_size`/`overlap` params from configs
- [ ] Write `tests/test_segmenter.py` (11 tests)
- [ ] Quality gates pass
- [ ] Commit: "Add character-based segmentation mode for card generation"

### Step 4: Lecture Transcript Refactor [[plan.lecture-transcript-refactor.plan-0]]

- [ ] Add `si_start_page` to `PrepareResult` in `zotero_paper_import.py`
- [ ] Write `_meta.json` from import script
- [ ] Read `_meta.json` in `pipeline.py`, pass `si_start_page` to lecture gen
- [ ] Split markdown file list in `generate_lecture_audio()` by SI boundary
- [ ] Implement `build_si_index()` and `extract_relevant_si()`
- [ ] Add `si_reference_content` to `generate_and_validate_chunk()`
- [ ] Add SI proportion constraint to critique prompt
- [ ] Add `si_balance` field to `LectureTranscriptFeedback`
- [ ] Add `lecture_si_instructions` to `swanki/conf/prompts/default.yaml`
- [ ] Refactor length control: remove per-section budgets, add global target + full-transcript enforcement
- [ ] Broaden `chunk_by_headers()` regex to match unnumbered headers
- [ ] Write unit tests for `build_si_index`, `extract_relevant_si`, length control
- [ ] Quality gates pass
- [ ] Commit: "Add SI-aware lecture generation and global length control"

### Step 5: PydanticAI Migration [[plan.instructor-to-pydanticAI.plan-0]]

- [ ] Phase 0: Create `swanki/llm/client.py`, centralize all `OpenAI()` instantiation
- [ ] Phase 0: Add `provider` field to `swanki/conf/models/default.yaml`
- [ ] Phase 1: Migrate `pdf_classifier.py` (1 call site, proof of concept)
- [ ] Phase 1: Add `pydantic-ai` to `pyproject.toml`
- [ ] Phase 2: Migrate audio modules (`lecture.py`, `card.py`, `reading.py`, `summary.py`)
- [ ] Phase 2: Migrate new SI functions from step 4
- [ ] Phase 3: Migrate `pipeline.py` (13+ call sites)
- [ ] Phase 3: Create `swanki/llm/agents.py` with agent registry
- [ ] Phase 4: Add Anthropic model config preset to `swanki/conf/models/`
- [ ] Phase 4: Remove `instructor` dependency
- [ ] Phase 4: Remove `tenacity` if no longer used
- [ ] Write unit tests for agent registry and client factory
- [ ] Write integration tests (`@pytest.mark.llm`) for at least one agent
- [ ] Quality gates pass
- [ ] Commit: "Migrate from instructor to pydanticAI for multi-provider LLM support"

## Final PR

After all 5 steps complete on the branch:

```bash
gh pr create --title "Major pipeline refactor: audio decoupling, config, segmentation, lecture, pydanticAI" \
  --body "..."
```

The PR should reference all 5 plan notes and include a summary of what changed across the full refactor.

## Estimated Scope

| Step      | New/Modified Files   | New Tests     | Lines Changed (est.)    |
|-----------|----------------------|---------------|-------------------------|
| 1         | 4                    | ~3            | ~40                     |
| 2         | ~10                  | ~8            | ~1500 (mostly deletion) |
| 3         | ~6                   | ~11           | ~300                    |
| 4         | ~5                   | ~8            | ~400                    |
| 5         | ~12                  | ~10           | ~600                    |
| **Total** | **~25 unique files** | **~40 tests** | **~2800**               |
