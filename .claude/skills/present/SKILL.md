# Generate Presentation

Generate a Reveal.js HTML presentation from Swanki-processed paper data.

## Arguments

`/present <citation_key> [instructions...]`

- `citation_key` (required): Zotero citation key (e.g., `merzbacherAccuratePredictionGene2025`)
- Everything after the key is treated as free-text instructions

## Workflow

1. Parse the citation key and instructions from the arguments.
2. Determine the data directory: `$SWANKI_DATA/<citation_key>/` or `../Swanki_Data/<citation_key>/`
3. Find the latest versioned output directory (e.g., `<key>_3/`)
4. Run the presentation generation:

```bash
/Users/michaelvolk/opt/miniconda3/envs/swanki/bin/python -c "
from pathlib import Path
from swanki.presentation import run

run(
    citation_key='<CITATION_KEY>',
    instructions='<INSTRUCTIONS>',
    slides_min=<MIN>,
    slides_max=<MAX>,
    data_dir=Path('<DATA_DIR>'),
    model='gpt-4o',
)
"
```

5. Report the output path and suggest opening in browser.

## Defaults

- Slides: 10-14 (override with "N slides" in instructions)
- Model: gpt-4o
- Output: `$SWANKI_DATA/<citation_key>/presentation/presentation.html`
- Figures extracted at 300 DPI from the clean PDF

## Example Invocations

```
/present merzbacherAccuratePredictionGene2025 12 slides, include all main figures and Fig S2
/present smithDeepLearning2024 8-10 slides, focus on methodology
```
