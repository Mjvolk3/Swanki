#!/usr/bin/env python3
"""
enrich_image_cards_complementary_audio.py

Takes image cards and enriches them by inserting complementary audio links
for front and back of each card.

Input dir: pan-transcriptome/anki-image-cards/
Audio dir: pan-transcriptome/anki-image-cards-complementary-audio/
Output dir: pan-transcriptome/anki-image-cards-with-complementary-audio/
"""
import os
import re
from pathlib import Path
from typing import List, Tuple


CARD_HEADER_RE = "## "
SPLIT_MARKER = "%"
IMAGE_PATTERN = re.compile(r"!\[\]\((.*?)\)")


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


def process_image_card(
    heading: str, body: List[str], stem: str, idx: int, audio_dir: Path
) -> List[str]:
    """
    Returns new card lines with audio links inserted, using paths relative to CWD.
    """
    # filenames for audio
    front_fn = f"{stem}_{idx}_front.mp3"
    back_fn = f"{stem}_{idx}_back.mp3"

    # Get full paths to audio files
    front_path = audio_dir / front_fn
    back_path = audio_dir / back_fn

    # Create paths relative to current working directory
    rel_front = os.path.relpath(front_path)
    rel_back = os.path.relpath(back_path)

    new_lines: List[str] = []
    new_lines.append(heading)

    # Insert front audio right after the heading
    new_lines.append(f"[audio-front]({rel_front})")

    # Split front/back by marker
    stripped = [l.strip() for l in body]
    if SPLIT_MARKER in stripped:
        split_idx = stripped.index(SPLIT_MARKER)
        front_lines = body[:split_idx]
        back_lines = body[split_idx + 1 :]

        # Front content with image
        new_lines.extend(front_lines)

        # Add marker
        new_lines.append(SPLIT_MARKER)

        # Add audio-back right after marker
        new_lines.append(f"[audio-back]({rel_back})")

        # Add back content
        new_lines.extend(back_lines)
    else:
        # No marker found (shouldn't happen for image cards, but handle it)
        # Add all content as front
        new_lines.extend(body)
        # Add marker and back audio at end
        new_lines.append(SPLIT_MARKER)
        new_lines.append(f"[audio-back]({rel_back})")

    new_lines.append("")
    return new_lines


def enrich_image_cards(
    image_cards_dir: Path, audio_dir: Path, output_dir: Path
) -> None:
    """
    Process all image cards, adding complementary audio links
    """
    os.makedirs(output_dir, exist_ok=True)

    # Get all image card files
    card_files = [f for f in sorted(os.listdir(image_cards_dir)) if f.endswith(".md")]
    print(f"Found {len(card_files)} image cards to process")

    for md in card_files:
        in_path = image_cards_dir / md
        out_path = output_dir / md
        stem = Path(md).stem  # e.g. page-3_card_1_1

        # Read card content
        with open(in_path, "r", encoding="utf-8") as f:
            lines = [l.rstrip("\n") for l in f]

        # Split into cards (usually just one per file for image cards)
        cards = split_cards(lines)

        new_lines: List[str] = []
        for idx, (heading, body) in enumerate(cards, start=1):
            processed_lines = process_image_card(heading, body, stem, idx, audio_dir)
            new_lines.extend(processed_lines)

        # Check if front and back audio files exist
        front_audio = audio_dir / f"{stem}_1_front.mp3"
        back_audio = audio_dir / f"{stem}_1_back.mp3"

        if not front_audio.exists() or not back_audio.exists():
            print(f"Warning: Audio missing for {md}")

        # Write enriched card
        with open(out_path, "w", encoding="utf-8") as f:
            f.write("\n".join(new_lines))

        print(f"Processed: {md}")

    print(f"Completed processing {len(card_files)} image cards")


def main():
    """Main entry point"""
    print("Starting image card enrichment with complementary audio")

    image_cards_dir = Path("pan-transcriptome/anki-image-cards")
    audio_dir = Path("pan-transcriptome/anki-image-cards-complementary-audio")
    output_dir = Path("pan-transcriptome/anki-image-cards-with-complementary-audio")

    enrich_image_cards(image_cards_dir, audio_dir, output_dir)
    print(f"Wrote enriched image cards to {output_dir}")


if __name__ == "__main__":
    main()
