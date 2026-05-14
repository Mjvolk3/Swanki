"""
swanki/utils/formatting.py
[[swanki.utils.formatting]]
https://github.com/Mjvolk3/Swanki/tree/main/swanki/utils/formatting.py

Formatting utilities for tags and other text processing.
"""

import re


def format_tags(tags: list[str], format_type: str = "slugified") -> list[str]:
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

    Returns:
    -------
    List[str]
        List of formatted tags

    Examples:
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

    Notes:
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
            formatted = re.sub(r"[^\w\s.-]", "", formatted)
            formatted = re.sub(r"\s+", "-", formatted)
            formatted = re.sub(r"-+", "-", formatted)  # Remove multiple hyphens
            formatted = formatted.strip("-")
            formatted_tags.append(formatted)
        elif format_type == "spaces":
            # Just clean up extra spaces
            formatted = " ".join(tag.split())
            formatted_tags.append(formatted)
        else:
            # Default to raw if unknown format
            formatted_tags.append(tag)

    return formatted_tags


def detect_tags_from_text(text: str) -> list[str]:
    r"""Detect tags from text based on # and comma delimited formats.

    Extracts tags from text using multiple detection strategies including
    hashtag format and comma-delimited lists.

    Parameters
    ----------
    text : str
        Text to extract tags from

    Returns:
    -------
    List[str]
        List of unique detected tags (order preserved)

    Examples:
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

    Notes:
    -----
    Detection strategies:
    1. Hashtags: #tag1 #tag2 (# prefix removed)
    2. Label lines: "Tags:", "Labels:", "Categories:" followed by comma list
    3. Comma lists: Short lines with commas, no periods

    Duplicates are removed while preserving first occurrence order.
    """
    tags = []

    # Look for hashtag format: #tag1, #tag2 or #tag1 #tag2
    hashtag_pattern = r"#[\w.-]+"
    hashtag_matches = re.findall(hashtag_pattern, text)
    for match in hashtag_matches:
        tags.append(match[1:])  # Remove the # prefix

    # If no hashtags found, look for comma-delimited format at the end of lines
    if not tags:
        # Look for patterns like "Tags: tag1, tag2, tag3" or just "tag1, tag2, tag3" at line end
        lines = text.strip().split("\n")
        for line in lines:
            line = line.strip()
            # Check if line starts with "Tags:" or similar
            if re.match(r"^(tags?|labels?|categories?):\s*", line, re.IGNORECASE):
                tag_text = re.sub(
                    r"^(tags?|labels?|categories?):\s*", "", line, flags=re.IGNORECASE
                )
                potential_tags = [t.strip() for t in tag_text.split(",")]
                tags.extend([t for t in potential_tags if t])
            # Check if line is just comma-separated values (heuristic: has commas and no periods)
            elif "," in line and "." not in line and len(line) < 100:
                potential_tags = [t.strip() for t in line.split(",")]
                if all(
                    len(t) < 30 for t in potential_tags if t
                ):  # Reasonable tag length
                    tags.extend([t for t in potential_tags if t])

    # Remove duplicates while preserving order
    seen = set()
    unique_tags = []
    for tag in tags:
        if tag.lower() not in seen:
            seen.add(tag.lower())
            unique_tags.append(tag)

    return unique_tags


def _split_camel_case(text: str) -> str:
    """Split camelCase and digit/letter boundaries into spaces."""
    result = ""
    for i, char in enumerate(text):
        if i > 0:
            prev = text[i - 1]
            if (prev.isalpha() and char.isdigit()) or (
                prev.isdigit() and char.isalpha()
            ):
                result += " "
            elif char.isupper():
                prev_is_lower = prev.islower()
                next_is_lower = i + 1 < len(text) and text[i + 1].islower()
                if prev_is_lower or (not prev_is_lower and next_is_lower):
                    result += " "
        result += char
    return result


def humanize_citation_key(citation_key: str) -> str:
    """Convert a citation key to human-readable format for audio.

    Converts the citation key to a readable format optimized for TTS,
    with proper pauses and structure.

    Parameters
    ----------
    citation_key : str
        Citation key (e.g., "bishopDeepLearningFoundations2024_deep-learning-revolution")

    Returns:
    -------
    str
        Human-readable version for speech

    Examples:
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
    if citation_key.startswith("@"):
        citation_key = citation_key[1:]

    # Split on underscores first (separates suffix like _deep-learning-revolution)
    parts = citation_key.split("_")
    main_part = parts[0]
    suffix_parts = [p.replace("-", " ") for p in parts[1:]]

    # Extract trailing year from main part (e.g., "Virtual2024" → "Virtual", "2024")
    # Also handle "50MCells2025" → strip year from end
    year_match = re.search(r"(\d{4})$", main_part)
    year = year_match.group(1) if year_match else ""
    if year:
        main_part = main_part[: -len(year)]

    # Split camelCase — preserve consecutive capitals (like "USA", "CNN", "CRISPR")
    result = _split_camel_case(main_part)
    words = result.split()
    if not words:
        return citation_key

    # Detect hyphenated author names at the start of main_part
    # e.g., "ahlmann-eltzeDeeplearning..." → author="Ahlmann-Eltze", rest="Deeplearning..."
    # Match: lowercase-lowercase followed by an uppercase letter starting the title
    hyphen_match = re.match(r"^([a-z]+-[a-z]+)([A-Z].*)?$", main_part)
    if hyphen_match:
        raw_author = hyphen_match.group(1)
        remaining_text = hyphen_match.group(2) or ""
        author = "-".join(
            p[0].upper() + p[1:] if len(p) > 1 else p.upper()
            for p in raw_author.split("-")
        )
        # Run the same camelCase splitter on remaining text
        words = _split_camel_case(remaining_text).split()
        title_start = 0
    else:
        raw_author = words[0]
        author = (
            raw_author[0].upper() + raw_author[1:]
            if len(raw_author) > 1
            else raw_author.upper()
        )
        title_start = 1

    # Handle "et al" and build title words
    title_words = []
    i = title_start
    while i < len(words):
        w = words[i]
        if w.lower() == "et" and i + 1 < len(words) and words[i + 1].lower() == "al":
            title_words.append("et al")
            i += 2
            continue
        # Keep short all-caps as acronyms (CRISPR, DNA, GPT, PRINT)
        if w.isupper() and len(w) >= 2:
            title_words.append(w)
        elif len(w) > 1:
            title_words.append(w[0].upper() + w[1:])
        else:
            title_words.append(w.upper())
        i += 1

    # Assemble: Author, Title Words, Year, suffix
    # "et al" goes right after author without extra comma separation
    if title_words and title_words[0] == "et al":
        segments = [f"{author} et al"]
        remaining_title = title_words[1:]
        if remaining_title:
            segments.append(" ".join(remaining_title))
    else:
        segments = [author]
        if title_words:
            segments.append(" ".join(title_words))
    if year:
        segments.append(year)
    for s in suffix_parts:
        if s.strip():
            segments.append(s.strip())

    return ", ".join(segments)


_CHAPTER_KEY_PATTERN = re.compile(
    r"^(?P<base>[A-Za-z][A-Za-z0-9]+)_(?P<num>\d{1,3})_(?P<slug>[a-z][a-z0-9-]+)$"
)


def humanize_chapter_slug(citation_key: str) -> str | None:
    """Render ``<base>_<NN>_<slug>`` keys as ``Chapter <N>: <human slug>``.

    Returns ``None`` for non-chapter inputs so callers can fall back to
    :func:`humanize_citation_key`. The numeric segment drops leading zeros
    so ``03`` becomes ``"3"`` (not ``"zero three"``); the slug's hyphens
    become spaces.

    Examples:
        >>> humanize_chapter_slug("hammingArtDoingScience2020_03_history-of-computers-hardware")
        'Chapter 3: history of computers hardware'
        >>> humanize_chapter_slug("hammingArtDoingScience2020_1_orientation")
        'Chapter 1: orientation'
        >>> humanize_chapter_slug("bishopDeepLearning2024") is None
        True

    Args:
        citation_key: Raw citation key (book chapter form preferred).

    Returns:
        Humanized chapter label, or ``None`` if the key has no chapter pattern.
    """
    if not citation_key:
        return None
    if citation_key.startswith("@"):
        citation_key = citation_key[1:]
    m = _CHAPTER_KEY_PATTERN.match(citation_key)
    if not m:
        return None
    num = int(m.group("num"))
    slug = m.group("slug").replace("-", " ")
    return f"Chapter {num}: {slug}"
