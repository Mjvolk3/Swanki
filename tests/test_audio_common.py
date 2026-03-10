"""
tests/test_audio_common.py
[[tests.test_audio_common]]
https://github.com/Mjvolk3/Swanki/tree/main/tests/test_audio_common.py
Test file: tests/test_audio_common.py

Tests for pure functions in swanki.audio._common.
"""

from pydub import AudioSegment

from swanki.audio._common import (
    chunk_text,
    clean_markdown_for_tts,
    combine_audio,
    filter_metadata,
    validate_audio_file,
)

# ---------------------------------------------------------------------------
# chunk_text
# ---------------------------------------------------------------------------


def test_chunk_text_single():
    text = "Short paragraph."
    chunks = chunk_text(text)
    assert chunks == ["Short paragraph."]


def test_chunk_text_splits_paragraphs():
    p1 = "A" * 2000
    p2 = "B" * 2000
    text = f"{p1}\n\n{p2}"
    chunks = chunk_text(text, max_chars=3000)
    assert len(chunks) == 2
    assert chunks[0] == p1
    assert chunks[1] == p2


def test_chunk_text_splits_sentences():
    sentences = ". ".join([f"Sentence {i}" for i in range(100)])
    chunks = chunk_text(sentences, max_chars=200)
    assert len(chunks) > 1
    for c in chunks:
        assert len(c) <= 200


def test_chunk_text_respects_max():
    text = "\n\n".join(["Hello world. " * 50 for _ in range(10)])
    chunks = chunk_text(text, max_chars=500)
    for c in chunks:
        assert len(c) <= 500


# ---------------------------------------------------------------------------
# clean_markdown_for_tts
# ---------------------------------------------------------------------------


def test_clean_markdown_headers():
    assert clean_markdown_for_tts("## Introduction") == "Introduction"
    assert clean_markdown_for_tts("### Sub-section") == "Sub-section"


def test_clean_markdown_bold_italic():
    assert (
        clean_markdown_for_tts("This is **bold** and *italic*")
        == "This is bold and italic"
    )


def test_clean_markdown_links():
    assert clean_markdown_for_tts("[click here](https://example.com)") == "click here"


def test_clean_markdown_code():
    assert clean_markdown_for_tts("Use `print()` to output") == "Use print() to output"


# ---------------------------------------------------------------------------
# filter_metadata
# ---------------------------------------------------------------------------


def test_filter_metadata_references():
    content = "Some text.\n\n## References\n\n1. Smith, A. Paper. 2020.\n2. Jones, B. Paper. 2021."
    filtered = filter_metadata(content)
    assert "Some text." in filtered
    assert "Smith" not in filtered


def test_filter_metadata_emails():
    content = "Author info\ncontact@university.edu\nMore content here."
    filtered = filter_metadata(content)
    assert "contact@university.edu" not in filtered
    assert "More content here." in filtered


def test_filter_metadata_affiliations():
    content = (
        "Introduction\nDepartment of Biology\nUniversity of Oxford\nThe study shows..."
    )
    filtered = filter_metadata(content)
    assert "Department of Biology" not in filtered
    assert "University of Oxford" not in filtered
    assert "The study shows..." in filtered


def test_filter_metadata_preserves_content():
    content = "## Introduction\n\nThis paper studies X.\n\n## Methods\n\nWe used Y."
    filtered = filter_metadata(content)
    assert "This paper studies X." in filtered
    assert "We used Y." in filtered


# ---------------------------------------------------------------------------
# combine_audio
# ---------------------------------------------------------------------------


def test_combine_audio(tmp_path):
    f1 = tmp_path / "a.mp3"
    f2 = tmp_path / "b.mp3"
    AudioSegment.silent(duration=1000).export(str(f1), format="mp3")
    AudioSegment.silent(duration=1000).export(str(f2), format="mp3")

    out = tmp_path / "combined.mp3"
    combine_audio([f1, f2], out)

    assert out.exists()
    combined = AudioSegment.from_mp3(str(out))
    # Two 1-second clips with 200ms crossfade -> ~1800ms
    assert len(combined) > 1500


def test_combine_audio_empty(tmp_path):
    out = tmp_path / "empty.mp3"
    combine_audio([], out)
    assert not out.exists()


# ---------------------------------------------------------------------------
# validate_audio_file
# ---------------------------------------------------------------------------


def test_validate_audio_file_missing(tmp_path):
    assert validate_audio_file(tmp_path / "nonexistent.mp3") is False


def test_validate_audio_file_too_small(tmp_path):
    tiny = tmp_path / "tiny.mp3"
    tiny.write_bytes(b"x" * 100)
    assert validate_audio_file(tiny) is False
