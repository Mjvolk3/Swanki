---
id: 9ccq60vkv7h3uenaxf7yfl9
title:   Init  
desc: ''
updated: 1773143266626
created: 1773143266626
---

## 2026.04.16 - Re-export `restitch_from_chunks`

Added `restitch_from_chunks` to the public surface alongside the four `generate_*_audio` functions, so callers can rebuild a final MP3 from a `chunk_manifest.json` without reaching into `_common`. Pairs with the chunk-retention work in lecture/reading/summary/card.
