#!/usr/bin/env bash
#
# scripts/run_lo_thesis_batch.sh
# [[scripts.run_lo_thesis_batch]]
# https://github.com/Mjvolk3/Swanki/tree/main/scripts/run_lo_thesis_batch.sh
#
# Batch-run swanki on the 27 Lo-Thesis papers with the Audrey Hepburn voice.
# Each run generates cards + complementary audio + summary/reading/lecture audio,
# then uploads a timestamped zip to the mv-ll Zotero group library (6063346)
# and tags the parent Zotero item with 🦊. The cron-driven abs_refresh picks
# up the tagged items within 5 min and routes audio into the mv-ll: Paper
# libraries.
#
# Run from this shell:
#     conda activate swanki
#     script -qc "bash $(realpath $0)" /dev/null
#
# The `script` wrapper satisfies Mathpix CLI's TTY requirement (see CLAUDE.md).
#
# Per-paper stdout/stderr is teed to ~/.cache/swanki-lo-thesis/<key>.log so a
# single failure doesn't lose progress context.

set -uo pipefail

# Load .env so SWANKI_DATA (and Zotero creds) propagate into this shell.
SWANKI_REPO="$HOME/Documents/projects/Swanki"
if [ -f "$SWANKI_REPO/.env" ]; then
    set -a; source "$SWANKI_REPO/.env"; set +a
fi

PAPERS="${LO_THESIS_KEYS:-/tmp/lo_thesis_keys.txt}"
DATA="${SWANKI_DATA:-/scratch/projects/torchcell-scratch/Swanki_Data}"
LOG_DIR="$HOME/.cache/swanki-lo-thesis"

# Target the mv-ll group library for uploads.
export ZOTERO_LIBRARY_ID=6063346
export ZOTERO_LIBRARY_TYPE=group

mkdir -p "$LOG_DIR"
cd "$HOME/Documents/projects/Swanki"

if ! command -v swanki >/dev/null 2>&1; then
    echo "ERROR: 'swanki' not on PATH — run 'conda activate swanki' first" >&2
    exit 1
fi

if [ ! -f "$PAPERS" ]; then
    echo "ERROR: keys file not found: $PAPERS" >&2
    exit 1
fi

total=$(grep -cve '^\s*$' "$PAPERS")
i=0
successes=0
failures=()

while IFS= read -r key; do
    # Skip blank/whitespace lines
    key="${key//$'\r'/}"
    [ -z "${key// }" ] && continue
    i=$((i + 1))

    echo
    echo "============================================================"
    echo "[$i/$total] $key"
    echo "============================================================"

    pdf="$DATA/$key/${key}_clean.pdf"
    [ -f "$pdf" ] || pdf="$DATA/$key/${key}.pdf"
    if [ ! -f "$pdf" ]; then
        echo "  MISSING PDF — skipping"
        failures+=("$key (missing pdf)")
        continue
    fi

    log="$LOG_DIR/${key}.log"
    echo "  logging → $log"
    # -e propagates child exit; -q silent; pty keeps Mathpix CLI happy.
    # script writes the session to $log AND echoes to this terminal in real time.
    # Nested output: each run lives at {SWANKI_DATA}/{key}/{key}[_N]/ so
    # source PDFs + all iteration runs stay grouped under one parent dir.
    if script -q -e -c "swanki \
            pdf_path='$pdf' \
            citation_key='$key' \
            +output_dir='$key/$key' \
            audio=all \
            anki=default \
            zotero=sync \
            models=fish_speech_audrey \
            pipeline.processing.confirm_before_generation=false" "$log" < /dev/null; then
        successes=$((successes + 1))
        echo "  ✓ done"
    else
        rc=$?
        failures+=("$key (exit $rc)")
        echo "  ✗ failed (exit $rc)"
    fi
done < "$PAPERS"

echo
echo "============================================================"
echo "batch complete: $successes/$total successful"
if [ ${#failures[@]} -gt 0 ]; then
    echo "failures:"
    printf '  - %s\n' "${failures[@]}"
fi
echo "per-paper logs: $LOG_DIR/"
echo "Zotero uploads target: group $ZOTERO_LIBRARY_ID"
echo "ABS pickup: automatic via cron abs_refresh (≤5 min)"
