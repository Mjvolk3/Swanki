# Introduction

Swanki is a powerful tool for converting PDFs into Anki flashcards with AI-generated content and audio. This guide covers common usage patterns, especially for processing book chapters.

## Processing Book Chapters

When working with textbooks or multi-chapter books, you often need to:
1. Extract specific chapters from a larger PDF
2. Remove unwanted pages (blank pages, references, etc.)
3. Process each chapter with consistent citation keys but separate output directories

### Main Use Case: Book Chapter Processing

```bash
# Process a book chapter with full audio generation
swanki pdf_path=/path/to/chapter.pdf citation_key=authorBookTitle2023 +output_dir=authorBookTitle2023_CH1 audio=full

# Example with auto-send to Anki
swanki pdf_path=/Users/michaelvolk/Documents/projects/Swanki_Data/Nishitani/Nishitani_intro.pdf citation_key=nishitaniSelfovercomingNihilism1990a +output_dir=nishitaniSelfovercomingNihilism1990a_intro audio=full anki=auto_send
```

### Preparing PDFs: Cutting and Combining

Before processing, you may need to extract specific pages or remove unwanted content:

#### Extract Specific Pages
```bash
# Extract pages 10-25 from a large PDF (chapter 2)
swanki-cut input.pdf 10-25 chapter2.pdf

# Extract introduction (pages 1-8)
swanki-cut textbook.pdf 1-8 intro.pdf
```

#### Remove Unwanted Pages and Combine
```bash
# Extract content pages, skipping blanks and references
swanki-cut book.pdf 1-50 part1.pdf    # Main content
swanki-cut book.pdf 55-100 part2.pdf  # Skip pages 51-54 (blank pages)

# Combine the cleaned sections
swanki-combine-pdf part1.pdf part2.pdf -o chapter_clean.pdf
```

### Complete Workflow Example

Here's a complete workflow for processing a book chapter:

```bash
# 1. Extract chapter 5 (pages 120-145) from the full book
swanki-cut full_textbook.pdf 120-145 chapter5_raw.pdf

# 2. Remove references section at the end (pages 141-145)
swanki-cut chapter5_raw.pdf 120-140 chapter5_clean.pdf

# 3. Process with Swanki
swanki pdf_path=chapter5_clean.pdf \
       citation_key=smithMachineLearning2023 \
       +output_dir=smithMachineLearning2023_CH5 \
       audio=full \
       anki=auto_send

# 4. Later, if you forgot to send to Anki
swanki-to-anki /path/to/smithMachineLearning2023_CH5
```

## Basic Examples

### Simple Processing
```bash
# Basic usage with defaults
swanki pdf_path=paper.pdf citation_key=doe2023
```

### With Audio Generation
```bash
# Generate all audio types
swanki pdf_path=paper.pdf citation_key=doe2023 audio=full

# Minimal audio (only card audio)
swanki pdf_path=paper.pdf citation_key=doe2023 audio=minimal
```

### Anki Integration
```bash
# Auto-send to Anki after processing
swanki pdf_path=paper.pdf citation_key=doe2023 anki=auto_send

# Custom deck hierarchy
swanki pdf_path=paper.pdf citation_key=doe2023 anki=auto_send anki.deck_name="Textbooks::MachineLearning::{citation_key}"

# Send existing cards to Anki (if you forgot to use auto_send)
swanki-to-anki /Users/michaelvolk/Documents/projects/Swanki_Data/nishitaniSelfovercomingNihilism1990a_intro

# Send multiple directories at once
swanki-to-anki /Users/michaelvolk/Documents/projects/Swanki_Data/nishitaniSelfovercomingNihilism1990a_*
```

### Batch Processing Multiple Chapters

For processing an entire book, you might create a script:

```bash
#!/bin/bash
# process_book.sh

BOOK="full_textbook.pdf"
CITATION="smithMachineLearning2023"

# Extract and process each chapter
swanki-cut $BOOK 1-15 ch1.pdf
swanki pdf_path=ch1.pdf citation_key=$CITATION +output_dir=${CITATION}_CH1 audio=full

swanki-cut $BOOK 16-35 ch2.pdf
swanki pdf_path=ch2.pdf citation_key=$CITATION +output_dir=${CITATION}_CH2 audio=full

# ... continue for all chapters

# Send all to Anki at once
swanki-to-anki ${CITATION}_*
```

## Tips

- **Citation Key Consistency**: Use the same citation key for all chapters of a book to maintain consistency in audio and references
- **Output Directory Naming**: Use `+output_dir` with suffixes like `_CH1`, `_CH2`, or `_intro` to organize chapters
- **Page Extraction**: Use `swanki-cut` to extract exact page ranges, avoiding blank pages or unwanted content
- **Batch Sending**: Use `swanki-to-anki` with wildcards to send multiple chapters at once

## Next Steps

- [Configuration Guide](configuration.md) - Learn about customizing prompts and settings
- [CLI Usage](cli-usage.md) - Detailed command reference
- [Quickstart](quickstart.md) - Get started quickly