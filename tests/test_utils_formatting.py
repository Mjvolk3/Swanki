"""
tests/test_utils_formatting.py
[[tests.test_utils_formatting]]
https://github.com/Mjvolk3/Swanki/tree/main/tests/test_utils_formatting.py

Tests for citation-key humanization helpers in swanki.utils.formatting.
Theme 8 fix surface (chapter-slug humanization for lecture bookends).
"""

from swanki.utils.formatting import (
    chapter_number_spoken,
    humanize_chapter_slug,
    humanize_citation_key,
    parse_chapter_key,
)


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


# ---------------------------------------------------------------------------
# parse_chapter_key (foundation for bookend "exact reading")
# ---------------------------------------------------------------------------


def test_parse_chapter_key_basic():
    base, num, slug = parse_chapter_key(
        "hammingArtDoingScience2020_03_history-of-computers-hardware"
    )
    assert base == "hammingArtDoingScience2020"
    assert num == "03"  # leading zero preserved (callers decide rendering)
    assert slug == "history of computers hardware"


def test_parse_chapter_key_strips_at_prefix():
    base, num, slug = parse_chapter_key("@paper2024_05_some-slug")
    assert base == "paper2024"
    assert num == "05"
    assert slug == "some slug"


def test_parse_chapter_key_returns_none_for_non_chapter():
    assert parse_chapter_key("bishopDeepLearning2024") is None
    assert parse_chapter_key("") is None
    assert parse_chapter_key("paper_only-suffix") is None


# ---------------------------------------------------------------------------
# chapter_number_spoken (drives the "o one" / "twelve" rendering in bookends)
# ---------------------------------------------------------------------------


def test_chapter_number_spoken_leading_zero_single_digit():
    assert chapter_number_spoken("01") == "o one"
    assert chapter_number_spoken("02") == "o two"
    assert chapter_number_spoken("05") == "o five"
    assert chapter_number_spoken("09") == "o nine"


def test_chapter_number_spoken_no_leading_zero():
    assert chapter_number_spoken("1") == "one"
    assert chapter_number_spoken("3") == "three"
    assert chapter_number_spoken("12") == "twelve"
    assert chapter_number_spoken("20") == "twenty"


def test_chapter_number_spoken_above_twenty_digit_by_digit():
    # Above the cardinal table; spelled digit-by-digit.
    assert chapter_number_spoken("25") == "two five"
    assert chapter_number_spoken("100") == "one zero zero"
