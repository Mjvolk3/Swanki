"""
tests/test_audio_common.py
[[tests.test_audio_common]]
https://github.com/Mjvolk3/Swanki/tree/main/tests/test_audio_common.py
Test file: tests/test_audio_common.py

Tests for pure functions in swanki.audio._common.
"""

import json
from pathlib import Path

from pydub import AudioSegment

from swanki.audio._common import (
    FISH_SPEECH_FORBIDDEN_TAGS,
    SECTION_BREAK_MARKER,
    _balanced_sentence_groups,
    _normalize_fish_speech_punct,
    append_chunk_pause,
    apply_pronunciation_overrides,
    build_bookend_text,
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
    preprocess_for_tts,
    restitch_from_chunks,
    split_transcript_by_sections,
    strip_chapter_filename_slug,
    strip_forbidden_fish_tags,
    validate_audio_file,
    verbalize_bit_strings,
    verbalize_large_numbers,
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


def _silence(path: Path, ms: int) -> None:
    AudioSegment.silent(duration=ms).export(str(path), format="mp3")


def test_combine_audio_with_section_pauses_bookends(tmp_path):
    chunk, start, end = (tmp_path / n for n in ("chunk.mp3", "start.mp3", "end.mp3"))
    _silence(chunk, 1000)
    _silence(start, 500)
    _silence(end, 500)

    out = tmp_path / "combined.mp3"
    combine_audio_with_section_pauses(
        [[chunk]],
        out,
        bookend_start=start,
        bookend_end=end,
        bookend_start_pause_ms=300,
        bookend_end_pause_ms=2000,
        bookend_trailing_pause_ms=1500,
    )

    assert out.exists()
    audio = AudioSegment.from_mp3(str(out))
    # 500 start + 300 + 1000 chunk + 2000 + 500 end + 1500 trailing = ~5800ms
    assert len(audio) > 5500


def test_combine_audio_bookend_pauses_are_asymmetric(tmp_path):
    """A larger end pause + trailing silence makes the same content longer
    than a symmetric-small-pause assembly."""
    chunk, start, end = (tmp_path / n for n in ("c.mp3", "s.mp3", "e.mp3"))
    for p in (chunk, start, end):
        _silence(p, 500)

    small = tmp_path / "small.mp3"
    big = tmp_path / "big.mp3"
    combine_audio_with_section_pauses(
        [[chunk]],
        small,
        bookend_start=start,
        bookend_end=end,
        bookend_start_pause_ms=300,
        bookend_end_pause_ms=300,
        bookend_trailing_pause_ms=0,
    )
    combine_audio_with_section_pauses(
        [[chunk]],
        big,
        bookend_start=start,
        bookend_end=end,
        bookend_start_pause_ms=300,
        bookend_end_pause_ms=2000,
        bookend_trailing_pause_ms=1500,
    )
    # big has 1700 extra end-pause + 1500 trailing = ~3200ms more.
    assert (
        len(AudioSegment.from_mp3(str(big))) - len(AudioSegment.from_mp3(str(small)))
        > 3000
    )


def test_combine_audio_trailing_pause_only_with_end_bookend(tmp_path):
    """No end bookend -> the trailing pause is not added."""
    chunk, start = (tmp_path / n for n in ("c.mp3", "s.mp3"))
    _silence(chunk, 1000)
    _silence(start, 500)
    out = tmp_path / "o.mp3"
    combine_audio_with_section_pauses(
        [[chunk]],
        out,
        section_pause_ms=0,
        bookend_start=start,
        bookend_end=None,
        bookend_start_pause_ms=300,
        bookend_end_pause_ms=2000,
        bookend_trailing_pause_ms=1500,
    )
    audio = AudioSegment.from_mp3(str(out))
    # 500 start + 300 start_pause + 1000 chunk = ~1800ms; NO 2000 end / 1500
    # trailing (no end bookend). section_pause_ms=0 isolates the bookend math.
    assert len(audio) < 2200


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
# verbalize_bit_strings
# ---------------------------------------------------------------------------


def test_verbalize_bit_strings_basic():
    assert verbalize_bit_strings("110") == "one-one-zero"
    assert verbalize_bit_strings("11") == "one-one"
    assert verbalize_bit_strings("0110") == "zero-one-one-zero"
    assert verbalize_bit_strings("0011") == "zero-zero-one-one"


def test_verbalize_bit_strings_single_digit_untouched():
    # Bare 0/1 read fine as words and appear constantly in prose.
    assert verbalize_bit_strings("I saw 0 errors and 1 success") == (
        "I saw 0 errors and 1 success"
    )


def test_verbalize_bit_strings_ch10_codewords_with_punctuation():
    # The real Hamming ch10 case: codewords abutting prose commas / periods
    # must still verbalize (the boundary tests reject only number-continuation
    # punctuation, not sentence punctuation).
    text = "Encode them as 0, 00, 01, and 11. If you receive 0011, decode it."
    expected = (
        "Encode them as 0, zero-zero, zero-one, and one-one. "
        "If you receive zero-zero-one-one, decode it."
    )
    assert verbalize_bit_strings(text) == expected


def test_verbalize_bit_strings_idempotent():
    once = verbalize_bit_strings("the codeword 1011010 has parity 11")
    twice = verbalize_bit_strings(once)
    assert once == twice
    assert "one-zero-one-one-zero-one-zero" in once
    assert "one-one" in once


def test_verbalize_bit_strings_protects_numbers_and_identifiers():
    # Decimals, thousands-commas, years, identifiers, paths, and times must
    # pass through unchanged.
    for token in [
        "1.5",
        "0.01",
        "1,000",
        "10,000",
        "2020",
        "2011",
        "v01",
        "chunk0",
        "chunk01",
        "10:01",
        "a/01",
    ]:
        assert verbalize_bit_strings(token) == token, token


def test_verbalize_bit_strings_respects_max_len():
    long_run = "1" * 33
    # Default cap 32 leaves a 33-bit run alone.
    assert verbalize_bit_strings(long_run) == long_run
    # A custom cap below the run length also leaves it alone...
    assert verbalize_bit_strings("10101", max_len=4) == "10101"
    # ...and at/above it expands.
    assert verbalize_bit_strings("10101", max_len=5) == "one-zero-one-zero-one"


def test_verbalize_bit_strings_section_break_marker_survives():
    assert verbalize_bit_strings(SECTION_BREAK_MARKER) == SECTION_BREAK_MARKER


def test_verbalize_bit_strings_mixed_sentence():
    text = "A Hamming distance of 11 between 0110 and 1001 looks large."
    assert verbalize_bit_strings(text) == (
        "A Hamming distance of one-one between zero-one-one-zero and "
        "one-zero-zero-one looks large."
    )


def test_verbalize_bit_strings_empty():
    assert verbalize_bit_strings("") == ""
    assert verbalize_bit_strings("no binary here at all") == ("no binary here at all")


# ---------------------------------------------------------------------------
# preprocess_for_tts
# ---------------------------------------------------------------------------


_FISH = {"provider": "fish_speech", "preprocessor": {}}


def test_preprocess_for_tts_add_pauses_injects_tags():
    text = "First paragraph here.\n\nSecond paragraph here."
    out = preprocess_for_tts(text, _FISH, add_pauses=True)
    assert "[pause]" in out  # add_tts_pauses ran on the blank line


def test_preprocess_for_tts_no_pauses_matches_card_behavior():
    text = "First paragraph here.\n\nSecond paragraph here."
    out = preprocess_for_tts(text, _FISH, add_pauses=False, clean_markdown=False)
    assert "[pause]" not in out  # pause step skipped (card path)


def test_preprocess_for_tts_bit_strings_opt_in():
    # Bit-string verbalize is OPT-IN (default off): a 0/1-only token survives
    # untouched so ordinary decimals are not mangled. Uses a sub-100 codeword so
    # the default-on large-number scrubber does not confound the assertion.
    out = preprocess_for_tts("code 11 here", _FISH, add_pauses=False)
    assert "11" in out and "one-one" not in out
    # ...and the per-paper opt-in (verbalize_bit_strings: true) re-enables it.
    fish_on = {
        "provider": "fish_speech",
        "preprocessor": {"verbalize_bit_strings": True},
    }
    out_on = preprocess_for_tts("code 11 here", fish_on, add_pauses=False)
    assert "one-one" in out_on and "11" not in out_on


def test_preprocess_for_tts_bit_strings_win_over_large_numbers():
    # Order matters for a dense-codeword paper: verbalize_bit_strings runs FIRST
    # and leaves no digits, so the default-on cardinal scrubber cannot re-read a
    # codeword as "one hundred ten".
    cfg = {"provider": "fish_speech", "preprocessor": {"verbalize_bit_strings": True}}
    out = preprocess_for_tts("code 110 here", cfg, add_pauses=False)
    assert "one-one-zero" in out
    assert "one hundred ten" not in out


def test_preprocess_for_tts_spells_large_numbers_by_default():
    out = preprocess_for_tts("measured 851 progeny", _FISH, add_pauses=False)
    assert "eight hundred fifty-one" in out and "851" not in out


def test_preprocess_for_tts_fish_only_steps_noop_for_elevenlabs():
    # No provider -> acronym + forbidden-tag steps are skipped. Bit-string
    # verbalize is opt-in (default off), so 11 survives here too.
    el = {"preprocessor": {}}
    out = preprocess_for_tts("SAR code 11", el, add_pauses=False)
    assert "S-A-R" not in out  # acronym expansion is fish-only
    assert "11" in out and "one-one" not in out  # verbalize off by default
    # When opted in, verbalize is provider-agnostic (runs even for elevenlabs).
    el_on = {"preprocessor": {"verbalize_bit_strings": True}}
    out_on = preprocess_for_tts("SAR code 11", el_on, add_pauses=False)
    assert "one-one" in out_on


def test_preprocess_for_tts_scrubber_idempotent_without_pauses():
    text = "code 11 and SAR"
    once = preprocess_for_tts(text, _FISH, add_pauses=False)
    twice = preprocess_for_tts(once, _FISH, add_pauses=False)
    assert once == twice


def test_preprocess_for_tts_ch10_codewords_when_opted_in():
    # Hamming coding-theory (CH10) is the one source kind that opts the scrubber
    # back on. With verbalize_bit_strings: true, bare codewords still read
    # digit-by-digit through the full preprocess chain. Guards the opt-in path
    # against future regex regressions.
    cfg = {"provider": "fish_speech", "preprocessor": {"verbalize_bit_strings": True}}
    text = "The codewords are 0, 10, 110, and 111 in order."
    out = preprocess_for_tts(text, cfg, add_pauses=False)
    assert "one-zero, one-one-zero, and one-one-one" in out
    assert "110" not in out and "111" not in out


def test_binary_codeword_prompt_examples_drop_ambiguous_ten():
    # The self-contradictory example list that named the decimal 10 as a binary
    # codeword ("e.g. 0, 10, 110, 1011") is what licensed the LLM to digit-spell
    # ordinary tens. Guard all four prompt sites: each carries a BINARY CODEWORDS
    # rule, and none lists 10 right after the leading "0," of the example.
    repo = Path(__file__).resolve().parent.parent
    sites = [
        "swanki/conf/prompts/default.yaml",
        "swanki/conf/prompts/book_voice.yaml",
        "swanki/audio/reading.py",
        "swanki/audio/summary.py",
    ]
    for rel in sites:
        text = (repo / rel).read_text()
        assert "BINARY CODEWORDS" in text, f"{rel} missing binary rule"
        assert "0, 10," not in text, f"{rel} still lists 10 as a codeword example"


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
        append_chunk_pause("Hello.\n[short pause]\n[pause]", "fish_speech") == "Hello."
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
    assert append_chunk_pause("Hello.", "elevenlabs") == 'Hello. <break time="1.0s" />'


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


def test_write_chunk_manifest_records_speed(tmp_path):
    # The gen speed is persisted so a later surgical edit re-TTSs at the same
    # speed; omitted (None) for callers that do not pass it.
    path = write_chunk_manifest(tmp_path, "lecture", "out.mp3", [], speed=1.0)
    assert json.loads(path.read_text())["speed"] == 1.0
    path2 = write_chunk_manifest(tmp_path, "summary", "out.mp3", [])
    assert json.loads(path2.read_text())["speed"] is None


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
    restitch_from_chunks(
        manifest_path,
        out,
        bookend_start_pause_ms=300,
        bookend_end_pause_ms=2000,
        bookend_trailing_pause_ms=1500,
    )

    assert out.exists()
    audio = AudioSegment.from_mp3(str(out))
    # 500 start + 300 + 1000 chunk + 2000 + 500 end + 1500 trailing = ~5800ms
    assert len(audio) > 5500
    # Overrides were persisted into the manifest for future restitches.
    saved = json.loads(manifest_path.read_text())["postprocessor"]
    assert saved["bookend_start_pause_ms"] == 300
    assert saved["bookend_end_pause_ms"] == 2000
    assert saved["bookend_trailing_pause_ms"] == 1500


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
        tmp_path,
        "lecture",
        "out.mp3",
        [],
        postprocessor=post,
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


# ---------------------------------------------------------------------------
# build_bookend_text — chapter bookend text generation for lecture/summary/reading
# ---------------------------------------------------------------------------


_CH_KEY = "hammingArtDoingScience2020_03_history-of-computers-hardware"
_CH_KEY_PREFIXED = "hammingArtDoingScience2020_CH03_history-of-computers-hardware"
_CH_EXACT = "Hamming, Art Doing Science, 2020, Chapter 3, history of computers hardware"


def test_build_bookend_text_lecture_chapter_start():
    out = build_bookend_text(_CH_KEY, "lecture", "start")
    assert out == f"This lecture is posted as {_CH_EXACT}. Let's Begin."


def test_build_bookend_text_lecture_chapter_end():
    out = build_bookend_text(_CH_KEY, "lecture", "end")
    assert out == f"This concludes the lecture. It is posted as {_CH_EXACT}."


def test_build_bookend_text_summary_chapter_start():
    out = build_bookend_text(_CH_KEY, "summary", "start")
    assert out == f"This summary is posted as {_CH_EXACT}. Let's Begin."


def test_build_bookend_text_summary_chapter_end():
    out = build_bookend_text(_CH_KEY, "summary", "end")
    assert out == f"This concludes the summary. It is posted as {_CH_EXACT}."


def test_build_bookend_text_reading_chapter_start():
    # audio_type=transcript is the internal name for reading audio; user-facing
    # word is "reading" so the spoken text says "reading".
    out = build_bookend_text(_CH_KEY, "transcript", "start")
    assert out == f"This reading is posted as {_CH_EXACT}. Let's Begin."


def test_build_bookend_text_reading_chapter_end():
    out = build_bookend_text(_CH_KEY, "transcript", "end")
    assert out == f"This concludes the reading. It is posted as {_CH_EXACT}."


def test_build_bookend_text_chapter_slug_roman_numeral_spelled_as_word():
    # ch07 AI-II: trailing "-ii" must be spoken as "two", not "i i" / "g i s".
    ck = "hammingArtDoingScience2020_07_artificial-intelligence-ii"
    exact = "Hamming, Art Doing Science, 2020, Chapter 7, artificial intelligence two"
    assert build_bookend_text(ck, "lecture", "start") == (
        f"This lecture is posted as {exact}. Let's Begin."
    )
    assert build_bookend_text(ck, "lecture", "end") == (
        f"This concludes the lecture. It is posted as {exact}."
    )


def test_build_bookend_text_chapter_slug_three_letter_roman():
    # ch08 AI-III: "-iii" -> "three".
    ck = "hammingArtDoingScience2020_08_artificial-intelligence-iii"
    out = build_bookend_text(ck, "summary", "start")
    assert (
        "Hamming, Art Doing Science, 2020, Chapter 8, artificial intelligence three"
        in out
    )
    assert "Let's Begin." in out


def test_build_bookend_text_legacy_and_ch_prefix_keys_are_equivalent():
    # `_03_<slug>` and `_CH03_<slug>` MUST produce byte-identical bookends for
    # every audio_type and position so adopting the documented CH prefix is a
    # no-op rename. Non-negotiable invariant; future regex tweaks must keep it.
    for at in ("lecture", "summary", "transcript"):
        for pos in ("start", "end"):
            legacy = build_bookend_text(_CH_KEY, at, pos)
            prefixed = build_bookend_text(_CH_KEY_PREFIXED, at, pos)
            assert legacy == prefixed, f"diverged for {at}/{pos}"


def test_build_bookend_text_uses_chapter_word_not_o_form():
    # Regression guard for the 2026.05.19b "Chapter N" rendering -- catches a
    # future revert to `chapter_number_spoken` ("o seven") leaking into the
    # bookend context_key.
    out = build_bookend_text(_CH_KEY, "lecture", "start")
    assert "Chapter 3" in out
    assert "o three" not in out


def test_build_bookend_text_non_chapter_lecture_keeps_legacy_form():
    assert (
        build_bookend_text("bishopDeepLearning2024", "lecture", "start")
        == "Today's lecture is posted as: Bishop, Deep Learning, 2024."
    )
    assert (
        build_bookend_text("bishopDeepLearning2024", "lecture", "end")
        == "And with that we conclude: Bishop, Deep Learning, 2024."
    )


def test_build_bookend_text_non_chapter_lecture_with_title():
    out = build_bookend_text(
        "bishopDeepLearning2024", "lecture", "start", paper_title="Some Paper Title"
    )
    assert out == (
        "Today's lecture is posted as: Bishop, Deep Learning, 2024. "
        "We are covering: Some Paper Title."
    )


def test_build_bookend_text_non_chapter_summary_keeps_label_form():
    # No natural "Here is the summary of ..." opener without a chapter number,
    # so non-chapter summary / transcript stays on the simple START:/END: label.
    assert (
        build_bookend_text("bishopDeepLearning2024", "summary", "start")
        == "START: Bishop, Deep Learning, 2024."
    )
    assert (
        build_bookend_text("bishopDeepLearning2024", "transcript", "end")
        == "END: Bishop, Deep Learning, 2024."
    )


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
            {
                "index": 0,
                "section": 0,
                "text": "a",
                "file": "c0.mp3",
                "boundary": "paragraph",
            },
            {
                "index": 1,
                "section": 0,
                "text": "b",
                "file": "c1.mp3",
                "boundary": "paragraph",
            },
            {
                "index": 2,
                "section": 0,
                "text": "c",
                "file": "c2.mp3",
                "boundary": "sentence",
            },
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
    assert out == 'the cell\'s ability "to detour"... continues'


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
    assert expand_acronyms_for_tts("USA and SAR", allowlist={"USA"}) == "USA and S-A-R"


def test_expand_acronyms_for_tts_skips_camelcase_lower_prefix():
    # myACRONYM is preceded by a lowercase letter -> not standalone.
    assert expand_acronyms_for_tts("myACRONYM stays put") == "myACRONYM stays put"


def test_expand_acronyms_for_tts_skips_camelcase_lower_suffix():
    # ABCfoo is followed by lowercase -> not standalone.
    assert expand_acronyms_for_tts("ABCfoo bar") == "ABCfoo bar"


def test_expand_acronyms_for_tts_no_change_for_lowercase():
    assert expand_acronyms_for_tts("nothing to do here") == "nothing to do here"


def test_expand_acronyms_for_tts_skips_single_letter():
    assert (
        expand_acronyms_for_tts("the X factor and A team") == "the X factor and A team"
    )


def test_expand_acronyms_for_tts_roman_numerals_become_words():
    # Regression: the acronym expander letter-spelled "II" -> "I-I", which Fish
    # read as "one one". Unambiguous Roman numerals now map to a cardinal word.
    assert expand_acronyms_for_tts("World War II size") == "World War two size"
    assert expand_acronyms_for_tts("World War III") == "World War three"
    assert expand_acronyms_for_tts("Part VII") == "Part seven"
    assert expand_acronyms_for_tts("Henry VIII") == "Henry eight"
    assert expand_acronyms_for_tts("Chapter IX") == "Chapter nine"
    assert expand_acronyms_for_tts("Section XV") == "Section fifteen"


def test_expand_acronyms_for_tts_ambiguous_roman_left_as_acronym():
    # IV (intravenous) and VI (the vi editor) collide with real initialisms, so
    # they keep letter-spelling — exactly as before the Roman-numeral guard.
    assert expand_acronyms_for_tts("the IV bag") == "the I-V bag"
    assert expand_acronyms_for_tts("open it in VI") == "open it in V-I"


def test_expand_acronyms_for_tts_real_acronyms_unaffected():
    # C/D/M-letter initialisms are absent from the Roman map -> still spelled.
    assert expand_acronyms_for_tts("the SAR system") == "the S-A-R system"
    assert expand_acronyms_for_tts("MIT") == "M-I-T"
    assert expand_acronyms_for_tts("an MD and a CV") == "an M-D and a C-V"
    assert expand_acronyms_for_tts("USA and SAR", allowlist={"USA"}) == "USA and S-A-R"


def test_roman_guard_does_not_touch_bit_string_codewords():
    # Codewords are digits ([01]+), handled by a separate rule; the Roman guard
    # (letters only) must not interfere with digit-by-digit verbalization.
    assert expand_acronyms_for_tts("the codeword 111") == "the codeword 111"
    assert verbalize_bit_strings("the codeword 111 and 1011") == (
        "the codeword one-one-one and one-zero-one-one"
    )


# ---------------------------------------------------------------------------
# RC1: section-break sentinel must survive acronym expansion verbatim
# ---------------------------------------------------------------------------


def test_expand_acronyms_preserves_section_break_marker():
    # Without protection, "BREAK" (preceded by "_", followed by "-") matches
    # the [A-Z]{2,6} rule and is mangled to "B-R-E-A-K", which the literal
    # splitter then fails to strip and Fish speaks aloud.
    text = f"intro\n\n{SECTION_BREAK_MARKER}\nnext"
    out = expand_acronyms_for_tts(text)
    assert SECTION_BREAK_MARKER in out
    assert "B-R-E-A-K" not in out
    assert "\x00" not in out


def test_expand_acronyms_preserves_marker_but_still_expands_neighbors():
    # The mask must protect ONLY the marker; real acronyms around it still
    # get letter-spelled.
    text = f"the SAR system\n{SECTION_BREAK_MARKER}\nthen NASA flew"
    out = expand_acronyms_for_tts(text)
    assert SECTION_BREAK_MARKER in out
    assert "S-A-R" in out
    assert "N-A-S-A" in out


def test_section_break_round_trips_through_expand_then_split():
    # End-to-end of the bug: expand then split. The marker must survive
    # expansion so split_transcript_by_sections can strip it; no section
    # may contain the marker or a mangled remnant.
    text = f"one TWO\n\n{SECTION_BREAK_MARKER}\n\nthree FOUR"
    expanded = expand_acronyms_for_tts(text)
    sections = split_transcript_by_sections(expanded)
    assert len(sections) == 2
    assert all(SECTION_BREAK_MARKER not in s for s in sections)
    assert all("B-R-E-A-K" not in s for s in sections)


def test_expand_acronyms_marker_protection_with_allowlist_and_override():
    # Real Hamming combined path (Scout C gotcha 2): SAR is in the allowlist
    # AND has a pronunciation override. Acronym pass skips SAR (allowlist),
    # the marker stays protected, then the override rewrites bare "SAR" to
    # "sar". The two mechanisms are complementary; the sentinel mask must
    # not disturb either.
    text = f"the SAR system\n{SECTION_BREAK_MARKER}\nover"
    out = expand_acronyms_for_tts(text, allowlist={"SAR"})
    assert "S-A-R" not in out  # allowlisted -> not letter-spelled
    assert "SAR" in out
    assert SECTION_BREAK_MARKER in out
    final = apply_pronunciation_overrides(out, {"SAR": "sar"})
    assert "the sar system" in final
    assert SECTION_BREAK_MARKER in final
    assert "B-R-E-A-K" not in final


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
    paragraphs = "\n\n".join(f"Paragraph {i}. " + ("filler. " * 30) for i in range(5))
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
# chunk_text_paragraphs - balanced chunker (fish opt-in via soft_max_chars)
# ---------------------------------------------------------------------------


def test_balanced_path_is_opt_in_default_byte_identical():
    # Without soft_max_chars the legacy greedy packer runs and output is
    # byte-identical to the documented legacy behavior.
    text = "Para one is short.\n\nPara two is also short."
    legacy = chunk_text_paragraphs(text, max_chars=200)
    explicit_none = chunk_text_paragraphs(
        text, max_chars=200, soft_max_chars=None, min_sentences_per_chunk=2
    )
    assert legacy == explicit_none
    assert legacy == [("Para one is short.\n\nPara two is also short.", "paragraph")]


def test_balanced_legacy_cap_paths_match_existing_tests():
    # The four legacy-path invariants still hold when soft_max_chars is None.
    paras = "\n\n".join(f"Paragraph {i}. " + ("filler. " * 30) for i in range(5))
    assert all(len(t) <= 700 for t, _ in chunk_text_paragraphs(paras, max_chars=700))


def test_balanced_even_split_groups_are_near_equal():
    sentences = [f"Sentence number {i} here." for i in range(8)]
    groups = _balanced_sentence_groups(sentences, 4)
    assert len(groups) == 4
    # Every sentence is preserved, in order, no duplication.
    assert [s for g in groups for s in g] == sentences
    sizes = [len(" ".join(g)) for g in groups]
    # Near-equal: spread between largest and smallest group stays small.
    assert max(sizes) - min(sizes) <= max(len(s) for s in sentences) + 5


def test_balanced_oversoft_paragraph_splits_into_even_chunks():
    # One paragraph well over soft splits into multiple near-soft chunks; the
    # first carries "paragraph", the rest "sentence" (Decision 7).
    para = " ".join(f"Sentence {i} ends here now." for i in range(40))
    chunks = chunk_text_paragraphs(
        para, max_chars=650, soft_max_chars=500, min_sentences_per_chunk=2
    )
    assert len(chunks) > 1
    assert all(len(t) <= 650 for t, _ in chunks)
    boundaries = [b for _, b in chunks]
    assert boundaries[0] == "paragraph"
    assert all(b == "sentence" for b in boundaries[1:])


def test_balanced_hard_cap_never_exceeded():
    para = " ".join(f"Sentence {i} runs on a bit here." for i in range(120))
    chunks = chunk_text_paragraphs(
        para, max_chars=650, soft_max_chars=500, min_sentences_per_chunk=2
    )
    assert all(len(t) <= 650 for t, _ in chunks), [len(t) for t, _ in chunks]


def test_balanced_no_single_sentence_chunk_when_mergeable():
    # A trailing lone sentence merges into a neighbor rather than standing as a
    # single-sentence chunk.
    para = " ".join(f"Sentence {i} ends here." for i in range(15))
    chunks = chunk_text_paragraphs(
        para, max_chars=200, soft_max_chars=140, min_sentences_per_chunk=2
    )

    def nsents(t):
        import re

        return len([s for s in re.split(r"(?<=[.!?])\s+", t) if s.strip()])

    # Every chunk that COULD have merged (i.e. is not at the hard-cap limit)
    # holds at least two sentences.
    lone = [t for t, _ in chunks if nsents(t) < 2 and len(t) < 140]
    assert lone == [], lone


def test_balanced_merges_lone_middle_sentence():
    # A single-sentence middle paragraph must merge into a neighbor rather than
    # stand alone, so no short chunk is left with one sentence.
    import re

    text = "Aa bb cc. Dd ee ff.\n\nGg hh ii jj.\n\nKk ll mm. Nn oo pp."
    chunks = chunk_text_paragraphs(
        text, max_chars=120, soft_max_chars=40, min_sentences_per_chunk=2
    )
    for t, _ in chunks:
        n = len([s for s in re.split(r"(?<=[.!?])\s+", t) if s.strip()])
        assert n >= 2 or len(t) >= 120


def test_balanced_lone_sentence_kept_when_unmergeable():
    # A single-sentence paragraph longer than the cap cannot merge with any
    # neighbor and is accepted as a lone chunk (the S8-survivor escape hatch).
    long_sentence = (
        "This one sentence is deliberately very long "
        + ("and keeps going " * 20)
        + "until it stops."
    )
    neighbor = "Short tail. Another short tail."
    text = f"{long_sentence}\n\n{neighbor}"
    chunks = chunk_text_paragraphs(
        text, max_chars=200, soft_max_chars=180, min_sentences_per_chunk=2
    )
    # The long sentence stays as its own chunk (merging would bust the cap).
    assert any(long_sentence[:30] in t for t, _ in chunks)


def test_balanced_first_chunk_boundary_is_paragraph():
    text = "Alpha one. Alpha two.\n\nBeta one. Beta two.\n\nGamma one. Gamma two."
    chunks = chunk_text_paragraphs(
        text, max_chars=200, soft_max_chars=40, min_sentences_per_chunk=2
    )
    assert chunks[0][1] == "paragraph"


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
        [[a, b]],
        out,
        section_pause_ms=0,
        chunk_pause_ms=500,
    )
    combined = AudioSegment.from_mp3(str(out))
    assert 2400 <= len(combined) <= 2600


def test_combine_audio_with_section_pauses_per_boundary_silence(tmp_path):
    # Three chunks: gap before chunk[1] is "paragraph" (1100ms), gap before
    # chunk[2] is "sentence" (500ms). Total = 1000 + 1100 + 1000 + 500 + 1000
    # = 4600ms. With uniform chunk_pause_ms it would be 1000+x+1000+x+1000.
    a = tmp_path / "a.mp3"
    b = tmp_path / "b.mp3"
    c = tmp_path / "c.mp3"
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


def test_combine_audio_with_section_pauses_falls_back_to_chunk_pause_ms_without_map(
    tmp_path,
):
    # When chunk_pause_ms_by_boundary is absent, the legacy uniform
    # chunk_pause_ms applies to every gap (no regression for existing callers).
    a = tmp_path / "a.mp3"
    b = tmp_path / "b.mp3"
    for p in (a, b):
        AudioSegment.silent(duration=1000).export(str(p), format="mp3")
    out = tmp_path / "out.mp3"
    combine_audio_with_section_pauses(
        [[a, b]],
        out,
        section_pause_ms=0,
        chunk_pause_ms=700,
        # boundaries provided but no map -> uniform behavior preserved
        chunk_boundaries=[["paragraph", "sentence"]],
    )
    combined = AudioSegment.from_mp3(str(out))
    # 1000 + 700 + 1000 = 2700ms
    assert 2600 <= len(combined) <= 2800


def test_combine_audio_with_section_pauses_missing_boundary_key_falls_back(tmp_path):
    # Per-boundary map missing a key -> that gap falls back to chunk_pause_ms.
    a = tmp_path / "a.mp3"
    b = tmp_path / "b.mp3"
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
        [[a, b]],
        out,
        section_pause_ms=0,
        chunk_pause_ms=0,
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
        [[a, b]],
        out_with,
        section_pause_ms=0,
        gain_match_target_dbfs=-25.0,
    )
    combine_audio_with_section_pauses(
        [[a, b]],
        out_without,
        section_pause_ms=0,
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
        [[a, b]],
        out,
        section_pause_ms=0,
        chunk_tail_trim_ms=0,
    )
    combined = AudioSegment.from_mp3(str(out))
    assert 1900 <= len(combined) <= 2100


# Table/figure landmark survives the reading scrubber chain into its own
# section, so combine_audio_with_section_pauses brackets it with real silence.


def test_table_landmark_splits_into_own_section():
    from swanki.audio._common import add_tts_pauses
    from swanki.processing.landmarks import landmark_block

    content = (
        "Body before the table."
        + landmark_block("Table", "A comparison of computers and humans.")
        + "Body after."
    )
    cleaned = clean_markdown_for_tts(content)
    with_pauses = add_tts_pauses(cleaned, "fish_speech")
    sections = split_transcript_by_sections(with_pauses)
    assert any(
        s.startswith("Table: A comparison of computers and humans.") for s in sections
    )
    assert sum(1 for s in sections if "Body before" in s) == 1
    assert sum(1 for s in sections if "Body after" in s) == 1


def test_figure_landmark_caption_not_doubled_by_empty_alt():
    # The cleaner emits ![](url): clean_markdown_for_tts must drop the empty
    # alt + URL, leaving only the landmark's spoken caption (no double-read).
    from swanki.processing.landmarks import landmark_block

    content = "![](img/fig1.png)" + landmark_block("Figure", "A growth curve.")
    cleaned = clean_markdown_for_tts(content)
    assert "img/fig1.png" not in cleaned
    assert cleaned.count("A growth curve.") == 1


# ---------------------------------------------------------------------------
# collapse_stacked_pause_tags: stacked tags must never survive (Fish renders
# every tag; a stack = pause + audible-breath artifact mid-chunk).
# ---------------------------------------------------------------------------


class TestCollapseStackedPauseTags:
    def test_mixed_stack_collapses_to_pause(self):
        from swanki.audio._common import collapse_stacked_pause_tags

        text = "computing.\n[short pause]\n[pause]\n\nIn the 1930s"
        out = collapse_stacked_pause_tags(text)
        assert out == "computing.\n[pause]\n\nIn the 1930s"

    def test_triple_with_manual_tag_collapses(self):
        from swanki.audio._common import collapse_stacked_pause_tags

        text = "digital.\n[short pause]\n[pause]\n\n[short pause] Next"
        out = collapse_stacked_pause_tags(text)
        assert out == "digital.\n[pause]\n\nNext"

    def test_short_pause_run_stays_short(self):
        from swanki.audio._common import collapse_stacked_pause_tags

        text = "a. [short pause] [short pause] b"
        assert collapse_stacked_pause_tags(text) == "a. [short pause] b"

    def test_long_pause_wins(self):
        from swanki.audio._common import collapse_stacked_pause_tags

        text = "a.\n[short pause]\n[long pause]\n\nb"
        assert collapse_stacked_pause_tags(text) == "a.\n[long pause]\n\nb"

    def test_single_tags_untouched(self):
        from swanki.audio._common import collapse_stacked_pause_tags

        text = "a. [short pause] b.\n[pause]\n\nc"
        assert collapse_stacked_pause_tags(text) == text

    def test_add_tts_pauses_paragraph_break_yields_single_tag(self):
        # Regression: the paragraph rule ([pause]) and the sentence rule
        # ([short pause]) both fire on a period-terminated paragraph break;
        # the mixed stack must collapse to one tag.
        import re

        from swanki.audio._common import add_tts_pauses

        out = add_tts_pauses(
            "This was analog computing, not digital computing.\n\n"
            "In the 1930s, slide rules were standard equipment.",
            "fish_speech",
        )
        assert not re.search(
            r"\[(?:short |long )?pause\]\s*\[(?:short |long )?pause\]", out
        )
        assert "[pause]" in out


# ---------------------------------------------------------------------------
# verbalize_large_numbers
# ---------------------------------------------------------------------------


def test_verbalize_large_numbers_spells_out_big_cardinals():
    out = verbalize_large_numbers("measured 851 progeny and 826 proteins")
    assert out == (
        "measured eight hundred fifty-one progeny and eight hundred twenty-six proteins"
    )


def test_verbalize_large_numbers_handles_comma_grouping():
    assert verbalize_large_numbers("1,225 proteins") == (
        "one thousand two hundred twenty-five proteins"
    )
    # Comma-grouped numbers are spelled out even below min_value.
    assert verbalize_large_numbers("1,000", min_value=10_000).startswith("one thousand")


def test_verbalize_large_numbers_leaves_small_numbers_alone():
    text = "about 10 to 20 percent, and 76 of them"
    assert verbalize_large_numbers(text) == text


def test_verbalize_large_numbers_skips_years_identifiers_and_decimals():
    text = "in 2025 the ERG11 gene and Fig. 5-11 at 10:30 with 1.5-fold change"
    assert verbalize_large_numbers(text) == text
    assert verbalize_large_numbers("the 1990s") == "the 1990s"


def test_verbalize_large_numbers_is_idempotent():
    once = verbalize_large_numbers("6400 associations across 923 proteins")
    assert verbalize_large_numbers(once) == once
    assert not any(ch.isdigit() for ch in once)


def test_verbalize_large_numbers_scales():
    assert verbalize_large_numbers("6476") == "six thousand four hundred seventy-six"
    assert verbalize_large_numbers("1,000,000") == "one million"
    assert verbalize_large_numbers("100") == "one hundred"
