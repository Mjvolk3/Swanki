---
id: 8sof3h0uoxrm9xv4gp1frl2
title: Republish_fixed_lectures
desc: ''
updated: 1776884695923
created: 1776884695923
---

## 2026.04.22 - Orchestrate the duplicate-opener fix end-to-end

Re-TTS → Zotero upload → ABS cleanup → library refresh for thornburg and zvyagin, addressing the regen pattern the user called out: every regenerated audio should end up on the Audiobookshelf server as the single current version, not as a new "chapter" alongside older versions.

Four steps:

1. `retts_cleaned_transcripts.py` — regenerate both MP3s from the hand-cleaned transcripts without touching the LLM.
2. Python block calling `sync_to_zotero` for each paper, bumping pyzotero's `DEFAULT_TIMEOUT` to 180 s first (default 30 s was timing out during item search on the user's Zotero library).
3. `find -delete` every `*.mp3` under each paper's `Swanki-Paper-{Lecture,Summary,Reading}/` ABS folder — ABS will re-populate from the newest Zotero zip on the next refresh, so deleting first guarantees only the new version ends up visible.
4. `bash scripts/abs_refresh.sh` — acquires the flock, pulls from Zotero, now includes the stale-chapter cleanup step, and forces an ABS library scan.

This is a one-shot for the 04-22 fix, not a general-purpose tool: paper paths and citation keys are hardcoded. Kept in the repo as a worked reference for future "fix-then-republish" sequences.