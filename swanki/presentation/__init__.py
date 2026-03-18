"""
swanki/presentation/__init__.py
[[swanki.presentation.__init__]]
https://github.com/Mjvolk3/swanki/tree/main/swanki/presentation/__init__.py
Test file: tests/swanki/presentation/test___init__.py

Generate Reveal.js presentations from Swanki-processed paper data.
"""

import argparse
import os
import sys
from pathlib import Path

from swanki.presentation.figure_extractor import FigureExtractor
from swanki.presentation.models import PresentationSpec
from swanki.presentation.renderer import PresentationRenderer
from swanki.presentation.slide_generator import SlideGenerator


def _find_latest_version(data_dir: Path) -> Path:
    """Find the latest numbered version directory.

    Args:
        data_dir: Base data directory for a citation key.

    Returns:
        Path to the latest versioned subdirectory.
    """
    key = data_dir.name
    versions = sorted(
        [
            d
            for d in data_dir.iterdir()
            if d.is_dir() and d.name.startswith(key) and d.name != key
        ],
        key=lambda p: p.name,
    )
    if not versions:
        # Fall back to the base directory itself if it has expected subdirs
        if (data_dir / key).is_dir():
            return data_dir / key
        return data_dir
    return versions[-1]


def _load_doc_summary(version_dir: Path) -> str:
    """Load document-summary.md content."""
    summary_path = version_dir / "document-summary.md"
    if summary_path.exists():
        return summary_path.read_text(encoding="utf-8")
    return ""


def _load_image_summaries(version_dir: Path) -> dict[str, str]:
    """Load image summary files into a dict keyed by filename stem."""
    summaries: dict[str, str] = {}
    img_dir = version_dir / "image-summaries"
    if img_dir.is_dir():
        for md_file in sorted(img_dir.glob("page-*_*.md")):
            if "_with_summaries" not in md_file.name:
                summaries[md_file.stem] = md_file.read_text(encoding="utf-8")
    return summaries


def _find_pdf(data_dir: Path, citation_key: str) -> Path:
    """Find the clean or original PDF for figure extraction."""
    clean = data_dir / f"{citation_key}_clean.pdf"
    if clean.exists():
        return clean
    original = data_dir / f"{citation_key}.pdf"
    if original.exists():
        return original
    msg = f"No PDF found in {data_dir} for {citation_key}"
    raise FileNotFoundError(msg)


def run(
    citation_key: str,
    instructions: str = "",
    slides_min: int = 10,
    slides_max: int = 14,
    custom_images: list[Path] | None = None,
    data_dir: Path | None = None,
    version: int | None = None,
    model: str = "gpt-4o",
) -> Path:
    """Generate a presentation end-to-end.

    Args:
        citation_key: Zotero citation key.
        instructions: Free-text instructions for the LLM.
        slides_min: Minimum number of slides.
        slides_max: Maximum number of slides.
        custom_images: Paths to additional images to include.
        data_dir: Override for SWANKI_DATA directory.
        version: Specific version number to use.
        model: LLM model name.

    Returns:
        Path to the generated presentation.html.
    """
    if data_dir is None:
        swanki_data = Path(os.getenv("SWANKI_DATA", "../Swanki_Data"))
        data_dir = swanki_data / citation_key

    if not data_dir.exists():
        msg = f"Data directory not found: {data_dir}"
        raise FileNotFoundError(msg)

    # Find version directory
    if version is not None:
        version_dir = data_dir / f"{citation_key}_{version}"
    else:
        version_dir = _find_latest_version(data_dir)

    print(f"Using data from: {version_dir}")

    # Load paper data
    doc_summary = _load_doc_summary(version_dir)
    image_summaries = _load_image_summaries(version_dir)

    # Find PDF for figure extraction
    pdf_path = _find_pdf(data_dir, citation_key)
    print(f"Using PDF: {pdf_path}")

    # Output directory
    output_dir = data_dir / "presentation"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Build spec
    spec = PresentationSpec(
        citation_key=citation_key,
        instructions=instructions,
        slide_count_min=slides_min,
        slide_count_max=slides_max,
        custom_images=custom_images or [],
    )

    # Generate slide structure via LLM
    print(f"Generating {slides_min}-{slides_max} slides with {model}...")
    generator = SlideGenerator(model=model)
    presentation = generator.generate(spec, doc_summary, image_summaries)
    print(f"Generated {len(presentation.slides)} slides")

    # Collect all figure refs across slides
    all_figures = []
    for slide in presentation.slides:
        all_figures.extend(slide.figures)

    # Extract figures from PDF
    figures_dir = output_dir / "figures"
    extractor = FigureExtractor(pdf_path, figures_dir)
    figure_paths = extractor.extract_all(all_figures)
    print(f"Extracted {len(figure_paths)} figures")

    # Copy custom images
    if spec.custom_images:
        custom_paths = extractor.copy_custom_images(spec.custom_images)
        figure_paths.update(custom_paths)

    # Render to HTML
    renderer = PresentationRenderer(output_dir)
    html_path = renderer.render(presentation, figure_paths)
    print(f"Presentation saved to: {html_path}")

    return html_path


def main() -> int:
    """CLI entry point for swanki-present."""
    parser = argparse.ArgumentParser(
        description="Generate Reveal.js presentation from Swanki paper data",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Examples:
  swanki-present merzbacherAccuratePredictionGene2025 \\
    -i "12 slides, include all main figures"

  swanki-present smithDeepLearning2024 \\
    --slides-min 8 --slides-max 10 \\
    --data-dir ../Swanki_Data/smithDeepLearning2024
""",
    )
    parser.add_argument("citation_key", help="Zotero citation key")
    parser.add_argument(
        "-i", "--instructions", default="", help="Custom instructions for the LLM"
    )
    parser.add_argument("--slides-min", type=int, default=10, help="Min slides")
    parser.add_argument("--slides-max", type=int, default=14, help="Max slides")
    parser.add_argument(
        "--custom-images", nargs="*", type=Path, default=[], help="Extra images"
    )
    parser.add_argument(
        "--data-dir", type=Path, default=None, help="Override SWANKI_DATA path"
    )
    parser.add_argument(
        "--version", type=int, default=None, help="Version number to use"
    )
    parser.add_argument("--model", default="gpt-4o", help="LLM model (default: gpt-4o)")

    args = parser.parse_args()

    html_path = run(
        citation_key=args.citation_key,
        instructions=args.instructions,
        slides_min=args.slides_min,
        slides_max=args.slides_max,
        custom_images=args.custom_images,
        data_dir=args.data_dir,
        version=args.version,
        model=args.model,
    )
    print(f"\nOpen in browser: file://{html_path.resolve()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
