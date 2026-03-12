"""
tests/test_pipeline_mode.py
[[tests.test_pipeline_mode]]
https://github.com/Mjvolk3/Swanki/tree/main/tests/test_pipeline_mode.py
Test file: N/A

Tests for the audio_only mode branching in Pipeline.process_full().
"""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from swanki.pipeline import Pipeline


@pytest.fixture()
def base_config():
    """Minimal config for Pipeline construction."""
    return {
        "mode": "full",
        "pipeline": {"processing": {"confirm_before_generation": False}},
        "audio": {"audio": {}},
        "output": {"output": {"formats": {}, "create_anki_deck": False}},
        "anki": {"anki": {"enabled": False, "auto_send": False}},
        "models": {"models": {"llm": {"model": "gpt-5"}, "tts": {}}},
        "prompts": {"prompts": {"audio": {}}},
        "refinement": {"refinement": {"enabled": False}},
    }


@pytest.fixture()
def mock_pipeline(base_config):
    """Pipeline with all heavy methods mocked out."""
    p = Pipeline(base_config)
    p.split_pdf = MagicMock(return_value=[Path("/tmp/p1.pdf")])
    p.convert_to_markdown = MagicMock(return_value=[Path("/tmp/p1.md")])
    p.clean_markdown = MagicMock(return_value=[Path("/tmp/p1_clean.md")])
    p.process_images = MagicMock(return_value=[])
    p.generate_document_summary = MagicMock()
    p.estimate_card_count = MagicMock(return_value=10)
    p._generate_cards_for_segment = MagicMock(return_value=[])
    p._generate_image_cards_for_page = MagicMock(return_value=[])
    p.generate_outputs = MagicMock(return_value={})
    p.generate_audio = MagicMock()
    p.send_to_anki = MagicMock()
    p.data_dir = Path("/tmp/swanki-test")
    return p


class TestAudioOnlyMode:
    """Tests for mode=audio_only skipping card generation."""

    def test_audio_only_skips_card_generation(
        self, mock_pipeline, base_config, tmp_path
    ):
        """In audio_only mode, card generation and output generation are skipped."""
        base_config["mode"] = "audio_only"
        mock_pipeline.config = base_config
        mock_pipeline.data_dir = tmp_path

        mock_pipeline.process_full(Path("/tmp/test.pdf"), "test2023")

        mock_pipeline.estimate_card_count.assert_not_called()
        mock_pipeline._generate_cards_for_segment.assert_not_called()
        mock_pipeline.generate_outputs.assert_not_called()

    def test_audio_only_still_runs_shared_stages(
        self, mock_pipeline, base_config, tmp_path
    ):
        """Shared stages (split, convert, clean, images, summary) still run."""
        base_config["mode"] = "audio_only"
        mock_pipeline.config = base_config
        mock_pipeline.data_dir = tmp_path

        mock_pipeline.process_full(Path("/tmp/test.pdf"), "test2023")

        mock_pipeline.split_pdf.assert_called_once()
        mock_pipeline.convert_to_markdown.assert_called_once()
        mock_pipeline.clean_markdown.assert_called_once()
        mock_pipeline.process_images.assert_called_once()
        mock_pipeline.generate_document_summary.assert_called_once()

    def test_audio_only_with_lecture_calls_generate_audio(
        self, mock_pipeline, base_config, tmp_path
    ):
        """Audio generation runs when audio types are enabled in audio_only mode."""
        base_config["mode"] = "audio_only"
        base_config["audio"]["audio"]["generate_lecture"] = True
        mock_pipeline.config = base_config
        mock_pipeline.data_dir = tmp_path

        mock_pipeline.process_full(Path("/tmp/test.pdf"), "test2023")

        mock_pipeline.generate_audio.assert_called_once()

    def test_full_mode_runs_card_generation(self, mock_pipeline, base_config, tmp_path):
        """In full mode, card generation proceeds normally."""
        base_config["mode"] = "full"
        mock_pipeline.config = base_config
        mock_pipeline.data_dir = tmp_path

        mock_pipeline.process_full(Path("/tmp/test.pdf"), "test2023")

        mock_pipeline.estimate_card_count.assert_called_once()
        mock_pipeline.generate_outputs.assert_called_once()

    def test_default_mode_is_full(self, mock_pipeline, base_config, tmp_path):
        """When mode is not specified, defaults to full."""
        del base_config["mode"]
        mock_pipeline.config = base_config
        mock_pipeline.data_dir = tmp_path

        mock_pipeline.process_full(Path("/tmp/test.pdf"), "test2023")

        mock_pipeline.estimate_card_count.assert_called_once()
        mock_pipeline.generate_outputs.assert_called_once()


class TestComplementaryAudioGuard:
    """Tests for the cards guard in generate_audio()."""

    def test_complementary_skipped_with_empty_cards(self, base_config, tmp_path):
        """Complementary audio is skipped when cards list is empty."""
        base_config["audio"]["audio"]["generate_complementary"] = True
        p = Pipeline(base_config)
        p.output_base = tmp_path
        p.audio_prefix = "test"
        p.citation_key = "test2023"

        summary = MagicMock()
        summary.summary = "Test summary"
        summary.key_contributions = []

        with patch.dict("os.environ", {"ELEVEN_LABS_API_KEY": "k"}):
            p.generate_audio(
                cards=[],
                summary=summary,
                outputs={},
                cleaned_files=[],
                image_summaries=[],
            )

        # No cards-with-audio file should exist
        assert "cards_audio" not in {}
