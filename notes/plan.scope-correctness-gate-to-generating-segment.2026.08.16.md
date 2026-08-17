---
id: t1ihf6pyq6zgpo9fjmxnvk8
title: '16'
desc: ''
updated: 1786925911648
created: 1786925911648
---

## Context

The post-generation correctness gate judges every card against the **entire
cleaned chapter**. `_apply_correctness_gate` (`swanki/pipeline/pipeline.py`
1959-1993) calls `_read_source_context()` (1947-1957), which concatenates every
`clean-md-singles/*.md` page, and hands that one string to
`run_correctness_gate` for all N cards. Each card therefore pays full chapter
tokens on input.

That is now measurably the most wasteful line item in a run. The gate is
**25-53% of a run's LLM cost**. For `alcamo CH01`: 46 gate calls x 8,179 input
tokens = 376,230 input tokens carrying roughly 13,600 tokens of unique
information -- **28x amplification**, with 99.2% of every call being re-sent
chapter text and the card itself around 120 tokens.

Prompt caching cannot rescue this -- that was tested, not assumed. Four controlled
experiments (2026-08-14) showed a cache hit requires a **byte-identical prompt**,
not merely a shared prefix: 3/4 hits when identical, 0/4 when the long prefix
matched but the trailing card varied, and `prompt_cache_key` changed nothing
(0/6). The card sits in the prompt tail (`_build_prompt`, card_correctness.py
94-105), so **every gate call differs**. Send less, don't cache more.

The information the judge actually needs is already computed. Card generation
builds a windowed `combined_content` per segment (focal segment plus
`context_radius` neighbours, pipeline.py ~1010-1027) and that window -- not the
chapter -- is literally what the card writer saw. Measured corpus-wide across 228
segmented output dirs / 1906 segments, replacing each card's whole chapter with
its actual window gives: whole chapter (today) **151.8M chars**; radius 2
(`combined_content` verbatim) **43.1M = 71.6% saving**; radius 1 27.7M = 81.7%;
focal-only 9.9M = 93.5%.

This also **restores documented intent**. The founding plan
[[plan.post-creation-llm-card-correctness-gate.2026.06.01]] decision 4 specified
that the gate receives "the originating source segment text plus the
DocumentSummary." The whole-chapter behaviour was a shipped deviation, and the
module docstring in `card_correctness.py` has been describing that deviation as
if it were the design.

Scope: this is a **context-scoping change, not a gate-semantics change**. The
verdict enum, the fail-open path, the audit format, the chokepoint position, and
the config surface all stay exactly as they are. Related but out of scope: issue
`#21` (cross-run carry context injected per run) would introduce a second
mechanism deciding what the judge sees; it is called out under follow-on so the
two are not designed twice.

Campaign sequencing is **decided, not open**: the remaining regeneration campaign
(31 decks, ~$269) is paused; this lands first so all 31 run under one screening
regime, never some chapters against a chapter and others against a window.

## Relevant Files

| Path                                             | Action    | Purpose                                                                                                                                                                                                                                                                                                                       | Stance                                                                                                                                                 |
|--------------------------------------------------|-----------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------|
| `swanki/pipeline/pipeline.py`                    | MODIFY    | Surface `combined_content` from `_generate_cards_for_segment` and page markdown from `_generate_image_cards_for_page`; record a `card_id -> evidence` map at the pooling sites (492 text, 521 image); pass it into the gate from `_apply_correctness_gate` (1959-1993). `_read_source_context` (1947-1957) stays as fallback. | stable (21 dated entries through 2026.08.10; documented invariants: gate sits at the `generate_outputs` chokepoint, callers MUST reassign `all_cards`) |
| `swanki/pipeline/card_correctness.py`            | MODIFY    | Accept a keyword-only per-card evidence map plus the whole-chapter fallback in `run_correctness_gate` (208-247); resolve per card before dispatch. Relabel the source block in `GATE_INSTRUCTIONS` (~37) and `_build_prompt` (94-105) as an originating excerpt. Correct the module docstring.                                | stable but thin (2 dated entries, both 2026.06.01)                                                                                                     |
| `swanki/models/cards.py`                         | REFERENCE | `PlainCard.card_id` (794) is the map key; `ensure_card_id` (893-897) fills only falsy ids and does not enforce uniqueness; `CardCorrectnessAssessment.verdict` (1396) is `Literal["pass","fixed","dropped"]` -- no "cannot verify" escape. No change.                                                                         | stable                                                                                                                                                 |
| `tests/test_card_correctness.py`                 | MODIFY    | ~11 positional `run_correctness_gate(cards, summary, "src", "m")` call sites plus `_verdict_by_front` monkeypatching `_assess_card` positionally; add map-hit, fallback-on-miss, audit-ordering, and collision-warning tests.                                                                                                 | stable                                                                                                                                                 |
| `swanki/pipeline/problem_set.py`                 | REFERENCE | `run_solution_manual_override` returns `tuple[list[PlainCard], ProvenanceLog]` -- the precedent for returning a sidecar alongside cards. Its cards fall back to whole chapter.                                                                                                                                                | stable                                                                                                                                                 |
| `swanki/conf/card_correctness_gate/default.yaml` | REFERENCE | Double-nested `{enabled: true, model: null, max_workers: 8}`. Deliberately **not** extended -- no new key.                                                                                                                                                                                                                    | stable                                                                                                                                                 |
| `swanki/conf/pipeline/*.yaml`                    | REFERENCE | `context_radius` is 2 in `default.yaml`/`book.yaml`/`larger.yaml`, 1 in `standard.yaml`, **0 in `smaller.yaml`**; the call site reads `.get("context_radius", 1)` (pipeline.py 476).                                                                                                                                          | stable                                                                                                                                                 |
| `notes/swanki.pipeline.card_correctness.md`      | MODIFY    | New dated section: window scoping, the docstring correction as a deviation record, the prompt relabel rationale.                                                                                                                                                                                                              | stable                                                                                                                                                 |
| `notes/swanki.pipeline.pipeline.md`              | MODIFY    | New dated section: evidence map lifecycle, pooling-site stamping, the clean-md-singles -> segments corpus swap.                                                                                                                                                                                                               | stable                                                                                                                                                 |

## Key Design Decisions

1. **Reuse `combined_content` verbatim; do not narrow to focal-only.** The whole
   point is that the judge sees *exactly* what the writer saw, which makes the
   change evidentiary-neutral by construction. Narrow further and an unsupported
   card becomes ambiguous between "this is wrong" and "you cropped the proof" --
   and the verdict enum has no way to express that difference, so the ambiguity
   resolves as screening. Verbatim already banks 71.6 of the 93.5 available
   points; the remaining 22 points cost the invariant. Rejected: focal-only
   (93.5% saving) precisely because it breaks the "same evidence" property.

2. **Map both regular/cloze cards and image cards.** Gate traffic by subtype
   across 85 real `correctness-assessment.json` audits (3599 cards) is regular
   58.9%, image 36.3%, problem_main 4.8%. Mapping only regular cards caps
   realized saving near 42%; adding image cards is worth more than any further
   narrowing of regular cards. Image cards get the page markdown that
   `_generate_image_cards_for_page` already reads (~2-3 KB) -- a tighter window
   arrived at by the *same* rule ("record what generation saw"), not a second
   policy.

3. **Problem-set and glossary cards fall back to the whole chapter.** Problem-set
   is 4.8% of traffic and builds its context inside `problem_set.py`, never
   surfacing it to `generate_outputs`; glossary never reaches
   `_generate_cards_for_segment` at all. Threading evidence out of those units
   means new coupling for a rounding error of the saving.

4. **No conditional on segment count.** When a document has fewer segments than
   `2 * context_radius + 1`, the window already *is* the whole segment corpus, so
   the scoped path degrades to the fallback's information content on its own. A
   `if len(segments) <= N: use whole chapter` branch would create two code paths
   and make the "judge sees what the writer saw" invariant true only sometimes --
   which is worse than either path alone.

5. **Accept the `clean-md-singles/` -> `segments/` corpus swap, and document
   it.** `_read_source_context` reads every clean page including
   classifier-rejected front/back matter (TOC, copyright page, index); segments
   are built only from classifier-accepted `main_files`. So the change is not
   purely a cost change -- it is a small, favourable *evidence* change: the
   rejected material was never evidence for any card. Named rather than buried,
   because "identical evidence" is the plan's central claim and this is its one
   honest exception.

6. **No new Hydra config key.** The escape hatch already exists twice over: the
   per-card fallback (a card with no mapped evidence gets the chapter) and `git
   revert`. A `use_segment_context: true` boolean would be flipped to true
   immediately, validated once, and then live forever as dead config.

7. **Correct the `card_correctness.py` module docstring and say so.** It documents
   the shipped whole-chapter behaviour as though it were the design. The docstring
   is a record of a deviation, not a constraint; the dated dendron section should
   state that this change restores documented intent rather than inventing
   behaviour.

8. **Handle `card_id` collisions by non-clobbering insert plus a warning.**
   Collisions are structurally possible -- `card_id` is a declared field on
   `PlainCard` inside `card_gen_agent`'s `output_type`, so the model can emit
   one, and `ensure_card_id` only fills falsy values without enforcing
   uniqueness -- but empirically zero duplicates appeared across 3599 cards.
   First writer wins, log a warning; a collision degrades one card to
   slightly-wrong-but-still-real evidence, never to a crash. Rejected: adding
   uniqueness enforcement to the model, which changes generation behaviour for a
   never-observed condition.

9. **Relabel the source block as an ORIGINATING EXCERPT (required, not
   optional).** This is calibration protection, not cosmetics. The verdict enum
   has no "cannot verify" and the only fail-open path is an exception returning
   `None` from `_assess_card`. A card whose supporting fact now sits just outside
   the window could read to the judge as "the prompt's premise is false" -->
   `dropped`, which is a hard delete from deck, `.apkg`, and audio. The prompt
   must state that the block is an excerpt and that **absence of supporting text
   in it is never grounds for `fixed` or `dropped`.**

## Approach

The evidence a card was written from is computed during generation and then
thrown away. The whole change is: stop throwing it away, carry it to the gate
keyed by `card_id`, and have the gate prefer it over the chapter.

**Surface the evidence at its source.** `_generate_cards_for_segment` (pipeline.py
978) builds `combined_content` at ~1010-1027 and drops it; return both, following
the `(cards, sidecar)` precedent of `run_solution_manual_override`. Same for
`_generate_image_cards_for_page` (~1274), which discards its page markdown.

**Stamp at the pooling sites, keyed by `card_id`.** There are exactly two:
pipeline.py:492 (`all_cards.extend(seg_cards)`) and pipeline.py:521
(`all_cards.extend(page_image_cards)`). Each pooled card gets
`self._card_evidence.setdefault(card.card_id or "", evidence)` into a
`dict[str, str]` held on the `Pipeline` instance: `setdefault` is decision 8's
non-clobbering insert (pair it with a warning when the key is already present),
`or ""` satisfies `mypy --strict` against the `Optional` `card_id` without
touching `models/cards.py`, and keying by `card_id` rather than list position is
load-bearing (gotcha 5).

**Resolve once, then fan out.** `_apply_correctness_gate` (1959-1993) computes
`self._read_source_context()` **exactly once** -- it already does, and this must
not regress into a lazy per-card call, since that re-reads and re-joins up to 46
markdown files per card (kuchel CH05 is 143 KB). It passes that string plus the
now read-only map into `run_correctness_gate` as **keyword-only** arguments.
Inside, resolution is one line per card before dispatch --
`evidence.get(card.card_id) or fallback` -- so the fallback is **per card**, not
"is the map non-empty". That matters because `generate_outputs` is reached from
four sites (pipeline.py:346 solution_manual, :370 glossary, :547 full, plus
audio-only with an empty list), and the first two never call
`_generate_cards_for_segment` at all, so their maps are legitimately empty.

`_assess_card` (108-138) does not change shape: it keeps its four positional
parameters and receives a per-card string in `source_context` where it used to
receive the chapter. Only the *value* changes, not the plumbing (see gotcha 3).

**Prompt.** In `GATE_INSTRUCTIONS` (~37) and `_build_prompt` (94-105), rename
`SOURCE TEXT` to `ORIGINATING EXCERPT` and add decision 9's calibration sentence.
Nothing else moves -- the factual-only, very-high-acceptance framing is what holds
the 98.36% pass rate.

**Nothing is deleted.** `_read_source_context`, the gate's chokepoint position
(call at pipeline.py:2065), the audit writer, and the config all stay; with an
empty map, behaviour is byte-identical to today.

## Gotchas

1. **Only pipeline.py:492 has `combined_content`.** Image cards (:521) carry one
   clean-md page plus per-image context; problem-set cards (:539) build context
   inside `problem_set.py` and never surface it. *Sidestep:* stamp each pooling
   site with the evidence its own producer returns, and never reuse the last
   segment's `combined_content` for a neighbouring extend -- that stamps the
   wrong text.

2. **Two of `generate_outputs`' four callers never segment** (see Approach), so
   they reach the gate with an empty map by design. *Sidestep:* the fallback must
   be per-card (`map.get(card_id) or fallback`); a guard shaped like `if
   self._card_evidence: use scoped path` is wrong in the mixed case and only
   accidentally right in the empty case.

3. **Signature changes break the commit, not just a test.** Pre-commit runs
   `pytest tests/ -x -q` over the whole suite, and `tests/test_card_correctness.py`
   has ~11 positional `run_correctness_gate(cards, summary, "src", "m")` calls
   plus a `_verdict_by_front` fake bound to `_assess_card`'s positional
   `(card, source_context, doc_summary, model_string)`. *Sidestep:* new
   parameters are keyword-only with defaults; `_assess_card`'s first four
   positional parameters keep their order and meaning; the map reaches
   `_apply_correctness_gate` via `self`, not a new positional argument (line
   262/283 stubs it as `fake_gate(cs, doc_summary, out)`).

4. **The gate is concurrent -- `ThreadPoolExecutor(max_workers=8)`.** A
   fully-populated, read-only `dict[str, str]` is safe under the GIL. It stops
   being safe the moment a worker mutates it. *Sidestep:* populate the map
   entirely during generation; resolve each card's evidence on the **submitting**
   thread before `executor.submit`; never call `_read_source_context()` inside a
   worker and never lazily backfill the map from inside `_assess_card`.

5. **`seg_idx` and list position diverge.** The biosec `continue` at
   pipeline.py:481-491 drops an entire segment's cards mid-loop. *Sidestep:* key
   the map by `card_id` only. Do not build a parallel list aligned to `all_cards`
   and do not index evidence by segment ordinal downstream.

6. **`_self_refine_cards` mints new uuids.** It returns brand-new `PlainCard`
   objects with new ids, and it runs at pipeline.py:1227/1238/1448/1766 -- all
   **before** the pooling sites, which is why stamping at pooling is correct
   today. *Sidestep:* this is a latent invariant, so make it visible: a comment
   at the stamp site stating that any move of refinement or dedup to after
   pooling silently invalidates every key (symptom: 100% fallback, no error).

7. **Pre-commit runs `mypy --strict` on `^swanki/`, baseline clean since 60c1da8.**
   *Sidestep:* annotate the instance attribute explicitly as `dict[str, str]` and
   the new gate parameter as `dict[str, str] | None`. (`check-frontmatter` also
   runs, so keep the docstring's header block intact while editing it.)

8. **`context_radius` has two defaults and one profile sets it to zero.**
   `swanki/conf/pipeline/default.yaml` sets 2, but the call site reads
   `processing_config.get("context_radius", 1)` (pipeline.py:476). *Sidestep:* do
   not write "radius 2" as a guarantee anywhere in code comments or notes -- say
   "the configured radius". Under `smaller.yaml` (`context_radius: 0`) the judge
   sees a single ~6k-char segment; that is still invariant-preserving, because
   the writer also saw only that segment.

9. **Cloze cards need no special handling.** They interpolate the same
   `combined_content` and merge before the single return, so they are mapped for
   free; with `cloze_per_segment: 0` in `default.yaml`/`book.yaml` they are
   correctness-relevant, not cost-relevant. *Sidestep:* no separate code path.

10. **`plan/swanki-corrections-into-source` is in flight in the same files** --
    `pipeline.py` (hunks ~2224/2433/2527) and `models/cards.py` (~1353). No line
    overlap with the regions here, but `pipeline.py` is ~3000 lines, so whichever
    branch lands second rebases against shifted offsets. *Sidestep:* rebase onto
    `main` immediately before enqueueing.

11. **Issue `#21` (cross-run carry context) overlaps conceptually** -- it injects a
    per-run object into prompts, making "what the judge sees" a shared concern.
    *Sidestep:* follow-on only; when `#21` lands, resolve the evidence map and the
    carry object at one place in `_apply_correctness_gate`, not via two mechanisms
    that each think they own the gate's context.

## Verification

- **Regression yardstick (the primary gate on this change).** Re-run the gate
  after the change and require a pass rate at or above ~98% with **zero drops**.
  The historical baseline across 85 audits / 3599 cards is 98.36% pass, 1.56%
  fixed, 0.08% assessment_failed, and zero dropped, ever. A first-ever drop is
  the over-screening signal and blocks the change until the prompt relabel is
  re-tuned.

- **Validate on a large segmented document -- alcamo cannot demonstrate this.**
  `alcamo CH01` has 3-5 segments, so its window *is* the whole document and the
  saving is structurally invisible there. Use
  `feldmannYeastMolecularCell2012_CH05` (48 segments, 269 KB chapter -> ~27 KB
  windows, ~10x reduction) or `kuchelSchaumOutlineBiochemistry2011_CH05` (25
  segments, ~5x). This is a hard requirement, not a preference.

- **Cheap end-to-end diff.** Re-run the gate over an existing chapter's already
  generated cards and diff the verdicts against the `correctness-assessment.json`
  already on disk for that chapter. Expected: near-identical verdicts, dramatic
  input-token drop. Any verdict that moves from `pass` to `fixed`/`dropped` gets
  read by hand before proceeding.

- **Unit tests** (`tests/test_card_correctness.py`):
  - map hit routes correctly -- a mapped card is judged against **its own**
    context, not the chapter (assert on the string `_assess_card` receives);
  - per-card fallback on miss -- a mixed list where only some cards are mapped
    sends the chapter for exactly the unmapped ones;
  - the audit still has exactly one entry per input card **in input order**
    under concurrency (`max_workers > 1`), unchanged from today's contract;
  - a duplicate `card_id` logs a warning and keeps the first writer's evidence.

- **Cost confirmation.** Compare per-run input tokens and USD from the run-cost
  instrumentation (705d5bb) before and after on the same document. Expect the
  corpus-measured ~71.6% cut in gate input characters at radius 2 (more at radius
  1 under `standard.yaml`), and near zero where the window is already the document.

- **Post-merge**: unpause the regeneration campaign only after the large-document
  validation and the zero-drop check both pass, so all 31 remaining decks are
  screened under one regime.
