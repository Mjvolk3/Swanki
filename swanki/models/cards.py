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
from typing import List, Optional, Literal
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
    
    @field_validator('text')
    def validate_cloze_format(cls, v):
        """Validate cloze deletion format and fix common issues.
        
        Ensures proper {{c1::text}} format and converts other cloze numbers to c1.
        """
        import re
        
        # Fix single braces to double braces for cloze deletions
        if '{c' in v and '{{c' not in v:
            v = re.sub(r'\{c(\d+)::', r'{{c1::', v)
            v = re.sub(r'([^}])\}([^}]|$)', r'\1}}\2', v)
        
        # Convert all cloze numbers (c2, c3, etc.) to c1 for simplicity
        v = re.sub(r'\{\{c\d+::', '{{c1::', v)
        
        # Ensure all cloze deletions are properly closed
        if '{{c1::' in v:
            # Count opening and closing braces
            opening_count = v.count('{{c1::')
            closing_count = v.count('}}')
            
            # If we have cloze openings but not enough closings, try to fix
            if opening_count > closing_count:
                # Find positions where we might be missing closing braces
                import re
                # Replace single } with }} at the end of cloze deletions
                v = re.sub(r'(\{\{c1::[^}]+)\}([^}]|$)', r'\1}}\2', v)
        
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