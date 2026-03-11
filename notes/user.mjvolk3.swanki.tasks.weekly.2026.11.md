---
id: jw01iia69oz5lqyr1yz7ifh
title: '11'
desc: ''
updated: 1773197267148
created: 1773142434234
---
## 2026.03.10

- [x] Refactored monolithic `swanki/utils/audio.py` (2918 lines) into `swanki/audio/` package with 5 focused modules and added 37 unit tests with mocked APIs. [[swanki.audio]]
- [x] Moved 6 outdated `.claude/commands/` files into `plan.*` dendron notes using dendron CLI, clearing the commands directory [[plan.clean-pdf]] [[plan.fix-cloze]] [[plan.refactor-progress-report]] [[plan.refactor-hydra]] [[plan.self-refine-refactor]] [[plan.update-after-deep-learning-revolution-review]]
- [x] Write plan for refactor information flow. We originally thought that cards would be only output but we have three audio outputs only one of which is dependent on the creation of cards, at least so I believe - complementary. Is it true that summary, lecture, transcript are decoupled from card creation? If so we should consider a refactor where audio only can be produced. Some of my users want this functionality, for instance they only want to create lectures. [[audio-decoupling-from-cards.plan-0]]
- [x] Write Plan for refactor discussion plans considering of moving from instructor to pydanticAI [[refactor-discussion.instructor-to-pydanticAI]]
- [x] Write plan refactor config plan [[config-refactor-less-clunky.plan-0]]
- [x] Write plan for improving lecture transcripts. [[lecture-transcript-refactor.plan-0]]
- [x] Write plan for segmenting text more consistently [[optional-create-cards-per-char.plan-0]]
- [x] Purged `.claude/settings.local.json` from git history and added `.claude/settings.json` as the committed project settings
- [x] Added worktree documentation to CLAUDE.md, merge-worktree skill, worktree permissions in settings.json, and .env.example for key-safe env template [[scripts.setup-worktree]]

***

- [ ] Cite pydantic in paper.
- [ ] Integrate edits from @Shekhar-Mishra
