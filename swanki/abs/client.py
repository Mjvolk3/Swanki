"""
swanki/abs/client.py
[[swanki.abs.client]]
https://github.com/Mjvolk3/Swanki/tree/main/swanki/abs/client.py
Test file: tests/test_abs_client.py

Single hardened Audiobookshelf HTTP client. Every ABS API call in swanki goes
through ``ABSClient`` -- one httpx session, one token chain, one retry policy
-- replacing the four transport stacks (requests/httpx/urllib/inline curl) the
legacy ``scripts/abs_*.py`` files grew. The retry classifier mirrors
``swanki/sync/zotero_client.py``: timeouts/transport errors and 5xx are
retried with bounded exponential backoff; 404 (and any other 4xx) is terminal
and raises immediately.

The ABS API is metadata-only for swanki: audio lands on disk and ABS scans
folders (Zotero is the source of truth; nothing uploads audio over this
client).
"""

import logging
import os
import random
import time
from collections.abc import Callable
from pathlib import Path
from typing import Any, cast

import httpx

logger = logging.getLogger(__name__)

DEFAULT_ABS_URL = "https://abs.michaelvolk.dev"
DEFAULT_TOKEN_FILE = Path.home() / "Documents/projects/infra/abs/.api-token"
USER_AGENT = "swanki-abs/1.0"

# Transient HTTP statuses worth retrying. 404 is deliberately excluded: a
# missing item/bookmark is terminal, and retrying masks the real condition.
RETRYABLE_STATUS = frozenset({500, 502, 503, 504})
MAX_TRIES = 3
BASE_DELAY = 2.0


def load_token() -> str:
    """Resolve the ABS API token via the unified chain.

    ``ABS_API_TOKEN_FILE`` (path, ``~`` expanded) -> ``ABS_API_TOKEN`` (raw
    token) -> the default token file. A missing file raises (fail fast).
    """
    token_file = os.environ.get("ABS_API_TOKEN_FILE")
    if token_file:
        return Path(token_file).expanduser().read_text().strip()
    token = os.environ.get("ABS_API_TOKEN")
    if token:
        return token.strip()
    return DEFAULT_TOKEN_FILE.expanduser().read_text().strip()


def _is_retryable(exc: Exception) -> bool:
    """Whether an exception from an ABS call is worth retrying."""
    if isinstance(exc, (httpx.TimeoutException, httpx.TransportError)):
        return True
    if isinstance(exc, httpx.HTTPStatusError):
        return exc.response.status_code in RETRYABLE_STATUS
    return False


def with_abs_retry[T](
    call: Callable[[], T],
    *,
    max_tries: int = MAX_TRIES,
    base_delay: float = BASE_DELAY,
    sleep: Callable[[float], None] = time.sleep,
) -> T:
    """Run an ABS call with bounded exponential-backoff retry.

    Args:
        call: Zero-arg callable performing the HTTP operation.
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
                "ABS call failed (%s); retry %d/%d in %.1fs",
                exc.__class__.__name__,
                attempt + 1,
                max_tries - 1,
                delay,
            )
            sleep(delay)
    raise AssertionError("with_abs_retry exhausted without raising")


def bookmark_time_key(time_s: float) -> int | float:
    """Coerce a bookmark time to the form ABS keys the DELETE endpoint on.

    ABS stores integral times as ints; ``DELETE .../bookmark/2105.0`` 404s
    where ``.../bookmark/2105`` succeeds. Non-integral floats pass through.
    """
    return int(time_s) if time_s == int(time_s) else time_s


class ABSClient:
    """Typed access to the small ABS API surface swanki actually uses."""

    def __init__(
        self,
        *,
        base_url: str | None = None,
        token: str | None = None,
        transport: httpx.BaseTransport | None = None,
        timeout: httpx.Timeout | None = None,
    ) -> None:
        """Build the client; env defaults for URL and token unless given.

        Args:
            base_url: ABS server URL; defaults to ``ABS_URL`` env then the
                production default.
            token: Bearer token; defaults to ``load_token()``.
            transport: Optional httpx transport (MockTransport in tests).
            timeout: Optional timeout override; defaults to 180s read / 60s
                connect, matching the hardened Zotero client.
        """
        self.base_url = (
            base_url or os.environ.get("ABS_URL", DEFAULT_ABS_URL)
        ).rstrip("/")
        kwargs: dict[str, Any] = {}
        if transport is not None:
            kwargs["transport"] = transport
        self._http = httpx.Client(
            base_url=self.base_url,
            headers={
                "Authorization": f"Bearer {token if token is not None else load_token()}",
                "User-Agent": USER_AGENT,
            },
            timeout=timeout or httpx.Timeout(180, connect=60),
            **kwargs,
        )

    def request(
        self,
        method: str,
        path: str,
        *,
        json: Any = None,
        params: dict[str, Any] | None = None,
    ) -> Any:
        """One retried API call; returns parsed JSON ({} on empty body)."""

        def _call() -> Any:
            r = self._http.request(method, path, json=json, params=params)
            r.raise_for_status()
            # Some ABS endpoints (e.g. POST /api/libraries/{id}/scan) return
            # an empty or plain-text body on success; only parse JSON bodies.
            if not r.content or "application/json" not in r.headers.get(
                "content-type", ""
            ):
                return {}
            return r.json()

        return with_abs_retry(_call)

    # -- libraries ---------------------------------------------------------

    def libraries(self) -> list[dict[str, Any]]:
        """All ABS libraries."""
        data = self.request("GET", "/api/libraries")
        return cast(
            list[dict[str, Any]],
            data.get("libraries", data) if isinstance(data, dict) else data,
        )

    def create_library(self, name: str, folder: str) -> dict[str, Any]:
        """Create one audiobook library rooted at ``folder``."""
        return cast(dict[str, Any], self.request(
            "POST",
            "/api/libraries",
            json={
                "name": name,
                "mediaType": "book",
                "folders": [{"fullPath": folder}],
            },
        ))

    def library_items(
        self, library_id: str, *, limit: int = 10000
    ) -> list[dict[str, Any]]:
        """All items in one library."""
        data = self.request(
            "GET", f"/api/libraries/{library_id}/items", params={"limit": limit}
        )
        return cast(
            list[dict[str, Any]],
            data.get("results", data) if isinstance(data, dict) else data,
        )

    def scan_library(self, library_id: str) -> None:
        """Trigger a folder scan; ABS indexes new/changed audio files."""
        self.request("POST", f"/api/libraries/{library_id}/scan")

    # -- items -------------------------------------------------------------

    def item(self, item_id: str, *, expanded: bool = True) -> dict[str, Any]:
        """One library item, expanded by default (includes media.audioFiles)."""
        params = {"expanded": 1} if expanded else None
        return cast(
            dict[str, Any],
            self.request("GET", f"/api/items/{item_id}", params=params),
        )

    def update_authors(self, item_id: str, author_names: list[str]) -> None:
        """PATCH the item's author metadata."""
        self.request(
            "PATCH",
            f"/api/items/{item_id}/media",
            json={"metadata": {"authors": [{"name": n} for n in author_names]}},
        )

    def post_chapters(
        self, item_id: str, chapters: list[dict[str, Any]]
    ) -> None:
        """POST a chapters array so DB + in-memory state both update."""
        self.request(
            "POST", f"/api/items/{item_id}/chapters", json={"chapters": chapters}
        )

    # -- collections -------------------------------------------------------

    def collections(self) -> list[dict[str, Any]]:
        """All ABS collections."""
        data = self.request("GET", "/api/collections")
        return cast(
            list[dict[str, Any]],
            data.get("collections", data) if isinstance(data, dict) else data,
        )

    def collection_books(self, collection_id: str) -> list[str]:
        """Book (item) ids currently in one collection."""
        data = self.request("GET", f"/api/collections/{collection_id}")
        return [b["id"] for b in data.get("books", [])]

    def create_collection(
        self, library_id: str, name: str, book_ids: list[str]
    ) -> dict[str, Any]:
        """Create a collection seeded with ``book_ids``."""
        return cast(
            dict[str, Any],
            self.request(
                "POST",
                "/api/collections",
                json={"libraryId": library_id, "name": name, "books": book_ids},
            ),
        )

    def add_collection_book(self, collection_id: str, book_id: str) -> None:
        """Add one book to a collection."""
        self.request(
            "POST", f"/api/collections/{collection_id}/book", json={"id": book_id}
        )

    def remove_collection_book(self, collection_id: str, book_id: str) -> None:
        """Remove one book from a collection."""
        self.request(
            "DELETE", f"/api/collections/{collection_id}/book/{book_id}"
        )

    # -- user (bookmarks) ----------------------------------------------------

    def me(self) -> dict[str, Any]:
        """The current user payload (holds ``bookmarks``)."""
        return cast(dict[str, Any], self.request("GET", "/api/me"))

    def delete_bookmark(self, library_item_id: str, time_s: float) -> None:
        """Delete one bookmark, keyed by item id + coerced time."""
        tv = bookmark_time_key(time_s)
        self.request(
            "DELETE", f"/api/me/item/{library_item_id}/bookmark/{tv}"
        )

    def create_bookmark(
        self, library_item_id: str, time_s: float, title: str
    ) -> dict[str, Any]:
        """Create one bookmark at an item-global time."""
        return cast(
            dict[str, Any],
            self.request(
                "POST",
                f"/api/me/item/{library_item_id}/bookmark",
                json={"time": bookmark_time_key(time_s), "title": title},
            ),
        )
