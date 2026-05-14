"""
swanki/voice_clone/__init__.py
[[swanki.voice_clone]]
https://github.com/Mjvolk3/Swanki/tree/main/swanki/voice_clone/__init__.py
Test file: tests/test_voice_clone.py

Voice-clone reference management for Fish Speech TTS. Handles persisting raw
YouTube extracts, denoising them with DeepFilterNet, and registering the
cleaned audio with the local Fish Speech server. Per-speaker on-disk layout::

    $SWANKI_MODELS/voice_refs/<speaker_id>/
        speaker.json
        clips/
            <YYYYMMDD>T<HHMM>-<slug>/
                original.wav
                denoised.wav
                transcript.txt
                clip.json

This shape is the unit we copy when cloning a new speaker from YouTube.
"""

from swanki.voice_clone.refs import (
    AudioFormat,
    DenoisingState,
    VoiceClip,
    VoiceSpeaker,
    YoutubeSource,
    clip_dir,
    clips_dir,
    iter_clips,
    list_clips,
    load_clip,
    load_speaker,
    preferred_audio,
    speaker_dir,
    voice_refs_root,
    write_clip,
    write_speaker,
)

__all__ = [
    "AudioFormat",
    "DenoisingState",
    "VoiceClip",
    "VoiceSpeaker",
    "YoutubeSource",
    "clip_dir",
    "clips_dir",
    "iter_clips",
    "list_clips",
    "load_clip",
    "load_speaker",
    "preferred_audio",
    "speaker_dir",
    "voice_refs_root",
    "write_clip",
    "write_speaker",
]
