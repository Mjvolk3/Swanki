"""
swanki/models/document.py
[[swanki.models.document]]
https://github.com/Mjvolk3/Swanki/tree/main/swanki/models/document.py
Test file: tests/test_models_validation.py

Data models for document structure and content representation.
"""

from pydantic import BaseModel, ConfigDict, Field, field_validator


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
    alt_text : str
        Alt text for the image
    context : str
        Surrounding text context from the source document

    Raises:
    ------
    ValueError
        If summary exceeds 300 words

    Examples:
    --------
    >>> image = ImageSummary(
    ...     page_idx=5,
    ...     image_url="images/figure_1.png",
    ...     summary="Diagram showing neural network architecture with 3 hidden layers",
    ...     extracted_text="Input Layer -> Hidden Layer 1 -> Hidden Layer 2 -> Output"
    ... )
    """

    model_config = ConfigDict(extra="forbid")

    page_idx: int
    image_url: str
    summary: str = Field(..., description="Detailed description (up to 300 words)")
    extracted_text: str | None = Field(None, description="Any text/equations in image")
    alt_text: str = Field("", description="Alt text for the image")
    context: str = Field("", description="Surrounding text context")

    @field_validator("summary")
    def summary_length(cls, v):
        """Validate that image summary is reasonably sized.

        Ensures the summary doesn't exceed 300 words to maintain
        clarity while allowing for detailed technical descriptions.

        Parameters
        ----------
        v : str
            The summary text to validate

        Returns:
        -------
        str
            The validated summary text

        Raises:
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
    for reference. Designed to create lecture-style summaries that help
    students deeply understand the material.

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
    key_equations : List[str], optional
        Important equations with intuitive explanations
    conceptual_framework : str, optional
        How concepts relate to each other
    learning_objectives : List[str], optional
        What students should understand after studying
    summary : str
        Comprehensive lecture-style summary (100-1500 words)

    Attributes:
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
    key_equations : List[str]
        Important equations with explanations
    conceptual_framework : str
        Conceptual relationships
    learning_objectives : List[str]
        Learning goals
    summary : str
        Full summary text

    Raises:
    ------
    ValueError
        If summary is not between 500-1500 words
        If more than 5 key contributions provided

    Examples:
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
    ...     key_equations=[
    ...         "Attention(Q,K,V) = softmax(QK^T/√d_k)V - Computes weighted sum of values based on query-key similarity"
    ...     ],
    ...     conceptual_framework="Transformers replace recurrence with attention mechanisms...",
    ...     learning_objectives=[
    ...         "Understand how self-attention replaces recurrent connections",
    ...         "Explain multi-head attention and its benefits"
    ...     ],
    ...     summary="This comprehensive lecture covers..." # 100-1500 word summary
    ... )
    """

    title: str
    authors: list[str]
    main_topic: str
    key_contributions: list[str] = Field(..., max_length=5)
    methodology: str
    acronyms: dict[str, str] = Field(
        default_factory=dict, description="Acronym definitions"
    )
    technical_terms: dict[str, str] = Field(
        default_factory=dict, description="Technical term definitions"
    )
    key_equations: list[str] = Field(
        default_factory=list, description="Important equations with explanations"
    )
    conceptual_framework: str | None = Field(
        None, description="How concepts relate to each other"
    )
    learning_objectives: list[str] = Field(
        default_factory=list, description="What students should understand"
    )
    summary: str = Field(..., description="100-1500 word summary")

    @field_validator("summary")
    def summary_length(cls, v):
        """Validate document summary length.

        Ensures the summary is appropriate for the document length.
        For shorter documents, allows shorter summaries while maintaining
        quality. For longer documents, encourages comprehensive coverage.

        Parameters
        ----------
        v : str
            The summary text to validate

        Returns:
        -------
        str
            The validated summary text

        Raises:
        ------
        ValueError
            If summary is too short (<100 words) or too long (>1500 words)
        """
        words = len(v.split())
        if words < 100:
            raise ValueError(f"Summary too short: {words} words (minimum 100)")
        if words > 1500:
            raise ValueError(f"Summary too long: {words} words (maximum 1500)")
        return v
