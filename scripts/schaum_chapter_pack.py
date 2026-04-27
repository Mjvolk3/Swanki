"""
scripts/schaum_chapter_pack.py
[[scripts.schaum_chapter_pack]]
https://github.com/Mjvolk3/Swanki/tree/main/scripts/schaum_chapter_pack.py

Preprocess a Schaum's-style book by chopping one chapter's pages and the
specific back-of-book pages that contain THAT chapter's answer key, then
concatenating into a single PDF for solution_manual mode.

The --answer-key-pages range should be the SMALLEST range covering this
chapter's answers, NOT the entire back-of-book region. Other chapters' answers
that happen to share the same page are tolerated (the regex pairer keys on
`^Chapter N` and ignores other-chapter blocks), but including many extra pages
inflates OCR cost and bloats the LLM context window for no benefit.

For Schaum's Microbiology (Alcamo, 2nd ed.), answers per chapter fit on a
fraction of a single page; pass `--answer-key-pages 328-328` for Ch1, etc.

Usage:
    python scripts/schaum_chapter_pack.py \\
        --source /scratch/alcamoSchaumsOutlineMicrobiology2010_clean.pdf \\
        --chapter-pages 8-18 \\
        --answer-key-pages 328-328 \\
        --output /scratch/alcamo_CH01_packed.pdf
"""

import argparse
import subprocess
import tempfile
from pathlib import Path


def pack_chapter(
    source_pdf: Path,
    chapter_pages: tuple[int, int],
    answer_key_pages: tuple[int, int],
    output_pdf: Path,
) -> None:
    """Chop chapter pages and answer-key region, concatenate into one PDF.

    Args:
        source_pdf: Path to the cleaned source PDF.
        chapter_pages: Inclusive PDF page range for the chapter.
        answer_key_pages: Inclusive PDF page range for the back-of-book answer key.
        output_pdf: Where to write the packed PDF.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        chapter_pdf = Path(tmpdir) / "chapter.pdf"
        answers_pdf = Path(tmpdir) / "answers.pdf"
        subprocess.run(
            [
                "qpdf",
                "--warning-exit-0",
                str(source_pdf),
                "--pages",
                ".",
                f"{chapter_pages[0]}-{chapter_pages[1]}",
                "--",
                str(chapter_pdf),
            ],
            check=True,
        )
        subprocess.run(
            [
                "qpdf",
                "--warning-exit-0",
                str(source_pdf),
                "--pages",
                ".",
                f"{answer_key_pages[0]}-{answer_key_pages[1]}",
                "--",
                str(answers_pdf),
            ],
            check=True,
        )
        subprocess.run(
            ["pdfunite", str(chapter_pdf), str(answers_pdf), str(output_pdf)],
            check=True,
        )


def _parse_range(spec: str) -> tuple[int, int]:
    """Parse a range like '8-18' into a tuple."""
    a, b = spec.split("-")
    return int(a), int(b)


def main() -> None:
    """CLI entry point."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--chapter-pages", required=True, type=_parse_range)
    parser.add_argument("--answer-key-pages", required=True, type=_parse_range)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    pack_chapter(
        args.source, args.chapter_pages, args.answer_key_pages, args.output
    )
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
