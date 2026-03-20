---
id: tts-open-source-plan-2026
title: Open-Source TTS
desc: 'Replace ElevenLabs with open-source TTS models running on GPU workstation via Docker/Slurm'
updated: 1774051200000
created: 1774051200000
---

# Plan: Replace ElevenLabs with Open-Source TTS

## Context

ElevenLabs costs are unsustainable for the volume of academic audio being generated (20+ papers with lecture/summary/reading audio each). The team has 4x NVIDIA Ada RTX 6000 GPUs (48GB VRAM each, 192GB total) available for local inference. Goal: find the highest-quality open-source TTS model that can produce a British academic educator voice, integrate it into the Swanki pipeline, and run `co-biotech2026.sh` without ElevenLabs.

## Phase 1: Model Shootout (3 candidates, same test text)

Generate the same ~500-word academic paragraph with each model, compare quality subjectively.

### Candidate 1: F5-TTS (Primary recommendation)

- **Why**: Best-in-class voice cloning from 3-10s reference audio. Non-autoregressive (flow-matching DiT), so fast inference. Trained on 100K hours. Can clone a specific British academic voice from a sample recording.
- **VRAM**: ~8-16GB -- fits easily on one RTX 6000
- **Voice strategy**: Record or source a 10-second British academic voice sample, clone it
- **License**: Open source (MIT-like)
- **HF**: `SWivid/F5-TTS` (1.15k likes, 884k downloads)
- **Install**: `pip install f5-tts`

### Candidate 2: Kokoro-82M (Speed/simplicity baseline)

- **Why**: #1 on HuggingFace TTS Arena for open-weight models despite only 82M params. Has **built-in British English voices** -- no voice cloning needed. 96x real-time on GPU. Apache 2.0.
- **VRAM**: <2GB -- can run 20+ instances in parallel
- **Voice strategy**: Use pre-trained British voice preset (e.g., `bf_emma`, `bm_george`)
- **Limitation**: No voice cloning -- stuck with pre-trained voices
- **HF**: `hexgrad/Kokoro-82M` (5.82k likes, 8.99M downloads -- most popular)
- **Install**: `pip install kokoro`

### Candidate 3: Fish Audio S2 Pro (Quality ceiling)

- **Why**: Best raw benchmarks (beats Seed-TTS, MiniMax). 5B params, Dual-AR architecture. Voice cloning. Updated 8 days ago on HF.
- **VRAM**: ~17-24GB -- fits on one RTX 6000
- **Voice strategy**: Voice cloning from reference audio
- **License**: Check HF page -- may have commercial restrictions
- **HF**: `fishaudio/s2-pro` (653 likes, 5B params)

### Honorable mentions (try if top 3 don't satisfy)

- **Chatterbox** (ResembleAI) -- 2.24M downloads, voice cloning, well-tested
- **Zonos v0.1** (Zyphra) -- emotion/prosody control, 200K hours training, Apache 2.0
- **VibeVoice-1.5B** (Microsoft) -- brand new (Jan 2026), 3B params, 217k downloads

### Shootout procedure

1. Pick one academic paragraph from an existing lecture transcript (e.g., thornburg paper)
2. On the GPU machine via Slurm, run each model in its Docker container
3. For each model, generate two variants:
   - **Kokoro**: built-in British voice presets (`bf_emma`, `bm_george`)
   - **F5-TTS**: clone from a British academic voice sample (source a 10-30s clip)
   - **Fish S2 Pro**: clone from the same British voice sample
4. Compare: naturalness, pronunciation of technical terms, British accent quality, prosody
5. Pick winner (and voice approach: pre-trained vs cloned)

## Phase 2: Swanki Integration (~50 lines changed)

### Architecture: Dispatch inside `text_to_speech()` + HTTP server on GPU machine

**Key insight**: Keep the `text_to_speech()` signature identical. All 12+ call sites across card.py, summary.py, reading.py, lecture.py unchanged. Dispatch internally based on a module-level provider setting.

### Changes to `swanki/audio/_common.py`

1. **Add `strip_ssml(text)`** -- regex to remove `<break time="..." />` tags (~5 lines). Open-source models don't support SSML; `add_tts_pauses()` keeps generating them for ElevenLabs compat.

2. **Add module-level state + `configure_tts_provider()`**:

   ```python
   _tts_provider: str = "elevenlabs"
   _tts_server_url: str | None = None

   def configure_tts_provider(provider: str, server_url: str | None = None) -> None:
       global _tts_provider, _tts_server_url
       _tts_provider = provider
       _tts_server_url = server_url
   ```

3. **Add `_text_to_speech_local()`** -- HTTP POST to the GPU server:

   ```python
   def _text_to_speech_local(text: str, output_path: Path, speed: float, tts_model: str) -> None:
       text = strip_ssml(text)
       response = httpx.post(
           f"{_tts_server_url}/v1/audio/speech",
           json={"input": text, "model": tts_model, "speed": speed},
           timeout=300.0,
       )
       response.raise_for_status()
       output_path.write_bytes(response.content)
   ```

4. **Add dispatch at top of `text_to_speech()`**:

   ```python
   if _tts_provider == "local":
       _text_to_speech_local(text, output_path, speed, tts_model)
       return
   # ... existing ElevenLabs code unchanged ...
   ```

### Changes to `swanki/pipeline/pipeline.py`

One line after `tts_config` is read (~line 1857):

```python
from swanki.audio._common import configure_tts_provider
configure_tts_provider(
    provider=tts_config.get("provider", "elevenlabs"),
    server_url=tts_config.get("server_url"),
)
```

### New file: `swanki/conf/models/local_tts.yaml`

```yaml
models:
  tts:
    provider: local
    server_url: http://gpu-machine:8000
    model: f5-tts            # or kokoro, depending on shootout winner
    voice_id: null
    lecture_model: null       # same model for all types (no cost differential)
    stability: 0.5
    similarity_boost: 0.5
```

Switch via: `swanki ... models=local_tts`

### Files NOT changed

- `card.py`, `summary.py`, `reading.py`, `lecture.py` -- zero changes
- `generate_bookend_audio()` -- calls `text_to_speech()` which dispatches internally
- `add_tts_pauses()` -- keeps generating SSML (stripped by local provider path)

## Phase 3: Dockerized TTS Server (Slurm-managed)

### Architecture

Docker container running FastAPI + chosen TTS model(s). Submitted as a Slurm job on the workstation. Swanki on Mac hits the container's HTTP endpoint over the network.

### Directory structure

```
docker/tts-server/
├── Dockerfile
├── requirements.txt
├── server.py              # FastAPI app
├── voices/                # Reference audio clips for voice cloning
│   └── british_academic.wav
└── slurm_tts.sh           # sbatch script
```

### `server.py` -- FastAPI TTS server

- `POST /v1/audio/speech` -- main endpoint, returns MP3 bytes
  - Body: `{"input": "...", "model": "f5-tts|kokoro|s2-pro", "speed": 1.0, "voice": "british_academic"}`
- `GET /health` -- readiness check
- Loads model(s) into GPU memory at startup
- Multiple model endpoints possible (serve both Kokoro and F5-TTS behind different `model` values for A/B testing)

### `Dockerfile`

- Base: `nvidia/cuda:12.x-runtime-ubuntu22.04`
- Install: Python 3.11+, PyTorch, chosen TTS lib(s), FastAPI, uvicorn
- Copy `server.py` + `voices/`
- Expose port 8000
- `CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]`

### `slurm_tts.sh`

```bash
#!/bin/bash
#SBATCH --job-name=tts-server
#SBATCH --gres=gpu:1              # 1 GPU sufficient for any single model
#SBATCH --mem=32G
#SBATCH --time=24:00:00           # long-running server
#SBATCH --output=tts-server-%j.log

# Build or pull container, then run
docker run --gpus '"device=0"' -p 8000:8000 \
  -v /path/to/voices:/app/voices \
  swanki-tts-server:latest
```

Submit: `sbatch slurm_tts.sh` -- server stays up for the batch run duration.

### Multi-model support

The container can serve multiple models simultaneously if VRAM allows:

- Kokoro (82M, <2GB) + F5-TTS (~16GB) = ~18GB -- fits on one RTX 6000
- This enables A/B testing by switching `model` in the request body without redeploying

## Phase 4: End-to-End Test

1. `sbatch slurm_tts.sh` on workstation -- container starts, serves on port 8000
2. Update `local_tts.yaml` with workstation IP/port
3. On Mac, run single paper: `swanki pdf_path=... citation_key=thornburg... models=local_tts audio=all`
4. Compare output quality against existing ElevenLabs audio in `Swanki_Data/thornburgBringingGeneticallyMinimal2026/`
5. If quality acceptable, run full `co-biotech2026.sh` with `models=local_tts`

## Verification

- [ ] Shootout: generate same text with all 3 models, pick winner
- [ ] Unit test: `text_to_speech()` dispatches to local provider when configured
- [ ] Integration: single paper generates all audio types via local TTS server
- [ ] Quality: A/B compare lecture audio against ElevenLabs version
- [ ] Batch: `co-biotech2026.sh` completes without errors using `models=local_tts`

## Critical Files

| File                                   | Change                                                                               |
|----------------------------------------|--------------------------------------------------------------------------------------|
| `swanki/audio/_common.py`              | Add `strip_ssml`, `configure_tts_provider`, `_text_to_speech_local`, dispatch branch |
| `swanki/pipeline/pipeline.py`          | One-line `configure_tts_provider()` call                                             |
| `swanki/conf/models/local_tts.yaml`    | New Hydra config for local TTS                                                       |
| `docker/tts-server/Dockerfile` (new)   | CUDA + TTS model container                                                           |
| `docker/tts-server/server.py` (new)    | FastAPI server wrapping chosen model(s)                                              |
| `docker/tts-server/slurm_tts.sh` (new) | Slurm batch script to launch container                                               |
| `swanki/conf/models/default.yaml`      | Reference only, no changes                                                           |
