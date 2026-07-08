#!/usr/bin/env bash
#
# scripts/swanki_replace_card.sbatch
# [[scripts.swanki_replace_card]]
# https://github.com/Mjvolk3/Swanki/tree/main/scripts/swanki_replace_card.sbatch
#
# SLURM-native surgical CARD replacement: one GPU, serverless Fish in-job, swap
# ONE card wholesale (new front + back text, BOTH audio sides re-TTSed) via
# scripts/swanki_replace_card.py (-> swanki.audio.card_replace.replace_card),
# then tear Fish down. Same Fish bring-up as scripts/swanki_card_edit.sbatch.
#
# Inputs (exported by the caller; sbatch --export=ALL):
#   SWANKI_CARD_MANIFEST  path to card_chunks/{uuid}_manifest.json   (required)
#   SWANKI_CARD_CITEKEY   citation key for the front prefix          (required)
#   SWANKI_CARD_FRONT     new front prose (no @citation prefix)      (required)
#   SWANKI_CARD_BACK      new back prose                             (required)
#   SWANKI_CARD_VOICE     models config name                         (default fish_speech)
#   SWANKI_CARD_NOTEID    numeric note-id override                   (optional)
#   SWANKI_CARD_ANKI      set (any value) to patch the collection; unset = dry-run
#   SWANKI_CARD_NOSYNC    set (any value) to skip the final AnkiWeb sync
#
#SBATCH --job-name=swanki-replace-card
#SBATCH --partition=main
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --time=UNLIMITED
#SBATCH --output=/home/michaelvolk/.swanki-queue/logs/slurm-%j.log
set -uo pipefail

manifest="${SWANKI_CARD_MANIFEST:?SWANKI_CARD_MANIFEST unset}"
citekey="${SWANKI_CARD_CITEKEY:?SWANKI_CARD_CITEKEY unset}"
front="${SWANKI_CARD_FRONT:?SWANKI_CARD_FRONT unset}"
back="${SWANKI_CARD_BACK:?SWANKI_CARD_BACK unset}"
voice="${SWANKI_CARD_VOICE:-fish_speech}"
noteid="${SWANKI_CARD_NOTEID:-}"
anki="${SWANKI_CARD_ANKI-__unset__}"
nosync="${SWANKI_CARD_NOSYNC-__unset__}"
[ -f "$manifest" ] || { echo "ERROR: manifest not found: $manifest" >&2; exit 2; }

# --- config knobs (mirror swanki_card_edit.sbatch) --------------------------
REPO="${SWANKI_REPO:-$HOME/Documents/projects/Swanki}"
CONDA_SH="${SWANKI_CONDA_SH:-$HOME/miniconda3/etc/profile.d/conda.sh}"
FISH_SIF="${SWANKI_FISH_SIF:-$HOME/Documents/projects/fish-speech/fish-speech-server.sif}"
FISH_REPO="${SWANKI_FISH_REPO:-$HOME/Documents/projects/fish-speech}"
PORT_BASE="${SWANKI_FISH_PORT_BASE:-8100}"
PORT_RANGE="${SWANKI_FISH_PORT_RANGE:-400}"
COMPILE="${SWANKI_FISH_COMPILE:-0}"
job="${SLURM_JOB_ID:-$$}"

# --- derive a free host port ------------------------------------------------
port=$(( PORT_BASE + job % PORT_RANGE ))
while ss -ltnH "( sport = :$port )" 2>/dev/null | grep -q ":$port"; do
    port=$(( port + 1 ))
done
echo "[swanki-replace-card $job] fish port=$port gpu=${CUDA_VISIBLE_DEVICES:-ambient} manifest=$manifest"

# --- bring up serverless Fish on the allocated GPU (cgroup child) ------------
tmpfs_flag=()
[ "${SWANKI_FISH_WRITABLE:-1}" = "1" ] && tmpfs_flag=(--writable-tmpfs)
apptainer exec --nv "${tmpfs_flag[@]}" --pwd /app \
    --bind "$FISH_REPO/checkpoints:/app/checkpoints,$FISH_REPO/references:/app/references" \
    --env "COMPILE=$COMPILE" \
    "$FISH_SIF" \
    "${SWANKI_FISH_PYTHON:-/app/.venv/bin/python}" tools/api_server.py --listen "0.0.0.0:$port" \
        --llama-checkpoint-path checkpoints/s2-pro \
        --decoder-checkpoint-path checkpoints/s2-pro/codec.pth \
        --decoder-config-name modded_dac_vq &
fish_pid=$!
trap 'kill "$fish_pid" 2>/dev/null' EXIT TERM INT

ready=0
for _ in $(seq 1 "${SWANKI_FISH_HEALTH_TIMEOUT:-300}"); do
    if curl -sf -m 3 "http://127.0.0.1:$port/v1/health" >/dev/null 2>&1; then
        ready=1; break
    fi
    sleep 1
done
[ "$ready" = 1 ] || { echo "ERROR: Fish did not become healthy on :$port" >&2; exit 1; }
export SWANKI_FISH_PORTS="$port"

# --- activate native conda env ----------------------------------------------
set +u
# shellcheck disable=SC1090
source "$CONDA_SH"
conda activate swanki
set -u
cd "$REPO" || { echo "ERROR: cannot cd $REPO" >&2; exit 1; }

# --- replace the card -------------------------------------------------------
run=(python scripts/swanki_replace_card.py --card-manifest "$manifest"
     --citation-key "$citekey" --new-front "$front" --new-back "$back" --voice "$voice")
[ -n "$noteid" ] && run+=(--note-id "$noteid")
[ "$anki" != "__unset__" ] && run+=(--anki)
[ "$nosync" != "__unset__" ] && run+=(--no-sync)

echo "[swanki-replace-card $job] ${run[*]}"
"${run[@]}" || { echo "ERROR: replace_card failed" >&2; exit 1; }
echo "[swanki-replace-card $job] DONE"
