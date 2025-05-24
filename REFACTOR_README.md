# Swanki Refactor - Modern PDF-to-Anki Card Generation

## Overview

This refactor introduces a modern, configuration-driven approach to generating Anki cards from PDFs using AI. The new system leverages:

- **Hydra Configuration**: Flexible, user-customizable pipeline with auto-generated defaults
- **Structured Output**: Migration to `instructor` library with Pydantic models for reliable structured outputs
- **Context-Aware Processing**: Summary-first approach for better card and audio quality
- **User Control**: Multiple configurable outputs via Hydra

## Quick Start

### Basic Usage

```bash
# Install dependencies
pip install -r env/requirements.txt

# Basic usage with all defaults
swanki --pdf_path=Luo_2020.pdf --citation_key=@luo2020
```

### Configuration Options

```bash
# Use comprehensive pipeline with full audio
swanki --pdf_path=Luo_2020.pdf --citation_key=@luo2020 \
       pipeline=comprehensive \
       audio=full

# Override specific settings
swanki --pdf_path=Luo_2020.pdf --citation_key=@luo2020 \
       processing.num_cards_per_page=5 \
       audio.generate_reading=true

# Use technical prompts
swanki --pdf_path=Luo_2020.pdf --citation_key=@luo2020 \
       prompts=technical
```

### Legacy Mode

For backward compatibility with existing scripts:

```bash
# Use legacy command format
swanki --legacy -f paper.pdf --citation-key @smith2023 --num-cards 3
```

## Configuration System

Default configurations are automatically generated in `~/.swanki_config/`:

- `config.yaml` - Main configuration
- `pipeline/` - Processing presets (default, comprehensive, fast)
- `prompts/` - Prompt templates (default, technical)
- `models/` - Model configurations (default, openai_tts)
- `audio/` - Audio generation settings (default, minimal, full)
- `output/` - Output format settings

## Environment Variables

Create a `.env` file based on `.env.example`:

```bash
# Directory for output files
SWANKI_DATA=/Users/username/Documents/Swanki_Data

# API Keys
OPENAI_API_KEY=your-key
MATHPIX_APP_ID=your-id
MATHPIX_APP_KEY=your-key
ELEVENLABS_API_KEY=your-key
```

## Key Improvements

1. **Structured Output**: Pydantic models ensure reliable card generation
2. **Document Summary**: Generated early and used as context throughout
3. **Flexible Configuration**: Easy to customize via Hydra configs
4. **Multiple Outputs**: Generate plain cards, audio-enriched cards, and summaries
5. **Better Audio**: Context-aware TTS with acronym expansion and pronunciation guides

## Pipeline Flow

1. **PDF Processing**: Split → Convert to Markdown → Clean
2. **Image Analysis**: Extract and summarize all images
3. **Document Summary**: Generate comprehensive summary with acronyms/terms
4. **Card Generation**: Use sliding window with summary context
5. **Audio Generation**: Multiple types (complementary, summary, reading)
6. **Output Generation**: Multiple formats for user choice

## Output Structure

```
$SWANKI_DATA/swanki-out/
├── cards-plain.md          # Plain flashcards
├── cards-with-audio.md     # Cards with audio links
├── cards-combined.md       # All cards combined
├── document-summary.md     # Document summary
└── audio/                  # Generated audio files
```

## Development

The codebase is organized as:

```
swanki/
├── config/          # Configuration generator
├── models/          # Pydantic models
├── pipeline/        # Main pipeline logic
├── utils/           # Utility functions
└── legacy/          # Backward compatibility
```

## Migration from Legacy

The refactor maintains full backward compatibility. Existing scripts will continue to work, but we recommend migrating to the new Hydra-based configuration system for better flexibility and reliability.