"""Tests for the ApkgExporter (.apkg direct export)."""

import json
import sqlite3
import tempfile
import zipfile
from pathlib import Path

import pytest

from swanki.processing.apkg_exporter import ApkgExporter


@pytest.fixture
def exporter():
    return ApkgExporter("Test::Deck")


@pytest.fixture
def tmp_dir():
    with tempfile.TemporaryDirectory() as d:
        yield Path(d)


# ── Basic structure ─────────────────────────────────────────────────────


def test_basic_card_export(exporter, tmp_dir):
    """Verify .apkg is a valid zip with collection.anki2 and media."""
    cards = [{"front": "Q1", "back": "A1", "tags": ["t1"]}]
    out = tmp_dir / "basic.apkg"
    exporter.export_from_cards(cards, out, tmp_dir)

    assert out.exists()
    with zipfile.ZipFile(str(out)) as zf:
        names = zf.namelist()
        assert "collection.anki2" in names
        assert "media" in names


def test_note_and_card_counts(exporter, tmp_dir):
    """Verify correct note/card row counts for basic cards."""
    cards = [
        {"front": "Q1", "back": "A1", "tags": []},
        {"front": "Q2", "back": "A2", "tags": []},
        {"front": "Q3", "back": "A3", "tags": []},
    ]
    out = tmp_dir / "counts.apkg"
    exporter.export_from_cards(cards, out, tmp_dir)

    db = _extract_db(out, tmp_dir)
    conn = sqlite3.connect(str(db))
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM notes")
    assert c.fetchone()[0] == 3
    c.execute("SELECT COUNT(*) FROM cards")
    assert c.fetchone()[0] == 3
    conn.close()


# ── Cloze cards ─────────────────────────────────────────────────────────


def test_cloze_generates_multiple_cards(exporter, tmp_dir):
    """Cloze with c1 and c2 should produce 2 card rows."""
    cards = [
        {
            "front": "The {{c1::mitochondria}} is the {{c2::powerhouse}} of the cell",
            "back": "",
            "tags": ["bio"],
        }
    ]
    out = tmp_dir / "cloze.apkg"
    exporter.export_from_cards(cards, out, tmp_dir)

    db = _extract_db(out, tmp_dir)
    conn = sqlite3.connect(str(db))
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM notes")
    assert c.fetchone()[0] == 1
    c.execute("SELECT COUNT(*) FROM cards")
    assert c.fetchone()[0] == 2
    # Check ord values (0-indexed: c1 -> 0, c2 -> 1)
    c.execute("SELECT ord FROM cards ORDER BY ord")
    ords = [row[0] for row in c.fetchall()]
    assert ords == [0, 1]
    conn.close()


# ── Mixed basic + cloze ────────────────────────────────────────────────


def test_mixed_basic_and_cloze(exporter, tmp_dir):
    """Mix of basic and cloze cards in one deck."""
    cards = [
        {"front": "What is DNA?", "back": "Deoxyribonucleic acid", "tags": []},
        {
            "front": "{{c1::ATP}} is the energy currency of the cell",
            "back": "",
            "tags": [],
        },
    ]
    out = tmp_dir / "mixed.apkg"
    exporter.export_from_cards(cards, out, tmp_dir)

    db = _extract_db(out, tmp_dir)
    conn = sqlite3.connect(str(db))
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM notes")
    assert c.fetchone()[0] == 2
    # 1 basic card + 1 cloze card = 2
    c.execute("SELECT COUNT(*) FROM cards")
    assert c.fetchone()[0] == 2
    conn.close()


# ── Media bundling ──────────────────────────────────────────────────────


def test_media_bundling(exporter, tmp_dir):
    """Media files referenced in cards should appear in the zip."""
    # Create fake audio files
    audio1 = tmp_dir / "front.mp3"
    audio2 = tmp_dir / "back.mp3"
    audio1.write_bytes(b"fake-audio-1")
    audio2.write_bytes(b"fake-audio-2")

    cards = [
        {
            "front": "Question\n[audio-front](front.mp3)",
            "back": "Answer\n[audio-back](back.mp3)",
            "tags": [],
        }
    ]
    out = tmp_dir / "media.apkg"
    exporter.export_from_cards(cards, out, tmp_dir)

    with zipfile.ZipFile(str(out)) as zf:
        media_json = json.loads(zf.read("media"))
        media_filenames = set(media_json.values())
        assert "front.mp3" in media_filenames
        assert "back.mp3" in media_filenames
        # Check the actual files are in the zip
        for idx in media_json:
            assert idx in zf.namelist()


# ── Stable IDs ──────────────────────────────────────────────────────────


def test_stable_ids_across_exports():
    """Same deck name should always produce the same model/deck IDs."""
    e1 = ApkgExporter("Stable::Test")
    e2 = ApkgExporter("Stable::Test")
    assert e1.deck_id == e2.deck_id
    assert e1.basic_model_id == e2.basic_model_id
    assert e1.cloze_model_id == e2.cloze_model_id


def test_different_decks_get_different_ids():
    e1 = ApkgExporter("Deck::A")
    e2 = ApkgExporter("Deck::B")
    assert e1.deck_id != e2.deck_id
    # Model IDs should be the same (shared across all decks)
    assert e1.basic_model_id == e2.basic_model_id


# ── export_from_file ────────────────────────────────────────────────────


def test_export_from_file(exporter, tmp_dir):
    """Round-trip: markdown file -> .apkg."""
    md = tmp_dir / "cards.md"
    md.write_text(
        "## Card 1\n\nWhat is water?\n%\nH2O\n\n#chemistry\n\n"
        "## Card 2\n\nThe {{c1::sun}} is a star\n%\n\n#astronomy\n"
    )
    out = tmp_dir / "file.apkg"
    exporter.export_from_file(md, out)

    db = _extract_db(out, tmp_dir)
    conn = sqlite3.connect(str(db))
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM notes")
    assert c.fetchone()[0] == 2
    conn.close()


# ── Schema correctness ─────────────────────────────────────────────────


def test_col_table_has_valid_json(exporter, tmp_dir):
    """Col table should have parseable JSON for models, decks, dconf."""
    cards = [{"front": "Q", "back": "A", "tags": []}]
    out = tmp_dir / "schema.apkg"
    exporter.export_from_cards(cards, out, tmp_dir)

    db = _extract_db(out, tmp_dir)
    conn = sqlite3.connect(str(db))
    c = conn.cursor()
    c.execute("SELECT models, decks, dconf, conf FROM col")
    row = c.fetchone()
    models = json.loads(row[0])
    decks = json.loads(row[1])
    dconf = json.loads(row[2])
    conf = json.loads(row[3])

    assert len(models) == 2  # Basic + Cloze
    assert len(decks) == 2  # Default + our deck
    assert "1" in dconf
    assert "activeDecks" in conf
    conn.close()


def test_cloze_model_type_is_1(exporter, tmp_dir):
    """Cloze model should have type=1 in the col models JSON."""
    cards = [{"front": "{{c1::test}}", "back": "", "tags": []}]
    out = tmp_dir / "cloze_type.apkg"
    exporter.export_from_cards(cards, out, tmp_dir)

    db = _extract_db(out, tmp_dir)
    conn = sqlite3.connect(str(db))
    c = conn.cursor()
    c.execute("SELECT models FROM col")
    models = json.loads(c.fetchone()[0])
    cloze_model = models[str(exporter.cloze_model_id)]
    assert cloze_model["type"] == 1
    conn.close()


def test_flds_uses_unit_separator(exporter, tmp_dir):
    r"""notes.flds should use \x1f as field delimiter."""
    cards = [{"front": "Front text", "back": "Back text", "tags": []}]
    out = tmp_dir / "flds.apkg"
    exporter.export_from_cards(cards, out, tmp_dir)

    db = _extract_db(out, tmp_dir)
    conn = sqlite3.connect(str(db))
    c = conn.cursor()
    c.execute("SELECT flds FROM notes")
    flds = c.fetchone()[0]
    assert "\x1f" in flds
    conn.close()


# ── Helpers ─────────────────────────────────────────────────────────────


def _extract_db(apkg_path: Path, dest_dir: Path) -> Path:
    """Extract collection.anki2 from an .apkg zip."""
    with zipfile.ZipFile(str(apkg_path)) as zf:
        zf.extract("collection.anki2", str(dest_dir))
    return dest_dir / "collection.anki2"
