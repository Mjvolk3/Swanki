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
    FISH_SPEECH_FORBIDDEN_TAGS,
    _normalize_fish_speech_punct,
    append_chunk_pause,
    apply_pronunciation_overrides,
    chunk_text,
    chunk_text_paragraphs,
    clean_markdown_for_tts,
    combine_audio,
    combine_audio_with_section_pauses,
    detect_repeated_phrases,
    expand_acronyms_for_tts,
    extract_acronyms,
    filter_metadata,
    generate_silence,
    restitch_from_chunks,
    split_transcript_by_sections,
    strip_chapter_filename_slug,
    strip_forbidden_fish_tags,
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


def test_append_chunk_pause_fish_speech_no_append():
    # May-14 fix: Fish chunks land at TTS with NO trailing pause tag. Inter-
    # chunk silence comes from chunk_pause_ms in combine_audio_with_section_pauses;
    # emitting a token here caused audible stutter at chunk boundaries (Fish
    # rendered the token first and then the silence played).
    assert append_chunk_pause("Hello.", "fish_speech") == "Hello."


def test_append_chunk_pause_fish_strips_existing_trailing_pause():
    assert append_chunk_pause("Hello. [pause]", "fish_speech") == "Hello."
    assert (
        append_chunk_pause("Hello.\n[short pause]\n[pause]", "fish_speech")
        == "Hello."
    )
    assert (
        append_chunk_pause("Hello. [short pause] [pause] [long pause]", "fish_speech")
        == "Hello."
    )


def test_append_chunk_pause_fish_strips_leading_pause():
    # Defensive: a chunk that starts at a paragraph boundary could have a
    # leading [pause] from add_tts_pauses. Strip those too — same reasoning as
    # trailing: chunk_pause_ms supplies the silence between chunks.
    assert append_chunk_pause("[pause] Hello.", "fish_speech") == "Hello."


def test_append_chunk_pause_fish_preserves_mid_chunk_pause():
    # Mid-chunk pauses signal complex-sentence comprehension or dramatic
    # effect; they must survive untouched.
    text = "Mid [pause] chunk text. End sentence."
    assert append_chunk_pause(text, "fish_speech") == text


def test_append_chunk_pause_elevenlabs():
    assert append_chunk_pause("Hello.") == 'Hello. <break time="1.0s" />'
    assert (
        append_chunk_pause("Hello.", "elevenlabs")
        == 'Hello. <break time="1.0s" />'
    )


def test_append_chunk_pause_idempotent_fish():
    # Stripping is idempotent; second pass on stripped text is a no-op.
    once = append_chunk_pause("Hello. [pause]", "fish_speech")
    twice = append_chunk_pause(once, "fish_speech")
    assert once == twice == "Hello."


def test_append_chunk_pause_idempotent_elevenlabs():
    once = append_chunk_pause("Hello.")
    twice = append_chunk_pause(once)
    assert once == twice


def test_append_chunk_pause_strips_trailing_whitespace():
    assert append_chunk_pause("Hello.   ", "fish_speech") == "Hello."


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


def test_write_chunk_manifest_records_postprocessor(tmp_path):
    # Regression guard: write_chunk_manifest must persist the boundary-fix
    # knobs so a later restitch_from_chunks reproduces the original render.
    post = {
        "section_pause_ms": 5000,
        "chunk_pause_ms": 700,
        "chunk_tail_trim_ms": 250,
        "chunk_crossfade_ms": 50,
        "gain_match_target_dbfs": -25.0,
    }
    path = write_chunk_manifest(
        tmp_path, "lecture", "out.mp3", [], postprocessor=post,
    )
    data = json.loads(path.read_text())
    assert data["postprocessor"] == post


def test_write_chunk_manifest_postprocessor_defaults_to_empty_dict(tmp_path):
    # Older callers that don't pass postprocessor still succeed; the manifest
    # records {} (NOT missing) so restitch's `manifest.get("postprocessor")`
    # always returns a dict.
    path = write_chunk_manifest(tmp_path, "summary", "out.mp3", [])
    data = json.loads(path.read_text())
    assert data["postprocessor"] == {}


def test_restitch_from_chunks_uses_manifest_chunk_pause_ms(tmp_path):
    # Regression guard for the bug fixed in this PR: when the manifest
    # records chunk_pause_ms=700, restitch must insert 700ms silence between
    # chunks (previously it dropped chunk_pause_ms entirely, producing
    # back-to-back chunks with zero gap).
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
            {"index": 1, "section": 0, "text": "b", "file": "chunk0.mp3"},
        ],
        postprocessor={
            "section_pause_ms": 0,
            "chunk_pause_ms": 700,
        },
    )
    out = tmp_path / "restitched.mp3"
    restitch_from_chunks(manifest_path, out)
    audio = AudioSegment.from_mp3(str(out))
    # 1000ms + 700ms gap + 1000ms = ~2700ms; without the fix this would be ~2000ms.
    assert 2500 < len(audio) < 2900, (
        f"chunk_pause_ms=700 not honored: got {len(audio)}ms, expected ~2700ms"
    )


def test_restitch_from_chunks_caller_override_wins_over_manifest(tmp_path):
    # Caller-passed section_pause_ms overrides the manifest value (so a
    # debugging session can tweak without rewriting the manifest).
    chunks_dir = tmp_path / "chunks"
    chunks_dir.mkdir()
    AudioSegment.silent(duration=500).export(str(chunks_dir / "c0.mp3"), format="mp3")
    AudioSegment.silent(duration=500).export(str(chunks_dir / "c1.mp3"), format="mp3")
    manifest_path = write_chunk_manifest(
        chunks_dir,
        "lecture",
        "out.mp3",
        [
            {"index": 0, "section": 0, "text": "a", "file": "c0.mp3"},
            {"index": 1, "section": 1, "text": "b", "file": "c1.mp3"},
        ],
        postprocessor={"section_pause_ms": 5000},
    )
    out = tmp_path / "restitched.mp3"
    restitch_from_chunks(manifest_path, out, section_pause_ms=1000)
    audio = AudioSegment.from_mp3(str(out))
    # 500ms + 1000ms (caller override) + 500ms = ~2000ms; manifest's 5000 ignored.
    assert 1800 < len(audio) < 2200


def test_restitch_from_chunks_uses_per_boundary_silence(tmp_path):
    # Manifest records per-chunk boundary types and a chunk_pause_ms_by_boundary
    # map; restitch must apply the per-boundary silence durations.
    chunks_dir = tmp_path / "chunks"
    chunks_dir.mkdir()
    for name in ("c0.mp3", "c1.mp3", "c2.mp3"):
        AudioSegment.silent(duration=1000).export(str(chunks_dir / name), format="mp3")
    manifest_path = write_chunk_manifest(
        chunks_dir,
        "lecture",
        "out.mp3",
        [
            {"index": 0, "section": 0, "text": "a", "file": "c0.mp3", "boundary": "paragraph"},
            {"index": 1, "section": 0, "text": "b", "file": "c1.mp3", "boundary": "paragraph"},
            {"index": 2, "section": 0, "text": "c", "file": "c2.mp3", "boundary": "sentence"},
        ],
        postprocessor={
            "section_pause_ms": 0,
            "chunk_pause_ms_by_boundary": {"paragraph": 1100, "sentence": 500},
        },
    )
    out = tmp_path / "restitched.mp3"
    restitch_from_chunks(manifest_path, out)
    audio = AudioSegment.from_mp3(str(out))
    # 1000 + 1100 (paragraph gap) + 1000 + 500 (sentence gap) + 1000 = 4600ms
    assert 4500 <= len(audio) <= 4700, (
        f"per-boundary silences not honored on restitch: {len(audio)}ms"
    )


# ---------------------------------------------------------------------------
# _normalize_fish_speech_punct
# ---------------------------------------------------------------------------


def test_normalize_fish_speech_punct_dashes():
    text = "diseases\u2014such as tumors with type 1\u2013associated lesions."
    out = _normalize_fish_speech_punct(text)
    assert out == "diseases, such as tumors with type 1-associated lesions."


def test_normalize_fish_speech_punct_quotes_and_ellipsis():
    text = "the cell\u2019s ability \u201cto detour\u201d\u2026 continues"
    out = _normalize_fish_speech_punct(text)
    assert out == "the cell's ability \"to detour\"... continues"


def test_normalize_fish_speech_punct_passthrough_ascii():
    text = "plain ASCII - no changes needed."
    assert _normalize_fish_speech_punct(text) == text


# ---------------------------------------------------------------------------
# strip_forbidden_fish_tags (Theme 9)
# ---------------------------------------------------------------------------


def test_strip_forbidden_fish_tags_removes_sigh():
    out = strip_forbidden_fish_tags("hello [sigh] world")
    assert out == "hello world"


def test_strip_forbidden_fish_tags_preserves_allowed():
    text = "First. [pause] Second. [short pause] Third. [emphasis] Done."
    assert strip_forbidden_fish_tags(text) == text


def test_strip_forbidden_fish_tags_idempotent():
    text = "hello [inhale] [sigh] world"
    once = strip_forbidden_fish_tags(text)
    twice = strip_forbidden_fish_tags(once)
    assert once == twice == "hello world"


def test_strip_forbidden_fish_tags_case_insensitive():
    assert strip_forbidden_fish_tags("a [SIGH] b [Inhale] c") == "a b c"


def test_strip_forbidden_fish_tags_constant_complete():
    # Sanity: all forbidden tags surface in the regex by being stripped.
    text = " ".join(f"[{t}]" for t in FISH_SPEECH_FORBIDDEN_TAGS)
    out = strip_forbidden_fish_tags(text)
    assert out.strip() == ""


# ---------------------------------------------------------------------------
# expand_acronyms_for_tts (Theme 6)
# ---------------------------------------------------------------------------


def test_expand_acronyms_for_tts_letter_by_letter():
    assert expand_acronyms_for_tts("the SAR system") == "the S-A-R system"


def test_expand_acronyms_for_tts_skips_allowlist():
    assert (
        expand_acronyms_for_tts("USA and SAR", allowlist={"USA"})
        == "USA and S-A-R"
    )


def test_expand_acronyms_for_tts_skips_camelcase_lower_prefix():
    # myACRONYM is preceded by a lowercase letter -> not standalone.
    assert (
        expand_acronyms_for_tts("myACRONYM stays put") == "myACRONYM stays put"
    )


def test_expand_acronyms_for_tts_skips_camelcase_lower_suffix():
    # ABCfoo is followed by lowercase -> not standalone.
    assert expand_acronyms_for_tts("ABCfoo bar") == "ABCfoo bar"


def test_expand_acronyms_for_tts_no_change_for_lowercase():
    assert expand_acronyms_for_tts("nothing to do here") == "nothing to do here"


def test_expand_acronyms_for_tts_skips_single_letter():
    assert expand_acronyms_for_tts("the X factor and A team") == "the X factor and A team"


# ---------------------------------------------------------------------------
# apply_pronunciation_overrides (Theme 7)
# ---------------------------------------------------------------------------


def test_apply_pronunciation_overrides_whole_word():
    out = apply_pronunciation_overrides(
        "Decisively important", {"Decisively": "decisively,"}
    )
    assert out == "decisively, important"


def test_apply_pronunciation_overrides_does_not_match_substring():
    # "Indecisively" contains "Decisively" as a suffix; whole-word boundary
    # should leave it alone.
    out = apply_pronunciation_overrides(
        "Indecisively yours", {"Decisively": "decisively,"}
    )
    assert out == "Indecisively yours"


def test_apply_pronunciation_overrides_empty_dict_noop():
    text = "no overrides here"
    assert apply_pronunciation_overrides(text, {}) == text


# ---------------------------------------------------------------------------
# strip_chapter_filename_slug (Theme 8 safety net)
# ---------------------------------------------------------------------------


def test_strip_chapter_filename_slug_basic():
    text = "now we present hammingArtDoingScience2020_03_history-of-computers-hardware here"
    out = strip_chapter_filename_slug(text)
    assert out == "now we present Chapter 3: history of computers hardware here"


def test_strip_chapter_filename_slug_no_match_no_change():
    text = "ordinary text without any chapter slug"
    assert strip_chapter_filename_slug(text) == text


def test_strip_chapter_filename_slug_drops_leading_zero():
    out = strip_chapter_filename_slug("paper2024_07_some-slug")
    assert "Chapter 7" in out
    assert "07" not in out


# ---------------------------------------------------------------------------
# detect_repeated_phrases (Theme 5)
# ---------------------------------------------------------------------------


def test_detect_repeated_phrases_basic():
    transcript = (
        "his last observation he said. " * 4
        + "different prose with no repetition follows."
    )
    repeats = detect_repeated_phrases(transcript, n=5, threshold=3)
    assert any("his last observation he said" in r for r in repeats)


def test_detect_repeated_phrases_filters_stopword_chatter():
    # "the way that you can" repeated 5 times -> insufficient content words.
    transcript = "the way that you can " * 5 + "but real prose contains many words."
    repeats = detect_repeated_phrases(
        transcript, n=5, threshold=3, min_distinct_content_words=3
    )
    assert all("the way that you can" not in r for r in repeats)


def test_detect_repeated_phrases_no_repetition_returns_empty():
    transcript = "one short transcript with no repeats whatsoever today."
    assert detect_repeated_phrases(transcript) == []


def test_detect_repeated_phrases_below_threshold_not_flagged():
    transcript = "a meaningful unique five-word phrase. " * 2
    assert detect_repeated_phrases(transcript, n=5, threshold=3) == []


# ---------------------------------------------------------------------------
# chunk_text_paragraphs - tighter max_chars (Theme 4)
# ---------------------------------------------------------------------------


def test_chunk_text_paragraphs_respects_700_char_cap():
    paragraphs = "\n\n".join(
        f"Paragraph {i}. " + ("filler. " * 30)
        for i in range(5)
    )
    chunks = chunk_text_paragraphs(paragraphs, max_chars=700)
    assert all(len(text) <= 700 for text, _b in chunks), [len(t) for t, _ in chunks]


def test_chunk_text_paragraphs_oversize_paragraph_falls_back_to_sentences():
    big = " ".join(f"Sentence {i} ends here." for i in range(60))
    chunks = chunk_text_paragraphs(big, max_chars=200)
    # Single oversize paragraph triggers sentence-fallback; chunks must stay
    # under the cap.
    assert all(len(text) <= 200 for text, _b in chunks)
    assert len(chunks) > 1
    # All chunks past the first land at sentence boundaries (the oversize
    # paragraph was subdivided), so their preceding-gap boundary type is
    # "sentence". The first chunk's boundary defaults to "paragraph".
    boundaries = [b for _, b in chunks]
    assert boundaries[0] == "paragraph"
    assert all(b == "sentence" for b in boundaries[1:])


def test_chunk_text_paragraphs_packs_under_budget():
    text = "Para one is short.\n\nPara two is also short."
    chunks = chunk_text_paragraphs(text, max_chars=200)
    # Both paragraphs fit in one chunk; that chunk's preceding-gap boundary
    # is "paragraph" (its first item starts a fresh paragraph).
    assert chunks == [("Para one is short.\n\nPara two is also short.", "paragraph")]


def test_chunk_text_paragraphs_two_paragraphs_split_to_two_chunks():
    # When two paragraphs are each near the budget, they land in separate
    # chunks and the second chunk's boundary is "paragraph".
    para_a = "Sentence A. " + "filler word. " * 10
    para_b = "Sentence B. " + "filler word. " * 10
    chunks = chunk_text_paragraphs(f"{para_a}\n\n{para_b}", max_chars=180)
    boundaries = [b for _, b in chunks]
    assert len(chunks) >= 2
    assert boundaries[0] == "paragraph"
    # Whichever subsequent chunk starts at the second paragraph's first item
    # should carry "paragraph"; sub-paragraph splits inside one paragraph
    # carry "sentence". At minimum one of the later chunks should be
    # "paragraph" (the start of paragraph B).
    assert "paragraph" in boundaries[1:]


# ---------------------------------------------------------------------------
# combine_audio_with_section_pauses - previously-untested params
# ---------------------------------------------------------------------------


def test_combine_audio_with_section_pauses_chunk_pause_inserts_silence(tmp_path):
    # Two 1-second sine-wave-ish chunks, 500ms inter-chunk silence -> 2.5s.
    a = tmp_path / "a.mp3"
    b = tmp_path / "b.mp3"
    AudioSegment.silent(duration=1000).export(str(a), format="mp3")
    AudioSegment.silent(duration=1000).export(str(b), format="mp3")
    out = tmp_path / "out.mp3"
    combine_audio_with_section_pauses(
        [[a, b]], out, section_pause_ms=0, chunk_pause_ms=500,
    )
    combined = AudioSegment.from_mp3(str(out))
    assert 2400 <= len(combined) <= 2600


def test_combine_audio_with_section_pauses_per_boundary_silence(tmp_path):
    # Three chunks: gap before chunk[1] is "paragraph" (1100ms), gap before
    # chunk[2] is "sentence" (500ms). Total = 1000 + 1100 + 1000 + 500 + 1000
    # = 4600ms. With uniform chunk_pause_ms it would be 1000+x+1000+x+1000.
    a = tmp_path / "a.mp3"; b = tmp_path / "b.mp3"; c = tmp_path / "c.mp3"
    for p in (a, b, c):
        AudioSegment.silent(duration=1000).export(str(p), format="mp3")
    out = tmp_path / "out.mp3"
    combine_audio_with_section_pauses(
        [[a, b, c]],
        out,
        section_pause_ms=0,
        # chunk_pause_ms acts as fallback only; per-boundary map should win.
        chunk_pause_ms=999999,
        chunk_boundaries=[["paragraph", "paragraph", "sentence"]],
        chunk_pause_ms_by_boundary={"paragraph": 1100, "sentence": 500},
    )
    combined = AudioSegment.from_mp3(str(out))
    # 1000 + 1100 + 1000 + 500 + 1000 = 4600ms (allow ~100ms tolerance)
    assert 4500 <= len(combined) <= 4700, (
        f"per-boundary silences not honored: got {len(combined)}ms, expected ~4600ms"
    )


def test_combine_audio_with_section_pauses_falls_back_to_chunk_pause_ms_without_map(tmp_path):
    # When chunk_pause_ms_by_boundary is absent, the legacy uniform
    # chunk_pause_ms applies to every gap (no regression for existing callers).
    a = tmp_path / "a.mp3"; b = tmp_path / "b.mp3"
    for p in (a, b):
        AudioSegment.silent(duration=1000).export(str(p), format="mp3")
    out = tmp_path / "out.mp3"
    combine_audio_with_section_pauses(
        [[a, b]], out, section_pause_ms=0, chunk_pause_ms=700,
        # boundaries provided but no map -> uniform behavior preserved
        chunk_boundaries=[["paragraph", "sentence"]],
    )
    combined = AudioSegment.from_mp3(str(out))
    # 1000 + 700 + 1000 = 2700ms
    assert 2600 <= len(combined) <= 2800


def test_combine_audio_with_section_pauses_missing_boundary_key_falls_back(tmp_path):
    # Per-boundary map missing a key -> that gap falls back to chunk_pause_ms.
    a = tmp_path / "a.mp3"; b = tmp_path / "b.mp3"
    for p in (a, b):
        AudioSegment.silent(duration=1000).export(str(p), format="mp3")
    out = tmp_path / "out.mp3"
    combine_audio_with_section_pauses(
        [[a, b]],
        out,
        section_pause_ms=0,
        chunk_pause_ms=700,
        chunk_boundaries=[["paragraph", "unknown_type"]],  # not in map
        chunk_pause_ms_by_boundary={"paragraph": 1100},  # missing "unknown_type"
    )
    combined = AudioSegment.from_mp3(str(out))
    # Gap falls back to chunk_pause_ms=700: 1000 + 700 + 1000 = 2700ms
    assert 2600 <= len(combined) <= 2800


def test_combine_audio_with_section_pauses_zero_chunk_pause_no_extra_silence(tmp_path):
    a = tmp_path / "a.mp3"
    b = tmp_path / "b.mp3"
    AudioSegment.silent(duration=1000).export(str(a), format="mp3")
    AudioSegment.silent(duration=1000).export(str(b), format="mp3")
    out = tmp_path / "out.mp3"
    combine_audio_with_section_pauses(
        [[a, b]], out, section_pause_ms=0, chunk_pause_ms=0,
    )
    combined = AudioSegment.from_mp3(str(out))
    # No inter-chunk silence requested -> ~2 seconds.
    assert 1900 <= len(combined) <= 2100


def test_combine_audio_with_section_pauses_gain_match_normalizes(tmp_path):
    # Two chunks at very different sustained levels; gain_match flattens the
    # mean dBFS to the target.
    from pydub.generators import Sine

    loud = Sine(440).to_audio_segment(duration=1000)
    quiet = loud - 12  # 12 dB quieter
    a = tmp_path / "a.mp3"
    b = tmp_path / "b.mp3"
    loud.export(str(a), format="mp3")
    quiet.export(str(b), format="mp3")
    out_with = tmp_path / "with.mp3"
    out_without = tmp_path / "without.mp3"
    combine_audio_with_section_pauses(
        [[a, b]], out_with, section_pause_ms=0, gain_match_target_dbfs=-25.0,
    )
    combine_audio_with_section_pauses(
        [[a, b]], out_without, section_pause_ms=0,
    )
    combined_with = AudioSegment.from_mp3(str(out_with))
    combined_without = AudioSegment.from_mp3(str(out_without))
    # With gain match, the combined dBFS should be closer to -25 than without.
    assert abs(combined_with.dBFS - (-25.0)) < abs(combined_without.dBFS - (-25.0))


def test_combine_audio_with_section_pauses_chunk_tail_trim_zero_no_op(tmp_path):
    # chunk_tail_trim_ms=0 must NOT trim anything (regression guard).
    a = tmp_path / "a.mp3"
    b = tmp_path / "b.mp3"
    AudioSegment.silent(duration=1000).export(str(a), format="mp3")
    AudioSegment.silent(duration=1000).export(str(b), format="mp3")
    out = tmp_path / "out.mp3"
    combine_audio_with_section_pauses(
        [[a, b]], out, section_pause_ms=0, chunk_tail_trim_ms=0,
    )
    combined = AudioSegment.from_mp3(str(out))
    assert 1900 <= len(combined) <= 2100
