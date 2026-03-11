---
id: yws3lko9xjyk9413ykk9e75
title: Plan 0
desc: ''
updated: 1773182866705
created: 1773180425409
---
Character-Based Segmentation for Card Generation

## Context

Some PDFs have pages with very little content (e.g., a single margin word after pandoc epub→PDF conversion). With per-page card limits (e.g., 3 cards/page), these near-empty pages still generate full card allocations from almost nothing. Instead of scaling card count per page, we add an alternative segmentation mode: **recombine** all per-page markdown files into one document, then **re-split** into uniform character-length segments at newline boundaries. Cards are generated per segment, naturally scaling to content density. Existing per-page mode remains the default.

## Unified Concept: "Segment"

A **segment** is the discrete unit from which cards are generated. Both modes produce a list of segment files — the difference is how they're created:

- **`page` mode** (default): segments = `clean-md-singles/page-*.md` (PDF page boundaries)
- **`char` mode** (new): segments = `segments/segment-*.md` (character-length splits at newline boundaries)

All downstream processing (context_radius, card generation, math density adjustment) operates on segments identically regardless of mode.

## Config Changes

**Replaces**: `num_cards_per_page`, `cloze_cards_per_page`, and dead `chunk_size`/`overlap` params.

```yaml
processing:
  segmentation: page            # "page" (default) or "char"
  context_radius: 2             # shared — surrounding pages OR surrounding segments
  cards_per_segment: 3          # replaces num_cards_per_page
  cloze_per_segment: 1          # replaces cloze_cards_per_page
  blocking_audio: true
  confirm_before_generation: true
  char_segmentation:            # only used when segmentation: char
    target_chars: 2000          # target characters per segment
  image_cards:
    # ... unchanged ...
```

**Preset defaults** (all use `segmentation: page`):

| Preset   | cards_per_segment | cloze_per_segment | context_radius |
|----------|-------------------|-------------------|----------------|
| default  | 2                 | 0                 | 2              |
| standard | 4                 | 1                 | 1              |
| larger   | 5                 | 3                 | 2              |
| smaller  | 2                 | 1                 | 0              |

Dead `chunk_size`/`overlap` params removed from all presets. See [[plan.config-refactor-less-clunky.plan-0]] for the broader config cleanup that will move these into `swanki/conf/` package defaults.

## New File: `swanki/pipeline/segmenter.py`

Pure utility module. No class, no dependencies beyond pathlib.

### `combine_markdown_files(md_files: list[Path]) -> tuple[str, list[int]]`

- Reads all clean-md-singles in order
- Joins with `\n\n` separator (image references kept — provides context to LLM)
- Returns `(combined_text, page_char_offsets)` where `page_char_offsets[i]` is the starting char index of page `i` in the combined text
- Page offsets enable segment-to-page mapping for image card interleaving

### `split_into_segments(text: str, target_chars: int) -> list[tuple[str, int, int]]`

- Splits combined text into segments of ~`target_chars` characters
- **Splits at newline boundaries** — scans backward from `target_chars` position to find nearest `\n`
- If no newline found within last 20% of target, falls back to nearest space
- Returns list of `(segment_text, start_char, end_char)` tuples — char ranges needed for page mapping
- Guarantees no mid-line splits (preserves equations, sentences, image refs)

### `write_segment_files(segments: list[tuple[str, int, int]], output_dir: Path) -> list[Path]`

- Creates `segments/` directory
- Writes `segment-1.md`, `segment-2.md`, etc.
- Returns list of segment file paths

### `build_segment_to_page_map(page_offsets: list[int], segment_ranges: list[tuple[int, int]], total_pages: int) -> list[list[int]]`

- Maps each segment to the page indices it overlaps with
- Used for interleaving image cards in document order
- Example: segment 0 covers chars 0–1980 → overlaps pages 0, 1, 2

## Pipeline Changes

**File: `swanki/pipeline/pipeline.py`**

### 1. Delete `generate_cards_with_context` (public method, line 1288)

This public method duplicates `_generate_cards_for_page_with_context` wrapped in its own loop. It's dead code — never called by `process_full()` or any other caller. Remove it and update the class docstring (line 106).

### 2. Rename `_generate_cards_for_page_with_context` → `_generate_cards_for_segment`

Same function, same signature — just rename to reflect the unified segment concept. Works identically for page-segments and char-segments.

### 3. Add segmentation stage in `process_full()`

Insert between step 5 (summary generation) and step 5.5 (estimation), so `estimate_card_count` can use actual segment files:

```python
# 5.5 Segmentation (if char mode)
processing_config = pipeline_config.get("processing", {})
segmentation_mode = processing_config.get("segmentation", "page")

if segmentation_mode == "char":
    self.state.current_stage = "segmentation"
    char_config = processing_config.get("char_segmentation", {})
    combined_text, page_offsets = combine_markdown_files(cleaned_files)
    segment_tuples = split_into_segments(
        combined_text, char_config.get("target_chars", 2000)
    )
    segment_dir = self.output_base / "segments"
    segment_files = write_segment_files(segment_tuples, segment_dir)
    segment_to_pages = build_segment_to_page_map(
        page_offsets,
        [(s, e) for _, s, e in segment_tuples],
        len(cleaned_files),
    )
    text_card_files = segment_files
else:
    text_card_files = cleaned_files
    segment_to_pages = None  # not needed — 1:1 with cleaned_files
```

### 4. Card generation loop with document-order interleaving

```python
cards_per_seg = processing_config.get("cards_per_segment", 3)

last_image_page = -1
for seg_idx, seg_file in enumerate(text_card_files):
    # Text cards for this segment
    seg_cards = self._generate_cards_for_segment(
        seg_idx, text_card_files, doc_summary,
        context_radius=processing_config.get("context_radius", 1),
        num_cards=cards_per_seg,
    )
    all_cards.extend(seg_cards)

    # Image cards — interleaved in document order
    if image_cards_enabled:
        if segment_to_pages is not None:
            # Char mode: use segment-to-page mapping
            pages_for_this_segment = segment_to_pages[seg_idx]
        else:
            # Page mode: segment index == page index
            pages_for_this_segment = [seg_idx]

        for page_idx in pages_for_this_segment:
            if page_idx > last_image_page:
                img_cards = self._generate_image_cards_for_page(
                    cleaned_files[page_idx], doc_summary, image_summaries,
                    cards_per_image=image_config.get("cards_per_image", 3),
                    # ... other image config ...
                )
                all_cards.extend(img_cards)
                last_image_page = page_idx
```

This preserves document order in both modes: text from segment N → images from pages covered by segment N → text from segment N+1.

### 5. Update `estimate_card_count`

```python
if segmentation_mode == "char":
    num_segments = len(segment_files)
else:
    num_segments = len(markdown_files)

cards_per_seg = processing_config.get("cards_per_segment", 3)
cloze_per_seg = processing_config.get("cloze_per_segment", 1)
text_cards = num_segments * (cards_per_seg + cloze_per_seg)
# image_cards unchanged
```

### 6. Rename config reads throughout pipeline

All `processing_config.get("num_cards_per_page", 3)` → `processing_config.get("cards_per_segment", 3)`.
All `processing_config.get("cloze_cards_per_page", 2)` → `processing_config.get("cloze_per_segment", 1)`.

## Output Directory

```
output_base/
  pdf-singles/         # existing
  md-singles/          # existing
  clean-md-singles/    # existing (= segments in page mode)
  segments/            # NEW — only when segmentation: char
    segment-1.md
    segment-2.md
    ...
  images/              # existing
```

## Sequencing Note (see [[plan.major-refactor-sequence.plan-0]])

This is **step 3** of the major refactor sequence. By this point, `generator.py` has been **deleted** (step 2 — config refactor). All config changes go directly to `swanki/conf/pipeline/*.yaml` package defaults.

### Adjustments from original plan

- ~~Config Generator Update~~ — **SKIP ENTIRELY**. `generator.py` no longer exists.
- All `.swanki_config/pipeline/*.yaml` references become `swanki/conf/pipeline/*.yaml`
- The `mode=audio_only` branch (step 1) exists in `process_full()` — the new segmentation stage must be placed inside the `mode == "full"` branch (segments are only needed for card generation, not audio-only mode)

### Quality gates for this step

- All new/modified code must pass `mypy --strict` on touched files
- Google-style docstrings on all functions in `segmenter.py`
- Frontmatter header block on `segmenter.py` per project conventions
- Frontmatter updated via `/update-py-notes` for touched `.py` files
- Full unit test suite in `tests/test_segmenter.py` (11 tests listed below)
- Sphinx docs updated for new `segmentation` config options
- `ruff check` and `ruff format` pass

## Files to Modify/Create

| File                                 | Action                                                                                                                                                                                                                                                   |
|--------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `swanki/pipeline/segmenter.py`       | **CREATE** — `combine_markdown_files`, `split_into_segments`, `write_segment_files`, `build_segment_to_page_map`                                                                                                                                         |
| `swanki/pipeline/__init__.py`        | **MODIFY** — export segmenter if needed                                                                                                                                                                                                                  |
| `swanki/pipeline/pipeline.py`        | **MODIFY** — delete `generate_cards_with_context`, rename `_generate_cards_for_page_with_context` → `_generate_cards_for_segment`, add segmentation stage, update card gen loop with interleaving, update `estimate_card_count`, rename config key reads |
| `swanki/conf/pipeline/default.yaml`  | **MODIFY** — new config keys, remove dead params                                                                                                                                                                                                         |
| `swanki/conf/pipeline/standard.yaml` | **MODIFY** — same                                                                                                                                                                                                                                        |
| `swanki/conf/pipeline/larger.yaml`   | **MODIFY** — same                                                                                                                                                                                                                                        |
| `swanki/conf/pipeline/smaller.yaml`  | **MODIFY** — same                                                                                                                                                                                                                                        |
| `tests/test_segmenter.py`            | **CREATE** — unit tests                                                                                                                                                                                                                                  |

## Tests: `tests/test_segmenter.py`

- `test_combine_preserves_images` — image refs kept in combined output
- `test_combine_returns_page_offsets` — offsets correctly track page boundaries
- `test_split_respects_newlines` — segments split at `\n`, not mid-line
- `test_split_fallback_to_space` — falls back to space split when no newline in range
- `test_split_short_content` — content shorter than target_chars → single segment
- `test_split_empty_content` — returns empty list
- `test_split_returns_char_ranges` — each tuple has correct (text, start, end)
- `test_write_segment_files` — creates numbered files in segments/
- `test_segment_preserves_equations` — LaTeX blocks not split mid-equation
- `test_segment_to_page_map` — mapping correctly identifies overlapping pages
- `test_segment_to_page_map_single_page_segment` — segment within one page maps to just that page

## Verification

1. Run unit tests: `python -m pytest tests/test_segmenter.py -xvs`
2. Run existing tests to confirm no regression: `python -m pytest tests/ -x`
3. Manual test with `segmentation: char`: inspect `segments/` directory for reasonable splits
4. Manual test with `segmentation: page`: confirm identical behavior to current
5. Verify card ordering in Anki: cards should appear in document order in both modes
