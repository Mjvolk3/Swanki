#!/bin/bash
# Fix the duplicate-lecture defect on thornburg + zvyagin:
#   1. Re-TTS from hand-cleaned transcripts (no LLM call) → new mp3 at canonical name.
#   2. Upload to Zotero as new timestamped attachment (source of truth).
#   3. Delete ALL existing mp3s under each paper's ABS folder so Prologue shows
#      only one track after sync.
#   4. abs_refresh pulls the latest zip and forces a library scan.

set -euo pipefail

cd /home/michaelvolk/Documents/projects/Swanki
source ~/miniconda3/etc/profile.d/conda.sh
conda activate swanki
set -a; source .env; set +a

echo "=== 1/4: re-TTS from cleaned transcripts ==="
python scripts/retts_cleaned_transcripts.py

echo ""
echo "=== 2/4: upload zips to Zotero ==="
python <<'PY'
from pathlib import Path
from pyzotero import _client as _pyz
_pyz.DEFAULT_TIMEOUT = 180
from swanki.sync.zotero import sync_to_zotero

JOBS = [
    (
        "/scratch/projects/torchcell-scratch/Swanki_Data/thornburgBringingGeneticallyMinimal2026/thornburgBringingGeneticallyMinimal2026-fish_2",
        "thornburgBringingGeneticallyMinimal2026",
        "thornburgBringingGeneticallyMinimal2026-fish",
    ),
    (
        "/scratch/projects/torchcell-scratch/Swanki_Data/zvyaginGenSLMsGenomescaleLanguage2023/zvyaginGenSLMsGenomescaleLanguage2023",
        "zvyaginGenSLMsGenomescaleLanguage2023",
        "zvyaginGenSLMsGenomescaleLanguage2023",
    ),
]
for out, cit, prefix in JOBS:
    print(f"uploading {cit} ...")
    sync_to_zotero(citation_key=cit, output_dir=Path(out), audio_prefix=prefix)
print("uploads done")
PY

echo ""
echo "=== 3/4: clear existing mp3s under each paper's ABS folder ==="
ABS_ROOT="/home/michaelvolk/Documents/projects/Swanki_ABS/michaelvolk"
for rel in \
    "Swanki-Paper-Lecture/thornburgBringingGeneticallyMinimal2026" \
    "Swanki-Paper-Summary/thornburgBringingGeneticallyMinimal2026" \
    "Swanki-Paper-Reading/thornburgBringingGeneticallyMinimal2026" \
    "Swanki-Paper-Lecture/zvyaginGenSLMsGenomescaleLanguage2023" \
    "Swanki-Paper-Summary/zvyaginGenSLMsGenomescaleLanguage2023" \
    "Swanki-Paper-Reading/zvyaginGenSLMsGenomescaleLanguage2023"; do
    dir="${ABS_ROOT}/${rel}"
    if [ -d "$dir" ]; then
        echo "  clearing $dir"
        find "$dir" -maxdepth 1 -type f -name '*.mp3' -delete
    fi
done

echo ""
echo "=== 4/4: abs_refresh (Zotero → ABS → scan) ==="
bash /home/michaelvolk/Documents/projects/Swanki/scripts/abs_refresh.sh

echo ""
echo "done — Prologue will now show a single lecture track per paper after its next sync."
