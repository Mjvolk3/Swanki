---
id: 6h3qqlh4dvtxn5enq9jsx7yj
title: Reading Table Figure Landmarks
desc: ''
updated: 1780274093769
created: 1780274093769
---

## Context

Tables and figures in the audio are inconsistent and partly broken. The user wants both turned into **navigational landmarks**: a short spoken cue — `Figure: <desc>` / `Table: <desc>` (NO number) — that tells the listener "look now, here's roughly what it is, you won't hear it again." This is a *reading*, so it stays light: never voice table cells, never read numeric grids row by row.

Decisions already locked by the user (option A):

- Caption present -> read the FULL caption verbatim. Same rule for figures and tables.
- No caption -> a generated description, <=1 sentence. Same for figures and tables.
- Read INLINE in page order (state it where it appears; do not defer to section/page end).
- Set off by REAL silence, not Fish `[pause]` — reuse the existing `---SECTION_BREAK---` mechanism that already yields deterministic `section_pause_ms` silence (3000ms fish / 2000ms eleven).
- Tables get the same treatment as figures, including a new "table-summaries" step mirroring image-summaries.

Today's reality (verified in code): figures become `![alt](url)` with the caption **truncated to 100 chars** (`markdown_cleaner.py:288-291`); wrapped `\begin{table}` blocks are **deleted with no extraction** (`table_blocks` pattern, applied L330); bare `\begin{tabular}` blocks (what the Hamming book uses) are matched by **nothing** and leak into `clean-md-singles` as raw rows, which is how the Ch1 numeric "doubling" grid got voiced as "2 17 3 27...". The old reading `system_prompt` "Rule 3" (`reading.py:218-226`) that says 'Figure N'/'Table N' must change to the no-number form (and confirm whether the reading transcript path even still uses it).

## Key architecture facts (verified, not assumed)

- **Reading IS LLM-processed.** `generate_reading_audio` Pass 1 calls `humanize_latex(full_content, model)` which is "per-chunk LLM passes" (`_common.py:12` docstring). Its contract: "DO NOT change any other text. Preserve prose exactly; only transform math/units/symbols and linearize tables." So short caption prose survives, and any math inside a caption still gets humanized. Pass 2 is the deterministic scrubber chain: `clean_markdown_for_tts` -> `strip_chapter_filename_slug` -> acronym/verbalize/pronunciation -> `add_tts_pauses` -> `split_transcript_by_sections` -> `combine_audio_with_section_pauses`.
- **`---SECTION_BREAK---` survives the whole chain.** `clean_markdown_for_tts` (`_common.py:32-53`) does not touch it; `expand_acronyms_for_tts` masks it (`_common.py:462-464`); `add_tts_pauses` ignores it; `split_transcript_by_sections` (`_common.py:1140`) splits on it; `combine_audio_with_section_pauses` (`_common.py:1376`) inserts real `AudioSegment.silent(section_pause_ms)`. A literal SECTION_BREAK block written into `clean-md-singles` therefore becomes real silence deterministically.
- **`clean_markdown_for_tts` turns `![alt](url)` into just `alt`** (markdown-link strip), dropping the URL. So whatever alt text we leave in the image syntax IS spoken — this is why we must NOT leave the caption in the image alt (double-read); caption goes only in the landmark, and the image becomes `![](url)` (empty alt).
- **Lecture path differs.** `generate_lecture_audio` also runs `humanize_latex`, but figures are handled by `_embed_images` (`lecture.py:533-562`) which textually rewrites `![alt](url)` -> "Looking at {alt}, we can see {summary}" using passed-in `image_summaries` strings. Tables are absent (deleted). This prose form CONFLICTS with the new landmark and must be retired.
- **Pipeline stage order** (`pipeline.py`): markdown_cleaning (`clean_markdown` L268) -> image_processing (`process_images` L272) -> summary_generation (L276) -> section_classification (L296) -> cards -> output -> audio (reading ~L2200 from `main_content_text` via `merge_main_content`/`join_pages`; lecture ~L2247 passes `image_summary_strings`).
- **`ImageSummary`** is pydantic (`models/document.py`); `ImageInfo` inside `image_processor.py` is a plain dict. Image summaries are up to 300 words (multi-sentence) — too long for a <=1-sentence figure landmark, so clamp to first sentence.
- **Hamming Ch1 fixtures** (`/scratch/projects/torchcell-scratch/Swanki_Data/hammingArtDoingScience2020/hammingArtDoingScience2020_01_orientation_12/clean-md-singles/`): `page-4.md` (numeric doubling grid) and `page-8.md` (computer-advantages list) are both bare `\begin{tabular}` with NO `\caption` -> both take the summary path -> `Table: <1-sentence>`.

## Approach

Deterministic landmark injection at the markdown layer (option A), shared by reading and lecture because both read from `clean-md-singles`. The body is removed at clean time so cells never reach any downstream stage. Caption-bearing items are fully deterministic with no LLM; caption-less items get a <=1-sentence summary from a new table-summaries step (tables) or a clamped image summary (figures).

The canonical landmark block written into `clean-md-singles` (page order preserved, replacing the original block in place):

```
---SECTION_BREAK---
Figure: <full caption verbatim | generated <=1-sentence>
---SECTION_BREAK---
```

(`Table:` identical.) Reused SECTION_BREAK = free real-silence brackets, no new marker vocabulary.

### Two-pass, LLM-free cleaner + a fill step (keeps ordering simple)

`markdown_cleaner` runs before any summary exists and must stay LLM-free. So:

1. **`markdown_cleaner`** detects each figure/table in page order. Caption present -> write the FINAL landmark with the verbatim caption. No caption -> write a landmark with a PLACEHOLDER sentinel `\x00LMK:<kind>:<page-stem>:<idx>\x00` (kind = `figure`/`table`) and stash the raw block body to `table-summaries/<page-stem>_<idx>.source.txt` so the summarizer has the source. Body is removed from `clean-md-singles` either way.
2. **`table_processor`** (NEW, after image_processing) scans `clean-md-singles` for `table` placeholders, reads the matching `.source.txt`, calls a TEXT LLM for a <=1-sentence "what this table shows" (never read cells), writes `table-summaries/<page-stem>_<idx>.md`, and replaces the placeholder in `clean-md-singles` with the sentence. Idempotent: skip if the `.md` already exists.
3. **Figure placeholders** (caption-less figures) are filled from the EXISTING image summary (`image-summaries/`), clamped to its first sentence. No new vision call. (A dedicated short-caption field is a follow-up; clamping is the v1.)

Placeholder choice (`\x00...\x00`): NUL-delimited so it cannot collide with prose, mirrors `_SECTION_BREAK_TTS_MASK`'s opaque-mask pattern, and is trivially regex-matchable for the fill step. Any unfilled placeholder (LLM failure) is stripped to empty by a final safety pass so it can never be voiced.

## Relevant files

| File | Action | Notes |
| --- | --- | --- |
| `swanki/processing/markdown_cleaner.py` | MODIFY | New `_emit_landmark` helper; figure block -> landmark (drop 100-char truncation; full caption; emit `![](url)` empty-alt to avoid double-read); add bare `\begin{tabular}` matching (incl. optional preceding `\caption`); change wrapped `\begin{table}` from delete to extract+landmark; stash caption-less block bodies. |
| `swanki/processing/table_processor.py` | NEW | Mirror `image_processor`: scan clean-md-singles, text-LLM summary for caption-less tables, write `table-summaries/`, fill placeholders. Returns `list[TableSummary]`. |
| `swanki/models/document.py` | MODIFY | New `TableSummary` pydantic model. |
| `swanki/pipeline/pipeline.py` | MODIFY | Call `table_processor` after `process_images` (~L272-276); thread results; figure-placeholder fill from image summaries. |
| `swanki/audio/lecture.py` | MODIFY | Retire the "Looking at {alt}..." prose in `_embed_images`; an `![](url)` now drops to nothing (URL only); landmarks flow through `humanize_latex` like reading; tables no longer deleted. |
| `swanki/audio/reading.py` | MODIFY | Update/remove the "Rule 3" `system_prompt` text (it says 'Figure N'); change to `Figure:`/`Table:` no-number form. Confirm transcript path needs no logic change. |
| `swanki/conf/prompts/default.yaml`, `book_voice.yaml` | MODIFY | Update "Figure N"/"Table N" reference guidance to `Figure:`/`Table:`; reconcile "NEVER use LaTeX tabular" lines with the landmark. |
| `swanki/pipeline/section_classifier.py` | VERIFY | `join_pages`: a page ending in `---SECTION_BREAK---` ends in `-` so it glues with a space; harmless since the split is on the literal marker. Add a test; only touch `_SENTENCE_TERMINAL_RE` if a real case breaks. |
| `tests/test_markdown_cleaner.py` | MODIFY/NEW | figure+table -> landmark; body removed; caption verbatim; bare tabular caught; Hamming page-4/page-8 -> placeholder+`Table:`. |
| `tests/test_table_processor.py` | NEW | placeholder fill with mocked text LLM; idempotence; <=1 sentence; never emits cells. |
| `tests/test_audio_common.py` | MODIFY | landmark block survives clean_markdown_for_tts + add_tts_pauses; splits into its own section. |

## Key design decisions

1. **Inject at markdown layer (option A), reuse SECTION_BREAK.** Rejected (B) prompt-based: the reading transcript path no longer obeys that prompt and the user wants ~100% determinism. Rejected (C) post-LLM token converter: unnecessary since SECTION_BREAK already survives and yields silence; a second marker vocabulary adds nothing.
2. **Let captions flow through `humanize_latex` rather than masking them.** `humanize_latex`'s contract preserves prose verbatim and only transforms math — which is what we want, because a caption can contain math (`Figure: plot of $\alpha$ vs $\beta$`). Full masking would leave that math raw. Rejected: masking landmark interiors (breaks math-in-caption; over-engineered).
3. **Cleaner stays LLM-free; a separate fill step does summaries.** Cleaner runs before summaries can exist. Placeholder + stashed source body decouples them and makes the summary step idempotent/cacheable, exactly like image-summaries.
4. **Figure landmark for caption-less figures reuses the existing image summary (clamped to 1 sentence).** No second vision call. Tables get a new TEXT summarizer (table body is text; vision is wasteful).
5. **Retire lecture's "Looking at {alt}" prose.** Reading and lecture must emit the identical landmark; the prose form conflicts and tables had no path at all. Removing it makes both consistent for free since both read clean-md-singles.
6. **Body removed at clean time for all three forms** (`\begin{table}`, bare `\begin{tabular}`, and — if confirmed present — MinerU pipe-table body). No cells survive to clean-md-singles, so none reach TTS or cards.

## TableSummary model

```python
class TableSummary(BaseModel):
    model_config = ConfigDict(extra="forbid")
    page_stem: str                 # e.g. "page-4", for keying back to occurrence
    occurrence_idx: int            # Nth table on the page (0-based), page order
    caption: str | None = None     # verbatim caption when present
    summary: str | None = None     # generated <=1 sentence; None when caption present
    source_block: str = ""         # raw matched block (audit / idempotent re-fill)

    @field_validator("summary")
    @classmethod
    def _one_sentence(cls, v: str | None) -> str | None:
        if v is None:
            return v
        v = v.strip().split("\n")[0]
        if len(v.split()) > 30:
            raise ValueError(f"table summary too long: {len(v.split())} words")
        return v
```

## Gotchas

1. **Double-read of figure caption.** `clean_markdown_for_tts` speaks the alt of `![alt](url)`. The cleaner MUST emit `![](url)` (empty alt) when it also emits a Figure landmark, so the caption is voiced exactly once (from the landmark). Verify `image_processor._extract_images_from_markdown` and lecture `_embed_images` tolerate empty alt (they do; alt is optional).
2. **`join_pages` interaction (likely no-op — VERIFY only).** A page ending in `---SECTION_BREAK---` ends in `-`, so `_SENTENCE_TERMINAL_RE` does NOT match -> `join_pages` glues the next page with a space, yielding `---SECTION_BREAK--- nextword`. HARMLESS: `split_transcript_by_sections` splits on the literal marker regardless of adjacent spaces. So no code change expected; just add a unit test asserting a landmark-terminated page still splits into its own section.
3. **Adjacent landmarks collapse.** Figure immediately followed by a table yields stacked SECTION_BREAKs -> one silence. Acceptable; `split_transcript_by_sections` drops empty sections.
4. **Unfilled placeholder safety.** If the table summary LLM fails, a NUL placeholder must never reach TTS. Final scrubber/cleaner pass strips any residual `\x00LMK:...\x00` to empty. Add a test.
5. **MinerU pipe tables (HIGH uncertainty — VERIFY DURING IMPL).** Verify whether MinerU output reaches clean-md-singles as `^|...|$` pipe tables (vs latex). If present, add a pipe-table detector (run of pipe rows, optional preceding caption line) -> landmark. If NOT observed in practice, defer pipe-table handling to a follow-up and handle only latex `table`/`tabular` in v1. Decide by inspecting a real MinerU `clean-md-singles` sample during implementation.
6. **Order: cleaner before table_processor before audio.** table_processor must run after `clean_markdown` and before audio generation; figure-placeholder fill must run after `process_images`. Wire in `pipeline.py` accordingly.
7. **occurrence_idx assignment.** Assign indices in a single page-order pass over BOTH figures and tables combined? No — key by kind separately (`figure` idx and `table` idx independent), since figure fill pulls from image-summaries (already per-image, in page order) and table fill pulls from table-summaries. Confirm image_processor emits image summaries in page+occurrence order so the figure-placeholder idx maps 1:1.

## Verification

- `~/miniconda3/envs/swanki/bin/python -m pytest tests/test_markdown_cleaner.py tests/test_table_processor.py tests/test_audio_common.py -q` (and `ruff`/`mypy` per project skills). Mock the text LLM; NO network, NO Fish.
- Manual transcript-level check on Hamming Ch1 `_12`: run the cleaner over `clean-md-singles/page-4.md` and `page-8.md`, confirm each `\begin{tabular}` becomes a `Table:` landmark placeholder (then a `Table: <sentence>` after a mocked fill), confirm NO numeric rows (`2 17`, `3 27`, ...) and NO label/phrase cells remain. Confirm a captioned figure fixture yields `Figure: <full caption>` (untruncated).
- Build the reading transcript text path (no audio) over a small fixture and assert the landmark splits into its own section via `split_transcript_by_sections`, i.e. real silence would bracket it.
- Do NOT regenerate audio (expensive Fish TTS); that is a separate manual step after merge.

## Out of scope

- Audio regeneration of any existing chapter.
- A dedicated short-caption field on `ImageSummary` (figure caption-less path clamps the existing summary for v1).
- Carry-context / cross-chapter glossary (tracked separately as enhancement #21).
- Voicing any table cell data in any form.
