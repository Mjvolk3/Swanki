# Clean PDF for Swanki

Fully automated PDF preparation: detect and remove reference pages from main paper and SI, then stitch them together.

## Input

The user provides:

- A paper directory path under `Swanki_Data/`, e.g. `/Users/michaelvolk/Documents/projects/Swanki_Data/sveshnikovaDesigningPathwaysBioproducing2025/`
- OR just a citation key, e.g. `sveshnikovaDesigningPathwaysBioproducing2025` (resolve to `/Users/michaelvolk/Documents/projects/Swanki_Data/{citation_key}/`)

## Procedure

### Step 1: Identify PDFs

Look in `{dir}/` for:

- `{citation_key}.pdf` — the main paper (required)
- `{citation_key}_si.pdf` or `{citation_key}_SI.pdf` — supplementary information (optional)

If no SI PDF exists, the user may have a combined PDF (main + SI in one file). Handle both cases.

### Step 2: Auto-detect reference pages

Use `/Users/michaelvolk/miniconda3/bin/python` with PyPDF2 for text extraction only (detection). Search ALL lines of every page for reference headings — they are often buried mid-page. When found mid-page, keep that page (body content before the heading is useful) and remove all subsequent pages.

```python
/Users/michaelvolk/miniconda3/bin/python -c "
from PyPDF2 import PdfReader
import warnings, re
warnings.filterwarnings('ignore')

def find_references_page(pdf_path):
    reader = PdfReader(pdf_path, strict=False)
    total = len(reader.pages)
    ref_patterns = r'^(References|REFERENCES|Bibliography|BIBLIOGRAPHY|Literature Cited)\s*$'
    for i, page in enumerate(reader.pages):
        text = page.extract_text() or ''
        lines = [l.strip() for l in text.split('\n') if l.strip()]
        for line in lines:
            if re.match(ref_patterns, line):
                return i, total
    return None, total

pdf_path = '...'
ref_page, total = find_references_page(pdf_path)
if ref_page is not None:
    keep_end = ref_page + 1
    print(f'REFS_START=page {ref_page} (mid-page heading)')
    print(f'TOTAL={total}')
    print(f'ACTION: keep pages 0:{keep_end} ({keep_end} pages)')
else:
    print(f'REFS_START=NOT_FOUND')
    print(f'TOTAL={total}')
"
```

Run this for both main PDF and SI PDF (if present).

Also detect if SI exists within the main PDF by searching for pages containing "Supplementary", "Supporting Information", "Supplemental" after the references section.

### Step 3: Report detection results

Before cutting, report to the user what was detected:

- Total pages in each PDF
- Where references were found
- The planned cuts

Then proceed automatically. Only stop if references were NOT detected (ask the user for page ranges in that case).

### Step 4: Execute cuts

Use `swanki-cut` from the swanki conda env for all PDF cutting. It uses Pythonic indexing (0-based, end-exclusive).

```bash
/Users/michaelvolk/opt/miniconda3/envs/swanki/bin/swanki-cut -s {start} -e {end} {input.pdf} {output.pdf}
```

IMPORTANT: Always use the full path `/Users/michaelvolk/opt/miniconda3/envs/swanki/bin/swanki-cut` (the base conda `swanki-cut` has import issues).

Naming for intermediate files:

- Single source, single cut: `{citation_key}_cut.pdf`
- Multiple cuts from same source: `{citation_key}_cut1.pdf`, `{citation_key}_cut2.pdf`, etc.
- Main body (no refs): `{citation_key}_main_cut.pdf`
- SI (no refs): `{citation_key}_si_cut.pdf`

### Step 5: Create _clean.pdf

For a single cut (no SI), use `pdfunite` to create _clean.pdf (better color/quality preservation than PyPDF2 copy):

```bash
pdfunite {dir}/{citation_key}_cut.pdf {dir}/{citation_key}_clean.pdf
```

If there are multiple pieces to stitch (main body + SI, or multiple cuts), combine with:

```bash
pdfunite piece1.pdf piece2.pdf ... {dir}/{citation_key}_clean.pdf
```

Keep all intermediate `_cut*.pdf` files (do not delete them).

### Step 6: Generate the .sh script

Create/update `{dir}/{citation_key}.sh`:

```bash
#!/bin/bash

swanki pdf_path={dir}/{citation_key}_clean.pdf citation_key={citation_key} +output_dir=../Swanki_Data/{citation_key}/{citation_key} audio=full anki=auto_send pipeline.processing.confirm_before_generation=false
```

### Step 7: Summary

Report to the user:

- Reference pages detected at page N
- Pages kept vs removed
- `_clean.pdf` final page count
- Files created
- `.sh` script contents

## Tools Reference

- `/Users/michaelvolk/opt/miniconda3/envs/swanki/bin/swanki-cut` — PDF cutting (Pythonic 0-based, end-exclusive indexing). Use `--info` for page count.
- `pdfunite file1.pdf file2.pdf ... output.pdf` — Combine/copy PDFs (poppler CLI, better quality than PyPDF2)
- `/Users/michaelvolk/miniconda3/bin/python` with PyPDF2 — text extraction for reference detection ONLY

## Conventions

- All page indices are 0-based, end-exclusive (Python slicing style)
- The final Swanki-ready PDF is always `{citation_key}_clean.pdf`
- Intermediate cut files are preserved
- The `.sh` script always references `_clean.pdf`
- References detection searches ALL lines of every page for "References", "REFERENCES", "Bibliography", "Literature Cited" as standalone headings (headings are often mid-page)
- When refs heading is mid-page, keep that page (body content above heading) and cut everything after
- Do NOT prompt the user for page ranges unless auto-detection fails
