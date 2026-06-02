"""
tests/test_pdf_prep.py
[[tests.test_pdf_prep]]
https://github.com/Mjvolk3/Swanki/tree/main/tests/test_pdf_prep.py

Round-trip tests for swanki.pdf_prep.pack_chapter: chapter chop plus one or
more (possibly non-contiguous) answer-key ranges concatenated into one packed
PDF via pure-Python pypdf.
"""

from pathlib import Path

import pytest
from pypdf import PdfReader, PdfWriter


def _make_pdf(path: Path, n_pages: int) -> None:
    """Write an n-page blank PDF to ``path``."""
    writer = PdfWriter()
    for _ in range(n_pages):
        writer.add_blank_page(width=72, height=72)
    with open(path, "wb") as fh:
        writer.write(fh)


@pytest.fixture
def source_pdf(tmp_path: Path) -> Path:
    """A 30-page source PDF standing in for a Schaum's book scan."""
    src = tmp_path / "source.pdf"
    _make_pdf(src, 30)
    return src


class TestPackChapter:
    def test_single_answer_key_range(self, source_pdf: Path, tmp_path: Path) -> None:
        from swanki.pdf_prep import pack_chapter

        out = tmp_path / "packed.pdf"
        n = pack_chapter(source_pdf, (8, 18), (28, 28), out)
        # 11 chapter pages + 1 answer-key page.
        assert n == 12
        assert len(PdfReader(out).pages) == 12

    def test_multiple_noncontiguous_answer_ranges(
        self, source_pdf: Path, tmp_path: Path
    ) -> None:
        from swanki.pdf_prep import pack_chapter

        out = tmp_path / "packed.pdf"
        n = pack_chapter(source_pdf, (1, 5), [(20, 21), (28, 30)], out)
        # 5 chapter + 2 + 3 answer-key pages.
        assert n == 10
        assert len(PdfReader(out).pages) == 10

    def test_out_of_bounds_range_raises(
        self, source_pdf: Path, tmp_path: Path
    ) -> None:
        from swanki.pdf_prep import pack_chapter

        out = tmp_path / "packed.pdf"
        with pytest.raises(ValueError):
            pack_chapter(source_pdf, (8, 18), (40, 41), out)

    def test_creates_parent_dir(self, source_pdf: Path, tmp_path: Path) -> None:
        from swanki.pdf_prep import pack_chapter

        out = tmp_path / "nested" / "dir" / "packed.pdf"
        pack_chapter(source_pdf, (1, 2), (10, 10), out)
        assert out.exists()
