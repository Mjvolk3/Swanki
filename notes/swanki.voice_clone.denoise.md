---
id: y6h6ukyr5gzqcttz5u2kjjd
title: Denoise
desc: ''
updated: 1777575456683
created: 1777575456683
---

## 2026.04.30 - DeepFilterNet wrapper for archival voice-clone references

Thin wrapper around DeepFilterNet3. Voice clips pulled from old YouTube uploads carry tape hiss, room tone, and broadband noise that Fish Speech otherwise picks up as part of the speaker identity — a noisy reference produces a noisy clone. DFN3 cleans those without flattening the prosody we actually want to keep (breath patterns, pitch inflection).

Bypasses `df.io.load_audio` / `df.io.save_audio` because DFN 0.5.6 imports paths removed in modern torchaudio (`torchaudio.backend.common.AudioMetaData`, `torchaudio.info`). Instead we:

1. Stub `torchaudio.backend.common.AudioMetaData` via `sys.modules` so `df`'s import chain resolves.
2. Read the input wav with `soundfile`, build a torch tensor, optionally resample with `torchaudio.functional.resample` to DFN's target sample rate.
3. Call `enhance(model, df_state, audio_t)` directly — that's the only DFN entry point we need.
4. Write the cleaned tensor back via `soundfile.write` as `PCM_16`.

The shim approach is more robust than pinning `torchaudio<2.0` because DFN itself doesn't require the removed APIs at the inference layer; only its convenience I/O wrappers did. Returns a small dict (`{"method": "deepfilternet", "model": "DeepFilterNet3"}`) suitable for stamping into a `VoiceClip.denoising` block so downstream code can tell which clips have been processed.

