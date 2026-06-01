---
id: lmk31tablefigaudio0531
title: Landmarks
desc: ''
updated: 1780274093769
created: 1780274093769
---

## Purpose

Shared sentinels and helpers for table/figure audio "landmarks" -- a short spoken `Figure: <desc>` / `Table: <desc>` cue (no number) bracketed by `---SECTION_BREAK---` so the audio layer surrounds it with real silence. Used by [[swanki.processing.markdown_cleaner]] (emits landmarks) and [[swanki.processing.table_processor]] / [[swanki.pipeline.pipeline]] (fill caption-less placeholders). Plan: [[plan.reading-table-figure-landmarks.2026.05.31]].

## Design

- **NUL-delimited placeholders** (`\x00FIGLMK:<url>\x00`, `\x00TBLLMK:<stem>:<idx>\x00`): opaque, cannot collide with prose, survive the markdown->TTS scrubber chain untouched, and are trivially regex-matched by the fill step. Mirrors `_common._SECTION_BREAK_TTS_MASK`'s opaque-mask idea.
- `landmark_block(kind, body)`: builds the `\n\n---SECTION_BREAK---\n{kind}: {body}\n---SECTION_BREAK---\n\n` block so it splits into its own audio section.
- `figure_placeholder(url)` keys figures by image URL (filled from image summaries by URL -- robust to ordering); `table_placeholder(stem, idx)` keys tables by page + occurrence.
- `clean_caption(raw)`: strips non-math LaTeX commands but **protects `$...$` / `$$...$$`** so a caption like `plot of $\alpha$ vs $\beta$` keeps its math for `humanize_latex` to verbalize downstream. (Replaces the old cleaner's command-strip that would have broken math.)
- `first_sentence(text, max_words=40)`: clamps a multi-sentence summary (e.g. an image summary) to one sentence for the landmark.
- `fill_figure_placeholders` / `fill_table_placeholder` / `iter_table_placeholders`: the fill API.
- `strip_unfilled_placeholders`: safety net -- if a fill fails, drops the whole `Figure:`/`Table:` line whose only content is an unfilled placeholder, then any stray sentinel, so a NUL sentinel can never reach TTS.
