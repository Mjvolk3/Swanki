# Configuration

Swanki uses Hydra for configuration management. When you first run Swanki, it creates a `.swanki_config/` directory with all default configurations.

## Configuration Structure

```
.swanki_config/
├── config.yaml           # Main configuration
├── pipeline/            # Processing pipeline settings
│   ├── default.yaml
│   ├── comprehensive.yaml
│   └── fast.yaml
├── prompts/             # AI prompt templates
│   ├── default.yaml
│   └── technical.yaml
├── models/              # LLM and TTS settings
│   ├── default.yaml
│   └── openai_tts.yaml
├── audio/               # Audio generation settings
│   ├── default.yaml
│   ├── cards.yaml
│   ├── summary.yaml
│   └── full.yaml
├── output/              # Output format settings
│   └── default.yaml
└── anki/                # Anki integration settings
    ├── default.yaml
    ├── auto_send.yaml
    └── custom_deck.yaml
```

## Key Configuration Options

### Pipeline Settings

Control how PDFs are processed:

```yaml
# pipeline/default.yaml
processing:
  window_size: 2           # Pages to process together
  skip: 1                  # Pages to skip between windows
  num_cards_per_page: 3    # Target cards per page
  image_cards:
    enabled: true          # Generate cards from images
    cards_per_image: 3     # Cards per image
```

### Model Settings

Configure AI models:

```yaml
# models/default.yaml
models:
  llm:
    provider: openai
    model: gpt-4o
    temperature: 0.7
  tts:
    provider: elevenlabs
    voice_id: 21m00Tcm4TlvDq8ikWAM
```

### Audio Settings

Control audio generation:

```yaml
# audio/cards.yaml
audio:
  generate_complementary: true  # Card audio
  generate_summary: false       # Summary narration
  generate_reading: false       # Full document reading
  complementary_speed: 1.6      # Playback speed
```

### Anki Settings

Configure Anki integration:

```yaml
# anki/auto_send.yaml
anki:
  enabled: true
  auto_send: true
  deck_name: "{citation_key}"   # Supports template variables
  update_existing: true
  media_upload: true
```

## Customizing Configurations

### Edit Existing Configs

Simply edit any file in `.swanki_config/`:

```bash
# Edit the default pipeline settings
nano .swanki_config/pipeline/default.yaml
```

### Create New Config Groups

Create your own configuration variants:

```bash
# Create a custom pipeline configuration
cat > .swanki_config/pipeline/my_custom.yaml << EOF
processing:
  window_size: 4
  num_cards_per_page: 10
  image_cards:
    enabled: true
    cards_per_image: 5
EOF
```

Then use it:

```bash
swanki pdf_path=paper.pdf citation_key=test pipeline=my_custom
```

### Override at Runtime

Override any setting from the command line:

```bash
# Single override
swanki pdf_path=paper.pdf citation_key=test processing.num_cards_per_page=5

# Multiple overrides
swanki pdf_path=paper.pdf citation_key=test \
  models.llm.model=gpt-4 \
  models.llm.temperature=0.5 \
  audio.generate_summary=true
```

## Environment Variables

- `SWANKI_DATA`: Base directory for output (default: `swanki-out`)
- `OPENAI_API_KEY`: OpenAI API key
- `ELEVEN_LABS_API_KEY`: ElevenLabs API key