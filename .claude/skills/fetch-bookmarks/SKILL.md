---
description: Fetch audio bookmark notes from BookPlayer for a citation key or directory
user_invocable: true
arguments: "[citation_key_or_dir] [--dir <bookplayer_dir>] [--all]"
---

# Fetch BookPlayer Bookmarks

Query the local BookPlayer SQLite database for user bookmark notes left while listening to Swanki audio.

## Arguments

- `[citation_key_or_dir]` (optional): Citation key substring to match (e.g. `bunneHowBuild`), or a BookPlayer directory name (e.g. `cobiot2026-major-refactor`)
- `--dir <bookplayer_dir>` (optional): Filter to a specific BookPlayer directory prefix (e.g. `cobiot2026-major-refactor`, `Papers/summary`)
- `--all` (optional): Show all user bookmarks across the entire library

If no arguments are given, list all BookPlayer top-level directories and their bookmark counts.

## Database

Path: `/Users/michaelvolk/Library/Group Containers/group.com.tortugapower.audiobookplayer.files/BookPlayer.sqlite`
Env var: `BOOKPLAYER_DB`

## BookPlayer Directory Structure

Files are organized by how they were imported. The same citation key can appear in multiple directories:

- `Papers/{summary,reading,lecture}/` — individual paper audio
- `co-biotechnology-2026-1/{Summary,Lecture,Transcript}/` — CO-Biotech 2026 collection v1
- `cobiot2026-major-refactor/{Summary,Lecture,Transcript}/` — CO-Biotech 2026 post-refactor
- Books: `Meditations/`, `Bishop Deep Learning/`, `Palsson - Systems Biology/`, etc.

**Always filter by `ZRELATIVEPATH`** (not just filename) since duplicates exist across directories.

## Bookmark Types

- Type `0` = user bookmark (these are the notes we care about)
- Type `1` = play position (auto, "Last position before playback started")
- Type `2` = skip/sleep (auto)

## Instructions

1. **No arguments** — show directory overview:
   ```sql
   SELECT
     CASE
       WHEN INSTR(i.ZRELATIVEPATH, '/') > 0
       THEN SUBSTR(i.ZRELATIVEPATH, 1, INSTR(i.ZRELATIVEPATH, '/') - 1)
       ELSE '(root)'
     END as directory,
     COUNT(*) as bookmark_count,
     SUM(CASE WHEN b.ZNOTE IS NOT NULL AND b.ZNOTE != '' AND b.ZNOTE NOT LIKE 'Last position%' THEN 1 ELSE 0 END) as with_notes
   FROM ZBOOKMARK b
   JOIN ZLIBRARYITEM i ON b.ZITEM = i.Z_PK
   WHERE b.ZTYPE = 0
   GROUP BY directory
   ORDER BY directory;
   ```

2. **Citation key given** — fetch all user bookmarks matching that key:
   ```sql
   SELECT i.ZRELATIVEPATH, b.ZTIME, b.ZNOTE
   FROM ZBOOKMARK b
   JOIN ZLIBRARYITEM i ON b.ZITEM = i.Z_PK
   WHERE b.ZTYPE = 0
     AND i.ZRELATIVEPATH LIKE '%<citation_key>%'
   ORDER BY i.ZRELATIVEPATH, b.ZTIME;
   ```

3. **`--dir` given** — fetch all user bookmarks under that directory:
   ```sql
   SELECT i.ZRELATIVEPATH, b.ZTIME, b.ZNOTE
   FROM ZBOOKMARK b
   JOIN ZLIBRARYITEM i ON b.ZITEM = i.Z_PK
   WHERE b.ZTYPE = 0
     AND i.ZRELATIVEPATH LIKE '<dir>/%'
   ORDER BY i.ZRELATIVEPATH, b.ZTIME;
   ```

4. **`--all`** — fetch every user bookmark with a non-empty note:
   ```sql
   SELECT i.ZRELATIVEPATH, b.ZTIME, b.ZNOTE
   FROM ZBOOKMARK b
   JOIN ZLIBRARYITEM i ON b.ZITEM = i.Z_PK
   WHERE b.ZTYPE = 0
     AND b.ZNOTE IS NOT NULL AND b.ZNOTE != ''
   ORDER BY i.ZRELATIVEPATH, b.ZTIME;
   ```

Run the query via `sqlite3` using the DB path above. Format the output as a markdown table or grouped list for the user:

- Group by audio file (relativePath)
- Format ZTIME as `MM:SS` (divide by 60 for minutes, mod 60 for seconds)
- Show the note text
- If a bookmark has no note, show `(no note)` in dimmed text
- If multiple directories match, clearly label which directory each result comes from

After displaying results, briefly summarize the actionable feedback themes (e.g. "3 notes about TTS pronunciation issues", "2 notes about math rendering").
