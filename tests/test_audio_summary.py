"""
tests/test_audio_summary.py
[[tests.test_audio_summary]]
https://github.com/Mjvolk3/Swanki/tree/main/tests/test_audio_summary.py
Test file: tests/test_audio_summary.py

Tests for swanki.audio.summary -- mocked summary audio generation.
"""

from unittest.mock import MagicMock, patch

from pydub import AudioSegment

from swanki.audio.summary import generate_summary_audio


def test_generate_summary_audio_mocked(tmp_audio_dir, mock_elevenlabs_api_key):
    output = tmp_audio_dir / "summary.mp3"

    mock_result = MagicMock()
    mock_result.output = "This paper introduces a novel method."

    with (
        patch("swanki.audio.summary.text_agent") as mock_agent,
        patch("swanki.audio.summary.text_to_speech") as mock_tts,
        patch("swanki.audio.summary.combine_audio_with_section_pauses") as mock_combine,
    ):
        mock_agent.run_sync.return_value = mock_result

        def fake_tts(text, voice_id, output_path, api_key, speed=1.0):
            AudioSegment.silent(duration=1000).export(str(output_path), format="mp3")

        mock_tts.side_effect = fake_tts
        mock_combine.side_effect = lambda sections, output, **kw: AudioSegment.silent(
            duration=2000
        ).export(str(output), format="mp3")

        filename = generate_summary_audio(
            summary_text="This paper introduces a novel method.",
            output_path=output,
            elevenlabs_api_key=mock_elevenlabs_api_key,
        )

        assert filename == "summary.mp3"
        mock_tts.assert_called()

    # Transcript files should be saved
    transcript_dir = tmp_audio_dir / "summary_transcript"
    assert transcript_dir.exists()


def test_summary_with_citation(tmp_audio_dir, mock_elevenlabs_api_key):
    output = tmp_audio_dir / "summary.mp3"

    mock_result = MagicMock()
    mock_result.output = (
        "Smith, Novel Method, 2023. This paper introduces a novel method."
    )

    with (
        patch("swanki.audio.summary.text_agent") as mock_agent,
        patch("swanki.audio.summary.text_to_speech") as mock_tts,
        patch("swanki.audio.summary.generate_bookend_audio") as mock_bookend,
        patch("swanki.audio.summary.combine_audio_with_section_pauses") as mock_combine,
    ):
        mock_agent.run_sync.return_value = mock_result

        def fake_tts(text, voice_id, output_path, api_key, speed=1.0):
            AudioSegment.silent(duration=1000).export(str(output_path), format="mp3")

        mock_tts.side_effect = fake_tts
        mock_bookend.return_value = tmp_audio_dir / "bookend.mp3"
        mock_combine.side_effect = lambda sections, output, **kw: AudioSegment.silent(
            duration=2000
        ).export(str(output), format="mp3")

        generate_summary_audio(
            summary_text="This paper introduces a novel method.",
            output_path=output,
            elevenlabs_api_key=mock_elevenlabs_api_key,
            citation_key="smithNovelMethod2023",
        )

    # Check that the transcript includes citation info
    transcript_dir = tmp_audio_dir / "summary_transcript"
    transcript_file = transcript_dir / "summary_transcript.md"
    content = transcript_file.read_text()
    assert "smithNovelMethod2023" in content
