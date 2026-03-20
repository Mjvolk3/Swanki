---
id: 41bar9loelgo7cgb4zxf1nw
title: Segmenter
desc: ''
updated: 1773263538662
created: 1773263538662
---

## 2026.03.11 - New module for character-based segmentation

Pure utility module supporting the "char" segmentation mode for card generation (Step 3 of [[plan.major-refactor-sequence.plan-0]]). Recombines per-page markdown files into a single document, then re-splits at newline boundaries into uniform character-length segments so card count scales naturally with content density.

- `combine_markdown_files()` -- concatenates page files and tracks character offsets per page.
- `split_into_segments()` -- splits text at newline boundaries (fallback to space) into ~target_chars segments. Returns (text, start, end) tuples.
- `write_segment_files()` -- writes numbered `segment-N.md` files to an output directory.
- `build_segment_to_page_map()` -- maps each segment to the page indices it overlaps, enabling document-order image card interleaving.
