#!/bin/bash
# scripts/push_campagne_lecture_fix.sh
# [[scripts.push_campagne_lecture_fix]]
# https://github.com/Mjvolk3/Swanki/tree/main/scripts/push_campagne_lecture_fix.sh
#
# One-off: regenerate campagne2021 lecture chunks 10+14 with the Unicode
# punctuation fix, then propagate to Zotero (source of truth) and ABS.
#
# Pipeline:
#   1. re-TTS chunks 10, 14 + restitch lecture mp3
#   2. upload Zotero attachment zip (apkg + 3 audio files)
#   3. clear old mp3s under each paper's ABS folder (lecture/summary/reading)
#   4. abs_refresh — pulls new zip, extracts, forces library scan

set -euo pipefail

cd /home/michaelvolk/Documents/projects/Swanki
source ~/miniconda3/etc/profile.d/conda.sh
conda activate swanki
set -a; source .env; set +a

# campagne lives in the mv-ll group library (Lo-Thesis), not the personal
# user library .env points at by default.
export ZOTERO_LIBRARY_ID=6063346
export ZOTERO_LIBRARY_TYPE=group

echo "=== 1/4: re-TTS chunks 10, 14 + restitch ==="
python scripts/regen_campagne_lecture_chunks.py

echo ""
echo "=== 2/4: upload zip to Zotero ==="
python <<'PY'
from pathlib import Path
from pyzotero import _client as _pyz
_pyz.DEFAULT_TIMEOUT = 180
from swanki.sync.zotero import sync_to_zotero

CIT = "campagneClinicalPharmacokineticsPharmacodynamics2021"
OUT = Path(f"/scratch/projects/torchcell-scratch/Swanki_Data/{CIT}")
sync_to_zotero(citation_key=CIT, output_dir=OUT, audio_prefix=CIT)
PY

echo ""
echo "=== 3/4: clear existing mp3s under ABS campagne folders ==="
ABS_ROOT="/home/michaelvolk/Documents/projects/Swanki_ABS/mv-ll"
for rel in \
    "Swanki-Paper-Lecture/campagneClinicalPharmacokineticsPharmacodynamics2021" \
    "Swanki-Paper-Summary/campagneClinicalPharmacokineticsPharmacodynamics2021" \
    "Swanki-Paper-Reading/campagneClinicalPharmacokineticsPharmacodynamics2021"; do
    dir="${ABS_ROOT}/${rel}"
    if [ -d "$dir" ]; then
        echo "  clearing $dir"
        find "$dir" -maxdepth 1 -type f -name '*.mp3' -delete
    fi
done

echo ""
echo "=== 4/4: abs_refresh ==="
bash /home/michaelvolk/Documents/projects/Swanki/scripts/abs_refresh.sh

echo ""
echo "done — Prologue will pick up the fixed campagne lecture on next sync."
