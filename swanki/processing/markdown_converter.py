"""Markdown conversion module for converting PDFs to markdown using Mathpix.

This module handles the conversion of PDF pages to markdown format using
the Mathpix OCR service, which is especially good at handling mathematical
content and complex layouts.
"""
from pathlib import Path
from typing import List, Optional, Dict, Any
import subprocess
import logging
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

logger = logging.getLogger(__name__)


class MarkdownConverter:
    """Handles PDF to Markdown conversion using Mathpix CLI."""
    
    def __init__(self, output_base: Path, max_workers: int = 4):
        """Initialize markdown converter.
        
        Args:
            output_base: Base directory for all output files
            max_workers: Maximum number of parallel conversion workers
        """
        self.output_base = output_base
        self.pdf_singles_dir = output_base / "pdf-singles"
        self.md_singles_dir = output_base / "md-singles"
        self.max_workers = max_workers
        
    def convert_all_pdfs(self) -> List[Path]:
        """Convert all PDF files in pdf-singles directory to markdown.
        
        Returns:
            List of paths to created markdown files
            
        Raises:
            RuntimeError: If Mathpix CLI is not available
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
        
        Args:
            pdf_path: Path to the PDF file to convert
            
        Returns:
            Path to the created markdown file, or None if conversion failed
        """
        return self._convert_single_pdf(pdf_path)
    
    def _convert_single_pdf(self, pdf_path: Path) -> Optional[Path]:
        """Internal method to convert a single PDF to markdown.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Path to created markdown file, or None if failed
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
        
        Returns:
            True if mpx command is available, False otherwise
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
        
        Returns:
            Dictionary of conversion options
        """
        # These could be made configurable in the future
        return {
            "math_inline_delimiters": ["$", "$"],
            "math_display_delimiters": ["$$", "$$"],
            "formats": ["text", "latex", "mathml"],
            "ocr": True,
            "enable_tables": True
        }