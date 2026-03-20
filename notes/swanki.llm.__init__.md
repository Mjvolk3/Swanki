---
id: 7niyfyldj2essncrf0n52an
title:   Init  
desc: ''
updated: 1773322227375
created: 1773322227375
---

## 2026.03.12 - New package for pydantic-ai agent registry

Package init that re-exports all agents and `get_model_string` from `swanki.llm.agents`. Provides a clean public API so consumers import from `swanki.llm` rather than reaching into submodules. Created as part of the instructor-to-pydantic-ai migration (Step 5 of [[plan.major-refactor-sequence.plan-0]]).
