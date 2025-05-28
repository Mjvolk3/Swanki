"""Markdown conversion module for converting PDFs to markdown using Mathpix.

This module handles the conversion of PDF pages to markdown format using
the Mathpix OCR service, which is especially good at handling mathematical
content and complex layouts. Supports parallel processing for efficiency.

Classes
-------
MarkdownConverter
    Handles PDF to Markdown conversion using Mathpix CLI

Examples
--------
>>> from swanki.processing import MarkdownConverter
>>> from pathlib import Path
>>> 
>>> converter = MarkdownConverter(output_base=Path("output"))
>>> markdown_files = converter.convert_all_pdfs()
>>> print(f"Converted {len(markdown_files)} files")
Converted 10 files

Notes
-----
Requires Mathpix CLI (mpx) to be installed and configured.
See https://mathpix.com/docs/ocr/cli for installation instructions.
"""
from pathlib import Path
from typing import List, Optional, Dict, Any
import subprocess
import logging
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

logger = logging.getLogger(__name__)


class MarkdownConverter:
    """Handles PDF to Markdown conversion using Mathpix CLI.
    
    Converts PDF files to markdown format with special handling for
    mathematical content, tables, and complex layouts. Supports both
    single file and batch conversion with parallel processing.
    
    Parameters
    ----------
    output_base : Path
        Base directory for all output files
    max_workers : int, optional
        Maximum number of parallel conversion workers (default is 4)
    
    Attributes
    ----------
    output_base : Path
        Base output directory
    pdf_singles_dir : Path
        Directory containing single-page PDFs
    md_singles_dir : Path
        Directory for markdown output files
    max_workers : int
        Number of parallel workers
    
    Methods
    -------
    convert_all_pdfs()
        Convert all PDFs in pdf-singles directory
    convert_single_pdf(pdf_path)
        Convert a specific PDF file
    get_conversion_options()
        Get current Mathpix conversion options
    
    Examples
    --------
    >>> converter = MarkdownConverter(Path("output"), max_workers=8)
    >>> 
    >>> # Convert all PDFs
    >>> all_files = converter.convert_all_pdfs()
    >>> 
    >>> # Convert single file
    >>> single = converter.convert_single_pdf(Path("page-1.pdf"))
    """
    
    def __init__(self, output_base: Path, max_workers: int = 4):
        """Initialize markdown converter.
        
        Parameters
        ----------
        output_base : Path
            Base directory for all output files. Expects 'pdf-singles'
            subdirectory to exist with PDF files to convert.
        max_workers : int, optional
            Maximum number of parallel conversion workers (default is 4).
            Higher values can speed up batch conversion.
        """
        self.output_base = output_base
        self.pdf_singles_dir = output_base / "pdf-singles"
        self.md_singles_dir = output_base / "md-singles"
        self.max_workers = max_workers
        
    def convert_all_pdfs(self) -> List[Path]:
        """Convert all PDF files in pdf-singles directory to markdown.
        
        Processes all 'page-*.pdf' files found in the pdf-singles directory,
        converting them to markdown format in parallel. Output files are
        saved to the md-singles directory.
        
        Returns
        -------
        List[Path]
            List of paths to successfully created markdown files,
            sorted by filename
        
        Raises
        ------
        RuntimeError
            If Mathpix CLI (mpx) is not available or not configured
        
        Examples
        --------
        >>> converter = MarkdownConverter(Path("output"))
        >>> files = converter.convert_all_pdfs()
        >>> for f in files:
        ...     print(f.name)
        page-1.md
        page-2.md
        page-3.md
        
        Notes
        -----
        Failed conversions are logged but don't stop the batch process.
        The method will return successfully converted files only.
        """
        # Check if mpx-cli is available
        if not self._check_mathpix_cli():
            raise RuntimeError("Mathpix CLI (mpx) not found. Please install it first.")
        
        # Create output directory
        self.md_singles_dir.mkdir(parents=True, exist_ok=True)
        
        # Get all PDF files
        pdf_files = sorted(self.pdf_singles_dir.glob("page-*.pdf"))
        
        if not pdf_files:
            logger.warning("No PDF files found to convert")
            return []
        
        logger.info(f"Converting {len(pdf_files)} PDF files to markdown")
        
        # Convert files in parallel
        markdown_files = []
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_pdf = {
                executor.submit(self._convert_single_pdf, pdf_file): pdf_file
                for pdf_file in pdf_files
            }
            
            for future in as_completed(future_to_pdf):
                pdf_file = future_to_pdf[future]
                try:
                    md_file = future.result()
                    if md_file:
                        markdown_files.append(md_file)
                except Exception as e:
                    logger.error(f"Failed to convert {pdf_file.name}: {e}")
        
        return sorted(markdown_files)
    
    def convert_single_pdf(self, pdf_path: Path) -> Optional[Path]:
        """Convert a single PDF file to markdown.
        
        Parameters
        ----------
        pdf_path : Path
            Path to the PDF file to convert
        
        Returns
        -------
        Path or None
            Path to the created markdown file if successful,
            None if conversion failed
        
        Examples
        --------
        >>> converter = MarkdownConverter(Path("output"))
        >>> md_file = converter.convert_single_pdf(Path("page.pdf"))
        >>> if md_file:
        ...     print(f"Created: {md_file}")
        ... else:
        ...     print("Conversion failed")
        """
        return self._convert_single_pdf(pdf_path)
    
    def _convert_single_pdf(self, pdf_path: Path) -> Optional[Path]:
        """Internal method to convert a single PDF to markdown.
        
        Parameters
        ----------
        pdf_path : Path
            Path to the PDF file
        
        Returns
        -------
        Path or None
            Path to created markdown file, or None if failed
        
        Notes
        -----
        Uses shell=True for proper PATH resolution and suppresses
        stderr to avoid clearLine error messages from mpx CLI.
        """
        if not pdf_path.exists():
            logger.error(f"PDF file not found: {pdf_path}")
            return None
        
        # Create output path
        md_filename = pdf_path.stem + ".md"
        md_path = self.md_singles_dir / md_filename
        
        # Simple approach - just run the command like you would from CLI
        cmd = f"mpx convert '{pdf_path}' '{md_path}'"
        
        try:
            # Use subprocess.run with shell=True to execute exactly as CLI would
            # Redirect stderr to devnull to avoid the clearLine error spam
            result = subprocess.run(
                cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,  # Suppress the clearLine errors
                text=True,
                timeout=60
            )
            
            # Check if the file was created successfully
            if md_path.exists():
                logger.debug(f"Converted {pdf_path.name} -> {md_path.name}")
                return md_path
            else:
                # If no file created, log any stdout that might have info
                if result.stdout:
                    logger.error(f"Conversion failed for {pdf_path.name}: {result.stdout}")
                else:
                    logger.error(f"Conversion failed for {pdf_path.name}: No output file created")
                return None
                
        except subprocess.TimeoutExpired:
            logger.error(f"Conversion timeout for {pdf_path.name}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error converting {pdf_path.name}: {e}")
            return None
    
    def _check_mathpix_cli(self) -> bool:
        """Check if Mathpix CLI is available.
        
        Returns
        -------
        bool
            True if mpx command is available, False otherwise
        
        Notes
        -----
        Checks for 'mpx --version' command availability.
        Does not verify API credentials.
        """
        try:
            # Use shell=True to ensure PATH is properly resolved
            result = subprocess.run(
                "mpx --version",
                shell=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            return result.returncode == 0
        except Exception:
            return False
    
    def get_conversion_options(self) -> Dict[str, Any]:
        """Get current Mathpix conversion options.
        
        Returns
        -------
        Dict[str, Any]
            Dictionary of conversion options including:
            - math_inline_delimiters: Delimiters for inline math
            - math_display_delimiters: Delimiters for display math
            - formats: Output formats to generate
            - ocr: Whether to use OCR
            - enable_tables: Whether to detect tables
        
        Examples
        --------
        >>> converter = MarkdownConverter(Path("output"))
        >>> options = converter.get_conversion_options()
        >>> print(options['math_inline_delimiters'])
        ['$', '$']
        
        Notes
        -----
        These options could be made configurable via the
        constructor in future versions.
        """
        # These could be made configurable in the future
        return {
            "math_inline_delimiters": ["$", "$"],
            "math_display_delimiters": ["$$", "$$"],
            "formats": ["text", "latex", "mathml"],
            "ocr": True,
            "enable_tables": True
        }