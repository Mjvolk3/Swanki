---
id: 3wkq8n5xvbr72mzt9chdpal
title: Run_agent
desc: The single seam every LLM call passes through -- model-tier routing plus token accounting in one wrapper
updated: 1786500000000
created: 1786500000000
---

## 2026.08.11 - One seam, because routing and accounting are the same problem

Swanki had no choke point for LLM calls. The model string was resolved at ~20
places, and 14 call sites bypassed even `with_safety_retry` by calling
`agent.run_sync` directly. That single fact blocked *both* goals: you cannot
route calls to different model tiers without a common entry point, and you
cannot account for their tokens without one either. They are one missing seam,
so `run_agent` is both rather than two parallel mechanisms.

Migrating a bare `run_sync` site to `run_agent` also gains it biosec-refusal
retry as a side effect, since the wrapper delegates to
[[swanki.llm.safety]]'s `with_safety_retry`.

**Tiers name intent, not a model.** `generation` is work that invents content or
judges whether content is right; `utility` is mechanical transformation. What
each resolves to is config, so the routing decision at a call site stays
readable years after the model names change.

**`models.llm` remains the generation tier.** The split is additive rather than
a symmetric rename into `generation`/`utility`. The decisive reason is the three
gate configs (`card_correctness_gate`, `image_leak_gate`,
`audio_correctness_gate`) whose `model: null` means "reuse `models.llm`" -- if
`models.llm` keeps meaning "the strong model", the gates stay strong with zero
code change. Correct behaviour is the default rather than something a reviewer
must notice. A symmetric rename would have silently repointed every gate at the
cheap fallback.

`resolve_tier_models` falls back to the generation model when
`models.llm.utility` is unset, so a config predating the split behaves
identically.

**`validate_tier` raises on an unknown tier.** pydantic-ai does not validate
model names -- an unrecognised one falls back to a generic profile and runs
happily, so a typo would produce plausible output from the wrong model. Failing
loudly at the seam is the only place that mistake is cheap.

Lives under `swanki/pipeline/` rather than `swanki/llm/`: `pyproject.toml`
relaxes mypy for `swanki.pipeline.*` but not `swanki.llm.*`, and a generic
wrapper over `Agent[Any, Any]` returning heterogeneous `RunResult` types fights
strict mypy for no benefit. Verified no circular import despite audio modules
importing from `swanki.pipeline` -- this module imports only `swanki.llm.*` and
its sibling ledger, never `pipeline.py`.

See [[swanki.pipeline.usage_ledger]] and
[[plan.split-generation-and-utility-models.2026.08.11]].

## 2026.08.11 - Tier registry, and transcripts/reading moved to luna

`configure_tiers` registers the resolved model per tier once at pipeline start;
`run_agent` then selects by tier with the caller's model string as fallback.
This avoids threading a second model through ~20 signatures -- the audio modules
all take `model: str` as a function parameter and never see config, so the
alternative was a mechanical edit of every caller in the chain.

Semantics, pinned by tests: **the registered tier model wins, the caller's
string is the fallback.** A run that never calls `configure_tiers` (a script, a
test, a partial rerun) behaves exactly as it did before tiering. The registry is
written once during setup and read-only afterwards, so the four thread pools on
this path need no lock -- but it is module-global, so tests clear it via an
autouse fixture or they pollute each other into false passes.

**Moved to the utility tier: card->spoken transcripts (`audio/card.py`) and
reading Pass-2 chunks (`audio/reading.py`).** Both are copy-with-cleanup --
expand LaTeX and acronyms, insert pause tags -- and the evidence they need no
reasoning is direct rather than inferred: the first instrumented run recorded
**zero reasoning tokens across 32 transcript calls**, averaging 498 input / 33
output. The model already declines to reason there, so sol's rate bought
nothing.

The reading path is additionally pre-defended against the one failure a weaker
model could introduce: `_PASS2_CHUNK_MIN_RATIO = 0.85` retries a short chunk
three times and then falls back to the humanized input verbatim, so dropped
prose cannot reach the transcript. The card path has **no** equivalent guard --
its safety argument is the small single-card input, not a mechanism, so a sample
read of the first regenerated fronts and backs is the check.

Measured saving on the one available run is only 12%, but that run
(`kasserPhilosophyScience_L01`) is `audio=complementary` and produced **zero**
reading chunks. On a full `audio=all` chapter, reading Pass-2 is ~315 of ~800
calls, so the real share is much larger -- pending measurement.
