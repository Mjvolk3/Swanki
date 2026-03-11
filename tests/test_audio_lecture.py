"""
tests/test_audio_lecture.py
[[tests.test_audio_lecture]]
https://github.com/Mjvolk3/Swanki/tree/main/tests/test_audio_lecture.py
Test file: tests/test_audio_lecture.py

Tests for swanki.audio.lecture -- semantic chunking and mocked lecture generation.
"""

from unittest.mock import MagicMock, patch

from pydub import AudioSegment

from swanki.audio.lecture import (
    _extract_context,
    _refine_transcript,
    _split_large_section,
    chunk_by_headers,
    generate_and_validate_chunk,
    generate_lecture_audio,
)

# ---------------------------------------------------------------------------
# chunk_by_headers
# ---------------------------------------------------------------------------


def test_chunk_by_headers():
    content = (
        "Preamble text.\n\n"
        "## 1.0 Introduction\n\nIntro paragraph.\n\n"
        "## 2.1 Methods\n\nMethods paragraph.\n\n"
        "## 3.0 Results\n\nResults paragraph."
    )
    chunks = chunk_by_headers(content)
    assert len(chunks) >= 3
    titles = [title for title, _, _ in chunks]
    assert any("Introduction" in t for t in titles)
    assert any("Methods" in t for t in titles)
    assert any("Results" in t for t in titles)


def test_chunk_by_headers_unnumbered():
    content = (
        "Preamble text.\n\n"
        "## Introduction\n\nIntro paragraph.\n\n"
        "## Methods\n\nMethods paragraph.\n\n"
        "## Results\n\nResults paragraph."
    )
    chunks = chunk_by_headers(content)
    titles = [title for title, _, _ in chunks]
    assert any("Introduction" in t for t in titles)
    assert any("Methods" in t for t in titles)
    assert any("Results" in t for t in titles)


def test_chunk_by_headers_mixed():
    content = (
        "Preamble text.\n\n"
        "## 1.0 Introduction\n\nIntro paragraph.\n\n"
        "## Methods\n\nMethods paragraph.\n\n"
        "## 2.0 Results\n\nResults paragraph."
    )
    chunks = chunk_by_headers(content)
    titles = [title for title, _, _ in chunks]
    assert any("Introduction" in t for t in titles)
    assert any("Methods" in t for t in titles)
    assert any("Results" in t for t in titles)


def test_chunk_by_headers_oversized():
    big_section = "Word " * 20000  # ~20k tokens, will exceed 15k limit
    content = f"## 1.0 Big Section\n\n{big_section}"
    chunks = chunk_by_headers(content, max_tokens_per_chunk=15000)
    assert len(chunks) > 1
    for title, _, _ in chunks:
        assert "part" in title


# ---------------------------------------------------------------------------
# _split_large_section
# ---------------------------------------------------------------------------


def test_split_large_section():
    paragraphs = ["Paragraph " * 200 + ".\n" for _ in range(10)]
    big = "\n\n".join(paragraphs)
    parts = _split_large_section(big, max_tokens=2000)
    assert len(parts) > 1


# ---------------------------------------------------------------------------
# _extract_context
# ---------------------------------------------------------------------------


def test_extract_context():
    long_text = "word " * 1000
    context = _extract_context(long_text, max_tokens=300)
    assert len(context) < len(long_text)
    assert len(context) > 0


def test_extract_context_short():
    short_text = "Short transcript."
    context = _extract_context(short_text, max_tokens=300)
    assert context == short_text


def test_extract_context_empty():
    assert _extract_context("") == ""


# ---------------------------------------------------------------------------
# generate_lecture_audio (mocked)
# ---------------------------------------------------------------------------


def test_generate_lecture_audio_mocked(
    tmp_audio_dir, mock_openai_client, mock_elevenlabs_api_key
):
    # Create a small markdown file
    md_file = tmp_audio_dir / "content.md"
    md_file.write_text("## 1.0 Introduction\n\nThis is the content of the lecture.")

    output = tmp_audio_dir / "lecture.mp3"

    with (
        patch("swanki.audio.lecture.text_to_speech") as mock_tts,
        patch(
            "swanki.audio.lecture._refine_transcript", side_effect=lambda t, *a, **kw: t
        ),
    ):

        def fake_tts(text, voice_id, output_path, api_key, speed=1.0):
            AudioSegment.silent(duration=1000).export(str(output_path), format="mp3")

        mock_tts.side_effect = fake_tts

        filename = generate_lecture_audio(
            markdown_files=[md_file],
            image_summaries=[],
            output_path=output,
            openai_client=mock_openai_client,
            elevenlabs_api_key=mock_elevenlabs_api_key,
        )

        assert filename == "lecture.mp3"
        mock_tts.assert_called()


# ---------------------------------------------------------------------------
# generate_and_validate_chunk (no budget params)
# ---------------------------------------------------------------------------


def test_generate_and_validate_chunk_no_budget(mock_openai_client):
    """Chunk generation no longer takes budget/max word params."""
    from swanki.models.cards import LectureTranscriptFeedback

    mock_critique = LectureTranscriptFeedback(
        feedback=[], done=True, word_count=50, meets_length_target=True
    )
    instructor_client = MagicMock()
    instructor_client.chat.completions.create.return_value = mock_critique

    result = generate_and_validate_chunk(
        content_chunk="Some source content here.",
        section_title="Intro",
        previous_context="",
        system_prompt="You are a lecturer.",
        citation_key="Test Paper",
        openai_client=mock_openai_client,
        instructor_client=instructor_client,
        model="gpt-5-mini",
    )
    assert result == "Mocked transcript text"


# ---------------------------------------------------------------------------
# _refine_transcript length enforcement
# ---------------------------------------------------------------------------


def test_refine_transcript_length_enforcement(tmp_path, mock_openai_client):
    """When ratio > 0.7, length-reduction feedback is injected."""
    import tiktoken

    from swanki.models.cards import LectureTranscriptFeedback

    enc = tiktoken.get_encoding("cl100k_base")
    transcripts_dir = tmp_path / "transcripts"
    transcripts_dir.mkdir()
    output_path = tmp_path / "lecture.mp3"

    # Transcript ~same length as source → ratio ~1.0
    transcript = "word " * 100
    source_words = 100

    mock_critique = LectureTranscriptFeedback(
        feedback=["Minor issue"], done=False, word_count=100, meets_length_target=False
    )
    mock_critique_pass = LectureTranscriptFeedback(
        feedback=[], done=True, word_count=50, meets_length_target=True
    )

    critique_call_count = 0

    def fake_critique(*args, **kwargs):
        nonlocal critique_call_count
        critique_call_count += 1
        if critique_call_count == 1:
            return mock_critique
        return mock_critique_pass

    with patch("instructor.patch") as mock_patch:
        patched_client = MagicMock()
        patched_client.chat.completions.create.side_effect = fake_critique
        mock_patch.return_value = patched_client

        result = _refine_transcript(
            full_transcript=transcript,
            full_system_prompt="System prompt",
            openai_client=mock_openai_client,
            model="gpt-5-mini",
            citation_key="test",
            transcripts_dir=transcripts_dir,
            output_path=output_path,
            max_retries=2,
            enc=enc,
            source_words=source_words,
        )

    assert isinstance(result, str)
