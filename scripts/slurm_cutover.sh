#!/usr/bin/env bash
#
# scripts/slurm_cutover.sh
# [[scripts.slurm_cutover]]
# https://github.com/Mjvolk3/Swanki/tree/main/scripts/slurm_cutover.sh
#
# USER-RUN cutover for the SLURM-native serverless-Fish migration. Dry-run by
# default: it PRINTS each step's command. Re-run with RUN=1 to execute. Several
# steps need sudo (slurmd/cgroup) and are marked [sudo]; some are destructive
# (decommission Docker Fish, retire the drainer) and are marked [DESTRUCTIVE].
# Read notes/runbook.slurm-cutover.md ([[runbook.slurm-cutover]]) first.
#
# Order matters: resume + isolate SLURM, prove 1-GPU isolation, build the image,
# measure cold start, run one paper end-to-end, and ONLY then decommission the
# live Docker Fish + drainer.
set -uo pipefail

RUN="${RUN:-0}"
GPUS="${SWANKI_QOS_GPUS:-1}"   # linear=1; parallel=N (QOS GrpTRES cap)
FISH_REPO="${SWANKI_FISH_REPO:-$HOME/Documents/projects/fish-speech}"
SIF="${SWANKI_FISH_SIF:-$FISH_REPO/fish-speech-server.sif}"
USER_NAME="${USER}"

step() {  # step "<label>" cmd args...
    local label="$1"; shift
    echo
    echo "=== $label ==="
    printf '  %q' "$@"; echo
    if [ "$RUN" = "1" ]; then "$@"; else echo "  (dry-run; set RUN=1 to execute)"; fi
}

echo "SLURM cutover — RUN=$RUN (dry-run unless RUN=1), QOS gpus=$GPUS"

# 1. Preflight (read-only).
step "preflight: node + gres" sinfo -N -o "%N %t %G"
step "preflight: cgroup device constraint" grep -i ConstrainDevices /etc/slurm/cgroup.conf

# 2. Resume the node (DOWN since the last reboot). [sudo]
step "[sudo] restart slurmd" sudo systemctl restart slurmd
step "[sudo] resume node" sudo scontrol update nodename=gilahyper state=resume reason=cutover

# 3. Acceptance gate: a 1-GPU job must see EXACTLY one GPU (cgroup isolation).
step "acceptance: 1-GPU isolation" srun --gres=gpu:1 --partition=main nvidia-smi -L

# 4. swanki account + QOS (linear/parallel knob = GrpTRES gres/gpu=N). [sudo]
step "[sudo] add swanki account" sudo sacctmgr -i add account swanki Description="swanki generation"
step "[sudo] add user to swanki account" sudo sacctmgr -i add user "$USER_NAME" account=swanki
step "[sudo] create swanki QOS" sudo sacctmgr -i add qos swanki
step "[sudo] cap swanki QOS to $GPUS GPU(s)" \
    sudo sacctmgr -i modify qos swanki set GrpTRES=gres/gpu="$GPUS"

# 5. Bake the Fish image (kills the ~2GB-per-start re-download) then build .sif.
#    Bake step = edit fish-speech/docker/Dockerfile so `uv sync` + model cache run
#    at BUILD time (see runbook), then:
step "build baked docker image" docker build -t fish-speech-server:cuda \
    -f "$FISH_REPO/docker/Dockerfile" "$FISH_REPO"
step "build apptainer .sif from docker image" \
    apptainer build "$SIF" docker-daemon://fish-speech-server:cuda

# 6. Cold-start measurement (one job; watch time-to-/v1/health in its log).
step "submit one paper (cold-start timing)" \
    env SWANKI_QUEUE_EXECUTOR=slurm "$HOME/Documents/projects/Swanki/scripts/swanki_enqueue.sh" \
        --pdf "${SAMPLE_PDF:-/path/to/sample.pdf}" --key "${SAMPLE_KEY:-sampleKey}"

# 7. ABS finalizer (singleton) after a batch.
step "submit ABS finalizer (singleton)" \
    sbatch "$HOME/Documents/projects/Swanki/scripts/swanki_finalize_abs.sbatch"

# 8. [DESTRUCTIVE] Decommission the out-of-band Docker Fish (frees the GPUs so
#    SLURM's view is accurate). Do this ONLY after step 6 proves serverless works.
step "[DESTRUCTIVE] stop Docker Fish fleet" docker stop fish-0 fish-1 fish-2 fish-3

# 9. [DESTRUCTIVE] Retire the bash drainer (SLURM is the scheduler now).
step "[DESTRUCTIVE] disable swanki-queue.service" \
    systemctl --user disable --now swanki-queue.service

echo
echo "Cutover steps printed. Re-run with RUN=1 once you have read the runbook."
