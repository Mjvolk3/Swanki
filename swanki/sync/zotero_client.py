"""
swanki/sync/zotero_client.py
[[swanki.sync.zotero_client]]
https://github.com/Mjvolk3/Swanki/tree/main/swanki/sync/zotero_client.py
Test file: tests/test_zotero_retry.py

Hardened pyzotero client construction and a call-site retry wrapper.

The Zotero API is intermittently flaky (502/503/504, slow reads). pyzotero
1.11.0 is entirely httpx-based and ships no retry on read operations, and it
passes an explicit per-call ``timeout=DEFAULT_TIMEOUT`` (30s) on every GET
(``pyzotero/_client.py``) that OVERRIDES any client-level timeout -- so handing
``zotero.Zotero(..., client=httpx.Client(timeout=...))`` does NOT lift the read
timeout. The only effective lever is the ``_client.DEFAULT_TIMEOUT`` module
global, which is read at call time. ``harden_zotero_timeouts`` raises it;
``with_zotero_retry`` adds bounded exponential-backoff retry on transient
failures (404 is terminal and is never retried).
"""

import logging
import random
import time
from collections.abc import Callable

import httpx
from pyzotero import _client as _pyz_client
from pyzotero import zotero

logger = logging.getLogger(__name__)

# Read timeout (seconds) for Zotero GETs. apkg/zip downloads over slow links
# blow past pyzotero's 30s default; 180s matches the value the legacy
# scripts/swanki_anki_sync.py poked in by hand.
ZOTERO_READ_TIMEOUT = 180

# Transient HTTP statuses worth retrying. 404 is deliberately excluded: a
# missing item/attachment is terminal, and retrying only burns the budget and
# masks the real "artifact absent" condition.
RETRYABLE_STATUS = frozenset({500, 502, 503, 504})

MAX_TRIES = 3
BASE_DELAY = 2.0


def harden_zotero_timeouts(seconds: int = ZOTERO_READ_TIMEOUT) -> None:
    """Lift pyzotero's per-call read timeout module-global.

    pyzotero reads ``_client.DEFAULT_TIMEOUT`` at call time and passes it as
    the explicit ``timeout=`` on every GET, overriding the client default.
    Rebinding the module global is therefore the effective way to extend the
    read timeout. Idempotent; safe to call before any Zotero read.

    Args:
        seconds: New per-call read timeout in seconds.
    """
    _pyz_client.DEFAULT_TIMEOUT = seconds  # type: ignore[attr-defined]


def make_zotero_client(
    library_id: str, library_type: str, api_key: str
) -> zotero.Zotero:
    """Build a pyzotero client with the hardened read timeout applied.

    Args:
        library_id: Zotero library id.
        library_type: ``user`` or ``group``.
        api_key: Zotero API key.

    Returns:
        A configured ``pyzotero.zotero.Zotero`` instance.
    """
    harden_zotero_timeouts()
    return zotero.Zotero(library_id, library_type, api_key)


def _is_retryable(exc: Exception) -> bool:
    """Whether an exception from a Zotero call is worth retrying.

    Retries httpx timeouts/transport errors and 5xx responses in
    ``RETRYABLE_STATUS``. A 404 (or any other 4xx) is terminal.
    """
    if isinstance(exc, (httpx.TimeoutException, httpx.TransportError)):
        return True
    if isinstance(exc, httpx.HTTPStatusError):
        return exc.response.status_code in RETRYABLE_STATUS
    return False


def with_zotero_retry[T](
    call: Callable[[], T],
    *,
    max_tries: int = MAX_TRIES,
    base_delay: float = BASE_DELAY,
    sleep: Callable[[float], None] = time.sleep,
) -> T:
    """Run a Zotero call with bounded exponential-backoff retry.

    Wrap a single read operation (``lambda: zot.items(...)``,
    ``lambda: zot.children(k)``, ``lambda: zot.file(k)``). Retries transient
    failures (httpx timeout/transport, 5xx) up to ``max_tries`` with
    exponential backoff plus jitter. A 404 / other 4xx raises immediately.

    Args:
        call: Zero-arg callable performing the Zotero operation.
        max_tries: Total attempts before giving up.
        base_delay: Base seconds for backoff; attempt ``n`` waits
            ``base_delay * 2**n`` plus up to ``base_delay`` of jitter.
        sleep: Sleep function (injectable for tests).

    Returns:
        The call's return value.

    Raises:
        Exception: the last transient error after ``max_tries``, or any
            non-retryable error (e.g. httpx 404) immediately.
    """
    for attempt in range(max_tries):
        try:
            return call()
        except Exception as exc:
            if not _is_retryable(exc) or attempt == max_tries - 1:
                raise
            delay = base_delay * (2**attempt) + random.uniform(0, base_delay)
            logger.warning(
                "Zotero call failed (%s); retry %d/%d in %.1fs",
                exc.__class__.__name__,
                attempt + 1,
                max_tries - 1,
                delay,
            )
            sleep(delay)
    # Unreachable: the loop either returns or raises.
    raise AssertionError("with_zotero_retry exhausted without raising")
