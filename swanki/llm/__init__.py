"""
swanki/llm/__init__.py
[[swanki.llm]]
https://github.com/Mjvolk3/Swanki/tree/main/swanki/llm/__init__.py

Agent registry and LLM utilities for pydantic-ai based inference.
"""

from .agents import (
    audio_feedback_agent,
    card_feedback_agent,
    card_gen_agent,
    document_summary_agent,
    get_model_string,
    lecture_critic_agent,
    text_agent,
)

__all__ = [
    "audio_feedback_agent",
    "card_feedback_agent",
    "card_gen_agent",
    "document_summary_agent",
    "get_model_string",
    "lecture_critic_agent",
    "text_agent",
]
