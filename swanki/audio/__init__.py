"""
swanki/audio/__init__.py
[[swanki.audio]]
https://github.com/Mjvolk3/Swanki/tree/main/swanki/audio/__init__.py

Audio generation package for Swanki TTS pipeline.
"""

from ._common import (
    ChunkTimeline,
    chunk_time_window,
    chunk_time_window_abs,
    restitch_from_chunks,
    time_to_chunk,
)
from .card import generate_card_audio
from .lecture import generate_lecture_audio
from .reading import generate_reading_audio
from .summary import generate_summary_audio
from .surgical import regenerate_and_restitch

__all__ = [
    "ChunkTimeline",
    "chunk_time_window",
    "chunk_time_window_abs",
    "generate_card_audio",
    "generate_lecture_audio",
    "generate_reading_audio",
    "generate_summary_audio",
    "regenerate_and_restitch",
    "restitch_from_chunks",
    "time_to_chunk",
]
