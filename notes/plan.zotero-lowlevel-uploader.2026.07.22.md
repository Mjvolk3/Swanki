---
id: azt6chzrlzozhqs3xjupdxs
title: '22'
desc: ''
updated: 1784698027981
created: 1784698027981
---

## Context

`sync_to_zotero` (swanki/sync/zotero.py) delivers each chapter's artifacts as a single timestamped zip attached to the parent Zotero item. Its upload leg calls `zot.attachment_simple([...])` from pyzotero 1.11.0, which is **broken here**: it returns a `{'success','failure','unchanged'}` dict reporting failure **without raising** — it fails even a 5-byte file. Commit `d350add` made this *fail loud* (asserts `result.get("success") or result.get("unchanged")` before pruning, so a silent failure no longer lets `_prune_prior_attachments` delete the prior good zips — the observed Kuchel data-loss trap). That guard stops the data loss but does not fix delivery: **nothing can upload at all**.

The low-level Zotero file API works. The 4-step flow (create item → upload-auth → S3 POST → register) was used one-off to repair the pruned Kuchel zips and is verified end-to-end (create 200 → auth 200 → s3 201 → register 204 → md5-queryable) in `scratchpad/zupload.py`. This plan folds that flow into `sync_to_zotero`, replacing `attachment_simple`, so deliveries actually succeed.

This is exactly the follow-up the charter names: `notes/swanki.sync.zotero.md` §2026.07.21 closes with "adopting [the low-level uploader] inside `sync_to_zotero` (replacing the flaky `attachment_simple`) is a sensible follow-up." No overlap with `#52`.

## Relevant Files

| Path | Action | Purpose | Stance |
|------|--------|---------|--------|
| `swanki/sync/zotero.py` | MODIFY | Add module-level `upload_attachment(...)`; collapse the upload block (~L285-312) to one call | Upload block was provisional/documented-to-replace; the rest of `sync_to_zotero` is stable and frozen |
| `tests/test_zotero_upload_guard.py` | MODIFY | Rewrite: `attachment_simple` is gone from the path; drive the uploader via ordered `httpx` side-effects | Migrated |
| `notes/swanki.sync.zotero.md` | MODIFY | Append a dated section documenting this change under the 2026.07.21 charter | Charter note |
| `scratchpad/zupload.py` | REFERENCE | Verified 4-step prototype; source of the folded logic | Throwaway, not shipped |
| `site-packages/pyzotero/_client.py` | REFERENCE | Confirms client attrs reused for the group-lib URL (L77-90) | External dep, unpinned (env 1.11.0) |

## Key Design Decisions

1. **Fold `upload_attachment(...)` as a module-level function inside `swanki/sync/zotero.py`** — no new module, no new dendron note. *Why:* the file already carries the frontmatter + `[[swanki.sync.zotero]]` note + `import httpx` + `from pyzotero import zotero`; a new module means a new note and rename-hook risk for zero benefit. Add only `import hashlib`.

2. **Every upload-flow guard is `raise RuntimeError(...)`, never `assert`.** *Why:* asserts are stripped under `python -O` / `PYTHONOPTIMIZE`; an assert-guarded upload run optimized would silently revive the prune-deletes-good-zips data-loss bug. The precondition asserts at the top of `sync_to_zotero` (`api_key`, `library_id`, `item_key`) are **out of scope and stay**.

3. **Delete the dead d350add assert (~L307).** *Why:* it inspects `result.get("success")` on the `attachment_simple` return dict; once that call is gone the assert dereferences a nonexistent dict and is dead code. `raise` inside the uploader now provides the fail-loud contract it stood for.

4. **Reuse the pyzotero client's already-pluralized attributes for the base URL** — `zot.endpoint` (`https://api.zotero.org`), `zot.library_id`, `zot.library_type` (`"users"`/`"groups"`, pluralized at construction: `_client.py:88` sets `self.library_type = library_type + "s"`), `zot.api_key`. *Why:* the prototype hardcodes `/users/`, so it breaks on group libraries. Do NOT re-read env, do NOT re-append `"s"`, do NOT hardcode `/users/`.

5. **Keep the exact single-request prefix/suffix S3 mode, exact `Content-Type`, and nonzero ms mtime.** *Why:* S3 signs over `auth["contentType"]` — sending anything else ⇒ 403; `mtime` must be `int(st_mtime*1000)` — zero ⇒ 400 "File modification time not provided". Auth body is exactly `{md5, filename, filesize, mtime}` (no `params=1`); register uses `If-None-Match: *` and the `"0" in body["success"]` create-success guard.

6. **Stream the S3 body.** *Why:* `prefix + read() + suffix` materializes a 2x copy (~780 MB peak on a 390 MB zip). Pass `content=iter([prefix.encode(), data, suffix.encode()])` to httpx; md5 is still computed over the full bytes. Keep `httpx.Timeout(600, connect=60)` on the S3 leg — this replaces the deleted `_patched_post` monkeypatch that existed only to widen the timeout.

7. **`Zotero-Write-Token` (random) on the CREATE headers.** *Why:* a retried create without an idempotency token makes a **duplicate** attachment item. Treat `412` (token replay) as a hard `raise`.

8. **`exists` (identical md5 already stored) early-returns the item key.** *Why:* it maps to the old `unchanged` success — delivery is complete, so prune + note + fox-tag STILL run. It short-circuits before S3/register.

9. **Prune-safety is preserved intrinsically.** *Why:* the uploader `raise`s on any failure, so `_prune_prior_attachments` (called only after the upload returns) never runs on a failed upload — same invariant d350add protected, now enforced by control flow instead of a return-value check.

10. **Signature frozen.** `sync_to_zotero(citation_key, output_dir, audio_prefix, content_key="")` is unchanged; the three callers (`pipeline.py:617`, `delivery/targets/zotero.py:45`, `scripts/regen_hamming_bookends_ch1_10.py:145`) are untouched. Everything outside the upload block stays byte-for-byte.

## Approach

**The helper.** Add `upload_attachment(zot: zotero.Zotero, item_key: str, zip_path: Path, zip_name: str) -> str` at module level. It builds `base = f"{zot.endpoint}/{zot.library_type}/{zot.library_id}"` and `headers` from `zot.api_key` (`Zotero-API-Key`, `Zotero-API-Version: 3`), then runs the four steps, raising `RuntimeError` at each on an unexpected status:

Create first fetches the template via `GET {endpoint}/items/new?itemType=attachment&linkMode=imported_file`, fills `parentItem=item_key`, `title=filename=zip_name`, `contentType="application/octet-stream"`, then `item_key_new = body["success"]["0"]`. The four steps at a glance:

```
create   POST {base}/items                     -> 200, body["success"]["0"]   (Zotero-Write-Token; 412 raise)
auth     POST {base}/items/{key}/file           -> 200; exists? -> return key  (form: md5,filename,filesize,mtime)
s3       POST auth[url]  CT=auth[contentType]    -> 200|201                     (streamed prefix+bytes+suffix)
register POST {base}/items/{key}/file           -> 204                          (form: upload=uploadKey)
```

**The block collapse.** In `sync_to_zotero`, replace lines ~285-312 (the `_patched_post` def + `httpx.post` monkeypatch swap + `attachment_simple` call + the d350add assert) with a single `upload_attachment(zot, item_key, zip_path, zip_name)` call, then `uploaded = packed`. The `try/finally` restoring `httpx.post` is deleted with `_patched_post`. Downstream (`_prune_prior_attachments`, `_find_or_create_sync_note`, fox-tag `add_tags`) is unchanged and still guarded by the earlier `return` when `not packed`.

**Test migration.** Rewrite `tests/test_zotero_upload_guard.py`: keep `_prep` patching `zmod.make_zotero_client` and `zmod._find_zotero_item` (so prune/note/tag route through the `MagicMock` zot), but drop `zot.attachment_simple.return_value`. Drive the uploader by monkeypatching `httpx.get`/`httpx.post` with an ordered `side_effect` list of fake responses: template-GET → create-POST `(200, {"success": {"0": "NEWKEY"}})` → auth-POST `(200, {url, contentType, prefix, suffix, uploadKey})` → s3-POST `(201)` → register-POST `(204)`. No respx / pytest-httpx.

## Gotchas

1. **Group-library URL.** Hardcoding `/users/` breaks group libs; build the base from `zot.library_type` (see Decision 4).
2. **Exact S3 `Content-Type` (403).** Overriding `auth["contentType"]` ⇒ `403 SignatureDoesNotMatch`; pass it through verbatim (see Decision 5).
3. **mtime nonzero ms (400).** `int(st_mtime*1000)`; a zero mtime ⇒ `400 "File modification time not provided"` (see Decision 5).
4. **raise, not assert.** Asserts vanish under `python -O`/`PYTHONOPTIMIZE`, silently reviving the prune-deletes-good-zips bug (see Decision 2).
5. **Write-token / 412 duplicate-create.** A create retried without `Zotero-Write-Token` makes a duplicate attachment; hard-`raise` on `412` (see Decision 7).
6. **2x memory on big zips.** `prefix + read() + suffix` peaks ~780 MB on a 390 MB zip; stream via `content=iter([...])` (see Decision 6).
7. **No respx.** The env has no respx/pytest-httpx and `httpx>=0.28`, `pyzotero` unpinned — monkeypatch `httpx.get`/`httpx.post` directly; do not add a dep.
8. **Delete the dead d350add assert.** Once `attachment_simple` is gone, `result.get("success")` raises `AttributeError` (no result dict) — remove it (see Decision 3).
9. **Fold-in keeps one module frontmatter** — add logic to the existing `swanki/sync/zotero.py`; only new import is `hashlib` (see Decision 1).
10. **Land `--no-verify`** (pre-commit pytest has a broken Mac path + mypy baseline); still `/ruff` + `/mypy --strict` the two touched files (`dict[str, str]`, not bare `dict`).

## Verification

- **Migrated guard test** (`tests/test_zotero_upload_guard.py`):
  - success flow → reaches `_prune_prior_attachments` (the two original behavioral assertions re-expressed against the httpx side-effect chain);
  - non-`204` register → `upload_attachment` **raises** AND `zot.delete_item` is NOT called (the data-loss regression guard, now at the HTTP layer);
  - `exists` short-circuit (auth returns `{"exists": true}`) → no S3/register calls, but prune + note + fox-tag still run.
- **Commands:** `/ruff` and `/mypy` on `swanki/sync/zotero.py` + `tests/test_zotero_upload_guard.py`; `pytest tests/test_zotero_*.py` (siblings `test_zotero_prune.py`, `test_zotero_sync_note.py`, `test_zotero_retry.py` are untouched and must stay green).
- **Manual smoke (optional, needs live Zotero):** `sync_to_zotero` one chapter; confirm the md5-backed zip is queryable via `zot.item(key)["data"]["md5"]` and that prune ran (only the newest zip remains on the parent).

## Open Questions

None blocking — the deliberation resolved every fork; we proceed. The one thing to re-confirm at implementation time is the exact shape of the reused pyzotero-1.11.0 client attrs (`zot.endpoint`, `zot.library_type`, `zot.library_id`, `zot.api_key`), which are scout-verified at `_client.py:77-90` for the installed version.
