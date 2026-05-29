---
id: bcb6ddd00435f709ba5237
title: Solution-Manual Stage-3 LLM Pairing + Enumerator Dedup
desc: ''
updated: 1779233593004
created: 1779233593004
---

Plan: Solution-Manual Stage-3 LLM Pairing + Enumerator Dedup

## Context

Closes the Phase-1 gap in `mode=solution_manual` that blocks Bishop "Deep Learning: Foundations and Concepts" (citation key `bishopDeepLearningFoundations2024`) and any other textbook whose worked solutions live in a separate solution manual with no explicit `Solution N.M` markers. Parent design doc: [[plan.solution-manual-mode-for-problem-set-pdfs.2026.04.25]].

CH02 packed-PDF validation on 2026-05-19 ran end-to-end, exited with `swanki.pipeline.problem_set.CoverageError: Coverage audit failed: 13 problems with no solution: ['2.1','2.17','2.25','2.3','2.30','2.31','2.32','2.34','2.35','2.41','2.5','2.6','2.8']`. Artifacts persisted at `/scratch/bishop_ch02_solman_validation/bishopDeepLearningFoundations2024_CH02_probabilities/` (58 cleaned-md pages, `problem-pairings.yaml`, `cards-debug.yaml`) — reusable as fixtures, no re-OCR needed.

Two compounding root causes (`swanki/pipeline/problem_set.py`):

1. **Enumerator double-counts** (`:464` `enumerate_problems` + `:90-96` `_THEORY_PROBLEM`). The regex `^([0-9]+)\.([0-9]+)\b\s+(.+?)` has no notion of "we crossed into the solutions region". On Bishop, `2.1 (*) In the cancer screening...` (chapter Exercises, page 36) and `2.1 We first compute $p(T=1)$...` (solutions, page 37) both match — yielding two `ProblemUnit`s with `problem_id='2.1'`. The validation YAML shows `dup ids: ['2.1', '2.3']` and `n_cards: 44` vs the real 31 problems.
2. **Stage 3 unimplemented** (`:511-683` `pair_problems_across_pages`, no-op at `:676` `method = "regex" if used_regex else "regex"`). Docstring `:516-521` explicitly says: *"Stage 3 (LLM fallback) is wired but disabled... reserved for future iteration once we have real Bishop fixtures with no explicit `Solution N.M` markers."* All scaffolding (`problem_pairing_agent`, `ProblemPairingResponse`, `problem_pairing` prompt, `PairingResult.method: Literal["regex","llm","mixed"]`) already exists — only the call site is missing.

CLAUDE.md governs: no `try/except`, fail fast, minimize conditionals, Pydantic-first. The implementation hews to the existing call-site pattern in `generate_cards_for_problem` (`:833-849`) and `section_classifier` (`section_classifier.py:271-283`).

## Approach

Two surgical changes to `swanki/pipeline/problem_set.py`, one prompt sharpening, one optional config knob, three tests + one fixture, three note updates.

**Enumerator fix — region-aware partition (recommended over post-hoc dedup).** Add `_partition_statement_solution_regions(full_text) -> tuple[str, str | None]` that locates the boundary between problem statements and worked solutions, and run `_THEORY_PROBLEM.finditer` only on the statements span. Boundary detector fires on the FIRST `^##\s+Chapter\s+\d+\b` heading that appears AFTER an `^##\s+Exercises\b` heading earlier in the text (the canonical Bishop shape: chapter body → `## Exercises` → packed-on solution manual that opens with `## Chapter N <Title>`). When no boundary is found (Schaum's: inline statement+solution blocks, no separate solution region), return `(full_text, None)` — preserves current behavior, zero regression. Stage-3 reuses the right-hand-side span as the candidate-solutions pool. Rejected alternatives: (b) post-hoc dedup by problem_id with statement-side priority (brittle heuristics on prose shape); (c) reactivate `section_classifier` inside `mode=solution_manual` (explicitly out of scope per request).

**Stage-3 implementation — single batched LLM call per chapter.** Slot a new block at `:674-676` between Stage-2e and the `method` literal: filter `unpaired = [p for p in pairings if not p.solutions]`, gate on `sm_config.get("stage3_enabled", True)` and non-empty `unpaired`, build a user prompt that lists `(problem_id, statement_first_chars)` pairs + the entire solution-region text, call `problem_pairing_agent.run_sync(user_prompt, instructions=stage3_system_prompt, model=get_model_string(models_config))`, merge each returned `ProblemLocation` into `pairings_by_id`, set `used_llm = True`. Solution-region text is bounded by the chapter slice (Bishop CH02 = 22 pp; well under gpt-5.5 context). The `solution_manual.batch_size: 5` knob stays "reserved" — one call per chapter, not per problem.

**Method literal fix.** Replace `:676` no-op with the canonical tri-state `method = "mixed" if used_llm and used_regex else "llm" if used_llm else "regex"`.

**Prompt sharpening.** The existing `prompts.solution_manual.problem_pairing` in `swanki/conf/prompts/solution_manual.yaml:38-45` is too thin for Bishop. Extend it with three additions: (i) name the bare `N.M` solution-numbering pattern, (ii) instruct the agent to ignore page running-headers like `Solutions 2.1–2.2` and chapter-title headers like `## Chapter 2 Probabilities`, (iii) require each returned `ProblemLocation` to set `problem_id` from the supplied list (not invent), `role="solution"`, and `text` to the verbatim solution body (statement+derivation through the next bare `N.M` or end-of-region). Keep the "omit if no match; do NOT fabricate" guarantee.

**Config knob.** Add `solution_manual.stage3_enabled: true` to `swanki/conf/pipeline/solution_manual.yaml`. Default true so Bishop "just works"; flip false to preserve regex-only Schaum's runs.

**Test strategy.** One real-data fixture snapshotted from the CH02 validation artifacts (no re-OCR), plus three tests in `tests/test_problem_set.py`: enumerator-dedup, Stage-3-mocked-agent-invoked, Stage-3-omits-unmatchable.

**Provenance.** Stage-3 solutions get `page_idx=0` (same as Stage-2's full-text-scan loss, `:578`); the YAML artifact carries the full solution text. The `PairingResult.method` field already records `"llm"` / `"mixed"` for downstream introspection.

**Failure behavior.** When LLM omits a problem, it stays unpaired. `audit_coverage` Part 2 raises `CoverageError` unless `allow_unsolved=true` (`solution_manual.yaml:25`, default false). This preserves the contract — no silent gaps. CH02's hand-picked solution slice (pages 4-25 of `Bishop-Solutions-2024.pdf`) covers all 31 worked solutions; Stage-3 should pair them all.

## File Specifications

### `swanki/pipeline/problem_set.py` (MODIFY)

**Current state:** 1050 lines. `enumerate_problems(:464)` runs `_THEORY_PROBLEM.finditer` on the full concatenated text. `pair_problems_across_pages(:511)` runs Stages 0-2e then returns with a no-op `method` literal. Imports at `:21-25` include `problem_card_gen_agent`, `problem_enumeration_agent` but NOT `problem_pairing_agent`.

**Changes:**

1. **Imports (`:21-25`)** — add `problem_pairing_agent` to the import list:

   ```python
   from ..llm.agents import (
       get_model_string,
       problem_card_gen_agent,
       problem_enumeration_agent,
       problem_pairing_agent,
   )
   ```

2. **New helper `_partition_statement_solution_regions`** — place immediately above `enumerate_problems` (after `_try_pair_or_unpaired` at `:461`):

   ```python
   _EXERCISES_HEADING = re.compile(r"^##\s+Exercises\b", re.MULTILINE | re.IGNORECASE)
   _SOLUTION_REGION_HEADING = re.compile(r"^##\s+Chapter\s+\d+\b", re.MULTILINE)


   def _partition_statement_solution_regions(
       full_text: str,
   ) -> tuple[str, str | None]:
       """Split a packed-document into (statements_region, solutions_region).

       Bishop-style packed PDFs concatenate the book chapter (ending with a
       ``## Exercises`` section) and a slice of the separate solution manual
       (opening with ``## Chapter N <Title>``). When that shape is present,
       return both regions. When absent (Schaum's: inline Q&A, no separate
       solution span), return ``(full_text, None)`` so callers fall back to
       the legacy single-region path.
       """
       ex = _EXERCISES_HEADING.search(full_text)
       if ex is None:
           return full_text, None
       sol = _SOLUTION_REGION_HEADING.search(full_text, ex.end())
       if sol is None:
           return full_text, None
       return full_text[: sol.start()], full_text[sol.start():]
   ```

3. **Refactor `enumerate_problems` (`:464-508`)** — partition before the theory-problem pass; pass the statements-region span (not `full_text`) to `_THEORY_PROBLEM.finditer`; keep all four review-subtype enumerators untouched (they already use `_section_span` for in-chapter scoping). New body:

   ```python
   def enumerate_problems(
       clean_md_files: list[Path], chapter_id: str | None = None
   ) -> list[ProblemUnit]:
       problems: list[ProblemUnit] = []
       full_text = "\n\n".join(f.read_text() for f in clean_md_files)
       statements_text, _solutions_region = _partition_statement_solution_regions(
           full_text
       )

       for m in _THEORY_PROBLEM.finditer(statements_text):
           chap, num, body = m.group(1), m.group(2), m.group(3).strip()
           parts = body.split("\n\n", 1)
           statement = parts[0].strip()
           solution = parts[1].strip() if len(parts) > 1 else None
           problems.append(
               ProblemUnit(
                   problem_id=f"{chap}.{num}",
                   subtype="theory_problem",
                   chapter=chap,
                   statement=statement,
                   solution=solution,
                   char_count=len(statement) + len(solution or ""),
               )
           )

       chapter_num = _detect_chapter(full_text, chapter_id)
       problems.extend(_enumerate_multiple_choice(full_text, chapter_num))
       problems.extend(_enumerate_matching(full_text, chapter_num))
       problems.extend(_enumerate_true_false(full_text, chapter_num))
       problems.extend(_enumerate_completion(full_text, chapter_num))

       return problems
   ```

   Note: `_detect_chapter` and the four review-subtype enumerators still see `full_text` (their existing back-of-book partition logic depends on `## Chapter N` headers that live in the solutions region for Schaum's; do not break that).

4. **Stage-3 block in `pair_problems_across_pages` (insert at `:674` — between Stage-2e's final `used_regex = True` and the method literal at `:676`):**

   ```python
       # Stage 3: LLM content-pairing for problems still without a solution.
       # Bishop-style separate solution manuals carry no `Solution N.M` markers,
       # so Stages 1-2 never bridge the statement → solution gap; the agent
       # matches by content. Omits unmatchable problems (per prompt contract);
       # `audit_coverage` + `allow_unsolved` enforce the gap.
       used_llm = False
       sm_config = config.get("pipeline", {}).get("solution_manual", {})
       if sm_config.get("stage3_enabled", True):
           unpaired = [p for p in pairings if not p.solutions]
           _, solutions_region = _partition_statement_solution_regions(full_text)
           if unpaired and solutions_region:
               prompts_root = config.get("prompts", {}).get("prompts", {})
               sm_prompts = prompts_root.get("solution_manual", {})
               system_prompt = sm_prompts.get("problem_pairing", "")
               problems_block = "\n".join(
                   f"- {p.problem_id}: {p.statement.text[:300]}"
                   for p in unpaired
               )
               user_prompt = (
                   "Unpaired problems (id: statement excerpt):\n"
                   f"{problems_block}\n\n"
                   "Solutions region (worked solutions, numbered as bare `N.M`):\n"
                   f"{solutions_region}"
               )
               models_config = config.get("models", {}).get("models", {}).get("llm", {})
               result = problem_pairing_agent.run_sync(
                   user_prompt,
                   instructions=system_prompt,
                   model=get_model_string(models_config),
               )
               response: ProblemPairingResponse = result.output
               for loc in response.solutions:
                   pair = pairings_by_id.get(loc.problem_id)
                   if pair is not None:
                       pair.solutions.append(loc)
                       used_llm = True
   ```

5. **Method-literal fix (`:676` — replace the tautological line):**

   ```python
       method: Literal["regex", "llm", "mixed"] = (
           "mixed" if used_llm and used_regex
           else "llm" if used_llm
           else "regex"
       )
   ```

6. **Add `ProblemPairingResponse` to the model imports** (`:28-39`) — it isn't currently imported into this file. Add `ProblemPairingResponse,` to the import block.

**Imports affected:** `..llm.agents.problem_pairing_agent`, `..models.problem_set.ProblemPairingResponse`. Both already exist; no model-layer changes.

**Edge cases:**
- Bishop chapter that has no `## Exercises` heading (e.g. a chapter cut without exercises): partition returns `(full_text, None)`, Stage-3 short-circuits on `solutions_region is None`, `audit_coverage` correctly raises if the chapter genuinely has unsolved problems.
- LLM returns a `problem_id` that isn't in `unpaired` (hallucination): `pairings_by_id.get(loc.problem_id)` returns None, the entry is dropped silently. Don't add a warning — keep the code dense; the audit surfaces gaps.
- LLM returns a solution for a problem that's already paired (rare; agent ignored "unpaired" framing): append anyway, audit doesn't care about multiple solutions per problem.
- `stage3_enabled: false` AND Bishop has unpaired problems: `audit_coverage` raises as before — the knob is an opt-out, not a coverage suppressor.

### `swanki/conf/prompts/solution_manual.yaml` (MODIFY)

**Current state:** 5-sentence `problem_pairing` prompt at `:38-45`. Generic; doesn't mention bare `N.M` numbering or page running-headers.

**Change:** Replace the `problem_pairing:` block with:

```yaml
    problem_pairing: |-
      You receive a list of unpaired problems (each with id and a short statement excerpt)
      and the verbatim text of the document's solutions region. Some solution manuals (e.g.
      Bishop's "Deep Learning: Foundations and Concepts" worked-solutions PDF) number their
      worked solutions as bare `N.M` (e.g. `2.1 We first compute ...`) — NOT under an
      explicit `Solution N.M` heading. Your job is to match each unpaired problem to its
      worked solution in this region.

      For each match, emit ONE ProblemLocation with:
      - problem_id: the exact id from the supplied unpaired list (do NOT invent ids).
      - role: "solution".
      - text: the verbatim solution body — from the bare `N.M` label through (but not
        including) the next bare `N.M` label or end-of-region. Include sub-parts (a),
        (b), (c) when present.

      Match by CONTENT, not by position: the solution should derive or compute what the
      problem statement asks for. Ignore page running-headers like `Solutions 2.1–2.2`
      and chapter-title headers like `## Chapter 2 Probabilities` — they are not solutions.

      If you cannot find a solution for a problem in the supplied region, OMIT that
      problem from your output. Do NOT fabricate. The pipeline's coverage audit will
      surface the gap.
```

Keep the surrounding YAML structure (`prompts: solution_manual:` parent keys) untouched.

### `swanki/conf/pipeline/solution_manual.yaml` (MODIFY)

**Current state (25 lines):** has `chapter_indexes`, `long_problem_chars`, `batch_size`, `enable_full_solution_cards`, `enable_llm_classifier`, `allow_unsolved`. No Stage-3 knob.

**Change:** add one line under `solution_manual:`, after `enable_llm_classifier`:

```yaml
  # Stage-3 LLM content-pairing fallback (Bishop-style manuals with no
  # explicit `Solution N.M` markers). Set false to preserve regex-only
  # Schaum's runs.
  stage3_enabled: true
```

### `tests/fixtures/problem_set/bishop_ch02_statement_solution_separated.md` (NEW)

**Purpose:** real-data fixture for enumerator-dedup + Stage-3 tests, snapshotted from the CH02 validation artifacts (no re-OCR cost).

**Source:** trim `/scratch/bishop_ch02_solman_validation/bishopDeepLearningFoundations2024_CH02_probabilities/clean-md-singles/page-{36,37,38}.md` into ~80-120 lines covering:
- Page 36 (chapter Exercises): `## Exercises` heading + statements `2.1 (*) ...`, `$2.2(\star \star)$ ...`, `2.3 (*) ...` (three statements is enough).
- Page 37 (solution manual): `## Chapter 2 Probabilities` heading + bare `2.1 We first compute $p(T=1)$ ...` (full solution for 2.1) + bare `2.3 The change-of-variables formula ...` (full solution for 2.3 — note: NO `2.2` solution to exercise the "omit if no match" contract).

Keep math notation verbatim (Mathpix output); the fixture mirrors what `_partition_statement_solution_regions` will see.

### `tests/test_problem_set.py` (MODIFY)

**Current state:** 402 LOC; covers Schaum's enumerators (MC/Matching/T-F/Completion), back-of-book pairing, `audit_coverage`, prompt dispatch. No Bishop-style fixture; no Stage-3 test.

**Changes:** Add three new tests in a new `class TestStage3LLMPairing:` block (or top-level functions; match the file's existing style).

**Test 1 — `test_enumerate_problems_dedups_solution_region`:**

- Load the new Bishop fixture as a single-element `clean_md_files` list.
- Call `enumerate_problems(clean_md_files, chapter_id="bishopDeepLearningFoundations2024_CH02")`.
- Assert `len(problems) == 3` (NOT 5+; no duplicates).
- Assert `{p.problem_id for p in problems} == {"2.1", "2.2", "2.3"}`.
- Assert every problem has `subtype == "theory_problem"`.
- Assert every problem's `solution is None` (the partition pushed the solutions region out of `_THEORY_PROBLEM`'s scope, so no false inline solution is lifted).

**Test 2 — `test_pair_llm_fallback_invoked_for_unmatched`:**

Uses `unittest.mock.patch` on `swanki.pipeline.problem_set.problem_pairing_agent.run_sync`.

```python
from unittest.mock import patch, MagicMock
from swanki.models.problem_set import (
    ProblemLocation,
    ProblemPairingResponse,
)


def test_pair_llm_fallback_invoked_for_unmatched(tmp_path: Path) -> None:
    fixture = Path(__file__).parent / "fixtures" / "problem_set" / "bishop_ch02_statement_solution_separated.md"
    problems = enumerate_problems([fixture])
    config = {
        "pipeline": {"solution_manual": {"stage3_enabled": True}},
        "prompts": {"prompts": {"solution_manual": {"problem_pairing": "test"}}},
        "models": {"models": {"llm": {"provider": "openai", "model": "gpt-5.5"}}},
    }
    fake_locs = [
        ProblemLocation(
            problem_id="2.1", role="solution",
            page_idx=0, start_char=0, end_char=10, text="We first compute ...",
        ),
        ProblemLocation(
            problem_id="2.3", role="solution",
            page_idx=0, start_char=0, end_char=10, text="The change-of-variables ...",
        ),
    ]
    fake_result = MagicMock()
    fake_result.output = ProblemPairingResponse(solutions=fake_locs)
    with patch(
        "swanki.pipeline.problem_set.problem_pairing_agent.run_sync",
        return_value=fake_result,
    ) as m:
        result = pair_problems_across_pages(problems, [fixture], config)
    assert m.called, "Stage-3 LLM pairer was not invoked"
    assert result.method in {"llm", "mixed"}
    paired_ids = {p.problem_id for p in result.pairings if p.solutions}
    assert {"2.1", "2.3"} <= paired_ids
    # 2.2 should remain unpaired (mock didn't return it)
    assert "2.2" not in paired_ids
```

**Test 3 — `test_stage3_disabled_preserves_regex_only`:**

Same fixture, but `config["pipeline"]["solution_manual"]["stage3_enabled"] = False`. Assert `problem_pairing_agent.run_sync` is NOT called, `result.method == "regex"`, all three problems have `solutions == []`.

### `notes/swanki.pipeline.problem_set.md` (MODIFY)

**Current state:** module note with dated sections (line 18 documents Stage-3 as "wired but not yet exercised"; line 30 lists it as "deferred to follow-up").

**Change:** Append a dated section `## 2026.05.19 — Stage-3 LLM pairing + enumerator region partition`. Body covers:
- The Bishop CH02 motivating case (cite the validation log `/scratch/bishop_ch02_solman_validation/...` and the 13-IDs CoverageError).
- The two-part fix: `_partition_statement_solution_regions` for enumerator dedup; activate `problem_pairing_agent` in Stage 3.
- Why region-aware partition over post-hoc dedup (deterministic, no extra LLM cost, Schaum's regression-free).
- The new `solution_manual.stage3_enabled` knob (default true).
- Link: [[plan.solution-manual-stage-3-llm-pairing.2026.05.19]].

Flip the "Stage 3: wired but not yet exercised" line and the "Deferred to follow-up" entry to past tense / SHIPPED.

### `notes/swanki.llm.agents.md` (MODIFY if it exists; CREATE if not)

**Current state:** check existence with `ls notes/swanki.llm.agents.md`. If present, the `problem_pairing_agent` entry will note "wired but not yet exercised".

**Change:** If the note exists, append a dated section flipping `problem_pairing_agent` to active and linking to this plan. If absent, do NOT create it — the plan stays minimal; module notes are added on demand per CLAUDE.md.

### `notes/user.mjvolk3.swanki.tasks.weekly.2026.17.md` (MODIFY)

**Change:** add ONE pending bullet near other 2026-05-19 entries:

```markdown
- [ ] Plan Stage-3 LLM pairing + enumerator dedup for solution_manual mode (Bishop unblock) [[plan.solution-manual-stage-3-llm-pairing.2026.05.19]]
```

After implementation lands, flip to `- [x]` with a one-sentence summary per the "When checking off a task ... always add a one-sentence summary" CLAUDE.md rule.

## Edge Cases

1. **No `## Exercises` heading in the chapter PDF.** Partition returns `(full_text, None)` → Stage-3 short-circuits → `audit_coverage` raises if there are genuinely unpaired problems. Acceptable; Bishop chapters all have `## Exercises`.
2. **Chapter PDF where the boundary `## Chapter N` happens to appear BEFORE `## Exercises`** (e.g. an in-chapter back-reference). The detector searches for `## Chapter N` AFTER `_EXERCISES_HEADING.end()`, so prior occurrences are ignored.
3. **LLM hallucinates a `problem_id` not in `unpaired`.** `pairings_by_id.get(...)` returns None → silently dropped. The audit will surface any actual gap; this is the fail-fast contract.
4. **Solutions region exceeds the model's context window.** Bishop's largest chapter slice is CH03 (18 pp) — well under gpt-5.5's window. If a future book exceeds this, chunk on bare `^\d+\.\d+\b` boundaries and call the agent per chunk; defer until needed.
5. **Schaum's regression.** Schaum's fixtures have no `## Exercises` heading and no separate `## Chapter N` solutions region → partition returns `(full_text, None)` → enumerator runs on full text exactly as before → all four review-subtype enumerators still see `full_text` for back-of-book → no behavioral change.
6. **`stage3_enabled: false` on Bishop.** Documented behavior: regex-only path; coverage audit fails the same way it does today. The knob is for power users with custom workflows; not a default escape hatch.
7. **`allow_unsolved: true` combined with Stage 3.** Stage 3 runs first; remaining unpaired logged as warnings; audit accepts. Acceptable.
8. **Method literal in serialized YAML.** `PairingResult.method: Literal["regex","llm","mixed"]` already accepts all three; existing tests use `method="regex"` and continue to pass.

## Verification

**Implementation order:** fixture → enumerator partition + Test 1 → Stage-3 + method-fix + Test 2-3 → prompt + config knob → dendron notes → CH02 re-validation → commit trio.

1. Unit tests:

   ```bash
   conda activate swanki
   pytest tests/test_problem_set.py -xvs -k "stage3 or dedup"
   pytest tests/test_problem_set.py tests/test_problem_set_models.py -x  # full suite, no regression
   ```

2. Type check + lint:

   ```bash
   mypy swanki/pipeline/problem_set.py
   ruff check swanki/pipeline/problem_set.py swanki/conf/prompts/solution_manual.yaml
   ```

3. CH02 end-to-end re-validation (uses the already-packed PDF; OCR + summary cached if the run dir is reused):

   ```bash
   cd /home/michaelvolk/Documents/projects/Swanki
   export PATH="$HOME/miniconda3/envs/swanki/bin:$HOME/.nvm/versions/node/v18.20.8/bin:$PATH"
   rm -rf /scratch/bishop_ch02_solman_validation_v2
   script -qc "swanki \
     pdf_path=/home/michaelvolk/Documents/projects/Deep-Learning-Foundations-and-Concepts/notes/assets/book/chapters/bishopDeepLearningFoundations2024_CH02_probabilities_packed.pdf \
     citation_key=bishopDeepLearningFoundations2024 \
     content_key=bishopDeepLearningFoundations2024_CH02_probabilities \
     +output_dir=/scratch/bishop_ch02_solman_validation_v2/bishopDeepLearningFoundations2024_CH02_probabilities \
     mode=solution_manual pipeline=solution_manual prompts=solution_manual \
     models=fish_speech audio=none anki=default zotero=default \
     pipeline.processing.confirm_before_generation=false" \
     /scratch/bishop_ch02_solman_validation_v2/run.log
   ```

4. Inspect the new pairing artifact:

   ```bash
   ~/miniconda3/envs/swanki/bin/python -c "
   import yaml, collections
   d = yaml.safe_load(open('/scratch/bishop_ch02_solman_validation_v2/bishopDeepLearningFoundations2024_CH02_probabilities/problem-pairings.yaml'))
   ids = [p['problem_id'] for p in d['pairings']]
   print('method:', d['method'], 'pairings:', len(ids))
   print('dup ids:', [k for k,v in collections.Counter(ids).items() if v>1])
   print('unsolved:', sorted(p['problem_id'] for p in d['pairings'] if not p['solutions']))
   "
   ```

   Pass criteria: `method` in `{"llm","mixed"}`; `pairings` length == 31 (Bishop CH02's exercise count); `dup ids: []`; `unsolved: []`; exit 0 on the swanki run (no `CoverageError`).

5. CH03-10 batch (unblocks task `#6`): edit `bishop-solutions-fish.sh` to uncomment Batch 2, run in background:

   ```bash
   bash /home/michaelvolk/Documents/projects/Deep-Learning-Foundations-and-Concepts/notes/assets/swanki/bishop-solutions-fish.sh
   ```

## Acceptance Criteria

- `pytest tests/test_problem_set.py` passes with the three new tests + all existing tests.
- CH02 packed-PDF run completes with exit 0; the new `problem-pairings.yaml` has `method` in `{"llm","mixed"}`, **zero duplicate problem_ids**, and **zero unsolved** entries.
- The 13 previously-unsolved IDs (`2.1, 2.3, 2.5, 2.6, 2.8, 2.17, 2.25, 2.30, 2.31, 2.32, 2.34, 2.35, 2.41`) each have at least one `solutions: [...]` entry whose text is the corresponding worked solution.
- Schaum's CH01 still produces `method="regex"` (no regression). The existing `test_problem_set.py` Schaum's tests pass.
- CH03-CH10 run successfully under the same invocation (uncomment Batch 2 in `bishop-solutions-fish.sh`); any per-chapter gaps surface as `CoverageError` with specific problem IDs.

## Execution

To implement, start a new Claude Code session and run:

```
/read-codebase pipeline llm models conf
```

Then:

```
Implement the plan at notes/plan.solution-manual-stage-3-llm-pairing.2026.05.19.md.
Read the plan first, then implement each file specification in order:
  1. tests/fixtures/problem_set/bishop_ch02_statement_solution_separated.md (NEW)
  2. swanki/pipeline/problem_set.py (MODIFY: imports, _partition helper, enumerate_problems, Stage-3 block, method literal)
  3. swanki/conf/prompts/solution_manual.yaml (MODIFY: problem_pairing)
  4. swanki/conf/pipeline/solution_manual.yaml (MODIFY: add stage3_enabled)
  5. tests/test_problem_set.py (MODIFY: three new tests)
Run pytest after step 2, again after step 5. Then run the CH02 re-validation
command from the Verification section. After it exits 0 with method in
{"llm","mixed"} and zero unsolved, update notes/swanki.pipeline.problem_set.md
and notes/user.mjvolk3.swanki.tasks.weekly.2026.17.md, then /update-notes ->
/stage -> /commit. Open a PR via the worktree-merge workflow.
```

Worktree name: `solman-stage3-pairing-dedup` under `~/projects/Swanki.worktrees/`.

## Critic Review

(populated after Phase 4)
