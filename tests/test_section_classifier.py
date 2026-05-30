"""
tests/test_section_classifier.py
[[tests.test_section_classifier]]
https://github.com/Mjvolk3/Swanki/tree/main/tests/test_section_classifier.py
Test file: tests/test_section_classifier.py

Tests for page-merge helpers in swanki.pipeline.section_classifier.
"""

from swanki.audio._common import add_tts_pauses
from swanki.pipeline.section_classifier import join_pages


def test_join_pages_glues_mid_sentence_break():
    # Hamming Ch1 p4->p5: a sentence split across the page boundary must be
    # spoken continuously, not separated by an audible pause.
    merged = join_pages(
        ["...learn new fields of knowledge when", "they arise so you will not"]
    )
    assert merged == "...learn new fields of knowledge when they arise so you will not"
    # And it must NOT become a [pause] once TTS pauses are applied.
    assert "knowledge when they arise" in add_tts_pauses(merged, "fish_speech")


def test_join_pages_keeps_break_after_sentence_end():
    merged = join_pages(["A first sentence.", "A second one."])
    assert merged == "A first sentence.\n\nA second one."
    # The blank line promotes to an inter-page pause for Fish.
    assert "[pause]" in add_tts_pauses(merged, "fish_speech")


def test_join_pages_treats_comma_and_dash_as_continuation():
    assert join_pages(["...of being right,", "studying successes"]) == (
        "...of being right, studying successes"
    )
    assert join_pages(["a thought—", "continued"]) == "a thought— continued"


def test_join_pages_respects_closing_punctuation_after_terminal():
    # Closing quote/paren after terminal punctuation still ends the sentence.
    assert join_pages(['He said "done."', "Next page."]) == (
        'He said "done."\n\nNext page.'
    )
    assert join_pages(["(an aside.)", "Next."]) == "(an aside.)\n\nNext."


def test_join_pages_skips_empty_pages_and_strips():
    assert join_pages(["  first.  ", "", "   ", "second."]) == "first.\n\nsecond."


def test_join_pages_single_and_empty():
    assert join_pages(["only page"]) == "only page"
    assert join_pages([]) == ""
    assert join_pages(["", "   "]) == ""
