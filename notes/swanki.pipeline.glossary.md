---
id: glspipelineglossary0001
title: Glossary Pipeline
desc: mode=glossary core — LLM-assisted enumeration, definition card plan, batched card-gen, hard-fail coverage audit
updated: 1779321600000
created: 1779321600000
---

## 2026.05.21 - Initial implementation

`run_glossary_override` is the whole-document runner for `mode=glossary`, mirroring [[swanki.pipeline.problem_set]] minus the statement/solution pairing and reference resolution — a glossary term and its definition are co-located, so there is nothing to pair.

Functions:

1. `enumerate_glossary` — LLM-assisted (not regex). Concatenates the per-page markdown and asks `glossary_enumeration_agent` for one `GlossaryUnit` per headword. LLM-assisted because MinerU's per-page layout for a dense two-column wordlist is not regex-stable (and OCR is always-on, default `ocr=mineru`).
2. `classify_definition_plan` — heuristic, returns one `definition_main` card per term in v1. `long_entry_chars` is the hook for the future encyclopedia elaboration upgrade; GRE entries are short and map to a single card.
3. `generate_cards_for_terms` — batches `batch_size` terms per `definition_card_gen_agent` call (each term needs no shared context). Stamps `card_subtype="definition_main"` and the canonical `GlossaryTag` from CODE after the LLM call (the LLM defaults `card_subtype` to "regular" and does not know the tag scheme — trust the structure, not the LLM), and drops surplus cards so nothing untagged ships. Card shape: front `**term**`; back = definition sentence + an `*e.g.*` usage-example line; back capped at 500 chars by `CardContent`.
4. `audit_coverage` — hard-fail. Exactly one `definition_main` card per enumerated term, keyed via `GlossaryTag.parse` and counted with `Counter` so it catches missing, duplicate, AND extra term slugs. Reuses `CoverageError` from problem_set.
5. `run_glossary_override` — enumerate -> plan -> generate -> dump `glossary-units.yaml` + `cards-debug.yaml` BEFORE the audit (so a hard-fail preserves the evidence) -> audit -> return cards.

Wired into `Pipeline.process_full` as a new `elif mode == "glossary":` dispatch branch parallel to `solution_manual`; the classifier is bypassed. Hydra groups: `pipeline=glossary`, `prompts=glossary`, `output=glossary` (`-vocab` apkg suffix). Audio and apkg export are card-format-agnostic and unchanged.

Scope: GRE wordlist only. The encyclopedia profile (length-driven short-def + elaboration cards) and a `glossary` SectionKind for `mode=full` routing of glossary sections inside mixed documents are deferred. See [[plan.glossary-definition-cards-gre-wordlist.2026.05.21]].
