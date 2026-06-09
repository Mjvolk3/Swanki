---
id: eedopg6z2s13rg83fqtzav1
title: Collections
desc: ''
updated: 1781029322310
created: 1781029322310
---

## 2026.06.09 - Zotero collection mirror (durable record for two deleted scripts)

Port of the deleted, previously undocumented
`scripts/abs_sync_zotero_collections.py`: invert `item.data.collections` per
projection and upsert one ABS collection per (zotero collection x audiotype).
Reconcile-don't-wipe is the load-bearing rule -- matched-by-name collections
have additions AND removals propagated, while ABS collections matching no
Zotero collection are left untouched so manually-curated ones survive.

- The manifest-driven `scripts/abs_setup_collections.py` (citekey lists in
  projections.yml) was absorbed-by-deletion: referenced by nothing, superseded
  by the Zotero mirror. Its only externally visible behavior (reconcile +
  missing-citekey logging) lives on in `upsert_collection` here.
