# swanki/__main__.py
import hydra
from hydra import compose, initialize_config_dir
from omegaconf import DictConfig, OmegaConf
from pathlib import Path
import sys
import argparse
from swanki.config.generator import ConfigGenerator
from swanki.pipeline import Pipeline


def legacy_main():
    """Legacy entry point for backward compatibility"""
    from swanki.legacy.__main__legacy import main as legacy_cli_main
    legacy_cli_main()


def process_with_config(cfg: DictConfig) -> None:
    """Process PDF with the given configuration"""
    # Convert to regular dict for easier use
    config = OmegaConf.to_container(cfg, resolve=True)
    
    # Initialize pipeline with config
    pipeline = Pipeline(config)
    
    # Process based on command line args
    if hasattr(cfg, 'pdf_path') and cfg.pdf_path:
        outputs = pipeline.process_full(
            pdf_path=Path(cfg.pdf_path),
            citation_key=cfg.citation_key if hasattr(cfg, 'citation_key') else None
        )
        print(f"Generated outputs: {outputs}")
    else:
        print("No PDF provided. Use: swanki pdf_path=path/to/file.pdf citation_key=@author2023")


@hydra.main(version_base=None, config_path=str(ConfigGenerator.ensure_configs()), config_name="config")
def cli_main(cfg: DictConfig) -> None:
    """CLI entry point with Hydra"""
    # Check if using legacy command format
    if len(sys.argv) > 1 and (
        '-f' in sys.argv or '--file' in sys.argv or
        '-n' in sys.argv or '--num-cards' in sys.argv
    ):
        print("Detected legacy command format. Using legacy mode...")
        legacy_main()
        return
    
    process_with_config(cfg)


def main():
    """Main entry point"""
    # Check for help or legacy mode first
    if '--help' in sys.argv or '-h' in sys.argv:
        print("""Swanki - Modern PDF-to-Anki card generation with AI

Usage:
  swanki pdf_path=path/to/file.pdf citation_key=author2023
  
Configuration Options:
  pipeline=<default|comprehensive|fast>  Choose pipeline preset
  audio=<default|minimal|full>          Choose audio generation settings
  prompts=<default|technical>           Choose prompt style
  models=<default|openai_tts>           Choose model configuration
  
Examples:
  # Basic usage with defaults
  swanki pdf_path=paper.pdf citation_key=smith2023
  
  # Comprehensive pipeline with full audio
  swanki pdf_path=paper.pdf citation_key=smith2023 pipeline=comprehensive audio=full
  
  # Override specific settings
  swanki pdf_path=paper.pdf citation_key=smith2023 processing.num_cards_per_page=5
  
  # Use legacy mode (backward compatibility)
  swanki --legacy -f paper.pdf --citation-key @smith2023 --num-cards 3
  
Configuration files are stored in: .swanki_config/ (in current directory)
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
