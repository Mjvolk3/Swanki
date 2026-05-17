"""
scripts/surgical_rechunk.py
[[scripts.surgical_rechunk]]
https://github.com/Mjvolk3/Swanki/tree/main/scripts/surgical_rechunk.py

Thin CLI over swanki.audio.surgical.regenerate_and_restitch. Re-TTS the
named chunk indices using their EXISTING manifest text (the reusable case
after an upstream code fix), then restitch -- every other chunk file is
reused untouched. Fish Speech is health-checked first; a down server aborts
before any partial work. For content edits (hand-corrected chunk text),
import regenerate_and_restitch directly with an explicit edits map instead.
"""

import argparse
import sys
from pathlib import Path

from dotenv import load_dotenv

from swanki.audio.surgical import fish_speech_healthy, regenerate_and_restitch

load_dotenv(dotenv_path=str(Path.cwd() / ".env"))


def main() -> None:
    """CLI: surgical re-TTS of existing-text chunks + restitch."""
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--manifest-path", required=True, type=Path)
    p.add_argument(
        "--audio-type",
        required=True,
        choices=["lecture", "reading", "summary", "card"],
        help="Asserted against manifest['audio_type'] (indices are local).",
    )
    p.add_argument(
        "--chunk-indices",
        required=True,
        help="Comma-separated chunk indices to re-render, e.g. 0,31,37",
    )
    p.add_argument("--reference-id", required=True, help="Fish reference voice id")
    p.add_argument("--server-url", default="http://localhost:8080")
    p.add_argument("--speed", type=float, default=1.1)
    p.add_argument("--temperature", type=float, default=0.8)
    p.add_argument("--section-pause-ms", type=int, default=None)
    p.add_argument(
        "--output-path",
        type=Path,
        default=None,
        help="Defaults to manifest.parent.parent / manifest['output_file'].",
    )
    args = p.parse_args()

    if not fish_speech_healthy(args.server_url):
        print(
            f"Fish Speech not reachable at {args.server_url} -- aborting "
            "before any re-TTS.",
            file=sys.stderr,
        )
        sys.exit(1)

    indices = [int(x) for x in args.chunk_indices.split(",") if x.strip()]
    chunk_edits = {i: None for i in indices}

    out = regenerate_and_restitch(
        args.manifest_path,
        chunk_edits,
        audio_type=args.audio_type,
        output_path=args.output_path,
        speed=args.speed,
        section_pause_ms=args.section_pause_ms,
        tts_kwargs={
            "provider": "fish_speech",
            "server_url": args.server_url,
            "reference_id": args.reference_id,
            "temperature": args.temperature,
            "format": "mp3",
        },
    )
    print(f"done -> {out}")


if __name__ == "__main__":
    main()
