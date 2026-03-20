"""Tests for swanki.llm.agents — model string building and agent registry."""

from swanki.llm.agents import get_model_string


def test_get_model_string_openai() -> None:
    """Default provider builds openai:model string."""
    config = {"provider": "openai", "model": "gpt-5.2-2025-12-11"}
    assert get_model_string(config) == "openai:gpt-5.2-2025-12-11"


def test_get_model_string_anthropic() -> None:
    """Anthropic provider builds anthropic:model string."""
    config = {"provider": "anthropic", "model": "claude-sonnet-4-20250514"}
    assert get_model_string(config) == "anthropic:claude-sonnet-4-20250514"


def test_get_model_string_defaults() -> None:
    """Missing keys fall back to openai:gpt-4."""
    assert get_model_string({}) == "openai:gpt-4"


def test_get_model_string_missing_model() -> None:
    """Missing model key falls back to gpt-4."""
    config = {"provider": "openai"}
    assert get_model_string(config) == "openai:gpt-4"


def test_get_model_string_missing_provider() -> None:
    """Missing provider key falls back to openai."""
    config = {"model": "gpt-4o"}
    assert get_model_string(config) == "openai:gpt-4o"


def test_agent_registry_exports() -> None:
    """All 6 agents and get_model_string are importable from swanki.llm."""
    from swanki.llm import (
        audio_feedback_agent,
        card_feedback_agent,
        card_gen_agent,
        document_summary_agent,
        get_model_string,
        lecture_critic_agent,
        text_agent,
    )

    assert document_summary_agent is not None
    assert card_gen_agent is not None
    assert card_feedback_agent is not None
    assert audio_feedback_agent is not None
    assert lecture_critic_agent is not None
    assert text_agent is not None
    assert callable(get_model_string)
