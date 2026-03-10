"""
tests/test_audio_lecture.py
[[tests.test_audio_lecture]]
https://github.com/Mjvolk3/Swanki/tree/main/tests/test_audio_lecture.py
Test file: tests/test_audio_lecture.py

Tests for swanki.audio.lecture -- semantic chunking and mocked lecture generation.
"""

from unittest.mock import patch

from pydub import AudioSegment

from swanki.audio.lecture import (
    _extract_context,
    _split_large_section,
    chunk_by_headers,
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
