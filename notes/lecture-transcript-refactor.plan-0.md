---
id: d5958htnunqq5m6o653ht9c
title: Plan 0
desc: ''
updated: 1773196343365
created: 1773180041048
---
Lecture Transcript Refactor

## Context

Two problems with lecture generation in `swanki/audio/lecture.py`:

**Problem 1 — SI as continuous stream**: When SI is stitched to the main paper PDF, the lecture generator treats it as one continuous document. This causes mid-lecture false conclusions ("time to summarize...") when the main paper ends, followed by an awkward restart when SI begins. Papers reference SI in their body ("Extended Data Fig. 6", "see Methods in SI"), and these reference points are where SI detail should be woven into the lecture — not as a separate block at the end.

Example: `ahlmann-eltzeDeeplearningbasedGenePerturbation2025` — main paper is 4 pages, SI is 13 pages. Currently all 17 pages are fed as a single stream.

**Problem 2 — Length control is broken**: Per-section word budgets fight against good lecture writing. Papers with many small sections produce absurdly long lectures because the LLM has a minimum output floor (~400-500 words) per section regardless of budget.

Evidence:

| Paper                      | Pages | Source words | Lecture words | Ratio   |
|----------------------------|-------|--------------|---------------|---------|
| tazza (8pp, no SI)         | 8     | 6,707        | 5,928         | **88%** |
| espinel-rios (14pp, no SI) | 14    | 10,419       | 5,130         | 49%     |
| avsec (26pp, 12+14 SI)     | 26    | 11,354       | 3,110         | 27%     |

tazza has 13 numbered sections → per-section budget of ~258 words → LLM generates ~450 words minimum per section → 13 × 450 = 5,850 words (88%). The cumulative length check (line 577) only logs a warning without adjusting behavior.

**Pipeline reality**: The pipeline processes ONE stitched PDF (`_combine.pdf` or `_clean.pdf`). It splits into `page-1.pdf` → `page-N.pdf`, converts each to markdown, cleans them, then passes the list of `cleaned_files` to `generate_lecture_audio()`. There are no separate main/SI files at pipeline time — just one ordered list of page-level markdown files.

## Approach: Split + Contextual SI Enrichment

At lecture generation time, use `si_start_page` metadata to split the markdown file list into main paper pages vs SI pages. Generate the lecture from main paper content only. Pass full SI content as reference material so the LLM can pull from it when the main text references SI figures, methods, or tables. Constrain output proportion: ≥50% main paper, ≤50% embedded SI enrichment.

## Changes

### 1. Track SI boundary — write `{key}_meta.json`

**File:** `scripts/zotero_paper_import.py` (lines 73-83, 267-316)

- Add `si_start_page: int | None = None` to `PrepareResult`
- In `clean_pdf()`, after computing `kept_pages` from main ranges (line 287), set `si_start_page = kept_pages` when `si_pdf` is present
- Write `{citation_key}_meta.json` alongside the stitched PDF:

  ```json
  {"si_start_page": 4}
  ```

- **Manual path**: User creates the one-line JSON by hand (document this, no tooling needed)

### 2. Read `_meta.json` in pipeline, pass to lecture generation

**File:** `swanki/pipeline/pipeline.py`

- `citation_key` is already passed as a parameter to `process_full()` (line 153) and available throughout — use it to look up `{citation_key}_meta.json` in `pdf_path.parent`
- Read `si_start_page` from it (if present, else None)
- Pass to `generate_lecture_audio()` at line 2327 as a new kwarg

### 3. Split markdown file list in `generate_lecture_audio()`

**File:** `swanki/audio/lecture.py` (line 359)

- Add `si_start_page: int | None = None` parameter
- When set, split the single `markdown_files` list:
  - `main_files = markdown_files[:si_start_page]` — pages from the paper itself
  - `si_files = markdown_files[si_start_page:]` — supplementary pages
- Build `main_content` from `main_files` with image summaries (existing embedding logic, lines 394-425)
- Build `si_content` from `si_files` with remaining image summaries
- **Chunk only `main_content`** via `chunk_by_headers()` — lecture structure follows the paper
- **Global length target** based on `main_content` length only (not main+SI) — see step 7
- When `si_start_page` is None: behave exactly as today (graceful degradation)

### 4. Build SI index + extract relevant snippets per section

**File:** `swanki/audio/lecture.py` — new function `build_si_index()`

Parse SI content into named segments using patterns like:

- `Extended Data Fig. \d+` → content until next figure marker
- `Supplementary Fig. \d+` → content until next figure marker
- `Supplementary Table \d+` → content until next table marker
- `Figure S\d+` → content until next figure marker
- `## Methods`, `## Data`, etc. → content until next section header

Returns: `dict[str, str]` mapping item names to their content (caption, image summary, surrounding text).

**File:** `swanki/audio/lecture.py` — new function `extract_relevant_si()`

For each main paper section chunk:

1. Scan for SI reference patterns in the text (e.g., `(Extended Data Fig. 6)`, `Supplementary Fig. 12`)
2. Look up matched keys in the SI index
3. For each matched item, include the item content **plus a context radius** — surrounding text from the SI that gives the item more meaning (e.g., the paragraph before/after a figure caption, nearby methods context). Use a configurable `si_context_chars` (default ~500 chars before and after the matched segment)
4. Return the referenced SI snippets with context, concatenated

**File:** `swanki/audio/lecture.py` — `generate_and_validate_chunk()` (line 184)

- Add `si_reference_content: str | None = None` parameter
- When present, append to the user message:

  ```
  --- REFERENCED SUPPLEMENTARY MATERIAL ---
  The main text references the following supplementary items.
  Briefly weave their content into your explanation at the reference points.

  Example: if the text says "(Extended Data Fig. 6)", use the content below
  to enrich: "the authors show that the predicted expression..."

  Do NOT treat these as separate sections.
  {si_reference_content}
  ```

**Calling pattern in `generate_lecture_audio()`:**

```python
si_index = build_si_index(si_content)  # once
# per section:
relevant_si = extract_relevant_si(section_content, si_index)
generate_and_validate_chunk(..., si_reference_content=relevant_si)
```

This avoids reprocessing the entire SI for every section — only the referenced items are passed.

### 5. Output proportion constraint — heavily enforce at critique stage

**File:** `swanki/audio/lecture.py`

- In the per-section validation (`generate_and_validate_chunk`), add a **mandatory** check to the critique prompt:

  ```
  SI BALANCE CHECK (CRITICAL):
  The lecture MUST be primarily about the main paper content.
  At least 50% of the transcript must cover the main paper's own findings,
  arguments, and narrative. At most 50% should be SI-derived enrichment.

  If the section spends MORE time on SI/Extended Data details than the
  paper's own points, set done=False with feedback:
  "SI content dominates this section — reduce SI detail and focus on
  the main paper's argument."

  SI enrichment should be brief (1-3 sentences per reference), not
  exhaustive. The paper's narrative drives the lecture.
  ```

- Add `si_balance` as a field on `LectureTranscriptFeedback` to track this explicitly
- If SI balance fails, the section is regenerated with stricter guidance

### 6. SI-handling instructions in system prompt

**File:** `.swanki_config/prompts/default.yaml` — add under `audio:`

```yaml
lecture_si_instructions: |-
  SUPPLEMENTARY INFORMATION HANDLING:
  The input contains main paper content plus supplementary reference material.
  - Structure your lecture around the MAIN PAPER only
  - When the paper references SI (e.g., "Extended Data Fig. 6", "see Methods",
    "Supplementary Table S1"), briefly weave in the relevant SI detail at that
    point — use the figure caption, image summary, or surrounding context
  - Do NOT give SI its own section or say "moving on to supplementary info"
  - SI methods: mention briefly when explaining how a study was done
  - Keep SI enrichment ≤50% of the transcript — it supplements, not replaces
  - The lecture should flow as one coherent narrative about the paper's findings
```

**File:** `swanki/audio/lecture.py` — append to system prompt when `si_start_page` is set

### Open question: `chunk_by_headers()` regex brittleness

The current `chunk_by_headers()` regex (`^(#+)\s+([0-9.]+)`) only matches numbered headers like `## 1.2 Methods`. Many papers use unnumbered headers (`## Methods`, `## Data`). This means most content may end up in a single giant chunk.

**Options** (for follow-up or this PR):

- a) Broaden regex to also match unnumbered `## Headers`
- b) LLM-based TOC generation — one call to outline the document structure, then chunk by that outline
- c) Leave as-is — for short main papers (4 pages), single-pass mode kicks in anyway

Recommend (a) as a minimal fix in this PR, with (b) as a future enhancement.

### 7. Length control refactor — replace per-section budgets with global target + full-transcript enforcement

**File:** `swanki/audio/lecture.py`

**Current broken approach** (lines 512-583):

- Computes per-section word budgets proportional to section size
- Per-section critique enforces section-level budget (lines 225-246)
- Cumulative check (line 577) only logs a warning
- Result: papers with many small sections blow up because each section has a ~400-500 word minimum floor

**New approach**:

1. **Remove per-section word budgets entirely** — don't pass `section_budget_words` / `section_max_words` to `generate_and_validate_chunk()`
2. **Set a global target as guidance in the system prompt**, not per-section enforcement:

   ```
   TARGET LENGTH: Aim for roughly 40-60% of the source manuscript length.
   Some sections will need more space (rich concepts, analogies) and some
   less (straightforward results). Let the content drive the length.
   ```

3. **Enforce at the full-transcript refinement stage** (the `_refine_transcript()` loop that runs after all sections are generated):
   - Compute `transcript_words / source_words` ratio
   - If ratio > 0.7 (too long), add explicit length reduction feedback and regenerate
   - If ratio < 0.3 (too short), flag as potentially under-developed
4. **Remove the per-section LENGTH CHECK from the critique prompt** (lines 225-241) — keep all other quality checks (LaTeX, citations, lists, tone)
5. **Keep the cumulative tracking** for logging/visibility, but remove the warning-only behavior — instead, if cumulative words exceed tolerance after generating all sections, trigger the full-transcript refinement with length-specific feedback

**Why this is better**:

- Sections can breathe — a concept that needs a rich analogy gets more space
- Short sections that are straightforward don't get inflated to meet minimum conversational length
- Length is enforced where it matters: the final transcript as a whole
- The LLM can make trade-offs across the lecture (compress methods, expand key findings)

## Known Issues & Edge Cases

### Cut files ≠ SI boundary (manual path)

Examined `waldburgerActiveLearningEnables2025`: `_cut0` (9 pp, main text) + `_cut1` (6 pp) where `_cut1` contains BOTH main figures (Fig 1-5, pages 10-14) AND supplementary figures (Fig S1, page 15). The actual SI boundary is page 15, not page 10. **The plan handles this correctly** — the manual path requires the user to specify the correct `si_start_page` in `_meta.json`, not derive it from cut file page counts. Must document this clearly.

### SI content can be large — solved by indexed extraction

`avsecAdvancingRegulatoryVariant2026`: 14 pages of Extended Data/SI. The SI index + extraction approach (step 4) avoids reprocessing all 14 pages per section — only the specific referenced items are passed to each call.

### Image summary ordering is naturally correct

The current image embedding code (lecture.py lines 398-425) iterates `image_idx` sequentially across files. When we split `markdown_files` into main then SI, processing main files first naturally assigns the right image summaries to each group because `image_idx` carries forward.

### Existing papers lack `_meta.json`

All current Swanki_Data papers have no `_meta.json`. The system degrades gracefully (`si_start_page = None` → today's behavior). Users can retroactively create `_meta.json` for existing papers to enable SI-aware re-generation.

### Proportion constraint is soft guidance

The "≥50% main, ≤50% SI" rule is enforced via the critique prompt, not programmatically. The critique model may not perfectly distinguish main vs SI content in the output. This is acceptable — we want soft guidance, not strict enforcement.

## Verification

1. Run on a paper with SI (e.g., `ahlmann-eltze...`) — verify no false mid-lecture conclusions
2. Check that "Extended Data Fig. X" references get brief enrichment from SI content
3. Run on a paper without SI — verify identical behavior (regression)
4. Check transcript proportion: ≥50% covers main paper findings

## Key Files

| File                                  | Change                                                               |
|---------------------------------------|----------------------------------------------------------------------|
| `scripts/zotero_paper_import.py`      | `PrepareResult.si_start_page`, write `_meta.json`                    |
| `swanki/pipeline/pipeline.py`         | Read `_meta.json`, pass `si_start_page` to lecture gen               |
| `swanki/audio/lecture.py`             | SI splitting + index, length control refactor, proportion constraint |
| `swanki/models/cards.py`              | Add `si_balance` field to `LectureTranscriptFeedback`                |
| `.swanki_config/prompts/default.yaml` | `lecture_si_instructions` prompt, updated length guidance            |
