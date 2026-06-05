"""
swanki/delivery/targets/anki.py
[[swanki.delivery.targets.anki]]
https://github.com/Mjvolk3/Swanki/tree/main/swanki/delivery/targets/anki.py
Test file: tests/test_delivery_anki.py

Anki SyncTarget: import this item's apkg(s) into a running headless Anki via
AnkiConnect, then trigger one AnkiWeb sync. This is the canonical AnkiConnect
client for the codebase; ``scripts/swanki_anki_sync.py`` (the walk-all manual
"push to anki" command) is a thin shim over these primitives.

Per-item, not library-wide: the queue delivers one job at a time, so the target
imports only the resolved apkgs for that job. Prereqs (headless Anki +
AnkiConnect on 127.0.0.1:8765, Flatpak ``--filesystem`` allowlist covering the
apkg path) are documented in ``notes/anki.headless-sync.md``.
"""

import logging
import os
from pathlib import Path
from typing import Any

import requests
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

ANKICONNECT_VERSION = 6
HTTP_TIMEOUT_SEC = 300


class AnkiConnectRequest(BaseModel):
    """JSON-RPC body shape AnkiConnect expects on every POST."""

    action: str
    version: int = ANKICONNECT_VERSION
    params: dict[str, Any] = Field(default_factory=dict)


class AnkiConnectResponse(BaseModel):
    """JSON-RPC reply shape. ``error`` is non-null on action failure."""

    result: Any = None
    error: str | None = None


class ImportPackageParams(BaseModel):
    """Params block for AnkiConnect's ``importPackage`` action.

    Only ``path`` is sent: the headless Anki build's ``importPackage`` rejects a
    ``deleteExisting`` kwarg (import merges by note GUID regardless).
    """

    path: str


def ankiconnect_call(
    url: str, action: str, params: dict[str, Any] | None = None
) -> Any:
    """POST a single AnkiConnect action and return the unwrapped ``result``.

    Args:
        url: AnkiConnect HTTP endpoint (e.g. ``http://127.0.0.1:8765``).
        action: AnkiConnect action name (``version``, ``importPackage``, ...).
        params: Action-specific params; an empty dict if omitted.

    Returns:
        The ``result`` field of the parsed response.

    Raises:
        requests.HTTPError: on non-2xx response.
        RuntimeError: when ``error`` is non-null (surfaces the addon's error
            string verbatim).
    """
    body = AnkiConnectRequest(action=action, params=params or {})
    r = requests.post(url, json=body.model_dump(), timeout=HTTP_TIMEOUT_SEC)
    r.raise_for_status()
    parsed = AnkiConnectResponse.model_validate(r.json())
    if parsed.error is not None:
        raise RuntimeError(f"AnkiConnect {action} failed: {parsed.error}")
    return parsed.result


def verify_ankiconnect(url: str) -> int:
    """Ping AnkiConnect's ``version`` action and assert minimum compat.

    The AnkiConnect addon is archived upstream, so a silent skip would let a
    job be marked delivered with nothing imported. This fails loud instead.

    Args:
        url: AnkiConnect endpoint URL.

    Returns:
        The integer version reported by the addon.

    Raises:
        AssertionError: if the reported version is below ``ANKICONNECT_VERSION``.
    """
    version = ankiconnect_call(url, "version")
    assert isinstance(version, int), (
        f"AnkiConnect version action returned non-int: {version!r}"
    )
    assert version >= ANKICONNECT_VERSION, (
        f"AnkiConnect version {version} below minimum {ANKICONNECT_VERSION}"
    )
    return version


def default_ankiconnect_url() -> str:
    """AnkiConnect endpoint from ``ANKI_HOST`` / ``ANKI_PORT`` env (or defaults)."""
    host = os.environ.get("ANKI_HOST", "127.0.0.1")
    port = int(os.environ.get("ANKI_PORT", "8765"))
    return f"http://{host}:{port}"


class AnkiTarget:
    """Import an ArtifactSet's apkg(s) into headless Anki, then sync once."""

    name = "anki"

    def __init__(self, url: str | None = None, *, sync_after: bool = True) -> None:
        """Set the AnkiConnect endpoint and whether to sync after imports."""
        self.url = url or default_ankiconnect_url()
        self.sync_after = sync_after

    def push(self, apkgs: list[Path], *, dry_run: bool = False) -> int:
        """Import each apkg, then trigger one AnkiWeb sync.

        Import + sync is not atomic: if the final sync fails the imports have
        already landed, so the caller MUST NOT record the Anki marker -- a
        re-drain re-imports (idempotent on identical apkg) and re-syncs.

        Args:
            apkgs: Local apkg paths to import (this job only).
            dry_run: When true, log the plan and POST nothing.

        Returns:
            Count of apkgs imported (or planned, in dry-run).
        """
        if not apkgs:
            logger.info("AnkiTarget: no apkgs to import; skipping")
            return 0
        if dry_run:
            for apkg in apkgs:
                print(f"  [dry-run] anki: would importPackage {apkg}")
            return len(apkgs)

        verify_ankiconnect(self.url)
        for apkg in apkgs:
            path = str(Path(apkg).resolve())
            ankiconnect_call(
                self.url, "importPackage", ImportPackageParams(path=path).model_dump()
            )
            print(f"  anki: imported {Path(apkg).name}")
        if self.sync_after:
            ankiconnect_call(self.url, "sync")
            print("  anki: sync ok")
        return len(apkgs)
