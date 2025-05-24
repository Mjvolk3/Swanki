from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Literal


class CardContent(BaseModel):
    """Structured content for a card side"""
    text: str = Field(..., min_length=1, max_length=500)
    requires_latex: bool = Field(default=False)
    audio_hint: Optional[str] = Field(None, description="Pronunciation guide for TTS")
    image_path: Optional[str] = Field(None, description="Path to image file for this card side")


class PlainCard(BaseModel):
    """Structured flashcard output"""
    front: CardContent
    back: CardContent
    tags: List[str] = Field(default_factory=list)
    difficulty: Literal["easy", "medium", "hard"] = "medium"
    
    def add_citation_prefix(self, citation_key: str):
        """Add citation key to front of card"""
        if citation_key and not self.front.text.startswith(citation_key):
            self.front.text = f"{citation_key}: {self.front.text}"
    
    def to_md(self, include_audio: bool = False, audio_front_uri: Optional[str] = None, audio_back_uri: Optional[str] = None, citation_key: Optional[str] = None, tag_format: str = "slugified") -> str:
        """Convert to markdown in VSCode Anki format
        
        Args:
            include_audio: Whether to include audio links
            audio_front_uri: URI for front audio file
            audio_back_uri: URI for back audio file
            citation_key: Citation key to prepend
            tag_format: How to format tags ("slugified", "spaces", "raw")
        """
        # Import here to avoid circular imports
        from ..utils.formatting import format_tags
        
        # Add citation key prefix if provided and not already present
        front_text = self.front.text
        if citation_key and not front_text.startswith(f"@{citation_key}:"):
            front_text = f"@{citation_key}: {front_text}"
        
        # Format tags
        formatted_tags = format_tags(self.tags, tag_format)
        
        # Format based on whether audio is included
        if include_audio and audio_front_uri and audio_back_uri:
            # VSCode Anki format with audio
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
    """Structured response for card generation"""
    cards: List[PlainCard]
    skipped_sections: List[str] = Field(default_factory=list, description="Sections not suitable for cards")
    
    @field_validator('cards')
    def validate_card_count(cls, v):
        if len(v) == 0:
            raise ValueError("Must generate at least one card")
        return v