#!/usr/bin/env bash
#
# scripts/swanki_card_edit.sbatch
# [[scripts.swanki_card_edit]]
# https://github.com/Mjvolk3/Swanki/tree/main/scripts/swanki_card_edit.sbatch
#
# SLURM-native surgical CARD audio edit: one GPU, serverless Fish in-job, apply
# ONE precise chunk edit to ONE card side via scripts/swanki_card_edit.py (->
# swanki.audio.card_edit.edit_card_chunk), tear Fish down. Same Fish bring-up as
# scripts/swanki_audio_edit.sbatch.
#
# Inputs (exported by the caller; sbatch --export=ALL):
#   SWANKI_CARD_MANIFEST  path to card_chunks/{uuid}_manifest.json   (required)
#   SWANKI_CARD_SIDE      front | back                               (default front)
#   SWANKI_CARD_IDX       tts-chunk-local index                      (default 0)
#   SWANKI_CARD_MODE      speech_only | comment | new_text           (default speech_only)
#   SWANKI_CARD_VOICE     models config name                         (default fish_speech_ball)
#   SWANKI_CARD_PAYLOAD   comment text / new_text                    (modes comment|new_text)
#   SWANKI_CARD_MODEL     llm string                                 (comment path only)
#   SWANKI_CARD_ANKI      [sound:...] filename to swap (empty = side mp3 basename); unset = no Anki swap
#
#SBATCH --job-name=swanki-card-edit
#SBATCH --partition=main
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --time=UNLIMITED
#SBATCH --output=/home/michaelvolk/.swanki-queue/logs/slurm-%j.log
set -uo pipefail

manifest="${SWANKI_CARD_MANIFEST:?SWANKI_CARD_MANIFEST unset}"
side="${SWANKI_CARD_SIDE:-front}"
idx="${SWANKI_CARD_IDX:-0}"
mode="${SWANKI_CARD_MODE:-speech_only}"
voice="${SWANKI_CARD_VOICE:-fish_speech_ball}"
payload="${SWANKI_CARD_PAYLOAD:-}"
model="${SWANKI_CARD_MODEL:-}"
anki="${SWANKI_CARD_ANKI-__unset__}"
[ -f "$manifest" ] || { echo "ERROR: manifest not found: $manifest" >&2; exit 2; }

# --- config knobs (mirror swanki_job.sbatch) --------------------------------
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
echo "[swanki-card-edit $job] fish port=$port gpu=${CUDA_VISIBLE_DEVICES:-ambient} manifest=$manifest side=$side idx=$idx mode=$mode"

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

# --- apply the edit ---------------------------------------------------------
edit=(python scripts/swanki_card_edit.py --card-manifest "$manifest" --side "$side"
      --idx "$idx" --voice "$voice")
case "$mode" in
    speech_only) edit+=(--speech-only) ;;
    comment)     edit+=(--comment "$payload"); [ -n "$model" ] && edit+=(--model "$model") ;;
    new_text)    edit+=(--new-text "$payload"); [ -n "$model" ] && edit+=(--model "$model") ;;
    *) echo "ERROR: bad SWANKI_CARD_MODE: $mode" >&2; exit 2 ;;
esac
[ "$anki" != "__unset__" ] && edit+=(--anki "$anki")

echo "[swanki-card-edit $job] ${edit[*]}"
"${edit[@]}" || { echo "ERROR: edit_card_chunk failed" >&2; exit 1; }
echo "[swanki-card-edit $job] DONE"
