---
id: 0x9jdz6ovrum6bdr8rxgpx7
title: Markdown_cleaner
desc: ''
updated: 1768701651032
created: 1768690902312
---

## Bug Fix: Image Extraction from LaTeX Figure Blocks (2026-01-17)

### Problem

No image cards were being generated for some PDFs (e.g., `guptaRetinalPigmentEpithelium2023`) even though the PDF contained images and previous papers worked fine.

**Symptoms:**

- `image-summaries/` directory was empty
- Log showed: `Processed 0 images total`
- `ImageProcessor` found 0 images in `clean-md-singles/`
- PDF actually contained 11 images (verified with `pdfimages -list`)

### Root Cause

**Two-part issue:**

1. **Pattern ordering bug** (introduced in commit `89493f9` on Dec 17, 2025):
   - New pattern `figure_blocks` was added to remove `\begin{figure}...\end{figure}` blocks
   - This pattern was applied BEFORE the `includegraphics` pattern could extract image URLs
   - Result: Entire figure blocks were deleted, losing all image URLs

2. **Mathpix output variation**:
   - **Some PDFs** (costanzo, kuzmin): Mathpix outputs BOTH formats:

     ```markdown
     ![](https://cdn.mathpix.com/...)

     \begin{figure}
     \includegraphics{https://cdn.mathpix.com/...}
     \caption{...}
     \end{figure}
     ```

     These worked because the standalone `![](url)` survived figure block removal.

   - **Other PDFs** (gupta): Mathpix outputs ONLY LaTeX format:

     ```latex
     \begin{figure}
     \includegraphics{https://cdn.mathpix.com/...}
     \caption{...}
     \end{figure}
     ```

     These failed because figure block removal deleted everything.

### The Fix

Added new method `_convert_figure_blocks_to_markdown()` that:

1. **Finds** all `\begin{figure}...\end{figure}` blocks
2. **Extracts** `\includegraphics{url}` from each block
3. **Extracts** caption text from `\caption{...}` for alt text
4. **Replaces** entire figure block with markdown: `![caption](url)`
5. **Runs BEFORE** table removal and other cleaning

**Key changes in `_apply_cleaning()`:**

```python
# OLD (broken):
multiline_patterns = ['figure_blocks', 'table_blocks']
for pattern_name in multiline_patterns:
    content = re.sub(pattern, replacement, content, flags=re.DOTALL)

# NEW (fixed):
content = self._convert_figure_blocks_to_markdown(content)  # Extract FIRST
multiline_patterns = ['table_blocks']  # Then remove tables only
```

### Files Modified

- `swanki/processing/markdown_cleaner.py`:
  - Added `_convert_figure_blocks_to_markdown()` method (lines 236-293)
  - Modified `_apply_cleaning()` to call new method before pattern removal (line 258)
  - Removed `figure_blocks` and `includegraphics` patterns from PATTERNS dict
  - Updated comments to explain figure handling

### Testing

To verify the fix works:

```bash
# Re-process the failing paper
swanki pdf_path=/path/to/guptaRetinalPigmentEpithelium2023_cut.pdf \
  citation_key=guptaRetinalPigmentEpithelium2023 \
  +output_dir=../Swanki_Data/guptaRetinalPigmentEpithelium2023/test_fixed

# Check that image-summaries/ is no longer empty
ls output_dir/image-summaries/

# Verify markdown images in clean-md-singles/
grep '!\[' output_dir/clean-md-singles/*.md
```

### Why This Happened

The original code assumed Mathpix would always output both markdown AND LaTeX formats. When commit `89493f9` added figure block removal for "cleaner reading audio," it inadvertently broke image extraction for PDFs where Mathpix only outputs LaTeX format.

The fix makes the pipeline robust to both Mathpix output styles by explicitly converting LaTeX figures to markdown before cleanup.

## 2026.03.12 - Ruff formatting pass

Applied ruff formatting: double quotes, import sorting, whitespace cleanup, Google-style docstring headers. No behavioral changes.

## 2026.05.31 - Table/figure audio landmarks

Figures and tables now become standardized audio "landmarks" -- a short spoken `Figure: <desc>` / `Table: <desc>` cue (no number) bracketed by `---SECTION_BREAK---` so the audio layer surrounds it with real silence. See [[plan.reading-table-figure-landmarks.2026.05.31]] and the shared [[swanki.processing.landmarks]] helpers.

Changes here:
- `_convert_figure_blocks_to_markdown`: the 100-char caption truncation is GONE -- the full caption is read verbatim. The image becomes `![](url)` (EMPTY alt) plus a `Figure:` landmark, so `clean_markdown_for_tts` (which speaks the alt) no longer double-reads the caption. Caption-less figures emit a `\x00FIGLMK:<url>\x00` placeholder filled later from the image summary (clamped to one sentence).
- New `_convert_table_blocks_to_landmarks(content, page_stem)`: replaces the old delete-only `table_blocks` regex. Handles BOTH wrapped `\begin{table}` floats AND bare `\begin{tabular}` (what the Hamming book uses -- previously matched by nothing, so raw numeric rows leaked into the reading, e.g. Ch1 "2 17 3 27..."). Wrapped floats are consumed first so an inner `tabular` is not double-counted. The cell BODY is always removed (cells are never voiced); a caption is read verbatim, else a `\x00TBLLMK:<stem>:<idx>\x00` placeholder is emitted and the raw block stashed to `table-summaries/<stem>_<idx>.source.txt` for [[swanki.processing.table_processor]] to summarize.
- `_apply_cleaning` gained a `page_stem` arg (keys table placeholders); `clean_single_file` passes `md_path.stem`.
- Scope: LaTeX `table`/`tabular` only. MinerU pipe tables are NOT handled -- verified 0 pipe tables across the corpus (95 files have `tabular`, 132 have `table`), so this is a deferred follow-up, not a gap.
