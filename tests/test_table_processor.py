"""
tests/test_table_processor.py
[[tests.test_table_processor]]
https://github.com/Mjvolk3/Swanki/tree/main/tests/test_table_processor.py
Test file: tests/test_table_processor.py

Tests for caption-less table landmark filling via the (mocked) text LLM.
"""

from pathlib import Path
from unittest.mock import MagicMock, patch

from swanki.processing.landmarks import landmark_block, table_placeholder
from swanki.processing.table_processor import TableProcessor


def _setup(tmp_path: Path, *, source: str = "factor & years \\\\ 2 & 17 \\\\") -> Path:
    clean = tmp_path / "clean-md-singles"
    clean.mkdir()
    summaries = tmp_path / "table-summaries"
    summaries.mkdir()
    page = clean / "page-4.md"
    page.write_text(
        "Intro.\n" + landmark_block("Table", table_placeholder("page-4", 0)) + "Outro.\n"
    )
    (summaries / "page-4_0.source.txt").write_text(source)
    return tmp_path


def _mock_llm(text: str):
    out = MagicMock()
    out.output = text
    return patch(
        "swanki.processing.table_processor.with_safety_retry", return_value=out
    )


def test_fills_placeholder_with_one_sentence(tmp_path):
    _setup(tmp_path)
    with _mock_llm("A comparison of parent age against the knowledge a child faces."):
        results = TableProcessor(tmp_path, "fake:model").process_all_tables()
    out = (tmp_path / "clean-md-singles" / "page-4.md").read_text()
    assert "Table: A comparison of parent age against the knowledge a child faces." in out
    assert "TBLLMK" not in out.replace("\x00", "")
    assert len(results) == 1
    assert results[0].page_stem == "page-4" and results[0].occurrence_idx == 0


def test_never_voices_cells(tmp_path):
    _setup(tmp_path, source="factor & years \\\\ 2 & 17 \\\\ 3 & 27 \\\\")
    with _mock_llm("A table of doubling factors versus parent age."):
        TableProcessor(tmp_path, "fake:model").process_all_tables()
    out = (tmp_path / "clean-md-singles" / "page-4.md").read_text()
    assert "2 17" not in out and "27" not in out


def test_clamps_multisentence_summary(tmp_path):
    _setup(tmp_path)
    with _mock_llm("First sentence here. Second sentence should be dropped."):
        TableProcessor(tmp_path, "fake:model").process_all_tables()
    out = (tmp_path / "clean-md-singles" / "page-4.md").read_text()
    assert "First sentence here." in out
    assert "Second sentence" not in out


def test_idempotent_uses_cache_no_second_llm_call(tmp_path):
    _setup(tmp_path)
    with _mock_llm("A cached description of the table."):
        TableProcessor(tmp_path, "fake:model").process_all_tables()
    # cache now exists; a second run must NOT call the LLM (placeholder gone,
    # and even if present the cache would be reused)
    with patch(
        "swanki.processing.table_processor.with_safety_retry",
        side_effect=AssertionError("LLM must not be called on rerun"),
    ):
        results = TableProcessor(tmp_path, "fake:model").process_all_tables()
    assert results == []


def test_cache_reused_when_placeholder_present(tmp_path):
    # Pre-seed the cache, then ensure the LLM is never called.
    _setup(tmp_path)
    (tmp_path / "table-summaries" / "page-4_0.md").write_text("Pre-seeded summary.")
    with patch(
        "swanki.processing.table_processor.with_safety_retry",
        side_effect=AssertionError("LLM must not be called when cache exists"),
    ):
        TableProcessor(tmp_path, "fake:model").process_all_tables()
    out = (tmp_path / "clean-md-singles" / "page-4.md").read_text()
    assert "Table: Pre-seeded summary." in out


def test_missing_source_leaves_placeholder(tmp_path):
    clean = tmp_path / "clean-md-singles"
    clean.mkdir()
    (tmp_path / "table-summaries").mkdir()
    page = clean / "page-9.md"
    page.write_text(landmark_block("Table", table_placeholder("page-9", 0)))
    # no source.txt stashed -> cannot summarize
    with patch(
        "swanki.processing.table_processor.with_safety_retry",
        side_effect=AssertionError("LLM must not be called without source"),
    ):
        results = TableProcessor(tmp_path, "fake:model").process_all_tables()
    assert results == []
    # placeholder still present (pipeline's strip pass removes it later)
    assert "TBLLMK" in page.read_text().replace("\x00", "")
