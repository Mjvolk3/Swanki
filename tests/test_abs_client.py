"""
tests/test_abs_client.py
[[tests.test_abs_client]]
https://github.com/Mjvolk3/Swanki/tree/main/tests/test_abs_client.py
Test file: tests/test_abs_client.py

Tests for swanki/abs/client.py -- the three-way token chain, the retry
classifier (timeouts/5xx retried, 404 terminal), and the response-shape
helpers. Fully mocked; no network.
"""

import httpx
import pytest

from swanki.abs import client as client_mod
from swanki.abs.client import ABSClient, load_token, with_abs_retry


def _no_sleep(_: float) -> None:
    return None


def _status_error(code: int) -> httpx.HTTPStatusError:
    req = httpx.Request("GET", "https://abs.test/api/x")
    return httpx.HTTPStatusError(
        f"{code}", request=req, response=httpx.Response(code, request=req)
    )


# -- token chain -------------------------------------------------------------


def test_token_file_env_wins_and_expands(tmp_path, monkeypatch):
    f = tmp_path / ".api-token"
    f.write_text("  sekrit \n")
    monkeypatch.setenv("ABS_API_TOKEN_FILE", str(f))
    monkeypatch.setenv("ABS_API_TOKEN", "should-not-win")
    assert load_token() == "sekrit"


def test_token_env_fallback(monkeypatch):
    monkeypatch.delenv("ABS_API_TOKEN_FILE", raising=False)
    monkeypatch.setenv("ABS_API_TOKEN", " raw-token ")
    assert load_token() == "raw-token"


def test_token_default_file_fallback(tmp_path, monkeypatch):
    monkeypatch.delenv("ABS_API_TOKEN_FILE", raising=False)
    monkeypatch.delenv("ABS_API_TOKEN", raising=False)
    f = tmp_path / ".api-token"
    f.write_text("default-tok")
    monkeypatch.setattr(client_mod, "DEFAULT_TOKEN_FILE", f)
    assert load_token() == "default-tok"


# -- retry classifier ----------------------------------------------------------


def test_retry_recovers_from_timeout():
    calls = {"n": 0}

    def flaky():
        calls["n"] += 1
        if calls["n"] < 3:
            raise httpx.ReadTimeout("slow")
        return "ok"

    assert with_abs_retry(flaky, sleep=_no_sleep) == "ok"
    assert calls["n"] == 3


def test_retry_recovers_from_503():
    calls = {"n": 0}

    def flaky():
        calls["n"] += 1
        if calls["n"] == 1:
            raise _status_error(503)
        return "ok"

    assert with_abs_retry(flaky, sleep=_no_sleep) == "ok"
    assert calls["n"] == 2


def test_404_is_terminal_no_retry():
    calls = {"n": 0}

    def fail():
        calls["n"] += 1
        raise _status_error(404)

    with pytest.raises(httpx.HTTPStatusError):
        with_abs_retry(fail, sleep=_no_sleep)
    assert calls["n"] == 1


def test_retry_exhausts_and_raises():
    def fail():
        raise _status_error(502)

    with pytest.raises(httpx.HTTPStatusError):
        with_abs_retry(fail, max_tries=2, sleep=_no_sleep)


# -- client surface ------------------------------------------------------------


def _client(handler) -> ABSClient:
    return ABSClient(
        base_url="https://abs.test",
        token="tok",
        transport=httpx.MockTransport(handler),
    )


def test_libraries_unwraps_envelope():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.headers["Authorization"] == "Bearer tok"
        return httpx.Response(
            200, json={"libraries": [{"id": "lib1"}, {"id": "lib2"}]}
        )

    assert [x["id"] for x in _client(handler).libraries()] == ["lib1", "lib2"]


def test_request_empty_body_returns_empty_dict():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200)

    c = _client(handler)
    c.scan_library("lib1")  # no JSON body; must not raise


def test_request_plain_text_body_returns_empty_dict():
    # The live /scan endpoint returns a non-JSON body on success; the legacy
    # curl discarded it. Must not attempt to JSON-parse it.
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200, text="OK", headers={"content-type": "text/plain"}
        )

    c = _client(handler)
    c.scan_library("lib1")


def test_request_404_raises():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(404, json={"error": "no"})

    with pytest.raises(httpx.HTTPStatusError):
        _client(handler).item("missing")
