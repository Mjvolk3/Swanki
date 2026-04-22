#!/bin/bash
# One-shot: publish the already-generated thornburg (v2) and zvyagin (v6) audio
# via Zotero (source of truth) → ABS refresh. Skips regeneration.
#
# Renames the versioned output files to the canonical "{prefix}-{kind}-audio.mp3"
# names that sync_to_zotero expects, then uploads each item's zip and triggers
# an ABS refresh so Prologue sees the new tracks.

set -euo pipefail

cd /home/michaelvolk/Documents/projects/Swanki
source ~/miniconda3/etc/profile.d/conda.sh
conda activate swanki
set -a; source .env; set +a

python <<'PY'
import shutil
from pathlib import Path

# Bump pyzotero's default read timeout before it's captured by closures.
from pyzotero import _client as _pyz
_pyz.DEFAULT_TIMEOUT = 180

from swanki.sync.zotero import sync_to_zotero

JOBS = [
    # (scratch_dir, citation_key, audio_prefix, version_suffix)
    (
        "/scratch/projects/torchcell-scratch/Swanki_Data/zvyaginGenSLMsGenomescaleLanguage2023/zvyaginGenSLMsGenomescaleLanguage2023",
        "zvyaginGenSLMsGenomescaleLanguage2023",
        "zvyaginGenSLMsGenomescaleLanguage2023",
        "_v6",
    ),
    (
        "/scratch/projects/torchcell-scratch/Swanki_Data/thornburgBringingGeneticallyMinimal2026/thornburgBringingGeneticallyMinimal2026-fish_2",
        "thornburgBringingGeneticallyMinimal2026",
        "thornburgBringingGeneticallyMinimal2026-fish",
        "_v2",
    ),
]

for scratch_dir, cit, prefix, suffix in JOBS:
    out = Path(scratch_dir)
    for kind in ("summary", "lecture"):
        src = out / f"{cit}-{kind}-audio{suffix}.mp3"
        dst = out / f"{prefix}-{kind}-audio.mp3"
        if not src.exists():
            print(f"skip {cit} {kind}: {src.name} not found")
            continue
        print(f"copy {src.name} -> {dst.name}")
        shutil.copy2(src, dst)
    print(f"uploading zip for {cit} ...")
    sync_to_zotero(citation_key=cit, output_dir=out, audio_prefix=prefix)
    print(f"uploaded {cit}")

print("all items uploaded to Zotero")
PY

echo ""
echo "Refreshing ABS (Zotero → ABS → library scan)..."
bash /home/michaelvolk/Documents/projects/Swanki/scripts/abs_refresh.sh
echo "done — Prologue should see the new tracks after its next sync."
