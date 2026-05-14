"""
swanki/voice_clone/refs.py
[[swanki.voice_clone.refs]]
https://github.com/Mjvolk3/Swanki/tree/main/swanki/voice_clone/refs.py
Test file: tests/test_voice_clone_refs.py

Pydantic models + path helpers for voice-clone references. Each speaker has a
directory under ``$SWANKI_MODELS/voice_refs/<speaker_id>/`` containing a
``speaker.json`` and a ``clips/`` subdir with one folder per extracted clip.

Layout::

    voice_refs/
        <speaker_id>/
            speaker.json
            clips/
                <YYYYMMDD>T<HHMM>-<slug>/
                    original.wav
                    denoised.wav
                    transcript.txt
                    clip.json
                ...

This shape is the unit we copy when cloning a new speaker from YouTube: pull
clip with yt-dlp, persist original.wav + transcript.txt + clip.json, optionally
denoise, register with Fish Speech.
"""

import json
import os
import re
from pathlib import Path

from pydantic import BaseModel, Field

DEFAULT_SWANKI_MODELS = "/scratch/projects/torchcell-scratch/Swanki_Models"

CLIP_ID_PATTERN = re.compile(r"^\d{8}T\d{4}-[a-z0-9-]+$")


class YoutubeSource(BaseModel):
    type: str = "youtube"
    url: str
    playlist_url: str | None = None
    title_hint: str | None = None
    start_timestamp: str
    end_timestamp: str
    duration_seconds: int


class AudioFormat(BaseModel):
    sample_rate_hz: int = 24000
    channels: int = 1
    encoding: str = "pcm_s16le"
    format: str = "wav"


class DenoisingState(BaseModel):
    applied: bool = False
    method: str | None = None
    model: str | None = None
    notes: str | None = None


class VoiceClip(BaseModel):
    """One reference clip: source media, audio params, denoising state, transcript."""

    clip_id: str
    source: YoutubeSource
    audio: AudioFormat = Field(default_factory=AudioFormat)
    yt_dlp_command: str | None = None
    denoising: DenoisingState = Field(default_factory=DenoisingState)
    transcript: str
    fish_speech_reference_id: str | None = None
    created: str
    history: list[str] = Field(default_factory=list)


class VoiceSpeaker(BaseModel):
    """A speaker with one or more reference clips."""

    speaker_id: str
    speaker_name: str
    active_clip_id: str | None = None
    notes: str | None = None


def voice_refs_root() -> Path:
    """Root dir for all voice references. Honors $SWANKI_MODELS, else default."""
    root = os.environ.get("SWANKI_MODELS", DEFAULT_SWANKI_MODELS)
    return Path(root) / "voice_refs"


def speaker_dir(speaker_id: str) -> Path:
    """Per-speaker dir under voice_refs_root()."""
    return voice_refs_root() / speaker_id


def clips_dir(speaker_id: str) -> Path:
    """Clips subdir under a speaker."""
    return speaker_dir(speaker_id) / "clips"


def clip_dir(speaker_id: str, clip_id: str) -> Path:
    """Per-clip dir."""
    return clips_dir(speaker_id) / clip_id


def load_speaker(speaker_id: str) -> VoiceSpeaker:
    """Load speaker.json from disk."""
    path = speaker_dir(speaker_id) / "speaker.json"
    assert path.exists(), f"missing speaker.json at {path}"
    return VoiceSpeaker.model_validate_json(path.read_text())


def write_speaker(speaker: VoiceSpeaker) -> Path:
    """Persist speaker.json."""
    d = speaker_dir(speaker.speaker_id)
    d.mkdir(parents=True, exist_ok=True)
    path = d / "speaker.json"
    path.write_text(speaker.model_dump_json(indent=2) + "\n")
    return path


def list_clips(speaker_id: str) -> list[str]:
    """Return clip_ids for a speaker, sorted lexicographically (chronological)."""
    cdir = clips_dir(speaker_id)
    if not cdir.is_dir():
        return []
    return sorted(p.name for p in cdir.iterdir() if p.is_dir() and CLIP_ID_PATTERN.match(p.name))


def load_clip(speaker_id: str, clip_id: str) -> VoiceClip:
    """Load clip.json for a specific clip."""
    path = clip_dir(speaker_id, clip_id) / "clip.json"
    assert path.exists(), f"missing clip.json at {path}"
    return VoiceClip.model_validate_json(path.read_text())


def write_clip(speaker_id: str, clip: VoiceClip) -> Path:
    """Persist clip.json next to a clip's audio files."""
    d = clip_dir(speaker_id, clip.clip_id)
    d.mkdir(parents=True, exist_ok=True)
    path = d / "clip.json"
    path.write_text(clip.model_dump_json(indent=2) + "\n")
    return path


def iter_clips(speaker_id: str):
    """Yield (clip_id, VoiceClip) pairs for a speaker, oldest first."""
    for cid in list_clips(speaker_id):
        yield cid, load_clip(speaker_id, cid)


def preferred_audio(speaker_id: str, clip_id: str) -> Path:
    """Return the denoised wav if present, else the original."""
    d = clip_dir(speaker_id, clip_id)
    denoised = d / "denoised.wav"
    return denoised if denoised.exists() else (d / "original.wav")
