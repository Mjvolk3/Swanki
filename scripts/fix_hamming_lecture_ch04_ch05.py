"""
scripts/fix_hamming_lecture_ch04_ch05.py
[[scripts.fix_hamming_lecture_ch04_ch05]]
https://github.com/Mjvolk3/Swanki/tree/main/scripts/fix_hamming_lecture_ch04_ch05.py

Surgical Track-B repair of two live Hamming LECTURE chunks flagged by
today's ABS bookmarks:

  ch04 (history-of-computers-software) chunk26 -- TEXT + speech regen.
    The transcript reframed Hamming's prediction as post-2020 hindsight
    ("We have moved in that direction, though not as cleanly as one might
    have hoped"). Per user: the spoken year "2020" itself is jarring in a
    ~1995 lecture (the book was published 2020), so drop the year entirely
    and keep the forward-looking prediction in first-person book voice
    ("...but I would think that, in time, it will be fairly universal
    practice...").

  ch05 (history-of-computer-application) chunk20 -- SPEECH-only regen.
    The indirect-question list ("who supplies replacements, who writes
    diagnostics, who fixes flaws, and how future improvements arrive") is
    correct text but Fish renders it with rising/question intonation.
    Re-TTS the same text to re-roll prosody (chunk_edits value None).

Other chunks are reused byte-for-byte; each chapter lecture mp3 is
restitched independently. Pairs with the Zotero re-zip + abs_refresh
republish so BookPlayer serves the corrected audio.
"""

from pathlib import Path

from dotenv import load_dotenv

from swanki.audio.surgical import fish_speech_healthy, regenerate_and_restitch

load_dotenv(dotenv_path=str(Path.cwd() / ".env"))

HAM = Path(
    "/scratch/projects/torchcell-scratch/Swanki_Data/hammingArtDoingScience2020"
)
CH04 = HAM / "hammingArtDoingScience2020_04_history-of-computers-software_4"
CH05 = HAM / "hammingArtDoingScience2020_05_history-of-computer-application_4"
CH04_MANIFEST = CH04 / "lecture_chunks" / "chunk_manifest.json"
CH05_MANIFEST = CH05 / "lecture_chunks" / "chunk_manifest.json"

FISH = {
    "provider": "fish_speech",
    "server_url": "http://localhost:8080",
    "reference_id": "hamming-20260428T1135-science-vs-engineering",
    "temperature": 0.8,
    "format": "mp3",
}
SPEED = 1.1

# ch04 chunk26: faithful to source page-7, first-person, forward-looking
# from 1995 (no post-2020 retrospective).
CH04_26 = (
    "In the long run, what I want is for the person with the problem to "
    "write the code directly, without an intermediary who knows computers "
    "but not the application. That day is unfortunately too far off to do "
    "much good immediately, [short pause] but I would think that, in "
    "time, it will be fairly universal practice for the expert in the "
    "field of application to do the actual program preparation, rather "
    "than have experts in computers, ignorant of the field of "
    "application, do it."
)


def main() -> None:
    """Pre-flight Fish, then patch ch04 chunk26 (text) + ch05 chunk20 (speech)."""
    assert CH04_MANIFEST.exists(), f"missing {CH04_MANIFEST}"
    assert CH05_MANIFEST.exists(), f"missing {CH05_MANIFEST}"
    if not fish_speech_healthy(FISH["server_url"]):
        raise SystemExit(
            f"Fish Speech not reachable at {FISH['server_url']} -- aborting."
        )

    out4 = regenerate_and_restitch(
        CH04_MANIFEST,
        {26: CH04_26},
        audio_type="lecture",
        speed=SPEED,
        tts_kwargs=FISH,
    )
    print(f"ch04 -> {out4}")

    out5 = regenerate_and_restitch(
        CH05_MANIFEST,
        {20: None},
        audio_type="lecture",
        speed=SPEED,
        tts_kwargs=FISH,
    )
    print(f"ch05 -> {out5}")


if __name__ == "__main__":
    main()
