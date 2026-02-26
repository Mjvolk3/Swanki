---
id: skw4jmy47javog5a892ic0x
title: Plan 0
desc: ''
updated: 1772085780155
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

## Extra Context

Papers are tracked in scratch notes as citation key checklists. Currently importing requires manually downloading PDFs from Zotero. This adds a script and skill: give a citation key -> download PDF(s) from Zotero -> create `Swanki_Data/{key}/` -> then `/clean-pdf` handles the rest.

## Changes

### 1. Create `scripts/zotero_import.py`

- Uses `pyzotero` to connect as user library (`Zotero(library_id, 'user', api_key)`)
- Reads `ZOTERO_API_KEY` and `ZOTERO_LIBRARY_ID` from `.env` via `python-dotenv`
- Search strategy: `zot.items(q=citation_key)` for server-side narrowing, then client-side filter on `data["extra"]` for `Citation Key: {key}` (BetterBibTeX) or `data.get("citationKey")` (Zotero 7 native)
- Falls back to `qmode="everything"` if first search finds nothing
- Gets PDF attachments via `zot.children(item_key)`, filters `contentType == "application/pdf"`
- Downloads via `zot.file(attachment_key)` -> writes bytes to `../Swanki_Data/{key}/{key}.pdf`
- Multiple PDFs: `{key}.pdf`, `{key}_si1.pdf`, `{key}_si2.pdf`
- Uses Pydantic models for config and download results (project convention)
- argparse CLI: `python scripts/zotero_import.py <key1> [key2 ...]`
- No try-except — asserts for preconditions, raises LookupError on no match

### 2. Create `.claude/skills/zotero-import/SKILL.md`

- Skill that accepts citation key(s) as arguments
- Step 1: Run `python scripts/zotero_import.py <keys>`
- Step 2: For each key, chain to `/clean-pdf {key}`
- Step 3: Report summary

### 3. Modify `pyproject.toml`

- Add `"pyzotero"` to dependencies (line 36, before closing `]`)

## Verification

```bash
/Users/michaelvolk/miniconda3/bin/python scripts/zotero_import.py montanolopezPhysiologicalLimitationsOpportunities2022
ls ../Swanki_Data/montanolopezPhysiologicalLimitationsOpportunities2022/
```

Confirm PDF appears in the directory.
