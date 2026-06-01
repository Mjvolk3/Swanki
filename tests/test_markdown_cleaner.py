"""
tests/test_markdown_cleaner.py
[[tests.test_markdown_cleaner]]
https://github.com/Mjvolk3/Swanki/tree/main/tests/test_markdown_cleaner.py
Test file: tests/test_markdown_cleaner.py

Tests for table/figure landmark emission in the markdown cleaner and the
landmark sentinel helpers.
"""

from pathlib import Path

from swanki.audio._common import (
    add_tts_pauses,
    clean_markdown_for_tts,
    split_transcript_by_sections,
)
from swanki.processing.landmarks import (
    clean_caption,
    fill_figure_placeholders,
    first_sentence,
    iter_table_placeholders,
    strip_unfilled_placeholders,
)
from swanki.processing.markdown_cleaner import MarkdownCleaner

FIG_WITH_CAPTION = (
    r"\begin{figure}\includegraphics{img/fig1.png}"
    r"\caption{Growth curve of the doubling effect over $t$ years.}\end{figure}"
)
FIG_NO_CAPTION = r"\begin{figure}\includegraphics{img/fig2.png}\end{figure}"
TABLE_WITH_CAPTION = (
    r"\begin{table}\caption{Doubling factors by parent age.}"
    r"\begin{tabular}{|l|l|}\hline 2 & 17 \\\hline\end{tabular}\end{table}"
)
BARE_TABULAR = (
    r"\begin{tabular}{|l|l|}\hline factor & years \\\hline 2 & 17 \\"
    r"\hline 3 & 27 \\\hline\end{tabular}"
)


def _clean(content: str, stem: str = "page-1", base: Path | None = None) -> str:
    return MarkdownCleaner(base or Path("/tmp"))._apply_cleaning(
        content, page_stem=stem
    )


def test_figure_with_caption_becomes_landmark_verbatim():
    out = _clean(FIG_WITH_CAPTION)
    assert "Figure: Growth curve of the doubling effect over $t$ years." in out
    # empty alt so clean_markdown_for_tts does not double-read the caption
    assert "![](img/fig1.png)" in out
    assert "---SECTION_BREAK---" in out


def test_figure_full_caption_not_truncated():
    long_cap = "word " * 60
    fig = (
        r"\begin{figure}\includegraphics{img/f.png}\caption{"
        + long_cap.strip()
        + r"}\end{figure}"
    )
    out = _clean(fig)
    # all 60 words survive (old code truncated to 100 chars)
    assert out.count("word") == 60


def test_figure_without_caption_emits_placeholder():
    out = _clean(FIG_NO_CAPTION)
    assert "Figure:" in out
    assert "FIGLMK:img/fig2.png" in out.replace("\x00", "")


def test_bare_tabular_becomes_table_landmark_no_cells(tmp_path):
    out = MarkdownCleaner(tmp_path)._apply_cleaning(BARE_TABULAR, page_stem="page-4")
    assert "Table:" in out
    assert "tabular" not in out
    # no cell data voiced
    assert "2 17" not in out.replace(" \\\\", "")
    assert "factor" not in out
    # placeholder keyed to page + idx 0, and source stashed for the summarizer
    stem_idx = list(iter_table_placeholders(out))
    assert stem_idx == [("page-4", 0)]
    assert (tmp_path / "table-summaries" / "page-4_0.source.txt").exists()


def test_wrapped_table_with_caption_read_verbatim_no_double_count(tmp_path):
    out = MarkdownCleaner(tmp_path)._apply_cleaning(
        TABLE_WITH_CAPTION, page_stem="page-2"
    )
    assert "Table: Doubling factors by parent age." in out
    # the inner tabular must NOT also yield a second (placeholder) landmark
    assert list(iter_table_placeholders(out)) == []
    assert out.count("Table:") == 1
    assert "2 17" not in out.replace(" \\\\", "")


def test_two_bare_tabulars_numbered_in_order(tmp_path):
    content = "Intro.\n\n" + BARE_TABULAR + "\n\nMiddle.\n\n" + BARE_TABULAR + "\n\nEnd."
    out = MarkdownCleaner(tmp_path)._apply_cleaning(content, page_stem="page-8")
    assert list(iter_table_placeholders(out)) == [("page-8", 0), ("page-8", 1)]


def test_hamming_page4_real_fixture(tmp_path):
    src = Path(
        "/scratch/projects/torchcell-scratch/Swanki_Data/"
        "hammingArtDoingScience2020/hammingArtDoingScience2020_01_orientation_12/"
        "clean-md-singles/page-4.md"
    )
    if not src.exists():
        return  # data not present on this machine; covered by synthetic tests
    out = MarkdownCleaner(tmp_path)._apply_cleaning(src.read_text(), page_stem="page-4")
    assert "Table:" in out
    assert "2 17" not in out  # numeric grid not voiced
    assert "tabular" not in out


def test_landmark_splits_into_own_audio_section():
    out = _clean(TABLE_WITH_CAPTION, stem="page-1")
    # follow the reading scrubber chain
    secs = split_transcript_by_sections(
        add_tts_pauses(clean_markdown_for_tts(out), "fish_speech")
    )
    assert any(s.startswith("Table: Doubling factors") for s in secs)


# --- landmark helper units ------------------------------------------------


def test_clean_caption_preserves_math():
    assert clean_caption(r"plot of $\alpha$ vs $\beta$ \label{f}") == (
        r"plot of $\alpha$ vs $\beta$"
    )


def test_first_sentence_clamps():
    assert first_sentence("One sentence. Two sentence.") == "One sentence."


def test_fill_and_strip_figure_placeholder():
    from swanki.processing.landmarks import figure_placeholder, landmark_block

    block = landmark_block("Figure", figure_placeholder("u.png"))
    filled = fill_figure_placeholders(block, {"u.png": "A bar chart."})
    assert "Figure: A bar chart." in filled
    assert "FIGLMK" not in filled.replace("\x00", "")


def test_strip_unfilled_placeholder_removes_orphan_line():
    from swanki.processing.landmarks import landmark_block, table_placeholder

    block = "Before." + landmark_block("Table", table_placeholder("p", 0)) + "After."
    stripped = strip_unfilled_placeholders(block)
    assert "TBLLMK" not in stripped.replace("\x00", "")
    assert "Table: \x00" not in stripped
    assert "Before." in stripped and "After." in stripped
