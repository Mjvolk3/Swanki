---
id: wbefdkgxcrxcb2a6ui3e70q
title: Refs
desc: ''
updated: 1777575450216
created: 1777575450216
---

## 2026.04.30 - Schema + path helpers for multi-clip voice references

Two pydantic models capture what we need to know about a cloned voice without rummaging through the filesystem:

- `VoiceClip` — one extracted reference clip: source URL, `start_timestamp` / `end_timestamp` in `HH:MM:SS`, `audio` format (sample rate / channels / encoding), the verbatim `yt_dlp_command` we ran to fetch it, denoising state (method + model + notes), the transcript, and the `fish_speech_reference_id` it was registered under.
- `VoiceSpeaker` — the speaker, identified by `speaker_id` and human-readable `speaker_name`, with an `active_clip_id` pointing at the clip currently wired into `swanki/conf/models/fish_speech_<speaker>.yaml`. Optional `notes` field records traits worth remembering (e.g. "voice is naturally breathy on this old recording — Fish Speech reproduces breath patterns when [pause] tags fire").

`CLIP_ID_PATTERN` enforces `<YYYYMMDD>T<HHMM>-<slug>` so directory listings sort chronologically and the latest clip is the lexicographically-last entry. The slug is kebab-case for filesystem safety.

Path helpers honor `$SWANKI_MODELS` (default `/scratch/projects/torchcell-scratch/Swanki_Models`):

- `speaker_dir(speaker_id)` -> `$SWANKI_MODELS/voice_refs/<speaker_id>/`
- `clips_dir(speaker_id)` -> `<speaker_dir>/clips/`
- `clip_dir(speaker_id, clip_id)` -> `<clips_dir>/<clip_id>/`

Persistence helpers serialize the pydantic models to disk (`write_speaker`, `write_clip`) and load them back (`load_speaker`, `load_clip`). `list_clips` returns the sorted clip ids so future iteration calls have a stable order. `iter_clips` is a generator yielding `(clip_id, VoiceClip)` pairs. `preferred_audio` returns the denoised wav if present else the original — callers don't have to reason about denoising state.

