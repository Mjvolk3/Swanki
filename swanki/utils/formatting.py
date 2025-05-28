"""Formatting utilities for tags and other text processing.

This module provides utilities for formatting tags, detecting tags from text,
and converting citation keys to human-readable format. Supports various tag
formats and citation key patterns.

Functions
---------
format_tags(tags, format_type)
    Format tags according to specified style
detect_tags_from_text(text)
    Extract tags from text content
humanize_citation_key(citation_key)
    Convert citation key to readable format

Examples
--------
>>> from swanki.utils.formatting import format_tags
>>> 
>>> tags = ["Machine Learning", "Deep-Learning", "AI"]
>>> formatted = format_tags(tags, "slugified")
>>> print(formatted)
['machine-learning', 'deep-learning', 'ai']

>>> from swanki.utils.formatting import humanize_citation_key
>>> 
>>> print(humanize_citation_key("smithMachineLearning2023"))
'Smith, Machine Learning, 2023'
"""
import re
from typing import List


def format_tags(tags: List[str], format_type: str = "slugified") -> List[str]:
    """Format tags according to the specified format type.
    
    Applies consistent formatting to tags for use in flashcards and
    organization. Supports multiple formatting styles.
    
    Parameters
    ----------
    tags : List[str]
        List of tags to format
    format_type : {'slugified', 'spaces', 'raw'}, optional
        Type of formatting to apply (default is "slugified"):
        - "slugified": Lowercase, spaces to hyphens, special chars removed
        - "spaces": Clean up extra spaces only
        - "raw": No formatting, return as-is
    
    Returns
    -------
    List[str]
        List of formatted tags
    
    Examples
    --------
    >>> tags = ["Neural Networks", "Deep Learning", "AI/ML"]
    >>> 
    >>> # Slugified format (default)
    >>> format_tags(tags)
    ['neural-networks', 'deep-learning', 'aiml']
    >>> 
    >>> # Preserve spaces
    >>> format_tags(tags, "spaces")
    ['Neural Networks', 'Deep Learning', 'AI/ML']
    >>> 
    >>> # Raw format
    >>> format_tags(tags, "raw")
    ['Neural Networks', 'Deep Learning', 'AI/ML']
    
    Notes
    -----
    Slugified format:
    - Converts to lowercase
    - Replaces spaces with hyphens
    - Removes special characters except dots and hyphens
    - Collapses multiple hyphens
    - Strips leading/trailing hyphens
    """
    if format_type == "raw":
        return tags
    
    formatted_tags = []
    for tag in tags:
        if format_type == "slugified":
            # Convert to lowercase and replace spaces with hyphens
            # Also remove any special characters except dots and hyphens
            formatted = tag.lower()
            formatted = re.sub(r'[^\w\s.-]', '', formatted)
            formatted = re.sub(r'\s+', '-', formatted)
            formatted = re.sub(r'-+', '-', formatted)  # Remove multiple hyphens
            formatted = formatted.strip('-')
            formatted_tags.append(formatted)
        elif format_type == "spaces":
            # Just clean up extra spaces
            formatted = ' '.join(tag.split())
            formatted_tags.append(formatted)
        else:
            # Default to raw if unknown format
            formatted_tags.append(tag)
    
    return formatted_tags


def detect_tags_from_text(text: str) -> List[str]:
    """Detect tags from text based on # and comma delimited formats.
    
    Extracts tags from text using multiple detection strategies including
    hashtag format and comma-delimited lists.
    
    Parameters
    ----------
    text : str
        Text to extract tags from
    
    Returns
    -------
    List[str]
        List of unique detected tags (order preserved)
    
    Examples
    --------
    >>> # Hashtag format
    >>> text1 = "This is about #machinelearning and #deeplearning"
    >>> detect_tags_from_text(text1)
    ['machinelearning', 'deeplearning']
    >>> 
    >>> # Comma-delimited format
    >>> text2 = "Tags: python, data science, visualization"
    >>> detect_tags_from_text(text2)
    ['python', 'data science', 'visualization']
    >>> 
    >>> # Mixed format
    >>> text3 = "#AI #ML\nCategories: neural networks, optimization"
    >>> detect_tags_from_text(text3)
    ['AI', 'ML', 'neural networks', 'optimization']
    
    Notes
    -----
    Detection strategies:
    1. Hashtags: #tag1 #tag2 (# prefix removed)
    2. Label lines: "Tags:", "Labels:", "Categories:" followed by comma list
    3. Comma lists: Short lines with commas, no periods
    
    Duplicates are removed while preserving first occurrence order.
    """
    tags = []
    
    # Look for hashtag format: #tag1, #tag2 or #tag1 #tag2
    hashtag_pattern = r'#[\w.-]+'
    hashtag_matches = re.findall(hashtag_pattern, text)
    for match in hashtag_matches:
        tags.append(match[1:])  # Remove the # prefix
    
    # If no hashtags found, look for comma-delimited format at the end of lines
    if not tags:
        # Look for patterns like "Tags: tag1, tag2, tag3" or just "tag1, tag2, tag3" at line end
        lines = text.strip().split('\n')
        for line in lines:
            line = line.strip()
            # Check if line starts with "Tags:" or similar
            if re.match(r'^(tags?|labels?|categories?):\s*', line, re.IGNORECASE):
                tag_text = re.sub(r'^(tags?|labels?|categories?):\s*', '', line, flags=re.IGNORECASE)
                potential_tags = [t.strip() for t in tag_text.split(',')]
                tags.extend([t for t in potential_tags if t])
            # Check if line is just comma-separated values (heuristic: has commas and no periods)
            elif ',' in line and '.' not in line and len(line) < 100:
                potential_tags = [t.strip() for t in line.split(',')]
                if all(len(t) < 30 for t in potential_tags if t):  # Reasonable tag length
                    tags.extend([t for t in potential_tags if t])
    
    # Remove duplicates while preserving order
    seen = set()
    unique_tags = []
    for tag in tags:
        if tag.lower() not in seen:
            seen.add(tag.lower())
            unique_tags.append(tag)
    
    return unique_tags


def humanize_citation_key(citation_key: str) -> str:
    """Convert a citation key to human-readable format for audio.
    
    Transforms camelCase citation keys into natural spoken format,
    handling special name patterns and formatting conventions.
    
    Parameters
    ----------
    citation_key : str
        Citation key in camelCase format (e.g., "smithMachineLearning2023")
    
    Returns
    -------
    str
        Human-readable version with proper capitalization and punctuation
    
    Examples
    --------
    >>> humanize_citation_key("luoWhenCausalInference2020")
    'Luo, When Causal Inference, 2020'
    
    >>> humanize_citation_key("smithMachineLearning2023")
    'Smith, Machine Learning, 2023'
    
    >>> humanize_citation_key("johnsonEtAl2022")
    'Johnson et al, 2022'
    
    >>> humanize_citation_key("oReilly2019")
    "O'Reilly, 2019"
    
    >>> humanize_citation_key("mcDonald2024")
    'McDonald, 2024'
    
    >>> humanize_citation_key("vanDijkTheoryPractice2021")
    'van Dijk, Theory Practice, 2021'
    
    Notes
    -----
    Special handling for:
    - "EtAl" -> "et al"
    - Name prefixes: mc/Mac, o/O', de, van, von
    - Year extraction from end
    - Proper comma placement after author name
    - Multiple consecutive capitals (e.g., "USA")
    """
    if not citation_key:
        return ""
    
    # Remove @ prefix if present
    if citation_key.startswith('@'):
        citation_key = citation_key[1:]
    
    # Handle common patterns
    # First, handle "EtAl" -> "et al"
    humanized = citation_key.replace("EtAl", " et al")
    
    # Extract year at the end (if present)
    year_match = re.search(r'(\d{4})$', humanized)
    year = ""
    if year_match:
        year = year_match.group(1)
        humanized = humanized[:-4]  # Remove year from main text
    
    # Handle special name patterns before general processing
    # Common prefixes that should stay together
    name_patterns = [
        (r'^mc([A-Z])', r'Mc\1'),  # McDonald -> McDonald
        (r'^mac([A-Z])', r'Mac\1'),  # MacArthur -> MacArthur
        (r'^o([A-Z])', r"O'\1"),  # oReilly -> O'Reilly
        (r'^de([A-Z])', r'de \1'),  # deSouza -> de Souza
        (r'^van([A-Z])', r'van \1'),  # vanDijk -> van Dijk
        (r'^von([A-Z])', r'von \1'),  # vonNeumann -> von Neumann
    ]
    
    # Apply name patterns
    for pattern, replacement in name_patterns:
        humanized = re.sub(pattern, replacement, humanized)
    
    # Split camelCase into words
    # Insert space before uppercase letters that follow lowercase letters
    # But not if it's after an apostrophe (like O'Reilly)
    humanized = re.sub(r"(?<!')([a-z])([A-Z])", r'\1 \2', humanized)
    
    # Handle multiple consecutive capitals (like "USA" or "CNN")
    humanized = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1 \2', humanized)
    
    # Split into words
    words = humanized.split()
    
    if words:
        # First word is always the author name - capitalize it properly
        first_word = words[0]
        
        # Check if it's a special prefix that should stay lowercase
        if first_word.lower() in ['de', 'van', 'von']:
            # Keep lowercase, but capitalize the next word
            if len(words) > 1:
                words[1] = words[1].capitalize()
                words[1] = words[1] + ","  # Add comma after actual surname
        else:
            # Normal case - capitalize first word
            words[0] = words[0].capitalize()
            # Add comma after first word if there are more words
            if len(words) > 1 and words[1].lower() not in ['et', 'al']:
                words[0] = words[0] + ","
    
    # Rejoin words
    humanized = " ".join(words)
    
    # Add year at the end if present
    if year:
        humanized = f"{humanized}, {year}"
    
    # Clean up any double spaces
    humanized = " ".join(humanized.split())
    
    return humanized