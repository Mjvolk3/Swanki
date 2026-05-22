---
id: glsdefcardgrewl20260521
title: Glossary Definition Cards - GRE Wordlist
desc: 'mode=glossary definition-card generation, mirroring problem_set; GRE wordlist only, encyclopedia deferred'
updated: 1779321600000
created: 1779321600000
---

## Goal

Add a `mode=glossary` whole-document override that turns a vocabulary/definition PDF into one Anki card per term (front = word, back = definition + an LLM-generated example sentence). Architecture mirrors `mode=solution_manual` / `problem_set` 1:1. Scope this work to the GRE wordlist (`/scratch/ManPrep1000GREwords/ManPrep1000GREwords.pdf`, citation_key `ManPrep1000GREwords`) only. The encyclopedia (`sarkarPhilosophyScienceEncyclopedia2005`), the `glossary` SectionKind for `mode=full` routing, length-driven multi-card elaboration, and reverse cards are explicitly OUT OF SCOPE.

## Locked decisions (do not re-litigate)

1. Always OCR via the existing Hydra `ocr` group (default `ocr: mineru`, `conf/config.yaml`). The enumerator consumes per-page `md-singles/page-N.md` produced by `swanki/ocr/__init__.py:convert_to_markdown`. Do NOT add a pdftotext path.
2. Whole-document override only: new `elif mode == "glossary":` branch in `pipeline.py`, parallel to `solution_manual`. No classifier, no section routing.
3. Single-shape unit. `GlossaryUnit{term, definition, char_count}`. Part-of-speech and multiple senses stay as prose inside `definition` -- no per-sense fields (mirrors the problem_set "LLM renders content, schema stays single-shape" decision, swanki.models.problem_set 2026.05.04).
4. One card per term, `card_subtype="definition_main"`, stamped from the plan AFTER the LLM call (never trust the LLM to set it -- swanki.models.cards 2026.04.26).
5. Hard-fail coverage audit before any output: exactly one `definition_main` card per enumerated term, keyed via a strict-regex `GlossaryTag.parse`. Dump debug artifacts BEFORE the audit so a failure preserves evidence.
6. Response wrappers live in `models/glossary.py`, agents in `llm/agents.py`, pipeline imports the agents -- avoids the `pipeline -> agents -> models` import cycle (swanki.models.problem_set 2026.04.26).
7. Enumeration is LLM-assisted (mirrors `problem_enumeration_agent`) as the PRIMARY path, because MinerU's per-page markdown shape for a dense two-column wordlist is not regex-stable. No deterministic regex enumerator.
8. Card-gen batches terms (config `batch_size`) in one LLM call -- each word needs no surrounding context; the audit still guarantees 1 card/term.

## Enumeration and card shape

- Enumerate: concatenate all `md-singles/page-N.md`, send to `glossary_enumeration_agent` with the `definition_enumeration` system prompt. Returns `GlossaryEnumerationResponse{units: list[GlossaryUnit]}`. Prompt instructs: emit one unit per dictionary headword; `term` is the clean headword (single lexical item, fix obvious OCR drift); `definition` is the full sense text verbatim-ish (keep POS markers like "(verb)" inline). Do not invent or skip terms.
- Plan: `classify_definition_plan(unit, glossary_cfg)` -> `DefinitionCardPlan(n_cards=1, include_main=True)`. The `long_entry_chars` knob exists for future elaboration but for GRE every plan is 1 card.
- Generate: `generate_cards_for_terms` batches `batch_size` units, builds one user prompt listing `(term, definition)` pairs + the requested count, calls `definition_card_gen_agent` with the `definition_card_gen` system prompt -> `DefinitionCardBatchResponse{cards: list[PlainCard]}`. Front = `**term**`. Back = the definition as a complete sentence ending in a period, then (if `generate_example`) a new line `*e.g.* <one sentence that uses the word>`. Bold ONLY the headword. Keep back <= 500 chars (GRE defs are short; the example must fit). Stamp `card_subtype="definition_main"` and append tags `["vocabulary", "gre", GlossaryTag(...).render()]` after the call.
- Audit: `audit_coverage(units, cards, citation_key)` -- Part A: every enumerated term slug appears as exactly one `definition_main` card tag (Counter-checked: missing / duplicated / extra). Reuse `CoverageError` from `problem_set` (generic missing/extra/duplicated sets). Hard-fail.

## File specs

### NEW swanki/models/glossary.py (mirror swanki/models/problem_set.py)
- `slugify_term(term: str) -> str` -- lowercase, strip, non-alnum runs -> single hyphen, trim hyphens.
- `GlossaryUnit(BaseModel)`: `term: str`, `definition: str`, `char_count: int = 0`.
- `DefinitionCardPlan(BaseModel)`: `n_cards: int = Field(ge=1, le=5)`, `include_main: bool = True`; `@model_validator(mode="after")` enforcing `n_cards == int(include_main)` (extend when elaboration lands). Mirror `CardPlan` (models/problem_set.py:58).
- `GlossaryEnumerationResponse{units: list[GlossaryUnit]}`, `DefinitionCardBatchResponse{cards: list[PlainCard]}` (import PlainCard from .cards).
- `_GLOSSARY_TAG_RE = re.compile(r"^([^.]+)\.glossary\.([a-z0-9-]+)$")` and `GlossaryTag(BaseModel){citation_key, term_slug}` with `render()` -> `f"{citation_key}.glossary.{term_slug}"` and `classmethod parse(tag, citation_key) -> GlossaryTag | None` (mirror ProblemTag, models/problem_set.py:173). Build the regex against real slugs (hyphenated, digit-bearing) and round-trip test before relying on the audit (problem_set 2026.05.04 trap).

### NEW swanki/pipeline/glossary.py (mirror swanki/pipeline/problem_set.py)
- `from .problem_set import CoverageError`.
- `enumerate_glossary(clean_md_files, config) -> list[GlossaryUnit]`: join page texts, read prompt at `config["prompts"]["prompts"]["glossary"]["definition_enumeration"]`, `glossary_enumeration_agent.run_sync(..., model=get_model_string(models_llm))`, set `char_count`, return units.
- `classify_definition_plan(unit, glossary_cfg) -> DefinitionCardPlan` (heuristic, returns 1 card).
- `generate_cards_for_terms(units, plans, doc_summary, citation_key, config) -> list[PlainCard]`: batch, prompt via `_format_definition_prompt`, call `definition_card_gen_agent`, stamp subtype + tags. Trust the plan count; if the LLM returns the wrong number for a batch the audit fails loudly.
- `audit_coverage(units, cards, citation_key, *, strict=True) -> None`.
- `run_glossary_override(pipeline, cleaned_files, doc_summary, strict=True) -> list[PlainCard]`: enumerate -> (strict: raise if zero units) -> plan -> generate -> dump `glossary-units.yaml` + `cards-debug.yaml` (with `n_cards` and tag list) -> audit -> return cards. Mirror run_solution_manual_override (problem_set.py:936) but return only cards (no provenance).

### MODIFY swanki/models/cards.py
- Extend the `PlainCard.card_subtype` Literal (cards.py:707-718) with `"definition_main"`, `"definition_example"`, `"definition_elaboration"`. (Also extend the `CardSubtype` alias in models/problem_set.py:24 for typing parity.)

### MODIFY swanki/llm/agents.py
- After the solution-manual agents block (agents.py:43-58) add:
  `glossary_enumeration_agent: Agent[None, GlossaryEnumerationResponse] = Agent(output_type=GlossaryEnumerationResponse, retries=3)` and
  `definition_card_gen_agent: Agent[None, DefinitionCardBatchResponse] = Agent(output_type=DefinitionCardBatchResponse, retries=3)`.
  Import the two response types from `..models.glossary`.

### MODIFY swanki/pipeline/pipeline.py
- Add `elif mode == "glossary":` immediately after the `solution_manual` branch (pipeline.py:311-335), before the `else` (full). Mirror the solution_manual branch: `from .glossary import run_glossary_override`; set `self.citation_key = effective_key`; `self.state.current_stage = "glossary"`; `all_cards = run_glossary_override(self, cleaned_files, doc_summary)`; `self.state.cards_generated = len(all_cards)`; `self.state.current_stage = "output_generation"`; `outputs = self.generate_outputs(all_cards, doc_summary, self.output_base)`. No provenance. The downstream audio/apkg/zotero blocks are card-format-agnostic and need no change.

### NEW swanki/conf/pipeline/glossary.yaml
```
defaults: [default, _self_]
processing:
  segmentation: none
  image_cards:
    enabled: false
glossary:
  long_entry_chars: 600
  batch_size: 25
  generate_example: true
```

### NEW swanki/conf/prompts/glossary.yaml
`defaults: [default, _self_]`; under `prompts.glossary`: `definition_enumeration` and `definition_card_gen` system prompts encoding the rules above (front=`**term**`, back=definition sentence + `*e.g.*` line, bold only headword, <=500 chars, emit exactly the requested count).

### NEW swanki/conf/output/glossary.yaml (mirror output/problem_set.yaml)
```
defaults: [default, _self_]
output:
  apkg_filename_suffix: "-vocab"
```

### MODIFY swanki/conf/config.yaml + swanki/__main__.py
- config.yaml: extend the `mode` comment to list `glossary`.
- __main__.py help text: add `mode=glossary`, `pipeline=glossary`, `prompts=glossary`, `output=glossary`, and an example invocation (mirror the solution_manual example at __main__.py:147).

### NEW tests (mirror tests/test_problem_set*.py; offline, agents mocked)
- `tests/test_glossary_models.py`: `DefinitionCardPlan` validator (n_cards must equal include_main count); `GlossaryTag` render/parse round-trip incl. hyphenated/digit slugs and a non-matching tag returning None; `slugify_term` cases.
- `tests/test_glossary.py`: `enumerate_glossary` with `definition_card_gen_agent`/`glossary_enumeration_agent` patched to return a fixed `GlossaryEnumerationResponse` built from `tests/fixtures/glossary/gre_p1.md`; `classify_definition_plan` -> 1 card; `generate_cards_for_terms` patched agent -> asserts `card_subtype=="definition_main"`, canonical `GlossaryTag` tag present, one card per term; `audit_coverage` raises `CoverageError` on missing/duplicate/extra; a `mode=glossary` dispatch test mirroring `tests/test_pipeline_mode.py` (mock heavy methods, assert `generate_outputs` called and the glossary path taken). Use `--llm`/`--integration` markers for any agent-real test.
- `tests/fixtures/glossary/gre_p1.md`: real MinerU OCR of the first GRE word page, captured once (see Verification).

### NEW dendron notes
- `notes/swanki.pipeline.glossary.md`, `notes/swanki.models.glossary.md` (paired notes, dated section describing the design).
- Append dated sections to `notes/swanki.models.cards.md`, `notes/swanki.llm.agents.md`, `notes/swanki.pipeline.pipeline.md`, `notes/swanki.__main__.md` per the update-src-notes convention.

## Verification

- Offline gate (must pass in the worktree): `pytest tests/test_glossary.py tests/test_glossary_models.py -q`; `ruff check` + `mypy` on the new/modified files per project strategy (google docstrings, single-frontmatter-docstring header, no try/except / fail-fast).
- OCR fixture capture: run MinerU ONCE on a one-page slice to produce `tests/fixtures/glossary/gre_p1.md`. Slice: `qpdf /scratch/ManPrep1000GREwords/ManPrep1000GREwords.pdf --pages . <first-word-page>-<first-word-page> -- /scratch/ManPrep1000GREwords/ManPrep1000GREwords_p1.pdf` (pick the first page that actually contains the numbered word list; page 1 may be front matter). If GPU 3 is occupied (CH02 regen / Fish), copy the OCR output by hand instead -- do NOT contend for the GPU inside the autonomous worktree.
- Manual live run (flagged, NOT executed by the worktree agent to avoid GPU-3 contention with the running CH02 job): `swanki pdf_path=/scratch/ManPrep1000GREwords/ManPrep1000GREwords_p1.pdf citation_key=ManPrep1000GREwords +content_key=ManPrep1000GREwords_p1 mode=glossary pipeline=glossary prompts=glossary output=glossary ocr=mineru models=fish_speech anki=default audio=none pipeline.processing.confirm_before_generation=false`. Expect: one `definition_main` card per word on the page, each back = definition + `*e.g.*` example, and a `-vocab` apkg. Leave this as the remaining manual step in the PR description.

## Risks

- MinerU ligature/char drops on dense text corrupt headwords (becomes the card front and tag slug). Mitigation: enumeration prompt asks the LLM to emit clean headwords; add a light validity check (term is alphabetic-ish, non-empty); document `ocr=mathpix` as the fallback for wordlist PDFs.
- LLM batch returns the wrong card count. Mitigation: the coverage audit hard-fails with the missing/extra term slugs; artifacts dumped first.
- GPU-3 contention with the live CH02 pipeline + Fish. Mitigation: no live MinerU/pipeline run inside the worktree; fixture + offline tests are the gate.
- Tag-regex too strict for real slugs. Mitigation: build `_GLOSSARY_TAG_RE` against real enumerated slugs and round-trip test before the audit depends on it.

## Execution order

1. `models/glossary.py` 2. `llm/agents.py` 3. `pipeline/glossary.py` 4. `models/cards.py` (+ problem_set Literal) 5. conf `pipeline/prompts/output` glossary yamls 6. `pipeline.py` dispatch 7. `config.yaml` + `__main__.py` 8. tests + fixture 9. dendron notes. Run ruff+mypy+pytest after each logical unit.
