---
id: jw01iia69oz5lqyr1yz7ifh
title: '11'
desc: ''
updated: 1773622820303
updated: 1773322944373
updated: 1773337846654
updated: 1773269920361
updated: 1773322264312
updated: 1773333750152
created: 1773142434234
---
## 2026.03.10

- [x] Refactored monolithic `swanki/utils/audio.py` (2918 lines) into `swanki/audio/` package with 5 focused modules and added 37 unit tests with mocked APIs. [[swanki.audio]]
- [x] Moved 6 outdated `.claude/commands/` files into `plan.*` dendron notes using dendron CLI, clearing the commands directory [[plan.clean-pdf]] [[plan.fix-cloze]] [[plan.refactor-progress-report]] [[plan.refactor-hydra]] [[plan.self-refine-refactor]] [[plan.update-after-deep-learning-revolution-review]]
- [x] Write plan for refactor information flow. We originally thought that cards would be only output but we have three audio outputs only one of which is dependent on the creation of cards, at least so I believe - complementary. Is it true that summary, lecture, transcript are decoupled from card creation? If so we should consider a refactor where audio only can be produced. Some of my users want this functionality, for instance they only want to create lectures. [[plan.audio-decoupling-from-cards.plan-0]]
- [x] Write Plan for refactor discussion plans considering of moving from instructor to pydanticAI [[plan.instructor-to-pydanticAI.plan-0]]
- [x] Write plan refactor config plan [[plan.config-refactor-less-clunky.plan-0]]
- [x] Write plan for improving lecture transcripts. [[plan.lecture-transcript-refactor.plan-0]]
- [x] Write plan for segmenting text more consistently [[plan.optional-create-cards-per-char.plan-0]]
- [x] Purged `.claude/settings.local.json` from git history and added `.claude/settings.json` as the committed project settings
- [x] Created master refactor sequence plan tying together all 5 interdependent plans (audio decoupling, config, segmentation, lecture transcript, pydanticAI) with execution order, conflict resolutions, per-step adjustments, and uniform quality gates. [[plan.major-refactor-sequence.plan-0]]
- [x] Added worktree documentation to CLAUDE.md, merge-worktree skill, worktree permissions in settings.json, and .env.example for key-safe env template [[scripts.setup-worktree]]

## 2026.03.11

- [x] Added sequencing notes, per-step adjustments, and quality gates (mypy, docstrings, tests, sphinx, ruff) to all 5 refactor plans so each is aware of its position in the execution order. [[plan.audio-decoupling-from-cards.plan-0]] [[plan.config-refactor-less-clunky.plan-0]] [[plan.optional-create-cards-per-char.plan-0]] [[plan.lecture-transcript-refactor.plan-0]] [[plan.instructor-to-pydanticAI.plan-0]]
- [x] Added migration risk section for self-critic and retry mechanisms with pointers to local instructor and pydantic-ai repo clones as reference for faithful replication. [[plan.instructor-to-pydanticAI.plan-0]]
- [x] Created fine-grained WIP scratchpad with full call site inventory (21 LLM calls across 7 files) and per-phase checklists for the pydanticAI migration. [[plan.instructor-to-pydanticAI.wip]]
- [x] Added `setup: worktree` VS Code task and fixed executable permission on `scripts/setup-worktree.sh`
- [x] Added README badges (CI status, Codecov coverage, Ruff, mypy strict, Python 3.13, MIT license) and Codecov integration to CI workflow
- [x] Added `settings.local.json` copy step to `setup-worktree.sh` so new worktrees inherit `Bash(*)` permissions automatically [[scripts.setup-worktree]]
- [x] Added "Finding Rationale for Changes" section to CLAUDE.md pointing to dendron module notes as the primary source of decision history

## 2026.03.12

- [x] Fixed VS Code test/coverage tasks to use hardcoded conda env path instead of `${command:python.interpreterPath}` which resolved to the wrong interpreter
- [x] Added multi-range PDF cutting to zotero import script so Extended Data (Nature) and STAR Methods/SI figures (Cell) are preserved while refs and publisher reporting summaries are cut; migrated from broken `swanki-cut` to `qpdf` [[scripts.zotero_paper_import#20260312---multi-range-pdf-cutting-and-qpdf-migration]]
- [x] Fixed worktree `.claude/settings.json` relative paths breaking by adding a rewrite step to `setup-worktree.sh` that adjusts `../` prefixes to the correct depth [[scripts.setup-worktree]]

## 2026.03.14

- [x] Fixed Zotero import script mis-ordering attachments (SI downloaded as main article) by adding title/filename heuristic, and tolerate qpdf exit-code-3 warnings [[scripts.zotero_paper_import#20260314---fix-attachment-ordering-and-qpdf-warning-tolerance]]
- [x] Drafted 12-slide lit review outline for Merzbacher et al. 2025 Flux Cone Learning paper [[scratch.2026.03.13.134811-outline]]

## 2026.03.15

- [ ] Planned Reveal.js presentation generation feature for creating academic slide decks from Swanki-processed paper data with LLM-driven content, figure extraction, and mermaid diagram support [[plan.presentation-generation-revealjs]]
- [x] Implemented Step 1 (audio decoupling) of major refactor: added `mode=audio_only` config to skip card generation, `lecture_only` audio preset, cards guard in `generate_audio()`, and 6 unit tests [[plan.audio-decoupling-from-cards.plan-0]] [[swanki.pipeline.pipeline]] [[tests.test_pipeline_mode]]
- [x] Implemented Step 2 (config refactor) of major refactor: replaced 1354-line `ConfigGenerator` with static YAML defaults in `swanki/conf/`, three-tier Hydra SearchPathPlugin (package/global/local), config helpers, renamed audio presets to self-documenting names, migrated custom configs to `~/.swanki/`, added `--show-defaults`/`--init-config`/`--config-info` CLI flags, and 16 unit tests [[plan.config-refactor-less-clunky.plan-0]] [[swanki.config.helpers#20260311---new-config-utility-module]] [[swanki.config.hydra_plugins#20260311---new-three-tier-hydra-searchpathplugin]] [[swanki.config.generator#20260311---add-mode-key-and-lecture_only-audio-preset]] [[tests.test_config_helpers#20260311---new-test-suite-for-config-helpers]] [[tests.test_hydra_plugins#20260311---new-test-suite-for-swankisearchpathplugin]]
- [x] Implemented Step 3 (character segmentation) of major refactor: created `segmenter.py` with 4 utility functions for char-based segmentation, added segmentation stage and document-order interleaving to `process_full()`, deleted 333 lines of dead code (`generate_cards_with_context`), renamed config keys to segment terminology, and wrote 11 unit tests [[plan.optional-create-cards-per-char.plan-0]] [[swanki.pipeline.segmenter#20260311---new-module-for-character-based-segmentation]] [[swanki.pipeline.pipeline#20260311---add-character-based-segmentation-mode-for-card-generation]] [[tests.test_segmenter#20260311---initial-test-suite-for-segmenter-module]] [[tests.test_pipeline_mode#20260311---update-mock-for-segment-rename]]
- [x] Implemented Step 4 (lecture transcript refactor) of major refactor: tracked SI boundary in `_meta.json`, removed per-section word budgets in favor of global ratio-based length control, broadened `chunk_by_headers()` to match unnumbered headers, added SI splitting/indexing/contextual enrichment with `build_si_index()` and `extract_relevant_si()`, SI proportion constraint in critique, `si_balance` on feedback model, pipeline reads `_meta.json`, and 11 new unit tests [[plan.lecture-transcript-refactor.plan-0]] [[swanki.audio.lecture]] [[swanki.models.cards]] [[swanki.pipeline.pipeline]] [[tests.test_audio_lecture]]
- [x] Implemented Step 5 (pydantic-ai migration) of major refactor: created `swanki/llm/` agent registry with 6 agents, replaced all 21 instructor/OpenAI call sites across 7 files with pydantic-ai `agent.run_sync()`, removed instructor/tenacity deps, added anthropic.yaml preset, and updated all test mocks [[plan.instructor-to-pydanticAI.wip]] [[swanki.llm.agents#20260312---centralized-pydantic-ai-agent-registry]] [[swanki.pipeline.pipeline#20260312---migrate-from-instructoropenai-to-pydantic-ai-agents]] [[swanki.audio.card#20260312---migrate-from-openai-client-to-pydantic-ai-agents]] [[swanki.audio.lecture#20260312---migrate-from-instructoropenai-to-pydantic-ai-agents]] [[swanki.processing.image_processor#20260312---migrate-from-openai-client-to-pydantic-ai-agents-and-modernize-code]]
- [x] Fixed all ruff errors and mypy --strict issues across migrated files: rewrote image_processor.py with modern types and Google-style docstrings, added missing type stubs to pyproject.toml ignore list, added class docstrings to PageLabel/PDFCutPlan [[swanki.processing.image_processor#20260312---migrate-from-openai-client-to-pydantic-ai-agents-and-modernize-code]] [[swanki.utils.pdf_classifier#20260312---migrate-from-instructor-to-pydantic-ai-and-add-docstrings]]
- [x] Pre-API hardening (cleanup plan steps 1-7): deleted `swanki/legacy/` (31 files, -3500 lines), removed `--legacy` CLI, applied ruff formatting and type annotation modernization across all modern modules, added `ConfigDict(extra="forbid")` to Pydantic models, added standard frontmatter docstrings, fixed mypy errors, and added 4 new test files (agents, config resolution, model validation, LLM smoke) [[plan.major-refactor-sequence-cleanup.plan-0]] [[swanki.__init__#20260312---remove-legacy-re-exports-from-top-level-package]] [[swanki.models.document#20260312---strict-model-config-and-new-imagesummary-fields]] [[swanki.processing.anki_processor#20260312---type-annotation-modernization-and-ruff-formatting]] [[swanki.pipeline.pipeline#20260312---add-mypy-type-narrowing-asserts-for-processingstate]]

***

- [ ] Cite pydantic in paper.
- [ ] Integrate edits from @Shekhar-Mishra
