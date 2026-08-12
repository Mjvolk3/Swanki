---
id: rmvrw8q9ahziqqwbtgnpw5k
title: Split generation and utility models
desc: 'Route swanki LLM call sites to a strong generation tier or a cheap utility tier, behind a universal run_agent wrapper that also emits per-run token accounting'
updated: 1786498069513
created: 1786498069514
---

## Context

Swanki runs every LLM call through one model. `swanki/conf/models/default.yaml`
sets `models.llm.provider: openai-responses` / `models.llm.model: gpt-5.6-sol`,
and all ~25 call sites resolve that same string via
`get_model_string()` (`swanki/llm/agents.py:95-106`).

Measured on one 46-page chapter yielding 166 cards: roughly 800-900 LLM calls,
of which about 85% are mechanical text transformation -- 332 per-card audio
transcripts, 315 reading-chunk transcripts, 48 figure descriptions, 20 summary
chunks. Card *generation* is under 10% of calls. Reasoning-token overhead is
largely per-call, so paying reasoning prices for "rewrite this cloze as spoken
prose" is where the money goes; two record-spend days lined up with heavy
generation runs on sol.

Two deliverables, in this order (Decision 6): **accounting** (a per-run JSON
artifact of model, tier, label and token counts per call -- no pricing
constants), then **routing** (a cheap utility tier for mechanical
transformation; generation, critique and all correctness gates stay strong).

There is no choke point today. `with_safety_retry()`
(`swanki/llm/safety.py:138`) covers 22 call sites and already returns the full
`RunResult` -- usage is free there. The other 14 call `agent.run_sync()` bare
(13 tracked + one untracked), so they are invisible to both routing and
accounting. Routing and accounting are therefore the *same* problem: one
missing seam.

Agents need no changes. Every agent in `swanki/llm/agents.py` is a model-less
module-level singleton; the model string is passed per call. The split is
entirely call-site routing.

## Relevant Files

| Path                                                           | Action    | Purpose                                                                                                                                                                                                                                                               |
|----------------------------------------------------------------|-----------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `swanki/pipeline/run_agent.py`                                 | NEW       | Universal `run_agent(agent, msg, *, tier, label, ...)` wrapper (Decision 2)                                                                                                                                                                                           |
| `swanki/pipeline/usage_ledger.py`                              | NEW       | Thread-safe in-process ledger + atomic merge-on-write of `llm-usage.json`                                                                                                                                                                                             |
| `swanki/conf/models/default.yaml`                              | MODIFY    | Add `models.llm.utility.{provider,model}`; leave `models.llm.{provider,model}` as the generation tier                                                                                                                                                                 |
| `swanki/conf/models/{anthropic,fish_speech*,openai_tts}.yaml`  | MODIFY    | Same additive sub-block per preset; `openai_tts.yaml` `provider: openai` is TTS-only -- do not touch it                                                                                                                                                               |
| `swanki/llm/agents.py`                                         | REFERENCE | `get_model_string()` :95-106; model-less singletons. Hard invariant: never revert `openai-responses` to `openai`                                                                                                                                                      |
| `swanki/llm/safety.py`                                         | REFERENCE | `with_safety_retry` :138; returns full `RunResult`, so `.usage()` is available                                                                                                                                                                                        |
| `swanki/pipeline/pipeline.py`                                  | MODIFY    | 9 wrapped sites (:919 summary, :1115/:1193/:1410/:1727/:3083 card gen, :2985 card feedback, :3220 audio feedback, :3297 text agent); gate model resolution :1964/:1997/:2509; audio pool :2334; artifact from `self.output_base` (set :246). Churning -- rebase often |
| `swanki/audio/lecture.py`                                      | MODIFY    | 8 sites: 4 via `with_safety_retry`, 4 bare (:208, :451, :1612 critic; :1725 refine) -- critique stays generation                                                                                                                                                      |
| `swanki/audio/card.py`                                         | MODIFY    | :239 card->spoken transcript (highest-volume utility candidate), :730 `_humanize_citation`                                                                                                                                                                            |
| `swanki/audio/_common.py`                                      | MODIFY    | :2536 `humanize_latex` (utility); 8-thread pool :1363                                                                                                                                                                                                                 |
| `swanki/audio/summary.py`                                      | MODIFY    | :125 bare `text_agent.run_sync` -- summary chunk transcripts (utility)                                                                                                                                                                                                |
| `swanki/audio/reading.py`                                      | MODIFY    | :131 reading-chunk transcripts (utility, ~315 calls/chapter); in-flux under open `plan.audio-reading-correctness-critic.2026.07.21`                                                                                                                                   |
| `swanki/audio/reading_correctness.py`                          | MODIFY    | :319 critic -- stays generation                                                                                                                                                                                                                                       |
| `swanki/audio/comment_edit.py`                                 | MODIFY    | :106 annotation-driven edit -- generation                                                                                                                                                                                                                             |
| `swanki/pipeline/card_correctness.py`                          | MODIFY    | :123 gate call, :238 8-thread pool; stays generation, gains accounting                                                                                                                                                                                                |
| `swanki/pipeline/image_leak_gate.py`                           | MODIFY    | :97/:119 gate calls, :230 pool; stays generation; in-flux (1 day old)                                                                                                                                                                                                 |
| `swanki/pipeline/glossary.py`                                  | MODIFY    | :63 enumeration (classification -> utility), :160 definition-card gen (generation)                                                                                                                                                                                    |
| `swanki/pipeline/section_classifier.py`                        | MODIFY    | :286 bare -- classification, utility                                                                                                                                                                                                                                  |
| `swanki/pipeline/problem_set.py`                               | MODIFY    | :878 pairing, :1062 card gen -- both bare, both generation                                                                                                                                                                                                            |
| `swanki/processing/image_processor.py`                         | MODIFY    | :281 figure description (~48/chapter, utility candidate); `max_tokens: 8000` + `temperature: 0.3` :285; documented invariant: `model` ctor arg required on purpose, no default                                                                                        |
| `swanki/processing/table_processor.py`                         | MODIFY    | :111 table transcription (utility); `max_tokens: 4000` + `temperature: 0.3` :115                                                                                                                                                                                      |
| `swanki/utils/pdf_classifier.py`                               | MODIFY    | :110-111 hardcodes `"openai:gpt-5.4-nano-2026-03-17"` -- prior art for a cheap tier; fold into the utility tier                                                                                                                                                       |
| `swanki/ocr/reading_order.py`                                  | REFERENCE | :161 bare `run_sync`, **UNTRACKED** -- do not migrate or stage (Gotcha 4)                                                                                                                                                                                             |
| `swanki/conf/card_correctness_gate/default.yaml`               | REFERENCE | `model: null` override -- documented hook for pinning a strong gate model when the main model is downgraded                                                                                                                                                           |
| `pyproject.toml`                                               | MODIFY    | Tighten `pydantic-ai>=0.1` (:30) to `>=1.77,<2`                                                                                                                                                                                                                       |
| `tests/test_agents.py`                                         | MODIFY    | 5 `get_model_string` default tests; add tier-resolution tests                                                                                                                                                                                                         |
| `tests/test_config_resolution.py`                              | REFERENCE | :83-100 asserts `"provider" in llm` across 7 presets; :18-33 pins `temperature == 0.7`. Additive config shape keeps both green                                                                                                                                        |
| `tests/test_usage_ledger.py`                                   | NEW       | Ledger merge, concurrency, reasoning-nesting, artifact shape                                                                                                                                                                                                          |
| `docs/{cli-usage.md:91,configuration.md:150,quickstart.md:74}` | MODIFY    | All three print `models.llm.model=...`; the working override is `models.models.llm.model=...` (Gotcha 7)                                                                                                                                                              |

## Key Design Decisions

1. **Config change is additive; `models.llm.{provider,model}` stays as-is and
   remains the generation tier.** Add a `models.llm.utility` sub-block. The
   decisive reason is the three gate-resolution sites (`pipeline.py:1964`,
   `:1997`, `:2509`) which do
   `gate_cfg.get("model") or get_model_string(llm_config)`. If `models.llm`
   keeps meaning "the strong model", the gates stay strong with *zero* code
   change -- correct behaviour is the default rather than something a reviewer
   has to notice. Rejected: renaming to `models.llm.generation` /
   `models.llm.utility` symmetrically -- tidier, but it silently repoints every
   gate at the new fallback, breaks `tests/test_config_resolution.py:83-100`,
   and invalidates every documented override string in the wild.

2. **One universal `run_agent()` wrapper is the seam for both routing and
   accounting.** It resolves the tier to a model string, delegates to
   `with_safety_retry`, and records usage from the returned `RunResult`.
   Migrating every site to it also gives the 14 bare `run_sync` calls
   safety-retry coverage as a side effect -- a robustness win currently missing
   at, e.g., `problem_set.py:878` and `glossary.py:63`. Rejected: instrumenting
   `safety.py` alone. That leaves ~40% of calls unmeasured and still needs
   separate routing plumbing at every bare site, i.e. the same edit twice.

3. **The new module lives under `swanki/pipeline/`, not `swanki/llm/`.**
   `pyproject.toml:166-169` relaxes mypy for `swanki.audio.*`,
   `swanki.pipeline.*`, `swanki.presentation.*`, `swanki.models.*` -- but *not*
   `swanki.llm.*`, which stays strict. A generic wrapper over `Agent[Any, Any]`
   returning heterogeneous `RunResult` types will fight strict mypy for no
   benefit, and it is pipeline plumbing anyway.

4. **All three gates -- card_correctness, image_leak, audio_correctness --
   stay on the generation tier.** The card-correctness gate is a *factual*
   catcher with a deliberately high acceptance rate, and the recorded user
   position is to push back on cheaper/stricter screening;
   `notes/swanki.pipeline.image_leak_gate.md` (2026.08.10) separately documents
   a measured 249-vs-85 detection gap proving the judgment is semantic, not
   lexical -- a non-reasoning model regresses it.
   `card_correctness_gate/default.yaml` anticipates this exact request: its
   `model: null` override exists "so a deliberately-strong model can be pinned
   for the gate even if a run downgrades the main model for cost." If gate cost
   proves material, the levers are `max_workers` or sampling, not model strength.

5. **Only mechanical transformation routes to utility:** card->spoken transcript
   (`card.py:239`), reading chunks (`reading.py:131`), summary chunks
   (`summary.py:125`), `humanize_latex` (`_common.py:2536`),
   `_humanize_citation` (`card.py:730`), figure description
   (`image_processor.py:281`), table transcription (`table_processor.py:111`),
   section classification (`section_classifier.py:286`), glossary *enumeration*
   (`glossary.py:63`), and the pdf cut classifier (`pdf_classifier.py:111`,
   already cheap). Everything that invents content or renders judgment -- card
   generation, problem pairing, glossary definition cards, lecture and reading
   critique, comment-driven edits, all gates -- stays on generation. The test is
   "does the output depend on knowing whether the content is *right*", not "is
   it short".

6. **Ship accounting first, routing second, as two merges.** The 85% claim is
   inferred, not measured; landing the wrapper plus the ledger and reading one
   chapter's real distribution converts it into a measured decision and produces
   the baseline that makes the routing PR reviewable. It also de-risks the
   migration: if `run_agent` breaks something it lands alone, with no
   simultaneous model change to confound the bisect.

7. **Both tiers keep the `openai-responses:` prefix.**
   `pydantic_ai/models/__init__.py:1346` maps that prefix to
   `OpenAIResponsesModel` unconditionally, with no model-name gating -- a cheap
   model on the Responses API needs no provider change. This preserves the hard
   invariant in `notes/swanki.llm.agents.md` (2026.07.27): reasoning models
   refuse function tools on `/v1/chat/completions` and every swanki agent uses
   structured output. Never flip `openai-responses` back to `openai`.

8. **Utility model must have `thinking_always_enabled=False`.** Verified by
   running pydantic-ai 1.77.0's profile function in the swanki env:
   `gpt-5.6-sol` and `gpt-5.5` are both `thinking_always=True` /
   `effort_none=False` -- so **gpt-5.5 is not a viable utility model**; it would
   still bill reasoning tokens and still have `temperature` stripped.
   `gpt-5.4-mini` and `gpt-5.4-nano` are both `thinking_always=False` /
   `effort_none=True`, and both are in `KnownModelName`. Cause is
   `pydantic_ai/profiles/openai.py:150-193`:
   `is_gpt_5_1_plus = model_name.startswith(('gpt-5.1','gpt-5.2','gpt-5.3','gpt-5.4'))`,
   and anything matching `gpt-5` outside that window is force-set to
   `thinking_always_enabled=True`.

9. **Reasoning tokens nest *under* output tokens in the artifact, never as a
   sibling.** On the Responses API `output_tokens` already *includes* reasoning
   tokens; pydantic-ai surfaces them separately at
   `RunUsage.details["reasoning_tokens"]`
   (`pydantic_ai/models/openai.py:3076-3078`). Recording them flat alongside
   `output_tokens` double-counts. Schema:
   `{"output_tokens": N, "output_detail": {"reasoning_tokens": M}}`, `M <= N`.

10. **Aggregate by returning usage out of workers, never by mutating a shared
    accumulator.** `RunUsage.incr` in 1.77.0 does plain `+=` with no lock
    (verified by source inspection), and there are four 8-thread pools
    (`card_correctness.py:238`, `image_leak_gate.py:230`, `_common.py:1363`,
    `pipeline.py:2334`) -- a shared accumulator loses rows non-deterministically,
    and an accounting artifact that undercounts under load is worse than none
    because it looks authoritative. Workers return their usage rows and the
    existing `as_completed` loops fold them in on the main thread. The
    module-level ledger still takes a `threading.Lock` on append as a backstop
    for sites outside a pool.

11. **Pin `pydantic-ai>=1.77,<2`** (from `>=0.1` at `pyproject.toml:30`).
    Installed is 1.77.0 with openai 2.30.0, where `input_tokens` /
    `output_tokens` are the live names and `request_tokens` / `response_tokens`
    survive only as `@deprecated` properties plus `AliasChoices` aliases
    (`pydantic_ai/usage.py:22-35, 62-68`). v2.0.0 (2026-06-23) removes those
    aliases, renames `vendor_details` -> `provider_details`, and flips a bare
    `openai:` prefix to Responses -- any of which silently reshapes the ledger.
    (pydantic.dev/docs/ai/changelog, fetched 2026-08-11.)

12. **The artifact goes to `self.output_base`, not `output_dir`.**
    `output_dir` is skipped on `audio_only` reruns, which are exactly the runs
    whose cost this work is meant to explain. `self.output_base` is set
    unconditionally at `pipeline.py:246`.

## Approach

Add the ledger and the wrapper first, then migrate every call site in one
mechanical sweep -- all to `tier="generation"` initially, so the first merge is
behaviour-preserving by construction and a reviewer only checks call shape,
never model choice. Bare `agent.run_sync(...)` callers that used the value
directly now take `.output`; callers already on `with_safety_retry` change one
argument (`model=` becomes `tier=`). Tier resolution reads `models.llm` for
generation and `models.llm.utility` for utility, and validates the tier string
at config load (Gotcha 6).

The ledger is a module-level list of dict rows plus a lock. Each row is
`{label, tier, model, input_tokens, cache_read_tokens, output_tokens,
output_detail: {reasoning_tokens}, requests, tool_calls, failed_attempts}`
(`failed_attempts` per Gotcha 8). At end of run the pipeline writes
`llm-usage.json` under `self.output_base`, merging any existing file so
audio-only reruns append to the same run record, and writing temp-then-rename so
a killed SLURM job cannot leave a truncated artifact. It carries per-call rows
plus rollups by tier and by label: the by-tier rollup validates or falsifies the
85% premise, the by-label rollup identifies the next thing worth moving.

Only after that lands, and after one instrumented chapter has been read, does the
second merge flip the ~10 mechanical sites to `tier="utility"`, add the utility
model to each `swanki/conf/models/*.yaml` preset, and drop `pdf_classifier.py`'s
hardcoded `"openai:gpt-5.4-nano-2026-03-17"`.

Rebase early against the `plan/swanki-corrections-into-source` worktree: it adds
39 lines to `pipeline.py` at `@@ -2224`, `@@ -2404`, `@@ -2493` -- the audio path,
precisely where audio usage capture goes.

## Gotchas

1. **A blind sed over `provider: openai` breaks TTS.**
   `swanki/conf/models/openai_tts.yaml` uses it for the *TTS* block, not the LLM
   block. Edit `models.llm` sub-keys by path, never by pattern.

2. **`temperature: 0.3` goes live for the first time if a site moves tiers.**
   `models.llm.temperature: 0.7` is dead config -- zero reads tree-wide. The
   only real LLM temperatures are three hardcoded `0.3` literals
   (`image_leak_gate.py:123`, `image_processor.py:285`,
   `table_processor.py:115`), and reasoning models *strip* `temperature`, so
   none has ever taken effect. Decision 4 keeps the gate strong, but
   `image_processor` and `table_processor` are utility candidates -- on a
   non-reasoning model their `0.3` suddenly applies. Pin temperature
   deliberately at any site that moves, and eyeball the first outputs.

3. **Do not lower `max_tokens` per tier without a retest.**
   `image_processor`'s 1024 -> 8000 and `table_processor`'s 256 -> 4000 were
   crash fixes: reasoning tokens consume the budget before any visible output
   appears. A cheap non-reasoning model needs less, but that is a measurement,
   not an assumption -- and truncation here fails as a silently empty figure
   description.

4. **`swanki/ocr/reading_order.py` is untracked, not dead.** It shows as `??`
   and holds a bare `run_sync` at :161 -- uncommitted in-flight work from a
   concurrent agent in another worktree. Do not migrate, delete, or stage it.

5. **~5 of the ~25 sites have no `label=`.** Those become unattributable ledger
   rows, defeating the by-label rollup that decides what to move next. Add a
   label at every site during the sweep; there is no second chance this cheap.

6. **A typo'd tier or model name fails silently, not loudly.**
   `gpt-5.6-sol` is not in `KnownModelName`; pydantic-ai falls back to a
   generic profile rather than raising. So a mistyped utility model would run,
   produce plausible output, and quietly behave like an unprofiled model.
   Validate tier strings at config load and log the resolved model string per
   tier once at startup.

7. **`config.get("models", {}).get("models", {})` -- the doubled key is real**
   (Hydra group name nested under the group key), appears 18 times repo-wide,
   and tier resolution must reproduce it. It is also why `docs/cli-usage.md:91`,
   `docs/configuration.md:150` and `docs/quickstart.md:74` are wrong: they print
   `models.llm.model=gpt-4`, but the override that binds is
   `models.models.llm.model=...`. Fix all three -- this plan doubles the
   override strings users will type.

8. **The ledger undercounts retried calls.** `with_safety_retry` re-raises on
   exhaustion and returns only the successful `RunResult`, so tokens burned by
   refused or transient-failed attempts never reach `.usage()`. Record
   `failed_attempts` per row and treat the artifact as a floor on spend, not
   an exact figure.

9. **Do not aggregate usage in a shared `RunUsage` across threads** -- unlocked
   `incr`, four 8-thread pools; mechanism and fix in Decision 10.

## Verification

- `pytest tests/test_config_resolution.py tests/test_agents.py -q` -- all must
  stay green **with no test edits**; any red means the config change stopped
  being additive.
- `pytest tests/test_usage_ledger.py -q` -- new: merge-on-write of an existing
  artifact, concurrent `record()` from 16 threads preserving row count, and
  `output_detail.reasoning_tokens <= output_tokens`.
- `pytest -q` full suite, inside the swanki conda env -- the bare-`PATH` python
  is the base env with pydantic-ai **1.51.0**, so a green run there says nothing
  about the 1.77.0 usage API this work depends on.
- `grep -rn "\.run_sync(" --include="*.py" swanki/` -- the completeness check for
  the sweep: the only tracked hits left should be inside `swanki/llm/safety.py`,
  plus the untracked `swanki/ocr/reading_order.py:161`.
- **Smoke, merge 1:** one chapter via
  `SWANKI_QUEUE_EXECUTOR=slurm scripts/swanki_enqueue.sh --pdf ... --key ...`,
  all sites still on `tier="generation"`. Confirm the deck matches a pre-change
  run for the same input, then read `<output_base>/llm-usage.json`: row count
  in the 800-900 band, and a by-label rollup showing whether mechanical
  transformation really is ~85% of calls. Record that number in this note.
- **Smoke, merge 2:** rerun the same chapter with utility routing on. Per-label
  call counts should be unchanged, the by-tier split should show the expected
  mass on utility, and generation-tier reasoning tokens should drop by roughly
  the mechanical share. Then hand-read a sample of spoken transcripts and
  figure descriptions -- the routing is only safe if the *text* holds up, and
  no test asserts that.
- Confirm `llm-usage.json` appears on an `audio_only` rerun (Decision 12); if
  it lands under `output_dir` it vanishes on exactly those runs.

## Open Questions

1. **Which utility model.** The user mentioned "luna". It does not exist in this
   repo, is not in pydantic-ai's `KnownModelName`, and could not be verified
   anywhere -- so this plan does not invent it. It defaults to **`gpt-5.4-mini`**
   on the `openai-responses` prefix; `gpt-5.4-nano` is the cheaper alternative
   and already runs in production at `pdf_classifier.py:111`, decent evidence it
   suffices for classification at minimum. Both are profile-verified
   `thinking_always_enabled=False`, and swapping between them is a one-line
   change in `swanki/conf/models/*.yaml`. If "luna" is real it must be
   profile-tested first: `thinking_always_enabled` must come back `False`, or it
   is not a utility model whatever it costs -- Decision 8 is where `gpt-5.5`
   fails exactly this test.
2. **Does figure description survive the downgrade?** It is multimodal and
   `image_processor.py` carries a documented invariant that its `model` ctor
   arg is required on purpose. Vision quality on the utility tier is the one
   routing choice in Decision 5 that the merge-1 ledger cannot settle -- it
   needs a hand read of ~10 descriptions before/after.
3. **Should the ledger be aggregated across a book's chapters?** Each chapter
   writes its own `llm-usage.json` under its own `output_base`. A per-book
   rollup would answer "what did this book cost" directly, but nothing in the
   pipeline owns book-level state today. Deferred until the per-chapter
   artifact has proven useful.
