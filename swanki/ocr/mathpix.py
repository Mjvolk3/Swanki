"""
swanki/ocr/mathpix.py
[[swanki.ocr.mathpix]]
https://github.com/Mjvolk3/Swanki/tree/main/swanki/ocr/mathpix.py
Test file: tests/test_ocr_mathpix.py

Mathpix per-page OCR via the mpx CLI, producing md-singles/page-N.md.
"""

import logging
import subprocess
from pathlib import Path

from swanki.processing.markdown_cleaner import _natural_sort_key

logger = logging.getLogger(__name__)


def convert_pages_mathpix(pages: list[Path], output_base: Path) -> list[Path]:
    """Convert per-page PDFs to markdown with the Mathpix CLI.

    Args:
        pages: Single-page PDF files (output_base/pdf-singles/page-N.pdf).
        output_base: Pipeline output directory; writes to output_base/md-singles.

    Returns:
        Naturally-sorted list of generated page markdown paths.

    Raises:
        RuntimeError: If no pages could be converted.
    """
    md_singles_dir = output_base / "md-singles"
    md_singles_dir.mkdir(parents=True, exist_ok=True)

    markdown_files: list[Path] = []
    logger.info(f"Converting {len(pages)} PDF pages to markdown (mathpix)")

    for page_pdf in pages:
        md_path = md_singles_dir / (page_pdf.stem + ".md")
        # mpx calls process.stdout.clearLine(), which crashes without a TTY;
        # wrap with `script -qc` to provide a pseudo-TTY and capture stderr.
        cmd = f"mpx convert '{page_pdf}' '{md_path}'"
        proc = subprocess.run(
            ["script", "-qc", cmd, "/dev/null"],
            capture_output=True,
            text=True,
            timeout=300,
        )
        if proc.returncode == 0 and md_path.exists() and md_path.stat().st_size > 0:
            logger.debug(f"Converted {page_pdf.name}")
            markdown_files.append(md_path)
        else:
            logger.warning(
                f"Failed to convert {page_pdf.name} (exit {proc.returncode}): "
                f"{proc.stderr[-500:]}"
            )

    if not markdown_files:
        raise RuntimeError("Failed to convert any PDF pages to markdown.")

    logger.info(f"Successfully converted {len(markdown_files)} pages to markdown")
    return sorted(markdown_files, key=_natural_sort_key)
