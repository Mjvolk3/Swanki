"""
swanki/processing/reading_reorder.py
[[swanki.processing.reading_reorder]]
https://github.com/Mjvolk3/Swanki/tree/main/swanki/processing/reading_reorder.py
Test file: tests/test_reading_reorder.py

Reading-flow fixups applied to the full reading source BEFORE it is chunked for
TTS (the per-chunk reading LLM cannot move a figure across chunk boundaries, so
document-level reordering has to happen here).

Two deterministic, content-preserving passes:

1. ``reorder_figures_to_referencing_section`` — a scientific PDF's two-column /
   page-top layout makes OCR drop each figure (image + "Fig. N | ..." caption)
   at a page break, so a figure is voiced in the middle of — or one section away
   from — the prose that discusses it (e.g. Fig 6 read inside Discussion instead
   of its own results section). This defers each main figure to the END of the
   section whose prose references "Fig. N" the MOST (subpanel refs like
   "Fig. 2a" count; a lone forward-reference does not hijack the figure). Result:
   read a section's prose to completion, THEN its figures. It is a strict
   PERMUTATION of the source's paragraph blocks — if the output is not an exact
   reordering (no block added, dropped or altered), the input is returned
   unchanged, so it can never corrupt content.

2. ``strip_reference_cruft`` — remove bare URLs and "accessed <date>" citation
   tails that are noise when voiced (e.g. "https://www.uniprot.org/, accessed 8
   November 2023"). Only citation cruft is removed; prose is untouched.
"""

import re

_HEADING = re.compile(r"^#{1,6}\s")
_IMAGE = re.compile(r"^!\[\]\(")
_FIGCAP = re.compile(r"^(?:Fig\.|Figure|Table)\s*(\d+)\b", re.IGNORECASE)
_EXTENDED = re.compile(r"^(?:Extended Data|Supplementary)", re.IGNORECASE)

_ACCESSED = re.compile(r",?\s*accessed\s+\d{1,2}\s+[A-Za-z]+\s+\d{4}", re.IGNORECASE)
_BARE_URL = re.compile(r"\(?\bhttps?://[^\s)]+\)?", re.IGNORECASE)


def _split_blocks(content: str) -> list[str]:
    """Paragraph blocks, split on blank lines (mid-sentence joins stay intact)."""
    return [b for b in re.split(r"\n\s*\n", content) if b.strip()]


def _classify(block: str) -> tuple[str, int | None]:
    """Return ``(kind, figure_number)`` for one block.

    Kinds: ``heading``, ``image``, ``figcap`` (a main Figure/Table caption, with
    its number), or ``prose``. Extended Data / Supplementary captions are left as
    ``prose`` so they are never reordered (their images are often absent).
    """
    s = block.lstrip()
    if _HEADING.match(s):
        return "heading", None
    if _IMAGE.match(s):
        return "image", None
    if _EXTENDED.match(s):
        return "prose", None
    m = _FIGCAP.match(s)
    if m:
        return "figcap", int(m.group(1))
    return "prose", None


def reorder_figures_to_referencing_section(content: str) -> str:
    """Defer each main figure to the end of the section that references it most.

    Permutation-safe: returns ``content`` unchanged if no figure moves or if the
    rebuilt block order is not an exact reordering of the input blocks.
    """
    blocks = _split_blocks(content)
    if not blocks:
        return content
    kinds = [_classify(b) for b in blocks]
    n = len(blocks)

    # Section index per block: a new section begins at each heading.
    sec = [0] * n
    cur = -1
    for i, (k, _) in enumerate(kinds):
        if k == "heading":
            cur += 1
        sec[i] = cur

    # Figure units: a caption plus the adjacent (prev, else next) image block.
    claimed = [False] * n
    units: list[tuple[int, list[int]]] = []
    for i, (k, num) in enumerate(kinds):
        if k != "figcap" or num is None:
            continue
        idxs = [i]
        claimed[i] = True
        if i - 1 >= 0 and kinds[i - 1][0] == "image" and not claimed[i - 1]:
            idxs.insert(0, i - 1)
            claimed[i - 1] = True
        elif i + 1 < n and kinds[i + 1][0] == "image" and not claimed[i + 1]:
            idxs.append(i + 1)
            claimed[i + 1] = True
        units.append((num, idxs))

    if not units:
        return content

    moved: set[int] = set()
    dest: dict[int, tuple[int, int, list[int]]] = {}
    for num, idxs in units:
        ref = re.compile(rf"Fig\.?\s*{num}(?![0-9])", re.IGNORECASE)
        counts: dict[int, int] = {}
        for i, b in enumerate(blocks):
            if kinds[i][0] == "prose":
                hits = len(ref.findall(b))
                if hits:
                    counts[sec[i]] = counts.get(sec[i], 0) + hits
        if not counts:
            continue
        target = max(sorted(counts), key=lambda s: counts[s])
        if target != sec[idxs[0]]:
            dest[idxs[0]] = (target, num, idxs)
            moved.update(idxs)

    if not dest:
        return content

    by_target: dict[int, list[tuple[int, list[int]]]] = {}
    for _, (tgt, num, idxs) in dest.items():
        by_target.setdefault(tgt, []).append((num, idxs))
    for tgt in by_target:
        by_target[tgt].sort()

    out: list[str] = []
    for si in range(cur + 1):
        for i in range(n):
            if sec[i] == si and i not in moved:
                out.append(blocks[i])
        for _, idxs in by_target.get(si, []):
            out.extend(blocks[j] for j in idxs)

    if sorted(out) != sorted(blocks):
        return content  # invariant broken -> fail safe, never corrupt content
    return "\n\n".join(out)


def strip_reference_cruft(content: str) -> str:
    """Drop bare URLs and 'accessed <date>' citation tails (noise when voiced)."""
    content = _ACCESSED.sub("", content)
    content = _BARE_URL.sub("", content)
    # collapse artifacts a removal may leave ("( , )", double spaces, " ,").
    content = re.sub(r"\(\s*[,;]?\s*\)", "", content)
    content = re.sub(r"[ \t]{2,}", " ", content)
    content = re.sub(r"\s+([,.;)])", r"\1", content)
    return content
