---
id: gkj1536fz68r1oj7v5ph30m
title: Client
desc: ''
updated: 1781029295820
created: 1781029295820
---

## 2026.06.09 - One hardened httpx client for the whole ABS surface

`ABSClient` replaces the four transport stacks the legacy scripts grew. One
httpx session (180s read / 60s connect, matching the hardened Zotero client),
one token chain (`ABS_API_TOKEN_FILE` -> `ABS_API_TOKEN` -> default infra file,
always `expanduser()`d -- previously only one script honored the env fallback
and not every script expanded `~`), and one retry policy ported from
[[swanki.sync.zotero_client]]: timeouts/transport errors and 500/502/503/504
retried with bounded exponential backoff, 404 terminal. The previously
unretried inline-curl library scan in `abs_refresh.sh` step 7 now goes through
the same policy, so a flaky network can no longer silently leave ABS stale.

- `bookmark_time_key` keeps the bookmark-DELETE coercion: ABS stores integral
  times as ints, so `DELETE .../bookmark/2105.0` 404s where `.../2105` works.
- Constructor takes `transport=` (httpx.MockTransport) so all tests run
  without network or token file.
- httpx is now a declared dependency in pyproject (was transitive-only via
  pyzotero while three swanki modules imported it directly).

## 2026.06.12 - create_bookmark

`create_bookmark(library_item_id, time_s, title)` — POST
`/api/me/item/{id}/bookmark`, time coerced through `bookmark_time_key` for
parity with the int-keyed DELETE. Completes the bookmark CRUD surface for
[[swanki.abs.bookmarks]] `add_bookmark`.
