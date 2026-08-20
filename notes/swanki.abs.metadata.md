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

## 2026.08.20 - Inherit an existing cover before rendering the PDF

A new projection's item folders start bare, so the `cover.jpg`-exists
idempotency guard fell straight through to `render_cover`, which renders page
1 of the Zotero PDF. For `hammingArtDoingScience2020` that is the
CRC/Routledge scan ("Also available as a printed book" across the bottom),
while `michaelvolk` and `mv-ra` have carried the curated Stripe Press cover
since April -- so MV-RP showed a visibly different edition of the same book
and read as a duplicate in the ABS clients.

`inherit_cover` now globs `abs_root/*/Swanki-*/<group>/cover.jpg` and copies
the first match before the PDF path is reached; rendering is the fallback for
a book no projection has a cover for yet. Counted separately in the summary
line (`N covers generated, M inherited`). The existing skip-if-present rule
still runs first, so an inherited cover is written once and never re-copied.
