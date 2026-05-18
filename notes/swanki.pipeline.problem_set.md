---
id: fdrhn9xj7mabuv9r5olalvz
title: Problem Set Pipeline
desc: Solution-manual mode core — enumerate, pair, resolve refs, generate cards, audit coverage. Used by mode=solution_manual override and (future) classifier-driven mode=full per-section routing.
updated: 1777607710601
created: 1777607710601
---

## 2026.04.26 - Initial implementation

Foundation module for `mode=solution_manual` (whole-document override path). Six top-level functions:

1. **`enumerate_problems`** — regex-first, pulls `^\d+\.\d+\b` blocks from cleaned markdown, splits each into statement (first paragraph) + solution (rest). LLM fallback (`problem_enumeration_agent`) is wired but not yet exercised; v1 relies on regex.
2. **`pair_problems_across_pages`** — three-stage pairing:
   - **Stage 0:** initialize one `ProblemPairing(statement, solutions=[])` per enumerated problem. Stage 0 guarantees `len(pairings.pairings) == len(problems)` so audit Part 1 is meaningful.
   - **Stage 1:** lift inline solutions (Schaum's `1.1` Q&A) into the pairing.
   - **Stage 2:** regex on `^Solution\s+N\.M` and `^Chapter\s+N\s*\nMultiple Choice` back-of-book blocks.
   - **Stage 3:** wired (`problem_pairing_agent`) but not yet exercised — reserved for Bishop with worked-solutions PDFs that lack explicit `Solution N.M` markers.
3. **`resolve_references`** — inlines `equation (X.Y)` / `Theorem X.Y` text from `ChapterIndex` into problem.statement and problem.solution. Collects `Figure X.Y` references into `problem.referenced_figures` for image attachment on cards.
4. **`classify_card_plan`** — heuristic-only in v1 (no LLM). Subproblem-driven (`(a)/(b)/(c)` parts) → 1 main + N subs (capped at 3). Long single-part problems (`char_count > long_problem_chars`, default 4000) → 2 cards (main + overview). Else → 1 main card.
5. **`generate_cards_for_problem`** — calls `problem_card_gen_agent`. Stamps `card_subtype` from the plan in order (the LLM defaults to `"regular"` in `PlainCard`, so trusting the plan is more robust than trusting the LLM). Appends the canonical `<citation_key>.problem.<id>` tag (audit Part 3 keys on it via `ProblemTag.parse`). Honors `enable_full_solution_cards` flag (downgrades the plan if disabled, default off).
6. **`audit_coverage`** — three-part hard-fail before APKG export:
   - **Part 1:** every enumerated problem appears in `pairings.pairings`.
   - **Part 2:** every pairing has ≥1 solution unless `allow_unsolved=True` (default False — zero tolerance).
   - **Part 3:** exactly one `card_subtype="problem_main"` card per paired problem, parsed via `ProblemTag` (catches missing, extra, AND duplicate via `Counter`).
7. **`run_solution_manual_override`** — whole-document orchestrator called from `Pipeline.process_full` when `mode=solution_manual`. Persists `problem-pairings.yaml` and `cards-debug.yaml` BEFORE the audit so failures preserve the LLM output for inspection.

**First end-to-end run:** Schaum's Microbiology Ch1 (PDF pages 8-18 chapter + page 328 back-of-book answer key) produced 30 `problem_main` + 1 `problem_overview` card via 30+1 LLM calls. Audit passed; the artifacts landed in `<key>-problem-set.apkg`. The cards-debug + pairings-yaml dump caught the original `card_subtype` defaulting bug (LLM was emitting cards without `card_subtype`, audit fired correctly with "30 problems missing from cards"); fix was to stamp the subtype from the plan after the LLM call.

**Deferred to follow-up:** classifier-driven `mode=full` per-section routing (`run_problem_set_for_section` is not yet implemented), Stage-3 LLM pairing fallback, and overlap-aware modulation of the prose card-gen pipeline.

## 2026.05.04 - MC / Matching / True-False / Completion enumeration

Added four new enumerator helpers to `enumerate_problems` (`_enumerate_multiple_choice`, `_enumerate_matching`, `_enumerate_true_false`, `_enumerate_completion`) plus four new pairing branches that share a unified back-of-book partition pattern. Each subtype gets a chapter-prefixed problem ID (`MC-CH{n}-{m}`, `MAT-CH{n}-{m}`, `TF-CH{n}-{m}`, `CMP-CH{n}-{m}`) and routes through the existing `problem_card_gen_agent` with a subtype-specific system prompt selected via the `_PROMPT_KEY_BY_SUBTYPE` dispatch in `generate_cards_for_problem`.

The legacy `_MC_ANSWER_BLOCK` regex was removed and replaced with the partition + per-section loop pattern. The original regex required immediate adjacency between `^Chapter N` and `Multiple Choice`, which never matched the actual Mathpix output `## Chapter 1\n\n## Multiple Choice\n\n1. c 2. c ...` (markdown-promoted H2 headers, NOT bare text). Verified empirically by inspecting `problem-pairings.yaml` from the alcamoSchaumsOutlineMicrobiology2010_CH01_6 run, which had every back-of-book MC entry stranded in `unpaired_solutions: []`. The new `_partition_back_of_book` helper walks every `^## Chapter N$` boundary, then within each chapter span scans `^## (Multiple Choice|Matching|True/False|Completion)$` to build a `{chapter: {section: body}}` map. The pairing loop iterates that map.

True/False solutions render as `"True."`, `"False."`, or `"False — replace underlined word with: <word>"`. The originally-underlined word is NOT recoverable from Mathpix OCR (the markup is dropped); the card design accepts this and lets the learner self-identify the underlined word by comparing the statement to the back-of-book correction.

Completion items require a `$\_\_\_\_$` token (Mathpix's blank rendering) in the body to be enumerated; numbered prose without a blank is correctly skipped. Multi-word answers in the back-of-book block (e.g. `organic compounds`, `peptide bond`, `dehydration synthesis`) are handled by `_CMP_ANSWER_SPLIT`, a non-greedy regex that allows answers to contain spaces. The Mathpix blank-token form is `\$(?:\\_)+\$` (alternating backslash-underscore pairs) — NOT `\$\\_+\$` which would not match.

Two adjacent fixes landed with this work:

- `_THEORY_PROBLEM` lookahead extended to terminate on review-section dividers and the back-of-book chapter header. Without this, the last theory-problem (e.g. `1.30`) greedy-tail-captured the entire MC + Matching + T/F + back-of-book content (~6900 chars) as its solution body.
- `_try_pair_or_unpaired` helper guarantees every parsed back-of-book answer either pairs OR appends to `unpaired_solutions`. The legacy Stage 2b loop dropped unmatched entries on the floor, which would have masked the OCR-drift case where Schaum's CH01 Matching item 5 is missing from the question section but still has an answer in the back-of-book.

`_extract_column_b` resolves the in-chapter Column B option list. Initial implementation found the back-of-book `## Chapter 1` header (page 12) instead of the in-chapter content (page 1) when the input was the review-section subset (no forward `# CHAPTER 1` heading present). Fix: scope the chapter-heading search to the span BEFORE `^## Answers to Review Questions`. Verified the pairings now carry full Column B option text — `MAT-CH1-1` solution is `(c) Viruses`, not just `(c)`.

`run_solution_manual_override` now writes `problem_subtype_counts` alongside `subtype_counts` to `cards-debug.yaml` so the integration smoke test can assert `{theory_problem: 6, multiple_choice: 15, matching: 9, true_false: 15}` for the Schaum's CH01 review-section subset.

End-state target: alcamoSchaumsOutlineMicrobiology2010 Ch1 review-section subset (pages 8-12) enumerates 45 problems (15 MC + 9 Matching + 15 T/F + 6 theory `1.25-1.30`) with every problem paired. The full chapter (pages 1-12) enumerates 69 problems (30 theory + 15 MC + 9 Matching + 15 T/F).

## 2026.05.17 - Tighten bolding rules in card-gen prompts

The prior rule "use **bold** on key technical term(s)" was too loose — the LLM bolded any technical word it saw, so cards like T/F 6 came out with both `**Fungi**` and `**prokaryotes**` bolded. Only `prokaryotes` is testable here (it's the swap word the back-of-book corrects to `eukaryotes`); `Fungi` is incidental list context that bolding falsely flagged as important.

Tightened the five card-gen prompts (theory + MC + Matching + T/F + Completion in `solution_manual.yaml`, plus the concept-card prompt in `default.yaml`) with subtype-specific guidance:

- **T/F**: bold ONLY the swap word for False statements; the single testable concept for True; 1-2 words max. Worked example baked into the prompt.
- **MC**: bold the central noun phrase the stem is testing, NOT scientist names or named entities.
- **Matching**: bold ONLY the two domain nouns in the prefix (`Match the **<domain>** to the **<target>**:`).
- **Completion**: bold only the context words immediately adjacent to `____`.
- **Theory** + **concept cards**: bold sparingly, only what the card is actually testing.

Universal rider: "Bolding everything trains the learner to ignore the emphasis." No new tests — these are LLM-judgment rules; verification is inspecting `cards-debug.yaml` after regen.

Two additional Matching-prompt revisions in the same round:

- **Drop the colon + em-dash construction**. Prior format put the Column-A statement under the question on its own line prefixed by `—` (e.g. "Match the **microorganism group** to the **capability**:\n— Performs photosynthesis"). The two-step framing is awkward to read. New rule: rewrite the Column-A statement as a direct question that integrates the Column-B domain (e.g. "Which **microorganism group** performs photosynthesis?"). Three worked examples included in the prompt to anchor the LLM.
- **Period after the answer phrase on the back**, before the rationale sentence. Prior cards came out as "(e) **Cyanobacteria** Cyanobacteria are photosynthetic..." — no terminator between the answer and the explanation, which both reads and TTS-renders as a run-on. Same period rule added to MC and Completion backs for consistency; T/F already used periods in its example forms.
