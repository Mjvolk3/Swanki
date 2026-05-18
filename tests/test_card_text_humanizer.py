"""
tests/test_card_text_humanizer.py
[[tests.test_card_text_humanizer]]
https://github.com/Mjvolk3/Swanki/tree/main/tests/test_card_text_humanizer.py

Unit tests for ``humanize_card_text_for_tts`` — the pre-LLM transcript pass
that expands problem-set type-label abbreviations (T/F, MC, canonical IDs
like MAT-CH1-3) and chapter / section scaffolding tokens so Fish Speech
reads them as natural prose instead of garbled letter sequences.
"""

import pytest

from swanki.utils.formatting import humanize_card_text_for_tts


class TestShortFormLabels:
    """The card-gen prompt enforces short-form labels like ``T/F 12:``."""

    def test_true_false_short(self) -> None:
        assert humanize_card_text_for_tts(
            "T/F 12: Microorganisms form the foundations."
        ) == "True or false 12: Microorganisms form the foundations."

    def test_multiple_choice_short(self) -> None:
        assert humanize_card_text_for_tts(
            "MC 13: Robert Koch is remembered."
        ) == "Multiple choice 13: Robert Koch is remembered."

    def test_matching_already_full_word_unchanged(self) -> None:
        assert humanize_card_text_for_tts(
            "Matching 6: Match the cell-shape description."
        ) == "Matching 6: Match the cell-shape description."

    def test_completion_already_full_word_unchanged(self) -> None:
        assert humanize_card_text_for_tts(
            "Completion 7: The six-carbon sugar is ____."
        ) == "Completion 7: The six-carbon sugar is ____."

    def test_problem_canonical_form_unchanged(self) -> None:
        # Theory problems use book-canonical "N.M" — readable by TTS as-is.
        assert humanize_card_text_for_tts(
            "Problem 1.30: Why are viruses not organisms?"
        ) == "Problem 1.30: Why are viruses not organisms?"


class TestLongFormLabels:
    """Defense-in-depth: the canonical problem_id form (LLM regression)."""

    def test_long_tf_form(self) -> None:
        assert humanize_card_text_for_tts(
            "TF-CH1-12: Microorganisms form the foundations."
        ) == "True or false 12: Microorganisms form the foundations."

    def test_long_mc_form(self) -> None:
        assert humanize_card_text_for_tts(
            "MC-CH1-13: Robert Koch is remembered."
        ) == "Multiple choice 13: Robert Koch is remembered."

    def test_long_matching_form(self) -> None:
        assert humanize_card_text_for_tts(
            "MAT-CH1-3: Match the description."
        ) == "Matching 3: Match the description."

    def test_long_completion_form(self) -> None:
        assert humanize_card_text_for_tts(
            "CMP-CH2-9: Fill in the blank."
        ) == "Completion 9: Fill in the blank."


class TestChapterSectionAbbreviations:
    def test_chapter_with_period_abbrev(self) -> None:
        assert humanize_card_text_for_tts("See Ch. 1 for details.") == \
            "See chapter 1 for details."

    def test_chapter_full_word_unchanged_form(self) -> None:
        # "Chapter 1" already reads naturally; we still normalize to lowercase
        # for consistent voicing.
        assert humanize_card_text_for_tts("Chapter 1 covers the basics.") == \
            "chapter 1 covers the basics."

    def test_chapter_bare_uppercase(self) -> None:
        assert humanize_card_text_for_tts("Also CH3 mentions photosynthesis.") == \
            "Also chapter 3 mentions photosynthesis."

    def test_section_with_period_abbrev(self) -> None:
        assert humanize_card_text_for_tts("See Sec. 4 for the proof.") == \
            "See section 4 for the proof."

    def test_section_bare_uppercase(self) -> None:
        assert humanize_card_text_for_tts("Refer to SEC2 for syntax.") == \
            "Refer to section 2 for syntax."


class TestChoiceLabels:
    """``(a)`` / ``(b)`` / ... at the start of a line are converted to ``A. ``
    / ``B. `` because Fish Speech tokenizes parentheses as phonetic glyphs
    (sounds like "pee a oh") and sometimes duplicates or skips choices.
    """

    def test_mc_choices_stripped(self) -> None:
        text = (
            "Multiple choice 2: Among the foods produced for human "
            "consumption by microorganisms is\n"
            "(a) milk\n"
            "(b) ham\n"
            "(c) yogurt\n"
            "(d) cucumbers"
        )
        expected = (
            "Multiple choice 2: Among the foods produced for human "
            "consumption by microorganisms is\n"
            "A. milk\n"
            "B. ham\n"
            "C. yogurt\n"
            "D. cucumbers"
        )
        assert humanize_card_text_for_tts(text) == expected

    def test_matching_options_stripped(self) -> None:
        text = (
            "Matching 6: Match the cell-shape description to the organism "
            "group:\n"
            "(a) Bacteria\n"
            "(b) Fungi\n"
            "(c) Viruses"
        )
        expected = (
            "Matching 6: Match the cell-shape description to the organism "
            "group:\n"
            "A. Bacteria\n"
            "B. Fungi\n"
            "C. Viruses"
        )
        assert humanize_card_text_for_tts(text) == expected

    def test_inline_choice_reference_preserved(self) -> None:
        # The line-anchor ``^`` (multiline mode) keeps mid-line references
        # like "see (a) above" intact — they read fine inline.
        text = "The pattern in option (a) and option (b) demonstrates the rule."
        assert humanize_card_text_for_tts(text) == text


class TestNoFalsePositives:
    """Tokens that look label-like but should NOT be expanded."""

    def test_lone_p_letter_unchanged(self) -> None:
        # ``P`` was deliberately removed from the expansion table because too
        # many false positives arise in body text (phosphorus, probability).
        text = "Phosphorus is element P. Probability is p(x)."
        assert humanize_card_text_for_tts(text) == text

    def test_label_without_trailing_colon_unchanged(self) -> None:
        # Without the trailing ":", the regex doesn't fire — embedded mentions
        # in prose like "we'll cover the MC 13 question" stay intact.
        text = "Discussion of the MC 13 question follows."
        assert humanize_card_text_for_tts(text) == text

    def test_label_embedded_mid_word_unchanged(self) -> None:
        # The lookbehind ``(?:^|(?<=[:\s]))`` requires a word boundary; "QMC 13:"
        # (Q + MC) does not start at a boundary so the pattern doesn't fire.
        text = "QMC 13: not a real label."
        assert humanize_card_text_for_tts(text) == text


class TestEdgeCases:
    def test_empty_string(self) -> None:
        assert humanize_card_text_for_tts("") == ""

    def test_no_labels(self) -> None:
        text = "Photosynthesis converts light energy to chemical energy."
        assert humanize_card_text_for_tts(text) == text

    def test_label_after_humanized_citation_prefix(self) -> None:
        # Mirrors the real flow: ``humanize_citation_key`` runs first, producing
        # a comma-separated form ("Alcamo Schaums Outline Microbiology, 2010,
        # CH01"), then this humanizer expands "CH01" (word-bounded) and the
        # short label "T/F 12:".
        text = (
            "Alcamo Schaums Outline Microbiology, 2010, CH01: "
            "T/F 12: The statement."
        )
        assert humanize_card_text_for_tts(text) == (
            "Alcamo Schaums Outline Microbiology, 2010, chapter 1: "
            "True or false 12: The statement."
        )

    def test_chapter_inside_underscore_identifier_unchanged(self) -> None:
        # Underscores are word characters in regex, so ``\b`` does NOT match
        # between ``_`` and ``CH`` — identifier-shaped tokens are left intact
        # as a safety property.
        text = "Tag: alcamo2010_CH01.problem.MC-CH1-13"
        assert humanize_card_text_for_tts(text) == text
