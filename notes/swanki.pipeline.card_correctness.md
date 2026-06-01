---
id: ntbjx05ean49k0o2wm3ay8a
title: Card_correctness
desc: Post-generation LLM correctness gate — keep/fix/quarantine each card, audit every verdict
updated: 1780333110918
created: 1780333110918
---

## 2026.06.01 - Initial implementation

Opt-in correctness gate addressing the "faithful but wrong" failure: a card can be a perfect transcription of the source and still teach a falsehood. The anchor case is an Alcamo Schaum's Microbiology CH02 multiple-choice card ("A hydrogen bond is a weak bond forming between (a) three pairs of electrons ... (d) protons and three pairs of electrons") that is verbatim from the textbook yet chemically nonsensical. Plan: [[plan.post-creation-llm-card-correctness-gate.2026.06.01]].

**Entry point.** `run_correctness_gate(cards, doc_summary, source_context, model_string, *, max_workers=8) -> (kept_cards, audit)`. Each card is assessed independently and concurrently (`ThreadPoolExecutor`, mirroring `markdown_converter`). `card_correctness_agent` (in [[swanki.llm.agents]]) returns a `CardCorrectnessAssessment` with `verdict ∈ {pass, fixed, dropped}` plus a reason and, for `fixed`, corrected front/back. Every call is wrapped in `with_safety_retry` ([[swanki.llm.safety]]) because microbiology content reliably trips the biosec `invalid_prompt` refusal.

**Verdict resolution.** `pass` keeps the card unchanged; `fixed` keeps a `model_copy` with corrected `front`/`back` text; `dropped` excludes the card (quarantine-from-deck — it never reaches markdown/.apkg but its full original content is logged); `assessment_failed` keeps the card fail-open. `assessment_failed` is assigned by the gate when `_assess_card` returns `None` (the call raised after retries) — the agent never returns it. We never silently drop an unjudged card; precedent is the per-segment skip-on-exhausted-retry (commit `14fbfab`).

**Why a single late stage at the `generate_outputs` chokepoint.** All three card-producing branches (`solution_manual`, `glossary`, `full`) funnel into `Pipeline.generate_outputs`. Gating once there (via `_apply_correctness_gate`, before any markdown/.apkg is written) covers every mode with one integration point and keeps the position-keyed sibling artifacts (`cards-plain.md`, etc.) consistent because they are all written from the post-gate kept-list. Wiring into each upstream branch was rejected: two of the three are in-flux and it triples merge surface for no gain.

**Source context is required.** Card text alone cannot separate "faithful but wrong" from correct, so the gate reads the cleaned source (`clean-md-singles/*.md`, joined by `Pipeline._read_source_context`) plus the `DocumentSummary`. The prompt instructs the model to judge against established reality, not fidelity to the source.

**Model + config.** Reuses `get_model_string(models.llm)` by default (`gpt-5.5`); a nullable `card_correctness_gate.model` override pins a stronger model even if a run downgrades the main model for cost. Hydra group `swanki/conf/card_correctness_gate/`, `enabled: false` by default (one model call per card; opt in per run with `card_correctness_gate.enabled=true`).

**Audit.** `write_audit` dumps a `summary` count block plus one `CardAuditEntry` per card to `<output_base>/correctness-assessment.yaml`, atomically (temp-then-rename). Sibling to `provenance.yaml`; never written into the Anki `Feedback` field or `PlainCard.user_feedback` (those are the review-time human-triage channel and part of the GUID seed). Fixing pre-export is GUID-safe — a corrected card gets its natural GUID in a fresh deck with no review history to lose; holding a GUID stable across a fix is the paused unify-regen problem and is out of scope.

Tests in `tests/test_card_correctness.py` monkeypatch `_assess_card` per card (no live LLM) to cover pass/fixed/dropped/assessment_failed, audit completeness, input-order preservation under concurrency, empty input, all-dropped, and atomic audit write.
