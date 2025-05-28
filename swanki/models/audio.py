"""Data models for audio transcript generation.

This module defines data structures for representing audio transcripts
used in text-to-speech (TTS) generation for flashcards. Transcripts
include both the original content and TTS-optimized versions.

Classes
-------
AudioTranscript
    Structured transcript data for TTS generation

Examples
--------
>>> from swanki.models.audio import AudioTranscript
>>> 
>>> transcript = AudioTranscript(
...     citation_key="Smith2023",
...     card_id="card_001",
...     content="What is machine learning?",
...     tts_version="What is machine learning? (pronounced: muh-sheen lur-ning)"
... )
>>> 
>>> # Get filename for saving
>>> filename = transcript.get_filename()
>>> print(filename)
'Smith2023_card_001.txt'
"""

from pydantic import BaseModel, Field


class AudioTranscript(BaseModel):
    """Structured audio transcript for TTS generation.
    
    Represents a transcript prepared for text-to-speech conversion,
    including both the original content and a TTS-optimized version
    with pronunciation hints.
    
    Parameters
    ----------
    citation_key : str
        Citation key identifying the source document
    card_id : str
        Unique identifier for the associated flashcard
    content : str
        Original text content
    tts_version : str
        TTS-friendly version with pronunciation guides
    
    Attributes
    ----------
    citation_key : str
        Source document citation
    card_id : str
        Flashcard identifier
    content : str
        Original content
    tts_version : str
        TTS-optimized content
    
    Methods
    -------
    get_filename()
        Generate a standardized filename for the transcript
    
    Examples
    --------
    >>> transcript = AudioTranscript(
    ...     citation_key="Doe2024",
    ...     card_id="q_42",
    ...     content="What is the P vs NP problem?",
    ...     tts_version="What is the P versus N P problem?"
    ... )
    >>> 
    >>> # Save transcript with generated filename
    >>> filename = transcript.get_filename()
    >>> print(filename)
    'Doe2024_q_42.txt'
    """
    citation_key: str
    card_id: str
    content: str
    tts_version: str = Field(..., description="TTS-friendly version with pronunciations")
    
    def get_filename(self) -> str:
        """Generate a standardized filename for the transcript.
        
        Creates a filename using the citation key and card ID,
        ensuring consistent naming across the system.
        
        Returns
        -------
        str
            Filename in format '{citation_key}_{card_id}.txt'
        
        Examples
        --------
        >>> transcript = AudioTranscript(
        ...     citation_key="Einstein1905",
        ...     card_id="relativity_01",
        ...     content="E=mc²",
        ...     tts_version="E equals m c squared"
        ... )
        >>> transcript.get_filename()
        'Einstein1905_relativity_01.txt'
        """
        return f"{self.citation_key}_{self.card_id}.txt"