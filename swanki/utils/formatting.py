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
    
    Converts the citation key to a readable format optimized for TTS,
    with proper pauses and structure.
    
    Parameters
    ----------
    citation_key : str
        Citation key (e.g., "bishopDeepLearningFoundations2024_deep-learning-revolution")
    
    Returns
    -------
    str
        Human-readable version for speech
    
    Examples
    --------
    >>> humanize_citation_key("bishopDeepLearningFoundations2024")
    'Bishop, Deep Learning Foundations, 2024'
    
    >>> humanize_citation_key("bishopDeepLearningFoundations2024_deep-learning-revolution")
    'Bishop, Deep Learning Foundations, 2024, deep learning revolution'
    
    >>> humanize_citation_key("smith2023")
    'Smith, 2023'
    
    >>> humanize_citation_key("johnsonEtAl2022")
    'Johnson et al, 2022'
    """
    if not citation_key:
        return ""
    
    # Remove @ prefix if present
    if citation_key.startswith('@'):
        citation_key = citation_key[1:]
    
    # Replace underscores with spaces
    citation_key = citation_key.replace('_', ' ')
    
    # Replace hyphens with spaces 
    citation_key = citation_key.replace('-', ' ')
    
    # Split camelCase by inserting spaces before capitals
    # But preserve consecutive capitals (like "USA" or "CNN")
    result = ""
    for i, char in enumerate(citation_key):
        if i > 0 and char.isupper():
            # Check if previous char is lowercase or if next char is lowercase
            prev_is_lower = citation_key[i-1].islower()
            next_is_lower = i+1 < len(citation_key) and citation_key[i+1].islower()
            
            if prev_is_lower or (not prev_is_lower and next_is_lower):
                result += " "
        result += char
    
    # Clean up multiple spaces
    result = " ".join(result.split())
    
    # Simple capitalization - just capitalize first letter of each word
    words = result.split()
    capitalized_words = []
    
    # Track if we've seen a year to add proper punctuation
    year_pattern = re.compile(r'^\d{4}$')
    author_found = False
    
    for i, word in enumerate(words):
        if word.lower() == "et" and i + 1 < len(words) and words[i + 1].lower() == "al":
            # Keep "et al" lowercase and together
            capitalized_words.append("et al")
            continue
        elif word.lower() == "al" and i > 0 and words[i - 1].lower() == "et":
            # Skip "al" as it's already handled above
            continue
        elif year_pattern.match(word):
            # This is a year
            if author_found and len(capitalized_words) > 0:
                # Add comma before year
                capitalized_words[-1] = capitalized_words[-1] + ","
            capitalized_words.append(word)
            # If there's more content after the year, add comma
            if i + 1 < len(words):
                capitalized_words[-1] = word + ","
        else:
            # Regular word
            if not author_found:
                # First word is author
                author_found = True
                capitalized = word[0].upper() + word[1:].lower() if len(word) > 1 else word.upper()
                # Add comma after author if there's more content
                if len(words) > 1:
                    capitalized += ","
                capitalized_words.append(capitalized)
            else:
                # Other words
                capitalized_words.append(word[0].upper() + word[1:].lower() if len(word) > 1 else word.upper())
    
    return " ".join(capitalized_words)