"""
scripts/regen_hamming_bookends_ch1_10.py
[[scripts.regen_hamming_bookends_ch1_10]]
https://github.com/Mjvolk3/Swanki/tree/main/scripts/regen_hamming_bookends_ch1_10.py

One-off: regenerate the lecture/summary/reading bookends for Hamming
chapters 01-10 with the new simple bookend format (2026-05-19:
"This {type} is posted as {context-key}. Let's Begin." + symmetric end),
restitch each chapter audio, sync to Zotero, then trigger abs_refresh.

Bookend mp3 filenames stored in `chunk_manifest.json` are preserved -- we
overwrite the same files. All non-bookend chunk mp3s stay byte-identical;
restitch refreshes only the bookends + the final stitched audio + the
`chunk_timeline.json` sidecar (free, via the 2026-05-18 timeline work).

Provenance: assumes the build_bookend_text change is already committed on
main (sync_to_zotero embeds `git rev-parse --short HEAD`).
"""

import json
import re
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(dotenv_path=str(Path.cwd() / ".env"))

from swanki.audio._common import (  # noqa: E402
    build_bookend_text,
    restitch_from_chunks,
    text_to_speech,
)
from swanki.audio.surgical import fish_speech_healthy  # noqa: E402

CITATION = "hammingArtDoingScience2020"
HAM_DIR = Path(
    "/scratch/projects/torchcell-scratch/Swanki_Data/hammingArtDoingScience2020"
)

FISH = {
    "provider": "fish_speech",
    "server_url": "http://localhost:8080",
    "reference_id": "hamming-20260428T1135-science-vs-engineering",
    "temperature": 0.8,
    "format": "mp3",
}

# Match audio/all.yaml speeds so bookend pacing matches the chapter body.
SPEED = {"lecture": 1.0, "summary": 1.1, "transcript": 1.2}

# manifest["audio_type"] uses "reading" externally; build_bookend_text takes
# the internal Literal "transcript" (legacy naming) and renders "reading".
MANIFEST_TO_BUILD = {
    "lecture": "lecture",
    "summary": "summary",
    "reading": "transcript",
}


def pick_live_dir(ch_num: str) -> Path:
    """Return the most-recently-modified `<base>_<NN>_<slug>...` dir that has
    all three audio types' chunk_manifest.json (the live, ABS-served version)."""
    cands = [
        d
        for d in HAM_DIR.glob(f"{CITATION}_{ch_num}_*")
        if d.is_dir()
        and (d / "lecture_chunks/chunk_manifest.json").exists()
        and (d / "reading_chunks/chunk_manifest.json").exists()
        and (d / "summary_chunks/chunk_manifest.json").exists()
    ]
    cands.sort(key=lambda d: d.stat().st_mtime, reverse=True)
    assert cands, f"No live dir found for ch{ch_num}"
    return cands[0]


def _content_key_from_dir(dir_name: str) -> str:
    """Strip a trailing `_<N>` reprocess suffix from a dir name to get the
    canonical chapter content_key. ch1-5 live in `*_NN_slug_<N>`; ch6-10 in
    bare `*_NN_slug`."""
    return re.sub(r"_\d+$", "", dir_name)


def regen_chapter(ch_num: str) -> Path:
    """Regenerate bookends + restitch all three audio types for one chapter.

    Returns the chapter dir Path (input to sync_to_zotero)."""
    d = pick_live_dir(ch_num)
    content_key = _content_key_from_dir(d.name)
    print(f"\n== ch{ch_num}  dir={d.name}  content_key={content_key}")

    for at in ("lecture", "summary", "reading"):
        chunks_dir = d / f"{at}_chunks"
        man_path = chunks_dir / "chunk_manifest.json"
        manifest = json.loads(man_path.read_text())
        build_type = MANIFEST_TO_BUILD[at]
        for pos in ("start", "end"):
            target = chunks_dir / manifest[f"bookend_{pos}"]
            text = build_bookend_text(content_key, build_type, pos)
            text_to_speech(
                text=text,
                voice_id="",
                output_path=target,
                api_key="",
                speed=SPEED[build_type],
                **FISH,
            )
            print(f"   {at} {pos}: {target.name}")
        final = d / manifest["output_file"]
        # Apply + persist the asymmetric bookend pauses (fast front, ~2s break
        # before the end bookend, trailing silence after). Passing the
        # overrides writes them into each manifest's postprocessor so later
        # surgical / comment_edit restitches inherit them.
        restitch_from_chunks(
            man_path,
            final,
            bookend_start_pause_ms=300,
            bookend_end_pause_ms=2000,
            bookend_trailing_pause_ms=1500,
        )
        print(f"   restitched -> {final.name}")
    return d


def main() -> None:
    """Preflight Fish, regen bookends + restitch ch01-10, then sync to Zotero."""
    if not fish_speech_healthy(FISH["server_url"]):
        sys.exit(f"Fish not reachable at {FISH['server_url']}")

    # Defer the Zotero sync import + DEFAULT_TIMEOUT patch until we're past
    # the regen so a transient pyzotero hiccup does not block the audio work.
    from pyzotero import _client as _pyz

    _pyz.DEFAULT_TIMEOUT = 180
    from swanki.sync.zotero import sync_to_zotero

    dirs: list[Path] = []
    for n in ("01", "02", "03", "04", "05", "06", "07", "08", "09", "10"):
        dirs.append(regen_chapter(n))

    print("\n== Zotero sync ==")
    for d in dirs:
        ck = _content_key_from_dir(d.name)
        print(f"  syncing {ck}")
        sync_to_zotero(
            citation_key=CITATION,
            output_dir=d,
            audio_prefix=ck,
            content_key=ck,
        )

    print("\ndone -- run scripts/abs_refresh.sh next to propagate to ABS")


if __name__ == "__main__":
    main()
