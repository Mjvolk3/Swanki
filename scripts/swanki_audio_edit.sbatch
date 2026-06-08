#!/usr/bin/env bash
#
# scripts/swanki_audio_edit.sbatch
# [[scripts.swanki_audio_edit]]
# https://github.com/Mjvolk3/Swanki/tree/main/scripts/swanki_audio_edit.sbatch
#
# SLURM-native surgical audio edit: one GPU, serverless Fish in-job, apply ONE
# chunk edit via scripts/swanki_audio_edit.py (-> swanki.audio.comment_edit.
# edit_chunk), tear Fish down. Post-cutover replacement for the old localhost:8080
# Docker-fleet surgical path the audio-fix-from-annotations skill assumes.
#
# Inputs (exported by the caller; sbatch --export=ALL):
#   SWANKI_EDIT_MANIFEST  path to the live chunk_manifest.json   (required)
#   SWANKI_EDIT_IDX       audio-type-local chunk index           (required)
#   SWANKI_EDIT_MODE      speech_only | comment | new_text       (default speech_only)
#   SWANKI_EDIT_VOICE     models config name                     (default fish_speech_hamming)
#   SWANKI_EDIT_SPEED     render speed; MUST match the original   (default 1.0)
#   SWANKI_EDIT_PAYLOAD   comment text / new_text                 (modes comment|new_text)
#   SWANKI_EDIT_MODEL     llm string                              (comment path only)
#
#SBATCH --job-name=swanki-edit
#SBATCH --partition=main
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --time=UNLIMITED
#SBATCH --output=slurm-%j.log
set -uo pipefail

manifest="${SWANKI_EDIT_MANIFEST:?SWANKI_EDIT_MANIFEST unset}"
idx="${SWANKI_EDIT_IDX:?SWANKI_EDIT_IDX unset}"
mode="${SWANKI_EDIT_MODE:-speech_only}"
voice="${SWANKI_EDIT_VOICE:-fish_speech_hamming}"
speed="${SWANKI_EDIT_SPEED:-1.0}"
payload="${SWANKI_EDIT_PAYLOAD:-}"
model="${SWANKI_EDIT_MODEL:-}"
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
echo "[swanki-edit $job] fish port=$port gpu=${CUDA_VISIBLE_DEVICES:-ambient} manifest=$manifest idx=$idx mode=$mode"

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
edit=(python scripts/swanki_audio_edit.py --manifest "$manifest" --idx "$idx"
      --voice "$voice" --speed "$speed")
case "$mode" in
    speech_only) edit+=(--speech-only) ;;
    comment)     edit+=(--comment "$payload"); [ -n "$model" ] && edit+=(--model "$model") ;;
    new_text)    edit+=(--new-text "$payload"); [ -n "$model" ] && edit+=(--model "$model") ;;
    *) echo "ERROR: bad SWANKI_EDIT_MODE: $mode" >&2; exit 2 ;;
esac

echo "[swanki-edit $job] ${edit[*]}"
"${edit[@]}" || { echo "ERROR: edit_chunk failed" >&2; exit 1; }
echo "[swanki-edit $job] DONE"
