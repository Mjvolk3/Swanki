r"""
swanki/processing/table_processor.py
[[swanki.processing.table_processor]]
https://github.com/Mjvolk3/Swanki/tree/main/swanki/processing/table_processor.py
Test file: tests/test_table_processor.py

Fill caption-less table landmarks with a one-sentence summary.

Mirrors :mod:`swanki.processing.image_processor`: the markdown cleaner has
already replaced each LaTeX table/tabular block in ``clean-md-singles`` with a
``Table:`` landmark -- a verbatim caption when one existed, or a
``\\x00TBLLMK:<page-stem>:<idx>\\x00`` placeholder plus a stashed
``table-summaries/<stem>_<idx>.source.txt`` of the raw block when it did not.
This step reads each stashed source, calls a TEXT LLM for a one-sentence
description of what the table SHOWS (never its cell values), caches it to
``table-summaries/<stem>_<idx>.md``, and rewrites the placeholder in place.
"""

from __future__ import annotations

import logging
from pathlib import Path

from ..llm.agents import text_agent
from ..llm.safety import with_safety_retry
from ..models.document import TableSummary
from .landmarks import (
    fill_table_placeholder,
    first_sentence,
    iter_table_placeholders,
)

logger = logging.getLogger(__name__)

_TABLE_SUMMARY_PROMPT = """You are describing a table for an audio listener who \
cannot see it. In ONE short sentence, say what the table SHOWS or compares -- \
its subject and the relationship between its columns. Do NOT read or list any \
cell values, numbers, or row entries. Do NOT start with "This table"; just \
describe it.

Table source:
{body}
"""


class TableProcessor:
    """Summarize caption-less tables and fill their landmark placeholders.

    Args:
        output_base: Base directory holding ``clean-md-singles`` and the
            ``table-summaries`` cache/stash directory.
        model: pydantic-ai model string for the text summarizer.
    """

    def __init__(self, output_base: Path, model: str) -> None:
        """Store output dirs and the text-summarizer model string."""
        self.output_base = output_base
        self.clean_md_singles_dir = output_base / "clean-md-singles"
        self.table_summaries_dir = output_base / "table-summaries"
        self.model = model

    def process_all_tables(self) -> list[TableSummary]:
        """Fill every table placeholder across all cleaned pages.

        Returns:
            One :class:`TableSummary` per filled placeholder, in page order.
        """
        self.table_summaries_dir.mkdir(parents=True, exist_ok=True)
        summaries: list[TableSummary] = []
        for md_file in sorted(self.clean_md_singles_dir.glob("*.md")):
            summaries.extend(self._process_file(md_file))
        logger.info(f"Filled {len(summaries)} table landmark(s)")
        return summaries

    def _process_file(self, md_path: Path) -> list[TableSummary]:
        content = md_path.read_text(encoding="utf-8")
        results: list[TableSummary] = []
        changed = False
        for page_stem, idx in iter_table_placeholders(content):
            summary = self._summary_for(page_stem, idx)
            if summary is None:
                # Leave the placeholder; the cleaner's strip pass removes any
                # unfilled landmark so a NUL sentinel never reaches TTS.
                logger.warning(f"No summary for table {page_stem}:{idx}; skipping")
                continue
            content = fill_table_placeholder(content, page_stem, idx, summary)
            changed = True
            results.append(
                TableSummary(page_stem=page_stem, occurrence_idx=idx, summary=summary)
            )
        if changed:
            md_path.write_text(content, encoding="utf-8")
        return results

    def _summary_for(self, page_stem: str, idx: int) -> str | None:
        """Return the one-sentence summary for one table, cached on disk.

        Idempotent: a cached ``<stem>_<idx>.md`` is reused; otherwise the
        stashed ``<stem>_<idx>.source.txt`` is summarized and cached.
        """
        cache = self.table_summaries_dir / f"{page_stem}_{idx}.md"
        if cache.exists():
            return first_sentence(cache.read_text(encoding="utf-8").strip())

        source = self.table_summaries_dir / f"{page_stem}_{idx}.source.txt"
        if not source.exists():
            logger.error(f"Missing table source stash: {source}")
            return None

        body = source.read_text(encoding="utf-8").strip()
        result = with_safety_retry(
            text_agent,
            _TABLE_SUMMARY_PROMPT.format(body=body),
            model=self.model,
            model_settings={"max_tokens": 4000, "temperature": 0.3},
            label="table summary",
        )
        summary = first_sentence(result.output.strip())
        cache.write_text(summary, encoding="utf-8")
        return summary
