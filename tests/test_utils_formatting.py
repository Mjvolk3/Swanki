"""
tests/test_utils_formatting.py
[[tests.test_utils_formatting]]
https://github.com/Mjvolk3/Swanki/tree/main/tests/test_utils_formatting.py

Tests for citation-key humanization helpers in swanki.utils.formatting.
Theme 8 fix surface (chapter-slug humanization for lecture bookends).
"""

from swanki.utils.formatting import humanize_chapter_slug, humanize_citation_key


# ---------------------------------------------------------------------------
# humanize_chapter_slug (Theme 8)
# ---------------------------------------------------------------------------


def test_humanize_chapter_slug_hamming_two_digit():
    out = humanize_chapter_slug(
        "hammingArtDoingScience2020_03_history-of-computers-hardware"
    )
    assert out == "Chapter 3: history of computers hardware"


def test_humanize_chapter_slug_single_digit_no_padding():
    out = humanize_chapter_slug("hammingArtDoingScience2020_1_orientation")
    assert out == "Chapter 1: orientation"


def test_humanize_chapter_slug_two_digit_chapter_number():
    out = humanize_chapter_slug("paper2024_12_foo-bar-baz")
    assert out == "Chapter 12: foo bar baz"


def test_humanize_chapter_slug_returns_none_for_non_chapter():
    assert humanize_chapter_slug("bishopDeepLearningFoundations2024") is None


def test_humanize_chapter_slug_returns_none_for_empty():
    assert humanize_chapter_slug("") is None


def test_humanize_chapter_slug_returns_none_when_no_chapter_number():
    # Suffix exists but no numeric segment between base and slug.
    assert humanize_chapter_slug("paper2024_some-arbitrary-suffix") is None


def test_humanize_chapter_slug_strips_at_prefix():
    out = humanize_chapter_slug("@paper2024_05_some-slug")
    assert out == "Chapter 5: some slug"


# ---------------------------------------------------------------------------
# humanize_citation_key — regression guard
# ---------------------------------------------------------------------------


def test_humanize_citation_key_unchanged_for_chapter_input():
    # The new humanize_chapter_slug is additive; humanize_citation_key still
    # returns the legacy comma-joined format so existing call sites keep
    # working when the chapter helper falls through.
    out = humanize_citation_key(
        "hammingArtDoingScience2020_03_history-of-computers-hardware"
    )
    assert "Hamming" in out
    assert "Art Doing Science" in out
    assert "2020" in out


def test_humanize_citation_key_base_only():
    assert (
        humanize_citation_key("hammingArtDoingScience2020")
        == "Hamming, Art Doing Science, 2020"
    )
