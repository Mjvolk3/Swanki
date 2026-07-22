"""
swanki/audio/reading_correctness.py
[[swanki.audio.reading_correctness]]
https://github.com/Mjvolk3/Swanki/tree/main/swanki/audio/reading_correctness.py
Test file: tests/test_reading_correctness.py

Report-only audio-path correctness critic for the reading and lecture tracks.

Structurally modeled on ``swanki/pipeline/card_correctness.py`` (Pydantic
verdicts, ``with_safety_retry`` around the LLM pass, atomic temp-then-rename
JSON audit writers) but wired as a separate hook that survives ``audio_only``
runs, where the card gate at ``generate_outputs`` never fires. It NEVER mutates
audio: every check emits a per-chapter JSON audit and nothing else.

Turning a verified finding into corrected, re-voiced audio is the NEXT layer,
now shipped as the opt-in apply layer ``swanki/audio/source_corrections.py``
(``apply_source_corrections``). That layer reads a HAND-AUTHORED per-chapter
spec -- a higher bar than this critic -- and is NEVER auto-populated from these
findings. This module stays strictly report-only.

Three checks:

1. Reading clause diff (deterministic, default on). Compares each Pass-2 input
   window to its transcript output over sentence-normalized tokens with
   ``difflib.SequenceMatcher`` and flags only residual inserted / duplicated /
   dropped blocks. Legitimate meaning-preserving Pass-2 edits (acronym
   first-use expansion, "et al" / citation collapse, ``---SECTION_BREAK---``
   markers, per-digit codeword spelling) are normalized out first so they do
   not flood the diff. A chunk that fell back to the humanized input verbatim
   is marked ``not_assessed`` -- never a clean pass.
2. Acronym double-emit validator (deterministic, default on). Run once on the
   FINAL ``tts_transcript`` (post-scrubber), where the phantom name only
   exists. Honors the ``_ROMAN_NUMERAL_WORDS`` carve-out and the
   ``acronym_allowlist``.
3. Lecture factual pass (LLM, default off). Assesses CLAIMS not wording with a
   very high acceptance rate; ``assessment_failed`` is kept fail-open.
"""

from __future__ import annotations

import difflib
import json
import logging
import re
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

from ..llm.agents import lecture_factual_agent
from ..llm.safety import with_safety_retry
from ..models.cards import (
    AcronymDoubleEmitFinding,
    LectureFactualAssessment,
    LectureFactualEntry,
    ReadingChunkFidelity,
)
from ._common import _ROMAN_NUMERAL_WORDS

logger = logging.getLogger(__name__)

SECTION_BREAK_MARKER = "---SECTION_BREAK---"


# ---------------------------------------------------------------------------
# Reading check 1: normalized clause diff (deterministic)
# ---------------------------------------------------------------------------

_DIGIT_WORDS = {
    "zero": "0",
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}
# Hyphenated per-digit codeword spelling, e.g. "one-one-zero" (the
# verbalize_bit_strings / codeword output). Folded back to "110" so a source
# "110" and its spelled transcript form align.
_DIGIT_WORD_SEQ_RE = re.compile(
    r"\b(?:zero|one|two|three|four|five|six|seven|eight|nine)"
    r"(?:-(?:zero|one|two|three|four|five|six|seven|eight|nine))+\b",
    re.IGNORECASE,
)
# Acronym first-use expansion in its three surface forms. All fold to the bare
# acronym so the legit Pass-2 rule-2 edit is aligned out before diffing.
_ACR_THEN_PAREN_RE = re.compile(r"\b([A-Z]{2,6})\s*\([^)]*\)")
_EXPANSION_THEN_PAREN_RE = re.compile(r"\b[A-Za-z][A-Za-z \-]{3,}\s*\(([A-Z]{2,6})\)")
_EXPANSION_THEN_COMMA_RE = re.compile(r"\b[a-z][a-z \-]{3,},\s+([A-Z]{2,6})\b")
_YEAR_RE = re.compile(r"\b(?:19|20)\d{2}[a-z]?\b")
_ET_AL_RE = re.compile(r"\bet\s+al\.?", re.IGNORECASE)
_SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+")


def _fold_codewords(text: str) -> str:
    """Collapse hyphenated digit-word runs ("one-one-zero") back to "110"."""

    def _sub(m: re.Match) -> str:
        return "".join(_DIGIT_WORDS[w.lower()] for w in m.group(0).split("-"))

    return _DIGIT_WORD_SEQ_RE.sub(_sub, text)


def _fold_acronym_first_use(text: str) -> str:
    """Reduce acronym first-use expansions to the bare acronym.

    Handles ``ATP (adenosine triphosphate)``, ``adenosine triphosphate (ATP)``,
    and ``adenosine triphosphate, ATP`` -- the three ways Pass-2 renders a
    first use -- so the source window and its transcript align on the acronym.
    """
    text = _ACR_THEN_PAREN_RE.sub(r"\1", text)
    text = _EXPANSION_THEN_PAREN_RE.sub(r"\1", text)
    text = _EXPANSION_THEN_COMMA_RE.sub(r"\1", text)
    return text


def _normalize_sentence(sentence: str) -> str:
    """Normalize one sentence for meaning-preserving comparison.

    Folds acronym first-use and codeword spelling, drops "et al", leftover
    parentheticals and citation years, lowercases, and strips punctuation, so
    only genuine wording differences survive the diff.
    """
    s = _fold_acronym_first_use(sentence)
    s = _fold_codewords(s)
    s = _ET_AL_RE.sub(" ", s)
    s = re.sub(r"\([^)]*\)", " ", s)
    s = _YEAR_RE.sub(" ", s)
    s = s.lower()
    s = re.sub(r"[^a-z0-9 ]+", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def _normalized_sentences(text: str) -> list[str]:
    """Strip section-break markers and return normalized, non-empty sentences."""
    text = text.replace(SECTION_BREAK_MARKER, " ")
    out: list[str] = []
    for part in _SENTENCE_SPLIT_RE.split(text):
        normalized = _normalize_sentence(part)
        if normalized:
            out.append(normalized)
    return out


def diff_chunk(
    chunk_index: int,
    source_chunk: str,
    transcript_chunk: str,
    fell_back: bool,
) -> ReadingChunkFidelity:
    """Diff one Pass-2 input window against its transcript output.

    Args:
        chunk_index: 0-based Pass-2 chunk index.
        source_chunk: The post-humanize source window fed to Pass-2.
        transcript_chunk: The Pass-2 transcript output for that window.
        fell_back: True when Pass-2 exhausted retries and returned the input
            verbatim; such chunks are marked ``not_assessed`` (Decision 6).

    Returns:
        A :class:`ReadingChunkFidelity` with residual inserted / duplicated /
        dropped sentence blocks, or a ``not_assessed`` entry when ``fell_back``.
    """
    if fell_back:
        return ReadingChunkFidelity(
            chunk_index=chunk_index, not_assessed=True, fell_back=True
        )

    src = _normalized_sentences(source_chunk)
    tr = _normalized_sentences(transcript_chunk)

    inserted: list[str] = []
    dropped: list[str] = []
    matcher = difflib.SequenceMatcher(a=src, b=tr, autojunk=False)
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag in ("insert", "replace"):
            inserted.extend(tr[j1:j2])
        if tag in ("delete", "replace"):
            dropped.extend(src[i1:i2])

    src_counts = Counter(src)
    tr_counts = Counter(tr)
    duplicated = [s for s, c in tr_counts.items() if c > 1 and c > src_counts.get(s, 0)]

    return ReadingChunkFidelity(
        chunk_index=chunk_index,
        not_assessed=False,
        fell_back=False,
        inserted=inserted,
        duplicated=duplicated,
        dropped=dropped,
    )


# ---------------------------------------------------------------------------
# Reading check 2: acronym double-emit validator (deterministic)
# ---------------------------------------------------------------------------

# A letter-spelled acronym as emitted by expand_acronyms_for_tts: single
# uppercase letters joined by hyphens, e.g. "A-T-P".
_LETTER_SPELLED = r"(?:[A-Z]-){1,5}[A-Z]"
# Expansion phrase immediately followed by the letter-spelled acronym -- the
# two-layer phantom-name bug ("adenosine triphosphate, A-T-P").
_LETTER_SPELLED_ADJ_RE = re.compile(
    r"([A-Za-z][A-Za-z \-]{3,}),\s+(" + _LETTER_SPELLED + r")\b"
)
# Any first-use expansion (bare OR letter-spelled acronym) after a comma, used
# to count cross-chunk double-expansions.
_FIRST_USE_RE = re.compile(
    r"([A-Za-z][A-Za-z \-]{3,}),\s+(" + _LETTER_SPELLED + r"|[A-Z]{2,6})\b"
)


def _bare_acronym(spelled: str) -> str:
    """Strip letter-spelling hyphens: ``A-T-P`` -> ``ATP``."""
    return spelled.replace("-", "")


def validate_acronym_double_emit(
    tts_transcript: str, allowlist: set[str] | None = None
) -> list[AcronymDoubleEmitFinding]:
    """Flag acronym double-emits on the final ``tts_transcript``.

    Detects the two-layer ``<expansion>, <letter-spelled acronym>`` phantom
    name and cross-chunk double-expansion of the same acronym. Tokens in
    ``allowlist`` (already pronounceable, e.g. ``USA``) and Roman numerals in
    ``_ROMAN_NUMERAL_WORDS`` (``II`` -> "two", never letter-spelled) are never
    flagged. Reports a known generator gap; does not fix it.

    Args:
        tts_transcript: The final, post-scrubber reading transcript.
        allowlist: Acronyms never letter-spelled (skip). ``None`` skips none.

    Returns:
        One finding per detected double-emit, in discovery order.
    """
    skip = allowlist or set()
    findings: list[AcronymDoubleEmitFinding] = []

    for m in _LETTER_SPELLED_ADJ_RE.finditer(tts_transcript):
        acronym = _bare_acronym(m.group(2))
        if acronym in skip or acronym in _ROMAN_NUMERAL_WORDS:
            continue
        findings.append(
            AcronymDoubleEmitFinding(
                acronym=acronym,
                expansion=m.group(1).strip(),
                kind="letter_spelled_after_expansion",
                snippet=m.group(0).strip(),
            )
        )

    seen: Counter[str] = Counter()
    example: dict[str, str] = {}
    for m in _FIRST_USE_RE.finditer(tts_transcript):
        acronym = _bare_acronym(m.group(2))
        if acronym in skip or acronym in _ROMAN_NUMERAL_WORDS:
            continue
        seen[acronym] += 1
        example.setdefault(acronym, m.group(0).strip())
    for acronym, count in seen.items():
        if count > 1:
            findings.append(
                AcronymDoubleEmitFinding(
                    acronym=acronym,
                    expansion="",
                    kind="cross_chunk_double_expansion",
                    snippet=(
                        f"{example[acronym]} "
                        f"(first-use expansion appears {count} times)"
                    ),
                )
            )

    return findings


# ---------------------------------------------------------------------------
# Lecture factual pass (LLM, default off)
# ---------------------------------------------------------------------------

LECTURE_FACTUAL_INSTRUCTIONS: str = (
    "You are a careful subject-matter fact-checker for an educational audio "
    "LECTURE transcript. You are given a DOCUMENT SUMMARY for context and the "
    "full LECTURE TRANSCRIPT (reformulated first-person prose).\n\n"
    "Your ONLY job is to catch clear FACTUAL errors in the CLAIMS the "
    "transcript makes -- NEVER wording, phrasing, tone, style, first-person "
    "framing, roadmaps, or pedagogical choices. The source is trusted and the "
    "acceptance rate must be VERY HIGH: when in any doubt, 'pass'. It is far "
    "better to let a borderline claim through than to flag a defensible one.\n\n"
    "Return one verdict:\n"
    "- 'pass' (the default and expected answer): the claims are factually "
    "defensible, OR you are not highly confident any claim is wrong, OR your "
    "only concern is stylistic.\n"
    "- 'fixed': ONLY when a claim is unambiguously, factually wrong AND the "
    "single correct version is obvious. Supply corrected_transcript with the "
    "minimal correction and name the claim.\n"
    "- 'dropped': ONLY when a claim is unambiguously wrong and unfixable.\n\n"
    "This assessment is REPORT-ONLY: a 'fixed' or 'dropped' verdict is recorded "
    "for audit and NEVER applied to the audio. Give a concise reason."
)


def _lecture_context(summary_context: str, transcript: str) -> str:
    """Assemble the lecture factual-assessment prompt."""
    return f"DOCUMENT SUMMARY\n{summary_context}\n\nLECTURE TRANSCRIPT\n{transcript}"


def _assess_lecture(
    transcript: str, summary_context: str, model_string: str
) -> LectureFactualAssessment | None:
    """Assess a lecture transcript's claims once.

    Returns:
        The agent's :class:`LectureFactualAssessment`, or ``None`` if the call
        failed after safety retries -- the caller treats ``None`` as
        ``assessment_failed`` and keeps the audio untouched (fail-open).
    """
    prompt = _lecture_context(summary_context, transcript)
    try:
        result = with_safety_retry(
            lecture_factual_agent,
            prompt,
            instructions=LECTURE_FACTUAL_INSTRUCTIONS,
            model=model_string,
            label="lecture factual",
        )
    except Exception as e:
        logger.error(
            "lecture factual pass could not assess transcript: %s; keeping fail-open",
            e,
        )
        return None
    return result.output


def run_lecture_factual_pass(
    transcript: str, summary_context: str, model_string: str
) -> list[LectureFactualEntry]:
    """Run the report-only lecture factual pass, returning audit entries.

    Never mutates the transcript or audio. An assessment that fails after
    safety retries yields a single ``assessment_failed`` entry (fail-open).

    Args:
        transcript: The final lecture transcript (claims are assessed).
        summary_context: Compact document-summary context block.
        model_string: Resolved pydantic-ai model string.

    Returns:
        A list of one :class:`LectureFactualEntry`.
    """
    assessment = _assess_lecture(transcript, summary_context, model_string)
    if assessment is None:
        return [
            LectureFactualEntry(
                verdict="assessment_failed",
                reason="assessment call failed after retries; kept fail-open",
            )
        ]
    entry = LectureFactualEntry(
        verdict=assessment.verdict,
        reason=assessment.reason,
        claim=assessment.claim or "",
        corrected=assessment.corrected_transcript,
    )
    if entry.verdict in ("fixed", "dropped"):
        logger.info(
            "lecture factual pass %s (report-only, not applied): %s",
            entry.verdict.upper(),
            entry.reason,
        )
    return [entry]


# ---------------------------------------------------------------------------
# Collectors (filled on the audio path, written by the pipeline hook)
# ---------------------------------------------------------------------------


@dataclass
class ReadingCorrectnessCollector:
    """Accumulates reading fidelity signal across the Pass-2 loop.

    Filled inside ``generate_reading_audio`` (per-chunk diff in the Pass-2
    loop; one acronym validation on the final ``tts_transcript``); the pipeline
    hook reads the accumulated blocks and writes the audit. Per-mode toggles
    let a run disable either deterministic check.
    """

    clause_diff: bool = True
    acronym_validator: bool = True
    chunk_fidelities: list[ReadingChunkFidelity] = field(default_factory=list)
    acronym_findings: list[AcronymDoubleEmitFinding] = field(default_factory=list)

    def record_chunk(
        self,
        chunk_index: int,
        source_chunk: str,
        transcript_chunk: str,
        fell_back: bool,
    ) -> None:
        """Diff one Pass-2 chunk and append its fidelity entry (if enabled)."""
        if not self.clause_diff:
            return
        self.chunk_fidelities.append(
            diff_chunk(chunk_index, source_chunk, transcript_chunk, fell_back)
        )

    def record_acronyms(self, tts_transcript: str, allowlist: set[str]) -> None:
        """Validate the final transcript for acronym double-emits (if enabled)."""
        if not self.acronym_validator:
            return
        self.acronym_findings = validate_acronym_double_emit(tts_transcript, allowlist)


@dataclass
class LectureCorrectnessCollector:
    """Carries lecture factual-pass config into ``generate_lecture_audio``.

    Default off. When ``enabled``, ``run`` assesses the final transcript and
    stores the entries; the pipeline hook writes them to the lecture audit.
    """

    enabled: bool
    model_string: str
    summary_context: str
    entries: list[LectureFactualEntry] = field(default_factory=list)

    def run(self, transcript: str) -> None:
        """Run the factual pass over ``transcript`` (if enabled)."""
        if not self.enabled:
            return
        self.entries = run_lecture_factual_pass(
            transcript, self.summary_context, self.model_string
        )


# ---------------------------------------------------------------------------
# Atomic audit writers
# ---------------------------------------------------------------------------


def _atomic_write_json(payload: dict, path: Path) -> None:
    """Write ``payload`` to ``path`` as JSON, atomically (temp then rename)."""
    tmp = path.with_suffix(path.suffix + ".tmp")
    with open(tmp, "w") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    tmp.rename(path)


def write_reading_audit(
    chunk_fidelities: list[ReadingChunkFidelity],
    acronym_findings: list[AcronymDoubleEmitFinding],
    path: Path,
) -> None:
    """Write the reading correctness audit to ``path`` (atomic).

    The payload is a ``summary`` count block, one ``chunks`` entry per Pass-2
    chunk (including ``not_assessed`` fallbacks), and the ``acronym_findings``.
    Report-only: writing this never changed any audio.
    """
    assessed = [c for c in chunk_fidelities if not c.not_assessed]
    payload = {
        "summary": {
            "total_chunks": len(chunk_fidelities),
            "assessed_chunks": len(assessed),
            "not_assessed_chunks": sum(1 for c in chunk_fidelities if c.not_assessed),
            "chunks_with_insertions": sum(1 for c in assessed if c.inserted),
            "chunks_with_duplications": sum(1 for c in assessed if c.duplicated),
            "chunks_with_drops": sum(1 for c in assessed if c.dropped),
            "acronym_findings": len(acronym_findings),
        },
        "chunks": [c.model_dump() for c in chunk_fidelities],
        "acronym_findings": [f.model_dump() for f in acronym_findings],
    }
    _atomic_write_json(payload, path)


def write_lecture_audit(entries: list[LectureFactualEntry], path: Path) -> None:
    """Write the lecture factual-pass audit to ``path`` (atomic).

    The payload is a ``summary`` verdict-count block plus one ``claims`` entry
    per assessment. Report-only.
    """
    payload = {
        "summary": {
            "total": len(entries),
            "passed": sum(1 for e in entries if e.verdict == "pass"),
            "fixed": sum(1 for e in entries if e.verdict == "fixed"),
            "dropped": sum(1 for e in entries if e.verdict == "dropped"),
            "assessment_failed": sum(
                1 for e in entries if e.verdict == "assessment_failed"
            ),
        },
        "claims": [e.model_dump() for e in entries],
    }
    _atomic_write_json(payload, path)
