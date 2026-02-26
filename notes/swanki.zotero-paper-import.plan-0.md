---
id: skw4jmy47javog5a892ic0x
title: Plan 0
desc: ''
updated: 1772083209035
created: 1772083204562
---
Zotero Paper Import for Swanki

## Context

Papers to process are tracked in scratch notes (e.g., `scratch.2026.02.06.104018-CO-Biotech2026-papers.md`) as checkbox lists with citation keys. Currently importing requires manually downloading PDFs. We want: give a citation key -> download PDF(s) from Zotero -> create `Swanki_Data/{key}/` -> then `/clean-pdf` handles the rest.

Test case: `montanolopezPhysiologicalLimitationsOpportunities2022` -- should create `../Swanki_Data/montanolopezPhysiologicalLimitationsOpportunities2022/` with the PDF.

## Files to Create/Modify

### 1. `scripts/zotero_import.py` (new)

Simple script. Takes citation key(s) as args. Reads `ZOTERO_API_KEY` and `ZOTERO_LIBRARY_ID` from `.env`. Connects via pyzotero as user library. Searches for item by citation key, downloads PDF attachment(s) to `../Swanki_Data/{key}/`. Prints what it downloaded.

### 2. `.claude/skills/zotero-import/SKILL.md` (new)

Skill that takes citation key(s), tells user to run the script, then after download runs `/clean-pdf`.

### 3. `pyproject.toml` (modify)

Add `pyzotero` to dependencies.

### 4. `.env` (user adds manually)

```
ZOTERO_API_KEY=<your-key>
ZOTERO_LIBRARY_ID=<your-user-id>
```

## Verification

Run `python scripts/zotero_import.py montanolopezPhysiologicalLimitationsOpportunities2022` and confirm PDF appears in `../Swanki_Data/montanolopezPhysiologicalLimitationsOpportunities2022/`.
