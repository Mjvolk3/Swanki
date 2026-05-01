"""
swanki/models/__init__.py
[[swanki.models.__init__]]
https://github.com/Mjvolk3/Swanki/tree/main/swanki/models/__init__.py
Test file: tests/test_models_validation.py

Pydantic data models for documents, cards, audio, and pipeline state.
"""

from .audio import AudioTranscript
from .cards import (
    AudioTranscriptFeedback,
    CardContent,
    CardFeedback,
    CardGenerationResponse,
    CardIssue,
    EnhancedCardGenerationResponse,
    ImageCard,
    ImageCardContent,
    PlainCard,
    RefinementHistory,
)
from .document import DocumentSummary, ImageSummary
from .pipeline import ProcessingState
from .problem_set import (
    CardPlan,
    CardPlanResponse,
    CardSubtype,
    PairingResult,
    ProblemCardBatchResponse,
    ProblemEnumerationResponse,
    ProblemLocation,
    ProblemPairing,
    ProblemPairingResponse,
    ProblemPart,
    ProblemProvenance,
    ProblemSubtype,
    ProblemTag,
    ProblemUnit,
    ProvenanceLog,
    ProvenanceSpan,
)
from .sections import (
    ClassificationResult,
    ContentSection,
    PageLabel,
    SectionKind,
    sections_from_page_labels,
)

__all__ = [
    "PlainCard",
    "CardContent",
    "CardGenerationResponse",
    "ImageCard",
    "ImageCardContent",
    "CardFeedback",
    "AudioTranscriptFeedback",
    "RefinementHistory",
    "EnhancedCardGenerationResponse",
    "CardIssue",
    "DocumentSummary",
    "ImageSummary",
    "AudioTranscript",
    "ProcessingState",
    # Problem-set models
    "CardPlan",
    "CardPlanResponse",
    "CardSubtype",
    "PairingResult",
    "ProblemCardBatchResponse",
    "ProblemEnumerationResponse",
    "ProblemLocation",
    "ProblemPairing",
    "ProblemPairingResponse",
    "ProblemPart",
    "ProblemProvenance",
    "ProblemSubtype",
    "ProblemTag",
    "ProblemUnit",
    "ProvenanceLog",
    "ProvenanceSpan",
    # Section classifier
    "ClassificationResult",
    "ContentSection",
    "PageLabel",
    "SectionKind",
    "sections_from_page_labels",
]
