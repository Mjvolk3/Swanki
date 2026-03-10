---
id: t6srrow4vo0g8r2x5v39fll
title: Utils Audio Refactor Utils Files Grew Too Large
desc: ''
updated: 1773102499525
created: 1773102423836
---
Refactor `swanki/utils/audio.py` into Top-Level Audio Package

## Context

`swanki/utils/audio.py` has grown to ~2918 lines. It serves 4 distinct audio types (card, summary, reading, lecture) plus shared TTS utilities. Audio is a major subsystem -- not a utility -- so it belongs as a top-level package alongside `models`, `pipeline`, `processing`.

## Target Structure

```
swanki/audio/                    <-- new top-level package
  __init__.py      (~20 lines)  - re-exports public API
  _common.py       (~390 lines) - shared TTS utilities, constants
  card.py          (~913 lines) - flashcard audio (front/back, cloze, citations)
  summary.py       (~154 lines) - document summary narration
  reading.py       (~326 lines) - full document reading
  lecture.py       (~1016 lines) - educational lecture generation
```

Delete: `swanki/utils/audio.py` (replaced by `swanki/audio/` package)

## 1. Create `swanki/audio/` package directory

New top-level package at `swanki/audio/`.

## 2. `swanki/audio/_common.py` -- Shared Utilities

Move these functions and constants:

| Symbol                   | Current Lines |
|--------------------------|---------------|
| `DEFAULT_VOICE_ID`       | 82-83         |
| `clean_markdown_for_tts` | 558-601       |
| `chunk_text`             | 604-657       |
| `text_to_speech`         | 660-775       |
| `combine_audio`          | 778-816       |
| `_validate_audio_file`   | 1017-1072     |
| `filter_metadata`        | 1561-1641     |

Imports needed: `logging`, `re`, `time`, `pathlib.Path`, `typing`, `httpx`, `elevenlabs`, `pydub`.

## 3. `swanki/audio/card.py` -- Card Audio

Move:

| Symbol                     | Current Lines |
|----------------------------|---------------|
| `generate_card_transcript` | 86-555        |
| `generate_citation_audio`  | 819-1014      |
| `generate_card_audio`      | 2672-2918     |

Imports from `_common`: `DEFAULT_VOICE_ID`, `chunk_text`, `text_to_speech`, `combine_audio`, `_validate_audio_file`.
Imports from models: `PlainCard`.
Imports from formatting: `humanize_citation_key`.

## 4. `swanki/audio/summary.py` -- Summary Audio

Move:

| Symbol                   | Current Lines |
|--------------------------|---------------|
| `generate_summary_audio` | 1075-1228     |

Imports from `_common`: `DEFAULT_VOICE_ID`, `chunk_text`, `text_to_speech`, `combine_audio`, `clean_markdown_for_tts`.
Imports from formatting: `humanize_citation_key`.

## 5. `swanki/audio/reading.py` -- Reading Audio

Move:

| Symbol                   | Current Lines |
|--------------------------|---------------|
| `_humanize_latex`        | 1231-1374     |
| `generate_reading_audio` | 1377-1558     |

Imports from `_common`: `DEFAULT_VOICE_ID`, `chunk_text`, `text_to_speech`, `combine_audio`, `clean_markdown_for_tts`.
Imports from formatting: `humanize_citation_key`.

## 6. `swanki/audio/lecture.py` -- Lecture Audio

Move:

| Symbol                        | Current Lines |
|-------------------------------|---------------|
| `critique_transcript_chunks`  | 1644-1728     |
| `chunk_by_headers`            | 1731-1810     |
| `split_large_section`         | 1813-1849     |
| `extract_context`             | 1852-1881     |
| `generate_and_validate_chunk` | 1884-2072     |
| `generate_lecture_audio`      | 2075-2669     |

Imports from `_common`: `DEFAULT_VOICE_ID`, `chunk_text`, `text_to_speech`, `combine_audio`, `clean_markdown_for_tts`, `filter_metadata`.
Imports from models: `LectureTranscriptFeedback`.
Imports from formatting: `humanize_citation_key`.

## 7. `swanki/audio/__init__.py` -- Public API

```python
"""Audio generation utilities for Swanki TTS pipeline."""
from .card import generate_card_audio
from .lecture import generate_lecture_audio
from .reading import generate_reading_audio
from .summary import generate_summary_audio

__all__ = [
    "generate_card_audio",
    "generate_lecture_audio",
    "generate_reading_audio",
    "generate_summary_audio",
]
```

## 8. Update import sites

Two files import from the old location:

**`swanki/pipeline/pipeline.py`** (line 77):
`from ..utils.audio import ...` --> `from ..audio import ...`

**`swanki/utils/__init__.py`** (lines 2-6):
Remove audio re-exports. Update `__all__` to drop the 3 audio symbols.

## 9. Update frontmatter in new files

Each new `.py` file gets docstring-style frontmatter pointing to its dendron note and test file.

## 10. Create dendron notes for new modules

Create notes for the new submodules:

- `notes/swanki.audio._common.md`
- `notes/swanki.audio.card.md`
- `notes/swanki.audio.summary.md`
- `notes/swanki.audio.reading.md`
- `notes/swanki.audio.lecture.md`

Update existing `notes/swanki.utils.audio.md` with a redirect note pointing to the new `swanki.audio` hierarchy.

---

## Verification

1. `python -c "from swanki.audio import generate_card_audio, generate_summary_audio, generate_reading_audio, generate_lecture_audio"` -- imports work
2. `ruff check swanki/audio/` -- no lint errors
3. `mypy swanki/audio/` -- type checks pass (at current baseline)
4. Existing tests still pass
