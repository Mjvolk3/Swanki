---
id: 4b9le8ji8j71cx9b61516zp
title: '01'
desc: ''
updated: 1780361428222
created: 1780361428222
---

## Problem

`_BACK_MATTER = re.compile(r"\b(Index|Glossary|Bibliography|References)\b", re.IGNORECASE)` (`swanki/pipeline/section_classifier.py:62-64`) matches those words ANYWHERE in prose. On Hamming ch04 it matched "index" in "index registers" (page-4, mid-chapter), flipped the page to `back_matter` at confidence 1.0, and because `current_kind` is sticky (`_heading_classify` loop, no reset until a new anchor), pages 4-8 all inherited `back_matter`. Result: 6 of 9 pages dropped from `main_content` -> only 2 segments -> 4 cards (old ch04 had 14). `filter_files_by_kind("main_content")` (`pipeline.py:373`) feeds card-gen + audio; `back_matter`/`front_matter` pages are silently DROPPED. ch04 is the ONLY chapter hit; the other 9 are 100% main_content.

Card count = `num_segments * (cards_per_segment + cloze_per_segment) + images*cards_per_image` (`estimate_card_count`, `pipeline.py:1839`); segments come only from `main_content` pages. So the low count is upstream page-classification loss, not chunking.

## Root-cause analysis (3 scouts confirmed)

- Trigger is the only defect. The cascade itself is CORRECT and load-bearing: real multi-page back-matter (paper References span the last 2-3 pages; Alcamo answer keys span ~12 pages) relies on stickiness, and `_pair_answer_keys` (`section_classifier.py:221-259`) re-classifies multi-page `back_matter` answer blocks -> `review_exercises`. So DO NOT de-stickify (would split legitimate runs / break answer-key pairing).
- The loop already exposes `i` and `len(texts)` -> positional guard is trivial. `front_matter` already has a positional guard (`i < 5`, line ~171); `back_matter` has none.
- Real back-matter in this corpus is always a promoted markdown heading: `## References`, `# Bibliography`, `## REFERENCES`, `## Bibliography and Notes`. Sampled 12 docs in `/scratch/.../Swanki_Data`: References/Bibliography land in the last ~20% of pages (>=80th percentile) in 11/12; the 1 mid-doc hit was prose ("original references" in a table footnote) -> exactly what anchoring kills.
- `confidence` is informational only (sole consumer: LLM-fallback trigger when overall < `section_classifier_min_confidence`, default 0.7). Not used in routing.
- Glossary mode does NOT call `classify_sections` (zero impact). solution_manual relies on `back_matter` + cascade + `_pair_answer_keys` (must stay intact).

## Fix (layered, trigger-only)

Edit `swanki/pipeline/section_classifier.py`.

1. Anchor `_BACK_MATTER` to a markdown heading (kills prose matches):
   ```python
   _BACK_MATTER = re.compile(
       r"^#{1,6}\s+(Index|Glossary|Bibliography|References)\b",
       re.IGNORECASE | re.MULTILINE,
   )
   ```
   Rejects "index registers", "original references" (not heading-anchored). Catches "## References", "# Bibliography", "## Bibliography and Notes". A real un-promoted back-matter line now falls to main_content (benign: a few extra cards) instead of dropping content (malignant) — and the LLM fallback still covers it.

2. Positional guard on the back_matter flip. Before the loop: `total = len(texts)`. In the back_matter branch (lines ~158-166) add `and i >= int(total * 0.8)` so only the last ~20% of pages may start a back_matter run. ch04 page-3 (i=3 of 9 = 0.33) is rejected; paper References (last page) still caught. For very short docs `int(total*0.8)` keeps the last page eligible.

3. Anchor `_FRONT_MATTER` the same way and keep its existing positional guard:
   ```python
   _FRONT_MATTER = re.compile(
       r"^#{1,6}\s+(Preface|Table of Contents|Copyright|Dedication)\b",
       re.IGNORECASE | re.MULTILINE,
   )
   ```
   Keep `i < 5` (works; out of scope to make it %-based). Anchoring removes the symmetric prose false-positive ("a preface to...").

4. Leave stickiness, confidence, `_pair_answer_keys`, `_REVIEW_*`, `_THEORY_HEADING`, `_CHAPTER_HEADER`, the LLM fallback, and all configs UNCHANGED. The two guards above fix the trigger; the existing cascade then behaves correctly for both false (now never starts mid-doc) and true (heading in tail region -> cascades through the real multi-page back-matter) cases.

## Tests — `tests/test_section_classifier.py`

Add `_heading_classify` cases (write temp `.md` via `tmp_path`, one file per page; import `_heading_classify`):

- REGRESSION (ch04): a mid-doc page (e.g. page idx 3 of 9) whose prose contains "I needed index registers" stays `main_content`; following pages stay `main_content`. (Fails before fix.)
- Real back-matter: a 5-page doc whose LAST page is `## References\n...` -> that page `back_matter`.
- Positional guard: a `## References` heading on page idx 1 of 9 (mid-doc) -> NOT `back_matter` (stays main_content). Guards against a real-but-misplaced heading.
- Multi-page back-matter still contiguous: last 2 pages, first is `## References`, second is continuation prose -> both `back_matter` (proves cascade preserved for true tail back-matter).
- front_matter: prose "...a preface to the topic..." on page 0 (no heading) -> main_content; `## Preface` on page 0 -> front_matter.

Keep existing `join_pages` tests untouched. Match the file's inline/parametric style.

## Verification

1. `pytest tests/test_section_classifier.py -q` green.
2. Re-run classification on ch04's existing clean-md-singles and assert all `main_content`:
   ```python
   from swanki.pipeline.section_classifier import classify_sections
   from pathlib import Path
   d = Path("/scratch/projects/torchcell-scratch/Swanki_Data/hammingArtDoingScience2020/hammingArtDoingScience2020_CH04_history-of-computers-software/clean-md-singles")
   files = sorted(d.glob("page-*.md"), key=lambda p:int(p.stem.split('-')[1]))
   r = classify_sections(files, {})
   assert all(l.kind=="main_content" for l in r.page_labels)
   ```
3. Sanity: re-run classify on a real paper with a tail References page (e.g. `campagneClinicalPharmacokineticsPharmacodynamics2021`) -> last page still `back_matter`.

## Module note

Append a `## 2026.06.01 - Back-matter false-positive: anchor cues + positional guard` section to `notes/swanki.pipeline.section_classifier.md`: the "index registers" incident, why trigger-only (not de-sticky, to preserve answer-key cohesion), the two guards, and the benign-vs-malignant failure trade.

## Post-merge: re-gen ch04 (delivery, after PR merges to main)

Run under `conda activate swanki` from repo root:
```bash
swanki pdf_path=/scratch/hammingArtDoingScience2020/ch04_clean.pdf \
  citation_key=hammingArtDoingScience2020 \
  content_key=hammingArtDoingScience2020_CH04_history-of-computers-software \
  +output_dir=hammingArtDoingScience2020/hammingArtDoingScience2020_CH04_history-of-computers-software \
  audio=all anki=default zotero=sync ocr=mineru \
  models=fish_speech_hamming prompts=book_voice +author="Richard Hamming" \
  pipeline.processing.confirm_before_generation=false
```
Expect ~14 cards (output dir auto-increments; new dir then becomes canonical). Verify apkg media>0; delete the live 4-card `hammingArtDoingScience2020_CH04_history-of-computers-software` Anki deck via AnkiConnect, importPackage the new apkg, one AnkiWeb sync. Zotero re-sync is automatic (`zotero=sync`); prune handles the prior CH04 zip.

## Scope / out-of-scope

In: the two regex anchors + the back_matter positional guard + tests + module note + ch04 re-gen.
Out: de-stickying, confidence-model changes, a `document_type` config flag, front_matter %-positional rework, the systemic `_citation.mp3` token-limit issue (tracked separately), `_prune` `everything()` hardening.
