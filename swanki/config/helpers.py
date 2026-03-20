"""
swanki/config/helpers.py
[[swanki.config.helpers]]
https://github.com/Mjvolk3/Swanki/tree/main/swanki/config/helpers.py
Test file: tests/test_config_helpers.py

Config utility functions replacing the deleted ConfigGenerator.
"""

import shutil
from pathlib import Path


def package_defaults_path() -> Path:
    """Return the path to package default configs.

    Returns:
        Absolute path to ``swanki/conf/`` inside the installed package.
    """
    return Path(__file__).parent.parent / "conf"


def user_config_dir() -> Path:
    """Return the path to the global user config directory.

    Returns:
        ``~/.swanki/`` expanded to an absolute path.
    """
    return Path.home() / ".swanki"


def init_user_config() -> Path:
    """Copy package defaults to ``~/.swanki/`` for customization.

    Creates ``~/.swanki/`` if it doesn't exist and copies all
    default YAML configs from the package into it.  Existing
    files are not overwritten.

    Returns:
        Path to the user config directory.
    """
    dest = user_config_dir()
    src = package_defaults_path()

    for yaml_file in src.rglob("*.yaml"):
        rel = yaml_file.relative_to(src)
        target = dest / rel
        if not target.exists():
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(yaml_file, target)

    return dest


def show_config_info() -> str:
    """Return a human-readable summary of config locations and files.

    Returns:
        Multi-line string listing package, global, and local config paths
        and any user-created override files.
    """
    lines: list[str] = []
    pkg = package_defaults_path()
    lines.append(f"Package defaults:  {pkg}")

    global_dir = user_config_dir()
    if global_dir.exists():
        yamls = sorted(global_dir.rglob("*.yaml"))
        lines.append(f"Global config:     {global_dir}    ({len(yamls)} files)")
        for y in yamls:
            lines.append(f"  {y.relative_to(global_dir)}")
    else:
        lines.append(f"Global config:     {global_dir}    (not found)")

    local_dir = Path.cwd() / ".swanki"
    if local_dir.exists():
        yamls = sorted(local_dir.rglob("*.yaml"))
        lines.append(f"Local config:      {local_dir}    ({len(yamls)} files)")
        for y in yamls:
            lines.append(f"  {y.relative_to(local_dir)}")
    else:
        lines.append("Local config:      .swanki/    (not found)")

    return "\n".join(lines)
