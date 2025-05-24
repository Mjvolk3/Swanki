#!/usr/bin/env python3
"""
Swanki: Complementary audio transcript generation for plain and image-based cards.
"""
import os
import os.path as osp
from pathlib import Path
from typing import List
from dotenv import load_dotenv
from openai import OpenAI
import tiktoken
from .md_to_anki import split_cards, split_front_back


def clean_transcript(raw_file: str, clean_file: str) -> None:
    """Simplify the raw transcript by stripping lines and collapsing blanks."""
    lines = [l.strip() for l in open(raw_file, "r", encoding="utf-8")]
    cleaned: List[str] = []
    prev_blank = False
    for l in lines:
        if not l:
            if not prev_blank:
                cleaned.append("")
                prev_blank = True
        else:
            cleaned.append(l)
            prev_blank = False
    with open(clean_file, "w", encoding="utf-8") as f:
        f.write("\n".join(cleaned))


def generate_front_transcript(
    transcript_input: str, transcript_output: str, model: str = "gpt-4o"
) -> None:
    """Generate a spoken-style transcript for the front (question) of a card."""
    load_dotenv()
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    text = open(transcript_input, "r", encoding="utf-8").read().strip()
    enc = tiktoken.get_encoding("cl100k_base")
    tokens = enc.encode(text)
    max_chunk = 3000
    out: List[str] = []
    for start in range(0, len(tokens), max_chunk):
        chunk = enc.decode(tokens[start : start + max_chunk])
        resp = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are creating an audio version of a scientific flashcard question that references an image. "
                        "Follow these guidelines precisely:\n\n"
                        "1. If there is a citation key (like @authorYear), ALWAYS start with it\n"
                        "2. Focus on conceptual understanding rather than details like P-values or specific colors\n"
                        "3. Provide just enough context about the image for the listener to understand the question\n"
                        "4. Keep your response to 2-3 sentences maximum\n"
                        "5. Use natural spoken language - convert any math notation to spoken form\n"
                        "6. Ensure the question is specific enough to be answerable without seeing the image\n"
                        "7. Focus on teaching concepts rather than testing recall of visual details\n"
                        "8. Maintain academic rigor appropriate for graduate-level education\n"
                        "Remember that listeners cannot see the image, so make sure the audio provides enough context"
                    ),
                },
                {"role": "user", "content": chunk},
            ],
            temperature=0.4,  # Lower temperature for more consistent output
            max_tokens=350,  # Limit length of response
        )
        out.append(resp.choices[0].message.content.strip())
    combined = "\n\n".join(out)
    with open(transcript_output, "w", encoding="utf-8") as f:
        f.write(combined)


def generate_back_transcript(
    transcript_input: str, transcript_output: str, model: str = "gpt-4o"
) -> None:
    """Generate a spoken-style transcript for the back (answer) of a card."""
    load_dotenv()
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    text = open(transcript_input, "r", encoding="utf-8").read().strip()
    enc = tiktoken.get_encoding("cl100k_base")
    tokens = enc.encode(text)
    max_chunk = 3000
    out: List[str] = []
    for start in range(0, len(tokens), max_chunk):
        chunk = enc.decode(tokens[start : start + max_chunk])
        resp = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are creating an audio version of a scientific flashcard answer. "
                        "Follow these guidelines precisely:\n\n"
                        "1. DO NOT restate the question - the listener just heard it\n"
                        "2. Directly answer the specific question asked\n"
                        "3. Keep your response to 3-4 sentences maximum\n"
                        "4. Focus on conceptual understanding rather than details\n"
                        "5. Use natural spoken language - convert any math notation to spoken form\n"
                        "6. DO NOT use phrases like 'We know we are being asked' or 'The question refers to'\n"
                        "7. DO NOT discuss elements not directly relevant to answering the question\n"
                        "8. Maintain academic rigor appropriate for graduate-level education\n"
                        "9. Be precise and focus on teaching the concept, not testing recall\n"
                        "Remember that listeners cannot see the image, so incorporate necessary visual context"
                    ),
                },
                {"role": "user", "content": chunk},
            ],
            temperature=0.4,  # Lower temperature for more consistent output
            max_tokens=500,  # Limit length of response
        )
        out.append(resp.choices[0].message.content.strip())
    combined = "\n\n".join(out)
    with open(transcript_output, "w", encoding="utf-8") as f:
        f.write(combined)


def generate_back_transcript(
    transcript_input: str, transcript_output: str, model: str = "gpt-4o"
) -> None:
    """Generate a spoken-style transcript for the back (answer) of a card."""
    load_dotenv()
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    text = open(transcript_input, "r", encoding="utf-8").read().strip()
    enc = tiktoken.get_encoding("cl100k_base")
    tokens = enc.encode(text)
    max_chunk = 3000
    out: List[str] = []
    for start in range(0, len(tokens), max_chunk):
        chunk = enc.decode(tokens[start : start + max_chunk])
        resp = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You're creating an audio version of a flashcard answer about scientific concepts. "
                        "The original answer refers to an image the listener cannot see. Your task is to:\n"
                        "1. If there is a citation key (like @authorYear), always mention it first.\n"
                        "2. Provide a clear, conceptual explanation that directly addresses the question\n"
                        "3. Begin with a brief restatement of the question for context, using natural language\n"
                        "4. Deliver the answer in a natural, spoken style without headings like 'Answer:'\n"
                        "5. Focus on the scientific significance and conceptual understanding\n"
                        "6. Include only relevant details that support conceptual understanding\n"
                        "7. Convert any mathematical notation into spoken language"
                    ),
                },
                {"role": "user", "content": chunk},
            ],
            temperature=0.7,
            max_tokens=1000,
        )
        out.append(resp.choices[0].message.content.strip())
    combined = "\n\n".join(out)
    with open(transcript_output, "w", encoding="utf-8") as f:
        f.write(combined)


def generate_complementary_audio_transcript_image_card(
    page_md: str, trans_dir: str, image_summary_dir: str, citation_key: str = None
) -> List[str]:
    """
    Generate complementary audio transcripts (front+back) for image cards:
    - Front: asks a rephrased question with context
    - Back: answers that question using context and original card content

    Args:
        page_md: Path to the image card markdown file
        trans_dir: Directory to save transcript files
        image_summary_dir: Directory containing image summaries
        citation_key: Optional citation key to prefix questions
    """
    stem = Path(page_md).stem  # e.g. page-3_card_1_1
    parts = stem.split("_")  # ['page-3','card','1','1']
    page = parts[0]
    img_idx = parts[2]
    summary_path = osp.join(image_summary_dir, f"{page}_{img_idx}.md")
    summary = ""
    if osp.exists(summary_path):
        summary = open(summary_path, "r", encoding="utf-8").read().strip()

    os.makedirs(trans_dir, exist_ok=True)
    results: List[str] = []
    lines = open(page_md, "r", encoding="utf-8").read().splitlines()
    cards = split_cards(lines)

    # Add citation key if provided
    citation_prefix = f"{citation_key}: " if citation_key else ""

    for idx, (heading, body) in enumerate(cards, start=1):
        # get front/back markdown
        _, front_md, back_md = split_front_back(heading, body)
        question_text = heading.lstrip("# ").strip()

        # Add citation key to question text if not already present
        if citation_key and not question_text.startswith(citation_prefix):
            question_text = citation_prefix + question_text

        # file paths
        front_input = osp.join(trans_dir, f"{stem}_{idx}_front_input.md")
        front_raw = osp.join(trans_dir, f"{stem}_{idx}_front_raw.md")
        front_clean = osp.join(trans_dir, f"{stem}_{idx}_front.md")
        back_input = osp.join(trans_dir, f"{stem}_{idx}_back_input.md")
        back_raw = osp.join(trans_dir, f"{stem}_{idx}_back_raw.md")
        back_clean = osp.join(trans_dir, f"{stem}_{idx}_back.md")

        # Prepare front transcript input: question + context
        front_payload = (
            f"Question: {question_text}\n"
            + (f"\nImage Description: {summary}" if summary else "")
            + "\n\nYour task is to create a concise audio version of this question that someone can understand without seeing the image. "
            + "If there is a citation key (e.g., @authorYear) at the beginning of the question, always start with it. "
            + "Provide just enough context about what's in the image to make the question clear."
        )
        with open(front_input, "w", encoding="utf-8") as f:
            f.write(front_payload)
        generate_front_transcript(front_input, front_raw)
        clean_transcript(front_raw, front_clean)
        results.append(front_clean)

        # Prepare back transcript input: answer label + context + back content
        back_payload = (
            f"Question: {question_text}\n"
            + (f"\nImage Description: {summary}" if summary else "")
            + f"\n\nAnswer: {back_md}"
            + "\n\nYour task is to create a concise audio version of this answer that someone can understand without seeing the image. "
            + "Do NOT restate the question - the listener has just heard it. "
            + "Directly answer the specific question that was asked."
        )
        with open(back_input, "w", encoding="utf-8") as f:
            f.write(back_payload)
        generate_back_transcript(back_input, back_raw)
        clean_transcript(back_raw, back_clean)
        results.append(back_clean)

    return results


def generate_complementary_audio_transcript_plain_card(
    page_md: str, trans_dir: str
) -> List[str]:
    """
    Generate complementary audio transcripts (front+back) for plain text cards:
    - Front: narrates the question in spoken form
    - Back: provides the answer in a form suitable for audio learning
    """
    stem = Path(page_md).stem  # e.g. page-1

    os.makedirs(trans_dir, exist_ok=True)
    results: List[str] = []
    lines = open(page_md, "r", encoding="utf-8").read().splitlines()
    cards = split_cards(lines)

    for idx, (heading, body) in enumerate(cards, start=1):
        # get front/back markdown
        _, front_md, back_md = split_front_back(heading, body)
        question_text = heading.lstrip("# ").strip()

        # file paths
        front_input = osp.join(trans_dir, f"{stem}_{idx}_front_input.md")
        front_raw = osp.join(trans_dir, f"{stem}_{idx}_front_raw.md")
        front_clean = osp.join(trans_dir, f"{stem}_{idx}_front.md")
        back_input = osp.join(trans_dir, f"{stem}_{idx}_back_input.md")
        back_raw = osp.join(trans_dir, f"{stem}_{idx}_back_raw.md")
        back_clean = osp.join(trans_dir, f"{stem}_{idx}_back.md")

        # Prepare front transcript input: just the question
        with open(front_input, "w", encoding="utf-8") as f:
            f.write(f"Question: {question_text}")
        generate_front_transcript(front_input, front_raw)
        clean_transcript(front_raw, front_clean)
        results.append(front_clean)

        # Prepare back transcript input: question + answer
        with open(back_input, "w", encoding="utf-8") as f:
            f.write(f"Question: {question_text}\n\nAnswer details: {back_md}")
        generate_back_transcript(back_input, back_raw)
        clean_transcript(back_raw, back_clean)
        results.append(back_clean)

    return results


if __name__ == "__main__":
    # Quick test for image-card transcript generation
    page_md = "pan-transcriptome/anki-image-cards/page-3_card_1_1.md"
    trans_dir = "pan-transcriptome/anki-image-cards-complementary-audio-transcript"
    summary_dir = "pan-transcriptome/image-summaries"

    os.makedirs(trans_dir, exist_ok=True)
    paths = generate_complementary_audio_transcript_image_card(
        page_md, trans_dir, summary_dir
    )
    print("Generated image-card transcripts:")
    for p in paths:
        print(p)
