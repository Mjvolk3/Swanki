"""
scripts/book_solution_pack.py
[[scripts.book_solution_pack]]
https://github.com/Mjvolk3/Swanki/tree/main/scripts/book_solution_pack.py

Pack one chapter for solution_manual mode when the worked solutions live in a
SEPARATE solution-manual PDF (not back-of-book pages of the chapter's own
source, which is what schaum_chapter_pack.py handles).

Concatenates an already-extracted chapter PDF (chapter body + its end-of-chapter
Exercises) with the page slice of the separate solutions manual that covers
THAT chapter's worked solutions. The slice should be the SMALLEST 1-indexed,
inclusive page range covering this chapter's solutions; other chapters' blocks
that share a boundary page are tolerated (the enumeration/pairing keys on the
book problem IDs), but extra pages inflate OCR cost and the LLM context window.

Usage:
    python scripts/book_solution_pack.py \\
        --chapter-pdf  .../chapters/Bishop_CH02.pdf \\
        --solutions-pdf .../Bishop-Solutions-2024.pdf \\
        --solution-pages 4-25 \\
        --output .../chapters/bishopDeepLearningFoundations2024_CH02_probabilities.pdf
"""

import argparse
import subprocess
import tempfile
from pathlib import Path


def pack_chapter(
    chapter_pdf: Path,
    solutions_pdf: Path,
    solution_pages: tuple[int, int],
    output_pdf: Path,
) -> None:
    """Concatenate a chapter PDF with its slice of a separate solutions PDF.

    Args:
        chapter_pdf: Already-extracted chapter PDF (body + Exercises).
        solutions_pdf: The separate solution-manual PDF.
        solution_pages: Inclusive 1-indexed page range for this chapter's solutions.
        output_pdf: Where to write the packed PDF.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        solutions_slice = Path(tmpdir) / "solutions.pdf"
        subprocess.run(
            [
                "qpdf",
                "--warning-exit-0",
                str(solutions_pdf),
                "--pages",
                ".",
                f"{solution_pages[0]}-{solution_pages[1]}",
                "--",
                str(solutions_slice),
            ],
            check=True,
        )
        output_pdf.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(
            ["pdfunite", str(chapter_pdf), str(solutions_slice), str(output_pdf)],
            check=True,
        )


def _parse_range(spec: str) -> tuple[int, int]:
    """Parse a range like '4-25' into a tuple."""
    a, b = spec.split("-")
    return int(a), int(b)


def main() -> None:
    """CLI entry point."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--chapter-pdf", required=True, type=Path)
    parser.add_argument("--solutions-pdf", required=True, type=Path)
    parser.add_argument("--solution-pages", required=True, type=_parse_range)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    pack_chapter(
        args.chapter_pdf,
        args.solutions_pdf,
        args.solution_pages,
        args.output,
    )
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
