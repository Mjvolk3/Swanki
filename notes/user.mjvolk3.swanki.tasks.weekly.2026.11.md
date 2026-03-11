---
id: jw01iia69oz5lqyr1yz7ifh
title: '11'
desc: ''
updated: 1773238033969
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

***

- [ ] Cite pydantic in paper.
- [ ] Integrate edits from @Shekhar-Mishra
