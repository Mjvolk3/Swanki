"""
tests/test_audio_common.py
[[tests.test_audio_common]]
https://github.com/Mjvolk3/Swanki/tree/main/tests/test_audio_common.py
Test file: tests/test_audio_common.py

Tests for pure functions in swanki.audio._common.
"""

import json

from pydub import AudioSegment

from swanki.audio._common import (
    append_chunk_pause,
    chunk_text,
    clean_markdown_for_tts,
    combine_audio,
    combine_audio_with_section_pauses,
    extract_acronyms,
    filter_metadata,
    generate_silence,
    restitch_from_chunks,
    split_transcript_by_sections,
    validate_audio_file,
    write_chunk_manifest,
)

# ---------------------------------------------------------------------------
# chunk_text
# ---------------------------------------------------------------------------


def test_chunk_text_single():
    text = "Short paragraph."
    chunks = chunk_text(text)
    assert chunks == ["Short paragraph."]


def test_chunk_text_splits_paragraphs():
    p1 = "A" * 2000
    p2 = "B" * 2000
    text = f"{p1}\n\n{p2}"
    chunks = chunk_text(text, max_chars=3000)
    assert len(chunks) == 2
    assert chunks[0] == p1
    assert chunks[1] == p2


def test_chunk_text_splits_sentences():
    sentences = ". ".join([f"Sentence {i}" for i in range(100)])
    chunks = chunk_text(sentences, max_chars=200)
    assert len(chunks) > 1
    for c in chunks:
        assert len(c) <= 200


def test_chunk_text_respects_max():
    text = "\n\n".join(["Hello world. " * 50 for _ in range(10)])
    chunks = chunk_text(text, max_chars=500)
    for c in chunks:
        assert len(c) <= 500


# ---------------------------------------------------------------------------
# clean_markdown_for_tts
# ---------------------------------------------------------------------------


def test_clean_markdown_headers():
    assert clean_markdown_for_tts("## Introduction") == "Introduction"
    assert clean_markdown_for_tts("### Sub-section") == "Sub-section"


def test_clean_markdown_bold_italic():
    assert (
        clean_markdown_for_tts("This is **bold** and *italic*")
        == "This is bold and italic"
    )


def test_clean_markdown_links():
    assert clean_markdown_for_tts("[click here](https://example.com)") == "click here"


def test_clean_markdown_code():
    assert clean_markdown_for_tts("Use `print()` to output") == "Use print() to output"


# ---------------------------------------------------------------------------
# filter_metadata
# ---------------------------------------------------------------------------


def test_filter_metadata_references():
    content = "Some text.\n\n## References\n\n1. Smith, A. Paper. 2020.\n2. Jones, B. Paper. 2021."
    filtered = filter_metadata(content)
    assert "Some text." in filtered
    assert "Smith" not in filtered


def test_filter_metadata_emails():
    content = "Author info\ncontact@university.edu\nMore content here."
    filtered = filter_metadata(content)
    assert "contact@university.edu" not in filtered
    assert "More content here." in filtered


def test_filter_metadata_affiliations():
    content = (
        "Introduction\nDepartment of Biology\nUniversity of Oxford\nThe study shows..."
    )
    filtered = filter_metadata(content)
    assert "Department of Biology" not in filtered
    assert "University of Oxford" not in filtered
    assert "The study shows..." in filtered


def test_filter_metadata_preserves_content():
    content = "## Introduction\n\nThis paper studies X.\n\n## Methods\n\nWe used Y."
    filtered = filter_metadata(content)
    assert "This paper studies X." in filtered
    assert "We used Y." in filtered


# ---------------------------------------------------------------------------
# combine_audio
# ---------------------------------------------------------------------------


def test_combine_audio(tmp_path):
    f1 = tmp_path / "a.mp3"
    f2 = tmp_path / "b.mp3"
    AudioSegment.silent(duration=1000).export(str(f1), format="mp3")
    AudioSegment.silent(duration=1000).export(str(f2), format="mp3")

    out = tmp_path / "combined.mp3"
    combine_audio([f1, f2], out)

    assert out.exists()
    combined = AudioSegment.from_mp3(str(out))
    # Two 1-second clips concatenated (default crossfade=0) -> ~2000ms
    assert len(combined) > 1800


def test_combine_audio_empty(tmp_path):
    out = tmp_path / "empty.mp3"
    combine_audio([], out)
    assert not out.exists()


def test_combine_audio_zero_crossfade_default(tmp_path):
    """Default crossfade is 0: output is direct concatenation, no overlap."""
    f1 = tmp_path / "a.mp3"
    f2 = tmp_path / "b.mp3"
    AudioSegment.silent(duration=1000).export(str(f1), format="mp3")
    AudioSegment.silent(duration=1000).export(str(f2), format="mp3")

    out = tmp_path / "combined.mp3"
    combine_audio([f1, f2], out)

    combined = AudioSegment.from_mp3(str(out))
    # ~2000ms total (no crossfade overlap), allow MP3 frame boundary slack
    assert 1900 <= len(combined) <= 2100


# ---------------------------------------------------------------------------
# validate_audio_file
# ---------------------------------------------------------------------------


def test_validate_audio_file_missing(tmp_path):
    assert validate_audio_file(tmp_path / "nonexistent.mp3") is False


def test_validate_audio_file_too_small(tmp_path):
    tiny = tmp_path / "tiny.mp3"
    tiny.write_bytes(b"x" * 100)
    assert validate_audio_file(tiny) is False


# ---------------------------------------------------------------------------
# generate_silence
# ---------------------------------------------------------------------------


def test_generate_silence(tmp_path):
    out = tmp_path / "silence.mp3"
    result = generate_silence(2000, out)
    assert result == out
    assert out.exists()
    audio = AudioSegment.from_mp3(str(out))
    assert abs(len(audio) - 2000) < 100  # ~2s within tolerance


def test_generate_silence_short(tmp_path):
    out = tmp_path / "short.mp3"
    generate_silence(500, out)
    audio = AudioSegment.from_mp3(str(out))
    assert abs(len(audio) - 500) < 100


# ---------------------------------------------------------------------------
# split_transcript_by_sections
# ---------------------------------------------------------------------------


def test_split_transcript_by_sections_basic():
    transcript = "Section one.\n\n---SECTION_BREAK---\n\nSection two."
    sections = split_transcript_by_sections(transcript)
    assert sections == ["Section one.", "Section two."]


def test_split_transcript_by_sections_empty_between():
    transcript = "A\n---SECTION_BREAK---\n---SECTION_BREAK---\nB"
    sections = split_transcript_by_sections(transcript)
    assert sections == ["A", "B"]


def test_split_transcript_by_sections_no_marker():
    transcript = "No breaks here, just text."
    sections = split_transcript_by_sections(transcript)
    assert sections == ["No breaks here, just text."]


def test_split_transcript_by_sections_custom_marker():
    transcript = "First<<SEP>>Second<<SEP>>Third"
    sections = split_transcript_by_sections(transcript, marker="<<SEP>>")
    assert sections == ["First", "Second", "Third"]


# ---------------------------------------------------------------------------
# combine_audio_with_section_pauses
# ---------------------------------------------------------------------------


def test_combine_audio_with_section_pauses_basic(tmp_path):
    # Create two sections, each with one chunk
    f1 = tmp_path / "s1_c0.mp3"
    f2 = tmp_path / "s2_c0.mp3"
    AudioSegment.silent(duration=1000).export(str(f1), format="mp3")
    AudioSegment.silent(duration=1000).export(str(f2), format="mp3")

    out = tmp_path / "combined.mp3"
    combine_audio_with_section_pauses([[f1], [f2]], out, section_pause_ms=2000)

    assert out.exists()
    audio = AudioSegment.from_mp3(str(out))
    # 1s + 2s pause + 1s = ~4s
    assert len(audio) > 3500


def test_combine_audio_with_section_pauses_bookends(tmp_path):
    chunk = tmp_path / "chunk.mp3"
    start = tmp_path / "start.mp3"
    end = tmp_path / "end.mp3"
    AudioSegment.silent(duration=1000).export(str(chunk), format="mp3")
    AudioSegment.silent(duration=500).export(str(start), format="mp3")
    AudioSegment.silent(duration=500).export(str(end), format="mp3")

    out = tmp_path / "combined.mp3"
    combine_audio_with_section_pauses(
        [[chunk]],
        out,
        bookend_start=start,
        bookend_end=end,
        bookend_pause_ms=500,
    )

    assert out.exists()
    audio = AudioSegment.from_mp3(str(out))
    # 500ms start + 500ms pause + 1000ms chunk + 500ms pause + 500ms end = ~3000ms
    assert len(audio) > 2500


def test_combine_audio_with_section_pauses_empty(tmp_path):
    out = tmp_path / "empty.mp3"
    combine_audio_with_section_pauses([], out)
    assert not out.exists()


# ---------------------------------------------------------------------------
# extract_acronyms
# ---------------------------------------------------------------------------


def test_extract_acronyms_parenthetical():
    text = (
        "We used the FSEOF (flux scanning based on enforced objective function) method."
    )
    result = extract_acronyms(text)
    assert "FSEOF" in result
    assert "flux scanning" in result["FSEOF"].lower()


def test_extract_acronyms_reverse_pattern():
    text = "The flux balance analysis (FBA) is commonly used."
    result = extract_acronyms(text)
    assert "FBA" in result


def test_extract_acronyms_multiple():
    text = (
        "We applied CRISPR (clustered regularly interspaced short palindromic repeats) "
        "and genome-scale metabolic models (GEMs) to the problem."
    )
    result = extract_acronyms(text)
    assert "CRISPR" in result
    assert "GEMs" not in result  # lowercase 's' makes it <2 uppercase
    assert "GEM" not in result  # only 3-char acronym inside parens is "GEMs"


def test_extract_acronyms_empty():
    assert extract_acronyms("No acronyms here.") == {}


def test_extract_acronyms_skips_all_caps_expansion():
    text = "The ABC (DEF) transporter."
    result = extract_acronyms(text)
    # "DEF" is all-caps so should be skipped as not a real expansion
    assert "ABC" not in result


# ---------------------------------------------------------------------------
# combine_audio_with_section_pauses — zero crossfade default
# ---------------------------------------------------------------------------


def test_combine_sections_zero_crossfade_default(tmp_path):
    """Default chunk_crossfade_ms=0: chunks within a section are concatenated."""
    c1 = tmp_path / "c1.mp3"
    c2 = tmp_path / "c2.mp3"
    AudioSegment.silent(duration=1000).export(str(c1), format="mp3")
    AudioSegment.silent(duration=1000).export(str(c2), format="mp3")

    out = tmp_path / "out.mp3"
    combine_audio_with_section_pauses([[c1, c2]], out, section_pause_ms=0)

    combined = AudioSegment.from_mp3(str(out))
    # Two concatenated chunks, no overlap, no section pause -> ~2000ms
    assert 1900 <= len(combined) <= 2100


# ---------------------------------------------------------------------------
# append_chunk_pause
# ---------------------------------------------------------------------------


def test_append_chunk_pause_fish_speech():
    assert append_chunk_pause("Hello.", "fish_speech") == "Hello. [long pause]"


def test_append_chunk_pause_elevenlabs():
    assert append_chunk_pause("Hello.") == 'Hello. <break time="1.0s" />'
    assert (
        append_chunk_pause("Hello.", "elevenlabs")
        == 'Hello. <break time="1.0s" />'
    )


def test_append_chunk_pause_idempotent_fish():
    once = append_chunk_pause("Hello.", "fish_speech")
    twice = append_chunk_pause(once, "fish_speech")
    assert once == twice


def test_append_chunk_pause_idempotent_elevenlabs():
    once = append_chunk_pause("Hello.")
    twice = append_chunk_pause(once)
    assert once == twice


def test_append_chunk_pause_strips_trailing_whitespace():
    assert append_chunk_pause("Hello.   ", "fish_speech") == "Hello. [long pause]"


# ---------------------------------------------------------------------------
# write_chunk_manifest
# ---------------------------------------------------------------------------


def test_write_chunk_manifest_basic(tmp_path):
    chunks = [
        {"index": 0, "section": 0, "text": "first", "file": "chunk0.mp3"},
        {"index": 1, "section": 1, "text": "second", "file": "chunk1.mp3"},
    ]
    path = write_chunk_manifest(
        tmp_path,
        "lecture",
        "lecture-audio.mp3",
        chunks,
        bookend_start="start.mp3",
        bookend_end="end.mp3",
    )
    assert path == tmp_path / "chunk_manifest.json"
    data = json.loads(path.read_text())
    assert data["audio_type"] == "lecture"
    assert data["output_file"] == "lecture-audio.mp3"
    assert data["bookend_start"] == "start.mp3"
    assert data["bookend_end"] == "end.mp3"
    assert data["chunks"] == chunks


def test_write_chunk_manifest_no_bookends(tmp_path):
    path = write_chunk_manifest(tmp_path, "summary", "out.mp3", [])
    data = json.loads(path.read_text())
    assert data["bookend_start"] is None
    assert data["bookend_end"] is None
    assert data["chunks"] == []


# ---------------------------------------------------------------------------
# restitch_from_chunks
# ---------------------------------------------------------------------------


def test_restitch_from_chunks_basic(tmp_path):
    chunks_dir = tmp_path / "chunks"
    chunks_dir.mkdir()
    c0 = chunks_dir / "chunk0.mp3"
    c1 = chunks_dir / "chunk1.mp3"
    AudioSegment.silent(duration=1000).export(str(c0), format="mp3")
    AudioSegment.silent(duration=1000).export(str(c1), format="mp3")

    manifest_path = write_chunk_manifest(
        chunks_dir,
        "lecture",
        "out.mp3",
        [
            {"index": 0, "section": 0, "text": "a", "file": "chunk0.mp3"},
            {"index": 1, "section": 1, "text": "b", "file": "chunk1.mp3"},
        ],
    )

    out = tmp_path / "restitched.mp3"
    restitch_from_chunks(manifest_path, out, section_pause_ms=2000)

    assert out.exists()
    audio = AudioSegment.from_mp3(str(out))
    # 1s + 2s pause + 1s = ~4s
    assert len(audio) > 3500


def test_restitch_from_chunks_with_bookends(tmp_path):
    chunks_dir = tmp_path / "chunks"
    chunks_dir.mkdir()
    chunk = chunks_dir / "chunk0.mp3"
    start = chunks_dir / "start.mp3"
    end = chunks_dir / "end.mp3"
    AudioSegment.silent(duration=1000).export(str(chunk), format="mp3")
    AudioSegment.silent(duration=500).export(str(start), format="mp3")
    AudioSegment.silent(duration=500).export(str(end), format="mp3")

    manifest_path = write_chunk_manifest(
        chunks_dir,
        "lecture",
        "out.mp3",
        [{"index": 0, "section": 0, "text": "a", "file": "chunk0.mp3"}],
        bookend_start="start.mp3",
        bookend_end="end.mp3",
    )

    out = tmp_path / "restitched.mp3"
    restitch_from_chunks(manifest_path, out, bookend_pause_ms=500)

    assert out.exists()
    audio = AudioSegment.from_mp3(str(out))
    # 500ms start + 500ms pause + 1000ms chunk + 500ms pause + 500ms end = ~3000ms
    assert len(audio) > 2500


def test_restitch_from_chunks_missing_file_fails(tmp_path):
    chunks_dir = tmp_path / "chunks"
    chunks_dir.mkdir()
    manifest_path = write_chunk_manifest(
        chunks_dir,
        "lecture",
        "out.mp3",
        [{"index": 0, "section": 0, "text": "a", "file": "missing.mp3"}],
    )
    out = tmp_path / "restitched.mp3"
    try:
        restitch_from_chunks(manifest_path, out)
    except AssertionError as e:
        assert "Chunk file missing" in str(e)
    else:
        raise AssertionError("Expected AssertionError for missing chunk file")
