from pydantic import BaseModel, Field
from pathlib import Path
from typing import Dict, Optional
from .document import DocumentSummary


class ProcessingState(BaseModel):
    """Track pipeline processing state"""
    pdf_path: Path
    citation_key: Optional[str] = None
    current_stage: str
    document_summary: Optional[DocumentSummary] = None
    cards_generated: int = 0
    audio_files_generated: int = 0
    outputs: Dict[str, Path] = Field(default_factory=dict)