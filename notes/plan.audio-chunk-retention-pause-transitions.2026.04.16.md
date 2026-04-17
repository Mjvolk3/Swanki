---
id: c1eh2i5g0lv3i5dnidacljq
title: Audio Chunk Retention and Pause-Based Transitions
desc: Replace crossfade with direct concat + Fish Speech pause tags, keep chunks for surgical regen
updated: 1776391123080
created: 1776390587081
---

Plan: Audio Chunk Retention and Pause-Based Transitions

## Context

Listening to Bishop Deep Learning CH01 lecture audio reveals two problems:

1. **Abrupt voice shifts between TTS chunks.** Each chunk is synthesized independently by Fish Speech. When chunks are joined with 200ms crossfade (`combine_audio_with_section_pauses` line 712), the overlap clips sentence endings and the timbre mismatch is audible -- an uncanny valley effect. Fish Speech already supports `[pause]`, `[short pause]`, and `[long pause]` inline tags that generate natural pauses as part of the audio. The `add_tts_pauses()` function already inserts these at paragraph boundaries. If we concatenate chunks directly (0 crossfade) instead of overlapping, the generated pauses handle spacing natively.

2. **Intermediate chunk files are deleted.** After combining, all chunk `.mp3` files are immediately unlinked (lecture.py:744-750, reading.py:230-236, summary.py:216-222, card.py:455-479). This means any quality issue requires full regeneration of all chunks + TTS. Keeping chunks enables surgical regeneration: re-TTS one bad chunk, restitch from the manifest, done.

## Approach

### Three changes, one principle: let Fish Speech handle pacing, keep the evidence.

**1. Direct concatenation instead of crossfade.**
Change `chunk_crossfade_ms` default from 200 to 0 in `combine_audio_with_section_pauses()`. Change `crossfade_ms` default from 200 to 0 in `combine_audio()`. This applies to both Fish Speech and ElevenLabs -- ElevenLabs uses SSML `<break>` tags which serve the same role. The `[pause]` tags (Fish Speech) and `<break>` tags (ElevenLabs) already exist in the text from `add_tts_pauses()`, so the generated audio already contains natural pauses at its boundaries.

**2. Append `[long pause]` to each chunk before TTS.**
After chunking but before TTS dispatch, append `[long pause]` (Fish Speech) or `<break time="1.0s" />` (ElevenLabs) to the end of each chunk's text. This ensures every chunk's audio ends with a generous pause, making direct concatenation seamless. This is provider-aware but trivial: one line per module in the TTS dispatch loop.

**3. Keep chunks in subdirectories with a manifest.**
Instead of deleting chunk files, move them to a `{type}_chunks/` subdirectory (e.g., `lecture_chunks/`, `reading_chunks/`, `summary_chunks/`, `complementary_chunks/`). Write a JSON manifest alongside them that maps chunk index to section, text, and file path. This enables:

- Re-running TTS on a single chunk
- Restitching from existing chunks without any TTS
- Debugging which chunk sounds wrong

A new `restitch_from_chunks()` function reads the manifest and reassembles the final audio, enabling the surgical workflow.

## File Specifications

### `swanki/audio/_common.py` (MODIFY)

**Current state:** Contains `combine_audio()` (line 487) and `combine_audio_with_section_pauses()` (line 674) with crossfade defaults of 200ms. Contains `add_tts_pauses()` (line 50) which inserts `[pause]`/`[short pause]` for Fish Speech.

**Changes:**

1. **Change `combine_audio()` crossfade default** (line 490): `crossfade_ms: int = 200` -> `crossfade_ms: int = 0`

2. **Change `combine_audio_with_section_pauses()` crossfade default** (line 678): `chunk_crossfade_ms: int = 200` -> `chunk_crossfade_ms: int = 0`

3. **Add `append_chunk_pause()` helper function** after `add_tts_pauses()`:

```python
def append_chunk_pause(text: str, provider: str = "elevenlabs") -> str:
    """Append a pause tag to the end of a TTS chunk.

    Ensures each chunk's audio ends with a natural pause so that
    direct concatenation of chunks sounds seamless.

    Args:
        text: Chunk text to append pause to.
        provider: TTS provider name.

    Returns:
        Text with trailing pause tag appended.
    """
    text = text.rstrip()
    if provider == "fish_speech":
        if not text.endswith("[long pause]"):
            text += " [long pause]"
    else:
        if not text.endswith("/>"):
            text += ' <break time="1.0s" />'
    return text
```

4. **Add `write_chunk_manifest()` function:**

```python
def write_chunk_manifest(
    chunks_dir: Path,
    audio_type: str,
    output_file: str,
    chunks: list[dict],
    bookend_start: str | None = None,
    bookend_end: str | None = None,
) -> Path:
    """Write a chunk manifest JSON for surgical regeneration.

    Args:
        chunks_dir: Directory containing chunk files.
        audio_type: One of "lecture", "reading", "summary", "card".
        output_file: Filename of the combined output.
        chunks: List of dicts with keys: index, section, text, file.
        bookend_start: Filename of start bookend, if any.
        bookend_end: Filename of end bookend, if any.

    Returns:
        Path to the written manifest file.
    """
    manifest = {
        "audio_type": audio_type,
        "output_file": output_file,
        "bookend_start": bookend_start,
        "bookend_end": bookend_end,
        "chunks": chunks,
    }
    manifest_path = chunks_dir / "chunk_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2))
    logger.info(f"Wrote chunk manifest: {manifest_path} ({len(chunks)} chunks)")
    return manifest_path
```

5. **Add `restitch_from_chunks()` function:**

```python
def restitch_from_chunks(
    manifest_path: Path,
    output_path: Path,
    section_pause_ms: int = 2000,
    bookend_pause_ms: int = 500,
) -> None:
    """Reassemble final audio from chunk files using a manifest.

    Reads the chunk manifest JSON, loads each chunk file, and
    combines them with section pauses. Used for surgical
    regeneration: re-TTS one chunk, then restitch.

    Args:
        manifest_path: Path to chunk_manifest.json.
        output_path: Path for the reassembled output MP3.
        section_pause_ms: Silence between sections.
        bookend_pause_ms: Silence after start / before end bookend.
    """
    manifest = json.loads(manifest_path.read_text())
    chunks_dir = manifest_path.parent

    # Group chunks by section
    sections: dict[int, list[Path]] = {}
    for chunk in manifest["chunks"]:
        sec = chunk["section"]
        if sec not in sections:
            sections[sec] = []
        chunk_path = chunks_dir / chunk["file"]
        assert chunk_path.exists(), f"Chunk file missing: {chunk_path}"
        sections[sec].append(chunk_path)

    section_lists = [sections[k] for k in sorted(sections.keys())]

    bookend_start = None
    bookend_end = None
    if manifest.get("bookend_start"):
        bookend_start = chunks_dir / manifest["bookend_start"]
    if manifest.get("bookend_end"):
        bookend_end = chunks_dir / manifest["bookend_end"]

    combine_audio_with_section_pauses(
        section_lists,
        output_path,
        section_pause_ms=section_pause_ms,
        chunk_crossfade_ms=0,
        bookend_start=bookend_start,
        bookend_end=bookend_end,
        bookend_pause_ms=bookend_pause_ms,
    )
    logger.info(f"Restitched audio from {sum(len(s) for s in section_lists)} chunks -> {output_path}")
```

6. **Add `import json`** at top of file (not currently imported).

### `swanki/audio/lecture.py` (MODIFY)

**Current state:** Chunks created at lines 705-713, parallel TTS at 715-727, combine at 735-741, cleanup at 744-750.

**Changes:**

1. **Append pause to each chunk before TTS** (after line 713, before TTS dispatch):

```python
    # Append trailing pause to each chunk for clean concatenation
    provider = str(tts_kwargs.get("provider", "elevenlabs"))
    all_jobs = [
        (sec_idx, append_chunk_pause(text, provider), chunk_path)
        for sec_idx, text, chunk_path in all_jobs
    ]
```

Add import: `from ._common import append_chunk_pause`

2. **Move chunks to subdirectory** -- change chunk path generation (line 711):

```python
    chunks_dir = output_path.parent / "lecture_chunks"
    chunks_dir.mkdir(parents=True, exist_ok=True)
    # ...
    chunk_path = chunks_dir / f"{prefix}_chunk{chunk_counter}.mp3"
```

3. **Move bookend files to chunks_dir** -- update `generate_bookend_audio` calls (around lines 655-670) to write bookends into `chunks_dir`:

```python
    bookend_start = generate_bookend_audio(
        citation_key, "lecture", "start", chunks_dir,  # was output_path.parent
        elevenlabs_api_key, voice_id, speed, paper_title=paper_title, **tts_kwargs,
    )
```

4. **Write chunk manifest and keep files** -- replace cleanup block (lines 744-750) with:

```python
    # Write chunk manifest for surgical regeneration
    chunk_entries = [
        {"index": i, "section": sec_idx, "text": text, "file": Path(chunk_path).name}
        for i, (sec_idx, text, chunk_path) in enumerate(all_jobs)
    ]
    write_chunk_manifest(
        chunks_dir, "lecture", output_path.name, chunk_entries,
        bookend_start=bookend_start.name if bookend_start else None,
        bookend_end=bookend_end.name if bookend_end else None,
    )
    # Chunk files are intentionally kept for surgical regeneration
```

5. **Update combine call** (line 735) to pass `chunk_crossfade_ms=0` explicitly (belt-and-suspenders with the default change):

```python
    combine_audio_with_section_pauses(
        all_section_chunks,
        output_path,
        section_pause_ms=lecture_pause,
        chunk_crossfade_ms=0,
        bookend_start=bookend_start,
        bookend_end=bookend_end,
    )
```

### `swanki/audio/reading.py` (MODIFY)

**Current state:** Same pattern as lecture. Chunks at 196-206, TTS at 208-214, combine at 221-227, cleanup at 230-236.

**Changes:** Mirror lecture.py changes:

1. **Append pause** to each chunk text before TTS dispatch (after line 206).
2. **Chunks subdirectory**: change chunk path to `output_path.parent / "reading_chunks" / f"{prefix}_chunk{chunk_counter}.mp3"`.
3. **Bookends to chunks_dir**: update `generate_bookend_audio` calls (around lines 163-183) to write into `reading_chunks/`.
4. **Replace cleanup with manifest write** (lines 230-236).
5. **Pass `chunk_crossfade_ms=0`** to `combine_audio_with_section_pauses`.
6. **Add imports**: `append_chunk_pause`, `write_chunk_manifest` from `._common`.

### `swanki/audio/summary.py` (MODIFY)

**Current state:** Same pattern. Chunks at 179-189, TTS at 193-199, combine at 207-213, cleanup at 216-222.

**Changes:** Mirror lecture.py changes:

1. **Append pause** to each chunk text before TTS dispatch (after line 189).
2. **Chunks subdirectory**: `output_path.parent / "summary_chunks" / ...`.
3. **Bookends to chunks_dir**: update `generate_bookend_audio` calls (around lines 140-160).
4. **Replace cleanup with manifest write** (lines 216-222).
5. **Pass `chunk_crossfade_ms=0`** to `combine_audio_with_section_pauses`.
6. **Add imports**: `append_chunk_pause`, `write_chunk_manifest` from `._common`.

### `swanki/audio/card.py` (MODIFY)

**Current state:** Uses `combine_audio()` (not section-aware). Front chunks at lines 441-457, back chunks at 463-479. Cleanup at 455-457 and 479.

**Changes:**

1. **Append pause** to each chunk text before TTS (before lines 449 and 473):

```python
    from ._common import append_chunk_pause
    provider = str(tts_kwargs.get("provider", "elevenlabs"))
    # In the front chunk loop:
    chunk = append_chunk_pause(chunk, provider)
    # In the back chunk loop:
    chunk = append_chunk_pause(chunk, provider)
```

2. **Chunks subdirectory**: change chunk paths to write into `audio_dir / "card_chunks"`:

```python
    chunks_subdir = audio_dir / "card_chunks"
    chunks_subdir.mkdir(parents=True, exist_ok=True)
    chunk_path = chunks_subdir / f"{prefix}_{card_index}_front_chunk{i}.mp3"
```

3. **Pass `crossfade_ms=0`** to `combine_audio()` calls at lines 453 and 477.

4. **Remove `.unlink()` calls** at lines 455-457 and 479. Keep chunk files.

5. **Write card chunk manifest** -- after generating both sides, write manifest to `card_chunks/`:

```python
    # Write chunk manifest per card for surgical regeneration
    card_chunk_entries = []
    # ... build entries from front_chunks and back_chunks ...
    write_chunk_manifest(
        chunks_subdir, "card", f"{front_filename}+{back_filename}",
        card_chunk_entries,
    )
```

Note: Card chunk manifest is simpler -- no sections, no bookends. Each card has its own set of front/back chunks. A single manifest per card or one manifest for all cards in the directory. One manifest for the whole directory is simpler: append entries per card, keyed by card_id.

**Revised approach for card manifest:** Instead of per-card manifests, write one `card_chunks/chunk_manifest.json` for all cards, with each entry keyed by card_id and side (front/back). This matches how `generate_audio()` in pipeline.py processes all cards together.

### `swanki/audio/__init__.py` (MODIFY)

**Current state:** Re-exports the four `generate_*_audio` functions.

**Changes:** Add re-export for `restitch_from_chunks`:

```python
from ._common import restitch_from_chunks

__all__ = [
    "generate_card_audio",
    "generate_lecture_audio",
    "generate_reading_audio",
    "generate_summary_audio",
    "restitch_from_chunks",
]
```

### `tests/test_audio_common.py` (MODIFY)

**Current state:** Tests `combine_audio` and `combine_audio_with_section_pauses` but not crossfade values, `add_tts_pauses`, or chunk manifests.

**Changes:** Add test cases:

- `test_combine_audio_zero_crossfade` -- verify `combine_audio(crossfade_ms=0)` produces concatenation (output duration = sum of inputs, no overlap)
- `test_combine_sections_zero_crossfade` -- same for `combine_audio_with_section_pauses(chunk_crossfade_ms=0)`
- `test_append_chunk_pause_fish_speech` -- verify `append_chunk_pause("Hello.", "fish_speech")` returns `"Hello. [long pause]"`
- `test_append_chunk_pause_elevenlabs` -- verify SSML break tag appended
- `test_append_chunk_pause_idempotent` -- verify no double-append if already has pause
- `test_write_chunk_manifest` -- verify JSON structure and file creation
- `test_restitch_from_chunks` -- create chunk files, write manifest, restitch, verify output exists and has correct duration

## Edge Cases

1. **Chunk text already ends with `[pause]` or `[long pause]`.** The `append_chunk_pause()` function checks for existing trailing tags to avoid doubling. Only appends if not already present.

2. **Single chunk per section (no stitching needed).** `combine_audio_with_section_pauses` handles this -- a section with one chunk just gets that chunk's audio directly. The manifest still records it for completeness.

3. **Card chunks with citation audio.** Citation audio is prepended as the first chunk but is NOT a TTS-generated chunk -- it should not get a `[long pause]` appended. The citation audio file is already generated separately. In the manifest, mark it with `"type": "citation"` vs `"type": "tts"`.

4. **ElevenLabs provider.** The `<break time="1.0s" />` SSML tag is appended instead of `[long pause]`. The crossfade change to 0 applies to both providers. ElevenLabs already generates breaks from SSML tags in `add_tts_pauses()`.

5. **Disk space from retained chunks.** A 30-minute lecture with 2000-char chunks generates roughly 30-50 chunk files at ~200KB each = ~10MB. Negligible compared to the final combined audio (~30MB). No cleanup needed.

6. **Re-running the pipeline on the same paper.** The pipeline already auto-increments output directories (`_0`, `_1`, etc.). Chunk subdirectories are inside these, so no collision.

7. **`restitch_from_chunks()` with missing chunk files.** Assert that each chunk file exists before assembly. Fail fast with a clear error naming the missing file.

8. **Parallel TTS dispatch compatibility.** `tts_chunks_parallel()` takes `(text, path)` pairs. The `append_chunk_pause()` is applied to the text before building the pairs, so parallel dispatch sees the paused text. No change to `tts_chunks_parallel()` needed.

## Verification

1. **Unit tests:**

   ```
   pytest tests/test_audio_common.py -xvs -k "crossfade or chunk_pause or manifest or restitch"
   ```

2. **Type check:**

   ```
   mypy swanki/audio/_common.py swanki/audio/lecture.py swanki/audio/reading.py swanki/audio/summary.py swanki/audio/card.py
   ```

3. **Lint:**

   ```
   ruff check swanki/audio/
   ```

4. **Integration test (lecture on test paper):**

   ```bash
   swanki pdf_path=/scratch/projects/torchcell-scratch/Swanki_Data/luoWhenCausalInference2020/luoWhenCausalInference2020.pdf \
     citation_key=luoWhenCausalInference2020 \
     models=fish_speech \
     audio=lecture
   ```

   Then verify:
   - `lecture_chunks/` directory exists with chunk `.mp3` files
   - `lecture_chunks/chunk_manifest.json` exists with correct structure
   - Final lecture audio plays without crossfade clipping
   - Listen for natural pause-based transitions between chunks

5. **Surgical regeneration test:**

   ```python
   from swanki.audio import restitch_from_chunks
   from pathlib import Path
   restitch_from_chunks(
       Path("...lecture_chunks/chunk_manifest.json"),
       Path("...restitched-lecture.mp3"),
   )
   ```

   Compare restitched audio to original combined audio -- should be identical.

## Execution

To implement, start a new Claude Code session:

```
/read-codebase audio
```

Then:

```
Implement the plan at notes/plan.audio-chunk-retention-pause-transitions.2026.04.16.md. Read the plan first, then implement each file specification in order. Run verification after each file. Commit with /update-notes -> /stage -> /commit after each logical unit.
```

**Implementation order (respects dependencies):**

1. `swanki/audio/_common.py` -- crossfade defaults, `append_chunk_pause()`, `write_chunk_manifest()`, `restitch_from_chunks()`, `import json`
2. `tests/test_audio_common.py` -- new test cases for above
3. `swanki/audio/lecture.py` -- chunks subdir, pause append, manifest write, remove cleanup
4. `swanki/audio/reading.py` -- same pattern
5. `swanki/audio/summary.py` -- same pattern
6. `swanki/audio/card.py` -- same pattern (uses `combine_audio`, not section-aware)
7. `swanki/audio/__init__.py` -- re-export `restitch_from_chunks`

## Critic Review

A full-codebase critic review was performed. All findings addressed below.

### Feasibility Issues (all resolved)

**F1. Card.py inline import style.** The plan showed `from ._common import append_chunk_pause` inline inside the function body. Card.py already has a top-level import block from `._common` at lines 19-25. **Fix:** add `append_chunk_pause` and `write_chunk_manifest` to the existing top-level import at lines 19-25, not as inline imports.

**F2. `append_chunk_pause` ElevenLabs idempotency check.** The `text.endswith("/>")` check matches any SSML self-closing tag, not just `<break>`. This is intentional -- we don't want to stack any trailing SSML tags. Documented as expected behavior.

**No blocking feasibility issues.**

### Completeness Gaps (all resolved)

**C1. Card.py manifest race condition with parallel processing.** Pipeline.py line 1978 dispatches card audio in parallel via `ThreadPoolExecutor`. Writing to a shared `card_chunks/chunk_manifest.json` from parallel workers would corrupt the file. **Fix:** Use per-card manifest files instead of one shared manifest. Each card writes `card_chunks/{card_uuid}_manifest.json`. A card manifest has no sections or bookends -- just `{"card_id": "...", "side": "front"|"back", "chunks": [...]}`. Alternatively, the card manifest can be written after the parallel loop completes in `pipeline.py:generate_audio()`, since all cards and their transcripts/paths are available there. **Recommended approach:** skip manifest writing inside `generate_card_audio()`. Instead, after the parallel card processing loop in `pipeline.py:1983`, build and write one `card_chunks/chunk_manifest.json` sequentially from the completed card data. This avoids all race conditions.

**C2. Citation audio path for card chunks.** Citation audio is written to `audio_dir` (not `card_chunks/`). It should stay in `audio_dir` since it's a shared file reused across cards (pipeline.py pre-generates it at line 1963 to avoid races). The card manifest should reference it by relative path `../citation_key_citation.mp3` or just note the citation path separately. **Fix:** In the card manifest, add a top-level `"citation_audio"` field with the path relative to `audio_dir`.

**C3. Reading/summary manifest bookend fields.** The plan says "mirror lecture.py" for reading and summary but only shows bookend manifest fields for lecture. **Fix:** Explicitly note that reading.py and summary.py manifests also include `bookend_start` and `bookend_end` fields, exactly as in lecture.py. Reading uses audio_type `"transcript"` for bookends, summary uses `"summary"`.

**C4. Existing `manifest.py` vs new chunk manifests.** These are separate systems. `manifest.py` tracks paper-level metadata (`_audio_manifest.json`). The new chunk manifests (`chunk_manifest.json`) track per-audio-file chunk-level data for surgical regeneration. No collision. The distinction is clear from filename and location (chunk manifest lives inside `*_chunks/` subdirectories).

### Specification Quality Summary

| File Spec | Rating | Notes |
|-----------|--------|-------|
| `swanki/audio/_common.py` | GREEN | Complete implementations shown |
| `swanki/audio/lecture.py` | GREEN | Detailed code snippets for all 5 changes |
| `swanki/audio/reading.py` | GREEN (upgraded from YELLOW) | Same pattern as lecture, differences noted in C3 |
| `swanki/audio/summary.py` | GREEN (upgraded from YELLOW) | Same pattern as lecture, differences noted in C3 |
| `swanki/audio/card.py` | GREEN (upgraded from RED) | Race condition resolved via C1, citation path via C2, imports via F1 |
| `swanki/audio/__init__.py` | GREEN | Simple re-export |
| `tests/test_audio_common.py` | GREEN | Test cases clear, setup patterns match existing tests |

All RED ratings resolved. No remaining gaps.
