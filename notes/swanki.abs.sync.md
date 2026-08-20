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

## 2026.08.20 - Fall through cards-only zips to the newest audio-bearing bundle

Standing up the `mv-rp` projection surfaced a silent data loss: MV-RP came out
missing Hamming CH04-CH10 in all three audio types while `michaelvolk` looked
complete. Cause is upstream of this module -- `latest_zips` keeps only the
newest zip per content-prefix, and the 2026.08.17 correctness-gate re-runs
(`ecea5d4`) emitted **cards-only** zips (one `.apkg`, no mp3s) for exactly
those chapters. A fresh projection therefore extracted nothing for them; the
existing tree only looked fine because it had extracted the audio months
earlier and nothing deletes it.

`sync_projection` now walks `zips_by_prefix` (see [[swanki.delivery.artifacts]])
newest-first and stops at the first bundle that actually carries audio.

- `extract_audio` returns `ExtractResult(written, found)` instead of an int.
  **`found` is pre-filter and that is load-bearing**: "wrote nothing" is wrong
  as a stop signal (a re-run with everything already on disk writes zero and
  would re-walk every historical zip forever), and post-filter types are wrong
  too (a lecture-only projection would never see `summary`/`reading` and would
  walk to the end of history for every chapter). Pre-filter `found` stops at
  the first audio-bearing zip in the common case -- no extra downloads -- and
  only falls through when a zip genuinely has no audio at all.
- A prefix with no audio-bearing zip anywhere now logs
  `warn: no audio-bearing zip for <prefix>` rather than vanishing silently.

Backfilled MV-RP's 21 missing files by hand via `targeted_refresh` per chapter
key before this landed; the fix is what stops it recurring on the next new
projection.
