---
id: 9pq4x7m2vbnr5tzc8wkdhaj
title: Usage_ledger
desc: Per-run LLM token accounting -- one row per call, rolled up by tier and label, written to llm-usage.json
updated: 1786500000000
created: 1786500000000
---

## 2026.08.11 - Why this exists

Swanki logged no token usage anywhere. A record spending day could only be
reconstructed afterwards from SLURM logs and call-site counting, which is how
the motivating question ("was this the model or the volume?") ended up
unanswerable. This ledger makes a run's spend readable from its own output
directory.

**Tokens and counts only, no pricing constants.** Prices move out of band; a
stale price table in the repo is worse than none because it yields confident
wrong numbers. The artifact reports what was consumed and leaves valuation to
whoever reads it.

Three shape decisions carry real risk if reversed:

- **`reasoning_tokens` nests under `output_detail`, never beside
  `output_tokens`.** On the Responses API `output_tokens` already *includes*
  reasoning; recording them as siblings double-counts. Same reasoning for
  `cache_read_tokens`, which is a breakdown of `input_tokens`, not an addition.
- **Every field is read via `getattr`/`.get` and coerced to `int`.**
  `reasoning_tokens` is not a first-class pydantic-ai attribute -- it arrives
  inside the provider-specific `details` dict and only on the Responses path, so
  a non-OpenAI provider supplies nothing.
- **`write_usage` merges rather than truncates, and writes temp-then-rename.**
  An `audio_only` rerun must add to the run record instead of erasing what
  generation reported, and a killed SLURM job must not leave a half-written file
  that reads as a complete accounting.

`record()` takes a lock because four `ThreadPoolExecutor` pools sit on this path
and pydantic-ai's own `RunUsage.incr` is unlocked. An accounting artifact that
undercounts under load is worse than none, because it looks authoritative.

The artifact lands at `<output_base>/llm-usage.json` -- deliberately not
`output_dir`, which `audio_only` reruns skip entirely, i.e. exactly the runs
whose cost this is meant to explain.

See [[swanki.pipeline.run_agent]] and
[[plan.split-generation-and-utility-models.2026.08.11]].
