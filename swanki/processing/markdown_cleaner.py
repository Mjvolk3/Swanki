# swanki/processing/markdown_cleaner
# [[swanki.processing.markdown_cleaner]]
# https://github.com/Mjvolk3/swanki/tree/main/swanki/processing/markdown_cleaner
# Test file: tests/swanki/processing/test_markdown_cleaner.py

"""Markdown cleaning module for post-processing converted markdown files.

This module cleans up markdown files after conversion from PDF, handling
LaTeX syntax conversion, reference removal, and general formatting cleanup.
Provides pattern-based cleaning with support for custom patterns.

Classes
-------
MarkdownCleaner
    Handles markdown file cleaning and post-processing

Examples
--------
>>> from swanki.processing import MarkdownCleaner
>>> from pathlib import Path
>>> 
>>> cleaner = MarkdownCleaner(output_base=Path("output"))
>>> cleaned_files = cleaner.clean_all_markdown_files()
>>> print(f"Cleaned {len(cleaned_files)} files")
Cleaned 10 files
"""
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import re
import logging

logger = logging.getLogger(__name__)


def _natural_sort_key(path: Path) -> tuple:
    """Extract numeric parts from filename for natural sorting.

    Converts 'page-10.md' to ('page-', 10, '.md') for proper numeric ordering.
    This ensures page-2.md comes before page-10.md.

    Parameters
    ----------
    path : Path
        File path to extract sort key from

    Returns
    -------
    tuple
        Tuple of alternating strings and integers for natural sorting

    Examples
    --------
    >>> _natural_sort_key(Path("page-1.md"))
    ('page-', 1, '.md')
    >>> _natural_sort_key(Path("page-10.md"))
    ('page-', 10, '.md')
    """
    parts = re.split(r'(\d+)', path.name)
    return tuple(int(part) if part.isdigit() else part for part in parts)


class MarkdownCleaner:
    """Handles markdown file cleaning and post-processing.
    
    Applies various cleaning operations to markdown files including
    LaTeX syntax conversion, reference removal, and formatting fixes.
    Uses regex patterns for transformations.
    
    Parameters
    ----------
    output_base : Path
        Base directory for all output files
    
    Attributes
    ----------
    output_base : Path
        Base output directory
    md_singles_dir : Path
        Directory containing raw markdown files
    clean_md_singles_dir : Path
        Directory for cleaned markdown output
    PATTERNS : Dict[str, Tuple[str, str]]
        Regex patterns for cleaning operations
    
    Methods
    -------
    clean_all_markdown_files()
        Clean all markdown files in directory
    clean_single_file(md_path)
        Clean a single markdown file
    add_custom_pattern(name, pattern, replacement)
        Add custom cleaning pattern
    get_cleaning_stats(original, cleaned)
        Get statistics about cleaning
    
    Examples
    --------
    >>> cleaner = MarkdownCleaner(Path("output"))
    >>> 
    >>> # Clean all files
    >>> cleaned = cleaner.clean_all_markdown_files()
    >>> 
    >>> # Add custom pattern
    >>> cleaner.add_custom_pattern(
    ...     "custom_cite",
    ...     r"\\cite{(.*?)}",
    ...     r"[\1]"
    ... )
    """
    
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
        # Note: Figure blocks are handled by _convert_figure_blocks_to_markdown() method
        'table_blocks': (r'\\begin\{table\}[\s\S]*?\\end\{table\}', ''),  # Remove table blocks
        'header_backslash': (r'^(#+\s+[\d.]+)\s+\\\\\s+', r'\1 '),  # Clean header backslashes
    }
    
    def __init__(self, output_base: Path):
        """Initialize markdown cleaner.
        
        Parameters
        ----------
        output_base : Path
            Base directory for all output files. Expects 'md-singles'
            subdirectory with markdown files to clean.
        """
        self.output_base = output_base
        self.md_singles_dir = output_base / "md-singles"
        self.clean_md_singles_dir = output_base / "clean-md-singles"
        
    def clean_all_markdown_files(self) -> List[Path]:
        """Clean all markdown files in the md-singles directory.
        
        Processes all .md files found in md-singles, applying cleaning
        patterns and saving results to clean-md-singles directory.
        
        Returns
        -------
        List[Path]
            List of paths to successfully cleaned markdown files
        
        Examples
        --------
        >>> cleaner = MarkdownCleaner(Path("output"))
        >>> files = cleaner.clean_all_markdown_files()
        >>> for f in files:
        ...     print(f.name)
        page-1.md
        page-2.md
        
        Notes
        -----
        Failed cleanings are logged but don't stop the process.
        Original files are preserved; cleaned versions are saved
        in a separate directory.
        """
        # Create output directory
        self.clean_md_singles_dir.mkdir(parents=True, exist_ok=True)

        # Get all markdown files with natural/numeric sorting
        md_files = sorted(self.md_singles_dir.glob("*.md"), key=_natural_sort_key)
        
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
        
        Applies all cleaning patterns to the file and saves the
        cleaned version in the clean-md-singles directory.
        
        Parameters
        ----------
        md_path : Path
            Path to the markdown file to clean
        
        Returns
        -------
        Path or None
            Path to the cleaned markdown file if successful,
            None if cleaning failed
        
        Examples
        --------
        >>> cleaner = MarkdownCleaner(Path("output"))
        >>> cleaned = cleaner.clean_single_file(Path("page.md"))
        >>> if cleaned:
        ...     print(f"Cleaned: {cleaned}")
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

    def _convert_figure_blocks_to_markdown(self, content: str) -> str:
        """Convert LaTeX figure blocks to markdown image syntax.

        Extracts \includegraphics{url} from \begin{figure}...\end{figure} blocks
        and converts them to markdown ![alt](url) format before the blocks are removed.

        Parameters
        ----------
        content : str
            Original markdown content with LaTeX figure blocks

        Returns
        -------
        str
            Content with figure blocks converted to markdown images

        Notes
        -----
        This method must run BEFORE figure_blocks pattern removal to preserve
        image URLs. Handles cases where Mathpix only outputs LaTeX format
        without standalone markdown images.
        """
        def replace_figure_block(match):
            """Replace a single figure block with markdown image."""
            figure_content = match.group(0)

            # Extract image URL from \includegraphics
            img_pattern = r'\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}'
            img_match = re.search(img_pattern, figure_content)

            if not img_match:
                # No image found, remove the block
                return ''

            image_url = img_match.group(1)

            # Extract caption text if available
            caption_pattern = r'\\caption\{(.*?)\}'
            caption_match = re.search(caption_pattern, figure_content, re.DOTALL)

            if caption_match:
                # Clean up caption text: remove nested LaTeX commands
                caption_text = caption_match.group(1)
                # Remove \captionsetup and other LaTeX commands from caption
                caption_text = re.sub(r'\\[a-zA-Z]+(\{[^}]*\}|\[[^\]]*\])*', '', caption_text)
                caption_text = caption_text.strip()
                alt_text = caption_text[:100] + '...' if len(caption_text) > 100 else caption_text
            else:
                alt_text = 'Image'

            # Return markdown image
            return f'![{alt_text}]({image_url})\n'

        # Replace all figure blocks with markdown images
        figure_pattern = r'\\begin\{figure\}[\s\S]*?\\end\{figure\}'
        content = re.sub(figure_pattern, replace_figure_block, content, flags=re.DOTALL)

        return content

    def _apply_cleaning(self, content: str) -> str:
        """Apply all cleaning operations to markdown content.

        Parameters
        ----------
        content : str
            Original markdown content

        Returns
        -------
        str
            Cleaned markdown content

        Notes
        -----
        Operations include:
        - LaTeX command conversion
        - Reference section handling
        - Multiple empty line reduction
        - Trailing whitespace removal
        """
        # Convert figure blocks to markdown images BEFORE removing them
        content = self._convert_figure_blocks_to_markdown(content)

        # Apply multiline patterns (tables, etc.) - figures already converted
        multiline_patterns = ['table_blocks']
        for pattern_name in multiline_patterns:
            if pattern_name in self.PATTERNS:
                pattern, replacement = self.PATTERNS[pattern_name]
                content = re.sub(pattern, replacement, content, flags=re.DOTALL)

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
        
        Parameters
        ----------
        line : str
            Original line content
        
        Returns
        -------
        str
            Line with all pattern replacements applied
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
        
        Allows extending the cleaner with additional regex patterns
        for project-specific cleaning needs.
        
        Parameters
        ----------
        name : str
            Unique name for the pattern
        pattern : str
            Regex pattern to match
        replacement : str
            Replacement string (can use capture groups)
        
        Examples
        --------
        >>> cleaner = MarkdownCleaner(Path("output"))
        >>> # Convert custom LaTeX command
        >>> cleaner.add_custom_pattern(
        ...     "custom_bold",
        ...     r"\\mybold{(.*?)}",
        ...     r"**\1**"
        ... )
        """
        self.PATTERNS[name] = (pattern, replacement)
        logger.info(f"Added custom cleaning pattern: {name}")
    
    def get_cleaning_stats(self, original: str, cleaned: str) -> Dict[str, int]:
        """Get statistics about the cleaning process.
        
        Provides metrics to evaluate the cleaning impact.
        
        Parameters
        ----------
        original : str
            Original content before cleaning
        cleaned : str
            Content after cleaning
        
        Returns
        -------
        Dict[str, int]
            Dictionary containing:
            - original_lines: Line count before cleaning
            - cleaned_lines: Line count after cleaning
            - original_chars: Character count before
            - cleaned_chars: Character count after
            - removed_chars: Characters removed
        
        Examples
        --------
        >>> cleaner = MarkdownCleaner(Path("output"))
        >>> original = "\\section{Title}\n\\textbf{Bold}"
        >>> cleaned = cleaner._apply_cleaning(original)
        >>> stats = cleaner.get_cleaning_stats(original, cleaned)
        >>> print(f"Removed {stats['removed_chars']} characters")
        """
        return {
            'original_lines': len(original.split('\n')),
            'cleaned_lines': len(cleaned.split('\n')),
            'original_chars': len(original),
            'cleaned_chars': len(cleaned),
            'removed_chars': len(original) - len(cleaned)
        }