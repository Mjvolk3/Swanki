"""
tests/test_audio_reading.py
[[tests.test_audio_reading]]
https://github.com/Mjvolk3/Swanki/tree/main/tests/test_audio_reading.py
Test file: tests/test_audio_reading.py

Tests for swanki.audio.reading -- mocked reading audio and LaTeX humanization.
"""

from unittest.mock import MagicMock, patch

from pydub import AudioSegment

from swanki.audio._common import humanize_latex
from swanki.audio.reading import (
    _READING_COVERAGE_MIN_RATIO,
    generate_reading_audio,
    reading_coverage_ratio,
)

# ---------------------------------------------------------------------------
# RC2: reading completeness guard (deterministic, no LLM)
# ---------------------------------------------------------------------------


def test_reading_coverage_full_passthrough_is_one():
    src = "Hamming argues that great work needs vision and courage."
    assert reading_coverage_ratio(src, src) == 1.0


def test_reading_coverage_expansion_stays_above_threshold():
    # Pass-2 only ever expands (acronym letter-spelling, citation rendering),
    # so a faithful transcript is >= source and must NOT trip the guard.
    src = "The SAR system and the CPU were new in 1950."
    transcript = (
        "The S-A-R system and the C-P-U were new in 1950. "
        "Hamming, 1986, notes this."
    )
    assert reading_coverage_ratio(src, transcript) >= _READING_COVERAGE_MIN_RATIO


def test_reading_coverage_dropped_paragraph_trips_guard():
    # A genuine ~30% drop (one of three sentences omitted) falls below 0.95.
    src = (
        "They arise so you will not be left behind, as so many good "
        "engineers are in the long run. In the position I found myself in "
        "at the Laboratories, I had a choice. The past was once the future."
    )
    dropped = (
        "In the position I found myself in at the Laboratories, I had a "
        "choice. The past was once the future."
    )
    assert reading_coverage_ratio(src, dropped) < _READING_COVERAGE_MIN_RATIO


def test_reading_coverage_empty_source_is_one():
    assert reading_coverage_ratio("", "anything") == 1.0


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
            model="openai:test",
        )

        assert filename == "reading.mp3"
        mock_tts.assert_called()

    transcript_dir = tmp_audio_dir / "full_read"
    assert transcript_dir.exists()


def test_humanize_latex():
    mock_result = MagicMock()
    mock_result.output = "The variable alpha equals 5."

    with patch("swanki.audio._common.text_agent") as mock_agent:
        mock_agent.run_sync.return_value = mock_result

        result = humanize_latex(
            "The variable $\\alpha$ equals 5.", "openai:test"
        )

        assert isinstance(result, str)
        assert len(result) > 0
        mock_agent.run_sync.assert_called()
