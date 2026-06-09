---
id: sof5t85u1ccouywm9heggz5
title: Libraries
desc: ''
updated: 1781029315687
created: 1781029315687
---

## 2026.06.09 - Library ensure + index (durable record for deleted setup script)

`ensure_libraries` is the port of the deleted, previously undocumented
`scripts/abs_setup_libraries.py`: idempotently create
`/audiobooks/<proj>/Swanki-<Kind>-<Audiotype>` libraries per projection;
existing folders are left untouched; a library name colliding across
projections gets the `<proj>: ` prefix.

- `build_library_index` inverts folder paths to
  `(projection, kind, audiotype) -> library_id`, normalizing audiotype to
  lowercase on BOTH store and lookup. The legacy scripts disagreed on case,
  which left `abs_setup_collections.py` lookups silently missing -- a latent
  bug fixed by the normalization.
- `library_items_by_title` documents the ABS<->Zotero contract: item title /
  folder name == citation key (group key for books); unmatched folders are
  silently skipped ON PURPOSE so non-swanki items coexist in the libraries.
