"""
scripts/swanki_card_edit.py
[[scripts.swanki_card_edit]]
https://github.com/Mjvolk3/Swanki/tree/main/scripts/swanki_card_edit.py

SLURM-native surgical CARD audio edit: apply ONE precise edit to ONE chunk of
ONE card side via swanki.audio.card_edit.edit_card_chunk against the job-private
Fish server (SWANKI_FISH_PORTS). Mirrors scripts/swanki_audio_edit.py: it only
assembles tts_kwargs from the voice config, registers the reference voice on the
in-job server, and dispatches to edit_card_chunk. Optionally swaps the rewritten
side mp3 into the headless Anki media collection (AnkiConnect storeMediaFile +
one sync) when --anki is passed; the [sound:...] filename is stable so the swap
overwrites in place and the note reference is untouched. Run via
scripts/swanki_card_edit.sbatch (serverless in-job Fish).
"""

import argparse
import base64
import os
from pathlib import Path

import yaml
from swanki_audio_edit import build_fish_tts_kwargs

from swanki.audio._common import ensure_fish_speech_reference
from swanki.audio.card_edit import edit_card_chunk


def swap_anki_media(side_mp3: Path, sound_filename: str, url: str) -> None:
    """Overwrite one Anki media file with the rewritten side mp3, then sync.

    AnkiConnect ``storeMediaFile`` writes base64 bytes under the existing
    ``[sound:...]`` filename (stable, so the note reference is untouched), then
    one ``sync`` pushes the collection to AnkiWeb.

    Args:
        side_mp3: Rewritten canonical side mp3.
        sound_filename: The media filename the card's ``[sound:...]`` references.
        url: AnkiConnect HTTP endpoint.
    """
    from swanki.delivery.targets.anki import ankiconnect_call

    assert side_mp3.exists(), f"side mp3 missing: {side_mp3}"
    ankiconnect_call(
        url,
        "storeMediaFile",
        {
            "filename": sound_filename,
            "data": base64.b64encode(side_mp3.read_bytes()).decode("ascii"),
        },
    )
    ankiconnect_call(url, "sync")


def _resolve_manifest(args: argparse.Namespace) -> Path:
    """Resolve the card manifest from --card-manifest or --output-dir + --card-uuid."""
    if args.card_manifest:
        return Path(args.card_manifest)
    assert args.output_dir and args.card_uuid, (
        "pass --card-manifest, or both --output-dir and --card-uuid"
    )
    return (
        Path(args.output_dir)
        / "gen-md-complementary-audio"
        / "card_chunks"
        / f"{args.card_uuid}_manifest.json"
    )


def main() -> None:
    """Resolve the in-job Fish, build tts_kwargs, and apply one card chunk edit."""
    ap = argparse.ArgumentParser(description="SLURM-native surgical card audio edit")
    ap.add_argument("--card-manifest", help="path to card_chunks/{uuid}_manifest.json")
    ap.add_argument("--output-dir", help="pipeline output dir (with --card-uuid)")
    ap.add_argument("--card-uuid", help="card uuid (with --output-dir)")
    ap.add_argument("--side", choices=["front", "back"], default="front")
    ap.add_argument("--idx", type=int, default=0, help="tts-chunk-local index")
    grp = ap.add_mutually_exclusive_group(required=True)
    grp.add_argument(
        "--speech-only", action="store_true", help="re-roll stored text verbatim"
    )
    grp.add_argument("--comment", help="reviewer comment driving the agent rewrite")
    grp.add_argument("--new-text", help="explicit replacement prose")
    ap.add_argument(
        "--voice", required=True, help="models config name, e.g. fish_speech_ball"
    )
    ap.add_argument(
        "--model", default=None, help="pydantic-ai llm string (comment path only)"
    )
    ap.add_argument(
        "--anki",
        nargs="?",
        const="",
        default=None,
        help="swap the rewritten side mp3 into Anki media; optional value is the "
        "[sound:...] filename (defaults to the side mp3 basename)",
    )
    ap.add_argument(
        "--repo",
        default=os.environ.get("SWANKI_REPO", str(Path(__file__).resolve().parents[1])),
    )
    args = ap.parse_args()

    ports = os.environ.get("SWANKI_FISH_PORTS", "8080").split(",")
    server_url = f"http://127.0.0.1:{ports[0].strip()}"

    voice_cfg = Path(args.repo) / "swanki" / "conf" / "models" / f"{args.voice}.yaml"
    tts_kwargs = build_fish_tts_kwargs(voice_cfg, server_url)
    tts_raw = yaml.safe_load(voice_cfg.read_text())["models"]["tts"]
    ensure_fish_speech_reference(
        server_url=server_url,
        reference_id=tts_kwargs["reference_id"],
        audio_path=Path(tts_raw.get("reference_audio_path", "")).expanduser(),
        text=tts_raw.get("reference_text", ""),
    )

    kw: dict = {}
    if args.speech_only:
        kw["speech_only"] = True
    elif args.comment is not None:
        kw["comment"] = args.comment
    else:
        kw["new_text"] = args.new_text

    manifest = _resolve_manifest(args)
    res = edit_card_chunk(
        manifest,
        args.side,
        args.idx,
        model=args.model,
        tts_kwargs=tts_kwargs,
        **kw,
    )
    print(
        f"[swanki_card_edit] side={res.side} idx={args.idx} "
        f"action={res.action} rationale={res.rationale}\n"
        f"  side_file={res.side_file}\n"
        f"  original_index={res.original_index}"
    )

    if args.anki is not None:
        sound_filename = args.anki or res.side_file.name
        anki_url = os.environ.get(
            "ANKICONNECT_URL",
            f"http://{os.environ.get('ANKI_HOST', '127.0.0.1')}:{os.environ.get('ANKI_PORT', '8765')}",
        )
        swap_anki_media(res.side_file, sound_filename, anki_url)
        print(f"[swanki_card_edit] swapped Anki media: {sound_filename}")


if __name__ == "__main__":
    main()
