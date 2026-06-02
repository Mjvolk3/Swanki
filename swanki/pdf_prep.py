"""
swanki/pdf_prep.py
[[swanki.pdf_prep]]
https://github.com/Mjvolk3/Swanki/tree/main/swanki/pdf_prep.py
Test file: tests/test_pdf_prep.py

Pre-pipeline PDF input preparation: chop one chapter's forward pages and one or
more (possibly non-contiguous) back-of-book answer-key page ranges out of a
source PDF and concatenate them into a single packed PDF for solution_manual
mode. Pure-Python via ``pypdf`` — no ``qpdf`` / ``pdfunite`` subprocess (CI has
neither), parallel to ``swanki/cut.py``.
"""

import argparse
from pathlib import Path

from pypdf import PdfReader, PdfWriter

PageRange = tuple[int, int]


def _add_range(writer: PdfWriter, reader: PdfReader, page_range: PageRange) -> None:
    """Append a 1-based, inclusive page range from reader onto writer.

    Args:
        writer: Destination PDF writer.
        reader: Source PDF reader.
        page_range: ``(first, last)`` 1-based inclusive page numbers.

    Raises:
        ValueError: If the range is malformed or out of bounds.
    """
    first, last = page_range
    total = len(reader.pages)
    if first < 1:
        raise ValueError(f"Range start must be >= 1, got {first}")
    if last > total:
        raise ValueError(f"Range end {last} exceeds source page count {total}")
    if first > last:
        raise ValueError(f"Range start {first} must be <= end {last}")
    for i in range(first - 1, last):
        writer.add_page(reader.pages[i])


def pack_chapter(
    source_pdf: Path,
    chapter_pages: PageRange,
    answer_key_pages: PageRange | list[PageRange],
    output_pdf: Path,
) -> int:
    """Chop chapter pages and answer-key range(s), concatenate into one PDF.

    Page ranges are 1-based and inclusive (matching the source PDF's printed /
    viewer page numbering). Answer-key ranges are appended in order after the
    chapter pages; pass a list for an answer key that spills across, or is split
    over, several non-contiguous page ranges.

    Args:
        source_pdf: Path to the cleaned source PDF.
        chapter_pages: Inclusive page range for the chapter.
        answer_key_pages: One inclusive range, or a list of them.
        output_pdf: Where to write the packed PDF.

    Returns:
        The number of pages written to ``output_pdf``.
    """
    answer_ranges = (
        [answer_key_pages]
        if isinstance(answer_key_pages, tuple)
        else list(answer_key_pages)
    )
    reader = PdfReader(source_pdf)
    writer = PdfWriter()
    _add_range(writer, reader, chapter_pages)
    for rng in answer_ranges:
        _add_range(writer, reader, rng)
    output_pdf.parent.mkdir(parents=True, exist_ok=True)
    with open(output_pdf, "wb") as fh:
        writer.write(fh)
    return len(writer.pages)


def _parse_range(spec: str) -> PageRange:
    """Parse a range like ``'8-18'`` into a ``(first, last)`` tuple."""
    a, b = spec.split("-")
    return int(a), int(b)


def main() -> None:
    """CLI entry point.

    Back-compatible with the prior ``scripts/schaum_chapter_pack.py`` flags
    (``--source`` / ``--chapter-pages`` / ``--answer-key-pages`` / ``--output``).
    ``--answer-key-pages`` may be passed more than once for a split answer key.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--chapter-pages", required=True, type=_parse_range)
    parser.add_argument(
        "--answer-key-pages",
        required=True,
        type=_parse_range,
        action="append",
        help="Inclusive answer-key page range; repeat for non-contiguous keys.",
    )
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    n_pages = pack_chapter(
        args.source, args.chapter_pages, args.answer_key_pages, args.output
    )
    print(f"Wrote {args.output} ({n_pages} pages)")


if __name__ == "__main__":
    main()
