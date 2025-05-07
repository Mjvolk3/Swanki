#!/usr/bin/env python3
from pathlib import Path
from typing import List
from elevenlabs.client import ElevenLabs
from pydub import AudioSegment
import os
from dotenv import load_dotenv
import time
import re


def text_to_speech(
    text: str, voice_id: str, output_dir: Path, chunk_index: int = 0
) -> Path:
    client = ElevenLabs(api_key=os.environ.get("ELEVEN_LABS_API_KEY"))
    output_path = output_dir / f"temp_audio_{chunk_index}.mp3"

    # Create voice settings as a dictionary
    voice_settings = {
        "stability": 0.5,            # Balanced stability
        "similarity_boost": 0.8,     # Strong voice identity
        "style": 0.15,               # Slight style enhancement for storytelling quality
        "use_speaker_boost": True,   # Maintain clarity
    }

    audio_stream = client.text_to_speech.convert(
        text=text,
        voice_id=voice_id,
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_192",
        voice_settings=voice_settings,
    )

    audio_data = (
        b"".join(audio_stream) if hasattr(audio_stream, "__iter__") else audio_stream
    )

    with open(output_path, "wb") as f:
        f.write(audio_data)

    return output_path


def chunk_text(text: str, max_chars: int = 3000) -> List[str]:
    if len(text) <= max_chars:
        return [text]

    # Split on paragraphs first
    paragraphs = text.split("\n\n")
    chunks = []
    current_chunk = ""

    for paragraph in paragraphs:
        # Look for natural pause points - ends of sentences
        if len(paragraph) > max_chars:
            # Split on sentence endings (., !, ?)
            sentence_breaks = [m.end() for m in re.finditer(r"[.!?]\s+", paragraph)]

            start = 0
            for end in sentence_breaks:
                part = paragraph[start:end]

                if len(current_chunk) + len(part) <= max_chars:
                    current_chunk += part
                else:
                    # Only break at sentence boundaries
                    chunks.append(current_chunk.strip())
                    current_chunk = part

                start = end

            # Add any remaining text
            if start < len(paragraph):
                remaining = paragraph[start:]
                if len(current_chunk) + len(remaining) <= max_chars:
                    current_chunk += remaining
                else:
                    chunks.append(current_chunk.strip())
                    current_chunk = remaining
        elif len(current_chunk) + len(paragraph) + 2 <= max_chars:  # +2 for "\n\n"
            current_chunk += paragraph + "\n\n"
        else:
            chunks.append(current_chunk.strip())
            current_chunk = paragraph + "\n\n"

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


def normalize_audio(audio: AudioSegment, target_dBFS: float = -20.0) -> AudioSegment:
    """Normalize audio to a consistent volume level."""
    if audio.dBFS == float("-inf"):  # Handle silent audio
        return audio
    change_in_dBFS = target_dBFS - audio.dBFS
    return audio.apply_gain(change_in_dBFS)


def smooth_volume_transitions(
    audio_segments: List[AudioSegment], crossfade_ms: int = 300
) -> AudioSegment:
    """Create a combined audio with smoother volume transitions between segments."""
    if not audio_segments:
        return AudioSegment.empty()

    # First normalize all segments to the same level
    normalized_segments = [normalize_audio(segment) for segment in audio_segments]

    # Apply pre-processing to reduce the "shouting" effect
    processed_segments = []
    for segment in normalized_segments:
        # Apply a slight compression to reduce dynamic range
        # This is a simplified approach - for real compression, consider using pydub's effects
        segment = segment.apply_gain(-2.0)  # Reduce overall volume slightly
        # Apply longer fades for smoother transitions
        segment = segment.fade_in(300).fade_out(300)
        processed_segments.append(segment)

    # Combine with longer crossfades
    combined = processed_segments[0]
    for segment in processed_segments[1:]:
        combined = combined.append(segment, crossfade=crossfade_ms)

    return combined


def apply_fade(audio: AudioSegment, duration_ms: int = 30) -> AudioSegment:
    return audio.fade_in(duration_ms).fade_out(duration_ms)


def combine_audio_files(file_paths: List[Path], output_path: Path) -> None:
    """Load audio files and combine them with smooth transitions."""
    audio_segments = [AudioSegment.from_mp3(file_path) for file_path in file_paths]

    # Apply the enhanced processing
    combined = smooth_volume_transitions(audio_segments)

    # Final normalization of the complete audio
    combined = normalize_audio(combined)

    # Add a slight fade at the very beginning and end
    combined = combined.fade_in(100).fade_out(100)

    # Export with higher quality settings
    combined.export(
        output_path,
        format="mp3",
        bitrate="192k",
        parameters=["-af", "aresample=resampler=soxr:precision=28:osf=s16"],
    )


def cleanup_temp_files(file_paths: List[Path]) -> None:
    """Remove temporary audio files."""
    for file_path in file_paths:
        if file_path.exists():
            os.remove(file_path)


def generate_audio_from_transcript(transcript_path: Path, output_dir: Path) -> Path:
    """Generate audio from a cleaned transcript file."""
    output_dir.mkdir(exist_ok=True)
    voice_id = "7p1Ofvcwsv7UBPoFNcpI"  # Using the specific voice ID provided

    with open(transcript_path, "r", encoding="utf-8") as f:
        transcript = f.read()

    print(f"Transcript length: {len(transcript)} characters")

    try:
        # Split transcript into chunks
        chunks = chunk_text(transcript, max_chars=3000)
        print(f"Split transcript into {len(chunks)} chunks")

        audio_paths = []

        # Process each chunk
        for i, chunk in enumerate(chunks):
            print(f"Processing chunk {i+1}/{len(chunks)} ({len(chunk)} characters)")
            audio_path = text_to_speech(chunk, voice_id, output_dir, i)
            audio_paths.append(audio_path)

            # Pause between API calls to avoid rate limiting
            if i < len(chunks) - 1:
                print("Pausing for 2 seconds...")
                time.sleep(2)

        # Create final output path
        final_path = output_dir / "final_transcript.mp3"
        print(f"Combining {len(audio_paths)} audio files...")
        combine_audio_files(audio_paths, final_path)

        # Cleanup temp files
        print("Cleaning up temporary files...")
        cleanup_temp_files(audio_paths)

        print(f"Successfully generated audio at: {final_path}")
        return final_path

    except Exception as e:
        print(f"Error generating audio: {e}")
        raise


def test_generate_audio():
    """Test function to generate audio from a transcript file."""
    # Load environment variables
    load_dotenv()

    # Print API key existence (not the actual key)
    if os.environ.get("ELEVEN_LABS_API_KEY"):
        print("ELEVEN_LABS_API_KEY found in environment")
    else:
        print("ERROR: ELEVEN_LABS_API_KEY not found in environment!")
        return

    # File paths
    transcript_path = Path(
        "/Users/michaelvolk/Documents/projects/Swanki/swanki-out/transcript-clean-output.md"
    )
    output_dir = Path("/Users/michaelvolk/Documents/projects/Swanki/swanki-out/audio")

    # Check if transcript file exists
    if not transcript_path.exists():
        print(f"ERROR: Transcript file not found at {transcript_path}")
        return

    print(f"Transcript file found at {transcript_path}")

    try:
        final_path = generate_audio_from_transcript(transcript_path, output_dir)
        print(f"Audio generated successfully at: {final_path}")
    except Exception as e:
        print(f"Failed to generate audio: {e}")


if __name__ == "__main__":
    test_generate_audio()
