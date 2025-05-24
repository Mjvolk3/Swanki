"""Content processing utilities for images, math, and text analysis."""
import re
from pathlib import Path
from typing import List, Dict, Optional, Tuple


def extract_images_from_markdown(markdown_content: str, base_path: Optional[Path] = None) -> List[Dict[str, str]]:
    """Extract image information from markdown content.
    
    Args:
        markdown_content: The markdown text to analyze
        base_path: Base path for resolving relative image paths
        
    Returns:
        List of dictionaries with image information:
        [{"path": "image.jpg", "alt": "alt text", "context": "surrounding text"}]
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
    
    Args:
        text: Text to analyze
        
    Returns:
        True if mathematical content is detected
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
    
    Args:
        markdown_content: The markdown text to analyze
        
    Returns:
        List of dictionaries with figure information
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
    
    Args:
        markdown_content: The markdown text to split
        
    Returns:
        List of sections with their content and metadata
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
    
    Args:
        image_info: Dictionary with image information
        surrounding_content: Text content around the image
        num_cards: Number of cards to generate
        image_on_front: Whether image can be on front of card
        image_on_back: Whether image can be on back of card
        
    Returns:
        List of prompts for card generation
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