"""
tests/test_audio_reading.py
[[tests.test_audio_reading]]
https://github.com/Mjvolk3/Swanki/tree/main/tests/test_audio_reading.py
Test file: tests/test_audio_reading.py

Tests for swanki.audio.reading -- mocked reading audio, LaTeX humanization,
and per-chunk completeness retry/fallback in both passes.
"""

from unittest.mock import MagicMock, patch

from pydub import AudioSegment

from swanki.audio._common import (
    _HUMANIZE_CHUNK_MIN_RATIO,
    _humanize_chunk_with_completeness,
    humanize_latex,
)
from swanki.audio.reading import (
    _PASS2_CHUNK_MIN_RATIO,
    _pass2_chunk_with_completeness,
    generate_reading_audio,
    reading_coverage_ratio,
)

# ---------------------------------------------------------------------------
# reading_coverage_ratio: pure diagnostic, not a guard
# ---------------------------------------------------------------------------


def test_reading_coverage_full_passthrough_is_one():
    src = "Hamming argues that great work needs vision and courage."
    assert reading_coverage_ratio(src, src) == 1.0


def test_reading_coverage_expansion_is_above_one():
    # Pass-2 only ever expands (acronym letter-spelling, citation rendering),
    # so a faithful transcript is >= source.
    src = "The SAR system and the CPU were new in 1950."
    transcript = (
        "The S-A-R system and the C-P-U were new in 1950. "
        "Hamming, 1986, notes this."
    )
    assert reading_coverage_ratio(src, transcript) > 1.0


def test_reading_coverage_dropped_paragraph_is_below_one():
    # A genuine ~30% drop registers as <1.0 -- diagnostic, not fatal.
    src = (
        "They arise so you will not be left behind, as so many good "
        "engineers are in the long run. In the position I found myself in "
        "at the Laboratories, I had a choice. The past was once the future."
    )
    dropped = (
        "In the position I found myself in at the Laboratories, I had a "
        "choice. The past was once the future."
    )
    assert reading_coverage_ratio(src, dropped) < 1.0


def test_reading_coverage_empty_source_is_one():
    assert reading_coverage_ratio("", "anything") == 1.0


# ---------------------------------------------------------------------------
# Per-chunk completeness retry + fallback -- Pass-1 (humanize_latex)
# ---------------------------------------------------------------------------


def test_humanize_chunk_returns_first_acceptable_output():
    # First attempt is above the floor -- no retry, no fallback.
    chunk = "The variable alpha equals five, and beta equals six."
    long_output = chunk + " Confirmed by independent measurement."

    mock_result = MagicMock()
    mock_result.output = long_output

    with patch("swanki.audio._common.text_agent") as mock_agent:
        mock_agent.run_sync.return_value = mock_result
        result = _humanize_chunk_with_completeness(chunk, "openai:test")
        assert result == long_output
        assert mock_agent.run_sync.call_count == 1


def test_humanize_chunk_retries_then_falls_back_to_input():
    # Every attempt returns a stub well below the floor -- expect 3 attempts
    # then a fallback to the raw input verbatim (so Pass-2 sees the source).
    chunk = (
        "The Hamming code corrects single-bit errors by adding parity bits. "
        "Each parity bit covers a specific subset of data bits. The receiver "
        "recomputes parity to localize any flipped bit."
    )

    mock_result = MagicMock()
    mock_result.output = "Sorry, I cannot help."

    with patch("swanki.audio._common.text_agent") as mock_agent:
        mock_agent.run_sync.return_value = mock_result
        result = _humanize_chunk_with_completeness(chunk, "openai:test")
        assert result == chunk
        assert mock_agent.run_sync.call_count == 3


def test_humanize_chunk_picks_best_when_a_retry_succeeds():
    # First attempt below the floor, second above -- should return the
    # second's output and stop retrying.
    chunk = "Alpha plus beta equals gamma. Delta equals one half."
    short_output = "Short."
    full_output = chunk + " Confirmed."

    mock_result_short = MagicMock()
    mock_result_short.output = short_output
    mock_result_full = MagicMock()
    mock_result_full.output = full_output

    with patch("swanki.audio._common.text_agent") as mock_agent:
        mock_agent.run_sync.side_effect = [mock_result_short, mock_result_full]
        result = _humanize_chunk_with_completeness(chunk, "openai:test")
        assert result == full_output
        assert mock_agent.run_sync.call_count == 2


def test_humanize_chunk_min_ratio_constant_is_sane():
    # The Hamming Ch1 disaster collapsed to ratio ~0.0075; the floor must be
    # well above that but well below normal math compression (~0.6).
    assert 0.1 <= _HUMANIZE_CHUNK_MIN_RATIO <= 0.7


# ---------------------------------------------------------------------------
# Per-chunk completeness retry + fallback -- Pass-2 (transcript)
# ---------------------------------------------------------------------------


def test_pass2_chunk_returns_first_acceptable_output():
    chunk = "The model achieves ninety percent accuracy on the benchmark."
    long_output = chunk + " The result is statistically significant."

    mock_result = MagicMock()
    mock_result.output = long_output

    with patch("swanki.audio.reading.text_agent") as mock_agent:
        mock_agent.run_sync.return_value = mock_result
        transcript, fell_back = _pass2_chunk_with_completeness(
            chunk, "system", "openai:test"
        )
        assert transcript == long_output
        assert fell_back is False
        assert mock_agent.run_sync.call_count == 1


def test_pass2_chunk_falls_back_after_retries_exhaust():
    chunk = (
        "Listeners hear sections separated by real silence and bookended "
        "with the citation key. Image URLs are stripped before the audio "
        "is rendered. The acronym map enforces single-expansion per term."
    )

    mock_result = MagicMock()
    mock_result.output = "Skipped."

    with patch("swanki.audio.reading.text_agent") as mock_agent:
        mock_agent.run_sync.return_value = mock_result
        transcript, fell_back = _pass2_chunk_with_completeness(
            chunk, "system", "openai:test"
        )
        assert transcript == chunk
        assert fell_back is True
        assert mock_agent.run_sync.call_count == 3


def test_pass2_chunk_min_ratio_constant_is_sane():
    # Pass-2 only expands, so the floor must be close to 1.0 -- 0.85 is the
    # design choice that tolerates image-URL stripping + "et al" drops.
    assert 0.7 <= _PASS2_CHUNK_MIN_RATIO <= 0.95


# ---------------------------------------------------------------------------
# End-to-end mocked reading audio
# ---------------------------------------------------------------------------


def test_generate_reading_audio_mocked(tmp_audio_dir, mock_elevenlabs_api_key):
    output = tmp_audio_dir / "reading.mp3"

    # Mock returns a transcript long enough to pass the per-chunk floor on
    # the first attempt -- exercises the happy path without retries.
    long_transcript = (
        "Introduction. This paper presents a method. "
        "The method works as follows in detail across many sentences. "
        "Each step is justified, every assumption is stated explicitly."
    )
    mock_result = MagicMock()
    mock_result.output = long_transcript

    with (
        patch("swanki.audio.reading.text_agent") as mock_agent,
        patch("swanki.audio._common.text_agent") as mock_common_agent,
        patch("swanki.audio.reading.text_to_speech") as mock_tts,
        patch("swanki.audio.reading.combine_audio_with_section_pauses") as mock_combine,
    ):
        mock_agent.run_sync.return_value = mock_result
        mock_common_agent.run_sync.return_value = mock_result

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
    mock_result.output = "The variable alpha equals five."

    with patch("swanki.audio._common.text_agent") as mock_agent:
        mock_agent.run_sync.return_value = mock_result

        result = humanize_latex(
            "The variable $\\alpha$ equals 5.", "openai:test"
        )

        assert isinstance(result, str)
        assert len(result) > 0
        mock_agent.run_sync.assert_called()
