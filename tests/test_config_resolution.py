"""Smoke tests for Hydra config resolution.

Verifies that default and anthropic model presets compose correctly
and that the config values the pipeline depends on actually resolve.
"""

from pathlib import Path

import yaml

CONF_DIR = Path(__file__).parent.parent / "swanki" / "conf"


def _load_yaml(relative: str) -> dict:
    return yaml.safe_load((CONF_DIR / relative).read_text())


def test_default_models_resolve() -> None:
    """Default model config has expected provider and model."""
    cfg = _load_yaml("models/default.yaml")
    llm = cfg["models"]["llm"]
    assert llm["provider"] == "openai"
    assert "gpt" in llm["model"]
    assert llm["temperature"] == 0.7
    assert llm["max_retries"] == 3


def test_anthropic_models_resolve() -> None:
    """Anthropic model config has expected provider and model."""
    cfg = _load_yaml("models/anthropic.yaml")
    llm = cfg["models"]["llm"]
    assert llm["provider"] == "anthropic"
    assert "claude" in llm["model"]


def test_default_tts_has_voice_id() -> None:
    """TTS config has a voice_id for ElevenLabs."""
    cfg = _load_yaml("models/default.yaml")
    tts = cfg["models"]["tts"]
    assert tts["provider"] == "elevenlabs"
    assert tts["voice_id"]


def test_root_config_has_all_defaults() -> None:
    """Root config.yaml references all expected config groups."""
    cfg = _load_yaml("config.yaml")
    defaults = cfg["defaults"]
    group_names = [list(d.keys())[0] if isinstance(d, dict) else d for d in defaults]
    for expected in [
        "pipeline",
        "prompts",
        "models",
        "audio",
        "output",
        "anki",
        "refinement",
    ]:
        assert expected in group_names, f"Missing default group: {expected}"


def test_audio_none_preset_exists() -> None:
    """Audio 'none' preset exists (used for cheap API testing)."""
    cfg = _load_yaml("audio/none.yaml")
    assert cfg is not None


def test_all_model_presets_have_models_key() -> None:
    """Every models/*.yaml has a top-level 'models' section."""
    models_dir = CONF_DIR / "models"
    for yaml_file in models_dir.glob("*.yaml"):
        cfg = yaml.safe_load(yaml_file.read_text())
        assert "models" in cfg, f"{yaml_file.name} missing 'models' key"


def test_llm_presets_have_provider_and_model() -> None:
    """Model presets with an LLM section have provider and model keys."""
    models_dir = CONF_DIR / "models"
    llm_presets = []
    for yaml_file in models_dir.glob("*.yaml"):
        cfg = yaml.safe_load(yaml_file.read_text())
        if "llm" in cfg.get("models", {}):
            llm = cfg["models"]["llm"]
            assert "provider" in llm, f"{yaml_file.name} missing provider"
            assert "model" in llm, f"{yaml_file.name} missing model"
            llm_presets.append(yaml_file.name)
    assert len(llm_presets) >= 2, "Expected at least default and anthropic LLM presets"
