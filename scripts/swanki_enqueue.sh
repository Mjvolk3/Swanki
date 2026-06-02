#!/usr/bin/env bash
#
# scripts/swanki_enqueue.sh
# [[scripts.swanki_enqueue]]
# https://github.com/Mjvolk3/Swanki/tree/main/scripts/swanki_enqueue.sh
#
# Enqueue one swanki generation job onto the serial drain queue
# (scripts/swanki_queue.sh, run by the swanki-queue.service systemd --user
# unit). Fire-and-forget: drop as many jobs as you like, in any order; the
# drainer runs them one at a time so the single shared Fish server is never
# oversubscribed. Job specs are JSON files under $SWANKI_QUEUE_DIR/pending/,
# ordered FIFO by filename timestamp.
#
# Usage:
#   scripts/swanki_enqueue.sh --pdf PATH --key CITATION_KEY \
#       [--content-key CK] [--voice fish_speech] [--author "Name"] \
#       [--extra "hydra.override=foo bar=baz"]
#
# Papers:        --pdf + --key (output_dir defaults to the citation key).
# Book chapters: also --content-key <key>_CH##_<slug>; output_dir is derived
#                as <key>/<content_key>. Voice defaults to the british-prof
#                seminar (fish_speech); pass a clone (fish_speech_bechtel,
#                fish_speech_hamming, ...) for author-voiced books.
set -euo pipefail

QUEUE_DIR="${SWANKI_QUEUE_DIR:-$HOME/.swanki-queue}"

pdf="" key="" content_key="" voice="fish_speech" author="" extra=""
while [ $# -gt 0 ]; do
    case "$1" in
        --pdf) pdf="$2"; shift 2 ;;
        --key) key="$2"; shift 2 ;;
        --content-key) content_key="$2"; shift 2 ;;
        --voice) voice="$2"; shift 2 ;;
        --author) author="$2"; shift 2 ;;
        --extra) extra="$2"; shift 2 ;;
        -h|--help) sed -n '2,30p' "$0"; exit 0 ;;
        *) echo "unknown arg: $1" >&2; exit 2 ;;
    esac
done

[ -n "$pdf" ] || { echo "ERROR: --pdf required" >&2; exit 2; }
[ -n "$key" ] || { echo "ERROR: --key required" >&2; exit 2; }
[ -f "$pdf" ] || { echo "ERROR: pdf not found: $pdf" >&2; exit 2; }

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
