"""PDF processing module for splitting PDFs into individual pages.

This module provides functionality to split multi-page PDF documents into
individual single-page PDF files, which is the first step in the Swanki
processing pipeline.
"""
from pathlib import Path
from typing import List, Optional
import logging
from PyPDF2 import PdfReader, PdfWriter

logger = logging.getLogger(__name__)


class PDFProcessor:
    """Handles PDF splitting and page extraction operations."""
    
    def __init__(self, output_base: Path):
        """Initialize PDF processor with output directory.
        
        Args:
            output_base: Base directory for all output files
        """
        self.output_base = output_base
        self.pdf_singles_dir = output_base / "pdf-singles"
        
    def split_pdf(self, pdf_path: Path) -> List[Path]:
        """Split a PDF into individual page files.
        
        Args:
            pdf_path: Path to the input PDF file
            
        Returns:
            List of paths to the created single-page PDF files
            
        Raises:
            FileNotFoundError: If input PDF doesn't exist
            ValueError: If PDF is empty or corrupted
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
                # Create writer for single page
                writer = PdfWriter()
                writer.add_page(page)
                
                # Generate output filename
                output_path = self.pdf_singles_dir / f"page-{page_num}.pdf"
                
                # Write single page PDF
                with open(output_path, "wb") as output_file:
                    writer.write(output_file)
                
                output_files.append(output_path)
                logger.debug(f"Created page {page_num}/{num_pages}: {output_path.name}")
            
            logger.info(f"Successfully split PDF into {len(output_files)} pages")
            return output_files
            
        except Exception as e:
            logger.error(f"Error splitting PDF: {e}")
            raise ValueError(f"Failed to process PDF: {e}")
    
    def get_page_count(self, pdf_path: Path) -> int:
        """Get the number of pages in a PDF.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Number of pages in the PDF
        """
        reader = PdfReader(pdf_path)
        return len(reader.pages)
    
    def extract_page(self, pdf_path: Path, page_number: int) -> Optional[Path]:
        """Extract a specific page from a PDF.
        
        Args:
            pdf_path: Path to the input PDF
            page_number: Page number to extract (1-based)
            
        Returns:
            Path to the extracted page PDF, or None if page doesn't exist
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