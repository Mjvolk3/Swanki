#!/usr/bin/env bash
#
# scripts/swanki_enqueue.sh
# [[scripts.swanki_enqueue]]
# https://github.com/Mjvolk3/Swanki/tree/main/scripts/swanki_enqueue.sh
#
# Enqueue one swanki generation job. Two backends, selected by
# SWANKI_QUEUE_EXECUTOR (same knob the drainer uses):
#
#   local | noop (default)  Write a JSON spec to $SWANKI_QUEUE_DIR/pending/ for
#                           the serial bash drainer (scripts/swanki_queue.sh).
#   slurm                   Render + submit scripts/swanki_job.sbatch via
#                           `sbatch --parsable`; SLURM owns scheduling. One GPU
#                           per job, serverless Fish in-job. Prints the jobid on
#                           stdout for dependency chaining.
#
# Usage:
#   scripts/swanki_enqueue.sh --pdf PATH --key CITATION_KEY \
#       [--content-key CK] [--voice fish_speech] [--author "Name"] \
#       [--extra "hydra.override=foo bar=baz"] \
#       [--dependency SPEC] [--after JOBID] [--singleton]
#
# Papers:        --pdf + --key (output_dir defaults to the citation key).
# Book chapters: also --content-key <key>_CH##_<slug>; output_dir is derived
#                as <key>/<content_key>. Voice defaults to the british-prof
#                seminar (fish_speech); pass a clone (fish_speech_bechtel,
#                fish_speech_hamming, ...) for author-voiced books.
#
# SLURM chaining (slurm backend only):
#   --after JOBID     run after JOBID finishes OK (afterok:JOBID)
#   --dependency SPEC raw sbatch dependency, e.g. afterany:101:102
#   --singleton       one swanki job at a time (linear), via job-name singleton
#   linear/parallel is also a QOS GrpTRES=gres/gpu=N cap (see the cutover runbook).
#
# DRY_RUN=1 with the slurm backend prints the submission instead of running it.
set -euo pipefail

QUEUE_DIR="${SWANKI_QUEUE_DIR:-$HOME/.swanki-queue}"
EXECUTOR="${SWANKI_QUEUE_EXECUTOR:-local}"
REPO="${SWANKI_REPO:-$(cd "$(dirname "$0")/.." && pwd)}"

pdf="" key="" content_key="" voice="fish_speech" author="" extra=""
dependency="" after="" singleton=0
while [ $# -gt 0 ]; do
    case "$1" in
        --pdf) pdf="$2"; shift 2 ;;
        --key) key="$2"; shift 2 ;;
        --content-key) content_key="$2"; shift 2 ;;
        --voice) voice="$2"; shift 2 ;;
        --author) author="$2"; shift 2 ;;
        --extra) extra="$2"; shift 2 ;;
        --dependency) dependency="$2"; shift 2 ;;
        --after) after="$2"; shift 2 ;;
        --singleton) singleton=1; shift ;;
        -h|--help) sed -n '2,38p' "$0"; exit 0 ;;
        *) echo "unknown arg: $1" >&2; exit 2 ;;
    esac
done

[ -n "$pdf" ] || { echo "ERROR: --pdf required" >&2; exit 2; }
[ -n "$key" ] || { echo "ERROR: --key required" >&2; exit 2; }
[ -f "$pdf" ] || { echo "ERROR: pdf not found: $pdf" >&2; exit 2; }

mkdir -p "$QUEUE_DIR/logs"

if [ "$EXECUTOR" = "slurm" ]; then
    # Compose the dependency expression (comma = AND in sbatch).
    deps=()
    [ "$singleton" = 1 ] && deps+=("singleton")
    [ -n "$after" ] && deps+=("afterok:$after")
    [ -n "$dependency" ] && deps+=("$dependency")

    sb=(sbatch --parsable --job-name="${SWANKI_JOB_NAME:-swanki}" --export=ALL
        --output="$QUEUE_DIR/logs/slurm-%j.log")
    if [ "${#deps[@]}" -gt 0 ]; then
        dep_join="$(IFS=,; echo "${deps[*]}")"
        sb+=(--dependency="$dep_join")
    fi
    # SWANKI_SBATCH_EXTRA passes raw sbatch flags through, e.g. to dedicate N GPUs
    # to swanki: `export SWANKI_SBATCH_EXTRA="--qos=swanki --account=swanki"` with a
    # QOS GrpTRES=gres/gpu=N cap (see notes/runbook.slurm-cutover.md). Word-split.
    # shellcheck disable=SC2206
    [ -n "${SWANKI_SBATCH_EXTRA:-}" ] && sb+=($SWANKI_SBATCH_EXTRA)
    sb+=("$REPO/scripts/swanki_job.sbatch")

    export SWANKI_JOB_PDF="$pdf" SWANKI_JOB_KEY="$key" \
        SWANKI_JOB_CONTENT_KEY="$content_key" SWANKI_JOB_VOICE="$voice" \
        SWANKI_JOB_AUTHOR="$author" SWANKI_JOB_EXTRA="$extra"

    if [ "${DRY_RUN:-0}" = "1" ]; then
        echo "DRY RUN — would submit (env exported, then):"
        printf '  SWANKI_JOB_PDF=%q SWANKI_JOB_KEY=%q SWANKI_JOB_CONTENT_KEY=%q\n' \
            "$pdf" "$key" "$content_key"
        printf '  SWANKI_JOB_VOICE=%q SWANKI_JOB_AUTHOR=%q SWANKI_JOB_EXTRA=%q\n' \
            "$voice" "$author" "$extra"
        printf '  '; printf '%q ' "${sb[@]}"; echo
        exit 0
    fi

    jid="$("${sb[@]}")"
    echo "$jid"  # jobid on stdout for chaining (--after "$jid")
    echo "submitted: slurm job $jid (key=$key${content_key:+ ck=$content_key})" >&2
    exit 0
fi

# --- legacy local/noop backend: write a JSON spec for the bash drainer -------
mkdir -p "$QUEUE_DIR"/{pending,running,done,failed,logs}
id="$(date +%Y%m%dT%H%M%S)-$(date +%N | cut -c1-4)-${key}"
spec="$QUEUE_DIR/pending/${id}.json"

jq -n \
    --arg id "$id" --arg pdf "$pdf" --arg key "$key" \
    --arg content_key "$content_key" --arg voice "$voice" \
    --arg author "$author" --arg extra "$extra" \
    --arg enqueued "$(date -Iseconds)" \
    '{id:$id, pdf:$pdf, citation_key:$key, content_key:$content_key,
      voice:$voice, author:$author, extra:$extra, enqueued:$enqueued}' \
    > "$spec"

echo "queued: $spec"
echo "pending: $(find "$QUEUE_DIR/pending" -maxdepth 1 -name '*.json' | wc -l)"
