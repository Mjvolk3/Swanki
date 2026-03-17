"""
tests/test_audio_reading.py
[[tests.test_audio_reading]]
https://github.com/Mjvolk3/Swanki/tree/main/tests/test_audio_reading.py
Test file: tests/test_audio_reading.py

Tests for swanki.audio.reading -- mocked reading audio and LaTeX humanization.
"""

from unittest.mock import MagicMock, patch

from pydub import AudioSegment

from swanki.audio.reading import _humanize_latex, generate_reading_audio


def test_generate_reading_audio_mocked(tmp_audio_dir, mock_elevenlabs_api_key):
    output = tmp_audio_dir / "reading.mp3"

    mock_result = MagicMock()
    mock_result.output = "Humanized and optimized text for audio."

    with (
        patch("swanki.audio.reading.text_agent") as mock_agent,
        patch("swanki.audio.reading.text_to_speech") as mock_tts,
        patch("swanki.audio.reading.combine_audio_with_section_pauses") as mock_combine,
    ):
        mock_agent.run_sync.return_value = mock_result

        def fake_tts(text, voice_id, output_path, api_key, speed=1.0, **kwargs):
            AudioSegment.silent(duration=1000).export(str(output_path), format="mp3")

        mock_tts.side_effect = fake_tts
        mock_combine.side_effect = lambda sections, output, **kw: AudioSegment.silent(
            duration=2000
        ).export(str(output), format="mp3")

        filename = generate_reading_audio(
            full_content="Introduction. This paper presents a method.",
            output_path=output,
            elevenlabs_api_key=mock_elevenlabs_api_key,
        )

        assert filename == "reading.mp3"
        mock_tts.assert_called()

    transcript_dir = tmp_audio_dir / "full_read"
    assert transcript_dir.exists()


def test_humanize_latex():
    mock_result = MagicMock()
    mock_result.output = "The variable alpha equals 5."

    with patch("swanki.audio.reading.text_agent") as mock_agent:
        mock_agent.run_sync.return_value = mock_result

        result = _humanize_latex(
            "The variable $\\alpha$ equals 5.", "openai:gpt-5-mini"
        )

        assert isinstance(result, str)
        assert len(result) > 0
        mock_agent.run_sync.assert_called()
