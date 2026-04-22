"""
scripts/retts_cleaned_transcripts.py
[[scripts.retts_cleaned_transcripts]]
https://github.com/Mjvolk3/Swanki/tree/main/scripts/retts_cleaned_transcripts.py

Re-render lecture audio from a hand-fixed transcript without re-running the LLM.

One-off for fixing the duplicate-lecture defect in thornburg v2 and zvyagin v6.
Reads a cleaned `*_fixed_transcript.md` (with the duplicate restart block
excised), runs the same TTS + concat pipeline as generate_lecture_audio, and
writes the audio to the canonical `{prefix}-lecture-audio.mp3` path.

Run:
  conda activate swanki && python scripts/retts_cleaned_transcripts.py
"""

import os
import time
from pathlib import Path

from dotenv import load_dotenv

from swanki.audio._common import (
    add_tts_pauses,
    append_chunk_pause,
    chunk_text_paragraphs,
    clean_markdown_for_tts,
    combine_audio_with_section_pauses,
    generate_bookend_audio,
    split_transcript_by_sections,
    text_to_speech,
    tts_chunks_parallel,
    write_chunk_manifest,
    LECTURE_TTS_MODEL,
)

load_dotenv()


FISH_KW = dict(
    provider="fish_speech",
    server_url="http://localhost:8080",
    reference_id="british-prof",
    temperature=0.8,
    format="mp3",
)


def strip_markdown_frontmatter(raw: str) -> str:
    """Drop the `# Lecture Audio Transcript` header / citation-key stanza."""
    marker = "**Generated Transcript:**"
    idx = raw.find(marker)
    if idx >= 0:
        return raw[idx + len(marker) :].lstrip()
    return raw


def render_transcript_to_audio(
    *,
    transcript: str,
    output_path: Path,
    transcripts_dir: Path,
    citation_key: str,
    paper_title: str | None = None,
    speed: float = 1.1,
    tts_kwargs: dict | None = None,
) -> None:
    """Replicates the TTS/assembly tail of generate_lecture_audio."""
    tts_kwargs = tts_kwargs or {}
    provider = str(tts_kwargs.get("provider", "elevenlabs"))
    is_fish = provider == "fish_speech"

    # Persist raw + cleaned transcript alongside outputs (matches main flow).
    transcripts_dir.mkdir(parents=True, exist_ok=True)
    raw_path = transcripts_dir / f"{output_path.stem}_transcript.md"
    raw_path.write_text(
        f"# Lecture Audio Transcript\n\n**Citation Key:** {citation_key}\n\n"
        f"**Generated Transcript:**\n\n{transcript}\n",
        encoding="utf-8",
    )

    tts_transcript = add_tts_pauses(
        clean_markdown_for_tts(transcript), provider=provider
    )
    cleaned_path = (
        transcripts_dir / f"{output_path.stem}_transcript_cleaned_markdown.md"
    )
    cleaned_path.write_text(
        f"Lecture Audio Transcript (Cleaned for TTS)\n\nCitation Key: {citation_key}\n\n"
        f"Generated Transcript:\n\n{tts_transcript}\n",
        encoding="utf-8",
    )

    chunks_dir = output_path.parent / "lecture_chunks"
    chunks_dir.mkdir(parents=True, exist_ok=True)

    bookend_start = generate_bookend_audio(
        citation_key,
        "lecture",
        "start",
        chunks_dir,
        elevenlabs_api_key="",
        voice_id="",
        speed=speed,
        paper_title=paper_title,
        **tts_kwargs,
    )
    bookend_end = generate_bookend_audio(
        citation_key,
        "lecture",
        "end",
        chunks_dir,
        elevenlabs_api_key="",
        voice_id="",
        speed=speed,
        **tts_kwargs,
    )

    sections_text = split_transcript_by_sections(tts_transcript) or [tts_transcript]
    prefix = f"{citation_key}_{output_path.stem}"

    all_jobs: list[tuple[int, str, Path]] = []
    chunk_counter = 0
    for sec_idx, section in enumerate(sections_text):
        audio_chunks = chunk_text_paragraphs(
            section, max_chars=2000 if is_fish else 4500
        )
        for chunk in audio_chunks:
            chunk_path = chunks_dir / f"{prefix}_chunk{chunk_counter}.mp3"
            all_jobs.append((sec_idx, chunk, chunk_path))
            chunk_counter += 1

    all_jobs = [
        (sec_idx, append_chunk_pause(text, provider), path)
        for sec_idx, text, path in all_jobs
    ]

    if is_fish and len(all_jobs) > 1:
        pairs = [(text, path) for _, text, path in all_jobs]
        tts_chunks_parallel(
            pairs, "", "", speed, tts_model=LECTURE_TTS_MODEL, **tts_kwargs
        )
    else:
        for _, chunk, chunk_path in all_jobs:
            text_to_speech(
                chunk, "", chunk_path, "", speed,
                tts_model=LECTURE_TTS_MODEL, **tts_kwargs,
            )
            time.sleep(1)

    section_chunks: list[list[Path]] = [[] for _ in sections_text]
    for sec_idx, _, chunk_path in all_jobs:
        section_chunks[sec_idx].append(chunk_path)

    combine_audio_with_section_pauses(
        section_chunks,
        output_path,
        section_pause_ms=4000 if is_fish else 3000,
        chunk_crossfade_ms=0,
        bookend_start=bookend_start,
        bookend_end=bookend_end,
    )

    chunk_entries = [
        {"index": i, "section": sec_idx, "text": text, "file": path.name}
        for i, (sec_idx, text, path) in enumerate(all_jobs)
    ]
    write_chunk_manifest(
        chunks_dir,
        "lecture",
        output_path.name,
        chunk_entries,
        bookend_start=bookend_start.name if bookend_start else None,
        bookend_end=bookend_end.name if bookend_end else None,
    )


JOBS = [
    dict(
        label="thornburg",
        cleaned_transcript=Path(
            "/scratch/projects/torchcell-scratch/Swanki_Data/thornburgBringingGeneticallyMinimal2026/thornburgBringingGeneticallyMinimal2026-fish_2/lecture_transcript/thornburgBringingGeneticallyMinimal2026-lecture-audio_v2_fixed_transcript.md"
        ),
        output_path=Path(
            "/scratch/projects/torchcell-scratch/Swanki_Data/thornburgBringingGeneticallyMinimal2026/thornburgBringingGeneticallyMinimal2026-fish_2/thornburgBringingGeneticallyMinimal2026-fish-lecture-audio.mp3"
        ),
        citation_key="thornburgBringingGeneticallyMinimal2026",
    ),
    dict(
        label="zvyagin",
        cleaned_transcript=Path(
            "/scratch/projects/torchcell-scratch/Swanki_Data/zvyaginGenSLMsGenomescaleLanguage2023/zvyaginGenSLMsGenomescaleLanguage2023/lecture_transcript/zvyaginGenSLMsGenomescaleLanguage2023-lecture-audio_v6_fixed_transcript.md"
        ),
        output_path=Path(
            "/scratch/projects/torchcell-scratch/Swanki_Data/zvyaginGenSLMsGenomescaleLanguage2023/zvyaginGenSLMsGenomescaleLanguage2023/zvyaginGenSLMsGenomescaleLanguage2023-lecture-audio.mp3"
        ),
        citation_key="zvyaginGenSLMsGenomescaleLanguage2023",
    ),
]


def main() -> None:
    for job in JOBS:
        print(f"=== re-TTS: {job['label']} ===")
        raw = job["cleaned_transcript"].read_text(encoding="utf-8")
        transcript = strip_markdown_frontmatter(raw)
        print(f"  transcript: {len(transcript.split())} words")
        transcripts_dir = job["output_path"].parent / "lecture_transcript"
        render_transcript_to_audio(
            transcript=transcript,
            output_path=job["output_path"],
            transcripts_dir=transcripts_dir,
            citation_key=job["citation_key"],
            speed=1.1,
            tts_kwargs=FISH_KW,
        )
        print(f"  wrote {job['output_path']}")


if __name__ == "__main__":
    main()
