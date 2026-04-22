#!/usr/bin/env bash
#
# scripts/abs_refresh.sh
# [[scripts.abs_refresh]]
# https://github.com/Mjvolk3/Swanki/tree/main/scripts/abs_refresh.sh
#
# End-to-end refresh of ABS state from Zotero. Idempotent; safe to run on a
# tight schedule (cron/systemd timer). A flock keeps overlapping runs from
# clobbering each other when a prior run is still mid-download.
#
# Pipeline:
#   1. swanki_abs_sync.py            — pull new mp3s from Zotero zips
#   2. abs_sync_zotero_collections.py — mirror Zotero collections → ABS collections
#   3. abs_enrich_metadata.py        — author + covers for new items
#   4. abs_clean_stale_chapters.py   — drop chapters that reference deleted files
#   5. POST /api/libraries/:id/scan  — force ABS to pick up new files

set -euo pipefail

LOCKFILE=/tmp/abs-refresh.lock
exec 200>"$LOCKFILE"
if ! flock -n 200; then
    echo "[$(date '+%Y-%m-%dT%H:%M:%S%z')] another abs_refresh in progress — skipping" >&2
    exit 0
fi

export ABS_API_TOKEN_FILE="${ABS_API_TOKEN_FILE:-$HOME/Documents/projects/infra/abs/.api-token}"
PY="${ABS_REFRESH_PY:-$HOME/miniconda3/envs/swanki/bin/python}"
SWANKI_DIR="${ABS_REFRESH_SWANKI_DIR:-$HOME/Documents/projects/Swanki}"
ABS_URL="${ABS_URL:-https://abs.michaelvolk.dev}"

cd "$SWANKI_DIR"

log() {
    echo "[$(date '+%Y-%m-%dT%H:%M:%S%z')] $*"
}

log "=== abs_refresh start ==="

log "step 1/6 — swanki_abs_sync"
"$PY" scripts/swanki_abs_sync.py

log "step 2/6 — abs_setup_libraries (idempotent)"
"$PY" scripts/abs_setup_libraries.py

log "step 3/6 — abs_sync_zotero_collections"
"$PY" scripts/abs_sync_zotero_collections.py

log "step 4/6 — abs_enrich_metadata"
"$PY" scripts/abs_enrich_metadata.py

log "step 5/6 — abs_clean_stale_chapters"
"$PY" scripts/abs_clean_stale_chapters.py

log "step 6/6 — scan libraries"
TOKEN=$(cat "$ABS_API_TOKEN_FILE")
for lib_id in $(curl -s -H "Authorization: Bearer $TOKEN" -H "User-Agent: swanki-abs-setup/1.0" \
                  "$ABS_URL/api/libraries" | jq -r '.libraries[].id'); do
    curl -s -X POST -H "Authorization: Bearer $TOKEN" -H "User-Agent: swanki-abs-setup/1.0" \
         "$ABS_URL/api/libraries/$lib_id/scan" > /dev/null
    log "  scanned $lib_id"
done

log "=== abs_refresh done ==="
