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

from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Literal


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
    """
    front: CardContent
    back: CardContent
    tags: List[str] = Field(default_factory=list)
    difficulty: Literal["easy", "medium", "hard"] = "medium"
    
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
        'Guido1991: What is Python?'
        """
        if citation_key and not self.front.text.startswith(citation_key):
            self.front.text = f"{citation_key}: {self.front.text}"
    
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
        if citation_key and not front_text.startswith(f"@{citation_key}:"):
            front_text = f"@{citation_key}: {front_text}"
        
        # Format tags
        formatted_tags = format_tags(self.tags, tag_format)
        
        # Check if this is a cloze card
        is_cloze = "{{c" in front_text or "{c1::" in front_text
        
        # Format based on card type and whether audio is included
        if is_cloze:
            # Cloze cards don't need back content or back audio
            # Fix single braces to double braces
            front_text = front_text.replace("{c1::", "{{c1::").replace("}}", "}")
            if "}}" not in front_text:
                front_text = front_text.replace("}", "}}")
            
            md = f"## {front_text}\n\n"
            
            # Add front image if present
            if self.front.image_path:
                md += f"![Image]({self.front.image_path})\n\n"
            
            if include_audio and audio_front_uri:
                md += f"[audio-front]({audio_front_uri})\n\n"
            
            if formatted_tags:
                md += f"#{', #'.join(formatted_tags)}\n\n"
        elif include_audio and audio_front_uri and audio_back_uri:
            # Regular cards with audio
            md = f"## {front_text}\n\n"
            
            # Add front image if present
            if self.front.image_path:
                md += f"![Image]({self.front.image_path})\n\n"
            
            md += f"[audio-front]({audio_front_uri})\n"
            md += " % \n"
            md += f"[audio-back]({audio_back_uri})\n\n"
            
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