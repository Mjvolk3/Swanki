"""Content processing utilities for images, math, and text analysis.

This module provides utilities for analyzing and extracting information
from markdown content, including image extraction, mathematical content
detection, figure caption parsing, and section splitting.

Functions
---------
extract_images_from_markdown(markdown_content, base_path)
    Extract image references from markdown
detect_math_content(text)
    Check if text contains mathematical notation
extract_figure_captions(markdown_content)
    Extract figure captions and context
split_content_by_sections(markdown_content)
    Split content into logical sections
generate_image_card_prompts(image_info, ...)
    Generate prompts for image-based cards

Examples
--------
>>> from swanki.utils.content import extract_images_from_markdown
>>> 
>>> markdown = "Here is an image: ![Figure 1](images/fig1.png)"
>>> images = extract_images_from_markdown(markdown)
>>> print(images[0]['alt'])
'Figure 1'

>>> from swanki.utils.content import detect_math_content
>>> 
>>> has_math = detect_math_content("The equation $E = mc^2$ is famous")
>>> print(has_math)
True
"""
import re
from pathlib import Path
from typing import List, Dict, Optional, Tuple


def extract_images_from_markdown(markdown_content: str, base_path: Optional[Path] = None) -> List[Dict[str, str]]:
    """Extract image information from markdown content.
    
    Finds all image references in markdown format and extracts
    metadata including paths, alt text, and surrounding context.
    
    Parameters
    ----------
    markdown_content : str
        The markdown text to analyze
    base_path : Path, optional
        Base path for resolving relative image paths
    
    Returns
    -------
    List[Dict[str, str]]
        List of dictionaries containing:
        - path: Resolved image path
        - alt: Alternative text
        - context: 200 chars of surrounding text
        - original_path: Original path from markdown
    
    Examples
    --------
    >>> content = "See ![diagram](img/fig1.png) for details."
    >>> images = extract_images_from_markdown(content, Path("/docs"))
    >>> print(images[0])
    {'path': '/docs/img/fig1.png', 'alt': 'diagram', ...}
    
    Notes
    -----
    Image pattern matches: ![alt text](path)
    HTTP/HTTPS URLs are preserved as-is.
    """
    images = []
    
    # Pattern for markdown images: ![alt](path)
    image_pattern = r'!\[([^\]]*)\]\(([^\)]+)\)'
    
    for match in re.finditer(image_pattern, markdown_content):
        alt_text = match.group(1)
        image_path = match.group(2)
        
        # Get context around the image (previous and next 100 characters)
        start = max(0, match.start() - 100)
        end = min(len(markdown_content), match.end() + 100)
        context = markdown_content[start:end]
        
        # Resolve relative paths if base_path provided
        if base_path and not image_path.startswith(('http://', 'https://', '/')):
            resolved_path = str(base_path / image_path)
        else:
            resolved_path = image_path
        
        images.append({
            "path": resolved_path,
            "alt": alt_text,
            "context": context.strip(),
            "original_path": image_path
        })
    
    return images


def detect_math_content(text: str) -> bool:
    """Detect if text contains mathematical content.
    
    Checks for various indicators of mathematical notation including
    LaTeX commands, math delimiters, Greek letters, and math keywords.
    
    Parameters
    ----------
    text : str
        Text to analyze for mathematical content
    
    Returns
    -------
    bool
        True if mathematical content is detected, False otherwise
    
    Examples
    --------
    >>> detect_math_content("The formula $x^2 + y^2 = z^2$")
    True
    
    >>> detect_math_content("This is plain text")
    False
    
    >>> detect_math_content("\\frac{1}{2} of the total")
    True
    
    Notes
    -----
    Detects:
    - Inline math: $...$
    - Display math: $$...$$
    - LaTeX commands: \frac, \sum, \int
    - Greek letters: \alpha, \beta, etc.
    - Math keywords: equation, theorem, proof
    - Simple arithmetic: 2 + 2
    """
    # Patterns that indicate mathematical content
    math_patterns = [
        r'\$[^$]+\$',  # Inline math $...$
        r'\$\$[^$]+\$\$',  # Display math $$...$$
        r'\\begin\{[^}]+\}',  # LaTeX environments
        r'\\[a-zA-Z]+\{',  # LaTeX commands
        r'\\frac\{',  # Fractions
        r'\\sum\b',  # Summation
        r'\\int\b',  # Integration
        r'\\partial\b',  # Partial derivatives
        r'\\alpha\b|\\beta\b|\\gamma\b|\\delta\b|\\epsilon\b|\\theta\b|\\lambda\b|\\mu\b|\\pi\b|\\sigma\b|\\tau\b|\\phi\b|\\chi\b|\\psi\b|\\omega\b',  # Greek letters
        r'\b\d+\s*[+\-*/]\s*\d+\b',  # Simple arithmetic
        r'\b[a-zA-Z]\s*[=<>]\s*[a-zA-Z0-9]',  # Equations
        r'\b(?:equation|formula|theorem|proof|lemma|corollary)\b',  # Math keywords
    ]
    
    for pattern in math_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    
    return False


def extract_figure_captions(markdown_content: str) -> List[Dict[str, str]]:
    """Extract figure captions and their associated content.
    
    Finds references to figures (Fig. 1, Figure 1, etc.) and extracts
    their captions and surrounding context.
    
    Parameters
    ----------
    markdown_content : str
        The markdown text to analyze
    
    Returns
    -------
    List[Dict[str, str]]
        List of dictionaries containing:
        - number: Figure number (e.g., "1", "2a")
        - caption: Caption text
        - context: 400 chars of surrounding context
    
    Examples
    --------
    >>> content = "Fig. 1: Neural network architecture. The model..."
    >>> figures = extract_figure_captions(content)
    >>> print(figures[0]['caption'])
    'Neural network architecture.'
    
    Notes
    -----
    Matches patterns:
    - "Fig. 1:", "Figure 1:", "fig. 1|"
    - Supports sub-figures: "Fig. 1a", "Figure 2b"
    - Case-insensitive matching
    """
    figures = []
    
    # Look for patterns like "Fig. 1", "Figure 1", etc.
    fig_pattern = r'(?:Fig\.|Figure|fig\.)\s*(\d+[a-z]?)\s*[|:]\s*([^\n]+)'
    
    for match in re.finditer(fig_pattern, markdown_content, re.IGNORECASE):
        fig_num = match.group(1)
        caption = match.group(2).strip()
        
        # Get surrounding context
        start = max(0, match.start() - 200)
        end = min(len(markdown_content), match.end() + 200)
        context = markdown_content[start:end]
        
        figures.append({
            "number": fig_num,
            "caption": caption,
            "context": context.strip()
        })
    
    return figures


def split_content_by_sections(markdown_content: str) -> List[Dict[str, str]]:
    """Split markdown content into logical sections.
    
    Divides content based on markdown headers (#, ##, etc.) to create
    structured sections suitable for processing.
    
    Parameters
    ----------
    markdown_content : str
        The markdown text to split into sections
    
    Returns
    -------
    List[Dict[str, str]]
        List of section dictionaries containing:
        - level: Header level (1-6)
        - title: Section title
        - content: Section content
    
    Examples
    --------
    >>> content = "# Introduction\nText...\n## Methods\nMore text..."
    >>> sections = split_content_by_sections(content)
    >>> print(sections[0]['title'])
    'Introduction'
    >>> print(sections[1]['level'])
    2
    
    Notes
    -----
    - Content before first header goes into "Introduction" section
    - Empty sections are excluded
    - Preserves header hierarchy
    """
    sections = []
    
    # Split by headers
    header_pattern = r'^(#{1,6})\s+(.+)$'
    lines = markdown_content.split('\n')
    current_section = {"level": 0, "title": "Introduction", "content": ""}
    
    for line in lines:
        header_match = re.match(header_pattern, line)
        if header_match:
            # Save previous section if it has content
            if current_section["content"].strip():
                sections.append(current_section.copy())
            
            # Start new section
            level = len(header_match.group(1))
            title = header_match.group(2).strip()
            current_section = {"level": level, "title": title, "content": ""}
        else:
            current_section["content"] += line + "\n"
    
    # Add the last section
    if current_section["content"].strip():
        sections.append(current_section)
    
    return sections


def generate_image_card_prompts(
    image_info: Dict[str, str], 
    surrounding_content: str,
    num_cards: int = 3,
    image_on_front: bool = True,
    image_on_back: bool = True
) -> List[str]:
    """Generate prompts for creating cards from image content.
    
    Creates prompts suitable for AI generation of flashcards based
    on image content and context.
    
    Parameters
    ----------
    image_info : Dict[str, str]
        Dictionary with 'path', 'alt', and 'context' keys
    surrounding_content : str
        Extended text content around the image
    num_cards : int, optional
        Number of cards to generate (default is 3)
    image_on_front : bool, optional
        Whether image can be on front of card (default is True)
    image_on_back : bool, optional
        Whether image can be on back of card (default is True)
    
    Returns
    -------
    List[str]
        List of formatted prompts for card generation
    
    Examples
    --------
    >>> image = {'path': 'fig.png', 'alt': 'Graph', 'context': '...'}
    >>> prompts = generate_image_card_prompts(
    ...     image,
    ...     "The graph shows exponential growth...",
    ...     num_cards=2
    ... )
    >>> len(prompts)
    1
    
    Notes
    -----
    Currently returns a single comprehensive prompt.
    Future versions may return multiple specialized prompts.
    """
    prompts = []
    
    base_prompt = f"""
Create educational flashcards based on this image and its context.

Image information:
- Path: {image_info['path']}
- Alt text: {image_info['alt']}
- Context: {image_info['context']}

Surrounding content:
{surrounding_content}

Requirements:
- Generate {num_cards} distinct flashcards
- Each card should test understanding of the image content
- Cards can reference specific parts of the image
- Include mathematical notation if present in the image
"""
    
    if image_on_front and image_on_back:
        base_prompt += "- Image can appear on either front or back of card as appropriate\n"
    elif image_on_front:
        base_prompt += "- Image should appear on the front of cards\n"
    elif image_on_back:
        base_prompt += "- Image should appear on the back of cards\n"
    
    prompts.append(base_prompt)
    
    return prompts