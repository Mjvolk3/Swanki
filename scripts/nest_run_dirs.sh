#!/usr/bin/env bash
#
# scripts/nest_run_dirs.sh
#
# Move flat `{SWANKI_DATA}/{citekey}_N/` sibling run dirs into the nested
# `{SWANKI_DATA}/{citekey}/{citekey}_N/` layout used by earlier papers
# (zvyagin, thornburg). Keeps source PDFs and all run outputs together
# per citekey so partial regens + iteration are tracked in one place.
#
# Usage:
#     bash scripts/nest_run_dirs.sh [keys_file]
# Defaults to the trimmed current keys list; pass an explicit file for
# other batches. One citekey per line.

set -uo pipefail

ROOT="${SWANKI_DATA:-/scratch/projects/torchcell-scratch/Swanki_Data}"
KEYS_FILE="${1:-/tmp/lo_thesis_keys_all.txt}"

if [ ! -f "$KEYS_FILE" ]; then
    echo "ERROR: keys file not found: $KEYS_FILE" >&2
    exit 1
fi

moved=0
skipped=0
shopt -s nullglob

while IFS= read -r key; do
    key="${key//$'\r'/}"
    [ -z "${key// }" ] && continue

    parent="$ROOT/$key"
    if [ ! -d "$parent" ]; then
        echo "SKIP  $key (no parent dir: $parent)"
        skipped=$((skipped + 1))
        continue
    fi

    for rundir in "$ROOT/${key}_"*; do
        [ -d "$rundir" ] || continue
        name="$(basename "$rundir")"
        dest="$parent/$name"
        if [ -e "$dest" ]; then
            echo "SKIP  $name (already at $dest)"
            skipped=$((skipped + 1))
            continue
        fi
        echo "MOVE  $rundir -> $dest"
        mv "$rundir" "$dest"
        moved=$((moved + 1))
    done
done < "$KEYS_FILE"

shopt -u nullglob

echo
echo "=== summary: moved=$moved skipped=$skipped ==="
