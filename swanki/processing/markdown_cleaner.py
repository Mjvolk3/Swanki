"""Markdown cleaning module for post-processing converted markdown files.

This module cleans up markdown files after conversion from PDF, handling
LaTeX syntax conversion, reference removal, and general formatting cleanup.
"""
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import re
import logging

logger = logging.getLogger(__name__)


class MarkdownCleaner:
    """Handles markdown file cleaning and post-processing."""
    
    # Regex patterns for cleaning
    PATTERNS = {
        'subsection': (r'\\subsection{(.*?)}', r'## \1'),
        'section': (r'\\section{(.*?)}', r'## \1'),
        'section_star': (r'\\section\*{(.*?)}', r'## \1'),
        'subsection_star': (r'\\subsection\*{(.*?)}', r'### \1'),
        'inline_math_paren': (r'\\\((.*?)\\\)', r'$\1$'),
        'display_math_bracket': (r'\\\[(.*?)\\\]', r'$$\1$$'),
        'reference_citation': (r'^\[\d+\].*$', ''),  # Remove reference lines
        'latex_textbf': (r'\\textbf{(.*?)}', r'**\1**'),
        'latex_textit': (r'\\textit{(.*?)}', r'*\1*'),
        'latex_emph': (r'\\emph{(.*?)}', r'*\1*'),
    }
    
    def __init__(self, output_base: Path):
        """Initialize markdown cleaner.
        
        Args:
            output_base: Base directory for all output files
        """
        self.output_base = output_base
        self.md_singles_dir = output_base / "md-singles"
        self.clean_md_singles_dir = output_base / "clean-md-singles"
        
    def clean_all_markdown_files(self) -> List[Path]:
        """Clean all markdown files in the md-singles directory.
        
        Returns:
            List of paths to cleaned markdown files
        """
        # Create output directory
        self.clean_md_singles_dir.mkdir(parents=True, exist_ok=True)
        
        # Get all markdown files
        md_files = sorted(self.md_singles_dir.glob("*.md"))
        
        if not md_files:
            logger.warning("No markdown files found to clean")
            return []
        
        logger.info(f"Cleaning {len(md_files)} markdown files")
        
        cleaned_files = []
        for md_file in md_files:
            cleaned_file = self.clean_single_file(md_file)
            if cleaned_file:
                cleaned_files.append(cleaned_file)
        
        return cleaned_files
    
    def clean_single_file(self, md_path: Path) -> Optional[Path]:
        """Clean a single markdown file.
        
        Args:
            md_path: Path to the markdown file to clean
            
        Returns:
            Path to the cleaned markdown file, or None if cleaning failed
        """
        if not md_path.exists():
            logger.error(f"Markdown file not found: {md_path}")
            return None
        
        try:
            # Read original content
            content = md_path.read_text(encoding='utf-8')
            
            # Apply cleaning
            cleaned_content = self._apply_cleaning(content)
            
            # Write cleaned content
            output_path = self.clean_md_singles_dir / md_path.name
            output_path.write_text(cleaned_content, encoding='utf-8')
            
            logger.debug(f"Cleaned {md_path.name} -> {output_path.name}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error cleaning {md_path.name}: {e}")
            return None
    
    def _apply_cleaning(self, content: str) -> str:
        """Apply all cleaning operations to markdown content.
        
        Args:
            content: Original markdown content
            
        Returns:
            Cleaned markdown content
        """
        # Split into lines for line-by-line processing
        lines = content.split('\n')
        cleaned_lines = []
        
        in_references = False
        consecutive_empty_lines = 0
        
        for line in lines:
            # Check for references section
            if re.search(r'\\section\*?\{References\}|^#{1,3}\s*References\s*$', line, re.IGNORECASE):
                in_references = True
            
            # Skip reference citations in references section
            if in_references and re.match(r'^\[\d+\]', line.strip()):
                continue
            
            # Apply regex replacements
            cleaned_line = self._apply_regex_replacements(line)
            
            # Handle multiple empty lines
            if cleaned_line.strip() == '':
                consecutive_empty_lines += 1
                if consecutive_empty_lines <= 2:  # Allow max 2 consecutive empty lines
                    cleaned_lines.append(cleaned_line)
            else:
                consecutive_empty_lines = 0
                cleaned_lines.append(cleaned_line)
        
        # Join lines and apply final cleanup
        cleaned_content = '\n'.join(cleaned_lines)
        
        # Remove trailing whitespace
        cleaned_content = '\n'.join(line.rstrip() for line in cleaned_content.split('\n'))
        
        # Ensure file ends with single newline
        cleaned_content = cleaned_content.rstrip() + '\n'
        
        return cleaned_content
    
    def _apply_regex_replacements(self, line: str) -> str:
        """Apply regex pattern replacements to a single line.
        
        Args:
            line: Original line content
            
        Returns:
            Line with replacements applied
        """
        for pattern_name, (pattern, replacement) in self.PATTERNS.items():
            if pattern_name == 'reference_citation':
                # Special handling for full line removal
                if re.match(pattern, line.strip()):
                    return ''
            else:
                line = re.sub(pattern, replacement, line)
        
        return line
    
    def add_custom_pattern(self, name: str, pattern: str, replacement: str):
        """Add a custom cleaning pattern.
        
        Args:
            name: Name for the pattern
            pattern: Regex pattern to match
            replacement: Replacement string
        """
        self.PATTERNS[name] = (pattern, replacement)
        logger.info(f"Added custom cleaning pattern: {name}")
    
    def get_cleaning_stats(self, original: str, cleaned: str) -> Dict[str, int]:
        """Get statistics about the cleaning process.
        
        Args:
            original: Original content
            cleaned: Cleaned content
            
        Returns:
            Dictionary with cleaning statistics
        """
        return {
            'original_lines': len(original.split('\n')),
            'cleaned_lines': len(cleaned.split('\n')),
            'original_chars': len(original),
            'cleaned_chars': len(cleaned),
            'removed_chars': len(original) - len(cleaned)
        }