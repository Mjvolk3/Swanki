"""PDF processing module for splitting PDFs into individual pages.

This module provides functionality to split multi-page PDF documents into
individual single-page PDF files, which is the first step in the Swanki
processing pipeline. The split pages are then converted to markdown for
further processing.

Classes
-------
PDFProcessor
    Handles PDF splitting and page extraction operations

Examples
--------
>>> from swanki.processing import PDFProcessor
>>> from pathlib import Path
>>> 
>>> processor = PDFProcessor(output_base=Path("output"))
>>> pages = processor.split_pdf(Path("paper.pdf"))
>>> print(f"Split into {len(pages)} pages")
Split into 10 pages
"""
from pathlib import Path
from typing import List, Optional
import logging
import shutil
import subprocess
from PyPDF2 import PdfReader, PdfWriter

logger = logging.getLogger(__name__)


class PDFProcessor:
    """Handles PDF splitting and page extraction operations.
    
    Provides methods to split multi-page PDFs into individual pages,
    extract specific pages, and query PDF metadata. All output files
    are organized in a dedicated directory structure.
    
    Parameters
    ----------
    output_base : Path
        Base directory for all output files
    
    Attributes
    ----------
    output_base : Path
        Base output directory
    pdf_singles_dir : Path
        Directory for single-page PDFs (output_base/pdf-singles)
    
    Methods
    -------
    split_pdf(pdf_path)
        Split PDF into individual page files
    get_page_count(pdf_path)
        Get number of pages in a PDF
    extract_page(pdf_path, page_number)
        Extract a specific page from a PDF
    
    Examples
    --------
    >>> processor = PDFProcessor(Path("./output"))
    >>> 
    >>> # Split entire PDF
    >>> pages = processor.split_pdf(Path("document.pdf"))
    >>> 
    >>> # Get page count
    >>> count = processor.get_page_count(Path("document.pdf"))
    >>> 
    >>> # Extract specific page
    >>> page_5 = processor.extract_page(Path("document.pdf"), 5)
    """
    
    def __init__(self, output_base: Path):
        """Initialize PDF processor with output directory.
        
        Parameters
        ----------
        output_base : Path
            Base directory for all output files. A 'pdf-singles'
            subdirectory will be created here for output.
        """
        self.output_base = output_base
        self.pdf_singles_dir = output_base / "pdf-singles"
        
    def split_pdf(self, pdf_path: Path) -> List[Path]:
        """Split a PDF into individual page files.
        
        Creates one PDF file per page from the input document. Files are
        named 'page-1.pdf', 'page-2.pdf', etc. and stored in the
        pdf-singles directory.
        
        Parameters
        ----------
        pdf_path : Path
            Path to the input PDF file
        
        Returns
        -------
        List[Path]
            List of paths to the created single-page PDF files,
            ordered by page number
        
        Raises
        ------
        FileNotFoundError
            If input PDF doesn't exist
        ValueError
            If PDF is empty, corrupted, or processing fails
        
        Examples
        --------
        >>> processor = PDFProcessor(Path("output"))
        >>> pages = processor.split_pdf(Path("research.pdf"))
        >>> print(pages[0])
        output/pdf-singles/page-1.pdf
        
        Notes
        -----
        The output directory is created if it doesn't exist.
        Existing files with the same names will be overwritten.
        """
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        # Create output directory
        self.pdf_singles_dir.mkdir(parents=True, exist_ok=True)
        
        try:
            reader = PdfReader(pdf_path)
            num_pages = len(reader.pages)

            if num_pages == 0:
                raise ValueError(f"PDF has no pages: {pdf_path}")

            logger.info(f"Splitting PDF with {num_pages} pages: {pdf_path.name}")

            output_files = []

            for page_num, page in enumerate(reader.pages, start=1):
                writer = PdfWriter()
                writer.add_page(page)

                output_path = self.pdf_singles_dir / f"page-{page_num}.pdf"

                with open(output_path, "wb") as output_file:
                    writer.write(output_file)

                output_files.append(output_path)
                logger.debug(f"Created page {page_num}/{num_pages}: {output_path.name}")

            logger.info(f"Successfully split PDF into {len(output_files)} pages")
            return output_files

        except Exception as e:
            logger.warning(f"PyPDF2 failed: {e}. Falling back to qpdf.")
            return self._split_pdf_qpdf(pdf_path)
    
    def _split_pdf_qpdf(self, pdf_path: Path) -> List[Path]:
        """Split PDF using qpdf as a fallback for malformed PDFs."""
        if not shutil.which("qpdf"):
            raise ValueError("qpdf is not installed; cannot split malformed PDF")

        reader = PdfReader(pdf_path)
        num_pages = len(reader.pages)
        self.pdf_singles_dir.mkdir(parents=True, exist_ok=True)

        output_files = []
        for page_num in range(1, num_pages + 1):
            output_path = self.pdf_singles_dir / f"page-{page_num}.pdf"
            result = subprocess.run(
                ["qpdf", str(pdf_path), "--pages", ".", str(page_num), "--", str(output_path)],
            )
            # qpdf exit 0=success, 3=warnings (ok). Anything else is a real error.
            if result.returncode not in (0, 3):
                raise ValueError(f"qpdf failed on page {page_num} with exit code {result.returncode}")
            output_files.append(output_path)
            logger.debug(f"Created page {page_num}/{num_pages} via qpdf: {output_path.name}")

        logger.info(f"Successfully split PDF into {len(output_files)} pages via qpdf")
        return output_files

    def get_page_count(self, pdf_path: Path) -> int:
        """Get the number of pages in a PDF.
        
        Parameters
        ----------
        pdf_path : Path
            Path to the PDF file
        
        Returns
        -------
        int
            Number of pages in the PDF
        
        Examples
        --------
        >>> processor = PDFProcessor(Path("output"))
        >>> count = processor.get_page_count(Path("paper.pdf"))
        >>> print(f"PDF has {count} pages")
        PDF has 25 pages
        """
        reader = PdfReader(pdf_path)
        return len(reader.pages)
    
    def extract_page(self, pdf_path: Path, page_number: int) -> Optional[Path]:
        """Extract a specific page from a PDF.
        
        Extracts a single page and saves it as a separate PDF file.
        Useful for re-processing specific pages.
        
        Parameters
        ----------
        pdf_path : Path
            Path to the input PDF
        page_number : int
            Page number to extract (1-based indexing)
        
        Returns
        -------
        Path or None
            Path to the extracted page PDF if successful,
            None if page number is out of range
        
        Examples
        --------
        >>> processor = PDFProcessor(Path("output"))
        >>> # Extract page 5
        >>> page_path = processor.extract_page(Path("doc.pdf"), 5)
        >>> if page_path:
        ...     print(f"Extracted: {page_path}")
        ... else:
        ...     print("Page does not exist")
        
        Notes
        -----
        Page numbering starts at 1, not 0. The output file
        will be named 'page-{page_number}.pdf'.
        """
        reader = PdfReader(pdf_path)
        
        if page_number < 1 or page_number > len(reader.pages):
            logger.warning(f"Page {page_number} does not exist in PDF")
            return None
        
        writer = PdfWriter()
        writer.add_page(reader.pages[page_number - 1])
        
        output_path = self.pdf_singles_dir / f"page-{page_number}.pdf"
        
        with open(output_path, "wb") as output_file:
            writer.write(output_file)
        
        return output_path