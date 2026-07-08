"""
tests/test_audio_card_replace.py
[[tests.test_audio_card_replace]]
Test file: tests/test_audio_card_replace.py

Tests for swanki.audio.card_replace -- surgical one-for-one card replacement.
The whole-side re-TTS (card_edit._whole_side_retts) and every AnkiConnect call
are patched, so NO Fish / ffmpeg / network runs. Coverage mirrors the plan's
verification: both-sides regen with explicit new_text, independent Front/Back
field rebuild (@citation front-only, one [sound:] per side), uuid-regex note
match (unique / 0 / >1), Feedback preservation, manifest-absent text-only
degrade, and the on-disk md patch (model_copy, uuid preserved).
"""

import json
from pathlib import Path
from unittest.mock import patch

import pytest

from swanki.audio.card_replace import replace_card
from swanki.models.cards import CardContent, PlainCard

UUID = "card-uuid-1"
KEY = "key"
FISH_KWARGS = {
    "provider": "fish_speech",
    "server_url": "http://localhost:8080",
    "reference_id": "test-voice",
    "preprocessor": {},
}


def _target_card() -> PlainCard:
    c = PlainCard(
        front=CardContent(text="Old front question?"),
        back=CardContent(text="Old back answer."),
        tags=["microbiology"],
        card_id=UUID,
    )
    c.audio_front_uri = f"gen-md-complementary-audio/{KEY}_{UUID}_front.mp3"
    c.audio_back_uri = f"gen-md-complementary-audio/{KEY}_{UUID}_back.mp3"
    return c


def _other_card() -> PlainCard:
    c = PlainCard(
        front=CardContent(text="Other card front?"),
        back=CardContent(text="Other back."),
        tags=["chemistry"],
        card_id="other-uuid",
    )
    c.audio_front_uri = f"gen-md-complementary-audio/{KEY}_other_front.mp3"
    c.audio_back_uri = f"gen-md-complementary-audio/{KEY}_other_back.mp3"
    return c


def _setup(tmp: Path) -> Path:
    """Write the nested manifest, mp3 stubs, and both md files; return manifest path."""
    audio_dir = tmp / "gen-md-complementary-audio"
    chunks_dir = audio_dir / "card_chunks"
    chunks_dir.mkdir(parents=True)

    (audio_dir / "key_citation.mp3").write_bytes(b"citation")
    (audio_dir / f"{KEY}_{UUID}_front.mp3").write_bytes(b"front-side")
    (audio_dir / f"{KEY}_{UUID}_back.mp3").write_bytes(b"back-side")

    manifest = {
        "audio_type": "card",
        "card_id": UUID,
        "card_index": 3,
        "front_file": f"{KEY}_{UUID}_front.mp3",
        "back_file": f"{KEY}_{UUID}_back.mp3",
        "citation_audio": "../key_citation.mp3",
        "sides": {
            "front": {
                "chunks": [{"index": 0, "type": "tts", "text": "f", "file": "x"}]
            },
            "back": {"chunks": [{"index": 0, "type": "tts", "text": "b", "file": "y"}]},
        },
    }
    mp = chunks_dir / f"{UUID}_manifest.json"
    mp.write_text(json.dumps(manifest, indent=2))

    cards = [_target_card(), _other_card()]
    (tmp / "cards-with-audio.md").write_text(
        "".join(c.to_md(include_audio=True, citation_key=KEY) for c in cards)
    )
    (tmp / "cards-plain.md").write_text(
        "".join(c.to_md(include_audio=False, citation_key=KEY) for c in cards)
    )
    return mp


def _fake_retts(**kw) -> Path:
    """Stand in for card_edit._whole_side_retts: return the canonical side mp3."""
    manifest = kw["manifest"]
    fname = manifest["front_file"] if kw["side"] == "front" else manifest["back_file"]
    return kw["card_manifest_path"].parent.parent / fname


def _fake_anki(calls: list, *, find: list | None = None):
    def inner(url, action, params=None):
        calls.append((action, params))
        if action == "findNotes":
            return [12345] if find is None else find
        if action == "notesInfo":
            return [
                {
                    "noteId": 12345,
                    "fields": {
                        "Front": {"value": "old", "order": 0},
                        "Back": {"value": "old", "order": 1},
                        "Feedback": {"value": "keep me", "order": 2},
                    },
                }
            ]
        return None

    return inner


def _run(tmp, calls, *, find=None, note_id=None):
    mp = _setup(tmp)
    with (
        patch(
            "swanki.audio.card_replace._whole_side_retts", side_effect=_fake_retts
        ) as retts,
        patch(
            "swanki.audio.card_replace.ankiconnect_call",
            side_effect=_fake_anki(calls, find=find),
        ),
    ):
        res = replace_card(
            mp,
            new_front_text="New front prose",
            new_back_text="New back prose",
            citation_key=KEY,
            tts_kwargs=FISH_KWARGS,
            ankiconnect_url="http://127.0.0.1:8765",
            note_id=note_id,
        )
    return mp, res, retts


def _fields_of(calls: list, action: str) -> dict:
    return next(p["note"]["fields"] for a, p in calls if a == action)


# (a) both-sides regen calls the whole-side re-TTS path with explicit new_text.
def test_both_sides_regen_with_new_text(tmp_path):
    calls: list = []
    _, res, retts = _run(tmp_path, calls)
    assert retts.call_count == 2
    by_side = {c.kwargs["side"]: c.kwargs["new_text"] for c in retts.call_args_list}
    assert by_side == {"front": "New front prose", "back": "New back prose"}
    assert res.front_file.name == f"{KEY}_{UUID}_front.mp3"
    assert res.back_file.name == f"{KEY}_{UUID}_back.mp3"


# (b) Front field: @citation prefix + one [sound:front]; Back: no prefix + one [sound:back].
def test_field_rebuild_front_prefix_back_none(tmp_path):
    calls: list = []
    _run(tmp_path, calls)
    fields = _fields_of(calls, "updateNoteFields")
    assert fields["Front"].startswith(f"@{KEY}:")
    assert fields["Front"].count("[sound:") == 1
    assert f"[sound:{KEY}_{UUID}_front.mp3]" in fields["Front"]
    assert f"@{KEY}:" not in fields["Back"]
    assert fields["Back"].count("[sound:") == 1
    assert f"[sound:{KEY}_{UUID}_back.mp3]" in fields["Back"]


def test_no_double_citation_prefix(tmp_path):
    """A new front already carrying @key: is not prefixed twice."""
    mp = _setup(tmp_path)
    calls: list = []
    with (
        patch("swanki.audio.card_replace._whole_side_retts", side_effect=_fake_retts),
        patch(
            "swanki.audio.card_replace.ankiconnect_call", side_effect=_fake_anki(calls)
        ),
    ):
        replace_card(
            mp,
            new_front_text=f"@{KEY}: Already prefixed",
            new_back_text="B",
            citation_key=KEY,
            tts_kwargs=FISH_KWARGS,
            ankiconnect_url="u",
        )
    fields = _fields_of(calls, "updateNoteFields")
    assert fields["Front"].count(f"@{KEY}:") == 1


# (c) uuid-regex note match: exactly one, raises on 0 / >1.
def test_note_match_unique(tmp_path):
    calls: list = []
    _, res, _ = _run(tmp_path, calls)
    assert res.note_id == 12345
    query = next(p["query"] for a, p in calls if a == "findNotes")
    assert f"Front:re:{UUID}" in query and f"Back:re:{UUID}" in query


def test_note_match_zero_raises(tmp_path):
    with pytest.raises(AssertionError, match="exactly one note"):
        _run(tmp_path, [], find=[])


def test_note_match_multiple_raises(tmp_path):
    with pytest.raises(AssertionError, match="exactly one note"):
        _run(tmp_path, [], find=[1, 2])


def test_note_id_override_skips_findnotes(tmp_path):
    calls: list = []
    _, res, _ = _run(tmp_path, calls, note_id=999)
    assert res.note_id == 999
    assert not any(a == "findNotes" for a, _ in calls)


# (d) updateNoteFields fields dict includes the preserved Feedback.
def test_feedback_preserved(tmp_path):
    calls: list = []
    _run(tmp_path, calls)
    fields = _fields_of(calls, "updateNoteFields")
    assert fields["Feedback"] == "keep me"


def test_store_media_both_sides_and_one_sync(tmp_path):
    calls: list = []
    _run(tmp_path, calls)
    stored = [p["filename"] for a, p in calls if a == "storeMediaFile"]
    assert stored == [f"{KEY}_{UUID}_front.mp3", f"{KEY}_{UUID}_back.mp3"]
    assert sum(1 for a, _ in calls if a == "sync") == 1


# (e) manifest-absent degrades to text-only and requires note_id.
def test_manifest_absent_requires_note_id(tmp_path):
    with pytest.raises(AssertionError, match="requires note_id"):
        replace_card(
            tmp_path / "nope.json",
            new_front_text="F",
            new_back_text="B",
            citation_key=KEY,
            tts_kwargs=FISH_KWARGS,
            ankiconnect_url="u",
            note_id=None,
        )


def test_manifest_absent_text_only(tmp_path):
    calls: list = []
    with (
        patch(
            "swanki.audio.card_replace._whole_side_retts", side_effect=_fake_retts
        ) as r,
        patch(
            "swanki.audio.card_replace.ankiconnect_call", side_effect=_fake_anki(calls)
        ),
    ):
        res = replace_card(
            tmp_path / "nope.json",
            new_front_text="Text front",
            new_back_text="Text back",
            citation_key=KEY,
            tts_kwargs=FISH_KWARGS,
            ankiconnect_url="u",
            note_id=777,
        )
    assert res.degraded is True
    assert res.front_file is None and res.back_file is None
    r.assert_not_called()
    assert not any(a == "storeMediaFile" for a, _ in calls)
    fields = _fields_of(calls, "updateNoteFields")
    assert fields["Front"].startswith(f"@{KEY}:") and "[sound:" not in fields["Front"]
    assert fields["Feedback"] == "keep me"


# (f) cards-plain.md / cards-with-audio.md updated via model_copy (uuid preserved).
def test_markdown_files_patched_uuid_preserved(tmp_path):
    calls: list = []
    _run(tmp_path, calls)

    audio_md = (tmp_path / "cards-with-audio.md").read_text()
    plain_md = (tmp_path / "cards-plain.md").read_text()

    # Target card replaced in BOTH files.
    assert "New front prose" in audio_md and "New back prose" in audio_md
    assert "New front prose" in plain_md and "New back prose" in plain_md
    assert "Old front question?" not in audio_md
    assert "Old back answer." not in plain_md

    # uuid (audio uri) preserved in cards-with-audio.md; other card untouched.
    assert f"{KEY}_{UUID}_front.mp3" in audio_md
    assert "Other card front?" in audio_md and "Other card front?" in plain_md
    # plain file carries no audio uris.
    assert "[audio-front]" not in plain_md
