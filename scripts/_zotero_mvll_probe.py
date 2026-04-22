"""
scripts/_zotero_mvll_probe.py

Find MV-LL group library and list items in Lo-Thesis-Papers collection.
One-off probe; safe to delete.
"""

import os
import re
import sys

import requests
from dotenv import load_dotenv
from pyzotero import zotero

load_dotenv("/home/michaelvolk/Documents/projects/Swanki/.env")

api_key = os.environ["ZOTERO_API_KEY"]
user_id = os.environ["ZOTERO_LIBRARY_ID"]

headers = {"Zotero-API-Key": api_key}
resp = requests.get(
    f"https://api.zotero.org/users/{user_id}/groups", headers=headers, timeout=30
)
resp.raise_for_status()
groups = resp.json()

print("Groups available:")
for g in groups:
    print(f"  id={g['id']} name={g['data']['name']}")

target = None
for g in groups:
    nm = g["data"]["name"].strip()
    if nm.upper().replace(" ", "").replace("_", "-") in {"MV-LL", "MVLL"}:
        target = g
        break
if not target:
    for g in groups:
        nm = g["data"]["name"]
        if "MV" in nm and "LL" in nm:
            target = g
            break

if not target:
    print("MV-LL group not found", file=sys.stderr)
    sys.exit(1)

group_id = target["id"]
print(f"\nMV-LL group id: {group_id}  name: {target['data']['name']}")

zot = zotero.Zotero(group_id, "group", api_key)
collections = zot.collections()
print("\nCollections:")
for c in collections:
    print(f"  key={c['key']} name={c['data']['name']}")

coll = None
for c in collections:
    if c["data"]["name"].strip().lower() == "lo-thesis-papers":
        coll = c
        break
if not coll:
    for c in collections:
        nm = c["data"]["name"].lower()
        if "lo" in nm and "thesis" in nm:
            coll = c
            break

if not coll:
    print("Lo-Thesis-Papers collection not found", file=sys.stderr)
    sys.exit(1)

coll_key = coll["key"]
print(f"\nLo-Thesis-Papers collection key: {coll_key}  name: {coll['data']['name']}")

items = zot.everything(zot.collection_items(coll_key))
parents = [
    it for it in items if it["data"].get("itemType") not in {"attachment", "note"}
]

print(f"\nItems ({len(parents)}):")
ck_re = re.compile(r"Citation Key:\s*(\S+)")
for idx, it in enumerate(parents, 1):
    data = it["data"]
    title = data.get("title", "<no title>")
    ck = data.get("citationKey")
    if not ck:
        extra = data.get("extra", "") or ""
        m = ck_re.search(extra)
        ck = m.group(1) if m else "<none>"
    print(f"  {idx}. {ck} -- {title}")
