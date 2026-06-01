"""
swanki/processing/landmarks.py
[[swanki.processing.landmarks]]
https://github.com/Mjvolk3/Swanki/tree/main/swanki/processing/landmarks.py
Test file: tests/test_markdown_cleaner.py

Table/figure audio "landmark" sentinels and helpers shared by the markdown
cleaner (which emits landmarks) and the table processor (which fills the
caption-less ones). A landmark is a short spoken cue -- ``Figure: <desc>`` or
``Table: <desc>`` (no number) -- bracketed by ``---SECTION_BREAK---`` so the
audio layer surrounds it with real silence. Table cell data is never voiced.
"""

import re
from collections.abc import Iterator

SECTION_BREAK = "---SECTION_BREAK---"

# NUL-delimited, opaque sentinels: they cannot collide with prose, survive the
# markdown -> TTS scrubber chain untouched, and are trivially regex-matched by
# the fill step. Mirrors `_common._SECTION_BREAK_TTS_MASK`'s opaque-mask idea.
_NUL = "\x00"
_FIGURE_PLACEHOLDER_RE = re.compile(r"\x00FIGLMK:(.*?)\x00", re.DOTALL)
_TABLE_PLACEHOLDER_RE = re.compile(r"\x00TBLLMK:([^:\x00]+):(\d+)\x00")
_ANY_PLACEHOLDER_RE = re.compile(r"\x00(?:FIG|TBL)LMK:.*?\x00", re.DOTALL)

# A `Figure:`/`Table:` line whose only content is an unfilled placeholder.
_ORPHAN_LANDMARK_LINE_RE = re.compile(
    r"(?:Figure|Table):[ \t]*\x00(?:FIG|TBL)LMK:.*?\x00[ \t]*", re.DOTALL
)


def figure_placeholder(url: str) -> str:
    """Sentinel for a caption-less figure, keyed by image URL for fill-by-url."""
    return f"{_NUL}FIGLMK:{url}{_NUL}"


def table_placeholder(page_stem: str, occurrence_idx: int) -> str:
    """Sentinel for a caption-less table, keyed by page stem + occurrence."""
    return f"{_NUL}TBLLMK:{page_stem}:{occurrence_idx}{_NUL}"


def landmark_block(kind: str, body: str) -> str:
    """Build a SECTION_BREAK-bracketed landmark block.

    Args:
        kind: ``"Figure"`` or ``"Table"``.
        body: The verbatim caption, or a placeholder sentinel to be filled.

    Returns:
        The landmark text, padded with blank lines so it splits into its own
        audio section.
    """
    return f"\n\n{SECTION_BREAK}\n{kind}: {body}\n{SECTION_BREAK}\n\n"


def iter_table_placeholders(text: str) -> Iterator[tuple[str, int]]:
    """Yield ``(page_stem, occurrence_idx)`` for each table placeholder."""
    for m in _TABLE_PLACEHOLDER_RE.finditer(text):
        yield m.group(1), int(m.group(2))


def fill_table_placeholder(text: str, page_stem: str, idx: int, summary: str) -> str:
    """Replace one table placeholder with its generated summary sentence."""
    return text.replace(table_placeholder(page_stem, idx), summary)


def fill_figure_placeholders(text: str, summary_by_url: dict[str, str]) -> str:
    r"""Replace caption-less figure placeholders with a one-sentence summary.

    Args:
        text: Markdown containing ``\x00FIGLMK:<url>\x00`` sentinels.
        summary_by_url: Map from image URL to its (already clamped) sentence.

    Returns:
        Text with matched figure placeholders filled; unmatched ones are left
        for :func:`strip_unfilled_placeholders` to remove.
    """

    def _sub(m: re.Match[str]) -> str:
        url = m.group(1)
        return summary_by_url.get(url, m.group(0))

    return _FIGURE_PLACEHOLDER_RE.sub(_sub, text)


def strip_unfilled_placeholders(text: str) -> str:
    """Remove any landmark placeholder that was never filled.

    A fill failure must never let a NUL sentinel reach TTS. Drops the whole
    ``Figure:``/``Table:`` line when its only content is an unfilled
    placeholder, then any stray sentinel.
    """
    text = _ORPHAN_LANDMARK_LINE_RE.sub("", text)
    text = _ANY_PLACEHOLDER_RE.sub("", text)
    return text


def first_sentence(text: str, max_words: int = 40) -> str:
    """Clamp a (possibly multi-sentence) summary to one short sentence.

    Used to turn a multi-sentence image summary into a one-line figure
    landmark. Splits on the first sentence terminator, then hard-caps words.
    """
    text = " ".join(text.split())
    m = re.search(r"[.!?](?:\s|$)", text)
    if m:
        text = text[: m.end()].strip()
    words = text.split()
    if len(words) > max_words:
        text = " ".join(words[:max_words]).rstrip(",;:") + "."
    return text


def clean_caption(raw: str) -> str:
    r"""Clean a LaTeX caption for verbatim reading, preserving inline math.

    Strips non-math LaTeX commands (``\captionsetup``, ``\label``, ...) but
    protects ``$...$`` / ``$$...$$`` spans so a caption like ``plot of $\alpha$
    vs $\beta$`` keeps its math for ``humanize_latex`` to verbalize downstream
    (rather than deleting the backslash-commands and breaking the math).
    """
    spans: list[str] = []

    def _mask(m: re.Match[str]) -> str:
        spans.append(m.group(0))
        return f"{_NUL}MATH{len(spans) - 1}{_NUL}"

    masked = re.sub(r"\$\$.*?\$\$|\$.*?\$", _mask, raw, flags=re.DOTALL)
    # Drop LaTeX commands and their brace/bracket args from the non-math text.
    masked = re.sub(r"\\[a-zA-Z]+(\{[^}]*\}|\[[^\]]*\])*", "", masked)
    masked = masked.replace("{", "").replace("}", "")

    def _unmask(m: re.Match[str]) -> str:
        return spans[int(m.group(1))]

    out = re.sub(r"\x00MATH(\d+)\x00", _unmask, masked)
    return " ".join(out.split()).strip()
