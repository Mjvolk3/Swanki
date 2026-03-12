---
name: zotero-paper-import
description: Download PDFs from Zotero by citation key, cut non-educational end-matter, and prepare for Swanki.
---

When the user asks to import papers from Zotero, follow this workflow:

## Input

The user provides one or more citation keys as arguments, e.g.:
- `/zotero-paper-import montanolopezPhysiologicalLimitationsOpportunities2022`
- `/zotero-paper-import key1 key2 key3`

## Procedure

### Step 1: Run the import script

```bash
/Users/michaelvolk/miniconda3/bin/python scripts/zotero_paper_import.py <key1> [key2 ...]
```

This single command handles everything per key:
1. Connects to Zotero and downloads PDFs into `../Swanki_Data/{key}/`
2. Detects non-educational end-matter (acknowledgments, author info, conflicts of interest, references, etc.) via PyPDF2 text extraction — supports **multi-range** cuts (e.g. keep main article, cut refs, keep Extended Data/STAR Methods/SI figures, cut Nature Portfolio reporting summary)
3. Cuts with `qpdf`, creates `_clean.pdf` via `pdfunite`
4. Writes the `.sh` runner script

Use `--download-only` to skip the cleaning step if needed.

### Step 2: Handle failures

If end-matter is NOT auto-detected for a paper (script reports "No end-matter heading detected, keeping all pages"), or if the auto-detected ranges look wrong (e.g. SI figures were cut), manually inspect the PDF pages and re-cut using `qpdf` + `pdfunite`:

```bash
# Example: keep pages 1-12 and 15-30, cutting refs (13-14) and reporting summary (31-33)
qpdf input.pdf --pages . 1-12 -- range0.pdf
qpdf input.pdf --pages . 15-30 -- range1.pdf
pdfunite range0.pdf range1.pdf output_clean.pdf
rm range0.pdf range1.pdf
```

### Step 3: Report summary

After all keys are processed, report:
- Which keys were successfully imported
- Pages kept vs removed per paper
- What heading triggered the cut (or that none was detected)
