---
id: qa6hj5ksj7udscnpq92ufg5
title: Zotero_client
desc: ''
updated: 1780593075974
created: 1780593075974
---

## 2026.06.04 - Hardened pyzotero client + retry wrapper

Part of [[swanki.delivery]] ([[plan.delivery-subsystem-source-target-sync.2026.06.04]]).

The Zotero API is intermittently flaky (502/503/504, slow reads) and pyzotero
1.11.0 ships no read-side retry. Two levers:

- `harden_zotero_timeouts()` lifts `pyzotero._client.DEFAULT_TIMEOUT` (default
  30s) to 180s. **Investigation correction to the plan:** pyzotero is entirely
  httpx-based, and `_client.py` passes an explicit per-call
  `timeout=DEFAULT_TIMEOUT` on every GET that *overrides* any client-level
  timeout — so handing `zotero.Zotero(client=httpx.Client(timeout=...))` does
  NOT lift the read timeout. Rebinding the module global (read at call time) is
  the only effective lever, which is what the legacy `swanki_anki_sync.py` poke
  did; we keep it but wrap it in a named helper.
- `with_zotero_retry(call)` adds bounded exponential-backoff-plus-jitter retry
  (3 tries) on `httpx.TimeoutException`/`TransportError` and 5xx in
  `{500,502,503,504}`. A 404 (or any other 4xx) is terminal and raises
  immediately — retrying a missing artifact only burns the budget. `sleep` is
  injectable so tests never block.

`make_zotero_client()` applies the timeout lift and returns a `Zotero`.
`sync_to_zotero` now builds its client via this and retry-wraps the item-find
pagination; `ZoteroSource` retry-wraps `items`/`children`/`file` downloads.
