#!/usr/bin/env bash
#
# scripts/swanki_queue.sh
# [[scripts.swanki_queue]]
# https://github.com/Mjvolk3/Swanki/tree/main/scripts/swanki_queue.sh
#
# Serial drain queue for swanki generation jobs. Polls
# $SWANKI_QUEUE_DIR/pending/ for JSON specs (written by swanki_enqueue.sh),
# claims the oldest, runs swanki, then DELIVERS the result before marking DONE.
# Loops forever — meant to run under systemd --user (swanki-queue.service).
#
# DONE = generated AND delivered. After a clean swanki run the drainer invokes
# `python -m swanki.delivery` for the job, which runs the Zotero backup then the
# Anki import (per item) and defers ABS. A spec moves to done/ only when that
# delivery succeeds; a generation failure goes to failed/, a delivery failure to
# undelivered/ (artifacts + .delivery.json markers stay on disk so a re-run
# resumes from the first unmarked target WITHOUT regenerating). ABS is debounced:
# each delivered job touches an abs-dirty flag and the drainer fires ONE
# `finalize-abs` refresh after the pending queue empties.
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
#   SWANKI_QUEUE_DELIVER      1|0 run delivery after gen (default 1)
set -uo pipefail

QUEUE_DIR="${SWANKI_QUEUE_DIR:-$HOME/.swanki-queue}"
CONCURRENCY="${SWANKI_QUEUE_CONCURRENCY:-1}"
EXECUTOR="${SWANKI_QUEUE_EXECUTOR:-local}"
REPO="${SWANKI_REPO:-$HOME/Documents/projects/Swanki}"
CONDA_SH="${SWANKI_CONDA_SH:-$HOME/miniconda3/etc/profile.d/conda.sh}"
POLL="${SWANKI_QUEUE_POLL:-5}"
DELIVER="${SWANKI_QUEUE_DELIVER:-1}"
ABS_DIRTY="$QUEUE_DIR/abs-dirty"

mkdir -p "$QUEUE_DIR"/{pending,running,done,failed,undelivered,logs}

# SWANKI_DATA tells the delivery step where the pipeline wrote artifacts; pull
# it from the repo .env if the drainer's own env doesn't carry it.
if [ -z "${SWANKI_DATA:-}" ] && [ -f "$REPO/.env" ]; then
    SWANKI_DATA="$(grep -E '^SWANKI_DATA=' "$REPO/.env" | tail -1 | cut -d= -f2- | tr -d '"')"
fi
SWANKI_DATA="${SWANKI_DATA:-$REPO/swanki-out}"

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

    # zotero=default: the delivery step (below) owns the Zotero backup now, so
    # the pipeline must NOT also upload (that would double-upload). Delivery
    # runs zotero -> anki -> abs in order with per-target markers.
    local args=(pdf_path="$pdf" citation_key="$key" audio=all anki=default
                ocr=mineru "models=$voice" zotero=default)
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

    if [ "$rc" -ne 0 ]; then
        mv "$spec" "$QUEUE_DIR/failed/"
        log "FAIL $id (rc=$rc, generation) — see $logf"
        return
    fi

    # Generation succeeded. Deliver (Zotero -> Anki; defer ABS) before DONE.
    if [ "$DELIVER" != "1" ] || [ "$EXECUTOR" != "local" ]; then
        mv "$spec" "$QUEUE_DIR/done/"
        log "DONE $id (delivery skipped)"
        return
    fi

    local base prefix jobout drc=0
    base="$key"; prefix="$key"
    [ -n "$ck" ] && { base="$key/$ck"; prefix="$ck"; }
    # The pipeline writes $SWANKI_DATA/<base> (auto-incremented _N if it
    # pre-existed); pick the newest matching dir as the delivery source.
    jobout="$(find "$SWANKI_DATA/$(dirname "$base")" -maxdepth 1 \
                -name "$(basename "$base")*" -type d 2>/dev/null \
                | sort | tail -1)"
    if [ -z "$jobout" ]; then
        mv "$spec" "$QUEUE_DIR/undelivered/"
        log "UNDELIVERED $id — no output dir under $SWANKI_DATA/$base"
        return
    fi

    log "DELIVER $id (jobout=$jobout) -> $logf"
    ( set +u
      # shellcheck disable=SC1090
      source "$CONDA_SH" && conda activate swanki && cd "$REPO" \
          && python -m swanki.delivery deliver \
                --citation-key "$key" --content-key "$ck" \
                --output-dir "$jobout" --audio-prefix "$prefix" ) \
        >>"$logf" 2>&1 || drc=$?

    if [ "$drc" -eq 0 ]; then
        touch "$ABS_DIRTY"        # one debounced ABS refresh at drain end
        mv "$spec" "$QUEUE_DIR/done/"
        log "DONE $id (zotero+anki delivered; abs deferred)"
    else
        mv "$spec" "$QUEUE_DIR/undelivered/"
        log "UNDELIVERED $id (rc=$drc) — markers in $jobout/.delivery.json; see $logf"
    fi
}

# Fire the single debounced ABS refresh when the queue drains, then clear the
# dirty flag. Blocking lock (--wait) so a contended cron refresh can't make this
# silently skip.
finalize_abs() {
    [ -f "$ABS_DIRTY" ] || return 0
    log "FINALIZE-ABS (debounced refresh)"
    ( set +u
      # shellcheck disable=SC1090
      source "$CONDA_SH" && conda activate swanki && cd "$REPO" \
          && python -m swanki.delivery finalize-abs ) \
        >>"$QUEUE_DIR/queue.log" 2>&1 \
        && rm -f "$ABS_DIRTY" && log "FINALIZE-ABS done" \
        || log "FINALIZE-ABS failed — abs-dirty retained, will retry next drain"
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
was_busy=false
while true; do
    running="$(find "$QUEUE_DIR/running" -maxdepth 1 -name '*.json' | wc -l)"
    pending="$(find "$QUEUE_DIR/pending" -maxdepth 1 -name '*.json' | wc -l)"
    if [ "$running" -lt "$CONCURRENCY" ] && [ "$pending" -gt 0 ]; then
        next="$(find "$QUEUE_DIR/pending" -maxdepth 1 -name '*.json' | sort | head -1)"
        if [ -n "$next" ]; then
            claimed="$QUEUE_DIR/running/$(basename "$next")"
            if mv "$next" "$claimed" 2>/dev/null; then
                was_busy=true
                run_one "$claimed" &
            fi
            continue   # try to fill remaining slots immediately (concurrency>1)
        fi
    fi
    # Fully drained: fire the debounced ABS refresh once on the busy->idle edge.
    if [ "$running" -eq 0 ] && [ "$pending" -eq 0 ] && [ "$was_busy" = true ]; then
        finalize_abs
        was_busy=false
    fi
    sleep "$POLL"
done
