"""
tests/test_audio_reading.py
[[tests.test_audio_reading]]
https://github.com/Mjvolk3/Swanki/tree/main/tests/test_audio_reading.py
Test file: tests/test_audio_reading.py

Tests for swanki.audio.reading -- mocked reading audio and LaTeX humanization.
"""

from unittest.mock import patch

from pydub import AudioSegment

from swanki.audio.reading import _humanize_latex, generate_reading_audio


def test_generate_reading_audio_mocked(
    tmp_audio_dir, mock_openai_client, mock_elevenlabs_api_key
):
    output = tmp_audio_dir / "reading.mp3"

    with (
        patch("swanki.audio.reading.text_to_speech") as mock_tts,
        patch("swanki.audio.reading.combine_audio") as mock_combine,
    ):

        def fake_tts(text, voice_id, output_path, api_key, speed=1.0):
            AudioSegment.silent(duration=1000).export(str(output_path), format="mp3")

        mock_tts.side_effect = fake_tts
        mock_combine.side_effect = lambda files, output, **kw: AudioSegment.silent(
            duration=2000
        ).export(str(output), format="mp3")

        filename = generate_reading_audio(
            full_content="Introduction. This paper presents a method.",
            output_path=output,
            openai_client=mock_openai_client,
            elevenlabs_api_key=mock_elevenlabs_api_key,
        )

        assert filename == "reading.mp3"
        mock_tts.assert_called()

    transcript_dir = tmp_audio_dir / "full_read"
    assert transcript_dir.exists()


def test_humanize_latex(mock_openai_client):
    mock_openai_client.chat.completions.create.return_value.choices[
        0
    ].message.content = "The variable alpha equals 5."

    result = _humanize_latex(
        "The variable $\\alpha$ equals 5.", mock_openai_client, "gpt-5-mini"
    )

    assert isinstance(result, str)
    assert len(result) > 0
    mock_openai_client.chat.completions.create.assert_called()
