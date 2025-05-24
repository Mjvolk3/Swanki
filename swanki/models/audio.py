from pydantic import BaseModel, Field


class AudioTranscript(BaseModel):
    """Structured audio transcript"""
    citation_key: str
    card_id: str
    content: str
    tts_version: str = Field(..., description="TTS-friendly version with pronunciations")
    
    def get_filename(self) -> str:
        return f"{self.citation_key}_{self.card_id}.txt"