"""
tests/test_section_classifier.py
[[tests.test_section_classifier]]
https://github.com/Mjvolk3/Swanki/tree/main/tests/test_section_classifier.py
Test file: tests/test_section_classifier.py

Tests for page-merge helpers in swanki.pipeline.section_classifier.
"""

from pathlib import Path

from swanki.audio._common import add_tts_pauses
from swanki.pipeline.section_classifier import _heading_classify, join_pages


def _pages(tmp_path: Path, texts: list[str]) -> list[Path]:
    """Write each text to page-N.md under tmp_path; return ordered paths."""
    files = []
    for i, t in enumerate(texts):
        p = tmp_path / f"page-{i}.md"
        p.write_text(t)
        files.append(p)
    return files


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


def test_index_registers_midprose_stays_main_content(tmp_path):
    # Regression (Hamming ch04): "index registers" is prose, not a back-matter
    # heading, and sits mid-document. It must NOT flip to back_matter or cascade
    # the drop across the rest of the chapter.
    texts = [
        "# Chapter 4\n\nHistory of computers software intro.",
        "FORTRAN and Algol prose about early languages.",
        "I knew floating point was necessary and I needed index registers "
        "which were not in the machine as delivered.",
        "LISP began around 1962; John McCarthy suggested the elements.",
        "More history prose about compilers and interpreters.",
        "Closing prose for the chapter.",
    ]
    labels = _heading_classify(_pages(tmp_path, texts)).page_labels
    assert [label.kind for label in labels] == ["main_content"] * len(texts)


def test_real_references_heading_in_tail_is_back_matter(tmp_path):
    texts = [
        "# Chapter 1\n\nBody.",
        "More body.",
        "Yet more body.",
        "Final body page.",
        "## References\n\n1. Smith et al. 2020. A paper.",
    ]
    labels = _heading_classify(_pages(tmp_path, texts)).page_labels
    assert labels[-1].kind == "back_matter"
    assert all(label.kind == "main_content" for label in labels[:-1])


def test_references_heading_mid_document_not_back_matter(tmp_path):
    # A real "## References" heading but at page idx 1 of 9 (mid-doc): the
    # positional tail guard rejects it, so content pages are not dropped.
    texts = (
        ["# Chapter 1\n\nBody."]
        + ["## References\n\nstray early heading."]
        + [f"Body page {i}." for i in range(7)]
    )
    labels = _heading_classify(_pages(tmp_path, texts)).page_labels
    assert labels[1].kind == "main_content"
    assert all(label.kind == "main_content" for label in labels)


def test_multi_page_back_matter_run_stays_contiguous(tmp_path):
    # A true tail heading still cascades through a multi-page back-matter run:
    # the heading page flips (heading + tail), the continuation inherits it.
    texts = [f"# Chapter 1\n\nBody page {i}." for i in range(8)] + [
        "## Bibliography\n\n1. First reference.",
        "2. Second reference continues onto this page.",
    ]
    labels = _heading_classify(_pages(tmp_path, texts)).page_labels
    assert labels[8].kind == "back_matter"
    assert labels[9].kind == "back_matter"


def test_front_matter_prose_not_flipped(tmp_path):
    labels = _heading_classify(
        _pages(tmp_path, ["This is a preface to the broader topic of computing."])
    ).page_labels
    assert labels[0].kind == "main_content"


def test_front_matter_heading_is_front_matter(tmp_path):
    labels = _heading_classify(
        _pages(
            tmp_path,
            ["## Preface\n\nThis book is about computing.", "# Chapter 1\n\nBody."],
        )
    ).page_labels
    assert labels[0].kind == "front_matter"
    assert labels[1].kind == "main_content"
