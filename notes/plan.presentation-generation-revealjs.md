---
id: 9j7ity9h5smldbgxx8fwwxx
title: Presentation Generation Revealjs
desc: ''
updated: 1773622847785
created: 1773622820237
---
Plan: Presentation Generation Feature + Scratch Outline Restoration

## Context

The user drafted a 12-slide lit review outline for the Merzbacher et al. 2025 Flux Cone Learning paper in `notes/scratch.2026.03.13.134811-outline.md`, but the content was accidentally deleted (file still exists with empty frontmatter). This needs to be recreated from the Swanki output data.

Beyond that, the user wants a new Swanki feature: generating slide presentations from processed paper data. The idea is to provide a prompted specification ("10-14 slides, include all figures, etc.") and get a professional academic presentation. Format: **Reveal.js HTML**. Interface: **both CLI (`swanki-present`) and Claude Code skill (`/present`)**.

---

## Part 1: Recreate Scratch Outline

**File:** `notes/scratch.2026.03.13.134811-outline.md`

Populate with a 12-slide lit review outline for the Merzbacher FCL paper using:

- `Swanki_Data/merzbacherAccuratePredictionGene2025/merzbacherAccuratePredictionGene2025_3/document-summary.md` (comprehensive summary)
- `Swanki_Data/merzbacherAccuratePredictionGene2025/merzbacherAccuratePredictionGene2025_3/image-summaries/` (figure descriptions)

Format: 12 numbered slides with titles and bullet-point content outlines, referencing figures by page number.

---

## Part 2: Presentation Generation Feature

### Architecture

New module `swanki/presentation/` as a standalone package within Swanki, following the existing processor pattern.

```
swanki/presentation/
    __init__.py          # CLI entry point (main)
    models.py            # Pydantic models for slide structure
    slide_generator.py   # LLM-driven content generation via instructor
    figure_extractor.py  # Figure extraction + cropping from pdf-singles
    renderer.py          # Markdown generation + pandoc → Reveal.js HTML
```

### Step 1: Pydantic Models (`swanki/presentation/models.py`)

- `FigureRef` — source page, optional crop bbox (normalized), caption, label
- `MermaidDiagram` — mermaid source code + caption
- `Slide` — title, markdown content, speaker notes, figures, mermaid diagrams, layout type
- `PresentationSpec` — citation key, user instructions, slide count range, custom image paths, output format
- `Presentation` — title, subtitle, authors, date, list of `Slide`

### Step 2: Figure Extractor (`swanki/presentation/figure_extractor.py`)

- Read from `pdf-singles/` directory (individual PDF pages already exist in Swanki output)
- Convert PDF page → PNG using `pdftoppm` subprocess (poppler, available on macOS via homebrew)
- Crop sub-figures using PIL when `FigureRef.crop_bbox` is set
- Copy custom images (png, svg, gif, drawio exports) to output figures dir
- Output to `$SWANKI_DATA/{key}/presentation/figures/`

### Step 3: Slide Generator (`swanki/presentation/slide_generator.py`)

- Single `instructor` call with `response_model=Presentation`
- Inputs: document-summary.md content, image summaries (with page numbers), user instructions
- Follows the pattern in `pipeline.py` for instructor usage
- LLM decides slide structure, which figures to include, where to place mermaid diagrams

### Step 4: Renderer (`swanki/presentation/renderer.py`)

- Convert `Presentation` model → pandoc-flavored markdown with YAML front matter
- Each slide separated by `---`
- Figures resolved to `![caption](figures/label.png)` paths
- Mermaid diagrams as fenced code blocks with `{.mermaid}` class
- Speaker notes in `:::notes` blocks
- Call pandoc: `pandoc slides.md -t revealjs --embed-resources --standalone --mathjax -F mermaid-filter -o presentation.html`
- Optionally include a custom CSS theme for academic styling

### Step 5: CLI Entry Point (`swanki/presentation/__init__.py`)

```
swanki-present merzbacherAccuratePredictionGene2025 \
  --instructions "10-14 slides, include all main text figures" \
  --custom-images path/to/diagram.png
```

- Add `swanki-present` entry point in `pyproject.toml`
- Arguments: citation_key (positional), --instructions, --slides-min, --slides-max, --custom-images, --output-dir
- Loads data from `$SWANKI_DATA/{citation_key}/` (latest version)

### Step 6: Claude Code Skill (`.claude/skills/present/SKILL.md`)

- Wraps the CLI command
- Accepts citation key and free-text instructions
- Runs `swanki-present` and reports results

### Step 7: Tests (`tests/test_presentation/`)

- `test_models.py` — model validation, serialization
- `test_figure_extractor.py` — extraction and cropping logic
- `test_renderer.py` — markdown generation (mock pandoc)

### Output Structure

```
$SWANKI_DATA/{citation_key}/presentation/
    slides.md              # Intermediate pandoc markdown
    figures/                # Extracted/cropped/custom figures
    presentation.html       # Reveal.js output
```

### Dependencies

- `pdf2image` or `pdftoppm` subprocess — PDF page → PNG (poppler already on system)
- `Pillow` — cropping (likely already available)
- No other new deps. `pandoc`, `mermaid-filter`, `instructor` all already in use.

### Key Files to Reference

- `swanki/pipeline/pipeline.py` — instructor usage pattern, data loading
- `swanki/models/document.py` — Pydantic model patterns, `DocumentSummary`
- `swanki/processing/image_processor.py` — image handling patterns
- `swanki/processing/apkg_exporter.py` — exporter class pattern
- `.claude/skills/pdf/SKILL.md` — pandoc invocation pattern
- `notes/assets/publish/scripts/bib_tex_pdf.sh` — pandoc flags reference
- `pyproject.toml` — entry points, dependencies

---

## Verification

1. **Scratch outline**: Read `notes/scratch.2026.03.13.134811-outline.md` and confirm 12 slides with content
2. **Models**: Run `python -c "from swanki.presentation.models import Presentation"` to verify imports
3. **Figure extraction**: Test with Merzbacher pdf-singles, verify PNG output
4. **End-to-end**: Run `swanki-present merzbacherAccuratePredictionGene2025 --instructions "12 slides, all main figures"` and open the resulting HTML
5. **Tests**: `python -m pytest tests/test_presentation/ -xvs`
