# Quick Start Guide

## Basic Usage

The simplest way to use Swanki is to process a PDF file:

```bash
swanki pdf_path=paper.pdf citation_key=smith2023
```

This will:
1. Split the PDF into individual pages
2. Convert each page to markdown using Mathpix
3. Clean the markdown files
4. Generate flashcards using AI
5. Save the cards to `swanki-out/smith2023/`

## Common Use Cases

### Generate Cards with Audio

```bash
swanki pdf_path=paper.pdf citation_key=jones2024 audio=cards
```

### Use Comprehensive Pipeline

For more thorough processing with more cards per page:

```bash
swanki pdf_path=paper.pdf citation_key=doe2023 pipeline=comprehensive
```

### Auto-send to Anki

Process and automatically send cards to Anki:

```bash
swanki pdf_path=paper.pdf citation_key=lee2024 anki=auto_send
```

### Custom Deck Name

Send to a specific Anki deck hierarchy:

```bash
swanki pdf_path=paper.pdf citation_key=wang2023 anki=custom_deck
```

## Output Structure

After processing, you'll find:

```
swanki-out/
└── smith2023/
    ├── pdf-singles/          # Individual PDF pages
    ├── md-singles/           # Raw markdown files
    ├── clean-md-singles/     # Cleaned markdown
    ├── cards-plain.md        # Flashcards without audio
    ├── cards-with-audio.md   # Flashcards with audio links
    └── document-summary.md   # AI-generated summary
```

## Configuration Customization

Swanki uses Hydra for configuration. Override any setting:

```bash
# More cards per page
swanki pdf_path=paper.pdf citation_key=kim2024 processing.num_cards_per_page=5

# Different AI model
swanki pdf_path=paper.pdf citation_key=chen2023 models.llm.model=gpt-4

# Custom output directory
SWANKI_DATA=/my/custom/path swanki pdf_path=paper.pdf citation_key=liu2024
```