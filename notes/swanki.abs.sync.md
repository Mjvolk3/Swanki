---
id: txq7yjp34x94rcoly48nm8m
title: Sync
desc: ''
updated: 1781029309063
created: 1781029309063
---

## 2026.06.09 - Zotero -> disk audio sync (port of scripts/swanki_abs_sync.py)

Near-verbatim port of the deleted `scripts/swanki_abs_sync.py` (see
[[scripts.swanki_abs_sync]] for its history). The load-bearing idempotency
rules are preserved exactly: skip mp3s whose timestamped+hashed filename is
already on disk; replace stale same-`(key, audio_type)` files on republish
(otherwise ABS shows both as separate chapters); skip Zotero attachments whose
file is missing (stale metadata) with a warning instead of aborting.

- `replace_stale` is factored out so the targeted refresh's local-file drop
  reuses the same replacement rule as the zip-extract path.
- The Zotero client now comes from `make_zotero_client` (hardened read
  timeout) instead of a bare `zotero.Zotero`.
- `MP3_PATTERN` gained a named `ts` group so newest-per-(key, type) selection
  can sort republishes without re-parsing.
