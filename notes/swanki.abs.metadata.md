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

## 2026.07.27 - Editor fallback: edited volumes had a blank ABS author

`derive_authors` filtered creators to `creatorType == "author"` only. Edited
volumes -- a large share of the textbooks swanki ingests -- carry **only**
editors in Zotero, so the filter returned `[]`, the caller's `if authors:` guard
skipped the PATCH, and the ABS item kept a blank author indefinitely. There was
no error and no log line; the refresh just reported "0 author updates" and
looked healthy.

Caught on `feldmannYeastMolecularCell2012`, whose sole Zotero creator is
`{'creatorType': 'editor', 'firstName': 'Horst', 'lastName': 'Feldmann'}` --
all three projections (Summary/Reading/Lecture) showed `authorName=''`.

Fix: try `author` first, fall back to `editor` when no authors exist. Authors
still win whenever both are present, and other creator types (translator,
contributor) are still ignored. Regression tests in
`tests/test_abs_projections.py`: author-preferred, order-preserved,
editor-fallback, other-types-ignored.

Note the blank-author state is self-healing on the next `finalize-abs` once the
item has any creators, because the author PATCH is deliberately not idempotency-
gated (unlike covers) -- it rewrites the same value every pass.
