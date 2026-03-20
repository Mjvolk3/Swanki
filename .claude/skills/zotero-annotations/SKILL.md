---
description: Extract Zotero PDF annotations by citation key and highlight color
user_invocable: true
arguments: "<citation_key> [color]"
---

# Zotero Annotation Extraction

Extract highlighted annotations from a Zotero PDF attachment, filtered by color.

## Arguments

- `<citation_key>` (required): The citation key to look up (e.g. `merzbacherAccuratePredictionGene2025`)
- `[color]` (optional): Color name or hex value. Default: `magenta`. Available: magenta, red, orange, yellow, green, cyan, blue, purple

## Instructions

Run the extraction script:

```bash
~/opt/miniconda3/envs/swanki/bin/python scripts/zotero_annotations.py <citation_key> --color <color>
```

Output the results as markdown to the user.
