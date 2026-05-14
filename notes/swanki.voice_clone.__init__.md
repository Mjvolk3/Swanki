---
id: za7a3pblylkqsioyjjv25aj
title: __init__
desc: ''
updated: 1777575443726
created: 1777575443726
---

## 2026.04.30 - New voice-clone management package

Introduces a per-speaker, multi-clip layout for Fish Speech voice references so we can iterate on clip selections (try a 30 s snippet, denoise it, A/B against the previous, etc.) without losing prior takes. The Hamming-book project drove this: the original 9:30–10:00 reference clip from Hamming's NPS 1995 lecture had usable prosody but produced lectures with awkward intonation; pulling a second 22:09–22:40 clip and registering it alongside (rather than overwriting) gave us a clean A/B and let us pick the better-sounding clone without re-extracting if we later want the older one.

The on-disk layout is what we copy when cloning a new speaker from YouTube:

```
$SWANKI_MODELS/voice_refs/<speaker_id>/
    speaker.json
    clips/
        <YYYYMMDD>T<HHMM>-<slug>/
            original.wav
            denoised.wav
            transcript.txt
            clip.json
        <YYYYMMDD>T<HHMM>-<slug>/
            ...
```

Module re-exports the pydantic models (`VoiceSpeaker`, `VoiceClip`, `YoutubeSource`, `AudioFormat`, `DenoisingState`) and the path helpers (`speaker_dir`, `clip_dir`, `load_speaker`, `load_clip`, `write_speaker`, `write_clip`, `iter_clips`, `preferred_audio`) so callers can iterate over a speaker's clips and pick the one that sounds best:

```python
from swanki.voice_clone import iter_clips, preferred_audio
for clip_id, clip in iter_clips("hamming"):
    print(clip_id, clip.fish_speech_reference_id, preferred_audio("hamming", clip_id))
```

Companion modules: `swanki.voice_clone.refs` (schema), `swanki.voice_clone.denoise` (DeepFilterNet wrapper). Companion CLI: [[scripts.clone_voice_from_youtube]] for end-to-end YouTube → denoise → register.

