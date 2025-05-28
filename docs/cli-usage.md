# CLI Usage

## Basic Command Structure

```bash
swanki [OPTIONS] [OVERRIDES]
```

## Required Arguments

- `pdf_path`: Path to the PDF file to process
- `citation_key`: Citation key for naming and organization

## Command Line Options

### Help

```bash
swanki --help
```

### Legacy Mode

For backward compatibility with older scripts:

```bash
swanki --legacy -f paper.pdf --citation-key @smith2023 --num-cards 3
```

### Send to Anki

Send existing cards to Anki without reprocessing:

```bash
swanki --send-to-anki cards.md --send --host 127.0.0.1 --port 8765
```

## Configuration Presets

### Pipeline Presets

- `default`: Balanced processing (default)
- `comprehensive`: More thorough processing, more cards
- `fast`: Quick processing, fewer cards

```bash
swanki pdf_path=paper.pdf citation_key=test pipeline=comprehensive
```

### Audio Presets

- `default`: No audio generation
- `cards`: Only card audio
- `summary`: Only summary audio
- `reading`: Only full reading audio
- `full`: All audio types

```bash
swanki pdf_path=paper.pdf citation_key=test audio=full
```

### Anki Presets

- `default`: Anki disabled
- `auto_send`: Enable and auto-send
- `custom_deck`: Custom deck hierarchy

```bash
swanki pdf_path=paper.pdf citation_key=test anki=auto_send
```

## Advanced Overrides

### Processing Parameters

```bash
# More cards per page
swanki pdf_path=paper.pdf citation_key=test processing.num_cards_per_page=5

# Larger processing window
swanki pdf_path=paper.pdf citation_key=test processing.window_size=3

# Disable image cards
swanki pdf_path=paper.pdf citation_key=test processing.image_cards.enabled=false
```

### Model Configuration

```bash
# Use GPT-4
swanki pdf_path=paper.pdf citation_key=test models.llm.model=gpt-4

# Lower temperature for more consistent output
swanki pdf_path=paper.pdf citation_key=test models.llm.temperature=0.3

# Different voice for TTS
swanki pdf_path=paper.pdf citation_key=test models.tts.voice_id=your_voice_id
```

### Output Configuration

```bash
# Custom output directory
SWANKI_DATA=/custom/path swanki pdf_path=paper.pdf citation_key=test

# Different tag format
swanki pdf_path=paper.pdf citation_key=test output.tag_format=spaces
```

## Examples

### Research Paper with Full Processing

```bash
swanki pdf_path=research.pdf \
  citation_key=johnson2024 \
  pipeline=comprehensive \
  audio=cards \
  anki=auto_send \
  anki.deck_name="Research::Papers::{citation_key}"
```

### Quick Review Material

```bash
swanki pdf_path=lecture_notes.pdf \
  citation_key=lecture_01 \
  pipeline=fast \
  processing.num_cards_per_page=2
```

### Technical Documentation

```bash
swanki pdf_path=manual.pdf \
  citation_key=api_docs \
  prompts=technical \
  processing.image_cards.enabled=true \
  processing.image_cards.cards_per_image=5
```

## Debugging

### View Hydra Configuration

To see the full configuration being used:

```bash
swanki pdf_path=paper.pdf citation_key=test --cfg job
```

### Check Output Structure

```bash
tree swanki-out/citation_key/
```