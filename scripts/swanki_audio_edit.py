"""
scripts/swanki_audio_edit.py
[[scripts.swanki_audio_edit]]
https://github.com/Mjvolk3/Swanki/tree/main/scripts/swanki_audio_edit.py

SLURM-native surgical audio edit: apply ONE reviewer comment to ONE chunk via
swanki.audio.comment_edit.edit_chunk against the job-private Fish server
(SWANKI_FISH_PORTS). Post-cutover the persistent Docker Fish fleet at :8080 is
gone, so surgical edits run as a one-GPU sbatch (scripts/swanki_audio_edit.sbatch)
that brings Fish up in-job; this is the thin launcher it invokes. It only assembles
tts_kwargs (mirroring pipeline._setup_tts) from the voice config and dispatches to
edit_chunk -- the edit/agent/re-TTS/restitch logic stays in edit_chunk.
"""

import argparse
import os
from pathlib import Path

import yaml

from swanki.audio._common import _discover_fish_speech_servers
from swanki.audio.comment_edit import edit_chunk


def build_fish_tts_kwargs(voice_cfg_path: Path, server_url: str) -> dict:
    """Build the fish_speech tts_kwargs from a models config, as the pipeline does.

    Mirrors swanki.pipeline._setup_tts: the same flat keys edit_chunk forwards to
    text_to_speech (provider/server_url/reference_id/temperature/format) plus the
    preprocessor/chunking/postprocessor sub-trees. server_url is overridden to the
    job-private Fish.

    Args:
        voice_cfg_path: Path to swanki/conf/models/<voice>.yaml.
        server_url: Resolved in-job Fish base URL.

    Returns:
        tts_kwargs dict ready for edit_chunk.
    """
    assert voice_cfg_path.exists(), f"voice config missing: {voice_cfg_path}"
    tts = yaml.safe_load(voice_cfg_path.read_text())["models"]["tts"]
    assert tts["provider"] == "fish_speech", (
        f"swanki_audio_edit supports fish_speech only, got {tts['provider']}"
    )
    return {
        "provider": "fish_speech",
        "server_url": server_url,
        "reference_id": tts["reference_id"],
        "temperature": tts.get("temperature", 0.8),
        "format": tts.get("format", "mp3"),
        "preprocessor": tts.get("preprocessor", {}),
        "chunking": tts.get("chunking", {}),
        "postprocessor": tts.get("postprocessor", {}),
    }


def main() -> None:
    """Resolve the in-job Fish, build tts_kwargs, and apply one chunk edit."""
    ap = argparse.ArgumentParser(description="SLURM-native surgical audio chunk edit")
    ap.add_argument("--manifest", required=True, help="path to chunk_manifest.json")
    ap.add_argument("--idx", type=int, required=True, help="audio-type-local chunk index")
    grp = ap.add_mutually_exclusive_group(required=True)
    grp.add_argument("--speech-only", action="store_true", help="re-roll stored text verbatim")
    grp.add_argument("--comment", help="reviewer comment driving the agent rewrite")
    grp.add_argument("--new-text", help="explicit replacement prose")
    ap.add_argument("--voice", required=True, help="models config name, e.g. fish_speech_hamming")
    ap.add_argument("--speed", type=float, default=1.0, help="must match the original render speed")
    ap.add_argument("--model", default=None, help="pydantic-ai llm string (comment path only)")
    ap.add_argument(
        "--repo",
        default=os.environ.get("SWANKI_REPO", str(Path(__file__).resolve().parents[1])),
    )
    args = ap.parse_args()

    ports = os.environ.get("SWANKI_FISH_PORTS", "8080").split(",")
    server_url = _discover_fish_speech_servers(f"http://127.0.0.1:{ports[0].strip()}")[0]

    voice_cfg = Path(args.repo) / "swanki" / "conf" / "models" / f"{args.voice}.yaml"
    tts_kwargs = build_fish_tts_kwargs(voice_cfg, server_url)

    kw: dict = {}
    if args.speech_only:
        kw["speech_only"] = True
    elif args.comment is not None:
        kw["comment"] = args.comment
    else:
        kw["new_text"] = args.new_text

    res = edit_chunk(
        Path(args.manifest),
        args.idx,
        tts_kwargs=tts_kwargs,
        speed=args.speed,
        model=args.model,
        **kw,
    )
    print(
        f"[swanki_audio_edit] action={res.action} rationale={res.rationale}\n"
        f"  output_file={res.output_file}\n"
        f"  new_window_ms=({res.start_ms}, {res.end_ms})"
    )


if __name__ == "__main__":
    main()
