#!/usr/bin/env bash
#
# scripts/regen_card_audio_side.sbatch
# [[scripts.regen_card_audio_side]]
# https://github.com/Mjvolk3/Swanki/tree/main/scripts/regen_card_audio_side.sbatch
#
# SLURM-native surgical single-card-side audio regen: one GPU, serverless Fish
# in-job, re-TTS one card side via scripts/regen_card_audio_side.py, tear Fish
# down. Same Fish bring-up as scripts/swanki_audio_edit.sbatch.
#
# Inputs (exported by the caller; sbatch --export=ALL):
#   SWANKI_REGEN_OUTDIR    pipeline output dir holding the card audio  (required)
#   SWANKI_REGEN_UUID      card uuid                                   (required)
#   SWANKI_REGEN_SIDE      front | back                               (default front)
#   SWANKI_REGEN_CONTENTKEY content_key (locates *_citation.mp3)       (required)
#   SWANKI_REGEN_VOICE     models config name                         (default fish_speech_ball)
#   SWANKI_REGEN_SPEED     render speed; match original gen           (default 1.6)
#
#SBATCH --job-name=swanki-regen-card
#SBATCH --partition=main
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --time=UNLIMITED
#SBATCH --output=/home/michaelvolk/.swanki-queue/logs/slurm-%j.log
set -uo pipefail

outdir="${SWANKI_REGEN_OUTDIR:?SWANKI_REGEN_OUTDIR unset}"
uuid="${SWANKI_REGEN_UUID:?SWANKI_REGEN_UUID unset}"
side="${SWANKI_REGEN_SIDE:-front}"
ck="${SWANKI_REGEN_CONTENTKEY:?SWANKI_REGEN_CONTENTKEY unset}"
voice="${SWANKI_REGEN_VOICE:-fish_speech_ball}"
speed="${SWANKI_REGEN_SPEED:-1.6}"
[ -d "$outdir" ] || { echo "ERROR: outdir not found: $outdir" >&2; exit 2; }

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
echo "[regen-card $job] fish port=$port gpu=${CUDA_VISIBLE_DEVICES:-ambient} uuid=$uuid side=$side"

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

# --- activate native conda env + regen --------------------------------------
set +u
# shellcheck disable=SC1090
source "$CONDA_SH"
conda activate swanki
set -u
cd "$REPO" || { echo "ERROR: cannot cd $REPO" >&2; exit 1; }

regen=(python scripts/regen_card_audio_side.py
       --output-dir "$outdir" --card-uuid "$uuid" --side "$side"
       --content-key "$ck" --voice "$voice" --speed "$speed")
echo "[regen-card $job] ${regen[*]}"
"${regen[@]}" || { echo "ERROR: regen failed" >&2; exit 1; }
echo "[regen-card $job] DONE"
