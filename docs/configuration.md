# Configuration

Swanki uses Hydra for configuration management. When you first run Swanki, it creates a `.swanki_config/` directory with all default configurations.

## Configuration Structure

```yaml
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

### Cloze Card Settings

Swanki enforces strict validation for cloze deletions:

- **Word Limit**: 1-5 words maximum per cloze deletion
- **Math Support**: Automatically handles LaTeX within cloze deletions
- **Image Cards**: Automatically converts image cards from cloze to Q&A format

```yaml
# Cloze validation is automatic and enforced
# Bad: {{c1::techniques that add constraints or penalties to prevent overfitting}}
# Good: {{c1::regularization techniques}}
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

## Sliding Window Processing

The sliding window approach is a key feature for generating contextually-aware flashcards from multi-page documents. Instead of processing each page in isolation, Swanki groups pages together in overlapping windows.

### How It Works

```yaml
# pipeline/default.yaml
processing:
  window_size: 2    # Pages to process together
  skip: 1           # Pages to skip between windows
```

With `window_size=2` and `skip=1`, pages are processed as:

- Window 1: Pages 1-2
- Window 2: Pages 2-3  
- Window 3: Pages 3-4
- And so on...

### Why Use Sliding Windows?

1. **Context Preservation**: Academic content often spans multiple pages. Processing pages together ensures concepts aren't fragmented.

2. **Better Card Quality**: Cards can reference information that bridges pages, creating more comprehensive questions.

3. **Flexible Coverage**: The `skip` parameter controls overlap between windows, balancing thoroughness with efficiency.

### Configuration Examples

#### Dense Coverage (Maximum Context)

```yaml
processing:
  window_size: 3    # Process 3 pages together
  skip: 1           # Move 1 page at a time
  num_cards_per_page: 5
```

This creates heavily overlapping windows for maximum context retention.

#### Balanced Approach (Default)

```yaml
processing:
  window_size: 2    # Process 2 pages together
  skip: 1           # Move 1 page at a time
  num_cards_per_page: 3
```

Good balance between context and processing efficiency.

#### Fast Processing (Minimal Overlap)

```yaml
processing:
  window_size: 2    # Process 2 pages together
  skip: 2           # No overlap between windows
  num_cards_per_page: 3
```

Faster processing with independent windows.

#### Chapter-Level Processing

```yaml
processing:
  window_size: 5    # Process 5 pages together
  skip: 3           # Some overlap between chapters
  num_cards_per_page: 10
```

Suitable for documents with chapter-like sections.

### Card Count Calculation

The total number of cards generated depends on:

- Number of windows: `max(1, (total_pages - window_size) // skip + 1)`
- Cards per window: `num_cards_per_page * window_size`

Example with 10 pages:

- `window_size=2, skip=1`: 9 windows × 6 cards = 54 cards
- `window_size=3, skip=2`: 4 windows × 9 cards = 36 cards
- `window_size=5, skip=5`: 2 windows × 15 cards = 30 cards

### Edge Cases

#### Window Size Exceeds Document Length

If `window_size > total_pages`, Swanki automatically adjusts:

```bash
# 5-page document with window_size=10
# Swanki uses window_size=5 instead
swanki pdf_path=short.pdf citation_key=test \
  pipeline.processing.window_size=10
```

#### Single Page Documents

Even with one page, at least one window is created:

```bash
# 1-page document still generates cards
swanki pdf_path=single.pdf citation_key=test
```

### Best Practices

1. **Research Papers (10-20 pages)**
   - Use `window_size=2-3` with `skip=1`
   - Ensures methodology connects with results

2. **Textbook Chapters (50+ pages)**
   - Use `window_size=5-8` with `skip=3-4`
   - Groups related sections together

3. **Dense Technical Content**
   - Use `window_size=2` with `skip=1`
   - Maximum overlap for complex material

4. **Quick Review Material**
   - Use `window_size=1` with `skip=1`
   - Process each page independently

### Command Line Examples

```bash
# Dense mathematical paper
swanki pdf_path=math_paper.pdf citation_key=Euler2024 \
  pipeline.processing.window_size=3 \
  pipeline.processing.skip=1 \
  pipeline.processing.num_cards_per_page=5

# Long textbook chapter
swanki pdf_path=chapter.pdf citation_key=Biology_Ch3 \
  pipeline.processing.window_size=8 \
  pipeline.processing.skip=4 \
  pipeline.processing.num_cards_per_page=10

# Quick flashcard generation
swanki pdf_path=notes.pdf citation_key=Lecture_Notes \
  pipeline.processing.window_size=1 \
  pipeline.processing.skip=1 \
  pipeline.processing.num_cards_per_page=2
```

## Environment Variables

- `SWANKI_DATA`: Base directory for output (default: `swanki-out`)
- `OPENAI_API_KEY`: OpenAI API key
- `ELEVEN_LABS_API_KEY`: ElevenLabs API key
