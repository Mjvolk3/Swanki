---
id: txffp856gae5hxzmio4inqa
title: Fish Speech S2 Pro TTS Experiment
desc: 'Timing and quality comparison of self-hosted Fish Speech vs ElevenLabs for luoWhenCausalInference2020'
updated: 1775234351567
created: 1775234351567
---

## Overview

Experiment comparing TTS providers for Swanki audio generation on `luoWhenCausalInference2020` (2-page causal inference paper, 8 cards).

**Infrastructure:**
- Machine: gilahyper (4x NVIDIA RTX 6000 Ada, 48GB each)
- Fish Speech S2 Pro (5B params) running via Docker on Slurm, 1 GPU
- ~20GB VRAM resident, single-threaded inference
- Voice: `british-prof` (cloned from ElevenLabs summary audio)

## Run 1: Fish Speech S2 Pro (random voice, no LaTeX humanization)

- **Date:** 2026-04-03
- **Config:** `models=fish_speech audio=all`, `chunk_length=200` (default), `max_new_tokens=1024` (default)
- **Voice:** random (no reference_id)
- **LaTeX humanization:** not yet added
- **Output:** `luoWhenCausalInference2020-fish_0/`
- **Status:** Completed (no timing captured -- first exploratory run)

## Run 2: Fish Speech S2 Pro (british-prof voice, with LaTeX humanization + prosody tags)

- **Date:** 2026-04-03
- **Config:** `models=fish_speech audio=all`, `chunk_length=200`, `max_new_tokens=1024`
- **Voice:** `british-prof` (registered reference)
- **LaTeX humanization:** two-pass (dedicated LLM pass before transcript)
- **Prosody tags:** Fish Speech inline `[pause]`, `[emphasis]`, `[excited]` in lecture prompt
- **Critic fix:** not yet applied (critic flagged prosody tags as meta-commentary)
- **Output:** `luoWhenCausalInference2020-fish_3/`

| Stage | Start | End | Duration |
|-------|-------|-----|----------|
| PDF + markdown + images + cards | 03:03 | 03:07 | ~4 min |
| Card audio (8 cards, 16 TTS calls) | 03:07 | 03:49 | ~42 min |
| Summary audio (8 TTS chunks) | 03:49 | 04:19 | ~30 min |
| Reading audio (5 TTS chunks) | 04:19 | 04:34 | ~15 min |
| Lecture (generate + 3x critique + 4 TTS chunks) | 04:34 | 04:47 | ~13 min |
| **Total** | **03:03** | **04:47** | **~1h 44m** |

**Observations:**
- TTS is the bottleneck: ~100 min of 104 min total
- Each TTS chunk takes ~2-5 min (Fish Speech inference on RTX 6000)
- GPU utilization spikes during inference, drops to 0% between requests (no batching/pipelining)
- Critic flagged `[pause]`/`[emphasis]` tags as meta-commentary (3 of 5 final issues)
- LaTeX humanization working well: "h of W equals zero", "X sub j", etc.

## Run 3: Fish Speech S2 Pro (chunk_length=500, max_new_tokens=2048, critic fix)

- **Date:** 2026-04-03 (pending)
- **Config:** `models=fish_speech audio=all`, `chunk_length=500`, `max_new_tokens=2048`
- **Changes since Run 2:**
  - Increased `chunk_length` 200 -> 500 (fewer internal iterations per TTS call)
  - Increased `max_new_tokens` 1024 -> 2048 (longer utterances per call)
  - Critic prompt now accepts Fish Speech prosody tags as valid
- **Output:** TBD
- **Hypothesis:** Larger chunks should reduce per-call overhead and total time

| Stage | Start | End | Duration |
|-------|-------|-----|----------|
| ... | | | |
| **Total** | | | |

## ElevenLabs Baseline (for comparison)

No ElevenLabs run on this paper from gilahyper (no prior data). Historical reference from M1 Mac runs: ElevenLabs typically completes a 2-page paper in ~10-15 min (API latency ~1-3s per chunk). Cost: ~$0.50-1.00 per paper depending on audio types.

## GPU Utilization Analysis

Fish Speech inference is **single-threaded, single-request**:
- LLAMA worker pulls one request from FIFO queue, processes it, then waits
- No dynamic batching, no request pipelining
- 0% GPU between requests is expected
- `--workers N` spawns separate processes (each loads full model ~20GB)
- With 48GB GPU: could fit `--workers 2` (~40GB) but adds complexity

**Potential speedups (not yet implemented):**
1. Concurrent HTTP requests from Swanki (asyncio/threading) to keep queue fed
2. Larger Swanki text chunks (currently 3000-4500 chars, model supports 32K context)
3. `--compile` flag for torch.compile optimization (one-time warmup cost)
