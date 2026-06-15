"""
scripts/clone_voice_from_youtube.py
[[scripts.clone_voice_from_youtube]]
https://github.com/Mjvolk3/Swanki/tree/main/scripts/clone_voice_from_youtube.py

End-to-end CLI: extract a voice-clone reference clip from YouTube into the
speaker/clips layout under ``$SWANKI_MODELS/voice_refs/<speaker_id>/clips/``,
persist transcript + clip.json, optionally denoise with DeepFilterNet, and
optionally register the cleaned audio with the local Fish Speech server.

Example:

    conda activate swanki
    python scripts/clone_voice_from_youtube.py \\
        --speaker-id hamming \\
        --speaker-name "Richard Hamming" \\
        --slug science-vs-engineering \\
        --url "https://www.youtube.com/watch?v=AD4b-52jtos" \\
        --start 22:09 --end 22:40 \\
        --transcript-file ./transcript.txt \\
        --denoise \\
        --register
"""

import argparse
import os
import subprocess
from datetime import date, datetime
from pathlib import Path

from swanki.voice_clone.refs import (
    AudioFormat,
    DenoisingState,
    VoiceClip,
    VoiceSpeaker,
    YoutubeSource,
    clip_dir,
    load_speaker,
    speaker_dir,
    write_clip,
    write_speaker,
)


def _seconds(stamp: str) -> float:
    """Parse MM:SS(.ms) or HH:MM:SS(.ms) into seconds (fractional allowed)."""
    parts = [float(p) for p in stamp.split(":")]
    if len(parts) == 2:
        return parts[0] * 60 + parts[1]
    if len(parts) == 3:
        return parts[0] * 3600 + parts[1] * 60 + parts[2]
    raise ValueError(f"bad timestamp: {stamp}")


def fetch_youtube_meta(url: str) -> dict[str, str | None]:
    """Pull channel/title/upload-date for the source video via yt-dlp --print."""
    fmt = "%(channel)s|||%(channel_url)s|||%(title)s|||%(upload_date)s"
    out = subprocess.run(
        ["yt-dlp", "--skip-download", "--print", fmt, url],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    channel, channel_url, title, upload_date = (out.split("|||") + [None] * 4)[:4]
    return {
        "channel": channel or None,
        "channel_url": channel_url or None,
        "video_title": title or None,
        "upload_date": upload_date or None,
    }


def extract_youtube_clip(
    url: str, start: str, end: str, output_wav: Path, sr: int = 24000
) -> str:
    """yt-dlp + ffmpeg the requested section to mono PCM wav.

    Returns the yt-dlp command that was run (for stamping into clip.json).
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


def register_with_fish_speech(
    reference_id: str, audio_path: Path, transcript: str, server_url: str
) -> None:
    """Register the cleaned audio with the local Fish Speech server."""
    from swanki.audio._common import ensure_fish_speech_reference

    ensure_fish_speech_reference(
        server_url=server_url,
        reference_id=reference_id,
        audio_path=audio_path,
        text=transcript,
    )


def main() -> None:
    p = argparse.ArgumentParser(
        description="Clone a voice clip from YouTube into voice_refs/<speaker_id>/clips/<clip_id>/"
    )
    p.add_argument("--speaker-id", required=True, help="Speaker dir name, e.g. 'hamming'")
    p.add_argument("--speaker-name", required=True, help="Human-readable speaker name")
    p.add_argument(
        "--slug",
        required=True,
        help="Short kebab-case clip descriptor; clip_id becomes <stamp>-<slug>",
    )
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

    clip_id = f"{datetime.now():%Y%m%dT%H%M}-{args.slug}"
    cdir = clip_dir(args.speaker_id, clip_id)
    cdir.mkdir(parents=True, exist_ok=True)

    # Persist the transcript verbatim (Fish Speech reads this as reference_text)
    transcript = args.transcript_file.read_text().strip()
    (cdir / "transcript.txt").write_text(transcript + "\n")

    print(f"=== fetching channel/title metadata for {args.url} ===")
    yt_meta = fetch_youtube_meta(args.url)
    print(f"    channel: {yt_meta['channel']} | title: {yt_meta['video_title']}")

    original_wav = cdir / "original.wav"
    print(f"=== extracting {args.start}-{args.end} from {args.url} ===")
    yt_cmd = extract_youtube_clip(
        args.url, args.start, args.end, original_wav, sr=args.sample_rate
    )

    denoising = DenoisingState()
    denoised_wav = cdir / "denoised.wav"
    if args.denoise:
        from swanki.voice_clone.denoise import denoise_with_deepfilternet

        print("=== denoising with DeepFilterNet ===")
        meta = denoise_with_deepfilternet(original_wav, denoised_wav)
        denoising = DenoisingState(
            applied=True, method=meta["method"], model=meta["model"]
        )

    reference_id = f"{args.speaker_id}-{clip_id}"
    today = date.today().isoformat()
    duration_s = round(_seconds(args.end) - _seconds(args.start))
    history = [
        f"{today}: {duration_s}s clip extracted from {args.start}-{args.end} of {args.url}."
    ]
    if denoising.applied:
        history.append(f"{today}: Denoised with {denoising.method} ({denoising.model}).")

    clip = VoiceClip(
        clip_id=clip_id,
        source=YoutubeSource(
            url=args.url,
            channel=yt_meta["channel"],
            channel_url=yt_meta["channel_url"],
            video_title=yt_meta["video_title"],
            upload_date=yt_meta["upload_date"],
            start_timestamp=args.start,
            end_timestamp=args.end,
            duration_seconds=duration_s,
        ),
        audio=AudioFormat(sample_rate_hz=args.sample_rate),
        yt_dlp_command=yt_cmd,
        denoising=denoising,
        transcript=transcript,
        fish_speech_reference_id=reference_id,
        created=today,
        history=history,
    )
    write_clip(args.speaker_id, clip)

    if (speaker_dir(args.speaker_id) / "speaker.json").exists():
        speaker = load_speaker(args.speaker_id)
        speaker.speaker_name = args.speaker_name
        speaker.active_clip_id = clip_id
    else:
        speaker = VoiceSpeaker(
            speaker_id=args.speaker_id,
            speaker_name=args.speaker_name,
            active_clip_id=clip_id,
        )
    write_speaker(speaker)

    if args.register:
        target_wav = denoised_wav if denoising.applied else original_wav
        print(f"=== registering '{reference_id}' on {args.fish_server_url} ===")
        register_with_fish_speech(
            reference_id, target_wav, transcript, args.fish_server_url
        )

    print(f"\nDone. Clip written to {cdir}")
    print(f"fish_speech reference_id: {reference_id}")


if __name__ == "__main__":
    main()
