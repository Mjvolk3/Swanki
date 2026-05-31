#!/usr/bin/env bash
#
# scripts/swanki_sync.sh
# [[scripts.swanki_sync]]
# https://github.com/Mjvolk3/Swanki/tree/main/scripts/swanki_sync.sh
#
# One-shot "sync to swanki servers" shortcut. Reads Zotero (the source of
# truth) and pushes the latest artifacts to the user's self-hosted servers:
#
#   1. ABS audio refresh -- bash scripts/abs_refresh.sh (existing, gated
#      per-projection by ``push_audio:`` in projections.yml).
#   2. Anki deck push    -- python scripts/swanki_anki_sync.py "$@"
#      (importPackage per latest apkg, then a single AnkiWeb sync).
#
# Args are forwarded to swanki_anki_sync.py (``--projection NAME``,
# ``--dry-run``, positional projections path). ``--dry-run`` also short-
# circuits the abs_refresh step since the audio path has no dry mode.
#
# Prereq: headless Anki + AnkiConnect on this host (notes/anki.headless-sync.md).

set -euo pipefail

SWANKI_DIR="$(git -C "$(dirname "$(readlink -f "$0")")" rev-parse --show-toplevel)"
cd "$SWANKI_DIR"

source ~/miniconda3/etc/profile.d/conda.sh
conda activate swanki
set -a
# shellcheck disable=SC1091
source .env
set +a

case " $* " in
    *' --dry-run '*) dry_run=true ;;
    *) dry_run=false ;;
esac

if [ "$dry_run" = true ]; then
    echo "[dry-run] would run scripts/abs_refresh.sh"
else
    echo "=== ABS audio refresh ==="
    bash "$SWANKI_DIR/scripts/abs_refresh.sh"
fi

echo
echo "=== Anki deck push ==="
python "$SWANKI_DIR/scripts/swanki_anki_sync.py" "$@"
