"""
tests/test_audio_card.py
[[tests.test_audio_card]]
https://github.com/Mjvolk3/Swanki/tree/main/tests/test_audio_card.py
Test file: tests/test_audio_card.py

Tests for swanki.audio.card -- cloze handling, prompt construction, and mocked generation.
"""

from unittest.mock import MagicMock, patch

from pydub import AudioSegment

from swanki.audio.card import (
    _build_transcript_system_prompt,
    _replace_all_cloze_with_blank,
    generate_card_audio,
    generate_card_transcript,
    generate_citation_audio,
)
from swanki.models.cards import CardContent, PlainCard


def _make_card(front_text, back_text="Answer", **kwargs):
    return PlainCard(
        front=CardContent(text=front_text),
        back=CardContent(text=back_text),
        tags=["test"],
        **kwargs,
    )


# ---------------------------------------------------------------------------
# _replace_all_cloze_with_blank
# ---------------------------------------------------------------------------


def test_replace_cloze_with_blank_simple():
    assert _replace_all_cloze_with_blank("{{c1::hello}}") == "blank"


def test_replace_cloze_with_blank_nested():
    text = "{{c1::$\\frac{a}{b}$}}"
    result = _replace_all_cloze_with_blank(text)
    assert result == "blank"
    assert "{{" not in result


def test_replace_cloze_with_blank_multiple():
    text = "{{c1::alpha}} and {{c2::beta}}"
    result = _replace_all_cloze_with_blank(text)
    assert result == "blank and blank"


# ---------------------------------------------------------------------------
# _build_transcript_system_prompt
# ---------------------------------------------------------------------------


def test_build_prompt_front_regular():
    prompt = _build_transcript_system_prompt(
        is_front=True, is_cloze=False, has_image=False
    )
    assert "QUESTION" in prompt
    assert "blank" not in prompt.lower()
    assert "NO IMAGE" in prompt


def test_build_prompt_front_cloze():
    prompt = _build_transcript_system_prompt(
        is_front=True, is_cloze=True, has_image=False
    )
    assert "blank" in prompt.lower()
    assert "NO IMAGE" in prompt


def test_build_prompt_back_cloze():
    prompt = _build_transcript_system_prompt(
        is_front=False, is_cloze=True, has_image=False
    )
    assert "Do NOT say 'blank'" in prompt or "do NOT say 'blank'" in prompt.lower()


def test_build_prompt_with_image():
    prompt = _build_transcript_system_prompt(
        is_front=True, is_cloze=False, has_image=True
    )
    assert "image" in prompt.lower()
    assert "NO IMAGE" not in prompt


def test_build_prompt_front_image_not_framed_as_answer():
    # The front image description is perceptual; the prompt must not imply it
    # answers the question.
    prompt = _build_transcript_system_prompt(
        is_front=True, is_cloze=False, has_image=True
    )
    assert "does NOT answer the question" in prompt


# ---------------------------------------------------------------------------
# front/back image-description picker (perceptual vs interpretive)
# ---------------------------------------------------------------------------


def _make_image_card(*, front_image: bool, perceptual, interpretive) -> PlainCard:
    """Build an image card with both summaries on whichever side holds the image."""
    front = CardContent(text="Why is dark-field microscopy useful?")
    back = CardContent(text="It improves contrast.")
    side = front if front_image else back
    side.image_path = "images/fig.png"
    side.image_summary = interpretive
    side.image_summary_perceptual = perceptual
    return PlainCard(front=front, back=back, tags=["test"])


def _sent_content(mock_agent) -> str:
    return " ".join(str(call.args[0]) for call in mock_agent.run_sync.call_args_list)


def test_front_audio_speaks_perceptual_not_interpretive():
    card = _make_image_card(
        front_image=True,
        perceptual="Bright glowing cell outlines on a dark field",
        interpretive="This scatters oblique light to boost contrast",
    )
    mock_result = MagicMock()
    mock_result.output = "Mocked"
    with patch("swanki.audio.card.text_agent") as mock_agent:
        mock_agent.run_sync.return_value = mock_result
        generate_card_transcript(card, is_front=True, model="openai:test")
        sent = _sent_content(mock_agent)
    assert "glowing" in sent
    assert "oblique" not in sent


def test_front_audio_falls_back_to_interpretive_when_no_perceptual():
    card = _make_image_card(
        front_image=True,
        perceptual=None,
        interpretive="This scatters oblique light to boost contrast",
    )
    mock_result = MagicMock()
    mock_result.output = "Mocked"
    with patch("swanki.audio.card.text_agent") as mock_agent:
        mock_agent.run_sync.return_value = mock_result
        generate_card_transcript(card, is_front=True, model="openai:test")
        sent = _sent_content(mock_agent)
    assert "oblique" in sent


def test_back_audio_speaks_interpretive_not_perceptual():
    card = _make_image_card(
        front_image=False,
        perceptual="Bright glowing cell outlines on a dark field",
        interpretive="This scatters oblique light to boost contrast",
    )
    mock_result = MagicMock()
    mock_result.output = "Mocked"
    with patch("swanki.audio.card.text_agent") as mock_agent:
        mock_agent.run_sync.return_value = mock_result
        generate_card_transcript(card, is_front=False, model="openai:test")
        sent = _sent_content(mock_agent)
    assert "oblique" in sent
    assert "glowing" not in sent


# ---------------------------------------------------------------------------
# generate_card_transcript (mocked)
# ---------------------------------------------------------------------------


def test_generate_card_transcript_mocked():
    card = _make_card("What is X?")

    mock_result = MagicMock()
    mock_result.output = "Mocked transcript text"

    with patch("swanki.audio.card.text_agent") as mock_agent:
        mock_agent.run_sync.return_value = mock_result
        transcript = generate_card_transcript(card, is_front=True, model="openai:test")
        assert isinstance(transcript, str)
        assert len(transcript) > 0
        mock_agent.run_sync.assert_called()


# ---------------------------------------------------------------------------
# generate_citation_audio (mocked)
# ---------------------------------------------------------------------------


def test_generate_citation_audio_mocked(tmp_audio_dir, mock_elevenlabs_api_key):
    output = tmp_audio_dir / "citation.mp3"

    mock_result = MagicMock()
    mock_result.output = "Smith, Machine Learning, 2023"

    with (
        patch("swanki.audio.card.text_agent") as mock_agent,
        patch("swanki.audio.card.text_to_speech") as mock_tts,
        patch("swanki.audio.card.validate_audio_file", return_value=True),
    ):
        mock_agent.run_sync.return_value = mock_result

        def fake_tts(text, voice_id, output_path, api_key, speed=1.0, **kwargs):
            AudioSegment.silent(duration=1000).export(str(output_path), format="mp3")

        mock_tts.side_effect = fake_tts

        result = generate_citation_audio(
            citation_key="smithML2023",
            output_path=output,
            elevenlabs_api_key=mock_elevenlabs_api_key,
            model="openai:test",
        )
        assert result == output


# ---------------------------------------------------------------------------
# generate_card_audio (mocked)
# ---------------------------------------------------------------------------


def test_generate_card_audio_mocked(tmp_audio_dir, mock_elevenlabs_api_key):
    card = _make_card("What is ML?", "Machine learning is...")

    mock_result = MagicMock()
    mock_result.output = "Mocked transcript text"

    with (
        patch("swanki.audio.card.text_agent") as mock_agent,
        patch("swanki.audio.card.text_to_speech") as mock_tts,
    ):
        mock_agent.run_sync.return_value = mock_result

        def fake_tts(text, voice_id, output_path, api_key, speed=1.0, **kwargs):
            AudioSegment.silent(duration=1000).export(str(output_path), format="mp3")

        mock_tts.side_effect = fake_tts

        front_file, back_file = generate_card_audio(
            card=card,
            card_index=1,
            page_base="page-1",
            audio_dir=tmp_audio_dir,
            elevenlabs_api_key=mock_elevenlabs_api_key,
            model="openai:test",
        )

        assert front_file.endswith("_front.mp3")
        assert back_file.endswith("_back.mp3")
        assert mock_tts.call_count >= 2
