"""
scripts/regen_campagne_lecture_chunks.py
[[scripts.regen_campagne_lecture_chunks]]
https://github.com/Mjvolk3/Swanki/tree/main/scripts/regen_campagne_lecture_chunks.py

Surgical re-TTS of chunks 10 and 14 of the campagne2021 lecture audio.
Both chunks contained Unicode em-/en-dashes that Fish Speech garbled.
The normalization pass in _tts_fish_speech now folds them to ASCII, so
regenerating just those two chunks and restitching replaces the garble
without re-rendering the full 25-minute lecture.
"""

import json
from pathlib import Path

from dotenv import load_dotenv

from swanki.audio._common import restitch_from_chunks, text_to_speech

load_dotenv()


CITATION_KEY = "campagneClinicalPharmacokineticsPharmacodynamics2021"
OUTPUT_DIR = Path(
    "/scratch/projects/torchcell-scratch/Swanki_Data/"
    "campagneClinicalPharmacokineticsPharmacodynamics2021"
)
CHUNKS_DIR = OUTPUT_DIR / "lecture_chunks"
MANIFEST = CHUNKS_DIR / "chunk_manifest.json"
LECTURE_OUT = OUTPUT_DIR / f"{CITATION_KEY}-lecture-audio.mp3"

REGEN_INDICES = [10, 14]
LECTURE_SPEED = 1.1
LECTURE_SECTION_PAUSE_MS = 4000

FISH_KW = dict(
    provider="fish_speech",
    server_url="http://localhost:8080",
    reference_id="audrey-hepburn",
    temperature=0.8,
    format="mp3",
)


def main() -> None:
    assert MANIFEST.exists(), f"Manifest missing: {MANIFEST}"
    manifest = json.loads(MANIFEST.read_text())
    chunks_by_idx = {c["index"]: c for c in manifest["chunks"]}

    for idx in REGEN_INDICES:
        assert idx in chunks_by_idx, f"Chunk {idx} not in manifest"
        chunk = chunks_by_idx[idx]
        out_path = CHUNKS_DIR / chunk["file"]
        print(f"regenerating chunk {idx} -> {out_path.name}")
        text_to_speech(
            text=chunk["text"],
            voice_id="",
            output_path=out_path,
            api_key="",
            speed=LECTURE_SPEED,
            **FISH_KW,
        )

    print("restitching lecture audio ...")
    restitch_from_chunks(
        MANIFEST,
        LECTURE_OUT,
        section_pause_ms=LECTURE_SECTION_PAUSE_MS,
    )
    print(f"wrote {LECTURE_OUT}")


if __name__ == "__main__":
    main()
