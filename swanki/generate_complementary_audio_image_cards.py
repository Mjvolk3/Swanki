#!/usr/bin/env python3
"""
Module to convert image card transcripts into MP3 audio files using ElevenLabs TTS.
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


def generate_audio_from_image_card_transcripts(
    transcript_dir: str, audio_dir: str, voice_id: str
) -> None:
    """Read all cleaned image card transcript MD files, generate and save MP3s."""
    load_dotenv()
    api_key = os.getenv("ELEVEN_LABS_API_KEY")
    if not api_key:
        raise RuntimeError("ELEVEN_LABS_API_KEY not set in environment.")
    os.makedirs(audio_dir, exist_ok=True)

    vid = voice_id or DEFAULT_VOICE_ID

    # Get all clean transcript files (not input or raw files)
    transcript_files = [
        f
        for f in sorted(os.listdir(transcript_dir))
        if f.endswith(".md")
        and not f.endswith("_input.md")
        and not f.endswith("_raw.md")
    ]

    print(f"Found {len(transcript_files)} transcript files to process")

    for md in transcript_files:
        name = Path(md).stem
        txt_path = Path(transcript_dir) / md
        with open(txt_path, "r", encoding="utf-8") as f:
            text = f.read().strip()

        if not text:
            print(f"Skipping empty transcript: {md}")
            continue

        print(f"Processing: {md} ({len(text)} chars)")

        # Split into manageable chunks for API
        chunks = chunk_text(text)
        paths: List[Path] = []

        # Process each chunk
        for i, chunk in enumerate(chunks, start=1):
            out_chunk = Path(audio_dir) / f"{name}_temp_{i}.mp3"
            print(f"  Generating chunk {i}/{len(chunks)}")

            try:
                text_to_speech(chunk, vid, out_chunk, api_key)
                paths.append(out_chunk)
                # Small pause to avoid rate limiting
                time.sleep(1)
            except Exception as e:
                print(f"  Error processing chunk {i}: {e}")

        if not paths:
            print(f"  No audio generated for {md}")
            continue

        # Combine chunks into final audio
        final = Path(audio_dir) / f"{name}.mp3"
        print(f"  Combining {len(paths)} chunks into final audio")

        if len(paths) > 1:
            try:
                combine_audio(paths, final)
                # Clean up temp files
                for p in paths:
                    os.remove(p)
            except Exception as e:
                print(f"  Error combining audio: {e}")
        else:
            # Just rename the single chunk
            paths[0].replace(final)

        print(f"  Completed: {final}")


def main():
    """Main entry point for the script."""
    print("Starting image card audio generation")

    # Paths for image card transcripts and audio
    transcript_dir = "pan-transcriptome/anki-image-cards-complementary-audio-transcript"
    audio_dir = "pan-transcriptome/anki-image-cards-complementary-audio"
    voice_id = DEFAULT_VOICE_ID

    generate_audio_from_image_card_transcripts(transcript_dir, audio_dir, voice_id)
    print(f"Audio generation complete. Files saved to {audio_dir}")


if __name__ == "__main__":
    main()
