"""
tests/test_config_helpers.py
[[tests.test_config_helpers]]
https://github.com/Mjvolk3/Swanki/tree/main/tests/test_config_helpers.py

Tests for swanki/config/helpers.py
"""

from pathlib import Path

from swanki.config.helpers import (
    init_user_config,
    package_defaults_path,
    show_config_info,
    user_config_dir,
)


def test_package_defaults_path_exists():
    path = package_defaults_path()
    assert path.exists()
    assert path.is_dir()
    assert (path / "config.yaml").exists()


def test_package_defaults_has_all_groups():
    path = package_defaults_path()
    for group in [
        "pipeline",
        "prompts",
        "models",
        "audio",
        "output",
        "anki",
        "refinement",
    ]:
        assert (path / group).is_dir(), f"Missing config group: {group}"


def test_audio_presets_renamed():
    audio = package_defaults_path() / "audio"
    expected = {
        "none.yaml",
        "all.yaml",
        "complementary_summary.yaml",
        "complementary_summary_lecture.yaml",
        "lecture.yaml",
        "summary_lecture.yaml",
    }
    actual = {f.name for f in audio.glob("*.yaml")}
    assert actual == expected


def test_no_old_audio_names():
    audio = package_defaults_path() / "audio"
    for old_name in [
        "default.yaml",
        "essential.yaml",
        "all_but_reading.yaml",
        "full.yaml",
        "lecture_only.yaml",
    ]:
        assert not (audio / old_name).exists(), f"Old preset still exists: {old_name}"


def test_user_config_dir():
    path = user_config_dir()
    assert path == Path.home() / ".swanki"


def test_init_user_config(tmp_path, monkeypatch):
    monkeypatch.setattr(
        "swanki.config.helpers.user_config_dir", lambda: tmp_path / ".swanki"
    )
    dest = init_user_config()
    assert dest.exists()
    assert (dest / "config.yaml").exists()
    assert (dest / "pipeline" / "default.yaml").exists()


def test_init_user_config_no_overwrite(tmp_path, monkeypatch):
    fake_dir = tmp_path / ".swanki"
    monkeypatch.setattr("swanki.config.helpers.user_config_dir", lambda: fake_dir)
    init_user_config()
    sentinel = fake_dir / "config.yaml"
    sentinel.write_text("custom")
    init_user_config()
    assert sentinel.read_text() == "custom"


def test_show_config_info():
    info = show_config_info()
    assert "Package defaults:" in info
    assert "Global config:" in info
    assert "Local config:" in info


def test_config_yaml_defaults_audio_none():
    import yaml

    config = package_defaults_path() / "config.yaml"
    with open(config) as f:
        data = yaml.safe_load(f)
    defaults = data["defaults"]
    audio_entry = next(d for d in defaults if isinstance(d, dict) and "audio" in d)
    assert audio_entry["audio"] == "none"


def test_config_yaml_has_mode_full():
    import yaml

    config = package_defaults_path() / "config.yaml"
    with open(config) as f:
        data = yaml.safe_load(f)
    assert data["mode"] == "full"
