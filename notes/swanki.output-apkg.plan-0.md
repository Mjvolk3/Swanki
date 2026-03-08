---
id: mwn6hgqre5zhbpw0ma60q8n
title: Plan 0
desc: ''
updated: 1772222376192
created: 1772221934152
---
Direct .apkg Export (No External Dependency)

## Context

Currently, Swanki generates cards as markdown and sends them to Anki via AnkiConnect (requires a running Anki instance). Users then review, prune, and manually export to `.apkg` for sharing. This is becoming unnecessary overhead. Adding direct `.apkg` output lets the pipeline produce a portable, shareable file without Anki running. Although we still like to do this for our own personal usage. We would like to simultaneously send via ankiconnect but also save the raw `.apkg` locally. The idea is If I run swanki with anki open on some paper I will see cards in anki on completion but will also already have the `.apkg` for easy sharing. 

We implement the `.apkg` format directly using `sqlite3` + `zipfile` (both stdlib) -- no `genanki` dependency. The `.apkg` file goes in the pipeline output directory alongside `cards-plain.md` and other outputs, named `{citation_key}.apkg`. The output directory structure is `Swanki_Data/{citation_key}/{citation_key}/` (the inner dir is the pipeline run output; on reruns it gets suffixed `{citation_key}_2/`, etc.):

```
Swanki_Data/luCellFactoryDesign2024/
  luCellFactoryDesign2024.pdf
  luCellFactoryDesign2024/              <-- pipeline output dir
    cards-plain.md
    cards-with-audio.md
    document-summary.md
    luCellFactoryDesign2024.apkg        <-- .apkg goes here
    ...
```

## .apkg Format Summary

An `.apkg` is a ZIP containing:

- `collection.anki2` -- SQLite database with tables: `col`, `notes`, `cards`, `revlog`, `graves`
- `media` -- JSON file mapping numeric indices to filenames (`{"0": "audio.mp3", "1": "image.png"}`)
- `0`, `1`, `2`, ... -- actual media files renamed to their index

Key details:

- `col` table has one row with JSON blobs for models, decks, deck config, and settings
- `notes.flds` uses `\x1f` (unit separator) to delimit fields
- Cards reference notes by `nid` and decks by `did`
- Cloze model uses `type: 1`; Basic uses `type: 0`
- For each cloze note, one card per `{{cN::...}}` pattern found
- IDs are epoch milliseconds; GUIDs are base91-encoded hashes for dedup on import

## Plan

### Step 1: Extract shared card-processing functions from AnkiProcessor

**File**: `swanki/processing/anki_processor.py`

The methods `_prepare_for_anki`, `_process_content`, `_fix_cloze_issues`, `_validate_and_fix_cloze_format`, `_convert_markdown_tables_to_html`, `_convert_markdown_lists_to_html`, `_process_table_lines`, `_extract_cards`, `_split_front_back`, `_parse_tags` have no dependency on `self` (no host/port/url access). Extract them to module-level functions. Keep `AnkiProcessor` methods as thin wrappers calling the module-level versions so existing callers are unaffected.

### Step 2: Create `ApkgExporter`

**New file**: `swanki/processing/apkg_exporter.py`

Uses only `sqlite3`, `zipfile`, `hashlib`, `json`, `os`, `re`, `tempfile` (all stdlib).

Core implementation:

- **Stable model IDs**: SHA-256 hash of fixed strings (`"swanki-basic-v1"`, `"swanki-cloze-v1"`), truncated to int
- **Stable deck ID**: SHA-256 hash of deck name, truncated to int
- **`_build_database(cards, deck_name) -> Path`**: Creates a temp SQLite file with the Anki schema (v11), inserts `col` row with model/deck/config JSON, inserts `notes` and `cards` rows
- **`_build_package(db_path, media_files, output_path)`**: Zips the database as `collection.anki2`, writes `media` JSON manifest, includes numbered media files
- **GUID generation**: SHA-256 of field content, first 10 chars base91-encoded
- **Checksum**: `int(hashlib.sha1(first_field.encode()).hexdigest()[:8], 16)` (matches Anki's csum)
- **Cloze card generation**: Regex scan for `{{c(\d+)::` patterns in Text field, create one card row per unique cloze number

Public API:

- `ApkgExporter(deck_name: str)`
- `export_from_file(md_path: Path, output_path: Path) -> Path` -- reads markdown, parses via extracted `extract_cards`, runs `prepare_for_anki` on fields, collects media, writes `.apkg`
- `export_from_cards(card_dicts: List[Dict], output_path: Path, base_dir: Path) -> Path` -- same from pre-parsed dicts

### Step 3: Register in `swanki/processing/__init__.py`

Add `ApkgExporter` to imports and `__all__`.

### Step 4: Integrate into pipeline

**File**: `swanki/pipeline/pipeline.py`

The `.apkg` export runs **independently of and alongside** AnkiConnect. Both can fire in the same pipeline run.

**4a. In `generate_outputs()` (~line 1971)**: After writing `cards-plain.md`, check `output_config.get("create_anki_deck", False)`. If true, instantiate `ApkgExporter` with the deck name (same logic as the AnkiConnect path at line 2424), call `export_from_file(plain_path, output_dir / f"{self.citation_key}.apkg")`.

**4b. After audio generation (~line 2430 area)**: If `create_anki_deck` is true and audio cards exist, re-export the `.apkg` using `cards-with-audio.md` so audio files get bundled into the package. Then proceed to AnkiConnect send as before -- both paths run.

The existing `create_anki_deck: false` default in `swanki/config/generator.py:973` means this is opt-in. Output lands in the citation key directory alongside other outputs (e.g., `Swanki_Data/luCellFactoryDesign2024/luCellFactoryDesign2024/luCellFactoryDesign2024.apkg`).

### Step 5: Tests

**New file**: `tests/test_apkg_exporter.py`

- Basic card export -- verify `.apkg` is a valid zip with `collection.anki2` and `media`
- Open the SQLite inside the zip and verify note/card row counts
- Cloze card with `{{c1::...}}` and `{{c2::...}}` -- verify 2 card rows generated
- Mixed Basic + Cloze in one deck
- Media bundling -- create temp audio files, verify they appear in the zip
- Stable IDs -- export same deck twice, verify model/deck IDs match
- Import into Anki manually as a smoke test (not automated)

## Key Files

| File                                  | Action                                       |
|---------------------------------------|----------------------------------------------|
| `swanki/processing/anki_processor.py` | Extract processing functions to module level |
| `swanki/processing/apkg_exporter.py`  | **New** -- ApkgExporter (sqlite3 + zipfile)  |
| `swanki/processing/__init__.py`       | Add export                                   |
| `swanki/pipeline/pipeline.py`         | Wire create_anki_deck alongside AnkiConnect  |
| `tests/test_apkg_exporter.py`         | **New** -- tests                             |

No new dependencies -- uses only Python stdlib (`sqlite3`, `zipfile`, `hashlib`, `json`, `tempfile`).

## Verification

1. Run `pytest tests/test_apkg_exporter.py -xvs`
2. Run the full pipeline on a paper with `create_anki_deck: true` and verify `{citation_key}.apkg` appears in the output directory
3. Import the `.apkg` into Anki and verify cards render correctly (math, cloze, images, audio)
