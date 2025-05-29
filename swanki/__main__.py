"""Command-line interface for Swanki.

This module provides the main entry point for the Swanki CLI, supporting
both modern Hydra-based configuration and legacy command formats for
backward compatibility.

The CLI supports various commands:
- PDF processing with AI card generation
- Sending cards to Anki
- Configuration customization
- Legacy mode for older scripts

Functions
---------
legacy_main()
    Run legacy CLI for backward compatibility
process_with_config(cfg)
    Process PDF with Hydra configuration
cli_main(cfg)
    Main Hydra CLI entry point
send_to_anki_command()
    Send existing cards to Anki
main()
    Primary entry point handling all modes

Examples
--------
Basic usage:
$ swanki pdf_path=paper.pdf citation_key=smith2023

With custom configuration:
$ swanki pdf_path=paper.pdf citation_key=smith2023 pipeline=comprehensive audio=full

Send to Anki:
$ swanki --send-to-anki cards.md --send

Legacy mode:
$ swanki --legacy -f paper.pdf --citation-key @smith2023
"""

import hydra
from hydra import compose, initialize_config_dir
from omegaconf import DictConfig, OmegaConf
from pathlib import Path
import sys
import argparse
from swanki.config.generator import ConfigGenerator
from swanki.pipeline import Pipeline


def legacy_main():
    """Run legacy CLI for backward compatibility.
    
    Delegates to the original legacy CLI implementation to support
    older command formats and scripts that depend on them.
    
    Notes
    -----
    This function is called when legacy flags like -f, --file,
    -n, or --num-cards are detected.
    
    See Also
    --------
    swanki.legacy.__main__legacy : Legacy CLI implementation
    """
    from swanki.legacy.__main__legacy import main as legacy_cli_main
    legacy_cli_main()


def process_with_config(cfg: DictConfig) -> None:
    """Process PDF with the given Hydra configuration.
    
    Initializes the pipeline with configuration and processes
    the specified PDF file to generate Anki cards.
    
    Parameters
    ----------
    cfg : DictConfig
        Hydra configuration object with processing options
    
    Notes
    -----
    Expects cfg.pdf_path and optionally cfg.citation_key
    to be set from command line arguments.
    """
    # Convert to regular dict for easier use
    config = OmegaConf.to_container(cfg, resolve=True)
    
    # Initialize pipeline with config
    pipeline = Pipeline(config)
    
    # Process based on command line args
    if hasattr(cfg, 'pdf_path') and cfg.pdf_path:
        outputs = pipeline.process_full(
            pdf_path=Path(cfg.pdf_path),
            citation_key=cfg.citation_key if hasattr(cfg, 'citation_key') else None,
            output_dir=cfg.output_dir if hasattr(cfg, 'output_dir') else None
        )
        print(f"Generated outputs: {outputs}")
    else:
        print("No PDF provided. Use: swanki pdf_path=path/to/file.pdf citation_key=@author2023")


@hydra.main(version_base=None, config_path=str(ConfigGenerator.ensure_configs()), config_name="config")
def cli_main(cfg: DictConfig) -> None:
    """Main CLI entry point with Hydra configuration.
    
    Handles both modern Hydra-based commands and detection of
    legacy command formats, delegating appropriately.
    
    Parameters
    ----------
    cfg : DictConfig
        Hydra configuration merged from config files and CLI
    
    Notes
    -----
    Decorated with @hydra.main to enable Hydra's configuration
    composition and command-line override features.
    """
    # Check if using legacy command format
    if len(sys.argv) > 1 and (
        '-f' in sys.argv or '--file' in sys.argv or
        '-n' in sys.argv or '--num-cards' in sys.argv
    ):
        print("Detected legacy command format. Using legacy mode...")
        legacy_main()
        return
    
    process_with_config(cfg)


def send_to_anki_command():
    """Send existing markdown cards to Anki.
    
    Delegates to the legacy md_to_anki command which handles
    parsing markdown files and sending cards via AnkiConnect.
    
    Notes
    -----
    Triggered by --send-to-anki flag. Expects additional
    arguments like file path, --send, --host, and --port.
    
    See Also
    --------
    swanki.legacy.md_to_anki : Anki sending implementation
    """
    from swanki.legacy.md_to_anki import main as md_to_anki_main
    # Simply delegate to the legacy md_to_anki command
    md_to_anki_main()

def main():
    """Primary entry point for the Swanki CLI.
    
    Handles routing between different command modes:
    - Help display (--help, -h)
    - Anki sending (--send-to-anki)
    - Legacy mode (--legacy or legacy flags)
    - Modern Hydra mode (default)
    
    The function checks for special flags first, then delegates
    to the appropriate handler based on the command format.
    
    Examples
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
    
    Notes
    -----
    This is the function called when running 'swanki' from
    the command line, as configured in pyproject.toml.
    """
    # Check for special commands first
    if '--send-to-anki' in sys.argv:
        # Remove our flag and let md_to_anki handle the rest
        sys.argv.remove('--send-to-anki')
        send_to_anki_command()
        return
    
    # Check for help or legacy mode first
    if '--help' in sys.argv or '-h' in sys.argv:
        print("""Swanki - Modern PDF-to-Anki card generation with AI

Usage:
  swanki pdf_path=path/to/file.pdf citation_key=author2023 [+output_dir=custom_name]
  
Configuration Options:
  pipeline=<default|comprehensive|fast>  Choose pipeline preset
  audio=<default|minimal|full>          Choose audio generation settings
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
  
  # Auto-send to Anki with custom deck
  swanki pdf_path=paper.pdf citation_key=smith2023 anki=auto_send anki.deck_name="Research::Papers::{citation_key}"
  
  # Send existing cards to Anki manually
  swanki --send-to-anki path/to/cards.md --send --host 127.0.0.1 --port 8765
  
  # Override specific settings
  swanki pdf_path=paper.pdf citation_key=smith2023 processing.num_cards_per_page=5
  
  # Use legacy mode (backward compatibility)
  swanki --legacy -f paper.pdf --citation-key @smith2023 --num-cards 3
  
Configuration files are stored in: .swanki_config/ (in current directory)

Template Variables:
  {citation_key} - Replaced with the citation key provided
  
Example Deck Names:
  "{citation_key}" -> "smith2023"
  "Research::Papers::{citation_key}" -> "Research::Papers::smith2023"
  "default::{citation_key}" -> "default::smith2023"
""")
        sys.exit(0)
    
    if '--legacy' in sys.argv:
        # Remove --legacy and run legacy mode
        sys.argv.remove('--legacy')
        legacy_main()
    else:
        # Let Hydra handle everything
        cli_main()


if __name__ == "__main__":
    main()
