from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Dict


class ImageSummary(BaseModel):
    """Structured image summary output"""
    page_idx: int
    image_url: str
    summary: str = Field(..., description="2-3 sentence description")
    extracted_text: Optional[str] = Field(None, description="Any text/equations in image")
    
    @field_validator('summary')
    def summary_length(cls, v):
        """Ensure summary is concise"""
        words = len(v.split())
        if words > 150:  # Increased limit for technical images
            raise ValueError(f"Summary too long: {words} words")
        return v


class DocumentSummary(BaseModel):
    """Structured document summary with key information"""
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
        words = len(v.split())
        if not 200 <= words <= 500:
            raise ValueError(f"Summary should be 200-500 words, got {words}")
        return v