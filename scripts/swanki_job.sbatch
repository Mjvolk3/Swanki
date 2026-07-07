#!/usr/bin/env bash
#
# scripts/swanki_job.sbatch
# [[scripts.swanki_job]]
# https://github.com/Mjvolk3/Swanki/tree/main/scripts/swanki_job.sbatch
#
# Per-paper SLURM job: one GPU, serverless Fish, generate, deliver, tear down.
#
# Submitted by scripts/swanki_enqueue.sh (SWANKI_QUEUE_EXECUTOR=slurm) or the
# swanki_queue.sh slurm bridge, which export the job inputs as SWANKI_JOB_* and
# `sbatch --export=ALL`. The job:
#   1. derives a free host port (apptainer uses HOST networking, no -p map),
#   2. brings up Fish from the baked .sif via `apptainer --nv` on the single
#      allocated GPU (the cgroup exposes exactly that card; --gres=gpu:1),
#   3. exports SWANKI_FISH_PORTS=<that one port> so swanki TTS targets it,
#   4. runs native-conda swanki (MinerU OCR + cards + Fish TTS, all on local
#      GPU index 0), then delivery (Zotero, then Anki under an flock, ABS
#      deferred to the singleton finalizer job), then tears Fish down on EXIT.
#
# DONE = delivered: a non-zero exit means generation or delivery failed and the
# artifacts + .delivery.json markers stay on disk for a resumable re-run. Anki
# being down exits 75 (nothing delivered yet, fully resumable).
#
# Defaults below are overridable on the sbatch CLI (CLI wins over #SBATCH) and
# via the SWANKI_* env knobs documented inline.
#
#SBATCH --job-name=swanki
#SBATCH --partition=main
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=16
#SBATCH --mem=64G
#SBATCH --time=UNLIMITED
#SBATCH --output=/home/michaelvolk/.swanki-queue/logs/slurm-%j.log
set -uo pipefail

# --- inputs (exported by the submitter) -------------------------------------
pdf="${SWANKI_JOB_PDF:-}"
key="${SWANKI_JOB_KEY:-}"
ck="${SWANKI_JOB_CONTENT_KEY:-}"
voice="${SWANKI_JOB_VOICE:-fish_speech}"
author="${SWANKI_JOB_AUTHOR:-}"
extra="${SWANKI_JOB_EXTRA:-}"

[ -n "$pdf" ] || { echo "ERROR: SWANKI_JOB_PDF unset" >&2; exit 2; }
[ -n "$key" ] || { echo "ERROR: SWANKI_JOB_KEY unset" >&2; exit 2; }
[ -f "$pdf" ] || { echo "ERROR: pdf not found: $pdf" >&2; exit 2; }

# --- config knobs -----------------------------------------------------------
REPO="${SWANKI_REPO:-$HOME/Documents/projects/Swanki}"
CONDA_SH="${SWANKI_CONDA_SH:-$HOME/miniconda3/etc/profile.d/conda.sh}"
FISH_SIF="${SWANKI_FISH_SIF:-$HOME/Documents/projects/fish-speech/fish-speech-server.sif}"
FISH_REPO="${SWANKI_FISH_REPO:-$HOME/Documents/projects/fish-speech}"
PORT_BASE="${SWANKI_FISH_PORT_BASE:-8100}"
PORT_RANGE="${SWANKI_FISH_PORT_RANGE:-400}"
COMPILE="${SWANKI_FISH_COMPILE:-1}"  # torch.compile ON by default: ~10x TTS
                                     # throughput (uncompiled s2-pro ~3.6 tok/s
                                     # => ~1.3h/chapter). Warmup adds ~60-90s.
                                     # Set SWANKI_FISH_COMPILE=0 for short jobs.
ANKI_URL="${SWANKI_ANKICONNECT_URL:-http://127.0.0.1:8765}"
QUEUE_DIR="${SWANKI_QUEUE_DIR:-$HOME/.swanki-queue}"
ANKI_LOCK="${SWANKI_ANKI_LOCK:-$QUEUE_DIR/anki.lock}"
ABS_DIRTY="${SWANKI_ABS_DIRTY:-$QUEUE_DIR/abs-dirty}"
mkdir -p "$QUEUE_DIR/logs"

# SWANKI_DATA tells delivery where the pipeline wrote artifacts; fall back to the
# repo .env (mirrors swanki_queue.sh).
if [ -z "${SWANKI_DATA:-}" ] && [ -f "$REPO/.env" ]; then
    SWANKI_DATA="$(grep -E '^SWANKI_DATA=' "$REPO/.env" | tail -1 | cut -d= -f2- | tr -d '"')"
fi
SWANKI_DATA="${SWANKI_DATA:-$REPO/swanki-out}"

job="${SLURM_JOB_ID:-$$}"

# --- 1. derive a free host port (apptainer shares the host network) ---------
port=$(( PORT_BASE + job % PORT_RANGE ))
while ss -ltnH "( sport = :$port )" 2>/dev/null | grep -q ":$port"; do
    port=$(( port + 1 ))
done
echo "[swanki-job $job] fish port=$port gpu=${CUDA_VISIBLE_DEVICES:-ambient}"

# --- 2. bring up serverless Fish on the allocated GPU -----------------------
# Run Fish as a direct background CHILD (apptainer exec, NOT `instance start`):
# an instance is a daemon that survives scancel/SIGKILL (the EXIT trap never
# fires), orphaning ~22GB of GPU memory so the NEXT job on that card OOMs. A
# child lives in the job's cgroup, so SLURM's cgroup-kill reaps it on ANY
# termination. --writable-tmpfs absorbs the read-only image's runtime writes;
# SWANKI_FISH_PYTHON is the venv interpreter (not on PATH once we bypass entrypoint).
tmpfs_flag=()
[ "${SWANKI_FISH_WRITABLE:-1}" = "1" ] && tmpfs_flag=(--writable-tmpfs)

# api_server.py enables torch.compile via the --compile CLI flag, NOT the COMPILE
# env var. COMPILE is read only by Fish's Docker entrypoint (build_compile_args),
# which we BYPASS by invoking api_server.py directly -- so passing --env COMPILE=1
# alone is a no-op and Fish runs uncompiled (~3.6 tok/s vs ~10x compiled).
# Translate COMPILE -> --compile here.
compile_flag=()
{ [ "$COMPILE" = "1" ] || [ "$COMPILE" = "true" ]; } && compile_flag=(--compile)

# Crash log for Layer-2 supervision (best-effort; $QUEUE_DIR is under $HOME, not
# the often-full /scratch). /tmp fallback if the logs dir is somehow unwritable.
CRASH_LOG="$QUEUE_DIR/logs/swanki-job-$job-fish-crash.log"
[ -w "$QUEUE_DIR/logs" ] || CRASH_LOG="/tmp/swanki-job-$job-fish-crash.log"

# start_fish: (re)launch Fish on $port as a cgroup child, reassign the GLOBAL
# fish_pid (so the late-bound EXIT/TERM/INT trap always reaps the CURRENT Fish),
# and block until /v1/health answers. Returns non-zero if Fish dies or never goes
# healthy within the bounded timeout -- the caller (initial launch or the Layer-2
# supervisor) decides whether that is fatal. Reused verbatim for every respawn so
# a restarted Fish is identical to the original (same .sif, port, checkpoints).
start_fish() {
    apptainer exec --nv "${tmpfs_flag[@]}" --pwd /app \
        --bind "$FISH_REPO/checkpoints:/app/checkpoints,$FISH_REPO/references:/app/references" \
        --env "COMPILE=$COMPILE" \
        "$FISH_SIF" \
        "${SWANKI_FISH_PYTHON:-/app/.venv/bin/python}" tools/api_server.py --listen "0.0.0.0:$port" \
            --llama-checkpoint-path checkpoints/s2-pro \
            --decoder-checkpoint-path checkpoints/s2-pro/codec.pth \
            --decoder-config-name modded_dac_vq "${compile_flag[@]}" &
    fish_pid=$!
    local i
    for i in $(seq 1 "${SWANKI_FISH_HEALTH_TIMEOUT:-300}"); do
        if curl -sf -m 3 "http://127.0.0.1:$port/v1/health" >/dev/null 2>&1; then
            return 0
        fi
        kill -0 "$fish_pid" 2>/dev/null || return 1   # Fish died before health
        sleep 1
    done
    return 1
}

# capture_fish_crash <label> [exit_code]: append a best-effort, timestamped record
# (exit code, dmesg/Xid, nvidia-smi Xid) to $CRASH_LOG so the next node-level kill
# is finally named. Every probe is guarded -- instrumentation must NEVER abort the
# job -- so this always returns 0.
capture_fish_crash() {
    local label="$1" rc="${2:-?}"
    {
        echo "=== fish crash [$label] $(date -u +%Y-%m-%dT%H:%M:%SZ) job=$job pid=${fish_pid:-?} rc=$rc gpu=${CUDA_VISIBLE_DEVICES:-ambient} port=$port ==="
        echo "--- kernel log tail ---"
        dmesg 2>/dev/null | tail -n 50 \
            || journalctl -k -n 50 2>/dev/null \
            || tail -n 50 /var/log/messages 2>/dev/null \
            || echo "(kernel log unavailable: dmesg restricted, no journalctl/-k, no /var/log/messages)"
        echo "--- nvidia-smi Xid ---"
        nvidia-smi -q 2>/dev/null | grep -iA3 xid || echo "(no Xid lines / nvidia-smi unavailable)"
        echo
    } >> "$CRASH_LOG" 2>/dev/null
    return 0
}

# The trap is late-bound on $fish_pid (decision 2): start_fish reassigns the
# global on every respawn, so this always kills whichever Fish is current.
fish_pid=""
trap 'kill "$fish_pid" 2>/dev/null' EXIT TERM INT

# Initial launch -- a cold Fish that never goes healthy is a hard failure.
start_fish || { echo "ERROR: Fish did not become healthy on :$port" >&2; exit 1; }
export SWANKI_FISH_PORTS="$port"

# --- 3. activate native conda env (swanki + swanki-mineru live here) ---------
set +u
# shellcheck disable=SC1090
source "$CONDA_SH"
conda activate swanki
set -u
cd "$REPO" || { echo "ERROR: cannot cd $REPO" >&2; exit 1; }

# --- 4. generate ------------------------------------------------------------
args=(pdf_path="$pdf" citation_key="$key" audio=all anki=default
      ocr=mineru "models=$voice" zotero=default)
[ -n "$ck" ] && args+=(content_key="$ck" "+output_dir=$key/$ck")
[ -n "$author" ] && args+=("+author=$author")
args+=(pipeline.processing.confirm_before_generation=false)
# Word-split $extra intentionally so callers can pass extra hydra overrides.
# shellcheck disable=SC2206
[ -n "$extra" ] && args+=($extra)

echo "[swanki-job $job] generating: swanki ${args[*]}"
if [ "${SWANKI_FISH_RESTART_ENABLED:-1}" = "1" ]; then
    # --- Layer 2: supervise generation ---------------------------------------
    # Background swanki and poll BOTH it and Fish from this one shell (the shell
    # that owns $fish_pid + the trap). When Fish dies mid-run, reap it, capture a
    # crash record, respawn on the SAME port, re-wait health, and continue -- the
    # client retry in swanki/audio/_common.py (_tts_fish_speech) re-discovers the
    # fresh server and resumes. Stretch that client's reconnect window so its
    # 2/5/15/30s backoff outlasts a respawn's ~30-60s model reload (default 4
    # attempts is too tight); honor a caller override.
    export SWANKI_FISH_TTS_ATTEMPTS="${SWANKI_FISH_TTS_ATTEMPTS:-8}"
    swanki "${args[@]}" &
    swanki_pid=$!
    gen_rc=0
    restarts=0
    while true; do
        # Check swanki FIRST so a completed run is never masked by a simultaneous
        # Fish teardown (on success the trap, not the loop, reaps Fish).
        if ! kill -0 "$swanki_pid" 2>/dev/null; then
            wait "$swanki_pid"; gen_rc=$?      # harvest swanki's real exit code
            break
        fi
        if ! kill -0 "$fish_pid" 2>/dev/null; then
            wait "$fish_pid" 2>/dev/null; fish_rc=$?   # fully reap, free the port
            capture_fish_crash "$restarts" "$fish_rc"
            restarts=$(( restarts + 1 ))
            if [ "$restarts" -gt "${SWANKI_FISH_MAX_RESTARTS:-3}" ]; then
                echo "ERROR: Fish exceeded max restarts ($(( restarts - 1 )))" >&2
                capture_fish_crash "final" "$fish_rc"
                kill "$swanki_pid" 2>/dev/null
                exit 1
            fi
            echo "[swanki-job $job] Fish died (rc=$fish_rc); respawn $restarts/${SWANKI_FISH_MAX_RESTARTS:-3} on :$port" >&2
            sleep "${SWANKI_FISH_RESPAWN_SETTLE:-5}"   # let the socket fully release
            start_fish || { echo "ERROR: respawned Fish never healthy on :$port" >&2
                            capture_fish_crash "respawn-unhealthy"
                            kill "$swanki_pid" 2>/dev/null; exit 1; }
        fi
        sleep "${SWANKI_FISH_POLL_S:-3}"
    done
    [ "$gen_rc" -eq 0 ] || { echo "ERROR: swanki generation failed (rc=$gen_rc)" >&2; exit 1; }
else
    # Kill-switch (SWANKI_FISH_RESTART_ENABLED=0): launch-once, no supervisor --
    # the old behavior, a fast fail on Fish death. For crash-loop debugging.
    swanki "${args[@]}" || { echo "ERROR: swanki generation failed" >&2; exit 1; }
fi

# Generation done. SWANKI_JOB_DELIVER=0 stops here (audio-only / parallel runs
# skip the card-oriented Zotero+Anki delivery: it races on a shared Zotero item
# and has no apkg under mode=audio_only -- push audio to ABS separately).
if [ "${SWANKI_JOB_DELIVER:-1}" != "1" ]; then
    echo "[swanki-job $job] DONE (generation only; delivery skipped)"
    exit 0
fi

# --- 5. locate the output dir (newest matching; swanki auto-increments _N) ---
base="$key"; prefix="$key"
[ -n "$ck" ] && { base="$key/$ck"; prefix="$ck"; }
jobout="$(find "$SWANKI_DATA/$(dirname "$base")" -maxdepth 1 \
            -name "$(basename "$base")*" -type d -printf '%T@ %p\n' 2>/dev/null \
            | sort -rn | head -1 | cut -d' ' -f2-)"
[ -n "$jobout" ] || { echo "ERROR: no output dir under $SWANKI_DATA/$base" >&2; exit 1; }
echo "[swanki-job $job] delivering from $jobout"

# --- 6. delivery: Anki health-check, then Zotero (free), Anki (locked) -------
# Defer if Anki is down so a transient outage does not burn a completed run.
if ! curl -sf -m 5 -X POST "$ANKI_URL" \
        -d '{"action":"version","version":6}' >/dev/null 2>&1; then
    echo "AnkiConnect unreachable at $ANKI_URL — delivery deferred; re-run delivery against $jobout" >&2
    exit 75
fi

deliver=(python -m swanki.delivery deliver
         --citation-key "$key" --content-key "$ck"
         --output-dir "$jobout" --audio-prefix "$prefix")

# Zotero backup: parallel-safe across jobs (distinct items), no lock.
"${deliver[@]}" --targets zotero || { echo "ERROR: zotero delivery failed" >&2; exit 1; }
# Anki import+sync: one headless AnkiConnect cannot serve concurrent jobs, so
# serialize ONLY this phase across the node with an flock.
flock "$ANKI_LOCK" "${deliver[@]}" --targets anki \
    || { echo "ERROR: anki delivery failed" >&2; exit 1; }

# ABS is debounced into the singleton finalizer job; just flag dirtiness.
touch "$ABS_DIRTY"
echo "[swanki-job $job] DONE (zotero+anki delivered; abs deferred to finalizer)"
