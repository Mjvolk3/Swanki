#!/bin/bash
# scripts/dendron-tree.sh
# [[scripts.dendron-tree]]
# https://github.com/Mjvolk3/Swanki/tree/main/scripts/dendron-tree.sh

# Render the dot-delimited dendron note hierarchy as a visual tree.
#
# Usage:
#   bash scripts/dendron-tree.sh [-L depth] [prefix]
#
# Options:
#   -L N      Limit display depth (passed through to tree)
#   prefix    Filter to a subtree (e.g. swanki.processing)
#
# Examples:
#   bash scripts/dendron-tree.sh              # full hierarchy
#   bash scripts/dendron-tree.sh -L 2         # top two levels
#   bash scripts/dendron-tree.sh swanki.processing  # subtree only

set -euo pipefail

NOTES_DIR="notes"
TREE_ARGS=()
PREFIX=""

# Parse arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        -L)
            TREE_ARGS+=("-L" "$2")
            shift 2
            ;;
        *)
            PREFIX="$1"
            shift
            ;;
    esac
done

# Create temp directory for the tree structure
TMPDIR_TREE=$(mktemp -d)
trap 'rm -rf "$TMPDIR_TREE"' EXIT

# Build directory structure from dendron filenames
for f in "$NOTES_DIR"/*.md; do
    fname="${f##*/}"      # strip path
    fname="${fname%.md}"  # strip .md extension

    # If prefix is set, filter to matching notes and strip the prefix
    if [[ -n "$PREFIX" ]]; then
        case "$fname" in
            "$PREFIX"|"$PREFIX".*)
                # Strip prefix (and trailing dot if present) to show relative tree
                remaining="${fname#"$PREFIX"}"
                remaining="${remaining#.}"
                if [[ -z "$remaining" ]]; then
                    # Exact match -- represent as a leaf file
                    touch "$TMPDIR_TREE/$PREFIX"
                    continue
                fi
                fname="$remaining"
                ;;
            *)
                continue
                ;;
        esac
    fi

    # Convert dots to slashes and create directory structure
    dirpath="${fname//./\/}"
    mkdir -p "$TMPDIR_TREE/$dirpath"
done

# Run tree on the temp directory
if [[ -n "$PREFIX" ]]; then
    echo "$PREFIX"
    tree "$TMPDIR_TREE" "${TREE_ARGS[@]}" --noreport | tail -n +2
else
    tree "$TMPDIR_TREE" "${TREE_ARGS[@]}" --noreport | head -1 | sed 's|.*|dendron|'
    tree "$TMPDIR_TREE" "${TREE_ARGS[@]}" --noreport | tail -n +2
fi
