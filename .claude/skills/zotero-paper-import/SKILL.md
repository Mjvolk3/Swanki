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
2. Detects non-educational end-matter (acknowledgments, author info, conflicts of interest, references, supporting information, etc.) via PyPDF2 text extraction — cuts at the **earliest** such heading
3. Cuts with `swanki-cut`, creates `_clean.pdf` via `pdfunite`
4. Writes the `.sh` runner script

Use `--download-only` to skip the cleaning step if needed.

### Step 2: Handle failures

If end-matter is NOT auto-detected for a paper (script reports "No end-matter heading detected, keeping all pages"), manually inspect the PDF and re-run the cut using `/clean-pdf {key}`.

### Step 3: Report summary

After all keys are processed, report:
- Which keys were successfully imported
- Pages kept vs removed per paper
- What heading triggered the cut (or that none was detected)
