#!/usr/bin/env python3
"""
Module to convert cleaned transcripts (front/back) into MP3 audio files using ElevenLabs TTS.
"""
import os
from pathlib import Path
from typing import List
from dotenv import load_dotenv
from elevenlabs import ElevenLabs, VoiceSettings
from pydub import AudioSegment
import tiktoken
import time
import re

# Default ElevenLabs voice ID (replace if needed)
DEFAULT_VOICE_ID = "7p1Ofvcwsv7UBPoFNcpI"


def chunk_text(text: str, max_chars: int = 3000) -> List[str]:
    """Split text into chunks of up to max_chars without breaking words or sentences."""
    paragraphs = text.split("\n\n")
    chunks: List[str] = []
    current = ""
    for p in paragraphs:
        if len(current) + len(p) + 2 <= max_chars:
            current = (current + "\n\n" + p).strip()
        else:
            if current:
                chunks.append(current)
            if len(p) <= max_chars:
                current = p
            else:
                sentences = re.split(r"(?<=[.!?]) +", p)
                part = ""
                for s in sentences:
                    if len(part) + len(s) + 1 <= max_chars:
                        part = (part + " " + s).strip()
                    else:
                        chunks.append(part)
                        part = s
                if part:
                    chunks.append(part)
                current = ""
    if current:
        chunks.append(current)
    return chunks


def text_to_speech(text: str, voice_id: str, output_path: Path, api_key: str) -> None:
    """Convert a text chunk to speech and save as MP3."""
    client = ElevenLabs(api_key=api_key)
    settings = VoiceSettings(
        stability=0.5, similarity_boost=0.75, style=0.2, use_speaker_boost=True
    )
    stream = client.text_to_speech.convert(
        text=text,
        voice_id=voice_id,
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_192",
        voice_settings=settings,
    )
    data = b"".join(stream) if hasattr(stream, "__iter__") else stream
    with open(output_path, "wb") as f:
        f.write(data)


def combine_audio(files: List[Path], output: Path) -> None:
    """Combine multiple MP3 files into one with smooth fades."""
    segments = [AudioSegment.from_mp3(str(f)) for f in files]
    combined = segments[0]
    for seg in segments[1:]:
        combined = combined.append(seg, crossfade=200)
    combined.export(str(output), format="mp3", bitrate="192k")


def generate_audio_from_transcripts(
    transcript_dir: str, audio_dir: str, voice_id: str
) -> None:
    """Read all cleaned transcript MD in transcript_dir, generate and save MP3s in audio_dir."""
    load_dotenv()
    api_key = os.getenv("ELEVEN_LABS_API_KEY")
    if not api_key:
        raise RuntimeError("ELEVEN_LABS_API_KEY not set in environment.")
    os.makedirs(audio_dir, exist_ok=True)

    vid = voice_id or DEFAULT_VOICE_ID

    for md in sorted(os.listdir(transcript_dir)):
        # skip non-cleaned and intermediate transcripts
        if not md.endswith(".md") or md.endswith("_input.md") or md.endswith("_raw.md"):
            continue
        name = Path(md).stem
        txt = Path(transcript_dir) / md
        with open(txt, "r", encoding="utf-8") as f:
            text = f.read().strip()
        chunks = chunk_text(text)
        paths: List[Path] = []
        for i, chunk in enumerate(chunks, start=1):
            out_chunk = Path(audio_dir) / f"{name}_{i}.mp3"
            text_to_speech(chunk, vid, out_chunk, api_key)
            paths.append(out_chunk)
            time.sleep(1)
        # combine into final audio per card side
        final = Path(audio_dir) / f"{name}.mp3"
        if len(paths) > 1:
            combine_audio(paths, final)
            for p in paths:
                os.remove(p)
        else:
            paths[0].replace(final)


if __name__ == "__main__":
    # Hardcoded test paths
    transcript_dir = "pan-transcriptome/gen-md-complementary-audio-transcript"
    audio_dir = "pan-transcriptome/gen-md-complementary-audio"
    voice_id = DEFAULT_VOICE_ID
    generate_audio_from_transcripts(transcript_dir, audio_dir, voice_id)
    print(f"Generated audio in {audio_dir}")
