#!/usr/bin/env bash
#
# scripts/swanki_finalize_abs.sbatch
# [[scripts.swanki_finalize_abs]]
# https://github.com/Mjvolk3/Swanki/tree/main/scripts/swanki_finalize_abs.sbatch
#
# Debounced ABS refresh as a SLURM singleton job. Each swanki_job.sbatch touches
# an abs-dirty flag after delivering Anki; submit this with
# `--dependency=singleton --job-name=swanki-abs` so only ONE ABS refresh ever
# runs at a time, after the batch settles -- the SLURM-native replacement for the
# old drainer's busy->idle finalize_abs edge. Needs no GPU.
#
#SBATCH --job-name=swanki-abs
#SBATCH --partition=main
#SBATCH --cpus-per-task=2
#SBATCH --mem=4G
#SBATCH --time=01:00:00
#SBATCH --dependency=singleton
#SBATCH --output=slurm-abs-%j.log
set -uo pipefail

REPO="${SWANKI_REPO:-$HOME/Documents/projects/Swanki}"
CONDA_SH="${SWANKI_CONDA_SH:-$HOME/miniconda3/etc/profile.d/conda.sh}"
QUEUE_DIR="${SWANKI_QUEUE_DIR:-$HOME/.swanki-queue}"
ABS_DIRTY="${SWANKI_ABS_DIRTY:-$QUEUE_DIR/abs-dirty}"

[ -f "$ABS_DIRTY" ] || { echo "abs-dirty absent — nothing to refresh"; exit 0; }

set +u
# shellcheck disable=SC1090
source "$CONDA_SH"
conda activate swanki
set -u
cd "$REPO" || { echo "ERROR: cannot cd $REPO" >&2; exit 1; }

python -m swanki.delivery finalize-abs \
    && rm -f "$ABS_DIRTY" \
    && echo "FINALIZE-ABS done" \
    || { echo "FINALIZE-ABS failed — abs-dirty retained" >&2; exit 1; }
