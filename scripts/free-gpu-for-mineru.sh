#!/usr/bin/env bash
# scripts/free-gpu-for-mineru.sh
# [[scripts.free-gpu-for-mineru]]
#
# Stop the Fish Speech docker container bound to GPU device=3 / port 8083 so
# MinerU can use GPU 3 (CUDA_VISIBLE_DEVICES=3). Swanki's Fish discovery already
# defaults SWANKI_FISH_PORTS to "8080,8081,8082", so the 3 remaining servers are
# used automatically. This is an explicit operator action -- never auto-run.
set -euo pipefail

PORT="${1:-8083}"

CID="$(docker ps --filter "publish=${PORT}" -q | head -1)"
if [[ -z "${CID}" ]]; then
  echo "No running container publishes port ${PORT}; GPU may already be free."
  exit 0
fi

echo "Stopping Fish container ${CID} (port ${PORT}, GPU device=3)..."
docker stop "${CID}"
echo "GPU 3 is now free for MinerU. Fish runs on ports 8080-8082."
echo
echo "To restore the Fish server on GPU 3 later, re-run the original container, e.g.:"
echo "  docker run --rm --gpus device=3 -e COMPILE=1 \\"
echo "    -v /home/michaelvolk/Documents/projects/fish-speech/checkpoints:/app/checkpoints \\"
echo "    -v /home/michaelvolk/Documents/projects/fish-speech/references:/app/references \\"
echo "    -p 8083:8080 fish-speech-server:cuda"
echo "  (then unset SWANKI_FISH_PORTS or set it to 8080,8081,8082,8083)"
