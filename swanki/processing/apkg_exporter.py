"""
swanki/processing/apkg_exporter.py
[[swanki.processing.apkg_exporter]]
https://github.com/Mjvolk3/Swanki/tree/main/swanki/processing/apkg_exporter.py
Test file: tests/test_apkg_exporter.py

Direct .apkg file exporter using only stdlib (sqlite3, zipfile).
"""

import hashlib
import json
import logging
import re
import sqlite3
import tempfile
import time
import zipfile
from pathlib import Path
from typing import Any

from .anki_processor import (
    extract_cards,
    prepare_for_anki,
    validate_and_fix_cloze_format,
)

logger = logging.getLogger(__name__)

# Anki schema version
SCHEMA_VERSION = 11

# Base91 alphabet used by Anki for GUIDs
BASE91_TABLE = (
    "abcdefghijklmnopqrstuvwxyz"
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    "0123456789"
    "!#$%&()*+,-./:;<=>?@[]^_`{|}~"
)


def _stable_id(seed: str) -> int:
    """Generate a stable integer ID from a string seed via SHA-256."""
    h = hashlib.sha256(seed.encode("utf-8")).hexdigest()
    return int(h[:12], 16)


def _guid(fields_text: str) -> str:
    """Generate a base91-encoded GUID from field content (10 chars)."""
    h = hashlib.sha256(fields_text.encode("utf-8")).digest()
    num = int.from_bytes(h[:8], "big")
    chars = []
    for _ in range(10):
        num, remainder = divmod(num, 91)
        chars.append(BASE91_TABLE[remainder])
    return "".join(chars)


def _checksum(first_field: str) -> int:
    """Compute Anki-compatible field checksum."""
    return int(hashlib.sha1(first_field.encode("utf-8")).hexdigest()[:8], 16)


def _epoch_ms() -> int:
    return int(time.time() * 1000)


class ApkgExporter:
    """Export flashcards to .apkg files.

    Parameters
    ----------
    deck_name : str
        Name of the deck (supports ``::`` hierarchy)
    """

    # Fixed seeds for stable model IDs across exports
    BASIC_MODEL_SEED = "swanki-basic-v1"
    CLOZE_MODEL_SEED = "swanki-cloze-v1"

    def __init__(self, deck_name: str):
        """Initialize exporter with a deck name."""
        self.deck_name = deck_name
        self.deck_id = _stable_id(f"swanki-deck::{deck_name}")
        self.basic_model_id = _stable_id(self.BASIC_MODEL_SEED)
        self.cloze_model_id = _stable_id(self.CLOZE_MODEL_SEED)

    # ── public API ──────────────────────────────────────────────────────

    def export_from_file(
        self, md_path: Path, output_path: Path, base_dir: Path | None = None
    ) -> Path:
        """Export cards from a markdown file to .apkg.

        Parameters
        ----------
        md_path : Path
            Markdown file containing cards
        output_path : Path
            Destination .apkg path
        base_dir : Path, optional
            Directory to resolve media paths against (defaults to md_path.parent)

        Returns:
        -------
        Path
            The written .apkg file path
        """
        if base_dir is None:
            base_dir = md_path.parent

        with open(md_path, encoding="utf-8") as f:
            lines = [line.rstrip("\n") for line in f]

        raw_cards = extract_cards(lines)
        logger.info(f"Parsed {len(raw_cards)} cards from {md_path.name}")

        return self.export_from_cards(raw_cards, output_path, base_dir)

    def export_from_cards(
        self,
        card_dicts: list[dict[str, Any]],
        output_path: Path,
        base_dir: Path,
    ) -> Path:
        """Export pre-parsed card dicts to .apkg.

        Parameters
        ----------
        card_dicts : List[Dict]
            Each dict has 'front', 'back', 'tags'
        output_path : Path
            Destination .apkg path
        base_dir : Path
            Directory to resolve relative media paths against

        Returns:
        -------
        Path
            The written .apkg file path
        """
        # Validate / fix cloze issues
        for card in card_dicts:
            validate_and_fix_cloze_format(card)

        # Prepare fields for Anki
        processed: list[dict[str, Any]] = []
        for card in card_dicts:
            is_cloze = "{{c" in card["front"]
            front_content = prepare_for_anki(card["front"])
            back_content = prepare_for_anki(card["back"])

            if is_cloze:
                fields = {"Text": front_content, "Back Extra": back_content}
            else:
                fields = {"Front": front_content, "Back": back_content}

            processed.append(
                {
                    "fields": fields,
                    "tags": card.get("tags", []),
                    "is_cloze": is_cloze,
                }
            )

        # Collect media
        media_files = self._collect_media(processed, base_dir)

        # Build database
        db_path = self._build_database(processed)

        # Package
        self._build_package(db_path, media_files, output_path)

        logger.info(
            f"Wrote {output_path} ({len(processed)} notes, {len(media_files)} media files)"
        )
        return output_path

    # ── internals ───────────────────────────────────────────────────────

    def _collect_media(
        self, processed_cards: list[dict[str, Any]], base_dir: Path
    ) -> list[Path]:
        """Collect referenced media files from processed card content."""
        seen: set[str] = set()
        media: list[Path] = []

        for card in processed_cards:
            for field_value in card["fields"].values():
                # [sound:filename.mp3]
                for m in re.findall(r"\[sound:([^\]]+)\]", field_value):
                    if m not in seen:
                        seen.add(m)
                        path = self._find_media(m, base_dir)
                        if path:
                            media.append(path)

                # <img src="filename.png">
                for m in re.findall(r'<img src="([^"]+)">', field_value):
                    if m.startswith(("http://", "https://")):
                        continue
                    if m not in seen:
                        seen.add(m)
                        path = self._find_media(m, base_dir)
                        if path:
                            media.append(path)

        return media

    @staticmethod
    def _find_media(filename: str, base_dir: Path) -> Path | None:
        """Resolve a media filename to an existing file path."""
        # Try base_dir directly
        candidate = base_dir / filename
        if candidate.exists():
            return candidate

        # Try parent directories (up to 3 levels)
        current = base_dir
        for _ in range(3):
            current = current.parent
            candidate = current / filename
            if candidate.exists():
                return candidate

        logger.debug(f"Media file not found: {filename} (searched from {base_dir})")
        return None

    def _build_database(self, processed_cards: list[dict[str, Any]]) -> Path:
        """Create a temporary SQLite database with Anki schema."""
        tmp = tempfile.NamedTemporaryFile(suffix=".anki2", delete=False)
        tmp.close()
        db_path = Path(tmp.name)

        conn = sqlite3.connect(str(db_path))
        c = conn.cursor()

        # Create Anki tables
        c.executescript(
            """
            CREATE TABLE col (
                id   INTEGER PRIMARY KEY,
                crt  INTEGER NOT NULL,
                mod  INTEGER NOT NULL,
                scm  INTEGER NOT NULL,
                ver  INTEGER NOT NULL,
                dty  INTEGER NOT NULL,
                usn  INTEGER NOT NULL,
                ls   INTEGER NOT NULL,
                conf TEXT NOT NULL,
                models TEXT NOT NULL,
                decks TEXT NOT NULL,
                dconf TEXT NOT NULL,
                tags TEXT NOT NULL
            );
            CREATE TABLE notes (
                id    INTEGER PRIMARY KEY,
                guid  TEXT NOT NULL,
                mid   INTEGER NOT NULL,
                mod   INTEGER NOT NULL,
                usn   INTEGER NOT NULL,
                tags  TEXT NOT NULL,
                flds  TEXT NOT NULL,
                sfld  TEXT NOT NULL,
                csum  INTEGER NOT NULL,
                flags INTEGER NOT NULL,
                data  TEXT NOT NULL
            );
            CREATE TABLE cards (
                id    INTEGER PRIMARY KEY,
                nid   INTEGER NOT NULL,
                did   INTEGER NOT NULL,
                ord   INTEGER NOT NULL,
                mod   INTEGER NOT NULL,
                usn   INTEGER NOT NULL,
                type  INTEGER NOT NULL,
                queue INTEGER NOT NULL,
                due   INTEGER NOT NULL,
                ivl   INTEGER NOT NULL,
                factor INTEGER NOT NULL,
                reps  INTEGER NOT NULL,
                lapses INTEGER NOT NULL,
                left  INTEGER NOT NULL,
                odue  INTEGER NOT NULL,
                odid  INTEGER NOT NULL,
                flags INTEGER NOT NULL,
                data  TEXT NOT NULL
            );
            CREATE TABLE revlog (
                id    INTEGER PRIMARY KEY,
                cid   INTEGER NOT NULL,
                usn   INTEGER NOT NULL,
                ease  INTEGER NOT NULL,
                ivl   INTEGER NOT NULL,
                lastIvl INTEGER NOT NULL,
                factor INTEGER NOT NULL,
                time  INTEGER NOT NULL,
                type  INTEGER NOT NULL
            );
            CREATE TABLE graves (
                usn  INTEGER NOT NULL,
                oid  INTEGER NOT NULL,
                type INTEGER NOT NULL
            );
            """
        )

        now_s = int(time.time())
        now_ms = _epoch_ms()

        # Models JSON
        basic_model = self._basic_model_json(now_s)
        cloze_model = self._cloze_model_json(now_s)
        models = {
            str(self.basic_model_id): basic_model,
            str(self.cloze_model_id): cloze_model,
        }

        # Deck JSON
        deck = {
            "id": self.deck_id,
            "mod": now_s,
            "name": self.deck_name,
            "usn": -1,
            "lrnToday": [0, 0],
            "revToday": [0, 0],
            "newToday": [0, 0],
            "timeToday": [0, 0],
            "collapsed": False,
            "browserCollapsed": False,
            "desc": "",
            "dyn": 0,
            "conf": 1,
            "extendNew": 0,
            "extendRev": 0,
        }
        # Include default deck so Anki doesn't complain
        default_deck = {
            "id": 1,
            "mod": 0,
            "name": "Default",
            "usn": 0,
            "lrnToday": [0, 0],
            "revToday": [0, 0],
            "newToday": [0, 0],
            "timeToday": [0, 0],
            "collapsed": False,
            "browserCollapsed": False,
            "desc": "",
            "dyn": 0,
            "conf": 1,
            "extendNew": 0,
            "extendRev": 0,
        }
        decks = {"1": default_deck, str(self.deck_id): deck}

        # Deck config
        dconf = {
            "1": {
                "id": 1,
                "mod": 0,
                "name": "Default",
                "usn": 0,
                "maxTaken": 60,
                "autoplay": True,
                "timer": 0,
                "replayq": True,
                "new": {
                    "bury": True,
                    "delays": [1, 10],
                    "initialFactor": 2500,
                    "ints": [1, 4, 7],
                    "order": 1,
                    "perDay": 20,
                },
                "rev": {
                    "bury": True,
                    "ease4": 1.3,
                    "fuzz": 0.05,
                    "ivlFct": 1,
                    "maxIvl": 36500,
                    "perDay": 200,
                    "minSpace": 1,
                },
                "lapse": {
                    "delays": [10],
                    "leechAction": 0,
                    "leechFails": 8,
                    "minInt": 1,
                    "mult": 0,
                },
            }
        }

        conf = json.dumps(
            {
                "activeDecks": [1],
                "curDeck": 1,
                "newSpread": 0,
                "collapseTime": 1200,
                "timeLim": 0,
                "estTimes": True,
                "dueCounts": True,
                "curModel": None,
                "nextPos": 1,
                "sortType": "noteFld",
                "sortBackwards": False,
                "addToCur": True,
            }
        )

        c.execute(
            "INSERT INTO col VALUES (1,?,?,?,?,0,-1,0,?,?,?,?,?)",
            (
                now_s,
                now_s,
                now_ms,
                SCHEMA_VERSION,
                conf,
                json.dumps(models),
                json.dumps(decks),
                json.dumps(dconf),
                json.dumps({}),
            ),
        )

        # Insert notes and cards
        card_id_counter = now_ms
        note_id_counter = now_ms

        for idx, card in enumerate(processed_cards):
            is_cloze = card["is_cloze"]
            fields = card["fields"]
            tags = card.get("tags", [])

            if is_cloze:
                mid = self.cloze_model_id
                field_values = [fields.get("Text", ""), fields.get("Back Extra", "")]
                first_field = field_values[0]
            else:
                mid = self.basic_model_id
                field_values = [fields.get("Front", ""), fields.get("Back", "")]
                first_field = field_values[0]

            flds = "\x1f".join(field_values)
            guid = _guid(flds)
            csum = _checksum(first_field)
            tags_str = " ".join(tags)

            note_id = note_id_counter + idx
            c.execute(
                "INSERT INTO notes VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                (
                    note_id,
                    guid,
                    mid,
                    now_s,
                    -1,
                    tags_str,
                    flds,
                    first_field,
                    csum,
                    0,
                    "",
                ),
            )

            # Cards
            if is_cloze:
                # One card per unique cloze number
                cloze_nums = set(
                    int(m) for m in re.findall(r"\{\{c(\d+)::", fields.get("Text", ""))
                )
                if not cloze_nums:
                    cloze_nums = {1}
                for cn in sorted(cloze_nums):
                    card_id = card_id_counter + idx * 100 + cn
                    c.execute(
                        "INSERT INTO cards VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                        (
                            card_id,
                            note_id,
                            self.deck_id,
                            cn - 1,  # ord is 0-indexed
                            now_s,
                            -1,
                            0,  # card type: new
                            0,  # queue status: new
                            0,  # due
                            0,  # ivl
                            0,  # factor
                            0,  # reps
                            0,  # lapses
                            0,  # left
                            0,  # odue
                            0,  # odid
                            0,  # flags
                            "",  # data
                        ),
                    )
            else:
                card_id = card_id_counter + idx * 100
                c.execute(
                    "INSERT INTO cards VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                    (
                        card_id,
                        note_id,
                        self.deck_id,
                        0,  # ord
                        now_s,
                        -1,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        "",
                    ),
                )

        conn.commit()
        conn.close()
        return db_path

    def _build_package(
        self, db_path: Path, media_files: list[Path], output_path: Path
    ) -> None:
        """Zip the database and media into an .apkg."""
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with zipfile.ZipFile(str(output_path), "w", zipfile.ZIP_DEFLATED) as zf:
            zf.write(str(db_path), "collection.anki2")

            media_json: dict[str, str] = {}
            for i, media_path in enumerate(media_files):
                idx = str(i)
                media_json[idx] = media_path.name
                zf.write(str(media_path), idx)

            zf.writestr("media", json.dumps(media_json))

        # Clean up temp db
        db_path.unlink(missing_ok=True)

    # ── model definitions ───────────────────────────────────────────────

    def _basic_model_json(self, mod: int) -> dict[str, Any]:
        return {
            "id": self.basic_model_id,
            "name": "Basic",
            "type": 0,
            "mod": mod,
            "usn": -1,
            "sortf": 0,
            "did": self.deck_id,
            "tmpls": [
                {
                    "name": "Card 1",
                    "qfmt": "{{Front}}",
                    "afmt": '{{FrontSide}}<hr id="answer">{{Back}}',
                    "bqfmt": "",
                    "bafmt": "",
                    "ord": 0,
                    "did": None,
                }
            ],
            "flds": [
                {
                    "name": "Front",
                    "ord": 0,
                    "sticky": False,
                    "rtl": False,
                    "font": "Arial",
                    "size": 20,
                    "media": [],
                },
                {
                    "name": "Back",
                    "ord": 1,
                    "sticky": False,
                    "rtl": False,
                    "font": "Arial",
                    "size": 20,
                    "media": [],
                },
            ],
            "css": ".card {\n font-family: arial;\n font-size: 20px;\n text-align: center;\n color: black;\n background-color: white;\n}\n",
            "latexPre": "\\documentclass[12pt]{article}\n\\special{papersize=3in,5in}\n\\usepackage[utf8]{inputenc}\n\\usepackage{amssymb,amsmath}\n\\pagestyle{empty}\n\\setlength{\\parindent}{0in}\n\\begin{document}\n",
            "latexPost": "\\end{document}",
            "latexsvg": False,
            "req": [[0, "all", [0]]],
            "tags": [],
            "vers": [],
        }

    def _cloze_model_json(self, mod: int) -> dict[str, Any]:
        return {
            "id": self.cloze_model_id,
            "name": "Cloze",
            "type": 1,
            "mod": mod,
            "usn": -1,
            "sortf": 0,
            "did": self.deck_id,
            "tmpls": [
                {
                    "name": "Cloze",
                    "qfmt": "{{cloze:Text}}",
                    "afmt": "{{cloze:Text}}<br>{{Back Extra}}",
                    "bqfmt": "",
                    "bafmt": "",
                    "ord": 0,
                    "did": None,
                }
            ],
            "flds": [
                {
                    "name": "Text",
                    "ord": 0,
                    "sticky": False,
                    "rtl": False,
                    "font": "Arial",
                    "size": 20,
                    "media": [],
                },
                {
                    "name": "Back Extra",
                    "ord": 1,
                    "sticky": False,
                    "rtl": False,
                    "font": "Arial",
                    "size": 20,
                    "media": [],
                },
            ],
            "css": ".card {\n font-family: arial;\n font-size: 20px;\n text-align: center;\n color: black;\n background-color: white;\n}\n.cloze {\n font-weight: bold;\n color: blue;\n}\n.nightMode .cloze {\n color: lightblue;\n}\n",
            "latexPre": "\\documentclass[12pt]{article}\n\\special{papersize=3in,5in}\n\\usepackage[utf8]{inputenc}\n\\usepackage{amssymb,amsmath}\n\\pagestyle{empty}\n\\setlength{\\parindent}{0in}\n\\begin{document}\n",
            "latexPost": "\\end{document}",
            "latexsvg": False,
            "req": [[0, "all", [0]]],
            "tags": [],
            "vers": [],
        }
