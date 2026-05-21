"""
tests/test_ocr_mineru_split.py
[[tests.test_ocr_mineru_split]]

Tests for splitting MinerU content_list.json into per-page md-singles.
"""

import shutil
from pathlib import Path

from swanki.ocr.mineru import split_content_list_to_pages

FIXTURE = Path(__file__).parent / "fixtures" / "mineru" / "sample_content_list.json"


def _setup_raw(tmp_path: Path) -> Path:
    raw_dir = tmp_path / "mineru-raw"
    images = raw_dir / "images"
    images.mkdir(parents=True)
    (images / "fig1.jpg").write_bytes(b"\xff\xd8\xff")
    (images / "tab1.jpg").write_bytes(b"\xff\xd8\xff")
    shutil.copy2(FIXTURE, raw_dir / "doc_content_list.json")
    return raw_dir


def test_split_groups_blocks_by_page_with_backfill(tmp_path):
    raw_dir = _setup_raw(tmp_path)
    output_base = tmp_path / "out"
    pages = split_content_list_to_pages(
        raw_dir / "doc_content_list.json", raw_dir, output_base, num_pages=3
    )
    assert [p.name for p in pages] == ["page-1.md", "page-2.md", "page-3.md"]
    # Page 3 has no blocks -> empty backfill file exists.
    assert (output_base / "md-singles" / "page-3.md").read_text() == ""


def test_split_renders_headings_and_equations(tmp_path):
    raw_dir = _setup_raw(tmp_path)
    output_base = tmp_path / "out"
    split_content_list_to_pages(
        raw_dir / "doc_content_list.json", raw_dir, output_base, num_pages=3
    )
    page1 = (output_base / "md-singles" / "page-1.md").read_text()
    assert "# Introduction" in page1
    assert "first paragraph" in page1
    assert "$$E = mc^2$$" in page1
    # header noise block must be skipped
    assert "Running Head" not in page1


def test_split_copies_images_and_rewrites_path(tmp_path):
    raw_dir = _setup_raw(tmp_path)
    output_base = tmp_path / "out"
    split_content_list_to_pages(
        raw_dir / "doc_content_list.json", raw_dir, output_base, num_pages=3
    )
    page2 = (output_base / "md-singles" / "page-2.md").read_text()
    assert "![](images/fig1.jpg)" in page2
    assert (output_base / "images" / "fig1.jpg").exists()
    # table body passes through
    assert "<table>" in page2
    # page_number noise skipped
    assert page2.strip() != "2"
