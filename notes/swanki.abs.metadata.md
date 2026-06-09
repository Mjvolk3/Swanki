---
id: 4pyuqs6e1y5snq5594bzep4
title: Metadata
desc: ''
updated: 1781029328923
created: 1781029328923
---

## 2026.06.09 - Author + cover enrichment (durable record for deleted script)

Port of the deleted, previously undocumented `scripts/abs_enrich_metadata.py`.
Authors (all, Zotero order) are PATCHed every run -- cheap and idempotent --
while cover generation (Zotero PDF download + pdftoppm page-1 render) is
skipped when `cover.jpg` already exists, keeping re-runs fast.

- ABS reports item paths in container view (`/audiobooks/...`);
  `container_to_host` rewrites to `$SWANKI_ABS_ROOT`. Items whose folder name
  matches no Zotero citation key are silently skipped (intentional contract,
  see [[swanki.abs.libraries]]).
