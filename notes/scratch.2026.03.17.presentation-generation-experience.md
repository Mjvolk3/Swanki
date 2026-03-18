---
id: ceajzs2ssmqz332due5hrjj
title: Presentation Generation Experience
desc: ''
updated: 1773775027458
created: 1773775027458
---

# Reveal.js Presentation Generation: Lessons Learned

## What We Built

Generated a Reveal.js HTML presentation for Merzbacher et al. 2025 "Flux Cone Learning" paper using a new `swanki/presentation/` module.

**Output location**: `../Swanki_Data/merzbacherAccuratePredictionGene2025/presentation/`

- `slides.md` -- pandoc markdown source
- `presentation.html` -- rendered Reveal.js output
- `figures/` -- extracted/cropped figure panels
- `style.css` -- custom styling
- `pointer.js` / `pointer.css` -- laser pointer plugin (quarto-ext/pointer)

## What Worked

- **Mathpix CDN images**: Pre-cropped figures from OCR were correctly bounded, better than manual pdftoppm crops
- **Local PIL cropping**: For sub-panel isolation (Fig 2a-f, Fig 4a-c), downloading the full Mathpix figure and cropping locally with PIL gave precise control
- **Mermaid diagrams**: Rendered via mermaid-filter with `MERMAID_FILTER_SCALE=4` for high resolution
- **Pointer plugin**: quarto-ext/pointer works well, toggle with Q key
- **Presenter view**: S key opens speaker notes window
- **KaTeX**: More reliable than MathJax for local serving

## Pain Points -- Why We Prefer PowerPoint

1. **Image sizing is a constant battle**: Every figure required multiple iterations to get height/crop right. No WYSIWYG -- change a number, re-render, refresh, check
2. **Content overflow**: Text falls off slides with no visual warning. Reveal.js doesn't auto-fit or warn
3. **No drag-and-drop**: Can't visually position elements. Everything is CSS/markdown attributes
4. **Figure cropping is tedious**: Manual bounding box iteration for each panel. PowerPoint lets you crop visually
5. **Whitespace control is hard**: Spacing between elements requires CSS hacks (`&nbsp;`, margin overrides)
6. **Title positioning**: Required CSS overrides (`center: false`, flexbox, fixed padding) to get consistent header positions
7. **Local server required**: Chrome blocks CDN scripts from `file://`, so must run `python -m http.server`
8. **No reuse across presentations**: PowerPoint makes it easy to copy slides/images between decks

## Programmatic PPTX Options for Future

### python-pptx (Recommended)

- Full control over slides, images, text, tables
- No LaTeX support (render math to images first)
- Template-based: create a master .pptx template with styling, populate programmatically
- Best for: custom academic styling with reproducible builds

### Pandoc to PPTX

- `pandoc slides.md -t pptx -o presentation.pptx`
- Limitations: uniform column widths in tables, image scaling issues, SVG problems
- Could use as base then post-process with python-pptx

### Marp

- `marp slides.md --pptx`
- Markdown-native, simple syntax
- Output is image-based (not editable text in PPTX)

### LLM + python-pptx

- Use instructor/pydantic to generate slide structure (our existing `SlideGenerator`)
- Render to .pptx via python-pptx instead of pandoc/reveal.js
- Can use PowerPoint templates for consistent academic styling

## Recommendation

Switch the `swanki/presentation/renderer.py` to output PPTX via python-pptx instead of Reveal.js HTML. Keep the same `SlideGenerator` (LLM content generation) and `FigureExtractor` (image cropping). Only the renderer changes. Use a PowerPoint template for consistent academic styling.
