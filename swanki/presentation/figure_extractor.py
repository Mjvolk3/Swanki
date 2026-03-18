"""
swanki/presentation/figure_extractor.py
[[swanki.presentation.figure_extractor]]
https://github.com/Mjvolk3/swanki/tree/main/swanki/presentation/figure_extractor.py
Test file: tests/swanki/presentation/test_figure_extractor.py

Extract and crop figures from PDF pages for presentation slides.
"""

import shutil
import subprocess
from pathlib import Path

from PIL import Image

from swanki.presentation.models import FigureRef


class FigureExtractor:
    """Extract figures from PDF pages using pdftoppm and optionally crop.

    Args:
        pdf_path: Path to the source PDF file.
        output_dir: Directory to write extracted figure PNGs.
    """

    def __init__(self, pdf_path: Path, output_dir: Path) -> None:
        """Initialize with PDF path and output directory."""
        self.pdf_path = pdf_path
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def extract_figure(self, ref: FigureRef) -> Path:
        """Extract a single figure from a PDF page.

        Args:
            ref: FigureRef specifying page, crop, and label.

        Returns:
            Path to the extracted PNG file.
        """
        output_prefix = self.output_dir / f"_tmp_{ref.label}"
        subprocess.run(
            [
                "pdftoppm",
                "-png",
                "-r",
                "300",
                "-f",
                str(ref.source_page),
                "-l",
                str(ref.source_page),
                str(self.pdf_path),
                str(output_prefix),
            ],
            check=True,
            capture_output=True,
        )

        # pdftoppm names output as prefix-PAGENUMBER.png
        candidates = sorted(self.output_dir.glob(f"_tmp_{ref.label}-*.png"))
        if not candidates:
            msg = f"pdftoppm produced no output for page {ref.source_page}"
            raise FileNotFoundError(msg)
        raw_png = candidates[0]

        final_path = self.output_dir / f"{ref.label}.png"

        if ref.crop_bbox is not None:
            img = Image.open(raw_png)
            w, h = img.size
            x0, y0, x1, y1 = ref.crop_bbox
            box = (int(x0 * w), int(y0 * h), int(x1 * w), int(y1 * h))
            cropped = img.crop(box)
            cropped.save(final_path)
            raw_png.unlink()
        else:
            raw_png.rename(final_path)

        return final_path

    def extract_all(self, figures: list[FigureRef]) -> dict[str, Path]:
        """Extract all referenced figures.

        Args:
            figures: List of FigureRef objects.

        Returns:
            Mapping from label to extracted PNG path.
        """
        paths: dict[str, Path] = {}
        for ref in figures:
            paths[ref.label] = self.extract_figure(ref)
        return paths

    def copy_custom_images(self, image_paths: list[Path]) -> dict[str, Path]:
        """Copy custom images into the figures directory.

        Args:
            image_paths: Paths to custom image files.

        Returns:
            Mapping from filename stem to copied path.
        """
        paths: dict[str, Path] = {}
        for src in image_paths:
            dest = self.output_dir / src.name
            shutil.copy2(src, dest)
            paths[src.stem] = dest
        return paths
