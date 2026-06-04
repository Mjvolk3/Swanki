"""
tests/test_zotero_retry.py
[[tests.test_zotero_retry]]
https://github.com/Mjvolk3/Swanki/tree/main/tests/test_zotero_retry.py

Unit tests for the hardened Zotero client + retry wrapper
(``swanki/sync/zotero_client.py``). No live network; the retry sleep is
stubbed so backoff math never blocks the suite.
"""

import httpx
import pytest

from swanki.sync.zotero_client import (
    RETRYABLE_STATUS,
    harden_zotero_timeouts,
    with_zotero_retry,
)


def _status_error(code: int) -> httpx.HTTPStatusError:
    """Build an httpx.HTTPStatusError carrying a given status code."""
    request = httpx.Request("GET", "https://api.zotero.org/x")
    response = httpx.Response(code, request=request)
    return httpx.HTTPStatusError(f"HTTP {code}", request=request, response=response)


class _Sequence:
    """Callable that raises a queued exception per call, else returns a value."""

    def __init__(self, *raises: Exception | None, value: object = "ok") -> None:
        self._raises = list(raises)
        self._value = value
        self.calls = 0

    def __call__(self) -> object:
        self.calls += 1
        exc = self._raises.pop(0) if self._raises else None
        if exc is not None:
            raise exc
        return self._value


def _no_sleep(_: float) -> None:
    return None


class TestRetryWrapper:
    def test_retries_503_then_succeeds(self) -> None:
        seq = _Sequence(_status_error(503), None, value="ok")
        result = with_zotero_retry(seq, sleep=_no_sleep)
        assert result == "ok"
        assert seq.calls == 2

    def test_retries_timeout_then_succeeds(self) -> None:
        seq = _Sequence(httpx.ReadTimeout("slow"), None, value=42)
        assert with_zotero_retry(seq, sleep=_no_sleep) == 42
        assert seq.calls == 2

    def test_404_raises_immediately_no_retry(self) -> None:
        seq = _Sequence(_status_error(404))
        with pytest.raises(httpx.HTTPStatusError):
            with_zotero_retry(seq, sleep=_no_sleep)
        assert seq.calls == 1  # not retried

    def test_exhausts_after_max_tries(self) -> None:
        seq = _Sequence(
            _status_error(504), _status_error(502), _status_error(503)
        )
        with pytest.raises(httpx.HTTPStatusError):
            with_zotero_retry(seq, max_tries=3, sleep=_no_sleep)
        assert seq.calls == 3

    def test_non_http_error_not_retried(self) -> None:
        seq = _Sequence(ValueError("bug"))
        with pytest.raises(ValueError):
            with_zotero_retry(seq, sleep=_no_sleep)
        assert seq.calls == 1

    def test_404_is_not_in_retryable_set(self) -> None:
        assert 404 not in RETRYABLE_STATUS
        assert {502, 503, 504}.issubset(RETRYABLE_STATUS)


class TestHardenTimeouts:
    def test_sets_module_global(self) -> None:
        from pyzotero import _client as pyz

        harden_zotero_timeouts(123)
        assert pyz.DEFAULT_TIMEOUT == 123
        harden_zotero_timeouts()  # restore default
        assert pyz.DEFAULT_TIMEOUT == 180
