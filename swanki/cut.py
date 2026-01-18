"""PDF cutting utility with Pythonic (0-based, end-exclusive) indexing.

This tool extracts a range of pages from a PDF file using Python's standard
slicing convention: start is inclusive, end is exclusive.

Examples:
    # Extract pages 0, 1, 2 (first 3 pages)
    swanki-cut -s 0 -e 3 input.pdf output.pdf
    
    # Extract pages 5 through 9 (5 pages total)
    swanki-cut -s 5 -e 10 input.pdf output.pdf
    
    # Extract just page 0 (first page)
    swanki-cut -s 0 -e 1 input.pdf output.pdf
"""
import argparse
import sys
import warnings
import subprocess
import tempfile
from pathlib import Path
from PyPDF2 import PdfReader, PdfWriter


def repair_pdf_with_qpdf(input_path: Path) -> Path:
    """Repair a corrupted PDF using qpdf.

    Args:
        input_path: Path to the corrupted PDF

    Returns:
        Path to the repaired PDF (in temp directory)
    """
    temp_dir = Path(tempfile.gettempdir())
    repaired_path = temp_dir / f"repaired_{input_path.name}"

    result = subprocess.run(
        ["qpdf", str(input_path), str(repaired_path)],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise RuntimeError(f"qpdf repair failed: {result.stderr}")

    return repaired_path


def cut_pdf(start: int, end: int, input_path: Path, output_path: Path) -> None:
    """Cut a PDF file using Pythonic indexing (0-based, end-exclusive).

    Args:
        start: Starting page index (0-based, inclusive)
        end: Ending page index (0-based, exclusive)
        input_path: Path to input PDF
        output_path: Path to output PDF

    Raises:
        FileNotFoundError: If input file doesn't exist
        ValueError: If page indices are invalid
    """
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    repaired_path = None
    try:
        # Try to process the PDF normally
        _do_cut_pdf(start, end, input_path, output_path)
    except (AssertionError, RuntimeError) as e:
        # PDF is corrupted, try repairing with qpdf
        print("PDF appears corrupted, attempting repair with qpdf...")
        repaired_path = repair_pdf_with_qpdf(input_path)
        _do_cut_pdf(start, end, repaired_path, output_path)
    finally:
        # Clean up temp file
        if repaired_path and repaired_path.exists():
            repaired_path.unlink()

    pages_extracted = end - start
    print(f"✓ Extracted {pages_extracted} pages [{start}:{end}] from {input_path.name}")
    print(f"  Saved to: {output_path}")


def _do_cut_pdf(start: int, end: int, input_path: Path, output_path: Path) -> None:
    """Internal function to perform the actual PDF cutting."""
    # Suppress PyPDF2 warnings about malformed PDFs
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore")
        reader = PdfReader(input_path, strict=False)
        total_pages = len(reader.pages)

        # Validate indices
        if start < 0:
            raise ValueError(f"Start index must be >= 0, got {start}")
        if end > total_pages:
            raise ValueError(f"End index must be <= {total_pages} (total pages), got {end}")
        if start >= end:
            raise ValueError(f"Start index must be < end index, got start={start}, end={end}")

        writer = PdfWriter()

        # Extract pages [start:end] (Pythonic slicing)
        for i in range(start, end):
            writer.add_page(reader.pages[i])

        # Write output
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)


def main():
    """Command-line interface for PDF cutting tool."""
    parser = argparse.ArgumentParser(
        description="Cut a PDF using Pythonic indexing (0-based, end-exclusive)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Extract first 5 pages (pages 0-4)
  swanki-cut -s 0 -e 5 paper.pdf chapter1.pdf
  
  # Extract pages 10-14 (5 pages)
  swanki-cut -s 10 -e 15 paper.pdf chapter2.pdf
  
  # Show PDF info without cutting
  swanki-cut --info paper.pdf

Note: This uses Python's slicing convention where:
  - Indices are 0-based (first page is 0)
  - End index is EXCLUSIVE (not included)
  - This matches Python's list[start:end] behavior
        """
    )
    
    parser.add_argument('-s', '--start', type=int, help="Start page index (0-based, inclusive)")
    parser.add_argument('-e', '--end', type=int, help="End page index (0-based, exclusive)")
    parser.add_argument('--info', action='store_true', help="Show PDF info and exit")
    parser.add_argument('input', type=str, help="Input PDF file path")
    parser.add_argument('output', type=str, nargs='?', help="Output PDF file path")
    
    args = parser.parse_args()
    
    input_path = Path(args.input)
    
    # Check if input exists
    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}", file=sys.stderr)
        return 1
    
    # Info mode - just show PDF details
    if args.info:
        try:
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore")
                reader = PdfReader(input_path, strict=False)
                total_pages = len(reader.pages)
            print(f"PDF Info: {input_path.name}")
            print(f"  Total pages: {total_pages}")
            print(f"  Valid indices: 0 to {total_pages-1}")
            print(f"  Example: -s 0 -e {total_pages} (extract all pages)")
            return 0
        except Exception as e:
            print(f"Error reading PDF: {e}", file=sys.stderr)
            return 1
    
    # Normal cut mode - require all arguments
    if args.start is None or args.end is None:
        print("Error: Both --start and --end are required for cutting", file=sys.stderr)
        parser.print_help()
        return 1
    
    if not args.output:
        print("Error: Output file path is required for cutting", file=sys.stderr)
        parser.print_help()
        return 1
    
    output_path = Path(args.output)
    
    try:
        cut_pdf(args.start, args.end, input_path, output_path)
        return 0
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())