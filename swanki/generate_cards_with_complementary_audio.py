#!/usr/bin/env python3
"""
gen_cards_complementary_audio.py

Takes standard gen-md files and enriches them by inserting
complementary audio links for front and back of each card.

Input dir: pan-transcriptome/gen-md/
Audio dir: pan-transcriptome/gen-md-complementary-audio/
Output dir: pan-transcriptome/gen-md-with-complementary-audio/
"""
import os
from pathlib import Path
from typing import List, Tuple

CARD_HEADER_RE = "## "
SPLIT_MARKER = "%"


def split_cards(lines: List[str]) -> List[Tuple[str, List[str]]]:
    """
    Splits a markdown file into cards by H2 (## ) headings.
    Returns list of (heading_line, body_lines).
    """
    cards: List[Tuple[str, List[str]]] = []
    current_head = None
    current_body: List[str] = []
    for line in lines:
        if line.startswith(CARD_HEADER_RE):
            if current_head is not None:
                cards.append((current_head, current_body))
            current_head = line.strip()
            current_body = []
        else:
            if current_head is not None:
                current_body.append(line)
    if current_head is not None:
        cards.append((current_head, current_body))
    return cards


def process_card(
    heading: str, body: List[str], base_name: str, idx: int, audio_dir: Path
) -> List[str]:
    """
    Returns new card lines with audio links inserted, using paths relative to CWD.
    """
    # filenames
    front_fn = f"{base_name}_{idx}_front.mp3"
    back_fn = f"{base_name}_{idx}_back.mp3"

    # Get full paths to audio files
    front_path = audio_dir / front_fn
    back_path = audio_dir / back_fn

    # Create paths relative to current working directory
    rel_front = os.path.relpath(front_path)
    rel_back = os.path.relpath(back_path)

    new_lines: List[str] = []
    new_lines.append(heading)
    # insert front audio
    new_lines.append(f"[audio-front]({rel_front})")

    # split front/back by marker
    stripped = [l.strip() for l in body]
    if SPLIT_MARKER in stripped:
        split_idx = stripped.index(SPLIT_MARKER)
        front_lines = body[:split_idx]
        back_lines = body[split_idx + 1 :]

        new_lines.extend(front_lines)
        new_lines.append(SPLIT_MARKER)
        new_lines.append(f"[audio-back]({rel_back})")
        new_lines.extend(back_lines)
    else:
        # no marker: add marker, audio, then full body as back
        new_lines.append(SPLIT_MARKER)
        new_lines.append(f"[audio-back]({rel_back})")
        new_lines.extend(body)

    new_lines.append("")
    return new_lines


def enrich_gen_md(gen_md_dir: Path, audio_dir: Path, output_dir: Path) -> None:
    os.makedirs(output_dir, exist_ok=True)
    for md in sorted(os.listdir(gen_md_dir)):
        if not md.endswith(".md"):
            continue
        in_path = gen_md_dir / md
        out_path = output_dir / md
        base = Path(md).stem  # e.g. page-1
        with open(in_path, "r", encoding="utf-8") as f:
            lines = [l.rstrip("\n") for l in f]
        cards = split_cards(lines)
        new_lines: List[str] = []
        for idx, (heading, body) in enumerate(cards, start=1):
            new_lines.extend(process_card(heading, body, base, idx, audio_dir))
        with open(out_path, "w", encoding="utf-8") as f:
            f.write("\n".join(new_lines))


if __name__ == "__main__":
    gen_md_dir = Path("pan-transcriptome/gen-md")
    audio_dir = Path("pan-transcriptome/gen-md-complementary-audio")
    output_dir = Path("pan-transcriptome/gen-md-with-complementary-audio")
    enrich_gen_md(gen_md_dir, audio_dir, output_dir)
    print(f"Wrote enriched cards to {output_dir}")
