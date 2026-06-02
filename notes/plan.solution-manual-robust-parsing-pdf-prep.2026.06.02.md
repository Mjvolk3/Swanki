---
id: 3xwyfizq4n0u4lbqkk7hg0p
title: '02'
desc: ''
updated: 1780434979065
created: 1780434979065
---

## Context

Schaum's `solution_manual` problem-set generation broke for the entire June queue: all 5 Alcamo (`alcamoSchaumsOutlineMicrobiology2010`) chapters fail with `CoverageError`. The code did not change. The OCR backend did. May runs used Mathpix, which emits back-of-book answer-key section titles as H2 (`## Chapter 1`, `## Matching`). June runs use `ocr=mineru`, which emits the same titles as H1 (`# Chapter 1`, `# Matching`). The back-of-book parser in `swanki/pipeline/problem_set.py` hard-codes `^##\s+` in three places, so under MinerU `_partition_back_of_book` matches nothing and returns `{}`. With no back-of-book bodies, the Matching and True/False forward sections have no answer to pair against, the unpaired solutions accumulate (observed as duplicate `TF-CH1-1` entries), and `audit_coverage` (zero-tolerance) hard-fails. This is the proven root cause: the section body itself (`1. c 2. c ...`) is plain text and OCR-agnostic *once extracted* — only the header anchors differ. MC/Completion appeared to partially survive because some flow inline through other stages, but they share the one back-of-book path.

The user asked for two things beyond the bug: make this parsing **robust and general** (OCR-agnostic; tolerant of the same-named section appearing twice in one chapter, e.g. Ch3/Ch5 each have two Matching sets numbered 1-10; tolerant of an answer body spilling across a page break), and **move the PDF-prep step** (chapter chop + answer-key concat) out of the ad-hoc `scripts/schaum_chapter_pack.py` and into the `swanki` library so it is a first-class, testable, CI-covered component.

## Relevant Files

| Path | Action | Purpose | Stance |
| --- | --- | --- | --- |
| `swanki/pipeline/problem_set.py` | MODIFY | Loosen 3 header regexes; list-valued partition; all-occurrence forward enumeration; k-th pairing; occurrence-indexed IDs | Provisional / in-flux (this is the hot file) |
| `swanki/models/problem_set.py` | MODIFY | Extend `_PROBLEM_TAG_RE` (L171-173) to tolerate optional middle occurrence segment | Stable — change is additive |
| `swanki/utils/formatting.py` | MODIFY | Update `_PROBLEM_LABEL_LONG`/`_SHORT` (L459-464) capture groups in lockstep with new ID shape | Stable — change is additive |
| `swanki/pdf_prep.py` | NEW | Chapter chop + (possibly multiple) answer-key range concat via pure-Python `pypdf` | New module, top-level sibling to `swanki/cut.py` |
| `swanki/cut.py` | MODIFY | Migrate `PyPDF2 import` (L16) to `pypdf`; reference for existing chop idiom | Reference / minimal touch |
| `scripts/schaum_chapter_pack.py` | MODIFY -> shim | Reduce to thin back-compat wrapper importing `swanki.pdf_prep` | Keep existing `.sh`/queue invocations working |
| `pyproject.toml` | MODIFY | Replace bare `"PyPDF2"` (L26) and mypy override (L140) with `pypdf>=4` | Stable |
| `tests/test_problem_set.py` | MODIFY | Partition/pairing tests on MinerU `#` + Mathpix `##` fixtures, two-Matching, page-spill | — |
| `tests/test_problem_set_models.py` | MODIFY | `ProblemTag` round-trip for bare and occurrence IDs | — |
| `tests/fixtures/problem_set/` | NEW fixtures | MinerU `#` fixture, two-Matching fixture, page-spill fixture (existing fixtures are all Mathpix `##`) | — |
| `notes/swanki.pipeline.problem_set.md` | MODIFY | Append dated rationale section | Docs |
| `notes/swanki.pdf_prep.md` | NEW | Module note for new `pdf_prep` | Docs |
| `swanki/ocr/mineru.py` | REFERENCE | Emits answer-key titles as H1 `#` — the trigger | Read-only |
| `swanki/ocr/mathpix.py` | REFERENCE | Emits the same titles as H2 `##` — the May-era assumption | Read-only |

## Key Design Decisions

1. **Fix the 3 local regexes, do NOT normalize headers in `markdown_cleaner`.** The bug is a local assumption in one parser. Header-level normalization in the shared cleaner would perturb every other consumer of the cleaned markdown (card text, audio, glossary) for a problem that lives entirely in the back-of-book partition. Local fix, local blast radius.

2. **Accept `^#{1,3}\s+`, not bare text and not optional-hash.** Mathpix gives `##`, MinerU gives `#`, and H3 is cheap defensive headroom. We deliberately require a *real* header anchor: the section words ("Matching", "Completion", "True/False") also appear as in-chapter dividers (`Multiple Choice.` with a period, bare text) and inside answer-body prose. Bare-text or `#{0,3}` matching would collide with those and corrupt span boundaries. This mirrors the already-shipped `_FORWARD_CHAPTER_HEADER` (L169, `#{1,2}`). The in-chapter dividers (`^Multiple Choice\.` etc.) are bare-text and already OCR-agnostic — untouched.

3. **Occurrence-indexed IDs, but suppress the index when a type appears once.** A chapter with two Matching sets needs distinct IDs while preserving each set's printed item numbers (both run 1-10). Scheme: `MAT-CH3-2-7` = type-chapter-occurrence-item. But when a section type appears exactly once in a chapter (the common case), omit the occurrence segment entirely so the ID stays `MAT-CH3-7` — **zero regression** for every chapter that already works. Rejected: a continuously-incrementing item counter across both sets (`MAT-CH3-11..20`), which destroys the book's printed numbering and confuses the visible card label.

4. **PDF prep in pure-Python `pypdf`, not a `qpdf`/`pdfunite` shell-out.** CI has `ffmpeg` but does NOT have `qpdf` or `pdfunite`. A subprocess-based packer would pass locally and fail CI. `pypdf` is the maintained successor to the deprecated `PyPDF2` already in `pyproject` (L26). Floor at `pypdf>=4`; do not rely on version-specific API beyond the stable `PdfReader`/`PdfWriter`.

5. **Module home `swanki/pdf_prep.py`** — top-level sibling to the existing `swanki/cut.py` (which already does PDF page surgery), not buried under `pipeline/`. PDF prep is a pre-pipeline input-preparation concern, parallel to `cut`.

6. **Migrate `cut.py` to `pypdf`, but leave `scripts/zotero_paper_import.py` alone.** Once `PyPDF2` is dropped from deps, every importer must move. `cut.py` is small and in-scope. `zotero_paper_import.py` is out of scope and would widen the blast radius into the Zotero import path (open PR `#25` territory) for no benefit to this task.

7. **One PR, three sequenced internal stages, in a worktree off `origin/main`.** Stage 1 (header fix) is critical and independently correct — it must be tested on its own MinerU fixture *before* the riskier ID work (Stages 2-3) is layered on, so the OCR fix is not entangled with ID-scheme churn. All three land together because they form the single "robust + general" deliverable the user requested.

## Approach

### Stage 1 — OCR header fix (critical, ship-alone-correct)

Loosen exactly three `##`-hardcoded regexes to `^#{1,3}\s+`:
- `_BACK_CHAPTER_HEADER` (L161): `^##\s+Chapter\s+(\d+)\s*$` -> `^#{1,3}\s+Chapter\s+(\d+)\s*$`
- `_BACK_SECTION_HEADER` (L162-165): `^##\s+(Multiple Choice|Matching|True/False|Completion)\s*$` -> `^#{1,3}\s+(...)\s*$`
- `column_b_re` (L373): `^##\s+Column B\s*$` -> `^#{1,3}\s+Column B\s*$`

This single change restores `_partition_back_of_book` for **all** subtypes (MC, Matching, True/False, Completion) under MinerU, because the bodies were always OCR-agnostic — only the anchors were not. Verify no MC/Completion regression on the existing Mathpix fixtures (they must still match under `#{1,3}`).

### Stage 2 — repeated same-named sections

Today `_partition_back_of_book` overwrites on collision (`sections[section_name] = body`, L418), so a chapter's second Matching set silently clobbers the first. Make the partition list-valued:

```python
# shape: {chapter_num: {section_name: [body_0, body_1, ...]}}
partition[ch]["Matching"] = ["1. c 2. a ...", "1. b 2. d ..."]
```

Make the forward enumerators all-occurrence-aware. Replace the first-match-only `_section_span` (L206) with an all-spans walker that yields every in-chapter occurrence of a section divider; the `_enumerate_*` functions (L223/248/288/318) iterate those spans. Pair the k-th forward section with the k-th back-of-book body. A count mismatch (forward sees 2 Matching, back sees 1) is **not** a silent drop — it surfaces through `audit_coverage` (L977) as a coverage failure naming the offending occurrence index.

ID rule, applied at emit time:

```python
# n = total occurrences of this (type, chapter) in the forward pass
problem_id = f"{type}-CH{ch}-{item}" if n == 1 else f"{type}-CH{ch}-{occ}-{item}"
```

So single-section chapters keep `MAT-CH3-7` (no regression); a chapter with two Matching sets gets `MAT-CH3-1-7` and `MAT-CH3-2-7`. Extend `_PROBLEM_TAG_RE` (models L171-173) from `[A-Z]+(?:-CH\d+)?-\d+` to tolerate an optional middle occurrence segment (e.g. `[A-Z]+(?:-CH\d+)?(?:-\d+)?-\d+`), and update the humanizer `_PROBLEM_LABEL_LONG`/`_SHORT` (formatting L459-464) capture groups in lockstep so the long-form label still expands. The visible card label disambiguates the second set (e.g. "Matching (set 2) 7:") while preserving the printed item number 7.

### Stage 3 — PDF prep into the lib

New `swanki/pdf_prep.py` exposing a chop-plus-concat API: given a source PDF, a chapter's forward page range, and **one or more** answer-key page ranges (answer keys spill across pages and may be non-contiguous), produce one packed PDF via `pypdf.PdfReader`/`PdfWriter` — no subprocess. Multiple answer-key ranges are appended in order after the chapter pages. Migrate `swanki/cut.py` import (L16) from `PyPDF2` to `pypdf` (drop-in `PdfReader`/`PdfWriter`). Replace `"PyPDF2"` with `"pypdf>=4"` in `pyproject.toml` (L26) and the mypy module override (L140). Reduce `scripts/schaum_chapter_pack.py` to a thin shim that imports `swanki.pdf_prep` and forwards its CLI args, so existing `.sh` and queue invocations keep working unchanged.

## Gotchas

1. **The third `##` is easy to miss.** `column_b_re` (L373) is defined inline inside the Matching-options helper, far from the two module-level header regexes (L161-165). Forgetting it means Matching answer *options* (Column B) still fail to parse under MinerU even after the obvious two are fixed.

2. **(O2) MinerU running-header chapter duplication.** MinerU may stamp `# Chapter N` as a running header atop *every* page in a chapter's answer region. With `#{1,3}`, `_BACK_CHAPTER_HEADER` then matches the same chapter many times, creating spurious empty chapter spans. Dedupe/merge consecutive same-number chapter matches into one span before partitioning.

3. **(O1) Page-spill answer body.** A section's answer body can be split mid-run by an injected page-number token or running-header line. The answer-body tokenizer must tolerate/strip standalone numeric lines and header lines *inside* a section body rather than assuming a contiguous clean run.

4. **CI has no `qpdf`/`pdfunite`.** The PDF packer MUST be pure-Python `pypdf`. A subprocess approach passes locally and silently fails CI. This is the single hardest constraint on Stage 3.

5. **MC/Completion regression risk.** They share the one back-of-book path. After loosening the regexes, explicitly re-verify MC and Completion still pair on the Mathpix fixtures — the fix must be a superset, not a sideways move.

6. **`ProblemTag` and humanizer must change in lockstep with IDs.** If `_PROBLEM_TAG_RE` (models L171) or `_PROBLEM_LABEL_LONG/_SHORT` (formatting L459-464) lag the new occurrence-segment ID shape, tags fail to round-trip and labels stop expanding. Change all three together or none.

7. **Concurrency on `problem_set.py`.** Main checkout is on `chore/makefile-queue-targets` in another session; PR `#25` (Zotero) does not touch `problem_set.py`; classifier PR `#27` is merged. Low conflict risk, but implement in an isolated worktree off `origin/main` and rebase at the end.

8. **`allow_unsolved` is the test escape hatch.** `audit_coverage` (L977) is zero-tolerance three-part hard-fail. `sm_config.allow_unsolved` (default `False`) lets unit tests and iterative runs exercise the parser without a full pipeline pairing pass — use it while iterating, not in shipped config.

9. **Repeated sections raise card count, raising correctness-gate cost.** The per-card correctness gate is now default-on; two Matching sets mean more cards mean more gate calls. Expected, not a bug — note it so a cost spike is not mistaken for a regression.

## Verification

- Unit: `_partition_back_of_book` returns populated dicts on a **MinerU `#`** fixture AND the existing **Mathpix `##`** fixtures (same parsed bodies from both).
- Unit: two-Matching fixture — both sets enumerate forward, partition holds a 2-element list, k-th pairing matches k-th body, IDs are `MAT-CHn-1-*` / `MAT-CHn-2-*`.
- Unit: page-spill fixture — answer body split by a stray numeric/header line still tokenizes to the full run.
- Unit: `ProblemTag` round-trips both bare `MAT-CH3-7` and occurrence `MAT-CH3-2-7`.
- Unit: humanizer expands the long label for both bare and occurrence IDs.
- Regression: MC and Completion still pair on the Mathpix fixtures (no sideways break).
- Unit: `pdf_prep` chop+concat round-trip — output page count equals chapter pages plus all answer-key ranges, including multiple/non-contiguous ranges.
- End-to-end: Alcamo CH01 (single-section) and CH03 (two-Matching + spill) pass `audit_coverage` with the existing packed PDFs under `ocr=mineru` (use `allow_unsolved` while iterating, then full pass).
- `ruff` + `mypy` clean on changed files; new tests green.
- CI stays green with no new system deps (no `qpdf`/`pdfunite`; `pypdf` is pip-only).

Real MinerU `#` source to build the fixture from:
`/scratch/projects/torchcell-scratch/Swanki_Data/alcamoSchaumsOutlineMicrobiology2010/alcamoSchaumsOutlineMicrobiology2010_CH01_introduction-to-microbiology/clean-md-singles/page-12.md` (and the CH03 dir for two-Matching + spill).

## Open Questions

- **(O1) Exact page-spill artifact.** Confirm from a real MinerU dump whether the splitter is a bare page number, a running header, or both. Default behavior absent confirmation: strip standalone numeric *and* header-only lines inside a section body.
- **(O2) Running-header chapter dedup approach.** Default: merge consecutive same-number `_BACK_CHAPTER_HEADER` matches into one span. Confirm MinerU actually re-stamps the header per page before adding complexity.
- **Visible label format for a 2nd same-type section.** Need a human-friendly disambiguator (e.g. "Matching (set 2) 7:" vs "Matching 2.7:"). Pick one once a two-Matching card is rendered and eyeballed.
