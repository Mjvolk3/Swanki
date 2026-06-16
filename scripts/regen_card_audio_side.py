"""
scripts/regen_card_audio_side.py
[[scripts.regen_card_audio_side]]
https://github.com/Mjvolk3/Swanki/tree/main/scripts/regen_card_audio_side.py

Re-TTS ONE side (front|back) of ONE flashcard's complementary audio from its
already-saved transcript, overwriting the mp3 in place -- WITHOUT re-rolling the
LLM transcript. For surgically fixing a stochastic Fish artifact (e.g. a "moan"
or breath glitch) in a single card's audio while keeping the exact wording.

Mirrors the front/back assembly in swanki.audio.card.generate_card_audio: chunk
the saved transcript, append_chunk_pause + preprocess + TTS each chunk, prepend
the existing citation audio (front only), combine. Needs a live Fish server --
run via scripts/regen_card_audio_side.sbatch (serverless in-job Fish), which
exports SWANKI_FISH_PORTS.

Example:

    python scripts/regen_card_audio_side.py \\
        --output-dir /scratch/.../<content_key>_0 \\
        --card-uuid 9cff566f-1eef-4f62-9a6a-d0fdfb5ff3d8 \\
        --side front --content-key <content_key> --voice fish_speech_ball
"""

import argparse
import os
import re
from pathlib import Path

from omegaconf import OmegaConf

from swanki.audio._common import (
    append_chunk_pause,
    chunk_text,
    combine_audio,
    ensure_fish_speech_reference,
    text_to_speech,
)
from swanki.audio.card import _preprocess_for_tts


def load_transcript(md_path: Path) -> str:
    """Extract the verbatim TTS text between the Generated Transcript and Citation markers."""
    text = md_path.read_text()
    m = re.search(
        r"\*\*Generated Transcript:\*\*\s*(.*?)\s*\*\*Citation Added", text, re.S
    )
    assert m, f"no 'Generated Transcript' block in {md_path}"
    return m.group(1).strip()


def build_tts_kwargs(voice: str) -> dict:
    """Compose the models=<voice> tts subtree exactly like pipeline.py, register the ref."""
    from hydra import compose, initialize_config_dir

    cfgdir = os.path.abspath("swanki/conf")
    with initialize_config_dir(version_base=None, config_dir=cfgdir):
        cfg = compose(config_name="config", overrides=[f"models={voice}"])
    tts = OmegaConf.to_container(cfg.models.models.tts, resolve=True)

    server_url = tts.get("server_url", "http://localhost:8080")
    # In-job serverless Fish exports its port here; prefer it over the config default.
    ports = os.environ.get("SWANKI_FISH_PORTS")
    if ports:
        server_url = f"http://127.0.0.1:{ports.split(',')[0].strip()}"

    reference_id = tts["reference_id"]
    ensure_fish_speech_reference(
        server_url=server_url,
        reference_id=reference_id,
        audio_path=Path(tts["reference_audio_path"]).expanduser(),
        text=tts.get("reference_text", ""),
    )
    return {
        "provider": "fish_speech",
        "server_url": server_url,
        "reference_id": reference_id,
        "temperature": tts.get("temperature", 0.8),
        "format": tts.get("format", "mp3"),
        "preprocessor": tts.get("preprocessor", {}),
        "chunking": tts.get("chunking", {}),
        "postprocessor": tts.get("postprocessor", {}),
    }


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output-dir", required=True, type=Path)
    p.add_argument("--card-uuid", required=True)
    p.add_argument("--side", choices=["front", "back"], default="front")
    p.add_argument(
        "--content-key",
        required=True,
        help="Used to locate <content_key>_citation.mp3 (front only).",
    )
    p.add_argument("--voice", required=True, help="models config name, e.g. fish_speech_ball")
    p.add_argument(
        "--speed", type=float, default=1.6, help="Match the original gen speed (complementary=1.6)."
    )
    args = p.parse_args()

    adir = args.output_dir / "gen-md-complementary-audio"
    tmd = next((args.output_dir / "complementary_transcripts").glob(f"*{args.card_uuid}*{args.side}.md"))
    out_mp3 = next(adir.glob(f"*{args.card_uuid}*{args.side}.mp3"))
    transcript = load_transcript(tmd)
    print(f"transcript ({len(transcript)} chars): {transcript[:90]}...")

    tts_kwargs = build_tts_kwargs(args.voice)

    work = args.output_dir / "regen_chunks"
    work.mkdir(exist_ok=True)
    chunk_paths: list[Path] = []

    if args.side == "front":
        citation = adir / f"{args.content_key}_citation.mp3"
        if citation.exists():
            chunk_paths.append(citation)
            print(f"prepending citation: {citation.name}")

    chunks = chunk_text(transcript)
    print(f"re-TTS {len(chunks)} chunk(s) at speed={args.speed}")
    for i, chunk in enumerate(chunks):
        cp = work / f"{args.card_uuid}_{args.side}_chunk{i}.mp3"
        paused = append_chunk_pause(chunk, "fish_speech")
        text_to_speech(_preprocess_for_tts(paused, tts_kwargs), "", cp, "", args.speed, **tts_kwargs)
        chunk_paths.append(cp)

    combine_audio(chunk_paths, out_mp3, crossfade_ms=0)
    print(f"WROTE {out_mp3}")


if __name__ == "__main__":
    main()
