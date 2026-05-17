---
id: wq1cinvq90m2ewja9ohlj8p
title: Zotero_annotations
desc: ''
updated: 1773463875898
created: 1773463875898
---

## 2026.03.13 - Zotero PDF annotation extraction by highlight color

New script to extract highlighted annotations from Zotero PDF attachments, filtered by color. Reuses connection helpers from `zotero_paper_import.py` (pyzotero). Supports named colors (magenta, red, orange, etc.) mapped to Zotero hex values. Outputs formatted markdown with page numbers and comments. Paired with `/zotero-annotations` skill for CLI usage.

## 2026.05.17 - Paginate annotation children

`get_annotations` called `zot.children(att["key"])` unpaginated (pyzotero
caps at 100). A PDF with >100 annotations would silently truncate. Wrapped
in `zot.everything(...)`, matching the companion fix in
[[scripts.zotero_paper_import]]. Surfaced while triaging Hamming Ch1: the
script returned zero annotations because the source PDF itself was hidden
by the same unpaginated-children bug in `get_pdf_attachments`
([[plan.hamming-chapter-1-audio-two-track-fixes.2026.05.17]]).
