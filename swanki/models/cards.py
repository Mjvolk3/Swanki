"""Data models for Anki flashcard generation.

This module defines the core data structures for representing flashcards,
including card content, formatting options, and generation responses.
Supports both regular Q&A cards and cloze deletion cards.

Classes
-------
CardContent
    Structured content for one side of a flashcard
PlainCard
    Complete flashcard with front/back content and metadata
CardGenerationResponse
    Response containing generated cards and processing metadata

Examples
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

from pydantic import BaseModel, Field, field_validator, model_validator
from typing import List, Optional, Literal, Union, Dict
import uuid
import logging

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
    
    Attributes
    ----------
    text : str
        The main text content
    requires_latex : bool
        LaTeX rendering flag
    audio_hint : str or None
        TTS pronunciation guide
    image_path : str or None
        Path to associated image
    
    Examples
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
    audio_hint: Optional[str] = Field(None, description="Pronunciation guide for TTS")
    image_path: Optional[str] = Field(None, description="Path to image file for this card side")
    image_summary: Optional[str] = Field(None, description="Description of the image for audio generation")
    
    @field_validator('text')
    def validate_text_content(cls, v):
        """Validate text content for cloze format and forbidden references.
        
        Combines validation for cloze deletion format and reference checking.
        """
        import re
        
        # First, fix cloze deletion format
        # Fix single braces to double braces for cloze deletions
        if '{c' in v and '{{c' not in v:
            v = re.sub(r'\{c(\d+)::', r'{{c1::', v)
            v = re.sub(r'([^}])\}([^}]|$)', r'\1}}\2', v)
        
        # Convert all cloze numbers (c2, c3, etc.) to c1 for simplicity
        v = re.sub(r'\{\{c\d+::', '{{c1::', v)
        
        # Fix LaTeX/math conflicts within cloze deletions
        if '{{c1::' in v:
            # Find all cloze deletions and fix LaTeX conflicts within them
            def fix_cloze_math_conflicts(match):
                cloze_content = match.group(1)
                
                # Check if this cloze contains LaTeX/math
                if any(indicator in cloze_content for indicator in ['$', '\\frac', '\\sum', '\\int', '\\begin', '\\end']):
                    # Fix }} within math expressions by adding space
                    # This prevents }} in LaTeX from being interpreted as cloze end
                    # Look for patterns like }{baz}} and change to }{baz} }
                    cloze_content = re.sub(r'(\})\}(?!\})', r'\1 }', cloze_content)
                    
                    # Fix :: within cloze content (e.g., std::variant)
                    # Add HTML comment to prevent :: from being interpreted as cloze separator
                    cloze_content = re.sub(r'::(?!})', r':<!-- -->:', cloze_content)
                
                return f'{{{{c1::{cloze_content}}}}}'
            
            # Apply fixes to all cloze deletions
            v = re.sub(r'\{\{c1::(.+?)\}\}', fix_cloze_math_conflicts, v, flags=re.DOTALL)
            
            # Ensure all cloze deletions are properly closed
            opening_count = v.count('{{c1::')
            closing_count = v.count('}}')
            
            # If we have cloze openings but not enough closings, try to fix
            if opening_count > closing_count:
                # Replace single } with }} at the end of cloze deletions
                v = re.sub(r'(\{\{c1::[^}]+)\}([^}]|$)', r'\1}}\2', v)
            
            # Validate that math equations are properly inside cloze markers
            # Check for math outside of cloze deletions in cloze cards
            cloze_pattern = r'\{\{c\d+::([^}]+)\}\}'
            clozes = list(re.finditer(cloze_pattern, v))
            
            if clozes:
                # This is a cloze card
                # Check if there's math notation outside the cloze markers
                # Remove all cloze content to check what's left
                text_without_clozes = re.sub(cloze_pattern, 'CLOZE_PLACEHOLDER', v)
                
                # Check for math patterns in the remaining text
                math_patterns = [
                    r'\\[\(\[]',  # MathJax delimiters
                    r'\$',         # LaTeX delimiters
                    r'\\[a-zA-Z]+\{',  # LaTeX commands like \frac{
                    r'\^',         # Superscripts
                    r'_\{',        # Subscripts with braces
                    r'\\sum|\\int|\\prod|\\lim',  # Common math operators
                ]
                
                for pattern in math_patterns:
                    if re.search(pattern, text_without_clozes):
                        # Check if the cloze content looks like a placeholder rather than actual content
                        # Be very specific about what constitutes a placeholder
                        placeholder_patterns = [
                            r'^(mathjax|equation|formula|expression|math)$',
                            r'^(the\s+)?(equation|formula|expression)$',
                        ]
                        
                        # Common meaningless placeholders that indicate poor card design
                        bad_placeholders = ['mathjax', 'equation', 'formula', 'expression', 'math', 'latex']
                        
                        for cloze in clozes:
                            cloze_content = cloze.group(1).strip()
                            
                            # Check if it's definitely a bad placeholder
                            is_bad_placeholder = cloze_content.lower() in bad_placeholders
                            
                            # If it has LaTeX/math in the cloze content, it's probably OK
                            has_math_in_cloze = any(re.search(p, cloze_content) for p in math_patterns)
                            
                            # If it's a bad placeholder AND there's math outside, that's an error
                            if is_bad_placeholder and not has_math_in_cloze:
                                # Double-check: is there substantial math notation outside?
                                # Remove this cloze and check if significant math remains
                                temp_text = v.replace(cloze.group(0), 'TEMP')
                                math_outside = sum(1 for p in math_patterns if re.search(p, temp_text))
                                
                                if math_outside >= 2:  # Multiple math indicators outside
                                    raise ValueError(
                                        f"Math equation appears to be outside cloze deletion. "
                                        f"Found cloze with placeholder '{cloze_content}' but math notation exists outside. "
                                        f"For math cloze cards, the entire equation should be inside {{{{c1::equation}}}}. "
                                        f"Example: 'The equation {{{{c1::\\(E = mc^2\\)}}}} shows mass-energy equivalence.'"
                                    )
        
        # Note: We keep LaTeX dollar notation in the card model
        # Conversion to MathJax happens only when sending to Anki
            
        # Convert [latex] tags to proper format
        if '[latex]' in v or '[$]' in v:
            # These are for LaTeX image generation, not MathJax
            # Log warning as MathJax is preferred
            logger.warning("Card uses LaTeX tags instead of MathJax. Consider using \\(...\\) or \\[...\\] instead.")
        
        # Basic reference check - keep simple for now
        if re.search(r'\[\d+\]', v):
            raise ValueError(
                "Text contains reference numbers like [1] or [12]. "
                "Cards must be self-contained without external references."
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
    
    Attributes
    ----------
    front : CardContent
        Front side content
    back : CardContent
        Back side content
    tags : List[str]
        Organizational tags
    difficulty : str
        Difficulty level
    
    Methods
    -------
    add_citation_prefix(citation_key)
        Add a citation key prefix to the front text
    to_md(include_audio, audio_front_uri, audio_back_uri, citation_key, tag_format)
        Convert card to VSCode Anki markdown format
    
    Examples
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
    tags: List[str] = Field(default_factory=list, min_length=1, description="At least one tag required")
    difficulty: Literal["easy", "medium", "hard"] = "medium"
    # Audio file URIs - set when audio is generated
    audio_front_uri: Optional[str] = Field(None, description="URI/path to front audio file")
    audio_back_uri: Optional[str] = Field(None, description="URI/path to back audio file")
    # Unique identifier for robust pairing
    card_id: Optional[str] = Field(None, description="Unique card identifier for audio pairing")
    # Audio transcripts for validation
    audio_front_transcript: Optional[str] = Field(None, description="Generated transcript for front audio")
    audio_back_transcript: Optional[str] = Field(None, description="Generated transcript for back audio")
    
    @field_validator('tags')
    def validate_tags(cls, v):
        """Ensure at least one tag is present and tags are valid."""
        # Clean up tags - remove empty strings and whitespace
        cleaned_tags = [tag.strip() for tag in v if tag and tag.strip()]
        
        if not cleaned_tags:
            raise ValueError("Every card must have at least one meaningful tag. No tags were provided.")
        
        # Validate tag format (optional - ensure they don't contain invalid characters)
        for tag in cleaned_tags:
            if not tag.replace('-', '').replace('.', '').replace('_', '').isalnum():
                raise ValueError(f"Invalid tag format: '{tag}'. Tags should only contain letters, numbers, hyphens, dots, and underscores.")
        
        return cleaned_tags
    
    @model_validator(mode='after')
    def fix_double_header(self):
        """Fix double header issue where citation is separate from question or ## appears in text."""
        import re
        
        # First, check if front text has double header pattern with citation
        # Pattern: "@citation: ## Question" or "citation: ## Question"
        double_header_pattern = r'^(@?\w+(?:Et\w+)?\d{4}:?\s*):?\s*##\s*(.+)$'
        match = re.match(double_header_pattern, self.front.text, re.MULTILINE | re.DOTALL)
        
        if match:
            # Extract citation and question
            citation = match.group(1).strip().rstrip(':')
            question = match.group(2).strip()
            # Reconstruct properly
            self.front.text = f"{citation}: {question}"
        elif self.front.text.startswith('## '):
            # If it just starts with ## without citation, remove the ##
            self.front.text = self.front.text[3:].strip()
        
        return self
    
    @model_validator(mode='after')
    def ensure_card_id(self):
        """Ensure card has a unique ID for robust audio pairing."""
        if not self.card_id:
            self.card_id = str(uuid.uuid4())
        return self
    
    
    def validate_audio_match(self) -> bool:
        """Validate that audio transcripts match card content.
        
        Checks if the generated audio transcripts are appropriate for
        the card content, particularly for cloze cards.
        
        Returns
        -------
        bool
            True if transcripts match expectations, False otherwise
        
        Notes
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
                logger.warning(f"Cloze card front transcript missing 'blank': {self.card_id}")
                return False
            
            # Back transcript should NOT have "blank"
            if self.audio_back_transcript and "blank" in self.audio_back_transcript.lower():
                logger.warning(f"Cloze card back transcript contains 'blank': {self.card_id}")
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
        
        Examples
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
    
    def to_md(self, include_audio: bool = False, audio_front_uri: Optional[str] = None, audio_back_uri: Optional[str] = None, citation_key: Optional[str] = None, tag_format: str = "slugified") -> str:
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
        
        Returns
        -------
        str
            Markdown formatted string for VSCode Anki
        
        Notes
        -----
        - Automatically detects and handles cloze deletion cards
        - Cloze cards use {{c1::text}} syntax
        - Regular cards use '##' for questions and '%' separator
        - Tags are formatted with '#' prefix
        
        Examples
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
            if not (front_text.startswith(f"@{citation_key}:") or front_text.startswith(f"{humanized}:")):
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
                md += f"#{', #'.join(formatted_tags)}\n\n"
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
                md += f"#{', #'.join(formatted_tags)}\n\n"
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
                md += f"#{', #'.join(formatted_tags)}\n\n"
        
        return md


class ImageCardContent(CardContent):
    """Content for image cards that requires an image summary.
    
    Extends CardContent to make image_summary required for cards
    that will have images attached.
    """
    image_summary: str = Field(..., min_length=10, description="Required description of the image for accessibility")
    
    @field_validator('image_summary')
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
    front: Union[ImageCardContent, CardContent]
    back: Union[ImageCardContent, CardContent] 
    tags: List[str] = Field(default_factory=list, min_length=1)
    difficulty: Literal["easy", "medium", "hard"] = "medium"
    card_id: Optional[str] = Field(None)
    
    @model_validator(mode='after')
    def ensure_at_least_one_image_summary(self):
        """Ensure at least one side has an image summary."""
        front_has_summary = isinstance(self.front, ImageCardContent) or (hasattr(self.front, 'image_summary') and self.front.image_summary)
        back_has_summary = isinstance(self.back, ImageCardContent) or (hasattr(self.back, 'image_summary') and self.back.image_summary)
        
        if not (front_has_summary or back_has_summary):
            raise ValueError("Image cards must have an image summary on at least one side")
        
        return self
    
    def to_plain_card(self) -> PlainCard:
        """Convert to PlainCard for compatibility."""
        return PlainCard(
            front=self.front,
            back=self.back,
            tags=self.tags,
            difficulty=self.difficulty,
            card_id=self.card_id
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
    
    Attributes
    ----------
    cards : List[PlainCard]
        Generated flashcards
    skipped_sections : List[str]
        Sections that were skipped
    
    Raises
    ------
    ValueError
        If no cards are generated (empty cards list)
    
    Examples
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
    cards: List[PlainCard]
    skipped_sections: List[str] = Field(default_factory=list, description="Sections not suitable for cards")
    
    @field_validator('cards')
    def validate_card_count(cls, v):
        """Validate that at least one card is generated.
        
        Parameters
        ----------
        v : List[PlainCard]
            List of cards to validate
        
        Returns
        -------
        List[PlainCard]
            The validated list of cards
        
        Raises
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
    
    Examples
    --------
    >>> feedback = CardFeedback(
    ...     feedback=[
    ...         "Card 1: Contains external reference [1]",
    ...         "Card 3: Uses generic tag #equation instead of #calculus.derivatives"
    ...     ],
    ...     done=False
    ... )
    """
    feedback: List[str] = Field(
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
        "external_reference", "insufficient_context", "generic_tags",
        "rote_memorization", "math_formatting", "cloze_problem",
        "undefined_acronym", "author_centric", "image_issue", "audio_issue"
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
    feedback: List[str] = Field(
        description="List of specific transcript issues to fix"
    )
    done: bool = Field(
        description="True if transcript is suitable for audio generation"
    )


class RefinementHistory(BaseModel):
    """Track refinement history for debugging and analysis.
    
    Keeps a record of all refinement iterations including the original
    cards, feedback received, and refined versions.
    
    Parameters
    ----------
    iterations : List[Dict]
        List of refinement iterations
    
    Methods
    -------
    add_iteration(cards, feedback, refined_cards)
        Add a new refinement iteration to history
    """
    iterations: List[Dict] = Field(default_factory=list)
    
    def add_iteration(self, cards: List[PlainCard], feedback: CardFeedback, 
                     refined_cards: Optional[List[PlainCard]] = None):
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
            "refined_cards": [card.model_dump() for card in refined_cards] if refined_cards else None
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
    quality_score: Optional[float] = Field(
        None, description="Self-assessed quality score 0-1"
    )
    iteration: Optional[int] = Field(
        None, description="Refinement iteration number"
    )
    refinement_history: Optional[RefinementHistory] = Field(
        None, description="History of refinement iterations"
    )