---
id: d4fkyehd4flqj47ihsir1zt
title: Test_llm_safety
desc: ''
updated: 1779602572418
created: 1779602572418
---

## 2026.05.24 - Coverage for the generic biosec-refusal retry wrapper

Eight tests for [[swanki.llm.safety]]'s `with_safety_retry`:

- **Happy path** -- first attempt succeeds; the original user message is sent
  verbatim with no preamble; `agent.run_sync` is called exactly once.
- **Retry on `invalid_prompt`** -- first attempt raises a safety refusal,
  second succeeds; the second call's user message starts with
  `EDU_CONTEXT_PREAMBLE` and ends with the original message verbatim.
- **Retry on `limited access ... safety`** -- both `SAFETY_REFUSAL_MARKERS`
  values trip the retry path (separate test to lock the matcher).
- **Exhaustion re-raises** -- 3 attempts all safety-refuse; the helper
  re-raises (with `max_safety_retries=2` → 3 total attempts).
- **Non-safety exception re-raises immediately** -- `RuntimeError("HTTP 500")`
  is not in the markers; the helper does NOT retry and re-raises on the first
  hit (so transient HTTP/timeout errors fail fast as the pydantic-ai
  per-agent `retries=N` already handles them at the lower layer).
- **`model_settings` forwarding** -- supplied dict is passed through as the
  `model_settings` kwarg on `agent.run_sync`.
- **`model_settings` omitted when None** -- the kwarg is absent (not `None`)
  on the run_sync call, so structured-output agents that don't accept it
  aren't bothered.
- **Constants sanity** -- both `SAFETY_REFUSAL_MARKERS` entries are present
  and `EDU_CONTEXT_PREAMBLE` carries the published-content framing.

Uses `unittest.mock.MagicMock` for the agent so the tests don't touch
pydantic-ai or any LLM provider. Bound to the helper's contract, not its
implementation -- the existing lecture-only helper's tests stay independent.
