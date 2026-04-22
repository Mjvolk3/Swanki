---
id: kt22fhvy7tek4afqi05mzcc
title: Publish_regen_to_abs
desc: ''
updated: 1776884702408
created: 1776884702408
---

## 2026.04.22 - Publish already-generated versioned audio via the Zotero→ABS path

Bridge script for the case where a `regen_lecture.sh` has produced versioned output (e.g. `{citekey}-lecture-audio_v6.mp3`) but the canonical `{prefix}-lecture-audio.mp3` filename that `sync_to_zotero` expects was never updated. Instead of re-running generation, this copies the versioned file into the canonical name, uploads to Zotero as a new timestamped attachment, then runs `abs_refresh.sh` so Audiobookshelf pulls the newest zip.

- Hardcoded JOBS table for thornburg (v2) and zvyagin (v6); simple to extend for new papers.
- Patches `pyzotero._client.DEFAULT_TIMEOUT = 180` before importing `sync_to_zotero` because the 30 s default was timing out on search.
- Treats Zotero as the source of truth per the user's workflow — new versions become new attachments with full history preserved on the Zotero item; `swanki_abs_sync.py` then pulls only the latest per item.
- Obsolete path (earlier version of this script wrote directly into `Swanki_ABS/` with `cp -v`, bypassing Zotero) was replaced once the user confirmed "Zotero then project to proper lib on server" as the intended flow.