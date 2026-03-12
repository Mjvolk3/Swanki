"""
swanki/__main__.py
[[swanki.__main__]]
https://github.com/Mjvolk3/Swanki/tree/main/swanki/__main__.py
Test file: tests/swanki/test___main__.py

Command-line interface for Swanki.
"""

import sys
from pathlib import Path

import hydra
from omegaconf import DictConfig, OmegaConf

from swanki.config.helpers import (
    init_user_config,
    package_defaults_path,
    show_config_info,
)
from swanki.pipeline import Pipeline


def process_with_config(cfg: DictConfig) -> None:
    """Process PDF with the given Hydra configuration.

    Args:
        cfg: Hydra configuration object with processing options.
    """
    config = OmegaConf.to_container(cfg, resolve=True)

    pipeline = Pipeline(config)  # type: ignore[arg-type]

    if hasattr(cfg, "pdf_path") and cfg.pdf_path:
        citation_key: str = (
            str(cfg.citation_key)
            if hasattr(cfg, "citation_key") and cfg.citation_key
            else ""
        )
        output_dir: str | None = (
            str(cfg.output_dir)
            if hasattr(cfg, "output_dir") and cfg.output_dir
            else None
        )
        outputs = pipeline.process_full(
            pdf_path=Path(cfg.pdf_path),
            citation_key=citation_key,
            output_dir=output_dir,
        )
        if outputs.get("anki_file"):
            print(f"✓ Cards generated: {outputs['anki_file']}")
        audio_files = outputs.get("audio_files")
        if audio_files:
            print(f"✓ Audio files: {audio_files}")
    else:
        print(
            "No PDF provided. Use: swanki pdf_path=path/to/file.pdf citation_key=@author2023"
        )


@hydra.main(
    version_base=None,
    config_path=None,
    config_name="config",
)
def cli_main(cfg: DictConfig) -> None:
    """Main CLI entry point with Hydra configuration.

    Args:
        cfg: Hydra configuration merged from config files and CLI.
    """
    process_with_config(cfg)


def send_to_anki_command() -> None:
    """Send existing markdown cards to Anki via the modern send_to_anki module."""
    from swanki.send_to_anki import main as send_to_anki_main

    send_to_anki_main()


def main() -> None:
    """Primary entry point for the Swanki CLI.

    Routes between different command modes:
    - ``--show-defaults``: print package defaults path
    - ``--init-config``: copy defaults to ``~/.swanki/``
    - ``--config-info``: show all config locations
    - ``--send-to-anki``: send cards to Anki
    - default: Hydra-based processing
    """
    if "--send-to-anki" in sys.argv:
        sys.argv.remove("--send-to-anki")
        send_to_anki_command()
        return

    if "--show-defaults" in sys.argv:
        print(package_defaults_path())
        sys.exit(0)

    if "--init-config" in sys.argv:
        dest = init_user_config()
        print(f"Configs copied to {dest}")
        sys.exit(0)

    if "--config-info" in sys.argv:
        print(show_config_info())
        sys.exit(0)

    if "--help" in sys.argv or "-h" in sys.argv:
        print("""Swanki - Modern PDF-to-Anki card generation with AI

Usage:
  swanki pdf_path=path/to/file.pdf citation_key=author2023 [+output_dir=custom_name]

Configuration:
  Package defaults live in swanki/conf/ (shipped with pip install).
  Override with files in ~/.swanki/ (global) or .swanki/ (project-local).
  CLI overrides (key=value) win over all config files.

  swanki --show-defaults    Print package defaults path
  swanki --init-config      Copy defaults to ~/.swanki/ for editing
  swanki --config-info      Show all active config locations

Configuration Options:
  mode=<full|audio_only>                                                   Pipeline mode
  pipeline=<default|standard|larger|smaller>                               Pipeline preset
  audio=<none|all|complementary_summary|complementary_summary_lecture|lecture|summary_lecture>
  prompts=<default|technical>                                              Prompt style
  models=<default|openai_tts>                                              Model config
  anki=<default|auto_send|custom_deck>                                     Anki integration
  refinement=<default|strict|minimal|disabled>                             Refinement strategy

Examples:
  swanki pdf_path=paper.pdf citation_key=smith2023
  swanki pdf_path=paper.pdf citation_key=smith2023 pipeline=larger audio=all
  swanki pdf_path=paper.pdf citation_key=smith2023 +output_dir=smith2023_CH5
  swanki pdf_path=paper.pdf citation_key=smith2023 mode=audio_only audio=lecture
  swanki pdf_path=paper.pdf citation_key=smith2023 anki=auto_send
  swanki --send-to-anki path/to/cards.md --send --host 127.0.0.1 --port 8765
""")
        sys.exit(0)

    cli_main()


if __name__ == "__main__":
    main()
