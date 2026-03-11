"""
swanki/__main__.py
[[swanki.__main__]]
https://github.com/Mjvolk3/Swanki/tree/main/swanki/__main__.py
Test file: tests/swanki/test___main__.py

Command-line interface for Swanki.
"""

import os
import sys
from pathlib import Path

import hydra
from omegaconf import DictConfig, OmegaConf

from swanki.config.generator import ConfigGenerator
from swanki.pipeline import Pipeline


def legacy_main() -> None:
    """Run legacy CLI for backward compatibility.

    Delegates to the original legacy CLI implementation to support
    older command formats and scripts that depend on them.

    Notes:
    -----
    This function is called when legacy flags like -f, --file,
    -n, or --num-cards are detected.

    See Also:
    --------
    swanki.legacy.__main__legacy : Legacy CLI implementation
    """
    from swanki.legacy.__main__legacy import main as legacy_cli_main

    legacy_cli_main()  # type: ignore[no-untyped-call]


def process_with_config(cfg: DictConfig) -> None:
    """Process PDF with the given Hydra configuration.

    Initializes the pipeline with configuration and processes
    the specified PDF file to generate Anki cards.

    Parameters
    ----------
    cfg : DictConfig
        Hydra configuration object with processing options

    Notes:
    -----
    Expects cfg.pdf_path and optionally cfg.citation_key
    to be set from command line arguments.
    """
    # Convert to regular dict for easier use
    config = OmegaConf.to_container(cfg, resolve=True)

    # Initialize pipeline with config
    pipeline = Pipeline(config)  # type: ignore[arg-type]

    # Process based on command line args
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
        # Only print essential output info
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
    config_path=str(
        ConfigGenerator.ensure_configs(
            interactive=os.getenv("SWANKI_NONINTERACTIVE") != "1"
        )
    ),
    config_name="config",
)
def cli_main(cfg: DictConfig) -> None:
    """Main CLI entry point with Hydra configuration.

    Handles both modern Hydra-based commands and detection of
    legacy command formats, delegating appropriately.

    Parameters
    ----------
    cfg : DictConfig
        Hydra configuration merged from config files and CLI

    Notes:
    -----
    Decorated with @hydra.main to enable Hydra's configuration
    composition and command-line override features.
    """
    # Check if using legacy command format
    if len(sys.argv) > 1 and (
        "-f" in sys.argv
        or "--file" in sys.argv
        or "-n" in sys.argv
        or "--num-cards" in sys.argv
    ):
        print("Detected legacy command format. Using legacy mode...")
        legacy_main()
        return

    process_with_config(cfg)


def send_to_anki_command() -> None:
    """Send existing markdown cards to Anki.

    Delegates to the legacy md_to_anki command which handles
    parsing markdown files and sending cards via AnkiConnect.

    Notes:
    -----
    Triggered by --send-to-anki flag. Expects additional
    arguments like file path, --send, --host, and --port.

    See Also:
    --------
    swanki.legacy.md_to_anki : Anki sending implementation
    """
    from swanki.legacy.md_to_anki import main as md_to_anki_main

    # Simply delegate to the legacy md_to_anki command
    md_to_anki_main()


def main() -> None:
    """Primary entry point for the Swanki CLI.

    Handles routing between different command modes:
    - Help display (--help, -h)
    - Anki sending (--send-to-anki)
    - Legacy mode (--legacy or legacy flags)
    - Modern Hydra mode (default)

    The function checks for special flags first, then delegates
    to the appropriate handler based on the command format.

    Examples:
    --------
    >>> # Modern usage
    >>> sys.argv = ['swanki', 'pdf_path=paper.pdf', 'citation_key=smith2023']
    >>> main()

    >>> # Legacy usage
    >>> sys.argv = ['swanki', '--legacy', '-f', 'paper.pdf']
    >>> main()

    >>> # Send to Anki
    >>> sys.argv = ['swanki', '--send-to-anki', 'cards.md', '--send']
    >>> main()

    Notes:
    -----
    This is the function called when running 'swanki' from
    the command line, as configured in pyproject.toml.
    """
    # Check for special commands first
    if "--send-to-anki" in sys.argv:
        # Remove our flag and let md_to_anki handle the rest
        sys.argv.remove("--send-to-anki")
        send_to_anki_command()
        return

    # Check for help or legacy mode first
    if "--help" in sys.argv or "-h" in sys.argv:
        print("""Swanki - Modern PDF-to-Anki card generation with AI

Usage:
  swanki pdf_path=path/to/file.pdf citation_key=author2023 [+output_dir=custom_name]
  
Configuration Options:
  mode=<full|audio_only>                Pipeline mode (audio_only skips card generation)
  pipeline=<default|comprehensive|fast>  Choose pipeline preset
  audio=<default|minimal|full|lecture_only>  Choose audio generation settings
  prompts=<default|technical>           Choose prompt style
  models=<default|openai_tts>           Choose model configuration
  anki=<default|auto_send|custom_deck>  Choose Anki integration settings
  
Examples:
  # Basic usage with defaults
  swanki pdf_path=paper.pdf citation_key=smith2023
  
  # Comprehensive pipeline with full audio
  swanki pdf_path=paper.pdf citation_key=smith2023 pipeline=comprehensive audio=full
  
  # Use custom output directory (e.g., for book chapters)
  swanki pdf_path=chapter5.pdf citation_key=smith2023 +output_dir=smith2023_CH5
  
  # Process specific section with full audio and auto-send to Anki
  swanki pdf_path=/path/to/Luo_2020.pdf citation_key=luoWhenCausalInference2020 +output_dir=luoWhenCausalInference2020_12 audio=full anki=auto_send
  
  # Generate only lecture audio (no cards)
  swanki pdf_path=paper.pdf citation_key=smith2023 mode=audio_only audio=lecture_only

  # Auto-send to Anki with custom deck
  swanki pdf_path=paper.pdf citation_key=smith2023 anki=auto_send anki.deck_name="Research::Papers::{citation_key}"
  
  # Send existing cards to Anki manually
  swanki --send-to-anki path/to/cards.md --send --host 127.0.0.1 --port 8765
  
  # Override specific settings
  swanki pdf_path=paper.pdf citation_key=smith2023 processing.num_cards_per_page=5
  
  # Force regenerate citation audio (if it seems corrupted)
  swanki pdf_path=paper.pdf citation_key=smith2023 audio.force_regenerate_citation=true
  
  # Use legacy mode (backward compatibility)
  swanki --legacy -f paper.pdf --citation-key @smith2023 --num-cards 3
  
Configuration:
  Files are stored in: .swanki_config/ (in current directory)
  
  First-time setup:
  - You'll be prompted once to create default configs
  - To skip prompts: export SWANKI_NONINTERACTIVE=1
  - Or for a single run: SWANKI_NONINTERACTIVE=1 swanki pdf_path=...

Template Variables:
  {citation_key} - Replaced with the citation key provided
  
Example Deck Names:
  "{citation_key}" -> "smith2023"
  "Research::Papers::{citation_key}" -> "Research::Papers::smith2023"
  "default::{citation_key}" -> "default::smith2023"
""")
        sys.exit(0)

    if "--legacy" in sys.argv:
        # Remove --legacy and run legacy mode
        sys.argv.remove("--legacy")
        legacy_main()
    else:
        # Let Hydra handle everything
        cli_main()


if __name__ == "__main__":
    main()
