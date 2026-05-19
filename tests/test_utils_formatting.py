"""
tests/test_utils_formatting.py
[[tests.test_utils_formatting]]
https://github.com/Mjvolk3/Swanki/tree/main/tests/test_utils_formatting.py

Tests for citation-key humanization helpers in swanki.utils.formatting.
Theme 8 fix surface (chapter-slug humanization for lecture bookends).
"""

from swanki.utils.formatting import (
    SHORTHAND_EXPANSIONS,
    _llm_guess_shorthand,
    chapter_number_spoken,
    humanize_chapter_slug,
    humanize_chapter_slug_spoken,
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


# ---------------------------------------------------------------------------
# humanize_chapter_slug_spoken (2026.05.19 — bookend roman-numeral fix)
# ---------------------------------------------------------------------------


def test_humanize_chapter_slug_spoken_trailing_roman_one():
    assert (
        humanize_chapter_slug_spoken("artificial intelligence i")
        == "artificial intelligence one"
    )


def test_humanize_chapter_slug_spoken_trailing_roman_two():
    assert (
        humanize_chapter_slug_spoken("artificial intelligence ii")
        == "artificial intelligence two"
    )


def test_humanize_chapter_slug_spoken_trailing_roman_three():
    assert (
        humanize_chapter_slug_spoken("artificial intelligence iii")
        == "artificial intelligence three"
    )


def test_humanize_chapter_slug_spoken_no_trailing_roman_unchanged():
    assert (
        humanize_chapter_slug_spoken("history of computers hardware")
        == "history of computers hardware"
    )


def test_humanize_chapter_slug_spoken_tolerates_hyphenated_input():
    assert (
        humanize_chapter_slug_spoken("digital-filters-iv")
        == "digital filters four"
    )


def test_humanize_chapter_slug_spoken_does_not_touch_mid_slug_letters():
    # "n" in "n dimensional space" is not the trailing token; left alone.
    assert (
        humanize_chapter_slug_spoken("n dimensional space")
        == "n dimensional space"
    )


def test_humanize_chapter_slug_spoken_empty():
    assert humanize_chapter_slug_spoken("") == ""


# ---------------------------------------------------------------------------
# parse_chapter_key — `_CH<NN>_<slug>` form (2026.05.19 — closes the
# feedback_book_chapter_slug convention gap without renaming existing assets)
# ---------------------------------------------------------------------------


def test_parse_chapter_key_accepts_ch_prefix():
    base, num, slug = parse_chapter_key(
        "hammingArtDoingScience2020_CH03_history-of-computers-hardware"
    )
    assert base == "hammingArtDoingScience2020"
    assert num == "03"
    assert slug == "history of computers hardware"


def test_parse_chapter_key_ch_prefix_identical_to_legacy():
    # Non-negotiable: both forms must produce identical tuples so the rest of
    # the pipeline (build_bookend_text etc.) is form-agnostic.
    assert parse_chapter_key(
        "hammingArtDoingScience2020_07_artificial-intelligence-ii"
    ) == parse_chapter_key(
        "hammingArtDoingScience2020_CH07_artificial-intelligence-ii"
    )


def test_parse_chapter_key_ch_prefix_with_at_sign():
    base, num, slug = parse_chapter_key("@paper2024_CH05_some-slug")
    assert base == "paper2024"
    assert num == "05"
    assert slug == "some slug"


def test_parse_chapter_key_two_digit_with_ch():
    base, num, slug = parse_chapter_key("paper2024_CH12_foo-bar-baz")
    assert num == "12"
    assert slug == "foo bar baz"


# ---------------------------------------------------------------------------
# SHORTHAND_EXPANSIONS + _llm_guess_shorthand (2026.05.19 — canonical
# reference for short tokens; LLM fallback stub for unknowns)
# ---------------------------------------------------------------------------


def test_shorthand_expansions_canonical_entries():
    assert SHORTHAND_EXPANSIONS["CH"] == "Chapter"
    assert SHORTHAND_EXPANSIONS["SI"] == "Supplementary Information"
    assert SHORTHAND_EXPANSIONS["S"] == "Section"
    assert SHORTHAND_EXPANSIONS["SEC"] == "Section"
    assert SHORTHAND_EXPANSIONS["PART"] == "Part"
    assert SHORTHAND_EXPANSIONS["APP"] == "Appendix"


def test_shorthand_expansions_keys_uppercase():
    # All keys uppercase so callers can normalize tokens via `.upper()` before
    # lookup without worrying about case.
    assert all(k == k.upper() for k in SHORTHAND_EXPANSIONS)


def test_llm_guess_shorthand_returns_none_today():
    # Inert stub: TODO Haiku/GPT-nano fallback. Until wired, every token
    # returns None so call sites can be deployed without a live LLM dependency.
    assert _llm_guess_shorthand("FIG") is None
    assert _llm_guess_shorthand("UNKNOWN") is None
    assert _llm_guess_shorthand("") is None
