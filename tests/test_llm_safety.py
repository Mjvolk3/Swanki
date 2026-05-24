"""
tests/test_llm_safety.py
[[tests.test_llm_safety]]
https://github.com/Mjvolk3/Swanki/tree/main/tests/test_llm_safety.py

Tests for swanki.llm.safety -- biosec-refusal-aware retry wrapper.
"""

from unittest.mock import MagicMock

import pytest

from swanki.llm.safety import (
    EDU_CONTEXT_PREAMBLE,
    SAFETY_REFUSAL_MARKERS,
    with_safety_retry,
)


def _safety_refusal_exception(marker: str) -> Exception:
    """Build an exception whose str(exc) contains a biosec-refusal marker."""
    return RuntimeError(
        f"status_code: 400, body: {{'code': 'invalid_prompt', 'message': "
        f"\"...{marker}...\"}}"
    )


def test_first_attempt_succeeds_no_preamble_added():
    """Happy path: the original user message is sent verbatim and returned."""
    agent = MagicMock()
    expected = MagicMock()
    agent.run_sync.return_value = expected

    result = with_safety_retry(
        agent,
        "Original message.",
        instructions="sys",
        model="openai:test",
        label="happy-path test",
    )

    assert result is expected
    agent.run_sync.assert_called_once()
    sent_msg = agent.run_sync.call_args[0][0]
    assert sent_msg == "Original message."
    assert EDU_CONTEXT_PREAMBLE not in sent_msg


def test_safety_refusal_retries_with_preamble():
    """A safety-refusal on attempt 1 triggers a retry with the preamble prepended."""
    agent = MagicMock()
    expected = MagicMock()
    agent.run_sync.side_effect = [
        _safety_refusal_exception("invalid_prompt"),
        expected,
    ]

    result = with_safety_retry(
        agent,
        "Original message.",
        instructions="sys",
        model="openai:test",
        label="retry test",
    )

    assert result is expected
    assert agent.run_sync.call_count == 2
    first_msg = agent.run_sync.call_args_list[0][0][0]
    second_msg = agent.run_sync.call_args_list[1][0][0]
    assert first_msg == "Original message."
    assert second_msg.startswith(EDU_CONTEXT_PREAMBLE)
    assert second_msg.endswith("Original message.")


def test_safety_refusal_marker_limited_access_also_triggers_retry():
    """Both SAFETY_REFUSAL_MARKERS values should trip the retry path."""
    agent = MagicMock()
    expected = MagicMock()
    agent.run_sync.side_effect = [
        _safety_refusal_exception("limited access to this content for safety"),
        expected,
    ]

    result = with_safety_retry(
        agent,
        "Original message.",
        instructions="sys",
        model="openai:test",
    )

    assert result is expected
    assert agent.run_sync.call_count == 2


def test_safety_refusal_exhausts_retries_then_raises():
    """All attempts safety-refuse -> the last exception is re-raised."""
    agent = MagicMock()
    last_exc = _safety_refusal_exception("invalid_prompt")
    agent.run_sync.side_effect = [
        _safety_refusal_exception("invalid_prompt"),
        _safety_refusal_exception("invalid_prompt"),
        last_exc,
    ]

    with pytest.raises(RuntimeError) as excinfo:
        with_safety_retry(
            agent,
            "Original message.",
            instructions="sys",
            model="openai:test",
            max_safety_retries=2,
        )

    assert "invalid_prompt" in str(excinfo.value)
    # Total attempts = max_safety_retries + 1 = 3
    assert agent.run_sync.call_count == 3


def test_non_safety_exception_reraises_immediately_no_retry():
    """A non-safety exception (HTTP 500, timeout, ...) re-raises on the first hit."""
    agent = MagicMock()
    agent.run_sync.side_effect = RuntimeError("HTTP 500 server error")

    with pytest.raises(RuntimeError) as excinfo:
        with_safety_retry(
            agent,
            "Original message.",
            instructions="sys",
            model="openai:test",
        )

    assert "HTTP 500" in str(excinfo.value)
    # No retries -- non-safety errors are immediate.
    agent.run_sync.assert_called_once()


def test_model_settings_forwarded_when_provided():
    """``model_settings`` is forwarded as a kwarg when supplied."""
    agent = MagicMock()
    agent.run_sync.return_value = MagicMock()

    with_safety_retry(
        agent,
        "msg",
        instructions="sys",
        model="openai:test",
        model_settings={"max_tokens": 8000},
    )

    kwargs = agent.run_sync.call_args.kwargs
    assert kwargs["model_settings"] == {"max_tokens": 8000}


def test_model_settings_omitted_when_none():
    """No ``model_settings`` kwarg is sent when caller passes None (default)."""
    agent = MagicMock()
    agent.run_sync.return_value = MagicMock()

    with_safety_retry(
        agent,
        "msg",
        instructions="sys",
        model="openai:test",
    )

    kwargs = agent.run_sync.call_args.kwargs
    assert "model_settings" not in kwargs


def test_constants_exposed():
    """The constants are part of the public API for callers that need to detect
    safety refusals downstream (e.g., lecture.py's empty-string fallback)."""
    assert "invalid_prompt" in SAFETY_REFUSAL_MARKERS
    assert "limited access to this content for safety" in SAFETY_REFUSAL_MARKERS
    assert "EDUCATIONAL CONTEXT" in EDU_CONTEXT_PREAMBLE
    assert "already-published" in EDU_CONTEXT_PREAMBLE
    assert "no novel" in EDU_CONTEXT_PREAMBLE.lower()
