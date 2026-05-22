"""
swanki/ocr/__init__.py
[[swanki.ocr]]
https://github.com/Mjvolk3/Swanki/tree/main/swanki/ocr/__init__.py
Test file: tests/test_ocr_dispatch.py

OCR provider dispatch (mathpix | mineru) returning per-page markdown paths.
"""

from pathlib import Path
from typing import Any

from swanki.ocr.mathpix import convert_pages_mathpix
from swanki.ocr.mineru import convert_pdf_mineru

__all__ = ["convert_to_markdown", "convert_pages_mathpix", "convert_pdf_mineru"]


def convert_to_markdown(
    provider: str,
    *,
    pages: list[Path],
    pdf_path: Path | None,
    output_base: Path,
    ocr_config: dict[str, Any],
) -> list[Path]:
    """Dispatch OCR to the configured provider, returning per-page markdown paths.

    Args:
        provider: "mathpix" or "mineru".
        pages: Per-page split PDFs (consumed by mathpix; ignored by mineru).
        pdf_path: Original source PDF (consumed by mineru; ignored by mathpix).
        output_base: Pipeline output directory; md-singles/ is written under it.
        ocr_config: The models.ocr config subtree.

    Returns:
        Sorted list of per-page markdown file paths (md-singles/page-N.md).

    Raises:
        ValueError: If provider is not "mathpix" or "mineru".
    """
    if provider == "mathpix":
        return convert_pages_mathpix(pages, output_base)
    if provider == "mineru":
        return convert_pdf_mineru(pdf_path, output_base, ocr_config)
    raise ValueError(f"Unknown OCR provider {provider!r}; use 'mathpix' or 'mineru'")
