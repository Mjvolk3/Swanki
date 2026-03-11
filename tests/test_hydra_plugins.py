"""
tests/test_hydra_plugins.py
[[tests.test_hydra_plugins]]
https://github.com/Mjvolk3/Swanki/tree/main/tests/test_hydra_plugins.py

Tests for swanki/config/hydra_plugins.py (SwankiSearchPathPlugin).
"""

from pathlib import Path
from unittest.mock import MagicMock

from swanki.config.hydra_plugins import SwankiSearchPathPlugin


def test_plugin_adds_package_defaults():
    plugin = SwankiSearchPathPlugin()
    search_path = MagicMock()
    plugin.manipulate_search_path(search_path)
    calls = search_path.append.call_args_list
    providers = [c.kwargs["provider"] for c in calls]
    assert "swanki-defaults" in providers


def test_plugin_adds_global_if_exists(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    (tmp_path / ".swanki").mkdir()
    plugin = SwankiSearchPathPlugin()
    search_path = MagicMock()
    plugin.manipulate_search_path(search_path)
    providers = [c.kwargs["provider"] for c in search_path.append.call_args_list]
    assert "swanki-global" in providers


def test_plugin_skips_global_if_missing(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    plugin = SwankiSearchPathPlugin()
    search_path = MagicMock()
    plugin.manipulate_search_path(search_path)
    providers = [c.kwargs["provider"] for c in search_path.append.call_args_list]
    assert "swanki-global" not in providers


def test_plugin_adds_local_if_exists(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "cwd", lambda: tmp_path)
    (tmp_path / ".swanki").mkdir()
    plugin = SwankiSearchPathPlugin()
    search_path = MagicMock()
    plugin.manipulate_search_path(search_path)
    providers = [c.kwargs["provider"] for c in search_path.append.call_args_list]
    assert "swanki-local" in providers


def test_plugin_skips_local_if_missing(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "cwd", lambda: tmp_path)
    plugin = SwankiSearchPathPlugin()
    search_path = MagicMock()
    plugin.manipulate_search_path(search_path)
    providers = [c.kwargs["provider"] for c in search_path.append.call_args_list]
    assert "swanki-local" not in providers


def test_plugin_priority_order(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    monkeypatch.setattr(Path, "cwd", lambda: tmp_path)
    (tmp_path / ".swanki").mkdir()
    plugin = SwankiSearchPathPlugin()
    search_path = MagicMock()
    plugin.manipulate_search_path(search_path)
    providers = [c.kwargs["provider"] for c in search_path.append.call_args_list]
    assert providers == ["swanki-defaults", "swanki-global", "swanki-local"]
