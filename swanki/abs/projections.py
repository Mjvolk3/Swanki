"""
swanki/abs/projections.py
[[swanki.abs.projections]]
https://github.com/Mjvolk3/Swanki/tree/main/swanki/abs/projections.py
Test file: tests/test_abs_projections.py

Single home for projection routing. ``projections.yml`` is hand-tuned infra
data living OUTSIDE the repo (`~/Documents/projects/infra/abs/projections.yml`,
never Hydra-ized); every entry point takes a ``projections_path`` with that
expanduser default. Configs stay raw dicts -- the shape callers (including
``scripts/swanki_anki_sync.py`` and its tests) already consume.

The citation-key fallback chain and ``resolve_library``, previously
copy-pasted across three scripts, live here once. The chain
(``data.citationKey`` -> ``"Citation Key:"`` regex on ``extra`` -> Zotero item
key) is load-bearing: items without an explicit citationKey field would
otherwise silently vanish from sync/enrich routing.
"""

import os
import re
from pathlib import Path
from typing import Any, cast

import yaml  # type: ignore[import-untyped]

DEFAULT_PROJECTIONS = (
    Path.home() / "Documents/projects/infra/abs/projections.yml"
)

BOOK_TYPES = {"book", "bookSection"}
CHAPTER_SUFFIX = re.compile(r"_CH\d+_.*$")


def load_projections(path: Path | None = None) -> dict[str, dict[str, Any]]:
    """Load the ``projections:`` mapping from the external YAML.

    Args:
        path: Projections file; defaults to the infra location.

    Returns:
        Raw per-projection config dicts keyed by projection name.
    """
    p = Path(path) if path is not None else DEFAULT_PROJECTIONS
    with p.expanduser().open() as f:
        return cast(dict[str, dict[str, Any]], yaml.safe_load(f)["projections"])


def resolve_library(cfg: dict[str, Any]) -> tuple[str, str]:
    """Resolve a projection's Zotero library id + type from its config.

    Args:
        cfg: The projection's ``zotero`` sub-dict (``library_id`` literal or
            ``library_id_env`` env-var indirection).

    Returns:
        ``(library_id, library_type)``; type defaults to ``user``.
    """
    if "library_id" in cfg:
        lib_id = str(cfg["library_id"])
    else:
        lib_id = os.environ[cfg["library_id_env"]]
    return lib_id, cfg.get("library_type", "user")


def citation_key(item: dict[str, Any]) -> str:
    """Extract the citation key from a Zotero item via the fallback chain."""
    key = item["data"].get("citationKey", "") or ""
    if key:
        return key
    extra = item["data"].get("extra", "")
    m = re.search(r"Citation Key:\s*(\S+)", extra)
    return m.group(1) if m else item["key"]


def classify(item: dict[str, Any]) -> str:
    """``Book`` for book/bookSection Zotero items, else ``Paper``."""
    return "Book" if item["data"].get("itemType") in BOOK_TYPES else "Paper"


def group_key(citekey: str, kind: str) -> str:
    """Group key for the ABS folder: books strip the ``_CH##_...`` suffix.

    All chapters of one book land in one ABS item (ordered tracks); papers
    keep their full key.
    """
    if kind == "Book":
        return CHAPTER_SUFFIX.sub("", citekey)
    return citekey


def kind_for_key(citekey: str) -> str:
    """Infer Paper/Book from the key shape alone (no Zotero round-trip).

    A ``_CH##_`` chapter suffix marks a book chapter. Used by the targeted
    refresh, which works from local artifacts without a Zotero query; the
    full refresh classifies from the Zotero item type instead.
    """
    return "Book" if CHAPTER_SUFFIX.search(citekey) else "Paper"
