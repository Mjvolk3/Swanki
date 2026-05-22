#!/usr/bin/env bash
# scripts/setup-mineru-env.sh
# [[scripts.setup-mineru-env]]
#
# Create (or update) the isolated `swanki-mineru` conda env for MinerU OCR and
# prepare the HF model cache. Idempotent. MinerU models download lazily on the
# first do_parse; pass --warm to force a warmup run is NOT implemented here to
# avoid needing a sample PDF -- the first real pipeline run warms the cache.
set -euo pipefail

ENV_NAME="swanki-mineru"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REQ_FILE="${REPO_ROOT}/env/swanki-mineru-requirements.txt"

if [[ -z "${SWANKI_DATA:-}" ]]; then
  echo "ERROR: SWANKI_DATA is not set; source your .env first." >&2
  exit 1
fi

# Resolve a conda/mamba frontend.
if command -v mamba >/dev/null 2>&1; then
  CONDA="mamba"
elif command -v conda >/dev/null 2>&1; then
  CONDA="conda"
else
  echo "ERROR: neither mamba nor conda found on PATH." >&2
  exit 1
fi

if "${CONDA}" env list | grep -qE "^${ENV_NAME}\s"; then
  echo "Env '${ENV_NAME}' already exists; updating deps."
else
  echo "Creating env '${ENV_NAME}' (python=3.11)."
  "${CONDA}" create -y -n "${ENV_NAME}" python=3.11
fi

"${CONDA}" run -n "${ENV_NAME}" pip install -r "${REQ_FILE}"

HF_CACHE="${SWANKI_DATA}/models/mineru/hf_cache"
mkdir -p "${HF_CACHE}"
echo "HF cache dir ready: ${HF_CACHE}"

echo
echo "Next steps:"
echo "  1. Free a GPU for MinerU:   bash scripts/free-gpu-for-mineru.sh"
echo "  2. Run a paper with MinerU: swanki ... models.ocr.provider=mineru"
echo "     (first run downloads ~6-10 GB of MinerU models into the HF cache)"
