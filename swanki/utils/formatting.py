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
    # Accept both `<base>_<NN>_<slug>` and `<base>_CH<NN>_<slug>` so chapter
    # content_keys can carry the documented `CH` prefix (feedback_book_chapter_slug
    # memory) without the legacy `_<NN>_` form regressing. Non-capturing `(?:CH)?`
    # keeps the `num` group identical for both forms.
    r"^(?P<base>[A-Za-z][A-Za-z0-9]+)_(?:CH)?(?P<num>\d{1,3})_(?P<slug>[a-z][a-z0-9-]+)$"
)


def parse_chapter_key(citation_key: str) -> tuple[str, str, str] | None:
    """Parse ``<base>_<NN>_<slug>`` into ``(base, num_str, slug_humanized)``.

    Returns ``None`` for non-chapter inputs so callers can fall back to
    plain :func:`humanize_citation_key`. The numeric segment is returned as a
    string (preserving leading zero) so callers can decide whether to render
    "01" as "o one" (spoken form) or 1 (cardinal) per their context. The slug
    has hyphens replaced with spaces.

    Examples:
        >>> parse_chapter_key("hammingArtDoingScience2020_03_history-of-computers-hardware")
        ('hammingArtDoingScience2020', '03', 'history of computers hardware')
        >>> parse_chapter_key("bishopDeepLearning2024") is None
        True
    """
    if not citation_key:
        return None
    if citation_key.startswith("@"):
        citation_key = citation_key[1:]
    m = _CHAPTER_KEY_PATTERN.match(citation_key)
    if not m:
        return None
    return m.group("base"), m.group("num"), m.group("slug").replace("-", " ")


_CARDINAL_WORDS = (
    "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
    "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
    "sixteen", "seventeen", "eighteen", "nineteen", "twenty",
)


def chapter_number_spoken(num_str: str) -> str:
    """Render a chapter-number string in spoken form.

    Single-digit numbers preserved with a leading zero (``"01"``) render as
    ``"o one"``, ``"02"`` -> ``"o two"``, ..., matching the way listeners read
    a written chapter slug aloud (the audio bookend says exactly what the
    citation key shows). Numbers without a leading zero render as cardinal
    words ("one", "two", "twenty"). Numbers above 20 fall back to
    digit-by-digit spelling (rare for chapter slugs).

    Examples:
        >>> chapter_number_spoken("01")
        'o one'
        >>> chapter_number_spoken("12")
        'twelve'
        >>> chapter_number_spoken("3")
        'three'
        >>> chapter_number_spoken("25")
        'two five'
    """
    n = int(num_str)
    if len(num_str) == 2 and num_str[0] == "0":
        return f"o {_CARDINAL_WORDS[int(num_str[1])]}"
    if 0 <= n <= 20:
        return _CARDINAL_WORDS[n]
    digits = "0123456789"
    return " ".join(_CARDINAL_WORDS[digits.index(d)] for d in num_str)


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
    parsed = parse_chapter_key(citation_key)
    if parsed is None:
        return None
    _, num_str, slug = parsed
    return f"Chapter {int(num_str)}: {slug}"


_ROMAN_TO_WORD = {
    "i": "one", "ii": "two", "iii": "three", "iv": "four", "v": "five",
    "vi": "six", "vii": "seven", "viii": "eight", "ix": "nine", "x": "ten",
    "xi": "eleven", "xii": "twelve", "xiii": "thirteen", "xiv": "fourteen",
    "xv": "fifteen", "xvi": "sixteen", "xvii": "seventeen", "xviii": "eighteen",
    "xix": "nineteen", "xx": "twenty",
}


def humanize_chapter_slug_spoken(slug: str) -> str:
    """Convert trailing roman-numeral suffix in a chapter slug to a word.

    `parse_chapter_key` already returns the slug with hyphens replaced by
    spaces, so this operates on a space-separated phrase. If the final
    space-separated token is a roman numeral (the common "Artificial
    Intelligence — II", "Coding Theory — I", "Digital Filters — IV"
    pattern), spell it as an English word so Fish Speech does not garble
    "ii" / "iii" as "g i s" or "i i". Only the trailing token is converted
    -- mid-slug "v" / "i" letters that are not numerals stay untouched. The
    function is also tolerant of raw hyphenated input (splits on either).

    Examples:
        >>> humanize_chapter_slug_spoken("artificial intelligence ii")
        'artificial intelligence two'
        >>> humanize_chapter_slug_spoken("artificial-intelligence-ii")
        'artificial intelligence two'
        >>> humanize_chapter_slug_spoken("history of computers hardware")
        'history of computers hardware'
        >>> humanize_chapter_slug_spoken("digital filters iv")
        'digital filters four'
        >>> humanize_chapter_slug_spoken("n dimensional space")
        'n dimensional space'

    Args:
        slug: Chapter slug (either already-space-separated from
            `parse_chapter_key`, or raw hyphenated form).

    Returns:
        Space-separated spoken form with trailing roman numerals as words.
    """
    if not slug:
        return ""
    tokens = slug.replace("-", " ").split()
    if not tokens:
        return ""
    last = tokens[-1].lower()
    if last in _ROMAN_TO_WORD:
        tokens[-1] = _ROMAN_TO_WORD[last]
    return " ".join(tokens)


# Per-card audio TTS humanization. The transcript LLM is told to read content
# verbatim, but problem-set type-label abbreviations ("MC 13:", "T/F 12:",
# "MAT-CH1-3:") and short scaffolding tokens like "CH1" / "Sec. 4" are
# tokenized as letter sequences by Fish Speech and read as garble. This
# regex-based pass expands them BEFORE the transcript LLM call.
# Two label patterns: the canonical short form enforced by the card-gen
# prompt ("MC 13:", "T/F 12:") and a defense-in-depth long form for LLM
# regressions that emit the canonical problem_id ("MC-CH1-13:",
# "TF-CH1-12:", "MAT-CH1-3:", "CMP-CH2-9:"). The long form is matched first.
_PROBLEM_LABEL_LONG = re.compile(
    r"(?m)(?:^|(?<=[:\s]))(MC|TF|MAT|CMP)-CH\d+(?:-(\d+))?-(\d+(?:\.\d+)?)\s*:"
)
_PROBLEM_LABEL_SHORT = re.compile(
    r"(?m)(?:^|(?<=[:\s]))(MC|T/F)\s+(\d+(?:\.\d+)?)\s*:"
)
_LABEL_EXPANSION = {
    "MC": "Multiple choice",
    "T/F": "True or false",
    "TF": "True or false",
    "MAT": "Matching",
    "CMP": "Completion",
}


# Canonical reference for short tokens that appear in citation/content keys
# and chapter slugs (e.g. `CH07` -> "Chapter", `SI` -> "Supplementary
# Information"). Wired into the bookend chapter-form rendering only -- the
# in-prose `_CHAPTER_BARE` / `_SECTION_BARE` substitutions and the
# `humanize_citation_key` path keep their existing behavior so per-card
# scaffolding tokens like "MC-CH1-13:" survive until the prose expander.
# Future LLM-fallback lookups (see `_llm_guess_shorthand`) fall back to this
# dict before guessing.
SHORTHAND_EXPANSIONS: dict[str, str] = {
    "CH": "Chapter",
    "SI": "Supplementary Information",
    "S": "Section",
    "SEC": "Section",
    "PART": "Part",
    "APP": "Appendix",
}


def _llm_guess_shorthand(token: str) -> str | None:
    """Guess the spoken expansion of a short token via a small LLM.

    Inert stub for the user's 2026-05-19 request: prepopulate
    `SHORTHAND_EXPANSIONS` for the known cases, then fall back to a small
    LLM (e.g. Claude Haiku or GPT-nano) for unknowns. Returns `None` today;
    a future wiring will issue a one-shot prompt with the token + an example
    of the canonical-expansion shape and parse the response. Kept here so
    call sites can be wired now without depending on the LLM being live.

    Args:
        token: The uppercase shorthand token (e.g. `"APP"`, `"FIG"`).

    Returns:
        The spoken expansion, or `None` if no guess is available.
    """
    # TODO(2026-05-19): wire Haiku/GPT-nano fallback per user request.
    _ = token
    return None

# Negative lookbehind shared by all chapter / section patterns: skip tokens
# preceded by another letter, digit, hyphen, or underscore (i.e. identifier-
# like contexts such as ``MC-CH1-13`` or ``alcamo2010_CH01.problem...``).
_CHAPTER_TOKEN = re.compile(
    r"(?<![A-Za-z0-9_\-])Ch(?:apter)?\.?\s*(\d+)\b", re.IGNORECASE
)
_CHAPTER_BARE = re.compile(r"(?<![A-Za-z0-9_\-])CH(\d+)\b")
_SECTION_TOKEN = re.compile(
    r"(?<![A-Za-z0-9_\-])Sec(?:tion)?\.?\s*(\d+)\b", re.IGNORECASE
)
_SECTION_BARE = re.compile(r"(?<![A-Za-z0-9_\-])SEC(\d+)\b")
# Lettered choice labels at the start of a line — e.g. MC stems and Matching
# Column-B options. Fish Speech reads "(a)" as the phonetic glyph sequence
# (something like "pee a oh"), derailing the choice. Strip the parens and
# uppercase the letter so it reads as "A." with a natural pause from the
# period. Line-anchored so inline back-references like "see (a) above" in
# body prose are not transformed.
_CHOICE_LABEL = re.compile(r"(?m)^\(([a-z])\)\s+")
# Inline parens around prose (e.g. ``(Bacillus anthracis)`` inside an image
# summary, ``(see above)``) — Fish Speech literally speaks "open parenthesis"
# / "close parenthesis" instead of the natural read. Replace with commas.
# Constraints: content must start with a LETTER (skips math like ``(2x+1)``,
# ``(x_1)``) and be at least 2 chars (skips single-letter ``(a)`` which is
# either handled by ``_CHOICE_LABEL`` at line start or preserved inline as a
# legitimate back-reference).
_INLINE_PAREN = re.compile(r"\(([A-Za-z][^()]{1,})\)")
# Pause-tag literals injected after the choice letter so Fish stops running
# "A." straight into the option text. Mid-chunk pause tags are preserved by
# ``swanki.audio._common.append_chunk_pause``; only chunk-boundary tags are
# stripped, so this is safe.
_CHOICE_PAUSE_FISH = "[short pause]"
_CHOICE_PAUSE_ELEVENLABS = '<break time="0.3s" />'


def _expand_problem_label(match: re.Match[str]) -> str:
    label = match.group(1)
    expanded = _LABEL_EXPANSION.get(label)
    if expanded is None:
        return match.group(0)
    # The long form has three groups (label, optional occurrence, item); the
    # short form has two (label, item) and no occurrence group.
    groups = match.groups()
    if len(groups) == 3:
        occ, num = groups[1], groups[2]
        if occ is not None:
            return f"{expanded} set {occ} {num}:"
        return f"{expanded} {num}:"
    return f"{expanded} {groups[1]}:"


def humanize_card_text_for_tts(text: str, provider: str = "fish_speech") -> str:
    """Expand abbreviations that confuse Fish Speech into spoken forms.

    Designed for per-card complementary-audio transcripts. Applied BEFORE the
    transcript LLM call so the LLM (and downstream TTS) sees natural prose.

    Args:
        text: The card text to humanize.
        provider: TTS provider name (``"fish_speech"`` or ``"elevenlabs"``).
            Drives the pause-tag form injected after choice letters.

    Expansions
    ----------
    - Problem-set type labels:
      ``MC 13:`` → ``Multiple choice 13:``
      ``T/F 12:`` → ``True or false 12:``
      ``MC-CH1-13:`` (LLM regression) → ``Multiple choice 13:``
      ``MAT-CH1-3:``                  → ``Matching 3:``
      ``TF-CH1-12:``                  → ``True or false 12:``
      ``CMP-CH2-9:``                  → ``Completion 9:``
    - Chapter / section scaffolding:
      ``CH1`` / ``Ch. 1`` / ``Chapter 1`` → ``chapter 1``
      ``SEC4`` / ``Sec. 4`` / ``Section 4`` → ``section 4``
    - Lettered choice labels at start of line (MC stems, Matching options),
      with a provider-specific pause tag inserted after the letter so the
      letter doesn't run straight into the option text:
      ``(a) milk``  → ``A. [short pause] milk``  (fish)
      ``(c) Viruses`` → ``C. <break time="0.3s" /> Viruses``  (elevenlabs)
    - Inline ``(prose)`` parens (e.g. image-summary citations like
      ``(Bacillus anthracis)``, or back-references like ``(see above)``):
      replaced with comma-delimited form so Fish stops reading "open
      parenthesis" / "close parenthesis" literally. Math like ``(2x+1)``
      is preserved (content must start with a letter to qualify).

    Notes:
        - ``P``/``Pt.`` (part) is intentionally NOT expanded — too many false
          positives in chemistry/biology body text where ``P`` is a single
          letter (phosphorus, probability symbols, etc.).
        - The label regex anchors to start-of-line OR after whitespace/colon
          so it does not eat embedded mentions inside body prose.
        - Single-letter inline parens like ``compare (a) above`` are
          preserved — they never reach Fish-Speech as standalone choice
          labels and are read naturally in prose context.
    """
    if not text:
        return text

    pause_tag = (
        _CHOICE_PAUSE_FISH if provider == "fish_speech" else _CHOICE_PAUSE_ELEVENLABS
    )

    def _ch(m: re.Match[str]) -> str:
        return f"chapter {int(m.group(1))}"

    def _sec(m: re.Match[str]) -> str:
        return f"section {int(m.group(1))}"

    def _choice(m: re.Match[str]) -> str:
        return f"{m.group(1).upper()}. {pause_tag} "

    # Long form first so "TF-CH1-12:" expands to "True or false 12:" before
    # the short pattern sees a leading "T/F " from a stray prefix.
    out = _PROBLEM_LABEL_LONG.sub(_expand_problem_label, text)
    out = _PROBLEM_LABEL_SHORT.sub(_expand_problem_label, out)
    out = _CHOICE_LABEL.sub(_choice, out)
    # Inline (prose) parens — strip to commas. Runs AFTER choice-label
    # expansion so single-letter "(a)" at line start is already converted
    # and only multi-char inline parens remain to match. Skips content that
    # contains "_" or "^" (math subscripts / superscripts) so identifiers
    # like ``(x_1)`` or ``(W^T)`` survive untouched.
    def _strip_paren(m: re.Match[str]) -> str:
        content = m.group(1)
        if "_" in content or "^" in content:
            return m.group(0)
        return f", {content},"

    out = _INLINE_PAREN.sub(_strip_paren, out)
    # int() on the captured digits drops leading zeros so "CH01" reads as
    # "chapter 1" not "chapter oh one".
    out = _CHAPTER_TOKEN.sub(_ch, out)
    out = _CHAPTER_BARE.sub(_ch, out)
    out = _SECTION_TOKEN.sub(_sec, out)
    out = _SECTION_BARE.sub(_sec, out)
    return out
