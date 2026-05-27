"""
scripts/swanki_anki_sync.py
[[scripts.swanki_anki_sync]]
https://github.com/Mjvolk3/Swanki/tree/main/scripts/swanki_anki_sync.py
Test file: tests/test_swanki_anki_sync.py

Push the latest ``.apkg`` per Zotero item into a running headless Anki via
AnkiConnect, then trigger one AnkiWeb sync at the end.

Mirror of ``scripts/swanki_abs_sync.py`` for the Anki side of the
"sync to swanki servers" shortcut. Reads the same projections config
(``infra/abs/projections.yml`` by default) and for each projection where
``push_anki`` is truthy walks fox-tagged Zotero items, resolves the newest
``.apkg`` per chapter via ``latest_apkgs``, downloads each to an absolute
path under ``SWANKI_ANKI_STAGE`` (default ``/scratch/Swanki_Anki_Stage``),
and POSTs ``importPackage`` to AnkiConnect. After all imports across all
projections complete, POSTs a single ``sync``.

Prerequisites (out of scope for this script; see ``notes/anki.headless-sync.md``):

- A headless Anki instance running on this host with the AnkiConnect addon.
- AnkiConnect reachable at ``http://127.0.0.1:8765`` (env ``ANKI_HOST`` /
  ``ANKI_PORT`` override).
- For Flatpak Anki: the staging directory must be included in the
  ``--filesystem`` allowlist (e.g. ``flatpak --user override
  --filesystem=/scratch:ro net.ankiweb.Anki``).
- Minimum AnkiConnect API version: 6.
"""

import argparse
import os
import sys
from pathlib import Path
from typing import Any

# Lift pyzotero's default read timeout BEFORE anything imports a Zotero
# client. The 30s default times out on apkg downloads for chapter-heavy
# books (see scripts/publish_regen_to_abs.sh).
from pyzotero import _client as _pyz  # noqa: I001

_pyz.DEFAULT_TIMEOUT = 180  # type: ignore[attr-defined]

import requests  # noqa: E402
from _swanki_zotero_artifacts import latest_apkgs  # noqa: E402
from dotenv import load_dotenv  # noqa: E402
from pydantic import BaseModel, Field  # noqa: E402
from pyzotero import zotero  # noqa: E402
from swanki_abs_sync import (  # noqa: E402
    DEFAULT_PROJECTIONS,
    citation_key,
    fetch_items,
    load_projections,
    resolve_library,
)

load_dotenv()

DEFAULT_STAGE_ROOT = Path("/scratch/Swanki_Anki_Stage")
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
    """Params block for AnkiConnect's ``importPackage`` action."""

    path: str
    deleteExisting: bool = False  # noqa: N815 -- wire field name


def ankiconnect_call(
    url: str, action: str, params: dict[str, Any] | None = None
) -> Any:
    """POST a single AnkiConnect action and return the unwrapped ``result``.

    Args:
        url: AnkiConnect HTTP endpoint (e.g. ``http://127.0.0.1:8765``).
        action: AnkiConnect action name (``version``, ``importPackage``, ...).
        params: Action-specific params; an empty dict if omitted.

    Returns:
        The ``result`` field of the parsed response. ``None`` when the
        action returns ``None`` on success (e.g. ``sync``).

    Raises:
        requests.HTTPError: on non-2xx response.
        ValueError: when the response body does not parse into
            ``AnkiConnectResponse``.
        RuntimeError: when ``error`` is non-null. Surfaces the addon's
            error string verbatim so the operator can see what failed.
    """
    body = AnkiConnectRequest(action=action, params=params or {})
    r = requests.post(url, json=body.model_dump(), timeout=HTTP_TIMEOUT_SEC)
    r.raise_for_status()
    parsed = AnkiConnectResponse.model_validate(r.json())
    if parsed.error is not None:
        raise RuntimeError(f"AnkiConnect {action} failed: {parsed.error}")
    return parsed.result


def verify_ankiconnect(url: str) -> int:
    """Ping AnkiConnect's ``version`` action; assert minimum compat.

    Args:
        url: AnkiConnect endpoint URL.

    Returns:
        The integer version reported by the addon.

    Raises:
        AssertionError: if the reported version is below
            ``ANKICONNECT_VERSION`` (the minimum we support).
    """
    version = ankiconnect_call(url, "version")
    assert isinstance(version, int), (
        f"AnkiConnect version action returned non-int: {version!r}"
    )
    assert version >= ANKICONNECT_VERSION, (
        f"AnkiConnect version {version} below minimum {ANKICONNECT_VERSION}"
    )
    return version


def push_projection(
    name: str,
    cfg: dict[str, Any],
    api_key: str,
    url: str,
    stage_root: Path,
    dry_run: bool,
) -> int:
    """Resolve and import the latest apkg per fox-tagged item in one projection.

    Args:
        name: Projection name (used for log prefixes and the staging subdir).
        cfg: Raw projection config dict (same shape ``swanki_abs_sync`` reads).
        api_key: Zotero API key.
        url: AnkiConnect endpoint URL.
        stage_root: Absolute staging-dir root. Subdir ``<projection>/`` is
            created under this.
        dry_run: When true, print the resolved plan and skip downloads +
            ``importPackage`` POSTs.

    Returns:
        Count of attachments successfully imported (or planned, in dry-run).
    """
    if not cfg.get("push_anki", True):
        print(
            f"\n=== Projection: {name} -- push_anki=false, skipping anki ==="
        )
        return 0

    lib_id, lib_type = resolve_library(cfg["zotero"])
    tag = cfg["zotero"].get("tag")
    stage_dir = (stage_root / name).resolve()
    stage_dir.mkdir(parents=True, exist_ok=True)

    print(
        f"\n=== Projection: {name} "
        f"(Zotero {lib_type}/{lib_id}, tag={tag!r}) ==="
    )
    zot = zotero.Zotero(lib_id, lib_type, api_key)
    items = fetch_items(zot, tag)
    print(f"  {len(items)} item(s) matched")

    imported = 0
    for item in items:
        ckey = citation_key(item)
        if not ckey:
            continue
        for att in latest_apkgs(zot, item["key"]):
            filename = att["data"]["filename"]
            target = stage_dir / filename
            if dry_run:
                print(f"  [dry-run] + {ckey}: would import {target}")
                imported += 1
                continue
            try:
                content = zot.file(att["key"])
            except Exception as e:
                # Stale attachment metadata pointing to a missing file; skip
                # instead of aborting the projection. Mirrors
                # swanki_abs_sync.py:208-217.
                print(
                    f"  ! {ckey}: skipping {filename} "
                    f"(key={att['key']}): {e}"
                )
                continue
            target.write_bytes(content)
            ankiconnect_call(
                url,
                "importPackage",
                ImportPackageParams(path=str(target)).model_dump(),
            )
            print(f"  + {ckey}: imported {filename}")
            imported += 1
    print(f"  imported {imported} apkg(s)")
    return imported


def main() -> None:
    """CLI entry. Push enabled projections, then trigger one AnkiWeb sync."""
    parser = argparse.ArgumentParser(
        description=(
            "Push latest .apkg per Zotero item to AnkiConnect, "
            "then sync once at the end."
        )
    )
    parser.add_argument(
        "projections_path",
        nargs="?",
        type=Path,
        default=DEFAULT_PROJECTIONS,
        help="Path to projections YAML (default: %(default)s)",
    )
    parser.add_argument(
        "--projection",
        metavar="NAME",
        help="Limit to a single projection; default = all push_anki-enabled.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the resolved plan without downloading or POSTing.",
    )
    args = parser.parse_args()

    host = os.environ.get("ANKI_HOST", "127.0.0.1")
    port = int(os.environ.get("ANKI_PORT", "8765"))
    url = f"http://{host}:{port}"
    stage_root = Path(
        os.environ.get("SWANKI_ANKI_STAGE", str(DEFAULT_STAGE_ROOT))
    )
    api_key = os.environ["ZOTERO_API_KEY"]
    projections = load_projections(args.projections_path)

    if args.projection:
        if args.projection not in projections:
            sys.exit(
                f"projection {args.projection!r} not found in "
                f"{args.projections_path}"
            )
        projections = {args.projection: projections[args.projection]}

    # Fail-fast ping. Surfaces ConnectionRefusedError if the headless Anki
    # service isn't running, before we touch Zotero.
    version = verify_ankiconnect(url)
    print(f"AnkiConnect {url} -- version {version}")

    total = 0
    for name, cfg in projections.items():
        total += push_projection(
            name, cfg, api_key, url, stage_root, args.dry_run
        )

    if total == 0:
        print("\nNothing to import; skipping final sync.")
        return

    if args.dry_run:
        print("\n[dry-run] would POST sync to AnkiConnect")
        return

    print("\nTriggering AnkiWeb sync ...")
    ankiconnect_call(url, "sync")
    print("sync ok")


if __name__ == "__main__":
    main()
