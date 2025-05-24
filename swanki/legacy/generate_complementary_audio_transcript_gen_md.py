# swanki/generate_complementary_audio_transcript_gen_md
# [[swanki.generate_complementary_audio_transcript_gen_md]]
# https://github.com/Mjvolk3/swanki/tree/main/swanki/generate_complementary_audio_transcript_gen_md
# Test file: tests/swanki/test_generate_complementary_audio_transcript_gen_md.py

import os
import os.path as osp
from typing import List
from dotenv import load_dotenv
from openai import OpenAI
import tiktoken
from .md_to_anki import split_cards, split_front_back
import re

def clean_transcript(raw_file: str, clean_file: str) -> None:
    """
    Simplify the raw transcript by stripping lines, dropping tag lines,
    and collapsing multiple blank lines into one.
    """
    with open(raw_file, "r", encoding="utf-8") as f:
        lines = [l.strip() for l in f]

    cleaned: List[str] = []
    prev_blank = False
    for l in lines:
        if not l:
            if not prev_blank:
                cleaned.append("")
                prev_blank = True
        elif not l.startswith("- #"):
            cleaned.append(l)
            prev_blank = False

    with open(clean_file, "w", encoding="utf-8") as f:
        f.write("\n".join(cleaned))


def generate_transcript(
    transcript_input_file: str,
    output_file: str,
    model: str = "gpt-4o",
    is_front: bool = True,
    is_cloze: bool = False,
) -> None:
    """
    Generates a complementary audio transcript for a card side.

    Args:
        transcript_input_file: Path to input markdown file
        output_file: Path to output transcript file
        model: OpenAI model to use
        is_front: Whether this is the front of a card (True) or back (False)
        is_cloze: Whether this is a cloze card
    """
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key)

    with open(transcript_input_file, "r", encoding="utf-8") as f:
        content = f.read().strip()

    # Early return for empty content
    if not content:
        with open(output_file, "w", encoding="utf-8") as out:
            out.write("")
        return

    # Prepare system message based on card type
    if is_front:
        if is_cloze:
            system_content = (
                "You are converting a cloze deletion card to audio format. "
                "Follow these rules precisely:\n"
                "1. If there is a citation key (like @authorYear), always mention it first\n"
                "2. Replace any {{c1::hidden text}} with the word 'BLANK'\n"
                "3. State the sentence naturally, saying 'BLANK' where content is hidden\n"
                "4. Speak any math expressions in natural language\n"
                "5. Keep your response concise and academic\n"
                "6. Never include phrases like 'Question:' or 'Guidance:'\n"
                "7. Never explain what you're doing, just provide the transcript\n"
            )
        else:
            system_content = (
                "You are converting a flashcard question to audio format. "
                "Follow these rules precisely:\n"
                "1. If there is a citation key (like @authorYear), always mention it first\n"
                "2. State only the question without any introductory phrases\n"
                "3. Speak any math expressions in natural language\n"
                "4. Keep your response concise and academic\n"
                "5. Never include phrases like 'Question:' or 'Guidance:'\n"
                "6. Never explain what you're doing, just provide the transcript\n"
            )
    else:  # Back of card
        if is_cloze:
            system_content = (
                "You are providing the answer to a cloze deletion card. "
                "Follow these rules precisely:\n"
                "1. Do NOT restate the question or cite the source again\n"
                "2. Simply state what the hidden text is: 'The missing word is...'\n"
                "3. Speak any math expressions in natural language\n"
                "4. Keep your response very brief - just the missing text\n"
                "5. Never include phrases like 'Answer:' or 'Guidance:'\n"
                "6. Never explain what you're doing, just provide the transcript\n"
            )
        else:
            system_content = (
                "You are providing the answer to a flashcard question. "
                "Follow these rules precisely:\n"
                "1. Do NOT restate the question or cite the source again\n"
                "2. Begin directly with the answer\n"
                "3. Speak any math expressions in natural language\n"
                "4. Keep your response concise and academic\n"
                "5. Never include phrases like 'Answer:' or 'Guidance:'\n"
                "6. Never explain what you're doing, just provide the transcript\n"
                "7. Never start with phrases like 'In the study...' or 'The research shows...'\n"
            )

    # Handle chunks for long content
    enc = tiktoken.get_encoding("cl100k_base")
    tokens = enc.encode(content)
    max_chunk = 3000
    out_chunks: List[str] = []

    for start in range(0, len(tokens), max_chunk):
        chunk = enc.decode(tokens[start : start + max_chunk])
        resp = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": chunk},
            ],
            temperature=0.3,  # Lower temperature for more consistent output
            max_tokens=1000,
        )
        out_chunks.append(resp.choices[0].message.content.strip())

    transcript = "\n\n".join(out_chunks)

    # Remove any remaining "Guidance:" or similar phrases
    transcript = re.sub(r"(Question|Answer|Guidance):\s*", "", transcript)

    with open(output_file, "w", encoding="utf-8") as out:
        out.write(transcript)


def generate_complementary_audio_transcript_plain_card(
    page_md: str, trans_dir: str, citation_key: str = None
) -> List[str]:
    """
    For a plain gen-md file, splits it into cards, then for each front/back:
    - writes input MD,
    - generates a raw transcript via generate_transcript,
    - cleans via clean_transcript,
    and returns cleaned transcript paths.
    """
    base = osp.splitext(osp.basename(page_md))[0]
    os.makedirs(trans_dir, exist_ok=True)
    transcripts: List[str] = []

    # Add citation key if provided
    citation_prefix = f"{citation_key}: " if citation_key else ""

    with open(page_md, "r", encoding="utf-8") as f:
        lines = [l.rstrip("\n") for l in f]
    cards = split_cards(lines)

    for idx, card in enumerate(cards, start=1):
        heading = card["heading"].lstrip("# ").strip()
        # Add citation key to heading if not already present
        if citation_key and not heading.startswith(citation_prefix):
            heading = citation_prefix + heading

        # Check if this is a cloze card
        is_cloze = "{{c" in heading

        # Process card
        if is_cloze:
            # For cloze cards, front is the entire text with cloze markup
            front_txt = heading
            back_txt = heading  # Same text, will be processed differently
        else:
            # For basic cards, split into front/back
            _, front_txt, back_txt = split_front_back(card["heading"], card["body"])

        front_input = osp.join(trans_dir, f"{base}_{idx}_front_input.md")
        back_input = osp.join(trans_dir, f"{base}_{idx}_back_input.md")
        raw_front = osp.join(trans_dir, f"{base}_{idx}_front_raw.md")
        clean_front = osp.join(trans_dir, f"{base}_{idx}_front.md")
        raw_back = osp.join(trans_dir, f"{base}_{idx}_back_raw.md")
        clean_back = osp.join(trans_dir, f"{base}_{idx}_back.md")

        # Write input files
        with open(front_input, "w", encoding="utf-8") as o:
            o.write(front_txt)
        with open(back_input, "w", encoding="utf-8") as o:
            o.write(back_txt)

        # Generate transcripts
        generate_transcript(front_input, raw_front, is_front=True, is_cloze=is_cloze)
        clean_transcript(raw_front, clean_front)
        transcripts.append(clean_front)

        generate_transcript(back_input, raw_back, is_front=False, is_cloze=is_cloze)
        clean_transcript(raw_back, clean_back)
        transcripts.append(clean_back)

    return transcripts


if __name__ == "__main__":
    page_md = "pan-transcriptome/gen-md/page-1.md"
    trans_dir = "pan-transcriptome/gen-md-complementary-audio-transcript"
    os.makedirs(trans_dir, exist_ok=True)
    paths = generate_complementary_audio_transcript_plain_card(page_md, trans_dir)
    print("Generated transcripts for plain cards:")
    for p in paths:
        print(p)
