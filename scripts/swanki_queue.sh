#!/usr/bin/env bash
#
# scripts/swanki_queue.sh
# [[scripts.swanki_queue]]
# https://github.com/Mjvolk3/Swanki/tree/main/scripts/swanki_queue.sh
#
# Serial drain queue for swanki generation jobs. Polls
# $SWANKI_QUEUE_DIR/pending/ for JSON specs (written by swanki_enqueue.sh),
# claims the oldest, runs swanki, and moves the spec to done/ or failed/ with a
# per-job log. Loops forever — meant to run under systemd --user
# (swanki-queue.service).
#
# Why serial: the single shared Fish TTS server is the bottleneck (one swanki
# run already saturates all its workers), so parallelism just thrashes the GPU.
# SWANKI_QUEUE_CONCURRENCY keys off Fish capacity, NOT GPU count — keep it at 1
# while one Fish server backs the box; raise it only if Fish is scaled to serve
# more concurrent streams.
#
# Env knobs:
#   SWANKI_QUEUE_DIR          queue root            (default ~/.swanki-queue)
#   SWANKI_QUEUE_CONCURRENCY  max in-flight jobs    (default 1)
#   SWANKI_QUEUE_EXECUTOR     local | noop | slurm  (default local)
#   SWANKI_REPO               repo root for `swanki`(default ~/Documents/projects/Swanki)
#   SWANKI_CONDA_SH           conda profile.d path  (default ~/miniconda3/etc/profile.d/conda.sh)
#   SWANKI_QUEUE_POLL         poll seconds          (default 5)
set -uo pipefail

QUEUE_DIR="${SWANKI_QUEUE_DIR:-$HOME/.swanki-queue}"
CONCURRENCY="${SWANKI_QUEUE_CONCURRENCY:-1}"
EXECUTOR="${SWANKI_QUEUE_EXECUTOR:-local}"
REPO="${SWANKI_REPO:-$HOME/Documents/projects/Swanki}"
CONDA_SH="${SWANKI_CONDA_SH:-$HOME/miniconda3/etc/profile.d/conda.sh}"
POLL="${SWANKI_QUEUE_POLL:-5}"

mkdir -p "$QUEUE_DIR"/{pending,running,done,failed,logs}

log() { echo "[$(date -Iseconds)] $*" | tee -a "$QUEUE_DIR/queue.log"; }

run_one() {
    local spec="$1"            # path under running/
    local id logf
    id="$(basename "$spec" .json)"
    logf="$QUEUE_DIR/logs/${id}.log"

    local pdf key ck voice author extra
    pdf="$(jq -r '.pdf' "$spec")"
    key="$(jq -r '.citation_key' "$spec")"
    ck="$(jq -r '.content_key // ""' "$spec")"
    voice="$(jq -r '.voice // "fish_speech"' "$spec")"
    author="$(jq -r '.author // ""' "$spec")"
    extra="$(jq -r '.extra // ""' "$spec")"

    local args=(pdf_path="$pdf" citation_key="$key" audio=all anki=default
                ocr=mineru "models=$voice" zotero=sync)
    [ -n "$ck" ] && args+=(content_key="$ck" "+output_dir=$key/$ck")
    [ -n "$author" ] && args+=("+author=$author")
    args+=(pipeline.processing.confirm_before_generation=false)
    # Word-split $extra intentionally so callers can pass extra hydra overrides.
    # shellcheck disable=SC2206
    [ -n "$extra" ] && args+=($extra)

    log "RUN $id (executor=$EXECUTOR voice=$voice) -> $logf"
    local rc=0
    case "$EXECUTOR" in
        local)
            ( set +u
              # shellcheck disable=SC1090
              source "$CONDA_SH" && conda activate swanki && cd "$REPO" \
                  && swanki "${args[@]}" ) >"$logf" 2>&1 || rc=$?
            ;;
        noop)
            # Dry-run: record the composed argv, do not call swanki.
            { echo "DRY RUN — would execute:"; printf '  swanki'; printf ' %q' "${args[@]}"; echo; } >"$logf"
            ;;
        slurm)
            # FORWARD-COMPAT STUB (dual-purpose era): submit to SLURM instead of
            # running locally. Keep this same spec/interface; the only rule is
            # to cap concurrent swanki jobs to Fish capacity (via
            # SWANKI_QUEUE_CONCURRENCY here, or `sbatch --dependency=singleton`
            # / array %N on the SLURM side). Not implemented yet.
            log "ERROR slurm executor not implemented yet (job $id)"; rc=70
            ;;
        *)
            log "ERROR unknown executor '$EXECUTOR' (job $id)"; rc=64
            ;;
    esac

    if [ "$rc" -eq 0 ]; then
        mv "$spec" "$QUEUE_DIR/done/"
        log "DONE $id"
    else
        mv "$spec" "$QUEUE_DIR/failed/"
        log "FAIL $id (rc=$rc) — see $logf"
    fi
}

# Startup recovery: a restart (systemd) kills in-flight children, orphaning
# their specs in running/. Requeue them so nothing is silently lost. swanki
# auto-increments output_dir, so a re-run is safe (writes a fresh dir).
orphans="$(find "$QUEUE_DIR/running" -maxdepth 1 -name '*.json' 2>/dev/null)"
if [ -n "$orphans" ]; then
    while IFS= read -r f; do
        mv "$f" "$QUEUE_DIR/pending/" && log "REQUEUE orphan $(basename "$f")"
    done <<< "$orphans"
fi

log "swanki-queue up (concurrency=$CONCURRENCY executor=$EXECUTOR repo=$REPO)"
while true; do
    running="$(find "$QUEUE_DIR/running" -maxdepth 1 -name '*.json' | wc -l)"
    if [ "$running" -lt "$CONCURRENCY" ]; then
        next="$(find "$QUEUE_DIR/pending" -maxdepth 1 -name '*.json' | sort | head -1)"
        if [ -n "$next" ]; then
            claimed="$QUEUE_DIR/running/$(basename "$next")"
            if mv "$next" "$claimed" 2>/dev/null; then
                run_one "$claimed" &
            fi
            continue   # try to fill remaining slots immediately (concurrency>1)
        fi
    fi
    sleep "$POLL"
done
