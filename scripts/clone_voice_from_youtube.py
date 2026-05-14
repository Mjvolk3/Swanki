"""
scripts/clone_voice_from_youtube.py
[[scripts.clone_voice_from_youtube]]
https://github.com/Mjvolk3/Swanki/tree/main/scripts/clone_voice_from_youtube.py

End-to-end CLI: extract a voice-clone reference clip from YouTube, persist the
original alongside its transcript and metadata under
``$SWANKI_MODELS/voice_refs/<voice_id>/``, optionally denoise with
DeepFilterNet, and (optionally) register the cleaned audio with the local
Fish Speech server.

Example:

    conda activate swanki
    python scripts/clone_voice_from_youtube.py \\
        --voice-id hamming-denoised \\
        --speaker "Richard Hamming" \\
        --url "https://www.youtube.com/watch?v=AD4b-52jtos" \\
        --start 9:30 --end 10:00 \\
        --transcript-file ./transcript.txt \\
        --denoise \\
        --register
"""

import argparse
import json
import os
import shutil
import subprocess
from datetime import date
from pathlib import Path

from swanki.voice_clone.refs import (
    AudioFormat,
    DenoisingState,
    FishSpeechState,
    VoiceRefMetadata,
    YoutubeSource,
    voice_ref_dir,
)


def _seconds(stamp: str) -> int:
    parts = [int(p) for p in stamp.split(":")]
    if len(parts) == 2:
        return parts[0] * 60 + parts[1]
    if len(parts) == 3:
        return parts[0] * 3600 + parts[1] * 60 + parts[2]
    raise ValueError(f"bad timestamp: {stamp}")


def extract_youtube_clip(
    url: str, start: str, end: str, output_wav: Path, sr: int = 24000
) -> str:
    """yt-dlp + ffmpeg the requested section to mono PCM wav.

    Returns the yt-dlp command that was run (for stamping into metadata).
    """
    cmd = [
        "yt-dlp",
        "--download-sections",
        f"*{start}-{end}",
        "--force-keyframes-at-cuts",
        "-x",
        "--audio-format",
        "wav",
        "--postprocessor-args",
        f"ffmpeg:-ac 1 -ar {sr}",
        "-o",
        str(output_wav),
        url,
    ]
    subprocess.run(cmd, check=True)
    return " ".join(cmd)


def write_metadata(
    voice_dir: Path,
    voice_id: str,
    speaker_name: str,
    url: str,
    start: str,
    end: str,
    sr: int,
    yt_cmd: str,
    denoised: bool,
    denoise_meta: dict[str, str] | None,
) -> None:
    history = [
        f"{date.today().isoformat()}: Original {_seconds(end) - _seconds(start)}s clip extracted from {url} ({start}-{end})."
    ]
    if denoised:
        history.append(
            f"{date.today().isoformat()}: Denoised with {denoise_meta['method']} ({denoise_meta['model']})."
        )

    metadata = VoiceRefMetadata(
        voice_id=voice_id,
        speaker_name=speaker_name,
        source=YoutubeSource(
            url=url,
            start_timestamp=start,
            end_timestamp=end,
            duration_seconds=_seconds(end) - _seconds(start),
        ),
        audio=AudioFormat(sample_rate_hz=sr),
        yt_dlp_command=yt_cmd,
        denoising=DenoisingState(
            applied=denoised,
            method=denoise_meta["method"] if denoised and denoise_meta else None,
            model=denoise_meta["model"] if denoised and denoise_meta else None,
        ),
        fish_speech=FishSpeechState(),
        created=date.today().isoformat(),
        history=history,
    )
    (voice_dir / "metadata.json").write_text(metadata.model_dump_json(indent=2))


def register_with_fish_speech(
    voice_id: str, audio_path: Path, transcript: str, server_url: str
) -> None:
    """Register the cleaned audio with the local Fish Speech server."""
    from swanki.audio._common import ensure_fish_speech_reference

    ensure_fish_speech_reference(
        server_url=server_url,
        reference_id=voice_id,
        audio_path=audio_path,
        text=transcript,
    )


def main() -> None:
    p = argparse.ArgumentParser(
        description="Clone a voice from YouTube into Swanki_Models/voice_refs/<id>/"
    )
    p.add_argument("--voice-id", required=True, help="Reference id used by Fish Speech")
    p.add_argument("--speaker", required=True, help="Human-readable speaker name")
    p.add_argument("--url", required=True, help="YouTube video URL")
    p.add_argument("--start", required=True, help="Start timestamp (e.g. 9:30)")
    p.add_argument("--end", required=True, help="End timestamp (e.g. 10:00)")
    p.add_argument(
        "--transcript-file",
        type=Path,
        required=True,
        help="Path to a .txt file with the verbatim transcript of the clip",
    )
    p.add_argument(
        "--sample-rate", type=int, default=24000, help="Output sample rate (Hz)"
    )
    p.add_argument(
        "--denoise",
        action="store_true",
        help="Run DeepFilterNet on the extracted clip; writes denoised.wav",
    )
    p.add_argument(
        "--register",
        action="store_true",
        help="Register the (denoised, else original) wav with the Fish Speech server",
    )
    p.add_argument(
        "--fish-server-url",
        default=os.environ.get("FISH_SPEECH_SERVER_URL", "http://localhost:8080"),
        help="Fish Speech server URL",
    )
    args = p.parse_args()

    voice_dir = voice_ref_dir(args.voice_id)
    voice_dir.mkdir(parents=True, exist_ok=True)

    # Persist the transcript verbatim (Fish Speech reads this as reference_text)
    transcript = args.transcript_file.read_text().strip()
    (voice_dir / "transcript.txt").write_text(transcript + "\n")

    original_wav = voice_dir / "original.wav"
    print(f"=== extracting {args.start}-{args.end} from {args.url} ===")
    yt_cmd = extract_youtube_clip(
        args.url, args.start, args.end, original_wav, sr=args.sample_rate
    )

    denoise_meta = None
    denoised_wav = voice_dir / "denoised.wav"
    if args.denoise:
        from swanki.voice_clone.denoise import denoise_with_deepfilternet

        print(f"=== denoising with DeepFilterNet ===")
        denoise_meta = denoise_with_deepfilternet(original_wav, denoised_wav)

    write_metadata(
        voice_dir=voice_dir,
        voice_id=args.voice_id,
        speaker_name=args.speaker,
        url=args.url,
        start=args.start,
        end=args.end,
        sr=args.sample_rate,
        yt_cmd=yt_cmd,
        denoised=args.denoise,
        denoise_meta=denoise_meta,
    )

    if args.register:
        target_wav = denoised_wav if args.denoise else original_wav
        print(f"=== registering '{args.voice_id}' on {args.fish_server_url} ===")
        register_with_fish_speech(
            args.voice_id, target_wav, transcript, args.fish_server_url
        )

    print(f"\nDone. Voice ref written to {voice_dir}")


if __name__ == "__main__":
    main()
