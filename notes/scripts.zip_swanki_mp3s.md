---
id: 4z8vjhdajgi3atcp5cs7zve
title: Zip_swanki_mp3s
desc: ''
updated: 1776292514824
created: 1776292514824
---

## 2026.04.15 - Nightly Zotero MP3 zip export for BookPlayer

Script to query Zotero for items tagged with the fox tag, download the most recent zip attachment per item, extract MP3s (summary, reading, lecture), and repack into `~/Downloads/swanki.zip` organized by class (Book vs Paper) and audio type. Books get an extra citation key subdirectory to group chapters. Runs nightly at 4:07am via cron on the M1 Mac.

- Queries all items tagged with the fox tag via pyzotero, paginates in batches of 100
- Deduplicates zip attachments by timestamp in filename (keeps most recent per citation key)
- Classifies items as Book (book, bookSection) or Paper (everything else) via Zotero itemType
- Books nest under `MV-Swanki/Book/{citationKey}/{audioType}/`, Papers under `MV-Swanki/Paper/{audioType}/`
- Skips broken uploads (404s from `_scratch_tmp_` prefixed files) gracefully
- Cron entry: `7 4 * * *` with logs at `/tmp/swanki-zip.log`
