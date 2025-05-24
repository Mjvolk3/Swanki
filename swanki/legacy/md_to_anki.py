#!/usr/bin/env python3
"""
Markdown to AnkiConnect parser and sender.

Reads a Markdown file, splits into cards by H2 headings,
processes front/back (with `$`, `$$` math support converting to MathJax),
tags, images, audio links, horizontal-splits (`%` or `***`/`---`),
ensures decks, syncs notes (add/update/skip), and media to AnkiConnect.
"""
import argparse
import base64
import json
import os
import re
import sys
from typing import Any, Dict, List, Tuple, Set

import requests  # pip install requests

# Regexes
TAG_LINE_RE = re.compile(r"^\s*[-*]\s*(#.+)$")
TAG_SPLIT_RE = re.compile(r",\s*")
IMAGE_RE = re.compile(r"!\[.*?\]\((.*?)\)")
AUDIO_LINK_RE = re.compile(r"\[audio(?:-front|-back)?\]\((.*?)\)")
MATH_FENCE_RE = re.compile(r"```+\s*([$]{1,2}[\s\S]*?[$]{1,2})\s*```+", re.DOTALL)
HR_SPLIT_RE = re.compile(r"^[*-]{3,}\s*$")


def extract_deck_name(lines: List[str]) -> str:
    # Check if first line contains a deck name
    if lines and lines[0].startswith("# "):
        # Extract just the deck name part if the line contains more content
        deck_part = lines[0].split("##")[0] if "##" in lines[0] else lines[0]
        deck_name = deck_part[2:].strip().replace("/", "::")
        return deck_name

    # Use a fixed name if no H1 header is found
    deck_name = "pan-transcript-test::cards"
    return deck_name


def split_cards(lines: List[str]) -> List[Dict[str, Any]]:
    indices = [i for i, l in enumerate(lines) if l.startswith("## ")]
    if not indices:
        return []
    indices.append(len(lines))
    cards: List[Dict[str, Any]] = []
    for start, end in zip(indices[:-1], indices[1:]):
        heading = lines[start][3:].strip()
        body = lines[start + 1 : end]
        cards.append({"heading": heading, "body": body})
    return cards


def parse_tags(body: List[str]) -> Tuple[List[str], List[str]]:
    tags: List[str] = []
    filtered: List[str] = []
    for line in body:
        m = TAG_LINE_RE.match(line)
        if m:
            raw = m.group(1)
            for t in TAG_SPLIT_RE.split(raw):
                tags.append(t.lstrip("#"))
        else:
            filtered.append(line)
    return tags, filtered


def unwrap_math(text: str) -> str:
    # Remove code fences around math expressions
    text = MATH_FENCE_RE.sub(lambda m: m.group(1), text)
    # Convert block math $$...$$ to MathJax display \[...\]
    text = re.sub(r"\$\$(.*?)\$\$", r"\\[\1\\]", text, flags=re.DOTALL)
    # Convert inline math $...$ to MathJax inline \(...\)
    # avoid matching $$
    text = re.sub(
        r"(?<!\$)\$(?!\$)(.*?)(?<!\$)\$(?!\$)", r"\\(\1\\)", text, flags=re.DOTALL
    )
    return text


def split_front_back(heading: str, body: List[str]) -> Tuple[str, str, str]:
    if "{{c" in heading:
        text = heading + "\n" + "\n".join(body)
        return "cloze", text, ""
    split_idx = None
    for i, line in enumerate(body):
        if line.strip() == "%" or HR_SPLIT_RE.match(line):
            split_idx = i
            break
    if split_idx is not None:
        front = heading + "\n" + "\n".join(body[:split_idx]).strip()
        back = "\n".join(body[split_idx + 1 :]).strip()
    else:
        front = heading
        back = "\n".join(body).strip()
    return "basic", front, back


def process_media(text: str, media: List[str], base_dir: str) -> str:
    def find_file(rel_path: str, base: str) -> str:
        """Find a file by trying different path combinations"""
        # Try direct path first
        if os.path.exists(rel_path):
            # Convert to absolute path if it's not already
            if not os.path.isabs(rel_path):
                return os.path.abspath(rel_path)
            return rel_path

        # Original candidates list
        candidates = [
            # 1. Direct join (standard case)
            os.path.normpath(os.path.join(base, rel_path)),
            # All your other candidate paths...
        ]

        # Return the first path that exists
        for path in candidates:
            if os.path.exists(path):
                return path

        # Nothing found - return the most likely path
        return candidates[0]

    def repl_audio(m: re.Match) -> str:
        rel = m.group(1)
        full = find_file(rel, base_dir)
        fname = os.path.basename(rel)
        media.append(full)
        return f"[sound:{fname}]"

    text = AUDIO_LINK_RE.sub(repl_audio, text)

    def repl_img(m: re.Match) -> str:
        rel = m.group(1)
        if rel.startswith(("http://", "https://")):
            return f'<img src="{rel}">'

        full = find_file(rel, base_dir)
        fname = os.path.basename(rel)
        media.append(full)
        return f'<img src="{fname}">'  # Fixed extra } here

    text = IMAGE_RE.sub(repl_img, text)
    return text


def build_notes(file_path: str) -> Tuple[List[Dict[str, Any]], List[str]]:
    base_dir = os.path.dirname(os.path.abspath(file_path))
    with open(file_path, encoding="utf-8") as f:
        lines = [l.rstrip("\n") for l in f]

    deck = extract_deck_name(lines)
    cards = split_cards(lines)
    notes: List[Dict[str, Any]] = []
    media_paths: List[str] = []

    for c in cards:
        tags, body = parse_tags(c["body"])
        kind, front_md, back_md = split_front_back(c["heading"], body)
        front = unwrap_math(process_media(front_md, media_paths, base_dir))
        back = unwrap_math(process_media(back_md, media_paths, base_dir))

        fields = (
            {"Text": front, "Extra": back}
            if kind == "cloze"
            else {"Front": front, "Back": back}
        )
        note = {
            "deckName": deck,
            "modelName": "Cloze" if kind == "cloze" else "Basic",
            "fields": fields,
            "tags": tags,
        }
        notes.append(note)

    return notes, media_paths


def ensure_decks(notes: List[Dict[str, Any]], host: str, port: int) -> None:
    url = f"http://{host}:{port}"
    decks: Set[str] = {note["deckName"] for note in notes}
    for d in decks:
        requests.post(
            url, json={"action": "createDeck", "version": 6, "params": {"deck": d}}
        )


def notes_differ(existing: Dict[str, Any], new_f: Dict[str, str]) -> bool:
    return any(existing.get(f, {}).get("value") != v for f, v in new_f.items())


def sync_notes(notes: List[Dict[str, Any]], host: str, port: int) -> None:
    url = f"http://{host}:{port}"
    for note in notes:
        deck = note["deckName"]
        model = note["modelName"]
        fields = note["fields"]
        key = "Front" if model == "Basic" else "Text"
        query = f'deck:"{deck}" {key}:"{fields[key]}"'
        fn = requests.post(
            url, json={"action": "findNotes", "version": 6, "params": {"query": query}}
        ).json()
        ids = fn.get("result", [])
        if not ids:
            requests.post(
                url, json={"action": "addNote", "version": 6, "params": {"note": note}}
            )
        else:
            info = requests.post(
                url,
                json={"action": "notesInfo", "version": 6, "params": {"notes": ids}},
            ).json()
            existing = info.get("result", [{}])[0].get("fields", {})
            if notes_differ(existing, fields):
                requests.post(
                    url,
                    json={
                        "action": "updateNoteFields",
                        "version": 6,
                        "params": {"note": {"id": ids[0], "fields": fields}},
                    },
                )


def send_media(media_paths: List[str], host: str, port: int) -> None:
    url = f"http://{host}:{port}"
    for path in media_paths:
        if not os.path.isfile(path):
            print(f"Warning: media not found: {path}", file=sys.stderr)
            continue
        data = base64.b64encode(open(path, "rb").read()).decode("utf-8")
        requests.post(
            url,
            json={
                "action": "storeMediaFile",
                "version": 6,
                "params": {"filename": os.path.basename(path), "data": data},
            },
        )


def main() -> None:
    p = argparse.ArgumentParser(description="MD ➔ AnkiConnect")
    p.add_argument("file", help="Markdown file")
    p.add_argument("--host", default="127.0.0.1")
    p.add_argument("--port", type=int, default=8765)
    p.add_argument("--send", action="store_true")
    p.add_argument("--out", "-o", help="Dump JSON")
    args = p.parse_args()

    notes, media = build_notes(args.file)
    if args.send:
        ensure_decks(notes, args.host, args.port)
        send_media(media, args.host, args.port)
        sync_notes(notes, args.host, args.port)
        print(f"Synced {len(notes)} notes.")
    else:
        dump = {"notes": notes, "media": media}
        js = json.dumps(dump, ensure_ascii=False, indent=2)
        if args.out:
            open(args.out, "w", encoding="utf-8").write(js)
        else:
            print(js)


if __name__ == "__main__":
    main()
