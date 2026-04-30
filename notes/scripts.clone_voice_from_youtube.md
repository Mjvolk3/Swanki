---
id: pvtjpb6zcxbntiorir0mmu3
title: Clone_voice_from_youtube
desc: ''
updated: 1777575463166
created: 1777575463166
---

## 2026.04.30 - End-to-end YouTube voice cloning CLI

Wraps the [[swanki.voice_clone]] package into a single command for cloning a new speaker:

```bash
python scripts/clone_voice_from_youtube.py \
  --voice-id hamming-denoised \
  --speaker "Richard Hamming" \
  --url "https://www.youtube.com/watch?v=AD4b-52jtos" \
  --start 9:30 --end 10:00 \
  --transcript-file ./transcript.txt \
  --denoise --register
```

Steps in order:

1. `extract_youtube_clip` — `yt-dlp --download-sections "*<start>-<end>" --force-keyframes-at-cuts -x --audio-format wav --postprocessor-args "ffmpeg:-ac 1 -ar <sr>"` writes `original.wav` into the per-clip dir. The full command string is preserved in `clip.json.yt_dlp_command` so we can reproduce or tweak later.
2. Persist the verbatim transcript to `transcript.txt` — Fish Speech's reference_text must match what's actually said in the audio (typos, stutters, repeats and all), or the clone drifts.
3. Optionally denoise via [[swanki.voice_clone.denoise]] writing `denoised.wav` next to the original.
4. Optionally register on the local Fish Speech server (`POST /v1/references/add`) under the `--voice-id`. Idempotent — re-uploads do not re-register.
5. Write `clip.json` with `VoiceClip` schema (source URL, timestamps, denoising state, transcript, registered reference id, history).

Each invocation creates a separate clip dir under `voice_refs/<speaker>/clips/<id>/`, so you can iterate on clip selection without losing prior takes — pull a different segment, register it under a new id, A/B against the previous, switch the active one in `swanki/conf/models/fish_speech_<speaker>.yaml`.

