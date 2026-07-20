"""
tests/test_reading_reorder.py
[[tests.test_reading_reorder]]

Tests for swanki.processing.reading_reorder: figure deferral to the
most-referencing section (permutation-safe) and reference-cruft stripping.
"""

from swanki.processing.reading_reorder import (
    reorder_figures_to_referencing_section,
    strip_reference_cruft,
)


def _blocks(text):
    import re

    return sorted(b for b in re.split(r"\n\s*\n", text) if b.strip())


def test_orphaned_figure_moves_to_most_referencing_section():
    # Fig 2 sits inside "Discussion" but is referenced only in "Results".
    src = (
        "# Results\n\n"
        "We built the model and validated it (Fig. 2a). "
        "Performance improved markedly (Fig. 2b).\n\n"
        "# Discussion\n\n"
        "Fig. 2 | Model overview. a, schematic. b, benchmark.\n\n"
        "Here we reflect on the broader implications."
    )
    out = reorder_figures_to_referencing_section(src)
    lines = [ln.strip() for ln in out.splitlines() if ln.strip()]
    res_i = lines.index("# Results")
    dis_i = lines.index("# Discussion")
    fig_i = next(i for i, ln in enumerate(lines) if ln.startswith("Fig. 2 |"))
    # figure now read within the Results section (before Discussion), at its end
    assert res_i < fig_i < dis_i


def test_is_permutation_no_content_lost():
    src = (
        "# A\n\nAlpha references Fig. 1 twice: Fig. 1a and Fig. 1b.\n\n"
        "# B\n\nBeta prose.\n\n"
        "Fig. 1 | caption text."
    )
    out = reorder_figures_to_referencing_section(src)
    assert _blocks(out) == _blocks(src)  # exact same set of paragraph blocks


def test_no_figures_is_noop():
    src = "# A\n\nJust prose.\n\n# B\n\nMore prose."
    assert reorder_figures_to_referencing_section(src) == src


def test_forward_reference_does_not_hijack():
    # A lone forward mention in section A must not outweigh 3 refs in section B.
    src = (
        "# A\n\nWe will later show results (Fig. 3).\n\n"
        "# B\n\nHere Fig. 3a, Fig. 3b and Fig. 3c are analysed in depth.\n\n"
        "Fig. 3 | detailed panels."
    )
    out = reorder_figures_to_referencing_section(src)
    lines = [ln.strip() for ln in out.splitlines() if ln.strip()]
    b_i = lines.index("# B")
    fig_i = next(i for i, ln in enumerate(lines) if ln.startswith("Fig. 3 |"))
    assert fig_i > b_i  # placed in B (most references), not A


def test_strip_accessed_date_and_urls():
    src = "the YMDB database (https://ymdb.ca/, accessed 16 March 2022) was used."
    out = strip_reference_cruft(src)
    assert "accessed" not in out.lower()
    assert "http" not in out
    assert "YMDB database" in out and "was used." in out


def test_strip_ocr_space_broken_url():
    # OCR often splits the scheme from the host: "https:// www.rdkit.org/".
    src = "predicted with RDKit, https:// www.rdkit.org/. All reactions inherited"
    out = strip_reference_cruft(src)
    assert "http" not in out and "rdkit.org" not in out
    assert "predicted with RDKit" in out and "All reactions inherited" in out
