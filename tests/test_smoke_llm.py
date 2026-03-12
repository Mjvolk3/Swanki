"""Smoke tests that hit real LLM APIs — skipped by default, run with --llm.

These validate the full stack: config → model string → pydantic-ai → API
→ Pydantic output validation. Each test makes 1-2 API calls.
"""

from dotenv import load_dotenv

load_dotenv()

import pytest  # noqa: E402

from swanki.llm.agents import (  # noqa: E402
    card_gen_agent,
    document_summary_agent,
    get_model_string,
    text_agent,
)


@pytest.mark.llm
def test_document_summary_agent_openai() -> None:
    """Verify document_summary_agent produces valid DocumentSummary via OpenAI."""
    model = get_model_string({"provider": "openai", "model": "gpt-4o-mini"})
    prompt = (
        "Summarize this short paper:\n\n"
        "# Test Paper\nAuthors: A. Test\n\n"
        "## Introduction\nThis paper presents a method for testing software. "
        "We propose automated unit testing with coverage analysis.\n\n"
        "## Methods\nWe use pytest with mocked dependencies.\n\n"
        "## Results\nAll tests passed with 95% coverage.\n\n"
        "## Conclusion\nAutomated testing improves software reliability."
    )
    result = document_summary_agent.run_sync(prompt, model=model)
    summary = result.output

    assert summary.title
    assert len(summary.authors) >= 1
    assert summary.main_topic
    assert len(summary.key_contributions) >= 1
    assert len(summary.key_contributions) <= 5
    assert 100 <= len(summary.summary.split()) <= 1500


@pytest.mark.llm
def test_text_agent_openai() -> None:
    """Verify text_agent returns a string via OpenAI."""
    model = get_model_string({"provider": "openai", "model": "gpt-4o-mini"})
    result = text_agent.run_sync("Say 'hello' and nothing else.", model=model)
    assert isinstance(result.output, str)
    assert len(result.output) > 0


@pytest.mark.llm
def test_card_gen_agent_openai() -> None:
    """Verify card_gen_agent produces valid cards via OpenAI."""
    model = get_model_string({"provider": "openai", "model": "gpt-4o-mini"})
    prompt = (
        "Generate exactly 1 basic flashcard from this content:\n\n"
        "Machine learning is a subset of artificial intelligence that "
        "enables systems to learn and improve from experience without "
        "being explicitly programmed.\n\n"
        "Requirements:\n"
        "- Generate exactly 1 card\n"
        "- Include at least one tag\n"
        "- Front should be a question, back should be the answer"
    )
    result = card_gen_agent.run_sync(prompt, model=model)
    response = result.output

    assert len(response.cards) >= 1
    assert response.cards[0].front.text
    assert response.cards[0].back.text
    assert len(response.cards[0].tags) >= 1
