---
id: n9xanvmt03qzjlcthbjgat0
title: '01'
desc: ''
updated: 1780331910105
created: 1780331910105
---

## Context

Swanki faithfully transcribes source material into flashcards, but faithful is not the same as correct. A book can be wrong, or a card can reproduce a question whose own premise is chemically nonsensical, and the current pipeline will happily ship it. The motivating case is an Alcamo Schaum's Microbiology multiple-choice card, generated verbatim from the chapter:

> "A hydrogen bond is a weak bond forming between (a) three pairs of electrons (b) protons (c) protons and neutrons (d) protons and three pairs of electrons" — answer "(d)..."

The card is a perfect reproduction of the textbook and still teaches a falsehood: a hydrogen bond is an electrostatic interaction between a hydrogen already bonded to an electronegative atom and a lone pair on another, not "protons and three pairs of electrons." A learner who trusts the deck memorizes nonsense. We want a learner-trust guarantee: every card that lands in the deck has been checked by the strongest configured model, and every card that was checked has a logged verdict and reason.

This plan adds a post-card-creation LLM correctness gate. After cards are generated (all generation modes), each card is independently assessed by the configured model (`gpt-5.5` in `swanki/conf/models/default.yaml`). Per card the verdict is: keep as-is (pass), repair and keep (fixed), or remove from the deck (dropped). Every verdict plus reason is written to a machine-readable audit YAML so the deck is auditable. The gate is deterministic and fully Pydantic-modeled, per repo convention (models over prompts).

This is adjacent to the glossary carry-context work (`#21`) only in that definition cards are explicitly in scope — a wrong definition is precisely the failure this gate exists to catch — but the gate does not depend on or reopen that work.

## Relevant Files

| path | action | purpose | stance |
| --- | --- | --- | --- |
| `swanki/pipeline/card_correctness.py` | NEW | `run_correctness_gate()` — per-card concurrent assessment, returns kept list + audit | n-a |
| `swanki/conf/card_correctness_gate/default.yaml` | NEW | Hydra config group: `enabled`, nullable `model` override | n-a |
| `tests/test_card_correctness.py` | NEW | unit tests with mocked agent + Alcamo smoke check | n-a |
| `notes/swanki.pipeline.card_correctness.md` | NEW | paired dendron module note + dated rationale section | n-a |
| `swanki/models/cards.py` | MODIFY | add `CardCorrectnessAssessment` + `CardAuditEntry` Pydantic models | stable |
| `swanki/llm/agents.py` | MODIFY | add `card_correctness_agent`, model via `get_model_string` + override | stable |
| `swanki/pipeline/pipeline.py` | MODIFY | call gate as a late stage inside `generate_outputs` (~line 533/1904) | in-flux |
| `swanki/llm/safety.py` | REFERENCE | `with_safety_retry(agent, prompt, instructions=, model=, label=)` wraps each call | stable |
| `swanki/processing/apkg_exporter.py` | REFERENCE | consumes the post-gate kept list; GUID = sha256(Front, Back, Feedback) | stable |
| `swanki/pipeline/problem_set.py` | REFERENCE | `audit_coverage()` runs before the gate; enumeration/pairing already sealed | in-flux |
| `swanki/conf/models/default.yaml` | REFERENCE | pins `model: gpt-5.5`; gate's default model resolves from here | stable |

## Key Design Decisions

1. **Single late stage at the `generate_outputs` chokepoint, not wired into the three upstream paths.** The `solution_manual` (~337), `glossary` (~359), and `full` (~533) branches all funnel into `self.generate_outputs(all_cards, doc_summary, output_base)`. Gating once at that chokepoint covers every mode with one integration point. Rejected: wiring into each branch — those paths are in-flux (heavy May 2026 biosec work) and three integration points triples the merge surface for no gain.

2. **Drop means quarantine-from-deck: remove from the kept list AND log full content.** An unfixable card is removed from the list passed to markdown/APKG (satisfies "do not add to deck") but its complete front/back plus reason are recorded in the audit YAML. Nothing is silently discarded; a human can review every dropped card. Rejected: leaving a placeholder in-list — it would still reach the deck.

3. **Position-keyed sibling artifacts are written FROM the post-gate kept list.** `cards-plain.md`, `cards-debug.yaml`, and `problem-pairings.yaml` are written by index/position. Dropping a card mid-list shifts those indices. Writing them after the gate from the filtered list keeps every count and position consistent. Audio is keyed by `card.card_id` UUID and is therefore index-safe regardless.

4. **Source context is REQUIRED input to the gate.** Card text alone cannot distinguish "faithful but wrong" from correct — the Alcamo card is internally well-formed. The gate receives the originating source segment text plus the `DocumentSummary` (both in scope at `generate_outputs` time; `doc_summary` is already threaded through every branch). Without source context the model would have to rely on parametric knowledge alone, which is exactly the weakness we are guarding against.

5. **Fixing pre-export is safe; the gate must NOT attempt stable-GUID-across-fix.** GUID = `sha256(Front \x1f Back \x1f Feedback)`. The gate runs strictly before APKG export, so a corrected card simply gets its natural GUID in a fresh deck — there is no prior review history to preserve. Attempting GUID stability across a text change is the paused unify-regen problem (`project_card_unify_regen.md`, paused 2026-05-31) and is explicitly out of scope. The audit logs before-and-after text so no fix is silent.

6. **Reuse `get_model_string(llm_config)` with a nullable per-gate override.** By default the gate uses the same model the rest of the pipeline uses (`gpt-5.5`), so no model name is hardcoded. A nullable `card_correctness_gate.model` lets a run pin the gate to a stronger model even if a cost-saving run downgrades `models.llm.model`; unset falls back to the main model.

7. **Per-card concurrent assessment, not one batch mega-prompt.** Independent per-card calls keep each judgment focused on one card + its source, isolate safety-retry/biosec handling per card, and make verdicts reproducible. Calls are dispatched concurrently with a bounded pool (the codebase already uses parallel TTS dispatch). Rejected: a single batched prompt — it blurs judgments across cards and makes per-card retry/logging awkward.

8. **Fail OPEN.** A card whose assessment errors or exhausts safety retries is logged with verdict `assessment_failed` and KEPT in the deck. We never silently drop a card we could not judge. Precedent: commit `14fbfab` (per-segment skip-on-exhausted-retry).

9. **All card subtypes are in scope.** The Alcamo case is a plain multiple-choice concept card, so a problem-set-only gate would miss it. Concept, problem-set (`problem_main`/`subproblem`/`full_solution`), definition, and image cards are all assessed. Image cards are judged on text plus `image_summary`, never on pixels.

## Approach

The gate lives in a new module `swanki/pipeline/card_correctness.py` exposing one entry point:

```python
def run_correctness_gate(
    cards: list[PlainCard],
    doc_summary: DocumentSummary,
    source_context: str,
    llm_config: DictConfig,
    gate_config: DictConfig,
) -> tuple[list[PlainCard], list[CardAuditEntry]]:
```

It returns a plain filtered list of kept cards (NOT a `CardGenerationResponse` — that model's `validate_card_count` requires >=1 card and must not re-validate the gate output) plus an audit entry per input card.

**Flow.** For each input card, build a per-card prompt containing the card front/back (and `image_summary` for image cards), the matching source segment text, and the document summary, then call `card_correctness_agent` through `with_safety_retry(agent, prompt, instructions=..., model=get_model_string(...), label="card_correctness")`. The agent returns a `CardCorrectnessAssessment` with a `verdict` Literal and a `reason`; when the verdict is `fixed` it also carries corrected front/back. Calls are dispatched concurrently with a bounded worker pool (reuse the existing parallel-dispatch pattern) so ~61–70 cards/chapter complete in reasonable wall time without flooding the provider. Results are reassembled in input order.

The verdict type is the load-bearing contract:

```python
verdict: Literal["pass", "fixed", "dropped", "assessment_failed"]
```

Resolution per verdict: `pass` keeps the card unchanged; `fixed` keeps a copy of the card with `front`/`back` replaced by the corrected content; `dropped` excludes the card from the kept list; `assessment_failed` keeps the card (fail-open). Every card — including dropped — produces a `CardAuditEntry` recording its identity (`card_id`, subtype), verdict, reason, and for fixed/dropped the original (and for fixed, corrected) text.

**Integration at the chokepoint.** Inside `Pipeline.generate_outputs` (called from all three branches, e.g. line 533 for `full`), before any markdown/APKG is written, call `run_correctness_gate(all_cards, doc_summary, source_context, llm_config, gate_config)`. The returned kept list becomes the list every downstream writer consumes, so the position-keyed artifacts and the deck stay consistent by construction. The problem-set `audit_coverage()` hard-fail audit has already run upstream, so enumeration and pairing are sealed before the gate touches anything.

**Hydra config group.** New group `swanki/conf/card_correctness_gate/default.yaml` with `enabled: <bool>` and `model: null` (nullable override). Resolved model = `card_correctness_gate.model` if set else `get_model_string(llm_config)`.

**Audit YAML.** Written atomically to `<output_base>/correctness-assessment.yaml` as a list of `CardAuditEntry` dumps. Overwritten each run (no cache in v1). Sibling to the existing `provenance.yaml` / `cards-debug.yaml` — the gate log is a separate file and never mixes into provenance.

The agent definition in `swanki/llm/agents.py` mirrors the existing `card_gen_agent` pattern: `Agent(output_type=CardCorrectnessAssessment, retries=3)`, model selected per-call via `get_model_string`. The new Pydantic models go in `swanki/models/cards.py` next to the existing card models.

## Gotchas

1. **Index shift on drop (CRITICAL).** `cards-plain.md`, `cards-debug.yaml`, and `problem-pairings.yaml` are position-written; removing a card mid-list desyncs them. Sidestep: write all position-keyed artifacts from the post-gate kept list. Audio is `card_id`-keyed and safe.

2. **Card text alone is insufficient (CRITICAL).** The Alcamo card is internally well-formed yet wrong. Sidestep: source segment text + `DocumentSummary` are required arguments to `run_correctness_gate`; do not call it without them.

3. **GUID change on fix is fine because the gate is pre-export.** A fixed card gets a new `sha256(Front, Back, Feedback)` GUID, but in a fresh deck with no prior review history nothing is lost. Do NOT try to hold the GUID stable across a fix — that is the paused unify-regen problem (`project_card_unify_regen.md`); leave it paused.

4. **Fail-open, never drop an unjudged card.** Assessment error / exhausted safety retries → verdict `assessment_failed` → card KEPT. Do not let an exception or empty agent result silently remove a card.

5. **Do NOT re-validate through `CardGenerationResponse`.** Its `validate_card_count` requires >=1 card; passing the gate's filtered list through it would crash when the kept list is legitimately small. The gate returns a plain `list[PlainCard]`.

6. **Empty-after-gate edge case.** If every card is dropped, the kept list is empty. Downstream writers and APKG export must tolerate zero cards (log a clear warning); the gate itself must not raise on an empty result.

7. **Do NOT touch the Anki Feedback field, `PlainCard.user_feedback`, or GUID derivation.** The Feedback field is ord 2 in the APKG/AnkiConnect and is part of the GUID seed; `user_feedback` is a review-time human-triage field authored inside Anki. The gate audit goes ONLY to `correctness-assessment.yaml`, never into a card field.

8. **mypy strict on the new core module.** Use explicit types throughout `card_correctness.py` (the `tuple[list[PlainCard], list[CardAuditEntry]]` return, the verdict Literal). Run `/mypy` before handoff. pydantic.mypy plugin is enabled.

9. **gilahyper conda env may be stale.** pydantic-ai is pinned loosely (`>=0.1`); verify the gate against the live env at `~/miniconda3/envs/swanki` before claiming it runs. Do not use pydantic-ai features that are not present in the installed version.

10. **Atomic audit write, modeled.** Write `correctness-assessment.yaml` via a temp-file-then-rename so a crashed run never leaves a half-written audit. Each entry is a `CardAuditEntry` dump, not an ad-hoc dict.

11. **Definition / glossary cards are in scope, not exempt.** A wrong definition is exactly the target failure; do not special-case them out.

## Verification

- Unit tests in `tests/test_card_correctness.py` with the agent mocked to return each verdict:
  - `pass` → card unchanged in kept list, audit entry verdict `pass`.
  - `fixed` → kept card carries the corrected front/back; audit logs original + corrected text.
  - `dropped` → card absent from kept list; audit entry has verdict `dropped` and the full original content.
  - `assessment_failed` → card KEPT (fail-open); audit verdict `assessment_failed`.
  - Audit has exactly one entry per input card (every card logged).
  - Count consistency: `len(kept) + len(dropped)` equals input count; position-keyed artifacts built from kept list match.
  - Empty-after-gate: all cards dropped → empty kept list, no exception.
- Alcamo smoke check: feed the real CH02 hydrogen-bond multiple-choice card with its source segment and confirm the live gate returns `dropped` (or `fixed`) with a chemically sound reason — not `pass`.
- `/mypy` and `/ruff` clean on the new and modified files.
- End-to-end run with the gate enabled on a small chapter; confirm `correctness-assessment.yaml` is written, deck card count equals kept count, and dropped cards are absent from the APKG.

## Open Questions

- Should the gate default to enabled or disabled in `card_correctness_gate/default.yaml`?
- Confirm fail-open is the desired posture (keep unjudged cards) versus fail-closed (drop on assessment failure)?
- Assess image cards (text + `image_summary`) in v1, or defer image cards to a later pass?
