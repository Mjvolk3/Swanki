#!/usr/bin/env bash
#
# scripts/regen_juuti.sh
#
# Re-run juuti-uusitaloAquaporinExpressionFunction2013 after its first pass
# failed on a transient Mathpix cropped-image URL (HTTP 400). Uses the full
# Lo-Thesis config (audio=all, audrey voice, mv-ll group Zotero upload).
# With the patched _find_zotero_item in place, the Zotero upload will succeed.
#
# Run from this shell:
#     conda activate swanki
#     bash scripts/regen_juuti.sh

set -uo pipefail

KEY=juuti-uusitaloAquaporinExpressionFunction2013
TMP_KEYS=/tmp/juuti_only.txt

echo "$KEY" > "$TMP_KEYS"

LO_THESIS_KEYS="$TMP_KEYS" bash "$(dirname "$0")/run_lo_thesis_batch.sh"
