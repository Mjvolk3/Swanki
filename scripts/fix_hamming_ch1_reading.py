"""
scripts/fix_hamming_ch1_reading.py
[[scripts.fix_hamming_ch1_reading]]
https://github.com/Mjvolk3/Swanki/tree/main/scripts/fix_hamming_ch1_reading.py

Surgical Track-B repair of the LIVE Hamming Ch1 reading audio, driven by
the 6 orange Zotero annotations (4 root causes). Re-TTS only chunks
0/31/37/53/54 with hand-corrected text and restitch -- every other chunk
mp3 is reused byte-for-byte. Source of corrected text is the OCR'd
clean-md-singles for this chapter (verbatim where reinstating dropped
prose). Run after Track-A landed; pairs with the Zotero/ABS republish in
scripts/push_hamming_ch1_reading_fix.sh.

  RC1  chunk0, chunk31  strip spoken "---SECTION_B-R-E-A-K---" leak
  RC2  chunk31          reinstate the dropped page 4->5 bridge sentence
  RC3  chunk37          give the aphorism a trailing beat
  RC4  chunk53, chunk54 read the advantages table across each row
"""

from pathlib import Path

from dotenv import load_dotenv

from swanki.audio.surgical import fish_speech_healthy, regenerate_and_restitch

load_dotenv(dotenv_path=str(Path.cwd() / ".env"))

SWANKI_DATA = Path("/scratch/projects/torchcell-scratch/Swanki_Data")
CH1 = (
    SWANKI_DATA
    / "hammingArtDoingScience2020"
    / "hammingArtDoingScience2020_01_orientation_12"
)
MANIFEST = CH1 / "reading_chunks" / "chunk_manifest.json"

# Hamming reading was rendered with the cloned Hamming voice (see
# swanki/conf/models/fish_speech_hamming.yaml); patched chunks MUST use the
# same reference or they will not match the untouched chunks.
FISH = {
    "provider": "fish_speech",
    "server_url": "http://localhost:8080",
    "reference_id": "hamming-20260428T1135-science-vs-engineering",
    "temperature": 0.8,
    "format": "mp3",
}
SPEED = 1.1

# RC1: chunk0 -- drop the mangled marker line; the surrounding [pause] tags
# already supply the break.
CHUNK0 = (
    "Hamming, Art Doing Science, 2020, 01, orientation\n\n"
    "[pause]\n\n"
    "Orientation\n\n"
    "[pause]\n\n"
    "The purpose of this course is to prepare you for your technical "
    "future. There is really no technical content in the course, though I "
    "will, of course, refer to a great deal of it, and hopefully it will "
    "generally be a good review of the fundamentals you have learned. Do "
    "not think the technical content is the course-it is only illustrative "
    "material. [short pause]  Style of thinking is the center of the "
    "course. I am concerned with educating and not training you."
)

# RC1 + RC2: chunk31 -- drop the mangled marker AND reinstate the bridge
# clause Pass-2 lost at the page 4->5 boundary. Verbatim from
# clean-md-singles/page-5.md ("(at least to me)" rendered as the audio
# style's comma form, matching the retained remainder).
CHUNK31 = (
    "they arise so you will not be left behind, as so many good engineers "
    "are in the long run. In the position I found myself in at the "
    "Laboratories, where I was the only one locally who seemed, at least "
    "to me, to have a firm grasp on computing, I was forced to learn "
    "numerical analysis, computers, pretty much all of the physical "
    "sciences at least enough to cope with the many different computing "
    "problems which arose and whose solution could benefit the Labs, as "
    "well as a lot of the social and some the biological sciences. Thus I "
    "am a veteran of learning enough to get along without at the same time "
    "devoting all my effort to learning new topics and thereby not "
    "contributing my share to the total effort of the organization."
)

# RC3: chunk37 -- same text, add a trailing [short pause] so the punchline
# lands instead of being swallowed by the chunk transition.
CHUNK37 = (
    "History is often used as a long-term guide; some people believe "
    "history repeats itself and others believe exactly the opposite! "
    "[short pause]  It is obvious:\n"
    "[short pause]\n"
    "[pause]\n\n"
    "The past was once the future and the future will become the past.\n"
    "[short pause]"
)

# RC4: chunk53/54 -- read each row across (label then its description as
# one clause), every row present, light [short pause] between rows instead
# of the heavy per-cell [pause] that made it sound fragmented and partial.
CHUNK53 = (
    "The course will center around computers. It is not merely because I "
    "spent much of my career in Computer Science and Engineering, rather "
    "it seems to me computers will dominate your technical lives. I will "
    "repeat a number of times in the book the following facts: Computers "
    "when compared to Humans have the advantages:\n"
    "[short pause]\n"
    "[pause]\n\n"
    "Economics: far cheaper, and getting more so.\n"
    "[short pause]\n"
    "Speed: far, far faster.\n"
    "[short pause]\n"
    "Accuracy: far more accurate, precise.\n"
    "[short pause]\n"
    "Reliability: far ahead, many have error correction built into them.\n"
    "[short pause]\n"
    "Rapidity of control: many current airplanes are unstable and require "
    "rapid computer control to make them practical."
)
CHUNK54 = (
    "Freedom from boredom: an overwhelming advantage.\n"
    "[short pause]\n"
    "Bandwidth in and out: again overwhelming.\n"
    "[short pause]\n"
    "Ease of retraining: change programs, not unlearn and then learn the "
    "new thing consuming hours and hours of human time and effort.\n"
    "[short pause]\n"
    "Hostile environments: outer space, underwater, high radiation fields, "
    "warfare, manufacturing situations that are unhealthful, etc.\n"
    "[short pause]\n"
    "Personnel problems: they tend to dominate management of humans but "
    "not of machines; with machines there are no pensions, personal "
    "squabbles, unions, personal leave, egos, deaths of relatives, "
    "recreation, etc."
)

EDITS: dict[int, str] = {
    0: CHUNK0,
    31: CHUNK31,
    37: CHUNK37,
    53: CHUNK53,
    54: CHUNK54,
}


def main() -> None:
    """Pre-flight Fish, then re-TTS the 5 chunks and restitch Ch1 reading."""
    assert MANIFEST.exists(), f"Live manifest missing: {MANIFEST}"
    if not fish_speech_healthy(FISH["server_url"]):
        raise SystemExit(
            f"Fish Speech not reachable at {FISH['server_url']} -- aborting "
            "before any re-TTS."
        )
    out = regenerate_and_restitch(
        MANIFEST,
        EDITS,
        audio_type="reading",
        speed=SPEED,
        tts_kwargs=FISH,
    )
    print(f"done -> {out}")


if __name__ == "__main__":
    main()
