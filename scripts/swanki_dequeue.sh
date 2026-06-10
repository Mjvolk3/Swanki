#!/usr/bin/env bash
#
# scripts/swanki_dequeue.sh
# [[scripts.swanki_dequeue]]
# https://github.com/Mjvolk3/Swanki/tree/main/scripts/swanki_dequeue.sh
#
# List and slice jobs out of the swanki generation queue
# (scripts/swanki_queue.sh). Job specs are JSON files under
# $SWANKI_QUEUE_DIR/pending/, ordered FIFO by filename timestamp. This is the
# inverse of swanki_enqueue.sh: pick pending jobs by index, range, id, citation
# key, or content key and remove them before the drainer claims them.
#
# Only pending/ is touched by default — running/ is an in-flight atomic-mv race
# with the drainer and is never sliced. Removed specs MOVE to cancelled/ (same
# archival pattern as done/ and failed/) so a mistaken slice is recoverable;
# pass --purge to hard-delete instead.
#
# Usage:
#   scripts/swanki_dequeue.sh --status               # full dashboard (drainer + all dirs)
#   scripts/swanki_dequeue.sh --list                 # numbered table of pending
#   scripts/swanki_dequeue.sh --index 3              # slice the 3rd pending job
#   scripts/swanki_dequeue.sh --index 2-4            # slice an inclusive range
#   scripts/swanki_dequeue.sh --index 1,4,5          # slice a comma list
#   scripts/swanki_dequeue.sh --id 20260603T130301-2081-kuchel...   # exact id
#   scripts/swanki_dequeue.sh --key kuchelSchaum...  # every job for a citation key
#   scripts/swanki_dequeue.sh --content-key ..._CH03_building-blocks-of-life
#   scripts/swanki_dequeue.sh --all                  # clear all pending
#
# Flags:
#   --dry-run   show what would be sliced, change nothing
#   --purge     hard-delete instead of moving to cancelled/
#   --state S   target state dir (pending|failed; default pending)
#   --yes       skip the confirmation prompt
#
# Indices are 1-based over the FIFO-sorted pending list and reflect the order
# shown by --list. Run --list first; indices shift after any removal.
set -euo pipefail

QUEUE_DIR="${SWANKI_QUEUE_DIR:-$HOME/.swanki-queue}"

mode="" sel="" state="pending" dry_run=0 purge=0 assume_yes=0
while [ $# -gt 0 ]; do
    case "$1" in
        --status)      mode="status"; shift ;;
        --list)        mode="list"; shift ;;
        --index)       mode="index"; sel="$2"; shift 2 ;;
        --id)          mode="id"; sel="$2"; shift 2 ;;
        --key)         mode="key"; sel="$2"; shift 2 ;;
        --content-key) mode="content_key"; sel="$2"; shift 2 ;;
        --all)         mode="all"; shift ;;
        --dry-run)     dry_run=1; shift ;;
        --purge)       purge=1; shift ;;
        --state)       state="$2"; shift 2 ;;
        --yes|-y)      assume_yes=1; shift ;;
        -h|--help)     sed -n '2,40p' "$0"; exit 0 ;;
        *) echo "unknown arg: $1" >&2; exit 2 ;;
    esac
done

[ -n "$mode" ] || { echo "ERROR: pick one of --status/--list/--index/--id/--key/--content-key/--all" >&2; exit 2; }
case "$state" in pending|failed) ;; *) echo "ERROR: --state must be pending or failed" >&2; exit 2 ;; esac

SRC="$QUEUE_DIR/$state"
[ -d "$SRC" ] || { echo "ERROR: no $state dir at $SRC" >&2; exit 2; }

# FIFO order = filename sort, same as the drainer's `sort | head -1`.
mapfile -t specs < <(find "$SRC" -maxdepth 1 -name '*.json' | sort)

field() { jq -r "$2 // \"\"" "$1"; }

print_row() {  # idx specfile
    local idx="$1" f="$2"
    printf '%3d  %-22s  %s\n' "$idx" \
        "$(field "$f" '.citation_key')" \
        "$(field "$f" '.content_key' | sed 's/^$/—/')"
}

count_dir() { find "$QUEUE_DIR/$1" -maxdepth 1 -name '*.json' 2>/dev/null | wc -l | tr -d ' '; }

if [ "$mode" = "status" ]; then
    active="$(systemctl --user is-active swanki-queue 2>/dev/null || echo 'unknown')"
    echo "swanki-queue: drainer=$active  (concurrency=${SWANKI_QUEUE_CONCURRENCY:-1}  dir=$QUEUE_DIR)"
    echo
    echo "running (in-flight — not sliceable):"
    mapfile -t run < <(find "$QUEUE_DIR/running" -maxdepth 1 -name '*.json' 2>/dev/null | sort)
    if [ "${#run[@]}" -eq 0 ]; then echo "  (idle)"; else
        for f in "${run[@]}"; do
            printf '  %-22s  %s\n' "$(field "$f" '.citation_key')" \
                "$(field "$f" '.content_key' | sed 's/^$/—/')"
        done
    fi
    echo
    echo "pending (FIFO, next = #1): ${#specs[@]}"
    i=1; for f in "${specs[@]}"; do print_row "$i" "$f"; i=$((i + 1)); done
    echo
    printf 'archives:  done %s  ·  failed %s  ·  cancelled %s\n' \
        "$(count_dir done)" "$(count_dir failed)" "$(count_dir cancelled)"
    if [ -f "$QUEUE_DIR/queue.log" ]; then
        echo; echo "recent log:"; tail -n 4 "$QUEUE_DIR/queue.log" | sed 's/^/  /'
    fi
    exit 0
fi

if [ "$mode" = "list" ]; then
    if [ "${#specs[@]}" -eq 0 ]; then echo "($state empty)"; exit 0; fi
    echo "$state ($state count: ${#specs[@]})"
    echo "  #  citation_key            content_key"
    i=1
    for f in "${specs[@]}"; do print_row "$i" "$f"; i=$((i + 1)); done
    exit 0
fi

# Build the list of victims (specfile paths) from the selector.
victims=()
case "$mode" in
    all)
        victims=("${specs[@]}")
        ;;
    index)
        # Expand "1,3,5" and "2-4" into a sorted unique index set.
        idxs=()
        IFS=',' read -ra parts <<< "$sel"
        for p in "${parts[@]}"; do
            if [[ "$p" == *-* ]]; then
                lo="${p%-*}"; hi="${p#*-}"
                for ((n = lo; n <= hi; n++)); do idxs+=("$n"); done
            else
                idxs+=("$p")
            fi
        done
        for n in "${idxs[@]}"; do
            [[ "$n" =~ ^[0-9]+$ ]] || { echo "ERROR: bad index '$n'" >&2; exit 2; }
            [ "$n" -ge 1 ] && [ "$n" -le "${#specs[@]}" ] \
                || { echo "ERROR: index $n out of range 1..${#specs[@]}" >&2; exit 2; }
            victims+=("${specs[$((n - 1))]}")
        done
        ;;
    id)
        for f in "${specs[@]}"; do
            [ "$(field "$f" '.id')" = "$sel" ] && victims+=("$f")
        done
        ;;
    key)
        for f in "${specs[@]}"; do
            [ "$(field "$f" '.citation_key')" = "$sel" ] && victims+=("$f")
        done
        ;;
    content_key)
        for f in "${specs[@]}"; do
            [ "$(field "$f" '.content_key')" = "$sel" ] && victims+=("$f")
        done
        ;;
esac

# Dedup victims (a comma index list could name the same file twice).
mapfile -t victims < <(printf '%s\n' "${victims[@]}" | awk 'NF' | sort -u)
[ "${#victims[@]}" -gt 0 ] || { echo "no $state jobs matched."; exit 1; }

echo "Will slice ${#victims[@]} job(s) from $state:"
i=1
for f in "${victims[@]}"; do print_row "$i" "$f"; i=$((i + 1)); done

if [ "$dry_run" = 1 ]; then echo "(dry-run — nothing changed)"; exit 0; fi

if [ "$assume_yes" = 0 ]; then
    printf 'Proceed? [y/N] '
    read -r ans
    case "$ans" in y|Y|yes|YES) ;; *) echo "aborted."; exit 1 ;; esac
fi

if [ "$purge" = 0 ]; then
    mkdir -p "$QUEUE_DIR/cancelled"
fi

sliced=0
for f in "${victims[@]}"; do
    # The spec may vanish if the drainer claimed it between listing and now;
    # mv/rm fail-fast on a missing file, so guard the race explicitly.
    [ -f "$f" ] || { echo "skip (already claimed): $(basename "$f")"; continue; }
    if [ "$purge" = 1 ]; then
        rm -f "$f" && sliced=$((sliced + 1))
    else
        mv "$f" "$QUEUE_DIR/cancelled/" && sliced=$((sliced + 1))
    fi
done

if [ "$purge" = 1 ]; then
    echo "purged $sliced job(s)."
else
    echo "moved $sliced job(s) to $QUEUE_DIR/cancelled/ (recoverable)."
fi
echo "pending: $(find "$QUEUE_DIR/pending" -maxdepth 1 -name '*.json' | wc -l)"
