#!/usr/bin/env bash
#
# scripts/lo_thesis_retro_publish.sh
#
# Retro-sync Lo-Thesis papers to Zotero for runs that completed before
# zotero=sync was added to run_lo_thesis_batch.sh. Finds the latest scratch
# dir per citekey (one containing a .apkg) and calls sync_to_zotero targeted
# at the mv-ll group library. Idempotent to re-run — new zips accumulate
# timestamped.
#
# Usage:
#     bash scripts/lo_thesis_retro_publish.sh [keys_file]
# Defaults to /tmp/lo_thesis_keys.txt. One citekey per line.

set -uo pipefail

cd "$(dirname "$0")/.."
source ~/miniconda3/etc/profile.d/conda.sh
conda activate swanki
set -a; source .env; set +a

export ZOTERO_LIBRARY_ID=6063346
export ZOTERO_LIBRARY_TYPE=group

keys_file="${1:-/tmp/lo_thesis_keys.txt}"

python - "$keys_file" <<'PY'
import sys
from pathlib import Path

from pyzotero import _client as _pyz
_pyz.DEFAULT_TIMEOUT = 180
from swanki.sync.zotero import sync_to_zotero

keys = [k.strip() for k in Path(sys.argv[1]).read_text().splitlines() if k.strip()]
SCRATCH = Path("/scratch/projects/torchcell-scratch/Swanki_Data")

ok = 0
skipped = []
failed = []
for key in keys:
    # Runs are nested under SCRATCH/<key>/<key>[_N]/ in the current layout.
    # Fall back to legacy flat SCRATCH/<key>[_N]/ for older batches.
    nested = list((SCRATCH / key).glob(f"{key}*")) if (SCRATCH / key).exists() else []
    flat = list(SCRATCH.glob(f"{key}_*"))
    candidates = sorted(
        [p for p in nested + flat if p.is_dir()],
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    complete = [c for c in candidates if list(c.glob("*.apkg"))]
    if not complete:
        skipped.append(key)
        print(f"SKIP {key}: no completed scratch dir (.apkg missing)")
        continue
    latest = complete[0]
    print(f"\n=== {key}")
    print(f"    dir: {latest}")
    try:
        sync_to_zotero(citation_key=key, output_dir=latest, audio_prefix=key)
        ok += 1
    except Exception as e:
        failed.append((key, str(e)))
        print(f"    FAILED: {e}")

print(f"\n=== summary: {ok}/{len(keys)} synced")
if skipped:
    print(f"skipped (no outputs yet): {len(skipped)}")
    for k in skipped:
        print(f"  - {k}")
if failed:
    print(f"failed: {len(failed)}")
    for k, err in failed:
        print(f"  - {k}: {err}")
PY

echo
echo "=== running abs_refresh to pull into mv-ll ==="
bash ~/Documents/projects/Swanki/scripts/abs_refresh.sh
