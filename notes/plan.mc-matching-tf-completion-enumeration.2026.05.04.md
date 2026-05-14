---
id: k3awssmxviv3t0ardcdq4n7
title: MC Matching TF Completion Enumeration
desc: Extend solution-manual problem enumeration + pairing beyond N.M theory-problems to cover Schaum's-style Multiple Choice, Matching, True/False, and Completion review subtypes
updated: 1777937930887
created: 1777937930887
---

Plan: MC / Matching / True-False / Completion Enumeration

## Context

The solution-manual pipeline shipped with `enumerate_problems` recognising only the `N.M` theory-problem form (see [[swanki.pipeline.problem_set]]). Schaum's-style chapters carry four additional review subtypes — Multiple Choice, Matching, True/False, Completion — that use single-digit `1.`/`2.`/... numbering and so are silently skipped today.

Empirical anchor: `alcamoSchaumsOutlineMicrobiology2010` Ch1 packed PDF runs end-to-end in `mode=full` and produces 25 cards (16 concept + 7 problem-set: `1.25`–`1.30` + 1 overview). It SHOULD produce ~70 cards: 30 theory-problems (already covered when chapter scope is right) + 15 MC + 10 Matching + 15 T/F. The missing ~40 cards are the gap this plan closes.

The classifier already routes the Schaum's chapter-end review pages to `review_exercises`. The schema already declares all five subtypes (`ProblemSubtype = Literal["theory_problem", "multiple_choice", "matching", "true_false", "completion"]` in `swanki/models/problem_set.py:21-23`). The `ProblemTag` regex (`_PROBLEM_TAG_RE` in `swanki/models/problem_set.py:168`) already accepts `MC-\d+|[A-Z]+-\d+` so `MAT-3`, `TF-7`, `CMP-1` round-trip without change. Stage-2b pairing has `_MC_ANSWER_BLOCK` already wired but it never matched anything (a) because no MC items were ever enumerated, and (b) because the regex anchor `^Chapter\s+\d+` doesn't match the actual back-of-book OCR which is `## Chapter 1\n## Multiple Choice` (markdown-promoted headers, not bare text).

The work is concentrated in `swanki/pipeline/problem_set.py` and `swanki/conf/prompts/solution_manual.yaml`. No changes needed in the classifier, agents, or pipeline orchestrator.

## Kanban Issues

No directly related issues found. The repo has zero open GitHub issues; tracking is via the weekly note. The pending plan bullet at line 22 of `notes/user.mjvolk3.swanki.tasks.weekly.2026.17.md` is the parent solution-manual plan; this work is the natural next bullet on the same branch.

## Approach

Five locked design decisions:

1. **Subtype-prefixed problem IDs** to avoid collision across subtypes and chapters: `MC-CH{n}-{m}`, `MAT-CH{n}-{m}`, `TF-CH{n}-{m}`, `CMP-CH{n}-{m}`. Bare forms (`MC-{m}`, `MAT-{m}`, `TF-{m}`, `CMP-{m}`) are accepted as a fallback when chapter context is unknown. The audit's `ProblemTag.parse` already handles all of these (regex `[A-Z]+-\d+` matches `MC-1`, `MAT-3`, etc.) — verified.
2. **Per-subtype enumerator helpers**, one function each (`_enumerate_multiple_choice`, `_enumerate_matching`, `_enumerate_true_false`, `_enumerate_completion`), called from `enumerate_problems` after the existing theory-problem loop. Each helper is anchored on the section divider (Schaum's inline form `Multiple Choice. ...`, `Matching. ...`, etc.) so it only enumerates within that section's text span.
3. **Per-subtype Stage-2 pairing**, one regex pass each, all anchored on the back-of-book block `^##\s*Chapter\s+(\d+)\s*\n+##\s*<Subtype>\s*\n+(.+)`. Subtype-specific pair regex extracts `(item_number, answer)` pairs from the answer row. T/F is the only one with mixed answers (single letter `T` OR multi-word replacement) — it gets a custom pair-splitter that handles both. The existing `_MC_ANSWER_BLOCK` regex is **fixed** as part of this work to handle the markdown-promoted header form (it currently never matches).
4. **Per-subtype card prompt** chosen by `problem.subtype` in `_format_problem_card_prompt`. Each prompt explains the question shape (MC = stem + four choices → back is full chosen choice; Matching = column-A statement + column-B options → back is full matched option text; True/False = statement → back is `T` or "false; replace X with Y"; Completion = sentence with blank → back is fill-in word). The system prompt (`prompts.solution_manual.problem_card_gen_<subtype>`) carries the format guidance; `problem_card_gen_agent` and `ProblemCardBatchResponse` are unchanged.
5. **No model-shape changes** to `ProblemUnit`. New per-subtype data (MC choices, Matching column B options, T/F underlined-word inference, Completion blank position) is encoded as **prose inside `problem.statement` and `problem.solution`**. This keeps the schema single-shape and makes the LLM the single source of card-content rendering. Adding optional fields like `choices: list[str] | None` was considered and rejected for v1 — they'd duplicate state the prompt already needs, and we'd then have to keep them in sync. The statement field for an MC item is e.g. `"1. The first scientist to observe microorganisms was\n(a) Pasteur\n(b) Koch\n(c) van Leeuwenhoek\n(d) Watson"` — that's everything the LLM needs to generate one card.

**Important non-goals:**

- True/False underlined-word recovery from OCR. The Schaum's CH01 OCR drops the `\underline{}` markup entirely (verified — page-11 line 5 has plain text "viruses and dinoflagellates" with no markup). The card design accepts this: front shows the statement; back shows `T` (true) OR `replacement` (the back-of-book word that replaces the originally-underlined one). Learners infer the underlined word by comparing the statement to the correction.
- LLM-driven enumeration fallback (`problem_enumeration_agent`). Already declared but never wired; staying dormant.
- Card-plan customization per subtype. MC/Matching/T-F/Completion all hit the simplest path of `classify_card_plan` (`n_cards=1, include_main=True`) — no subparts, no overview, no full solution. The existing heuristic produces correct plans without modification.

**End-state contract:** running `mode=full` on Schaum's CH01 packed PDF produces (depending on classifier page split) approximately 70 review-section cards distinguished by tag (`<key>.problem.MC-CH1-1`, `.MAT-CH1-3`, `.TF-CH1-7`, etc.) plus the existing 6 theory-problem cards (`1.25`–`1.30`) plus the ~16 concept cards from the main_content pipeline. All in one integrated `.apkg`. Audit hard-fails if any enumerated subtype problem is missing a `problem_main` card or its back-of-book solution.

## File Specifications

### `swanki/pipeline/problem_set.py` (MODIFY)

**Current state:** 618 lines. Single-subtype enumerator at lines 110-146 (`enumerate_problems`); Stage-0/1/2/2b pairing at lines 149-260 (`pair_problems_across_pages`); subtype-blind prompt formatter at lines 342-378 (`_format_problem_card_prompt`); card stamping at lines 423-445.

**Changes:**

1. **Fix `_MC_ANSWER_BLOCK` regex** (lines 98-101). The current pattern `^Chapter\s+([0-9]+)\s*\n+\s*Multiple Choice\s*\n+\s*((?:[0-9]+\.\s*[a-z]\s*)+)` does not match the actual OCR output `## Chapter 1\n\n## Multiple Choice\n\n1. c 2. c ...`. Replace with a permissive pattern accepting both `## ` prefixes and bare forms. Same fix applies to all four new subtype back-of-book regexes.

   ```python
   # Optional `## ` prefix on the chapter and section headers (Mathpix promotes
   # them to H2 in the back-of-book region, leaves them bare in mid-chapter).
   _BACK_CHAPTER = r"^(?:##\s+)?Chapter\s+(\d+)\s*$"
   _BACK_SECTION_MC = r"(?:##\s+)?Multiple Choice\s*$"
   _BACK_SECTION_MAT = r"(?:##\s+)?Matching\s*$"
   _BACK_SECTION_TF = r"(?:##\s+)?True/False\s*$"
   _BACK_SECTION_CMP = r"(?:##\s+)?Completion\s*$"
   ```

2. **Add new section-header regexes** for in-chapter MC/Matching/T-F/Completion section dividers. Schaum's writes them inline: `Multiple Choice. Select the letter ...`, `Matching. Match the choices ...`, `True/False. For each of the following ...`, `Completion. Fill in the blanks ...`. Anchors are at lines 7-19 of pages 8 / 10 / 11 of the Ch1 OCR.

   ```python
   # Drop the verb requirement — "<Subtype>." is canonical, descriptive prose
   # after it varies (Bishop uses "Pick"/"Mark"/"Identify", Schaum's uses
   # "Select"/"For each"/"Match"/"Fill"). Match the bare period instead.
   _MC_SECTION = re.compile(r"^Multiple Choice\.\s+\S", re.MULTILINE)
   _MATCHING_SECTION = re.compile(r"^Matching\.\s+\S", re.MULTILINE)
   _TF_SECTION = re.compile(r"^True/False\.\s+\S", re.MULTILINE)
   _COMPLETION_SECTION = re.compile(r"^Completion\.\s+\S", re.MULTILINE)
   ```

   These regexes locate the section's *start*; the section's *end* is the start of the next section regex match or end-of-text. Use a small helper `_section_span(full_text, start_re) -> (start, end)` to avoid duplicating the lookahead in each enumerator.

3a. **Fix `_THEORY_PROBLEM` greedy tail** (lines 89-92). The existing regex `^([0-9]+)\.([0-9]+)\b\s+(.+?)(?=^[0-9]+\.[0-9]+\b|\Z)` only terminates on the next `N.M` or end-of-text. **Verified:** when the last theory-problem (e.g. `1.30`) precedes the review section, its captured solution body runs ~6900 chars and includes the entire MC + Matching + T/F + back-of-book content. Add the review-section dividers AND the chapter-end markdown header to the lookahead:

   ```python
   _THEORY_PROBLEM = re.compile(
       r"^([0-9]+)\.([0-9]+)\b\s+(.+?)"
       r"(?=^[0-9]+\.[0-9]+\b|^##\s+REVIEW QUESTIONS|"
       r"^Multiple Choice\.|^Matching\.|^True/False\.|^Completion\.|"
       r"^##\s*Chapter\s+\d|\Z)",
       re.MULTILINE | re.DOTALL,
   )
   ```

   This bounds problem 1.30's solution to its own paragraphs only; everything after the chapter ends is not its body.

3. **Add four enumerator helpers**. Each takes `full_text` (concatenation of cleaned-md pages) and `chapter` (string like `"1"`) and returns `list[ProblemUnit]`. Called from `enumerate_problems` after the existing theory-problem loop.

   **`_enumerate_multiple_choice(full_text, chapter)`:**

   - Locate MC section span using `_MC_SECTION` lookahead to next section (`_MATCHING_SECTION | _TF_SECTION | _COMPLETION_SECTION | r"^##" | \Z`).
   - Within the span, match each item: `^(\d+)\.\s+(.+?)\n((?:\([a-z]\)\s+.+?\n){2,5})` with **`re.MULTILINE` ONLY (NOT `re.DOTALL`)**. Group 1 = item number, group 2 = stem, group 3 = choices block (lines like `(a) text\n(b) text\n(c) text\n(d) text`). DOTALL was tested empirically and reduced the match count from 15 to 1 because the lazy `(.+?)` greedily consumes newlines before the choices block. Without DOTALL all 15 items match. Choice quantifier widened to `\([a-z]\)` and `{2,5}` to handle Bishop or 5-choice variants.
   - For each match build:
     ```python
     statement = f"{item_num}. {stem}\n{choices_block}".strip()
     pid = f"MC-CH{chapter}-{item_num}"
     ProblemUnit(
         problem_id=pid,
         subtype="multiple_choice",
         chapter=chapter,
         statement=statement,
         solution=None,  # paired in Stage 2c
         char_count=len(statement),
     )
     ```

   **`_enumerate_matching(full_text, chapter)`:**

   - Locate Matching section span: `_MATCHING_SECTION` to next section.
   - Inside, find Column A block (`^##\s+Column A\s*\n` to `^##\s+Column B`) and Column B block (`^##\s+Column B\s*\n` to end-of-section). Both regexes are simple.
   - **Column A items**: `^(?:\$(?:\\_)+\$\s+)?(\d+)\.\s+(.+?)(?=^(?:\$(?:\\_)+\$\s+)?\d+\.\s|^##|\Z)` (multiline+DOTALL). The `$\_\_\_\_$` prefix is Mathpix's rendering of an answer-blank line and must be stripped; some items lack it. **Note:** the actual OCR is `$\_\_\_\_$` (alternating backslash-underscore pairs, NOT a single backslash followed by multiple underscores). The regex must use `\$(?:\\_)+\$`, NOT `\$\\_+\$`.
   - **Column B options**: `^\(([a-e])\)\s+(.+)$` per line — build a `dict[str, str]` mapping letter → option text.
   - For each Column A item:
     ```python
     pid = f"MAT-CH{chapter}-{item_num}"
     # Statement must include Column B options inline for self-containment
     options_text = "\n".join(f"({L}) {opt}" for L, opt in column_b.items())
     statement = f"{item_num}. {stmt}\n\nOptions:\n{options_text}"
     ProblemUnit(
         problem_id=pid,
         subtype="matching",
         chapter=chapter,
         statement=statement,
         solution=None,
         char_count=len(statement),
     )
     ```
   - **OCR drift handling**: Schaum's CH01 OCR is missing item 5 in Column A (Mathpix glitch). Enumerator must NOT fabricate missing items — just enumerate what's present. The audit will flag the back-of-book entry for item 5 as `unpaired_solutions` (because no problem was enumerated to pair it to). That's the right signal.

   **`_enumerate_true_false(full_text, chapter)`:**

   - Locate T/F section span: `_TF_SECTION` to next section.
   - Match each item: `^(?:\$(?:\\_)+\$\s+)?(\d+)\.\s+(.+?)(?=^(?:\$(?:\\_)+\$\s+)?\d+\.\s|^##|\Z)` (multiline+DOTALL). **Same blank-token form as Matching:** `\$(?:\\_)+\$`, NOT `\$\\_+\$`.
   - The `$\_\_\_\_$ ` prefix is Mathpix's answer-blank line marker — strip it from the captured statement.
   - The underlined word is **not preserved** in the OCR. The card's statement carries the full prose; the back will be `T` or the replacement word. Learners self-identify the underlined word from the correction.
   - Build:
     ```python
     pid = f"TF-CH{chapter}-{item_num}"
     statement = f"{item_num}. True or false: {stmt_text}\n\nIf false, what word replaces the originally underlined term?"
     ProblemUnit(
         problem_id=pid,
         subtype="true_false",
         chapter=chapter,
         statement=statement,
         solution=None,
         char_count=len(statement),
     )
     ```

   **`_enumerate_completion(full_text, chapter)`:**

   - Locate Completion section span. Schaum's CH01 doesn't have Completion; CH02 does (back-of-book at page 12 line 26). Anchor on `_COMPLETION_SECTION`.
   - Match each item: `^(\d+)\.\s+(.+?\$(?:\\_)+\$.+?)(?=^\d+\.\s|^##|\Z)` (multiline+DOTALL). The body MUST contain a `$\_\_\_\_$` token (Mathpix's blank rendering) — that's how Completion items are distinguished from numbered prose. **Same blank-token form as Matching/T-F:** `\$(?:\\_)+\$`, NOT `\$\\_+\$`.
   - Build:
     ```python
     pid = f"CMP-CH{chapter}-{item_num}"
     # Replace mathpix blank token with a readable placeholder
     readable = body.replace("$\\_\\_\\_\\_$", "____")
     statement = f"{item_num}. Fill in the blank: {readable}"
     ProblemUnit(
         problem_id=pid,
         subtype="completion",
         chapter=chapter,
         statement=statement,
         solution=None,
         char_count=len(statement),
     )
     ```

4. **Wire enumerators into `enumerate_problems`**. After the existing theory-problem loop (line 144), add:

   ```python
   # Detect chapter context for subtype-prefixed IDs. Use the chapter_id arg if
   # provided (e.g. "alcamo2010_CH01" → "1"); otherwise scan the text for a
   # `# CHAPTER N` or `## Chapter N` header.
   chapter_num = _detect_chapter(full_text, chapter_id)

   problems.extend(_enumerate_multiple_choice(full_text, chapter_num))
   problems.extend(_enumerate_matching(full_text, chapter_num))
   problems.extend(_enumerate_true_false(full_text, chapter_num))
   problems.extend(_enumerate_completion(full_text, chapter_num))

   return problems
   ```

   Add `_detect_chapter(full_text, chapter_id) -> str` helper:
   - If `chapter_id` matches `r"_CH0?(\d+)"`, return the captured digits. The `0?` consumes any leading zero so `"alcamo2010_CH01"` returns `"1"` (NOT `"01"`). Verified empirically.
   - Else regex search for `^#{1,2}\s*(?:CHAPTER|Chapter)\s+(\d+)` in `full_text` and return the first match.
   - Default to `"unknown"` (the audit will flag).

5. **Restructure back-of-book pairing to two-pass + add four subtype pairers**. The existing Stage 2b regex `^Chapter\s+(\d+)\s*\n+\s*Multiple Choice` requires immediate adjacency between `Chapter N` header and `Multiple Choice` heading — verified against page-12 OCR this **never matches** because Schaum's intersperses other section blocks between them (Chapter 2 has `Multiple Choice → True/False → Completion`; the Matching pairer can't find Matching when MC sits between Chapter and Matching). Replace Stage 2b's monolithic regex AND add Stages 2c/2d/2e via a single chapter-partition + section-scan pattern.

   **Helper functions to add at module level:**

   ```python
   _BACK_CHAPTER_HEADER = re.compile(r"^##\s+Chapter\s+(\d+)\s*$", re.MULTILINE)
   _BACK_SECTION_HEADER = re.compile(
       r"^##\s+(Multiple Choice|Matching|True/False|Completion)\s*$",
       re.MULTILINE,
   )

   def _partition_back_of_book(full_text: str) -> dict[str, dict[str, str]]:
       """Walk the back-of-book block and return {chapter_num: {section: body}}.

       Pass 1: locate every `^## Chapter N$` boundary; record start index per chapter.
       Pass 2: within each chapter span, scan `^## (Multiple Choice|Matching|...)`
       boundaries; capture the body text from each section header to the next
       section header or chapter header or end-of-text.
       """
       # ... see skeleton below ...

   def _extract_column_b(full_text: str, chapter: str) -> dict[str, str]:
       """Locate the in-chapter `## Column B` block for the given chapter and
       parse its `(letter) option` lines into a dict.

       Walks `_CHAPTER_HEADER` boundaries to find the chapter's span, then within
       the span finds `^##\\s+Column B\\s*$\\n((?:\\([a-z]\\)\\s+.+\\n)+)`. Returns
       {} if Column B is absent (chapter has no Matching section).
       """
       # ... see skeleton below ...
   ```

   **Stage 2b/2c/2d/2e** then becomes uniform:

   ```python
   back_of_book = _partition_back_of_book(full_text)
   for chapter_num, sections in back_of_book.items():
       for section_name, body in sections.items():
           if section_name == "Multiple Choice":
               # Pair pattern: 1. c 2. c 3. a ... (single letter answer)
               for m in _MC_ANSWER_PAIR.finditer(body):
                   mc_num, letter = m.group(1), m.group(2)
                   _try_pair_or_unpaired(
                       pairings_by_id,
                       unpaired_solutions,
                       candidate_ids=[f"MC-CH{chapter_num}-{mc_num}", f"MC-{mc_num}"],
                       text=f"({letter})",  # MC pairer keeps short — full choice expansion is the LLM's job via the system prompt
                       role="solution",
                       page_idx=0,
                   )
           elif section_name == "Matching":
               column_b = _extract_column_b(full_text, chapter_num)
               for m in _MC_ANSWER_PAIR.finditer(body):
                   mat_num, letter = m.group(1), m.group(2)
                   option_text = column_b.get(letter, f"({letter})")
                   _try_pair_or_unpaired(
                       pairings_by_id,
                       unpaired_solutions,
                       candidate_ids=[f"MAT-CH{chapter_num}-{mat_num}", f"MAT-{mat_num}"],
                       text=f"({letter}) {option_text}",
                       role="solution",
                       page_idx=0,
                   )
           elif section_name == "True/False":
               # Mixed letter (T/F) or replacement word/phrase (multi-word ok).
               for m in _TF_ANSWER_SPLIT.finditer(body):
                   tf_num, raw_answer = m.group(1), m.group(2).strip()
                   if raw_answer == "T":
                       text = "True."
                   elif raw_answer == "F":
                       text = "False."
                   else:
                       text = f"False — replace underlined word with: {raw_answer}"
                   _try_pair_or_unpaired(
                       pairings_by_id,
                       unpaired_solutions,
                       candidate_ids=[f"TF-CH{chapter_num}-{tf_num}", f"TF-{tf_num}"],
                       text=text,
                       role="solution",
                       page_idx=0,
                   )
           elif section_name == "Completion":
               for m in _CMP_ANSWER_SPLIT.finditer(body):
                   cmp_num, answer = m.group(1), m.group(2).strip()
                   _try_pair_or_unpaired(
                       pairings_by_id,
                       unpaired_solutions,
                       candidate_ids=[f"CMP-CH{chapter_num}-{cmp_num}", f"CMP-{cmp_num}"],
                       text=answer,
                       role="solution",
                       page_idx=0,
                   )
   ```

   `_try_pair_or_unpaired` is a small helper that tries each candidate ID in order, appends to the matching pairing when found, OR appends to `unpaired_solutions` when none match. **Critical:** the existing Stage 2b loop body (lines 230-247) DROPS unmatched pairs on the floor; that bug-mirroring would break `test_unpaired_back_of_book_answer_for_missing_matching_item5_logs_warning`. The new helper must always either pair or add to `unpaired_solutions`.

   ```python
   def _try_pair_or_unpaired(
       pairings_by_id: dict[str, ProblemPairing],
       unpaired_solutions: list[ProblemLocation],
       candidate_ids: list[str],
       text: str,
       role: Literal["statement", "solution"],
       page_idx: int,
   ) -> bool:
       """Try each candidate ID; append to first match's pairing OR to unpaired_solutions.

       Returns True if paired, False if added to unpaired.
       """
       for cid in candidate_ids:
           pair = pairings_by_id.get(cid)
           if pair is not None:
               pair.solutions.append(
                   ProblemLocation(
                       problem_id=cid, role=role, page_idx=page_idx,
                       start_char=0, end_char=len(text), text=text,
                   )
               )
               return True
       unpaired_solutions.append(
           ProblemLocation(
               problem_id=candidate_ids[0], role=role, page_idx=page_idx,
               start_char=0, end_char=len(text), text=text,
           )
       )
       return False
   ```

   **Answer-split regexes (T/F and Completion handle multi-word answers):**

   ```python
   # T/F: answer is single letter T/F OR a multi-word phrase. Use a non-greedy
   # capture that terminates at the next `\d+\.` lookahead OR end-of-text.
   _TF_ANSWER_SPLIT = re.compile(
       r"(\d+)\.\s+(T|F|.+?)(?=\s+\d+\.\s|\s*\Z)",
       re.DOTALL,
   )

   # Completion: answer is one word or short phrase, multi-word common.
   # Optional whitespace before the period handles OCR drift like `4 . hydrogen`.
   _CMP_ANSWER_SPLIT = re.compile(
       r"(\d+)\s*\.\s+(.+?)(?=\s+\d+\s*\.|\s*\Z)",
       re.DOTALL,
   )
   ```

   The `.+?` (any-char-non-greedy) is robust against multi-word phrases including spaces and even digits (rare). The `[^0-9]+?` form was tested and breaks on Bishop-style answers that might contain digits; `.+?` with the boundary lookahead is the right trade-off.

   **Strip all captured answers** before persisting — verified that `15. underlined\n\n` captures with trailing newlines that need `.strip()`.

6. **Subtype-aware prompt formatter** in `_format_problem_card_prompt` (line 342). Replace the single shared template with a dispatch table:

   ```python
   _PROMPT_KEY_BY_SUBTYPE = {
       "theory_problem": "problem_card_gen",  # existing
       "multiple_choice": "problem_card_gen_multiple_choice",
       "matching": "problem_card_gen_matching",
       "true_false": "problem_card_gen_true_false",
       "completion": "problem_card_gen_completion",
   }

   def _format_problem_card_prompt(problem, plan, doc_summary, citation_key) -> str:
       # ... existing tag/subtype-list construction unchanged ...
       template_key = _PROMPT_KEY_BY_SUBTYPE.get(problem.subtype, "problem_card_gen")
       # The user prompt body stays identical (all the LLM needs is the resolved
       # statement + solution + plan); the subtype-specific guidance lives in the
       # SYSTEM prompt loaded at the call site (problem_card_gen_agent.run_sync
       # at line 417 reads `instructions=system_prompt`).
       # Return the shared user prompt; the system prompt selection happens in
       # generate_cards_for_problem.
       return (... unchanged template ...)
   ```

   Then update `generate_cards_for_problem` (line 408) to load the per-subtype system prompt:

   ```python
   prompts_root = config.get("prompts", {}).get("prompts", {})
   sm_prompts = prompts_root.get("solution_manual", {})
   prompt_key = _PROMPT_KEY_BY_SUBTYPE.get(problem.subtype, "problem_card_gen")
   system_prompt = sm_prompts.get(prompt_key, sm_prompts.get("problem_card_gen", ""))
   ```

7. **Add `problem_subtype_counts` to the cards-debug.yaml dump** in `run_solution_manual_override`. Currently the artifact has `subtype_counts: dict[str, int]` keyed by `card_subtype` (problem_main / problem_overview / etc.). With four new `ProblemUnit.subtype` values, observability of "which review-section subtypes are landing" requires a separate count. Add a sibling field built from the input `problems` list:

   ```python
   from collections import Counter
   problem_subtype_counts = Counter(p.subtype for p in problems)
   debug_path.write_text(
       yaml.safe_dump(
           {
               "n_cards": len(all_cards),
               "subtype_counts": dict(Counter(c.card_subtype for c in all_cards)),
               "problem_subtype_counts": dict(problem_subtype_counts),
               "cards": [...],
           },
           sort_keys=False,
       )
   )
   ```

   Lets the integration smoke test verify `problem_subtype_counts == {"theory_problem": 6, "multiple_choice": 15, "matching": 9, "true_false": 15}` for Schaum's CH01.

8. **Update strict-mode error message** (line 547-552) to mention all enumerated subtypes:

   ```python
   raise RuntimeError(
       "No problems enumerated. Verify the input PDF contains numbered "
       "items in any of: theory-problems (N.M), Multiple Choice (1./2./...), "
       "Matching (Column A items), True/False (numbered statements), "
       "or Completion (numbered fill-in-blank items)."
   )
   ```

**Code diff sketch for `enumerate_problems`:**

```python
def enumerate_problems(clean_md_files, chapter_id=None) -> list[ProblemUnit]:
    problems: list[ProblemUnit] = []
    full_text = "\n\n".join(f.read_text() for f in clean_md_files)

    # 1. Theory-problems (existing — unchanged)
    for m in _THEORY_PROBLEM.finditer(full_text):
        # ... existing body ...
        problems.append(ProblemUnit(...))

    # 2. Detect chapter for subtype-prefixed IDs
    chapter_num = _detect_chapter(full_text, chapter_id)

    # 3. Review subtypes — each enumerator no-ops if its section header isn't found
    problems.extend(_enumerate_multiple_choice(full_text, chapter_num))
    problems.extend(_enumerate_matching(full_text, chapter_num))
    problems.extend(_enumerate_true_false(full_text, chapter_num))
    problems.extend(_enumerate_completion(full_text, chapter_num))

    return problems
```

### `swanki/conf/prompts/solution_manual.yaml` (MODIFY)

**Current state:** lines 38-66 have `prompts.solution_manual.problem_card_gen` as the single shared system prompt.

**Changes:** keep `problem_card_gen` as the theory-problem default; add four new keys. All four reuse the existing prompt's "tag preservation, self-containment, no length cap on full_solution, provenance for full_solution" rules but add format-specific instructions.

```yaml
prompts:
  solution_manual:
    # ... existing problem_enumeration, main_with_overlap_instruction, problem_card_gen ...

    problem_card_gen_multiple_choice: |-
      You receive ONE multiple-choice problem with its stem and four lettered choices
      (a)-(d), plus the back-of-book correct letter (in `Solution:` field, formatted as
      "(c)"). Generate exactly one problem_main card.

      Front: include the full stem + ALL four choices verbatim, formatted as a
      readable list. Begin with the problem ID label, e.g. "MC 1.1: ..." (NOT just
      the bare number).

      Back: state the correct full choice text — NOT just the letter. Example: if
      the answer is "(c) van Leeuwenhoek", write "(c) van Leeuwenhoek" with a brief
      one-sentence justification. Keep total back text ≤500 chars.

      Required tags + canonical problem tag are listed in the user prompt; preserve
      all of them on the emitted card.

      Set card_subtype="problem_main" on the emitted card.

    problem_card_gen_matching: |-
      You receive ONE Matching item: a Column-A statement plus the full Column B
      option list (5 options, letters a-e). Solution is the back-of-book matched
      letter (formatted as "(c) Viruses" — full option text included).

      Front: present the Column A statement and ALL Column B options inline so the
      learner can match without external context. Format as numbered statement +
      bulleted options.

      Back: the correct option (full text + letter) plus a one-line rationale.
      ≤500 chars.

      Set card_subtype="problem_main".

    problem_card_gen_true_false: |-
      You receive ONE True/False statement (the originally-underlined word is NOT
      marked in the source — it was lost in OCR). Solution is either "T" / "True",
      "F" / "False", or "False — replace underlined word with: <word>".

      Front: present the statement verbatim, prefixed with "True or False:". Add
      "If false, which word replaces the originally underlined term?" as the second
      line.

      Back: render as one of:
        - "True." (no further text needed)
        - "False — should read '<word>' instead of '<originally-underlined>'." If
          you cannot identify the originally-underlined word from context, just
          write "False — the corrected word is <word>".
      ≤500 chars.

      Set card_subtype="problem_main".

    problem_card_gen_completion: |-
      You receive ONE Completion item: a sentence with one blank (rendered as
      "____"). Solution is the fill-in word or short phrase from the back-of-book.

      Front: present the sentence with the blank intact, prefixed with "Fill in
      the blank:".

      Back: state the answer phrase, then a one-sentence rationale connecting it to
      the sentence's meaning. ≤500 chars.

      Set card_subtype="problem_main".
```

### `swanki/models/problem_set.py` (MODIFY)

**Current state:** `_PROBLEM_TAG_RE` at line 168 accepts `[0-9]+\.[0-9]+|MC-\d+|[A-Z]+-\d+`. Verified empirically: this **does not** match the chapter-prefixed forms `MC-CH1-1`, `MAT-CH1-3`, `TF-CH1-7`, `CMP-CH2-9` because the regex requires the prefix-letters to be immediately followed by `-\d+`, not by `-CH\d+-\d+`.

**Critical chain:** without this fix, every newly-enumerated review problem's tag fails to parse. `audit_coverage` Part 3 (problem_set.py:489-505) calls `ProblemTag.parse` per `problem_main` card tag, increments `main_card_counts[pid]` only on a successful parse, and raises `CoverageError(missing={...})` when any enumerated problem ID has zero parsed cards. Result: integration smoke test hard-fails with every prefixed problem listed as missing-from-cards.

**Changes:**

1. **Update `_PROBLEM_TAG_RE`** (line 168) to accept the chapter-prefixed forms:

   ```python
   _PROBLEM_TAG_RE = re.compile(
       r"^([^.]+)\.problem\.([0-9]+\.[0-9]+|[A-Z]+(?:-CH\d+)?-\d+)$"
   )
   ```

   The middle alternation `[A-Z]+(?:-CH\d+)?-\d+` covers:
   - `MC-1` (bare form, fallback when chapter unknown)
   - `MC-CH1-7` (chapter-prefixed primary form)
   - `MAT-CH1-3`, `TF-CH1-7`, `CMP-CH2-9` (other subtypes)
   - The leading `[0-9]+\.[0-9]+` alternative for theory-problems is unchanged.

2. **No other model changes.** `ProblemSubtype` literal already includes all five subtypes (line 21-23). `ProblemUnit` shape is unchanged (subtype-specific data lives in `statement`/`solution` prose).

### `tests/test_problem_set.py` (NEW)

**Purpose:** unit tests for the new enumerators and pairing stages, anchored on the actual Schaum's CH01 OCR fixtures. First problem-set test file in the repo.

**Depends on:** `pytest`, `swanki.pipeline.problem_set`, fixture files under `tests/fixtures/problem_set/`.

**Test cases:**

- `test_enumerate_multiple_choice_finds_all_15` — fixture is `tests/fixtures/problem_set/schaum_ch01_mc_section.md` (extracted from page-8 lines 21-29 + page-9 + page-10 lines 1-30). Assert `_enumerate_multiple_choice` returns exactly 15 ProblemUnits with IDs `MC-CH1-1` through `MC-CH1-15`, each with the four `(a)/(b)/(c)/(d)` choices in the statement.
- `test_enumerate_matching_skips_missing_item5` — fixture extracted from page-10 lines 32-48 + page-11 lines 1-2. The Schaum's OCR drops Column-A item 5; assert `_enumerate_matching` returns 9 items (IDs `MAT-CH1-1`, `-2`, `-3`, `-4`, `-6`, `-7`, `-8`, `-9`, `-10`) and does NOT fabricate item 5. Each statement includes the full Column B options block (5 items, letters a-e).
- `test_enumerate_true_false_strips_blank_marker` — fixture from page-11 lines 4-19. Assert 15 items, IDs `TF-CH1-1` through `TF-CH1-15`. Assert the `$\_\_\_\_$` prefix is stripped from each `statement`. Assert the front prompt contains "True or false:" as the prefix.
- `test_enumerate_completion_requires_blank_token` — synthesized fixture from page-12 line 26 (CH2 Completion answer block) plus a fabricated Chapter-2 question section that includes the `$\_\_\_\_$` token. Assert `_enumerate_completion` returns N items only when the body contains the blank token; numbered-but-blankless items (e.g. plain numbered prose) are NOT enumerated.
- `test_pair_mc_back_of_book_with_markdown_chapter_header` — fixture is page-12 (back-of-book block). Construct 15 MC pairings via the enumerator, then run `pair_problems_across_pages`. Assert each `MC-CH1-{n}` pairing has exactly one solution. Assert solution text format is `"(c) <full choice text>"` not just `"(c)"`. **This is the test that would have caught the existing `_MC_ANSWER_BLOCK` bug** — the regex must handle `## Chapter 1\n## Multiple Choice` (markdown-promoted headers).
- `test_pair_matching_lookup_column_b` — same fixture; assert `MAT-CH1-{n}` pairings carry solution text like `"(c) Viruses"` (full Column B option text), not just `"(c)"`.
- `test_pair_true_false_handles_mixed_letter_word` — assert pairings for items where answer is `T` get text `"True"`; pairings where answer is multi-word like `"Louis Pasteur"` get text `"False — replace underlined word with: Louis Pasteur"`.
- `test_pair_completion_handles_multi_word_answers` — fixture from page-12 line 26 (CH2 Completion). Assert `CMP-CH2-3` gets text `"organic compounds"` (multi-word) and `CMP-CH2-9` gets text `"dehydration synthesis"`.
- `test_audit_coverage_with_all_subtypes_passes` — construct ProblemUnits for 30 theory + 15 MC + 9 Matching (item 5 missing) + 15 T/F = 69 problems. Construct PairingResult with all paired. Construct 69 `problem_main` cards with correct ProblemTag prefixes. Assert `audit_coverage(problems, pairings, cards, citation_key, allow_unsolved=False)` does not raise.
- `test_audit_coverage_unpaired_mc_raises` — same fixture with one MC pairing's `solutions=[]`; assert `CoverageError` raised with `unsolved=={"MC-CH1-7"}`.
- `test_audit_coverage_missing_main_card_raises` — same fixture with one card removed; assert `CoverageError(missing={"<id>"})`.
- `test_unpaired_back_of_book_answer_for_missing_matching_item5_logs_warning` — fixture has Column A items 1, 2, 3, 4, 6, 7, 8, 9, 10 (no 5); back-of-book has answers for 1-10. Assert `pair_problems_across_pages` puts the answer for item 5 into `result.unpaired_solutions` (not into any pairing). **Critical:** this depends on the new `_try_pair_or_unpaired` helper appending to `unpaired_solutions` when no candidate ID matches — the existing Stage 2b drop-on-floor pattern must NOT be mirrored.
- `test_format_problem_card_prompt_dispatches_per_subtype` — monkeypatch `problem_card_gen_agent.run_sync` to capture the `instructions` kwarg. Build one ProblemUnit per subtype (theory_problem, multiple_choice, matching, true_false, completion). Call `generate_cards_for_problem` for each. Assert the captured `instructions` matches `prompts.solution_manual.problem_card_gen_<subtype>` (or the legacy `problem_card_gen` for theory_problem). Catches dispatch typos in `_PROMPT_KEY_BY_SUBTYPE`.

**Fixture path resolution:** all tests resolve fixture files via `Path(__file__).parent / "fixtures" / "problem_set" / "<name>.md"` — NOT via raw string paths like `"tests/fixtures/..."` (which break when pytest runs from a non-repo cwd). Match the existing convention used by other test files in the repo.

**Markers:** all unit tests, no `@pytest.mark.llm` or `@pytest.mark.integration`. LLM call is not exercised; only enumeration + pairing + audit, which are pure regex/Pydantic.

### `tests/fixtures/problem_set/` (NEW directory)

Six markdown fixture files, each carrying a real OCR snippet from `/scratch/projects/torchcell-scratch/Swanki_Data/alcamoSchaumsOutlineMicrobiology2010_CH01_6/clean-md-singles/`. Direct copies — do NOT hand-edit; the goal is to test against the real Mathpix output so future OCR changes surface as test failures.

- `schaum_ch01_mc_section.md` — copied from `page-8.md` line 21 to `page-10.md` line 30 (boundaries: starts with `## REVIEW QUESTIONS` heading, ends just before the `Matching.` line).
- `schaum_ch01_matching_section.md` — copied from `page-10.md` line 32 to `page-11.md` line 2.
- `schaum_ch01_true_false_section.md` — copied from `page-11.md` lines 4-19.
- `schaum_ch02_completion_section.md` — synthesized fixture with a `Completion. Fill in the blanks ...` header plus 15 numbered items, each containing a `$\_\_\_\_$` blank token. Hand-write because CH01 has no Completion section. Pair fixture answers in next file.
- `schaum_ch01_back_of_book.md` — copied from `page-12.md` (full file, includes CH1 + CH2 + CH3 answer blocks).
- `schaum_ch01_packed_full.md` — concatenation of pages 1-12 (the entire packed OCR). Used by the integration test `test_audit_coverage_with_all_subtypes_passes`.

Tests load fixtures via `Path(__file__).parent / "fixtures" / "problem_set" / "<name>.md"`. No `conftest.py` registration needed; pytest picks them up via the resolved path.

**Fixture build commands** (run during implementation):

```bash
WT=/home/michaelvolk/Documents/projects/Swanki.worktrees/plan/solution-manual-mode-for-problem-set-pdfs
SRC=/scratch/projects/torchcell-scratch/Swanki_Data/alcamoSchaumsOutlineMicrobiology2010_CH01_6/clean-md-singles
mkdir -p "$WT/tests/fixtures/problem_set"

# MC section spans page-8 line 21 through page-10 line 30
{ sed -n '21,29p' "$SRC/page-8.md"; cat "$SRC/page-9.md"; sed -n '1,30p' "$SRC/page-10.md"; } > "$WT/tests/fixtures/problem_set/schaum_ch01_mc_section.md"

# Matching section: page-10 line 32 through page-11 line 2
{ sed -n '32,$p' "$SRC/page-10.md"; sed -n '1,2p' "$SRC/page-11.md"; } > "$WT/tests/fixtures/problem_set/schaum_ch01_matching_section.md"

# T/F section: page-11 lines 4-19
sed -n '4,19p' "$SRC/page-11.md" > "$WT/tests/fixtures/problem_set/schaum_ch01_true_false_section.md"

# Back-of-book: full page-12
cp "$SRC/page-12.md" "$WT/tests/fixtures/problem_set/schaum_ch01_back_of_book.md"

# Concatenated full chapter
for i in $(seq 1 12); do cat "$SRC/page-$i.md"; printf '\n\n'; done > "$WT/tests/fixtures/problem_set/schaum_ch01_packed_full.md"

# CH02 Completion fixture — hand-write (no real OCR available for the question section)
```

### `tests/test_problem_set_models.py` (NEW)

**Purpose:** Pydantic validation tests — small, defensive, no enumeration logic.

**Test cases:**

- `test_problem_tag_round_trip_mc` — `ProblemTag(citation_key="alcamo2010", problem_id="MC-CH1-7").render()` returns `"alcamo2010.problem.MC-CH1-7"`; `ProblemTag.parse(rendered, "alcamo2010")` returns the same model.
- `test_problem_tag_round_trip_matching_tf_completion` — same for `MAT-CH1-3`, `TF-CH1-7`, `CMP-CH2-9`.
- `test_problem_tag_parse_rejects_lowercase_prefix` — `ProblemTag.parse("alcamo2010.problem.mc-CH1-7", "alcamo2010")` returns `None`.
- `test_problem_unit_subtype_literal_accepts_all_five` — construct ProblemUnit with each of the 5 subtypes; no validation error.
- `test_problem_unit_rejects_invalid_subtype` — construct with `subtype="bogus"`; assert `ValidationError`.

**Markers:** none.

### `notes/swanki.pipeline.problem_set.md` (MODIFY)

**Current state:** has dated section `2026.04.26 - Initial implementation`.

**Changes:** append a new dated section.

```markdown
## 2026.05.04 - MC / Matching / True-False / Completion enumeration

Added four new enumerator helpers to `enumerate_problems` (multiple choice, matching, true/false, completion) and four new Stage-2 pairing branches (Stage 2c/2d/2e for matching/T-F/completion answer blocks). Each subtype gets a prefixed problem_id (`MC-CH{n}-{m}`, `MAT-CH{n}-{m}`, etc.) and routes through the existing `problem_card_gen_agent` with a subtype-specific system prompt loaded from `prompts.solution_manual.problem_card_gen_<subtype>`.

The `_MC_ANSWER_BLOCK` regex was also fixed to accept the markdown-promoted form `## Chapter N\n## Multiple Choice` (Mathpix promotes the back-of-book section headers to H2 even though the in-chapter dividers remain inline). The original regex never matched anything because of this — verified empirically by inspecting `problem-pairings.yaml` from the alcamoSchaumsOutlineMicrobiology2010_CH01_6 run, which had all back-of-book answers in `unpaired_solutions: []`.

True/False solutions render as `"True"`, `"False"`, or `"False — replace underlined word with: <word>"`. The originally-underlined word is NOT recoverable from Mathpix OCR (verified — the markup is dropped); the card design accepts this and lets the learner self-identify the underlined word by comparing the statement to the correction.

Completion items require a `$\_\_\_\_$` token (Mathpix's blank rendering) in the body to be enumerated; numbered prose without a blank is correctly skipped. Multi-word answers in the back-of-book block (e.g. `"organic compounds"`, `"peptide bond"`) are handled by a non-greedy split regex that lets answers contain spaces.

End-state target: alcamoSchaumsOutlineMicrobiology2010 Ch1 should produce ~70 review-section cards (15 MC + ~9 Matching + 15 T/F + 30 theory) instead of the previous 6.
```

## Edge Cases

1. **Chapter context absent.** If `chapter_id` is empty AND `_detect_chapter` finds no `Chapter N` header, the IDs use `"unknown"` as the chapter prefix (`MC-CHunknown-1`). The audit will still pair correctly because Stage-2c/2d/2e build IDs from the back-of-book `Chapter N` block (so back-of-book is the source of truth for chapter number when forward-detection fails). The bare-form fallback (`MC-1`) covers the case where back-of-book also lacks a `Chapter N` header.
2. **OCR drops a numbered item.** Schaum's CH01 Matching is missing item 5. Enumerator MUST NOT fabricate; it returns 9 items. The back-of-book entry for item 5 lands in `unpaired_solutions` as a warning. The audit does not hard-fail (Part 1 only checks that enumerated problems appear in pairings; missing-from-OCR items aren't enumerated and so are not in the contract).
3. **Two chapters in the same input PDF.** Schaum's books are typically one-chapter-at-a-time via `schaum_chapter_pack.py`, but Bishop and others may concatenate multiple chapters. The chapter-prefixed IDs make this safe; Stage-2 pairing iterates all `Chapter N` blocks. Bare-form fallback is dropped when chapter prefix is detected.
4. **Mid-chapter section divider on a transition page.** Already covered by the existing classifier's inline-heading regex (lines 49-53 of `swanki/pipeline/section_classifier.py`). If a chapter page contains both the last theory-problem AND the start of `Multiple Choice. ...`, the page is classified as `review_exercises` and theory-problems on that page get problem-set treatment. This is a known limit (plan note Edge Case 13) — not addressed in this work.
5. **MC answer letter outside `[a-d]`.** Schaum's might use `(e)` for some chapters. The MC enumerator regex `\([a-d]\)` would skip `(e)`. Widen to `\([a-z]\)` to be safe, but cap at 5 choices in the regex `{2,5}` quantifier.
6. **True/False replacement word contains a digit.** `_TF_ANSWER_SPLIT` uses `[^0-9]+?` which would terminate prematurely. Inspect Schaum's CH01 T/F answers (page-12 lines 13-14) — none contain digits. If Bishop or future fixtures break this, swap to a smarter splitter that uses `\d+\.\s` lookahead instead of `[^0-9]+?` greedy capture.
7. **Completion answer is a single character or symbol.** `[^0-9]+?` non-greedy still works because the next-item-boundary lookahead `(?=\s+\d+\s*\.|\Z)` handles both. Verify with the `4 . hydrogen bonds` OCR drift case (space before period).
8. **Matching's Column B has fewer letters than items.** Schaum's CH01 has 5 options (a-e) for 10 items — options repeat as answers. The enumerator stores the dict, and Stage 2c looks up by letter. No issue. If options exceed the alphabet (>26), the existing regex naturally matches `[a-z]` and the upstream OCR would handle multi-char letters separately if they exist.
9. **Audit Part 3 with cards spanning all subtypes.** With 15 MC cards (each tagged `MC-CH1-N`) + 9 Matching (MAT-CH1-N) + 15 T/F (TF-CH1-N), the `Counter`-based check at audit_coverage line 503 naturally counts each subtype's IDs separately. No code change needed; verify by running the audit test in the new test suite.
10. **Multiple `Multiple Choice` sections in one chapter.** Some chapters have a mid-chapter MC review AND an end-of-chapter MC review. The current section-locator helper picks the FIRST occurrence; if a chapter has two, only the first is enumerated. Not seen in Schaum's; flag for future work.

## Verification

After each file is implemented:

1. **Unit tests:** `pytest tests/test_problem_set.py tests/test_problem_set_models.py -xvs`
2. **Type check:** `mypy swanki/pipeline/problem_set.py swanki/models/problem_set.py`
3. **Lint:** `ruff check swanki/pipeline/problem_set.py swanki/conf/prompts/solution_manual.yaml`
4. **Integration smoke test:** re-run the existing `bash /scratch/alcamoSchaumsOutlineMicrobiology2010/ch01_packed.sh` (no edits to the runner). Expect:
   - `mode=full routing: 7 main_content pages, 5 review_exercises pages` (same as before).
   - `Wrote pairing artifact:` and `Wrote cards debug artifact:` log lines.
   - `cards-debug.yaml` shows `subtype_counts` with both `problem_main` (≥40) and the new per-subtype problem IDs visible in tags. Approximate target: 16 concept + 6 theory + 15 MC + 9 Matching + 15 T/F = ~61 cards (Schaum's CH01 has no Completion).
   - Audit passes (no `CoverageError`).
   - Per-card audio fires for all cards (`audio=all` in the runner).
   - Zotero sync uploads apkg + 3 doc-level mp3s.

## Execution

To implement, start a new Claude Code session in this worktree:

```
cd ~/projects/Swanki.worktrees/plan/solution-manual-mode-for-problem-set-pdfs
/read-codebase pipeline models
```

Then:

```
Implement the plan at notes/plan.mc-matching-tf-completion-enumeration.2026.05.04.md.
Read the plan first, then implement each file specification in order:

1. swanki/models/problem_set.py (MODIFY) — update _PROBLEM_TAG_RE to accept
   chapter-prefixed forms (MC-CH1-1, MAT-CH1-3, TF-CH1-7, CMP-CH2-9). This
   is the load-bearing fix; without it audit Part 3 would reject every new
   review-section card and fail.
2. swanki/pipeline/problem_set.py (MODIFY):
   - Fix _THEORY_PROBLEM lookahead so the last theory-problem doesn't
     greedy-capture the entire review section.
   - Restructure back-of-book pairing: replace _MC_ANSWER_BLOCK monolithic
     regex with _partition_back_of_book + _extract_column_b helpers.
   - Add _try_pair_or_unpaired helper (always pair OR append to
     unpaired_solutions; never drop on floor).
   - Add 4 in-chapter section regexes (drop the verb requirement —
     `_MC_SECTION = r"^Multiple Choice\.\s+\S"` is enough).
   - Add 4 enumerator helpers (MC, Matching, T/F, Completion). MC regex
     uses re.MULTILINE ONLY (NOT DOTALL — verified DOTALL drops 14/15
     items). Mathpix blank-token regex is `\$(?:\\_)+\$` everywhere
     (NOT `\$\\_+\$`).
   - Add _detect_chapter helper.
   - Wire 4 enumerators into enumerate_problems after the theory loop.
   - Add 4 pairing stages via the partition+section pattern (Stage 2c
     Matching, 2d T/F, 2e Completion; refactor existing 2b MC into the
     same shape).
   - Subtype-aware prompt-key dispatch in generate_cards_for_problem
     via _PROMPT_KEY_BY_SUBTYPE.
   - Add problem_subtype_counts to cards-debug.yaml dump.
   - Update strict-mode error message.
3. swanki/conf/prompts/solution_manual.yaml (MODIFY) — add 4 new
   problem_card_gen_<subtype> system prompts.
4. tests/fixtures/problem_set/ (NEW dir) — run the fixture-build commands
   listed in the plan to extract 5 real OCR snippets + hand-write the
   CH02 Completion fixture.
5. tests/test_problem_set_models.py (NEW) — ProblemTag round-trip tests
   for chapter-prefixed forms (this test verifies step 1's regex update).
6. tests/test_problem_set.py (NEW) — enumerator + pairing + audit tests +
   prompt-dispatch mock test.
7. notes/swanki.pipeline.problem_set.md (MODIFY) — append 2026.05.04
   dated section.
8. notes/swanki.models.problem_set.md (MODIFY) — append a 2026.05.04
   dated section noting the _PROBLEM_TAG_RE update.

Verify after each file (pytest + mypy + ruff). Commit with /update-notes ->
/stage -> /commit after the source changes (steps 1-3), then again after
fixtures + tests (steps 4-6), then again for the dendron notes (steps 7-8).

When all files are complete, run the integration smoke test from the
Verification section.
```

## Critic Review

### Feasibility

Critic found 6 P0 issues by running regexes against the actual Schaum's CH01 OCR. All resolved in revisions:

- **`ProblemTag.parse` rejected chapter-prefixed IDs** — initial plan claimed `[A-Z]+-\d+` accepts `MC-CH1-1`; verified empirically it does not. Added `swanki/models/problem_set.py` MODIFY spec with the regex extended to `[A-Z]+(?:-CH\d+)?-\d+`. Without this, audit Part 3 would hard-fail every newly-enumerated review problem.
- **MC enumerator with DOTALL matched only 1/15 items** — initial regex `^(\d+)\.\s+(.+?)$\n((?:\([a-d]\)\s+.+\n){2,4})` with DOTALL lost the line-anchor semantics. Plan now specifies `re.MULTILINE` only, with a callout noting DOTALL was tested and reduces matches.
- **Mathpix blank-token regex was wrong shape** — initial `\$\\_+\$` doesn't match the OCR's actual `$\_\_\_\_$` (alternating backslash-underscore pairs). Plan now uses `\$(?:\\_)+\$` everywhere with explicit notes.
- **Back-of-book pairing required immediate `Chapter N\nMultiple Choice` adjacency** — broke for chapters where `True/False` and `Completion` follow MC. Plan now restructures pairing into two-pass: `_partition_back_of_book` builds `{chapter: {section: body}}`, then a uniform per-subtype loop iterates the partition.
- **Column B lookup under-specified** — plan now includes `_extract_column_b(full_text, chapter)` helper signature and skeleton.
- **Theory-problem regex greedy-tail captured the entire review section** — verified empirically that problem 1.30's solution body ran ~7000 chars including all MC/Matching/T-F. Plan now extends `_THEORY_PROBLEM` lookahead to terminate on review-section dividers and the chapter-end markdown header.

Minor fixes:

- `_MC_SECTION` verb requirement narrowed to dropping verbs entirely (`^Multiple Choice\.\s+\S` only).
- MC choice quantifier unified to `\([a-z]\)` and `{2,5}`.
- T/F item-15 trailing-whitespace strip applied in pairing helper.
- `_detect_chapter` regex `_CH0?(\d+)` correctly captures `1` from `_CH01` (verified, doc-clarified).
- Missing-id pairing now appends to `unpaired_solutions` via `_try_pair_or_unpaired` helper (existing Stage 2b dropped on floor).

### Completeness

- **`_PROBLEM_TAG_RE` modify** now in spec (was claimed unchanged; critic caught the gap).
- **`problem_subtype_counts` debug field** added to `cards-debug.yaml` dump for per-subtype enumeration observability.
- **Fixture path resolution** specified via `Path(__file__).parent / "fixtures" / "problem_set"` to match repo convention.
- **Mock-based prompt-dispatch test** (`test_format_problem_card_prompt_dispatches_per_subtype`) added.
- **Fixture build commands** added inline (`sed -n` extracts from real OCR pages with explicit line ranges).
- **Stage 2c missing-id behavior** clarified — append to `unpaired_solutions` not drop.
- **Theory-problem greedy-tail bug** addressed.

### Specification Quality

After revisions:

| File | Rating |
|---|---|
| `swanki/models/problem_set.py` (MODIFY) | GREEN — single regex change, fully specified |
| `swanki/pipeline/problem_set.py` (MODIFY) | GREEN — all regexes verified against real OCR; helpers (`_partition_back_of_book`, `_extract_column_b`, `_try_pair_or_unpaired`) have signatures + skeletons |
| `swanki/conf/prompts/solution_manual.yaml` (MODIFY) | GREEN — four prompt strings with format-specific instructions |
| `tests/fixtures/problem_set/` (NEW) | GREEN — fixture build commands inline, real-OCR sourced |
| `tests/test_problem_set.py` (NEW) | GREEN — enumeration + pairing + audit + dispatch coverage |
| `tests/test_problem_set_models.py` (NEW) | GREEN — round-trip tests for all chapter-prefixed forms |
| `notes/swanki.pipeline.problem_set.md` (MODIFY) | GREEN — append-only dated section |
| `notes/swanki.models.problem_set.md` (MODIFY) | GREEN — append-only dated section noting tag-regex update |

Plan is ready for `/wt-implement` on a fresh context.
