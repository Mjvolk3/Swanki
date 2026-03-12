"""
swanki/models/pipeline.py
[[swanki.models.pipeline]]
https://github.com/Mjvolk3/Swanki/tree/main/swanki/models/pipeline.py

Data models for pipeline state management.
"""

from pathlib import Path

from pydantic import BaseModel, Field

from .document import DocumentSummary


class ProcessingState(BaseModel):
    """Track pipeline processing state and outputs.

    Maintains the current state of document processing through the pipeline,
    including the current stage, generated outputs, and processing metrics.
    Used for progress tracking and resuming interrupted processing.

    Parameters
    ----------
    pdf_path : Path
        Path to the source PDF being processed
    citation_key : str, optional
        Citation key for the document
    current_stage : str
        Current processing stage (e.g., 'pdf_conversion', 'card_generation')
    document_summary : DocumentSummary, optional
        Generated document summary
    cards_generated : int, optional
        Number of flashcards generated (default is 0)
    audio_files_generated : int, optional
        Number of audio files created (default is 0)
    outputs : Dict[str, Path], optional
        Dictionary mapping output types to file paths

    Attributes:
    ----------
    pdf_path : Path
        Source PDF path
    citation_key : str or None
        Document citation key
    current_stage : str
        Current processing stage
    document_summary : DocumentSummary or None
        Document summary if generated
    cards_generated : int
        Count of generated cards
    audio_files_generated : int
        Count of generated audio files
    outputs : Dict[str, Path]
        Output file paths by type

    Examples:
    --------
    >>> from pathlib import Path
    >>>
    >>> # Initialize processing state
    >>> state = ProcessingState(
    ...     pdf_path=Path("/docs/paper.pdf"),
    ...     current_stage="initialization"
    ... )
    >>>
    >>> # Update as processing progresses
    >>> state.current_stage = "pdf_conversion"
    >>> state.outputs["markdown"] = Path("/output/paper.md")
    >>>
    >>> # Track generation metrics
    >>> state.cards_generated = 25
    >>> state.audio_files_generated = 50
    >>>
    >>> # Add document summary
    >>> from swanki.models.document import DocumentSummary
    >>> state.document_summary = DocumentSummary(
    ...     title="Example Paper",
    ...     authors=["Author, A."],
    ...     main_topic="Machine Learning",
    ...     key_contributions=["New algorithm"],
    ...     methodology="Experimental",
    ...     summary="This paper presents..." * 50  # 200+ words
    ... )
    """

    pdf_path: Path
    citation_key: str | None = None
    current_stage: str
    document_summary: DocumentSummary | None = None
    cards_generated: int = 0
    audio_files_generated: int = 0
    outputs: dict[str, Path] = Field(default_factory=dict)
