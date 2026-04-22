"""
scripts/abs_setup_libraries.py
[[scripts.abs_setup_libraries]]
https://github.com/Mjvolk3/Swanki/tree/main/scripts/abs_setup_libraries.py

Declarative library setup for audiobookshelf.

Reads ``infra/abs/projections.yml`` and idempotently creates the six audiobook
libraries per projection that ``swanki_abs_sync.py`` populates:

    /audiobooks/<projection>/Swanki-<Kind>-<Audiotype>/

Auth uses an ABS API token read from a file (preferred, chmod 600) via the
``ABS_API_TOKEN_FILE`` env var, or passed directly via ``ABS_API_TOKEN``.
Token value is never logged. Libraries already present (by name) are left
untouched.

Usage:
    export ABS_API_TOKEN_FILE=~/Documents/projects/infra/abs/.api-token
    python scripts/abs_setup_libraries.py
"""

import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

import yaml

DEFAULT_ABS_URL = "https://abs.michaelvolk.dev"
DEFAULT_PROJECTIONS = (
    Path.home() / "Documents/projects/infra/abs/projections.yml"
)
KINDS = ("Paper", "Book")


def load_token() -> str:
    token_file = os.environ.get("ABS_API_TOKEN_FILE")
    if token_file:
        return Path(token_file).expanduser().read_text().strip()
    token = os.environ.get("ABS_API_TOKEN")
    if token:
        return token.strip()
    raise SystemExit(
        "Set ABS_API_TOKEN_FILE (path to token file) or ABS_API_TOKEN."
    )


def api(base: str, token: str, method: str, path: str, body: dict | None = None) -> dict:
    url = f"{base.rstrip('/')}{path}"
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(
        url,
        data=data,
        method=method,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "swanki-abs-setup/1.0",
        },
    )
    with urllib.request.urlopen(req) as resp:
        raw = resp.read().decode()
    return json.loads(raw) if raw else {}


def existing_libraries(base: str, token: str) -> list[dict]:
    data = api(base, token, "GET", "/api/libraries")
    return data.get("libraries", data) if isinstance(data, dict) else data


def create_library(
    base: str, token: str, name: str, folder: str
) -> None:
    payload = {
        "name": name,
        "mediaType": "book",
        "folders": [{"fullPath": folder}],
    }
    api(base, token, "POST", "/api/libraries", payload)
    print(f"  + {name}  →  {folder}")


def main() -> None:
    base = os.environ.get("ABS_URL", DEFAULT_ABS_URL)
    projections_path = Path(
        sys.argv[1] if len(sys.argv) > 1 else DEFAULT_PROJECTIONS
    )
    with projections_path.open() as f:
        projections = yaml.safe_load(f)["projections"]

    token = load_token()
    libs = existing_libraries(base, token)
    by_folder = {
        folder["fullPath"]: lib
        for lib in libs for folder in lib.get("folders", [])
    }
    existing_names = {lib["name"] for lib in libs}
    print(f"Found {len(libs)} existing libraries on {base}")

    added = 0
    for proj_name, cfg in projections.items():
        kinds = cfg.get("kinds") or list(KINDS)
        for kind in kinds:
            for audiotype in cfg["audiotypes"]:
                folder = (
                    f"/audiobooks/{proj_name}/"
                    f"Swanki-{kind}-{audiotype.capitalize()}"
                )
                if folder in by_folder:
                    print(f"  = {by_folder[folder]['name']}  (at {folder})")
                    continue

                simple = f"{kind} — {audiotype.capitalize()}"
                name = simple if simple not in existing_names \
                    else f"{proj_name}: {simple}"
                create_library(base, token, name, folder)
                existing_names.add(name)
                added += 1
    print(f"\nAdded {added} librar{'y' if added == 1 else 'ies'}")


if __name__ == "__main__":
    main()
