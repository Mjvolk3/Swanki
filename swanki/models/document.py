"""Data models for document structure and content representation.

This module defines data structures for representing document summaries
and image content extracted from academic PDFs. These models are used
throughout the processing pipeline to maintain structured information.

Classes
-------
ImageSummary
    Summary and metadata for an extracted image
DocumentSummary
    Comprehensive summary of a document with metadata

Examples
--------
>>> from swanki.models.document import DocumentSummary
>>> 
>>> summary = DocumentSummary(
...     title="Deep Learning Fundamentals",
...     authors=["Smith, J.", "Doe, A."],
...     main_topic="Neural network architectures",
...     key_contributions=["New activation function", "Improved backprop"],
...     methodology="Experimental study with benchmarks",
...     summary="This paper presents..." # 200-500 words
... )
"""

from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Dict


class ImageSummary(BaseModel):
    """Structured summary and metadata for an extracted image.
    
    Represents an image extracted from a document page, including its
    location, URL, descriptive summary, and any text content extracted
    from the image (such as equations or labels).
    
    Parameters
    ----------
    page_idx : int
        Zero-based page index where the image was found
    image_url : str
        URL or path to the extracted image file
    summary : str
        Detailed description of the image content (up to 300 words)
    extracted_text : str, optional
        Any text or equations extracted from the image via OCR
    
    Attributes
    ----------
    page_idx : int
        Page index in source document
    image_url : str
        Image file location
    summary : str
        Descriptive summary
    extracted_text : str or None
        OCR-extracted text content
    
    Raises
    ------
    ValueError
        If summary exceeds 150 words
    
    Examples
    --------
    >>> image = ImageSummary(
    ...     page_idx=5,
    ...     image_url="images/figure_1.png",
    ...     summary="Diagram showing neural network architecture with 3 hidden layers",
    ...     extracted_text="Input Layer -> Hidden Layer 1 -> Hidden Layer 2 -> Output"
    ... )
    """
    page_idx: int
    image_url: str
    summary: str = Field(..., description="Detailed description (up to 300 words)")
    extracted_text: Optional[str] = Field(None, description="Any text/equations in image")
    
    @field_validator('summary')
    def summary_length(cls, v):
        """Validate that image summary is reasonably sized.
        
        Ensures the summary doesn't exceed 300 words to maintain
        clarity while allowing for detailed technical descriptions.
        
        Parameters
        ----------
        v : str
            The summary text to validate
        
        Returns
        -------
        str
            The validated summary text
        
        Raises
        ------
        ValueError
            If summary exceeds 300 words
        """
        words = len(v.split())
        if words > 300:  # Increased limit for complex technical images
            raise ValueError(f"Summary too long: {words} words")
        return v


class DocumentSummary(BaseModel):
    """Comprehensive summary of a document with metadata.
    
    Captures the essential information from an academic document including
    bibliographic data, key contributions, methodology, and a structured
    summary. Also maintains dictionaries of acronyms and technical terms
    for reference.
    
    Parameters
    ----------
    title : str
        Document title
    authors : List[str]
        List of author names
    main_topic : str
        Primary topic or field of the document
    key_contributions : List[str]
        Main contributions (max 5 items)
    methodology : str
        Research methodology description
    acronyms : Dict[str, str], optional
        Dictionary mapping acronyms to their definitions
    technical_terms : Dict[str, str], optional
        Dictionary of technical terms and their definitions
    summary : str
        Comprehensive summary (200-500 words)
    
    Attributes
    ----------
    title : str
        Document title
    authors : List[str]
        Author list
    main_topic : str
        Primary topic
    key_contributions : List[str]
        Key contributions (max 5)
    methodology : str
        Methodology description
    acronyms : Dict[str, str]
        Acronym definitions
    technical_terms : Dict[str, str]
        Technical term definitions
    summary : str
        Full summary text
    
    Raises
    ------
    ValueError
        If summary is not between 200-500 words
        If more than 5 key contributions provided
    
    Examples
    --------
    >>> doc_summary = DocumentSummary(
    ...     title="Attention Is All You Need",
    ...     authors=["Vaswani, A.", "Shazeer, N.", "Parmar, N."],
    ...     main_topic="Transformer architecture for NLP",
    ...     key_contributions=[
    ...         "Introduced self-attention mechanism",
    ...         "Eliminated recurrence in sequence models",
    ...         "Achieved SOTA on translation tasks"
    ...     ],
    ...     methodology="Architecture design and empirical evaluation",
    ...     acronyms={"NLP": "Natural Language Processing", "SOTA": "State of the Art"},
    ...     technical_terms={
    ...         "self-attention": "Mechanism to relate different positions in a sequence"
    ...     },
    ...     summary="This paper introduces the Transformer..." # 200-500 word summary
    ... )
    """
    title: str
    authors: List[str]
    main_topic: str
    key_contributions: List[str] = Field(..., max_length=5)
    methodology: str
    acronyms: Dict[str, str] = Field(default_factory=dict, description="Acronym definitions")
    technical_terms: Dict[str, str] = Field(default_factory=dict, description="Technical term definitions")
    summary: str = Field(..., description="200-500 word summary")
    
    @field_validator('summary')
    def summary_length(cls, v):
        """Validate document summary length.
        
        Ensures the summary is comprehensive yet concise, falling within
        the 200-500 word range suitable for document overview.
        
        Parameters
        ----------
        v : str
            The summary text to validate
        
        Returns
        -------
        str
            The validated summary text
        
        Raises
        ------
        ValueError
            If summary is not between 200-500 words
        """
        words = len(v.split())
        if not 200 <= words <= 500:
            raise ValueError(f"Summary should be 200-500 words, got {words}")
        return v