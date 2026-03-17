"""
swanki/models/cards.py
[[swanki.models.cards]]
https://github.com/Mjvolk3/Swanki/tree/main/swanki/models/cards.py
Test file: tests/test_cards.py

Data models for Anki flashcard generation.

Classes
-------
CardContent
    Structured content for one side of a flashcard
PlainCard
    Complete flashcard with front/back content and metadata
CardGenerationResponse
    Response containing generated cards and processing metadata

Examples:
--------
>>> from swanki.models.cards import PlainCard, CardContent
>>>
>>> # Create a simple flashcard
>>> card = PlainCard(
...     front=CardContent(text="What is Python?"),
...     back=CardContent(text="A high-level programming language"),
...     tags=["programming", "python"],
...     difficulty="easy"
... )
>>>
>>> # Convert to markdown format
>>> markdown = card.to_md()
"""

import logging
import re
import uuid
from typing import Literal

from pydantic import BaseModel, Field, field_validator, model_validator

logger = logging.getLogger(__name__)


class CardContent(BaseModel):
    """Structured content for a card side.

    Represents the content for either the front or back of a flashcard,
    including text, LaTeX requirements, audio hints, and optional images.

    Parameters
    ----------
    text : str
        The main text content (1-500 characters)
    requires_latex : bool, optional
        Whether the text contains LaTeX that needs rendering (default is False)
    audio_hint : str, optional
        Pronunciation guide or hint for text-to-speech generation
    image_path : str, optional
        Path to an image file to include with this card side

    Attributes:
    ----------
    text : str
        The main text content
    requires_latex : bool
        LaTeX rendering flag
    audio_hint : str or None
        TTS pronunciation guide
    image_path : str or None
        Path to associated image

    Examples:
    --------
    >>> content = CardContent(
    ...     text="What is the derivative of x²?",
    ...     requires_latex=True
    ... )
    >>>
    >>> # With image
    >>> content_with_image = CardContent(
    ...     text="Identify this structure",
    ...     image_path="images/cell_diagram.png"
    ... )
    """

    text: str = Field(..., min_length=1, max_length=500)
    requires_latex: bool = Field(default=False)
    audio_hint: str | None = Field(None, description="Pronunciation guide for TTS")
    image_path: str | None = Field(
        None, description="Path to image file for this card side"
    )
    image_summary: str | None = Field(
        None, description="Description of the image for audio generation"
    )

    @field_validator("text")
    def validate_text_content(cls, v):
        """Validate text content for cloze format and forbidden references.

        Combines validation for cloze deletion format and reference checking.
        """
        import re

        # First, fix cloze deletion format
        # Fix single braces to double braces for cloze deletions
        if "{c" in v and "{{c" not in v:
            v = re.sub(r"\{c(\d+)::", r"{{c1::", v)
            v = re.sub(r"([^}])\}([^}]|$)", r"\1}}\2", v)

        # Check for multiple cloze numbers (c1, c2, c3) which should be avoided
        cloze_pattern = r"\{\{c(\d+)::"
        cloze_numbers = re.findall(cloze_pattern, v)
        unique_numbers = set(cloze_numbers)

        if len(unique_numbers) > 1:
            # Multiple different cloze numbers - this should be split into separate cards
            raise ValueError(
                f"Card uses multiple cloze numbers ({', '.join(sorted(unique_numbers))}). "
                "Cards should use only {{c1::}} and be split into separate cards. "
                "Example: Instead of '{{c1::A}} equals {{c2::B}}', create two cards: "
                "'{{c1::A}} equals B' and 'A equals {{c1::B}}'"
            )

        # Count cloze deletions
        cloze_count = len(cloze_numbers)
        if cloze_count > 1:
            # Multiple c1s - only allowed for same concept or connected ideas
            logger.warning(
                f"Card has {cloze_count} cloze deletions. Multiple {{c1::}} should only be used "
                "when masking the same concept appearing multiple times or tightly connected ideas."
            )

        # Check cloze deletion length and nested math delimiters
        if "{{c1::" in v:
            cloze_pattern = r"\{\{c\d+::([^}]+)\}\}"
            clozes = re.findall(cloze_pattern, v)
            for cloze_content in clozes:
                # Check for nested dollar signs in cloze (this causes rendering issues)
                if cloze_content.startswith("$") and cloze_content.endswith("$"):
                    raise ValueError(
                        f"Cloze deletion contains nested math delimiters: {{{{c1::{cloze_content[:30]}...}}}}\n"
                        f"When the entire line is already in math mode ($ or $$), don't add $ inside the cloze.\n"
                        f"Example fixes:\n"
                        f"  WRONG: $$A = {{{{c1::$B + C$}}}}$$\n"
                        f"  RIGHT: $$A = {{{{c1::B + C}}}}$$\n"
                        f"  WRONG: $f(x) = {{{{c1::$2x + 1$}}}}$\n"
                        f"  RIGHT: $f(x) = {{{{c1::2x + 1}}}}$"
                    )

                # Skip word count check if it's a math expression (contains \, or other math indicators)
                if any(
                    indicator in cloze_content
                    for indicator in ["\\", "^", "_", "{", "}"]
                ):
                    continue
                # Check word count for non-math clozes
                word_count = len(cloze_content.split())
                if word_count > 5:
                    raise ValueError(
                        f"Cloze deletion is too long ({word_count} words). Maximum is 5 words.\n"
                        f"Content: '{cloze_content[:50]}...'\n"
                        f"Shorten to key terms only. Example:\n"
                        f"  WRONG: {{{{c1::techniques that add constraints or penalties to prevent overfitting}}}}\n"
                        f"  RIGHT: {{{{c1::regularization techniques}}}}"
                    )

        # Fix LaTeX/math conflicts within cloze deletions
        if "{{c1::" in v:
            # Find all cloze deletions and fix LaTeX conflicts within them
            def fix_cloze_math_conflicts(match):
                cloze_content = match.group(1)

                # Check if this cloze contains LaTeX/math
                if any(
                    indicator in cloze_content
                    for indicator in [
                        "$",
                        "\\frac",
                        "\\sum",
                        "\\int",
                        "\\begin",
                        "\\end",
                        "\\(",
                        "\\text",
                    ]
                ):
                    # First, validate and fix common LaTeX issues
                    # Fix missing parentheses in expressions like "1 - \cos(x, y)"
                    # This pattern catches: number operator \command
                    cloze_content = re.sub(
                        r"(\d+)\s*(-|\+)\s*(\\[a-zA-Z]+)", r"(\1 \2 \3", cloze_content
                    )

                    # Fix malformed summation indices
                    # Common error: \sum_{i=1}}^{m}} should be \sum_{i=1}^{m}
                    cloze_content = re.sub(
                        r"\\sum_\{([^}]+)\}\}", r"\\sum_{\1}", cloze_content
                    )
                    cloze_content = re.sub(r"\^\{([^}]+)\}\}", r"^{\1}", cloze_content)

                    # Fix }} within math expressions by adding space
                    # This prevents }} in LaTeX from being interpreted as cloze end
                    # Look for patterns like }{baz}} and change to }{baz} }
                    cloze_content = re.sub(r"(\})\}(?!\})", r"\1 }", cloze_content)

                    # Fix :: within cloze content (e.g., std::variant)
                    # Add HTML comment to prevent :: from being interpreted as cloze separator
                    cloze_content = re.sub(r"::(?!})", r":<!-- -->:", cloze_content)

                    # Ensure balanced parentheses for expressions
                    # Count parentheses and add missing ones
                    open_parens = cloze_content.count("(") - cloze_content.count("\\(")
                    close_parens = cloze_content.count(")") - cloze_content.count("\\)")
                    if open_parens > close_parens:
                        cloze_content += ")" * (open_parens - close_parens)

                    # Validate LaTeX command balance
                    # Common patterns that should be balanced
                    for cmd in ["\\frac", "\\text", "\\boldsymbol"]:
                        cmd_count = cloze_content.count(cmd + "{")
                        # Count braces that follow this command
                        pattern = re.escape(cmd) + r"\{[^}]*\}"
                        matches = re.findall(pattern, cloze_content)
                        if cmd_count > len(matches):
                            logger.warning(
                                f"Potentially unbalanced {cmd} command in cloze"
                            )

                return f"{{{{c1::{cloze_content}}}}}"

            # Apply fixes to all cloze deletions
            v = re.sub(
                r"\{\{c1::(.+?)\}\}", fix_cloze_math_conflicts, v, flags=re.DOTALL
            )

            # Ensure all cloze deletions are properly closed
            opening_count = v.count("{{c1::")
            closing_count = v.count("}}")

            # If we have cloze openings but not enough closings, try to fix
            if opening_count > closing_count:
                # Replace single } with }} at the end of cloze deletions
                v = re.sub(r"(\{\{c1::[^}]+)\}([^}]|$)", r"\1}}\2", v)

            # Validate that math equations are properly inside cloze markers
            # Check for math outside of cloze deletions in cloze cards
            cloze_pattern = r"\{\{c\d+::([^}]+)\}\}"
            clozes = list(re.finditer(cloze_pattern, v))

            if clozes:
                # This is a cloze card
                # Check if there's math notation outside the cloze markers
                # Remove all cloze content to check what's left
                text_without_clozes = re.sub(cloze_pattern, "CLOZE_PLACEHOLDER", v)

                # Check for math patterns in the remaining text
                math_patterns = [
                    r"\\[\(\[]",  # MathJax delimiters
                    r"\$",  # LaTeX delimiters
                    r"\\[a-zA-Z]+\{",  # LaTeX commands like \frac{
                    r"\^",  # Superscripts
                    r"_\{",  # Subscripts with braces
                    r"\\sum|\\int|\\prod|\\lim",  # Common math operators
                ]

                for pattern in math_patterns:
                    if re.search(pattern, text_without_clozes):
                        # Common meaningless placeholders that indicate poor card design
                        bad_placeholders = [
                            "mathjax",
                            "equation",
                            "formula",
                            "expression",
                            "math",
                            "latex",
                        ]

                        for cloze in clozes:
                            cloze_content = cloze.group(1).strip()

                            # Check if it's definitely a bad placeholder
                            is_bad_placeholder = (
                                cloze_content.lower() in bad_placeholders
                            )

                            # If it has LaTeX/math in the cloze content, it's probably OK
                            has_math_in_cloze = any(
                                re.search(p, cloze_content) for p in math_patterns
                            )

                            # If it's a bad placeholder AND there's math outside, that's an error
                            if is_bad_placeholder and not has_math_in_cloze:
                                # Double-check: is there substantial math notation outside?
                                # Remove this cloze and check if significant math remains
                                temp_text = v.replace(cloze.group(0), "TEMP")
                                math_outside = sum(
                                    1 for p in math_patterns if re.search(p, temp_text)
                                )

                                if (
                                    math_outside >= 2
                                ):  # Multiple math indicators outside
                                    raise ValueError(
                                        f"Math equation appears to be outside cloze deletion. "
                                        f"Found cloze with placeholder '{cloze_content}' but math notation exists outside. "
                                        f"For math cloze cards, the entire equation should be inside {{{{c1::equation}}}}. "
                                        f"Example: 'The equation {{{{c1::\\(E = mc^2\\)}}}} shows mass-energy equivalence.'"
                                    )

        # Note: We keep LaTeX dollar notation in the card model
        # Conversion to MathJax happens only when sending to Anki

        # Convert [latex] tags to proper format
        if "[latex]" in v or "[$]" in v:
            # These are for LaTeX image generation, not MathJax
            # Log warning as MathJax is preferred
            logger.warning(
                "Card uses LaTeX tags instead of MathJax. Consider using \\(...\\) or \\[...\\] instead."
            )

        # Basic reference check - keep simple for now
        if re.search(r"\[\d+\]", v):
            raise ValueError(
                "Text contains reference numbers like [1] or [12]. "
                "Cards must be self-contained without external references."
            )

        # Check for meta-content leakage
        meta_content_terms = [
            "focal page",
            "surrounding page",
            "context page",
            "FOCAL PAGE CONTENT",
            "CONTEXT FROM SURROUNDING",
            "focal content",
            "page content",
        ]

        text_lower = v.lower()
        for term in meta_content_terms:
            if term.lower() in text_lower:
                raise ValueError(
                    f"Text contains meta-content reference '{term}'. "
                    "Cards must ask about the actual content, not document structure. "
                    "Example fix: Instead of 'What does the focal page discuss?', "
                    "ask 'What is the purpose of backpropagation?'"
                )

        # Check for unformatted mathematical content
        # This checks for common patterns that indicate math but aren't wrapped in LaTeX

        # FIRST: Fix incomplete subscript braces (e.g., X_{0 → X_{0}, X_p} → X_{p})
        # This prevents validation errors from malformed LaTeX
        v = re.sub(
            r"([A-Z])_\{([a-z0-9]+)(?!\})", r"\1_{\2}", v
        )  # Add missing closing brace
        v = re.sub(
            r"([A-Z])_([a-z0-9]+)\}", r"\1_{\2}", v
        )  # Fix orphaned closing brace

        # Fix split subscripts like W_{i}j} → W_{ij} (brace closes too early)
        v = re.sub(r"([A-Za-z])_\{([a-z0-9]+)\}([a-z0-9]+)\}", r"\1_{\2\3}", v)

        # Also fix subscripts without any braces at all (X_0 → X_{0})
        v = re.sub(r"([A-Z])_([a-z0-9]+)(?![}{])", r"\1_{\2}", v)

        # Fix double closing braces in subscripts inside LaTeX: _{ij}} → _{ij}
        # The LLM sometimes generates extra } after subscripts
        v = re.sub(r"(_\{[^}]+\})\}", r"\1", v)

        # Auto-fix unbalanced braces inside $...$ spans
        # Missing }: $\sigma_{\mathrm{DNA}$ → $\sigma_{\mathrm{DNA}}$
        # Excess }:  $\mathrm{IPP}}$ → $\mathrm{IPP}$
        def _fix_latex_braces(m: re.Match[str]) -> str:
            content = m.group(1)
            depth = sum(1 if c == "{" else -1 if c == "}" else 0 for c in content)
            if depth > 0:
                return "$" + content + "}" * depth + "$"
            if depth < 0:
                # Strip excess closing braces from the end
                fixed = content
                for _ in range(-depth):
                    idx = fixed.rfind("}")
                    if idx >= 0:
                        fixed = fixed[:idx] + fixed[idx + 1 :]
                return "$" + fixed + "$"
            return m.group(0)

        v = re.sub(r"\$([^$]+)\$", _fix_latex_braces, v)

        # Auto-wrap bare math using span-aware checking (not lookbehind/lookahead)
        # to handle cases like $V_{i}^{\min}=$V_{i}^{\max}$=0$ where broken $
        # delimiters leave expressions bare but adjacent to $
        def _get_latex_spans(text: str) -> list[tuple[int, int]]:
            """Find all $...$ span positions in text."""
            spans: list[tuple[int, int]] = []
            for m in re.finditer(r"\$[^$]+\$", text):
                spans.append((m.start(), m.end()))
            for m in re.finditer(r"\\\(.*?\\\)", text, flags=re.DOTALL):
                spans.append((m.start(), m.end()))
            for m in re.finditer(r"\\\[.*?\\\]", text, flags=re.DOTALL):
                spans.append((m.start(), m.end()))
            return spans

        def _in_latex_span(pos: int, spans: list[tuple[int, int]]) -> bool:
            return any(start <= pos < end for start, end in spans)

        def _wrap_bare_math(text: str, pattern: str) -> str:
            """Wrap bare math expressions not inside existing $...$ spans."""
            spans = _get_latex_spans(text)
            result = []
            last_end = 0
            for m in re.finditer(pattern, text):
                if _in_latex_span(m.start(), spans):
                    continue
                result.append(text[last_end : m.start()])
                result.append(f"${m.group(0)}$")
                last_end = m.end()
            result.append(text[last_end:])
            return "".join(result)

        # Wrap subscript+superscript: V_{i}^{\max}, V_{i}^\max, V_{i}^max
        v = _wrap_bare_math(
            v,
            r"\b[A-Za-z]_\{[^}]+\}\^(?:\{[^}]+\}|\\[a-zA-Z]+|[a-z0-9]+)",
        )
        # Wrap subscript-only (uppercase letter): V_{i}
        # but not if followed by ^ (would be caught by sub+super pattern)
        v = _wrap_bare_math(v, r"\b[A-Z]_\{[^}]+\}(?!\^)")

        # Then, remove already properly formatted LaTeX to avoid false positives
        # Also remove any LaTeX commands that might remain

        # Match LaTeX with \( \) delimiters
        text_without_latex = re.sub(
            r"\\\(.*?\\\)", "LATEX_PLACEHOLDER", v, flags=re.DOTALL
        )
        # Match LaTeX with \[ \] delimiters
        text_without_latex = re.sub(
            r"\\\[.*?\\\]", "LATEX_PLACEHOLDER", text_without_latex, flags=re.DOTALL
        )
        # Match single $ delimiters - use non-greedy matching to get the shortest match
        text_without_latex = re.sub(
            r"\$[^$]+\$", "LATEX_PLACEHOLDER", text_without_latex
        )
        # Match double $$ delimiters
        text_without_latex = re.sub(
            r"\$\$[^$]+\$\$", "LATEX_PLACEHOLDER", text_without_latex
        )

        # Remove any remaining LaTeX commands (like \alpha, \beta, etc.)
        # This catches cases where LaTeX might be partially formatted or escaped
        text_without_latex = re.sub(
            r"\\(alpha|beta|gamma|delta|epsilon|theta|lambda|mu|sigma|omega|Alpha|Beta|Gamma|Delta|Theta|Lambda|Sigma|Omega)\b",
            "LATEX_CMD",
            text_without_latex,
        )

        # Also remove content inside cloze markers as it might have special formatting
        text_without_latex = re.sub(
            r"\{\{c\d+::[^}]+\}\}", "CLOZE_PLACEHOLDER", text_without_latex
        )

        # Detect bare math in text_without_latex and auto-fix in v
        # This is the safety net: anything the auto-wrap above missed gets
        # fixed here instead of raising a ValueError that crashes the pipeline.
        _skip_contexts = [
            ".com",
            ".org",
            ".edu",
            ".io",
            ".pdf",
            ".png",
            ".jpg",
            "LATEX_PLACEHOLDER",
            "CLOZE_PLACEHOLDER",
        ]

        def _context_ok(match: re.Match[str]) -> bool:
            ctx = match.string[max(0, match.start() - 10) : match.end() + 10]
            return not any(x in ctx for x in _skip_contexts)

        auto_fixed_exprs: list[str] = []

        # Pattern 1a: subscript+superscript
        pattern_sub_super = r"\b([A-Z])_\{?([a-z0-9]+)\}?\^\{?[^}]+\}?"
        for match in re.finditer(pattern_sub_super, text_without_latex):
            if _context_ok(match):
                expr = match.group(0)
                # Wrap this expression in v (outside existing $ spans)
                v = _wrap_bare_math(v, re.escape(expr))
                auto_fixed_exprs.append(expr)

        # Pattern 1b: subscript-only
        pattern_sub_only = r"\b([A-Z])_\{?([a-z0-9]+)\}?\b"
        for match in re.finditer(pattern_sub_only, text_without_latex):
            end_pos = match.end()
            if end_pos < len(text_without_latex) and text_without_latex[end_pos] == "^":
                continue
            if _context_ok(match):
                expr = match.group(0)
                if not expr.endswith("("):
                    v = _wrap_bare_math(v, re.escape(expr))
                    auto_fixed_exprs.append(expr)

        # Pattern 2: Function notation
        function_pattern = r"\b([a-z](?:_[a-z0-9]+)?)\(([A-Z][^)]*?)\)"
        _english = {
            "a",
            "an",
            "the",
            "of",
            "in",
            "on",
            "at",
            "to",
            "by",
            "as",
            "is",
            "or",
            "and",
        }
        for match in re.finditer(function_pattern, text_without_latex):
            if match.group(1) not in _english and _context_ok(match):
                expr = match.group(0)
                v = _wrap_bare_math(v, re.escape(expr))
                auto_fixed_exprs.append(expr)

        # Pattern 3: Equations with single letters
        equation_pattern = r"\b([A-Z])\s*(=|≠|≤|≥|!=|<=|>=|<|>)\s*([0-9A-Z]+)"
        for match in re.finditer(equation_pattern, text_without_latex):
            if _context_ok(match):
                expr = match.group(0)
                v = _wrap_bare_math(v, re.escape(expr))
                auto_fixed_exprs.append(expr)

        # Pattern 4: Matrix operations
        matrix_pattern = r"\(([A-Z])\s*([-+×])\s*([A-Z])\)"
        for match in re.finditer(matrix_pattern, text_without_latex):
            if match.group(1) not in ["I"] or match.group(3) in [
                "W",
                "X",
                "Y",
                "A",
                "B",
            ]:
                if _context_ok(match):
                    expr = match.group(0)
                    v = _wrap_bare_math(v, re.escape(expr))
                    auto_fixed_exprs.append(expr)

        # Pattern 5: Greek letters written out
        greek_pattern = r"\b(alpha|beta|gamma|delta|epsilon|theta|lambda|mu|sigma|omega|Alpha|Beta|Gamma|Delta|Theta|Lambda|Sigma|Omega)\b"
        for match in re.finditer(greek_pattern, text_without_latex):
            greek = match.group(0)
            # Replace bare greek word with LaTeX command in v
            v = re.sub(rf"(?<!\$)(?<!\\)\b{greek}\b(?!\$)", rf"$\\{greek}$", v)
            auto_fixed_exprs.append(greek)

        if auto_fixed_exprs:
            logger.info(
                f"Auto-fixed {len(auto_fixed_exprs)} bare math expressions: "
                f"{', '.join(auto_fixed_exprs[:5])}"
            )

        # Final brace-balance pass — auto-fix any remaining issues
        # instead of crashing the pipeline after LLM retries are exhausted.
        def _final_brace_fix(pattern: str, v_text: str) -> str:
            def _fix(m: re.Match[str]) -> str:
                content = m.group(1)
                depth = sum(1 if c == "{" else -1 if c == "}" else 0 for c in content)
                if depth > 0:
                    fixed = m.group(0).replace(
                        "$" + content + "$", "$" + content + "}" * depth + "$"
                    )
                    logger.info(
                        f"Auto-fixed missing braces: {m.group(0)[:40]} → {fixed[:40]}"
                    )
                    return fixed
                if depth < 0:
                    fixed_content = content
                    for _ in range(-depth):
                        idx = fixed_content.rfind("}")
                        if idx >= 0:
                            fixed_content = (
                                fixed_content[:idx] + fixed_content[idx + 1 :]
                            )
                    logger.info(
                        f"Auto-fixed excess braces: {m.group(0)[:40]} → ${fixed_content}$"
                    )
                    return "$" + fixed_content + "$"
                return m.group(0)

            return re.sub(pattern, _fix, v_text)

        v = _final_brace_fix(r"\$([^$]+)\$", v)

        # Also fix \(...\) delimiters
        def _fix_paren_braces(m: re.Match[str]) -> str:
            content = m.group(1)
            depth = sum(1 if c == "{" else -1 if c == "}" else 0 for c in content)
            if depth > 0:
                return "\\(" + content + "}" * depth + "\\)"
            if depth < 0:
                fixed = content
                for _ in range(-depth):
                    idx = fixed.rfind("}")
                    if idx >= 0:
                        fixed = fixed[:idx] + fixed[idx + 1 :]
                return "\\(" + fixed + "\\)"
            return m.group(0)

        v = re.sub(r"\\\((.+?)\\\)", _fix_paren_braces, v, flags=re.DOTALL)

        # Check if cloze card ends with a question mark
        if "{{c1::" in v and v.strip().endswith("?"):
            logger.warning(
                "Cloze card ends with a question mark. Cloze cards should be statements, not questions. "
                "Example: Instead of 'How does X affect {{c1::Y}}?', use 'X affects Y by {{c1::causing specific change}}'"
            )

        return v


class PlainCard(BaseModel):
    """Structured flashcard with front/back content and metadata.

    Represents a complete Anki flashcard with support for regular Q&A format
    and cloze deletions. Includes methods for adding citations and converting
    to various output formats.

    Parameters
    ----------
    front : CardContent
        Content for the front of the card
    back : CardContent
        Content for the back of the card
    tags : List[str], optional
        List of tags for organizing cards (default is empty list)
    difficulty : {'easy', 'medium', 'hard'}, optional
        Difficulty level of the card (default is 'medium')

    Attributes:
    ----------
    front : CardContent
        Front side content
    back : CardContent
        Back side content
    tags : List[str]
        Organizational tags
    difficulty : str
        Difficulty level

    Methods:
    -------
    add_citation_prefix(citation_key)
        Add a citation key prefix to the front text
    to_md(include_audio, audio_front_uri, audio_back_uri, citation_key, tag_format)
        Convert card to VSCode Anki markdown format

    Examples:
    --------
    >>> card = PlainCard(
    ...     front=CardContent(text="What is machine learning?"),
    ...     back=CardContent(text="A subset of AI that enables systems to learn from data"),
    ...     tags=["ai", "ml", "basics"],
    ...     difficulty="easy"
    ... )
    >>>
    >>> # Add citation
    >>> card.add_citation_prefix("Smith2023")
    >>>
    >>> # Convert to markdown
    >>> md = card.to_md(citation_key="Smith2023")
    >>>
    >>> # With audio URIs stored in the card
    >>> card.audio_front_uri = "audio/card_1_front.mp3"
    >>> card.audio_back_uri = "audio/card_1_back.mp3"
    >>> md_with_audio = card.to_md(include_audio=True)
    """

    front: CardContent
    back: CardContent
    tags: list[str] = Field(
        default_factory=list, min_length=1, description="At least one tag required"
    )
    difficulty: Literal["easy", "medium", "hard"] = "medium"
    # Audio file URIs - set when audio is generated
    audio_front_uri: str | None = Field(
        None, description="URI/path to front audio file"
    )
    audio_back_uri: str | None = Field(None, description="URI/path to back audio file")
    # Unique identifier for robust pairing
    card_id: str | None = Field(
        None, description="Unique card identifier for audio pairing"
    )
    # Audio transcripts for validation
    audio_front_transcript: str | None = Field(
        None, description="Generated transcript for front audio"
    )
    audio_back_transcript: str | None = Field(
        None, description="Generated transcript for back audio"
    )

    @field_validator("tags", mode="before")
    def validate_tags(cls, v):
        """Ensure at least one tag is present and tags are valid."""
        # Clean up tags - remove empty strings, whitespace, and # prefix
        cleaned_tags = []
        for tag in v:
            if tag and tag.strip():
                # Remove # prefix if present
                cleaned_tag = tag.strip().lstrip("#")
                # Replace underscores with hyphens (more standard for tags)
                cleaned_tag = cleaned_tag.replace("_", "-")
                if cleaned_tag:
                    cleaned_tags.append(cleaned_tag)

        if not cleaned_tags:
            raise ValueError(
                "Every card must have at least one meaningful tag. No tags were provided."
            )

        # Validate tag format (ensure they don't contain invalid characters)
        for i, tag in enumerate(cleaned_tags):
            if not tag.replace("-", "").replace(".", "").replace("_", "").isalnum():
                # Try to fix common issues
                # Remove any remaining invalid characters
                fixed_tag = "".join(c if c.isalnum() or c in "-." else "-" for c in tag)
                # Remove multiple consecutive hyphens
                fixed_tag = re.sub(r"-+", "-", fixed_tag)
                # Remove leading/trailing hyphens
                fixed_tag = fixed_tag.strip("-")
                if fixed_tag:
                    cleaned_tags[i] = fixed_tag
                else:
                    raise ValueError(
                        f"Invalid tag format: '{tag}'. Tags should only contain letters, numbers, hyphens, and dots."
                    )

        return cleaned_tags

    @model_validator(mode="after")
    def fix_double_header(self):
        """Fix double header issue where citation is separate from question or ## appears in text."""
        import re

        # First, check if front text has double header pattern with citation
        # Pattern: "@citation: ## Question" or "citation: ## Question"
        double_header_pattern = r"^(@?\w+(?:Et\w+)?\d{4}:?\s*):?\s*##\s*(.+)$"
        match = re.match(
            double_header_pattern, self.front.text, re.MULTILINE | re.DOTALL
        )

        if match:
            # Extract citation and question
            citation = match.group(1).strip().rstrip(":")
            question = match.group(2).strip()
            # Reconstruct properly
            self.front.text = f"{citation}: {question}"
        elif self.front.text.startswith("## "):
            # If it just starts with ## without citation, remove the ##
            self.front.text = self.front.text[3:].strip()

        return self

    @model_validator(mode="after")
    def ensure_card_id(self):
        """Ensure card has a unique ID for robust audio pairing."""
        if not self.card_id:
            self.card_id = str(uuid.uuid4())
        return self

    @model_validator(mode="after")
    def ensure_image_cards_not_cloze(self):
        """Ensure cards with images are not cloze cards."""
        # Check if this card has an image
        has_image = (self.front.image_path is not None) or (
            self.back.image_path is not None
        )

        # Check if this is a cloze card
        is_cloze = "{{c" in self.front.text or "{{c" in self.back.text

        if has_image and is_cloze:
            # Try to convert cloze to Q&A format
            import re

            cloze_pattern = r"\{\{c\d+::([^}]+)\}\}"

            if "{{c" in self.front.text:
                # Extract the cloze content
                matches = re.findall(cloze_pattern, self.front.text)
                if matches:
                    # Convert to a question format
                    base_text = re.sub(cloze_pattern, "____", self.front.text)
                    # Change to a question
                    if not base_text.endswith("?"):
                        base_text = f"What fills the blank in: {base_text}?"
                    self.front.text = base_text
                    # Put the answer in the back if it's not already there
                    if not self.back.text or self.back.text == " ":
                        self.back.text = ", ".join(matches)

                    logger.warning(
                        f"Converted image cloze card to Q&A format: {self.front.text[:50]}..."
                    )

            # If still cloze after attempted fix, raise error
            if "{{c" in self.front.text or "{{c" in self.back.text:
                raise ValueError(
                    "Image cards cannot be cloze cards. Use Q&A format instead.\n"
                    f"Current front: {self.front.text[:50]}...\n"
                    "Convert to a question like: 'What does the diagram show?'"
                )

        return self

    @model_validator(mode="after")
    def fix_cloze_card_format(self):
        """Fix common cloze card formatting issues.

        Ensures cloze deletions are in the front text, not the back.
        For cloze cards, the back should only contain supplementary info or be empty.
        """
        import re

        # Check if this is a cloze card
        has_cloze_in_front = "{{c" in self.front.text
        has_cloze_in_back = "{{c" in self.back.text

        if has_cloze_in_back and not has_cloze_in_front:
            # This is a misformatted cloze card - cloze is in the back instead of front
            logger.warning(
                "Fixing misformatted cloze card: moving cloze from back to front"
            )

            # Extract the cloze content from the back
            cloze_pattern = r"\{\{c\d+::(.+?)\}\}"
            cloze_matches = re.findall(cloze_pattern, self.back.text, re.DOTALL)

            if cloze_matches:
                # Get the cloze content
                cloze_content = cloze_matches[0]

                # Check if the front looks like a question
                if self.front.text.endswith("?"):
                    # Transform Q&A format to statement format
                    # Remove question mark and transform to statement
                    base_text = self.front.text.rstrip("?")

                    # Common question patterns to statement transformations
                    transformations = [
                        (
                            r"^What is the (.+)$",
                            r"The \1 is {{c1::" + cloze_content + "}}",
                        ),
                        (
                            r"^What are the (.+)$",
                            r"The \1 are {{c1::" + cloze_content + "}}",
                        ),
                        (r"^Which (.+)$", r"{{c1::" + cloze_content + "}} \1"),
                        (r"^How does (.+)$", r"\1 {{c1::" + cloze_content + "}}"),
                        (
                            r"^In (.+), what (.+)$",
                            r"In \1, {{c1::" + cloze_content + "}} \2",
                        ),
                    ]

                    transformed = False
                    for pattern, replacement in transformations:
                        if re.match(pattern, base_text, re.IGNORECASE):
                            self.front.text = re.sub(
                                pattern, replacement, base_text, flags=re.IGNORECASE
                            )
                            transformed = True
                            break

                    if not transformed:
                        # Generic transformation
                        self.front.text = f"{base_text} is {{{{c1::{cloze_content}}}}}"
                else:
                    # Just append the cloze to the front
                    self.front.text = f"{self.front.text} {{{{c1::{cloze_content}}}}}"

                # Clear the back text (it should only have audio for cloze cards)
                self.back.text = ""
                logger.info(f"Fixed cloze card format: '{self.front.text[:80]}...'")

        elif has_cloze_in_back and has_cloze_in_front:
            # Both front and back have cloze - this is wrong
            logger.warning(
                "Cloze card has cloze markers in both front and back - removing from back"
            )
            # Remove cloze from back
            self.back.text = re.sub(r"\{\{c\d+::[^}]+\}\}", "", self.back.text).strip()
            if not self.back.text:
                self.back.text = ""

        # Validate cloze cards don't have substantial content in back
        if has_cloze_in_front and len(self.back.text) > 50:
            logger.warning(
                f"Cloze card has substantial back content ({len(self.back.text)} chars) - this should be minimal"
            )

        return self

    def validate_audio_match(self) -> bool:
        """Validate that audio transcripts match card content.

        Checks if the generated audio transcripts are appropriate for
        the card content, particularly for cloze cards.

        Returns:
        -------
        bool
            True if transcripts match expectations, False otherwise

        Notes:
        -----
        - For cloze cards, front transcript should contain "blank"
        - Back transcript should reveal the hidden content
        - Both should include citation if present
        """
        if not self.audio_front_transcript:
            return True  # No transcript to validate

        is_cloze = "{{c" in self.front.text

        if is_cloze:
            # Front transcript should have "blank" where cloze markers are
            if "blank" not in self.audio_front_transcript.lower():
                logger.warning(
                    f"Cloze card front transcript missing 'blank': {self.card_id}"
                )
                return False

            # Back transcript should NOT have "blank"
            if (
                self.audio_back_transcript
                and "blank" in self.audio_back_transcript.lower()
            ):
                logger.warning(
                    f"Cloze card back transcript contains 'blank': {self.card_id}"
                )
                return False

        return True

    def add_citation_prefix(self, citation_key: str):
        """Add citation key to front of card.

        Prepends a citation key to the front text if not already present.
        This helps track the source of the card content.

        Parameters
        ----------
        citation_key : str
            The citation key to add (e.g., 'Smith2023')

        Examples:
        --------
        >>> card = PlainCard(
        ...     front=CardContent(text="What is Python?"),
        ...     back=CardContent(text="A programming language")
        ... )
        >>> card.add_citation_prefix("Guido1991")
        >>> print(card.front.text)
        '@Guido1991: What is Python?'
        """
        if citation_key and not self.front.text.startswith(f"@{citation_key}"):
            self.front.text = f"@{citation_key}: {self.front.text}"

    def to_md(
        self,
        include_audio: bool = False,
        audio_front_uri: str | None = None,
        audio_back_uri: str | None = None,
        citation_key: str | None = None,
        tag_format: str = "slugified",
    ) -> str:
        """Convert to markdown in VSCode Anki format.

        Generates markdown formatted for the VSCode Anki extension, with support
        for regular cards, cloze deletions, images, and audio files.

        Parameters
        ----------
        include_audio : bool, optional
            Whether to include audio links (default is False)
        audio_front_uri : str, optional
            URI for front audio file
        audio_back_uri : str, optional
            URI for back audio file
        citation_key : str, optional
            Citation key to prepend with @ symbol
        tag_format : {'slugified', 'spaces', 'raw'}, optional
            How to format tags (default is 'slugified')

        Returns:
        -------
        str
            Markdown formatted string for VSCode Anki

        Notes:
        -----
        - Automatically detects and handles cloze deletion cards
        - Cloze cards use {{c1::text}} syntax
        - Regular cards use '##' for questions and '%' separator
        - Tags are formatted with '#' prefix

        Examples:
        --------
        >>> card = PlainCard(
        ...     front=CardContent(text="What is Python?"),
        ...     back=CardContent(text="A programming language"),
        ...     tags=["programming", "python"]
        ... )
        >>> print(card.to_md())
        ## What is Python?

        A programming language

        #programming, #python

        >>> # With audio
        >>> md_with_audio = card.to_md(
        ...     include_audio=True,
        ...     audio_front_uri="audio/q1.mp3",
        ...     audio_back_uri="audio/a1.mp3"
        ... )
        """
        # Import here to avoid circular imports
        from ..utils.formatting import format_tags

        # Add citation key prefix if provided and not already present
        front_text = self.front.text
        if citation_key:
            # Import here to avoid circular imports
            from ..utils.formatting import humanize_citation_key

            humanized = humanize_citation_key(citation_key)
            # Check if citation is already present (either raw or humanized)
            if not (
                front_text.startswith(f"@{citation_key}:")
                or front_text.startswith(f"{humanized}:")
            ):
                # Use @citation_key format for card text (not humanized)
                front_text = f"@{citation_key}: {front_text}"

        # Format tags
        formatted_tags = format_tags(self.tags, tag_format)

        # Use stored audio URIs if available, otherwise use passed parameters
        front_uri = self.audio_front_uri if self.audio_front_uri else audio_front_uri
        back_uri = self.audio_back_uri if self.audio_back_uri else audio_back_uri

        # Check if this is a cloze card
        is_cloze = "{{c" in front_text or "{c1::" in front_text

        # Format based on card type and whether audio is included
        if is_cloze:
            md = f"## {front_text}\n\n"

            # Add front image if present
            if self.front.image_path:
                md += f"![Image]({self.front.image_path})\n\n"

            # For cloze cards with audio: use same format as regular cards
            # This ensures the AnkiProcessor can find and convert the audio links
            if include_audio and front_uri:
                md += f"[audio-front]({front_uri})\n"

            # Add separator for Extra field
            md += " % \n"

            # Back audio reveals the masked words (goes in Extra)
            if include_audio and back_uri:
                md += f"[audio-back]({back_uri})\n\n"

            if formatted_tags:
                md += f"- #{', #'.join(formatted_tags)}\n\n"
        elif include_audio and front_uri and back_uri:
            # Regular cards with audio
            md = f"## {front_text}\n\n"

            # Add front image if present
            if self.front.image_path:
                md += f"![Image]({self.front.image_path})\n\n"

            md += f"[audio-front]({front_uri})\n"
            md += " % \n"
            md += f"[audio-back]({back_uri})\n\n"

            # Add back image if present
            if self.back.image_path:
                md += f"![Image]({self.back.image_path})\n\n"

            md += f"{self.back.text}\n\n"
            if formatted_tags:
                md += f"- #{', #'.join(formatted_tags)}\n\n"
        else:
            # VSCode Anki format without audio
            md = f"## {front_text}\n\n"

            # Add front image if present
            if self.front.image_path:
                md += f"![Image]({self.front.image_path})\n\n"

            md += f"{self.back.text}\n\n"

            # Add back image if present
            if self.back.image_path:
                md += f"![Image]({self.back.image_path})\n\n"

            if formatted_tags:
                md += f"- #{', #'.join(formatted_tags)}\n\n"

        return md


class ImageCardContent(CardContent):
    """Content for image cards that requires an image summary.

    Extends CardContent to make image_summary required for cards
    that will have images attached.
    """

    image_summary: str = Field(
        ...,
        min_length=10,
        description="Required description of the image for accessibility",
    )

    @field_validator("image_summary")
    def validate_image_summary(cls, v):
        """Ensure image summary is meaningful."""
        if len(v.split()) < 5:
            raise ValueError("Image summary must be at least 5 words to be meaningful")
        return v


class ImageCard(BaseModel):
    """Flashcard specifically for image-based content.

    Ensures that cards with images always have proper summaries
    for accessibility and audio generation.
    """

    front: ImageCardContent | CardContent
    back: ImageCardContent | CardContent
    tags: list[str] = Field(default_factory=list, min_length=1)
    difficulty: Literal["easy", "medium", "hard"] = "medium"
    card_id: str | None = Field(None)

    @model_validator(mode="after")
    def ensure_at_least_one_image_summary(self):
        """Ensure at least one side has an image summary."""
        front_has_summary = isinstance(self.front, ImageCardContent) or (
            hasattr(self.front, "image_summary") and self.front.image_summary
        )
        back_has_summary = isinstance(self.back, ImageCardContent) or (
            hasattr(self.back, "image_summary") and self.back.image_summary
        )

        if not (front_has_summary or back_has_summary):
            raise ValueError(
                "Image cards must have an image summary on at least one side"
            )

        return self

    def to_plain_card(self) -> PlainCard:
        """Convert to PlainCard for compatibility."""
        return PlainCard(
            front=self.front,
            back=self.back,
            tags=self.tags,
            difficulty=self.difficulty,
            card_id=self.card_id,
        )


class CardGenerationResponse(BaseModel):
    """Structured response for card generation.

    Contains the generated cards and metadata about the generation process,
    including any sections that were skipped.

    Parameters
    ----------
    cards : List[PlainCard]
        List of generated flashcards
    skipped_sections : List[str], optional
        Sections not suitable for card generation (default is empty list)

    Attributes:
    ----------
    cards : List[PlainCard]
        Generated flashcards
    skipped_sections : List[str]
        Sections that were skipped

    Raises:
    ------
    ValueError
        If no cards are generated (empty cards list)

    Examples:
    --------
    >>> from swanki.models.cards import CardGenerationResponse, PlainCard
    >>>
    >>> response = CardGenerationResponse(
    ...     cards=[
    ...         PlainCard(
    ...             front=CardContent(text="Q1"),
    ...             back=CardContent(text="A1")
    ...         )
    ...     ],
    ...     skipped_sections=["References", "Acknowledgments"]
    ... )
    """

    cards: list[PlainCard]
    skipped_sections: list[str] = Field(
        default_factory=list, description="Sections not suitable for cards"
    )

    @field_validator("cards")
    def validate_card_count(cls, v):
        """Validate that at least one card is generated.

        Parameters
        ----------
        v : List[PlainCard]
            List of cards to validate

        Returns:
        -------
        List[PlainCard]
            The validated list of cards

        Raises:
        ------
        ValueError
            If the cards list is empty
        """
        if len(v) == 0:
            raise ValueError("Must generate at least one card")
        return v


class CardFeedback(BaseModel):
    """Structured feedback for card quality issues.

    Used in the self-refine pattern to provide specific feedback
    about issues found in generated cards and whether refinement is needed.

    Parameters
    ----------
    feedback : List[str]
        List of specific issues to fix in the cards
    done : bool
        True if cards meet quality standards, False if refinement needed

    Examples:
    --------
    >>> feedback = CardFeedback(
    ...     feedback=[
    ...         "Card 1: Contains external reference [1]",
    ...         "Card 3: Uses generic tag #equation instead of #calculus.derivatives"
    ...     ],
    ...     done=False
    ... )
    """

    feedback: list[str] = Field(
        description="List of specific issues to fix in the cards"
    )
    done: bool = Field(
        description="True if cards meet quality standards, False if refinement needed"
    )


class CardIssue(BaseModel):
    """Individual issue found in a card.

    Provides structured information about a specific quality issue
    in a card, including the type of issue and how to fix it.

    Parameters
    ----------
    card_index : int
        Index of the card with the issue (0-based)
    issue_type : str
        Type of issue detected
    description : str
        Detailed description of the issue
    example : str
        Example from the card showing the issue
    suggestion : str
        How to fix this issue
    """

    card_index: int
    issue_type: Literal[
        "external_reference",
        "insufficient_context",
        "generic_tags",
        "rote_memorization",
        "math_formatting",
        "cloze_problem",
        "undefined_acronym",
        "author_centric",
        "image_issue",
        "audio_issue",
        "trivial_content",
        "missing_educational_value",
        "random_equation_detail",
        "answer_in_question",
        "cloze_with_question",
        "missing_context",
        "meta_content_leakage",
        "instruction_leakage",
        "structural_reference",
    ]
    description: str
    example: str = Field(description="Example from the card showing the issue")
    suggestion: str = Field(description="How to fix this issue")


class AudioTranscriptFeedback(BaseModel):
    """Feedback for audio transcript quality.

    Used to evaluate whether generated audio transcripts are suitable
    for text-to-speech and contain all necessary information.

    Parameters
    ----------
    feedback : List[str]
        List of specific issues in the transcript
    done : bool
        True if transcript is ready for audio generation
    """

    feedback: list[str] = Field(description="List of specific transcript issues to fix")
    done: bool = Field(
        description="True if transcript is suitable for audio generation"
    )


class LectureTranscriptFeedback(BaseModel):
    r"""Feedback for lecture transcript quality.

    Used to evaluate whether generated lecture transcripts are suitable
    for audio generation and follow content guidelines.

    Parameters
    ----------
    feedback : List[str]
        List of specific issues in the transcript
    done : bool
        True if transcript meets quality standards

    Examples:
    --------
    >>> feedback = LectureTranscriptFeedback(
    ...     feedback=[
    ...         "Chars 0-8000: Contains LaTeX table \\begin{tabular} at position 1234",
    ...         "Chars 16000-24000: Citation '(Smith et al., 2009)' found at position 18500"
    ...     ],
    ...     done=False
    ... )
    """

    feedback: list[str] = Field(
        description="List of specific issues found (e.g., 'Chars 0-8000: Contains LaTeX table instead of summary')"
    )
    done: bool = Field(
        description="True if transcript passes all quality checks, False if refinement needed"
    )

    # Length tracking (NEW)
    word_count: int = Field(
        description="Approximate word count of transcript (count words, not tokens)"
    )
    meets_length_target: bool = Field(
        description="True if word count is <= 60% of source (50% target + 10% tolerance)"
    )
    si_balance: bool = Field(
        default=True,
        description="True if SI content does not dominate the section",
    )


class RefinementHistory(BaseModel):
    """Track refinement history for debugging and analysis.

    Keeps a record of all refinement iterations including the original
    cards, feedback received, and refined versions.

    Parameters
    ----------
    iterations : List[Dict]
        List of refinement iterations

    Methods:
    -------
    add_iteration(cards, feedback, refined_cards)
        Add a new refinement iteration to history
    """

    iterations: list[dict] = Field(default_factory=list)

    def add_iteration(
        self,
        cards: list[PlainCard],
        feedback: CardFeedback,
        refined_cards: list[PlainCard] | None = None,
    ):
        """Add a refinement iteration to history.

        Parameters
        ----------
        cards : List[PlainCard]
            Cards before refinement
        feedback : CardFeedback
            Feedback received for these cards
        refined_cards : List[PlainCard], optional
            Cards after refinement (if refinement occurred)
        """
        iteration = {
            "iteration_number": len(self.iterations) + 1,
            "original_cards": [card.model_dump() for card in cards],
            "feedback": feedback.model_dump(),
            "refined_cards": [card.model_dump() for card in refined_cards]
            if refined_cards
            else None,
        }
        self.iterations.append(iteration)


class EnhancedCardGenerationResponse(CardGenerationResponse):
    """Extended response with quality tracking.

    Adds quality metrics and refinement tracking to the standard
    card generation response.

    Parameters
    ----------
    cards : List[PlainCard]
        List of generated flashcards
    skipped_sections : List[str], optional
        Sections not suitable for card generation
    quality_score : float, optional
        Self-assessed quality score 0-1
    iteration : int, optional
        Refinement iteration number
    refinement_history : RefinementHistory, optional
        Full history of refinements
    """

    quality_score: float | None = Field(
        None, description="Self-assessed quality score 0-1"
    )
    iteration: int | None = Field(None, description="Refinement iteration number")
    refinement_history: RefinementHistory | None = Field(
        None, description="History of refinement iterations"
    )
