"""
scripts/swanki_replace_card.py
[[scripts.swanki_replace_card]]
https://github.com/Mjvolk3/Swanki/tree/main/scripts/swanki_replace_card.py

SLURM-native surgical CARD replacement: swap ONE card wholesale (new front + back
text, BOTH audio sides re-TTSed) in the live headless Anki collection via
swanki.audio.card_replace.replace_card against the job-private Fish server
(SWANKI_FISH_PORTS). Mirrors scripts/swanki_card_edit.py: it assembles tts_kwargs
from the voice config, registers the reference voice on the in-job server, then
dispatches to replace_card. The collection mutation (updateNoteFields +
storeMediaFile + one AnkiWeb sync) only fires when --anki is passed; without it
the tool prints the resolved plan and touches nothing. Run via
scripts/swanki_replace_card.sbatch (serverless in-job Fish).
"""

import argparse
import os
from pathlib import Path

import yaml
from swanki_audio_edit import build_fish_tts_kwargs

from swanki.audio._common import ensure_fish_speech_reference
from swanki.audio.card_replace import replace_card
from swanki.delivery.targets.anki import default_ankiconnect_url


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


def _read_side(text: str | None, path: str | None, label: str) -> str:
    """Return the replacement side text from an inline value or a file."""
    if path is not None:
        return Path(path).read_text().strip()
    assert text is not None, f"pass --new-{label} or --new-{label}-file"
    return text


def main() -> None:
    """Resolve the in-job Fish, build tts_kwargs, and replace one card wholesale."""
    ap = argparse.ArgumentParser(description="SLURM-native surgical card replacement")
    ap.add_argument("--card-manifest", help="path to card_chunks/{uuid}_manifest.json")
    ap.add_argument("--output-dir", help="pipeline output dir (with --card-uuid)")
    ap.add_argument("--card-uuid", help="card uuid (with --output-dir)")
    ap.add_argument("--citation-key", required=True, help="citation key for front prefix")
    ap.add_argument("--new-front", help="new front prose (no @citation prefix)")
    ap.add_argument("--new-front-file", help="file holding the new front prose")
    ap.add_argument("--new-back", help="new back prose")
    ap.add_argument("--new-back-file", help="file holding the new back prose")
    ap.add_argument(
        "--voice", required=True, help="models config name, e.g. fish_speech_ball"
    )
    ap.add_argument(
        "--note-id",
        type=int,
        default=None,
        help="numeric note-id override (required in the text-only degrade path)",
    )
    ap.add_argument(
        "--anki",
        action="store_true",
        help="actually patch the live collection (else dry-run: print the plan only)",
    )
    ap.add_argument("--no-sync", action="store_true", help="skip the final AnkiWeb sync")
    ap.add_argument(
        "--repo",
        default=os.environ.get("SWANKI_REPO", str(Path(__file__).resolve().parents[1])),
    )
    args = ap.parse_args()

    manifest = _resolve_manifest(args)
    new_front = _read_side(args.new_front, args.new_front_file, "front")
    new_back = _read_side(args.new_back, args.new_back_file, "back")

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

    anki_url = os.environ.get("ANKICONNECT_URL", default_ankiconnect_url())

    if not args.anki:
        print(
            "[swanki_replace_card] DRY-RUN (pass --anki to patch the collection)\n"
            f"  manifest={manifest}\n"
            f"  citation_key={args.citation_key} note_id={args.note_id}\n"
            f"  new_front={new_front!r}\n"
            f"  new_back={new_back!r}"
        )
        return

    res = replace_card(
        manifest,
        new_front_text=new_front,
        new_back_text=new_back,
        citation_key=args.citation_key,
        tts_kwargs=tts_kwargs,
        ankiconnect_url=anki_url,
        note_id=args.note_id,
        sync_after=not args.no_sync,
    )
    print(
        f"[swanki_replace_card] note_id={res.note_id} degraded={res.degraded} "
        f"synced={res.synced}\n"
        f"  front_file={res.front_file}\n"
        f"  back_file={res.back_file}"
    )


if __name__ == "__main__":
    main()
