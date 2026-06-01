---
id: tp31tablefigaudio053101
title: Table_processor
desc: ''
updated: 1780274093769
created: 1780274093769
---

## Purpose

Fill caption-less table landmarks with a one-sentence summary. Mirrors [[swanki.processing.image_processor]]: [[swanki.processing.markdown_cleaner]] has already replaced each LaTeX table/tabular block in `clean-md-singles` with a `Table:` landmark -- a verbatim caption when one existed, or a `\x00TBLLMK:<stem>:<idx>\x00` placeholder plus a stashed `table-summaries/<stem>_<idx>.source.txt` of the raw block when it did not. This step summarizes each stash and fills the placeholder. Plan: [[plan.reading-table-figure-landmarks.2026.05.31]].

## Design

- **Text LLM, not vision.** Tables in `clean-md-singles` are LaTeX/markdown text, so the summary comes from a `text_agent` call wrapped in `with_safety_retry` (same biosec-refusal handling as image summaries). The prompt asks for ONE short sentence describing what the table SHOWS -- never its cell values.
- **Idempotent + cached.** Each summary is cached to `table-summaries/<stem>_<idx>.md`; a re-run reuses the cache (and, since the placeholder is already filled, makes no LLM call). `first_sentence` clamps the output.
- **Fail-soft.** A missing source stash or an LLM failure leaves the placeholder in place; the pipeline's `strip_unfilled_placeholders` pass ([[swanki.pipeline.pipeline]] `process_tables`) then removes it so a NUL sentinel never reaches TTS.
- Returns `list[TableSummary]` (see [[swanki.models.document]]).

## Pipeline wiring

`Pipeline.process_tables(image_summaries)` runs right after `process_images` and before section classification: it (1) fills caption-less FIGURE placeholders from the already-generated image summaries (clamped to one sentence, matched by URL), (2) runs `TableProcessor.process_all_tables()` for tables, then (3) strips any unfilled placeholder. All three edit `clean-md-singles` in place so both reading and lecture read the finished landmarks.
