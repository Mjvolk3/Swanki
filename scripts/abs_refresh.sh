#!/usr/bin/env bash
#
# scripts/abs_refresh.sh
# [[scripts.abs_refresh]]
# https://github.com/Mjvolk3/Swanki/tree/main/scripts/abs_refresh.sh
#
# Exec shim: the 7-step refresh orchestration moved into the package
# (swanki/abs/refresh.py, `python -m swanki.abs refresh`). This wrapper keeps
# the historical entry point alive for the cron line, the legacy one-off
# publish scripts, and muscle memory -- without touching crontab.
#
# Lock modes (now enforced by fcntl.flock in Python on the SAME
# /tmp/abs-refresh.lock, so in-flight runs of old and new worlds still
# exclude each other; this shim carries no lock of its own):
#   default   non-blocking: skip if a run is already in progress (cron path).
#   --wait    block until the lock frees (delivery path).

set -euo pipefail

PY="${ABS_REFRESH_PY:-$HOME/miniconda3/envs/swanki/bin/python}"
SWANKI_DIR="${ABS_REFRESH_SWANKI_DIR:-$HOME/Documents/projects/Swanki}"

cd "$SWANKI_DIR"
exec "$PY" -m swanki.abs refresh "$@"
