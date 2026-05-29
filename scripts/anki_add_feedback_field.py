"""
scripts/anki_add_feedback_field.py
[[scripts.anki_add_feedback_field]]
https://github.com/Mjvolk3/Swanki/tree/main/scripts/anki_add_feedback_field.py

One-shot migration to add a ``Feedback`` field to existing Swanki Basic and
Cloze note types in a running Anki collection.

Why this exists
---------------
New .apkg exports include a ``Feedback`` field (ord 2) on the Basic and Cloze
note types, used as a free-text triage channel filled in during review.
Existing collections that were populated before the field was added carry the
same model id but only two fields. Re-importing a newer .apkg on top of those
older notes is brittle. Run this script once on the workstation with Anki to
align the live note types with the new schema; afterwards future imports drop
in cleanly and existing notes simply have an empty ``Feedback`` field.

Requirements
------------
- Anki running with the AnkiConnect add-on (default host 127.0.0.1:8765).
- gilahyper has no Anki client, so run this on the laptop. Idempotent.

Usage
-----
::

    python scripts/anki_add_feedback_field.py
    python scripts/anki_add_feedback_field.py --host 127.0.0.1 --port 8765
    python scripts/anki_add_feedback_field.py --models Basic Cloze
"""

from __future__ import annotations

import argparse
import json
import sys
from urllib import request
from urllib.error import URLError

FIELD_NAME = "Feedback"
FIELD_INDEX = 2  # after Front/Back or Text/Back Extra
DEFAULT_MODELS = ("Basic", "Cloze")


def _call(url: str, action: str, params: dict | None = None) -> dict:
    """POST to AnkiConnect and return the parsed JSON envelope."""
    payload = json.dumps(
        {"action": action, "version": 6, "params": params or {}}
    ).encode("utf-8")
    req = request.Request(url, data=payload, headers={"Content-Type": "application/json"})
    with request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read().decode("utf-8"))


def add_feedback_field(url: str, model_name: str) -> str:
    """Add the Feedback field to ``model_name`` if missing.

    Returns a status string: ``"added"``, ``"already_present"``, or
    ``"missing_model"``.
    """
    names_env = _call(url, "modelNames")
    if names_env.get("error"):
        raise RuntimeError(f"modelNames failed: {names_env['error']}")
    if model_name not in names_env.get("result", []):
        return "missing_model"

    fields_env = _call(url, "modelFieldNames", {"modelName": model_name})
    if fields_env.get("error"):
        raise RuntimeError(f"modelFieldNames failed: {fields_env['error']}")
    if FIELD_NAME in fields_env.get("result", []):
        return "already_present"

    add_env = _call(
        url,
        "modelFieldAdd",
        {"modelName": model_name, "fieldName": FIELD_NAME, "index": FIELD_INDEX},
    )
    if add_env.get("error"):
        raise RuntimeError(
            f"modelFieldAdd({model_name!r}) failed: {add_env['error']}"
        )
    return "added"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument(
        "--models",
        nargs="+",
        default=list(DEFAULT_MODELS),
        help="Note types to patch (default: Basic Cloze)",
    )
    args = parser.parse_args()
    url = f"http://{args.host}:{args.port}"

    try:
        _call(url, "version")
    except URLError as e:
        print(f"Cannot reach AnkiConnect at {url}: {e}", file=sys.stderr)
        print("Open Anki and ensure the AnkiConnect add-on is installed.", file=sys.stderr)
        return 2

    exit_code = 0
    for model in args.models:
        status = add_feedback_field(url, model)
        print(f"  {model:<10s} -> {status}")
        if status == "missing_model":
            print(
                f"    (skipped: note type {model!r} not in this collection)",
                file=sys.stderr,
            )
            exit_code = 1
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
