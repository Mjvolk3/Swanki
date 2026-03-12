"""
tests/conftest.py
[[tests.conftest]]
https://github.com/Mjvolk3/Swanki/tree/main/tests/conftest.py
Test file: N/A

Shared fixtures and marker gating for the Swanki test suite.
"""

from unittest.mock import MagicMock

import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--llm", action="store_true", default=False, help="Run LLM API tests"
    )
    parser.addoption(
        "--integration",
        action="store_true",
        default=False,
        help="Run integration tests",
    )


def pytest_collection_modifyitems(config, items):
    skip_llm = pytest.mark.skip(reason="Need --llm to run")
    skip_integration = pytest.mark.skip(reason="Need --integration to run")

    for item in items:
        if "llm" in item.keywords and not config.getoption("--llm"):
            item.add_marker(skip_llm)
        if "integration" in item.keywords and not config.getoption("--integration"):
            item.add_marker(skip_integration)


@pytest.fixture()
def tmp_audio_dir(tmp_path):
    d = tmp_path / "audio"
    d.mkdir()
    return d


@pytest.fixture()
def mock_text_agent_result():
    """Mock pydantic-ai agent result with .output attribute."""
    mock_result = MagicMock()
    mock_result.output = "Mocked transcript text"
    return mock_result


@pytest.fixture()
def mock_elevenlabs_api_key():
    return "test-key"
