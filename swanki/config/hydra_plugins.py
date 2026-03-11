"""
swanki/config/hydra_plugins.py
[[swanki.config.hydra_plugins]]
https://github.com/Mjvolk3/Swanki/tree/main/swanki/config/hydra_plugins.py
Test file: tests/test_hydra_plugins.py

Hydra SearchPathPlugin for three-tier config resolution (package → global → local).
"""

from pathlib import Path

from hydra.core.config_search_path import ConfigSearchPath
from hydra.plugins.search_path_plugin import SearchPathPlugin


class SwankiSearchPathPlugin(SearchPathPlugin):
    """Three-tier config resolution plugin for Swanki.

    Adds search paths so Hydra finds configs in priority order:

    1. Package defaults: ``swanki/conf/`` (lowest priority)
    2. Global user prefs: ``~/.swanki/`` (medium priority)
    3. Local project overrides: ``.swanki/`` in cwd (highest priority)

    CLI overrides (``key=value``) sit above all three.

    Registration is via ``pyproject.toml`` entry point::

        [project.entry-points."hydra_plugins"]
        swanki = "swanki.config.hydra_plugins"
    """

    provider = "swanki"

    def manipulate_search_path(self, search_path: ConfigSearchPath) -> None:
        """Append package, global, and local search paths.

        Args:
            search_path: Hydra's config search path to extend.
        """
        search_path.append(
            provider="swanki-defaults",
            path="pkg://swanki/conf",
        )

        global_config = Path.home() / ".swanki"
        if global_config.exists():
            search_path.append(
                provider="swanki-global",
                path=f"file://{global_config}",
            )

        local_config = Path.cwd() / ".swanki"
        if local_config.exists():
            search_path.append(
                provider="swanki-local",
                path=f"file://{local_config}",
            )
