"""
scripts/zotero_annotations.py
[[scripts.zotero_annotations]]
https://github.com/Mjvolk3/Swanki/tree/main/scripts/zotero_annotations.py

Extract Zotero PDF annotations filtered by highlight color.
"""

import argparse
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel
from pyzotero import zotero

# Reuse connection helpers from zotero_paper_import
sys.path.insert(0, str(Path(__file__).resolve().parent))
from zotero_paper_import import (
    ZoteroConfig,
    connect,
    find_item_by_citation_key,
    get_pdf_attachments,
)

load_dotenv()

ZOTERO_API_KEY = os.environ["ZOTERO_API_KEY"]
ZOTERO_LIBRARY_ID = os.environ["ZOTERO_LIBRARY_ID"]

# Named color map (Zotero hex values)
COLOR_MAP = {
    "magenta": "#e56eee",
    "red": "#ff6666",
    "orange": "#f19837",
    "yellow": "#ffd400",
    "green": "#5fb236",
    "cyan": "#2ea8e5",
    "blue": "#aaaaff",
    "purple": "#a28ae5",
}


class ZoteroAnnotation(BaseModel):
    """A single PDF annotation from Zotero."""

    text: str
    comment: str
    page: str
    color: str


def get_annotations(
    zot: zotero.Zotero,
    item_key: str,
    color_filter: str | None = None,
) -> list[ZoteroAnnotation]:
    """Get annotations from PDF attachments of a Zotero item.

    Args:
        zot: Zotero API client.
        item_key: Parent item key.
        color_filter: Hex color to filter by (e.g. "#e56eee").

    Returns:
        List of matching annotations.
    """
    attachments = get_pdf_attachments(zot, item_key)
    annotations: list[ZoteroAnnotation] = []

    for att in attachments:
        children = zot.children(att["key"])
        for child in children:
            data = child.get("data", {})
            if data.get("itemType") != "annotation":
                continue
            if data.get("annotationType") != "highlight":
                continue

            ann_color = data.get("annotationColor", "")
            if color_filter and ann_color.lower() != color_filter.lower():
                continue

            text = data.get("annotationText", "").strip()
            comment = data.get("annotationComment", "").strip()
            page = data.get("annotationPageLabel", "")

            if text:
                annotations.append(
                    ZoteroAnnotation(
                        text=text,
                        comment=comment,
                        page=page,
                        color=ann_color,
                    )
                )

    return annotations


def format_annotations_markdown(annotations: list[ZoteroAnnotation]) -> str:
    """Format annotations as a markdown list.

    Args:
        annotations: List of annotations to format.

    Returns:
        Markdown-formatted string.
    """
    if not annotations:
        return "No annotations found.\n"

    lines: list[str] = []
    for ann in annotations:
        parts = [f"- **p.{ann.page}**: {ann.text}"]
        if ann.comment:
            parts.append(f"  - *Comment:* {ann.comment}")
        lines.extend(parts)

    return "\n".join(lines) + "\n"


def main():
    """CLI: extract Zotero annotations by citation key and color."""
    parser = argparse.ArgumentParser(
        description="Extract Zotero PDF annotations filtered by highlight color"
    )
    parser.add_argument("citation_key", help="Citation key to look up")
    parser.add_argument(
        "--color",
        default="magenta",
        help=f"Color name ({', '.join(COLOR_MAP)}) or hex value (default: magenta)",
    )
    args = parser.parse_args()

    # Resolve color name to hex
    color_hex = COLOR_MAP.get(args.color.lower(), args.color)

    config = ZoteroConfig(library_id=ZOTERO_LIBRARY_ID, api_key=ZOTERO_API_KEY)
    zot = connect(config)

    item = find_item_by_citation_key(zot, args.citation_key)
    annotations = get_annotations(zot, item["key"], color_filter=color_hex)

    print(f"## Annotations for {args.citation_key} ({args.color})\n")
    print(format_annotations_markdown(annotations))
    print(f"Total: {len(annotations)} annotation(s)")


if __name__ == "__main__":
    main()
