"""
swanki/pipeline/image_leak_gate.py
[[swanki.pipeline.image_leak_gate]]
https://github.com/Mjvolk3/Swanki/tree/main/swanki/pipeline/image_leak_gate.py
Test file: tests/test_image_leak_gate.py

Post-generation gate that stops a card's spoken figure description from giving
away its own answer.

The front description is read aloud before the learner responds. It is written
at image-processing time, before any card exists, so it cannot know what the
card ends up asking -- which is how a faithful description of a figure becomes a
spoiler for the one question that figure supports. This gate closes that loop:
once cards are final, each front-image card is judged against its own answer and
the description is regenerated question-aware until it stops leaking.

Judging is semantic, not lexical. Shared vocabulary between a description and an
answer is expected and harmless when the words name things visibly in the figure;
a description in entirely different words still leaks if it states or implies the
relationship being tested.
"""

import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from pydantic_ai import BinaryContent, ImageUrl

from ..llm.agents import image_description_agent, image_leak_judge_agent
from ..models.cards import ImageLeakAuditEntry, ImageLeakVerdict, PlainCard
from ..models.document import ImageDescription
from .run_agent import GENERATION, run_agent

logger = logging.getLogger(__name__)

JUDGE_PROMPT = """A flashcard has a figure. On the card FRONT, before the learner answers,
this description of the figure is read aloud to them.

QUESTION (what the learner must answer):
{question}

CORRECT ANSWER (hidden until they respond):
{answer}

DESCRIPTION SPOKEN ALOUD ON THE FRONT:
{spoken}

Does hearing that description before answering substantially give away the answer, or the
key concept the question is testing?

Judge MEANING, not word overlap. A description may share vocabulary with the answer and
still be fine if it only reports what is visibly in the figure (labels, axes, shapes,
colors, layout) -- a sighted learner would see those anyway. Conversely a description that
uses entirely different words still LEAKS if it states, paraphrases, explains, or strongly
implies the relationship, mechanism, conclusion, or classification being asked for.

Reading a label that literally contains the answer term counts as a leak. Describing where
things sit, what they look like, or how they are arranged does not."""

REWRITE_PROMPT = """You are writing the spoken description of a figure that plays on the
FRONT of a flashcard, before the learner has answered.

The flashcard question is:
    {question}

Describe ONLY what is visually present in the figure: shapes, labels, axes, arrangement,
colors, what stands out, and roughly where things sit. An audio-only learner must be able
to picture the figure from your words alone.

CRITICAL: this plays BEFORE the answer is revealed. You must NOT state, name, paraphrase,
or imply the answer to the question above, nor the figure's conclusion or takeaway. If a
visual element would give the answer away, describe its appearance and position without
naming what it demonstrates. Keep it under {max_words} words -- it is read aloud.
{extra}
For the `interpretive` field, give the normal full takeaway (it is not used here)."""


def _resolve_image(
    card: PlainCard, output_base: Path
) -> BinaryContent | ImageUrl | None:
    """Return vision content for a card's front image, or None if unusable."""
    raw = card.front.image_path
    if not raw:
        return None
    if raw.startswith("http"):
        return ImageUrl(url=raw)
    for cand in (output_base / raw, output_base.parent / raw, Path(raw)):
        if cand.exists() and cand.is_file():
            mime = "image/png" if cand.suffix.lower() == ".png" else "image/jpeg"
            return BinaryContent(data=cand.read_bytes(), media_type=mime)
    logger.warning(f"image-leak gate: image not found for card {card.card_id}: {raw}")
    return None


def _judge(card: PlainCard, spoken: str, model: str) -> ImageLeakVerdict:
    """Ask the judge whether ``spoken`` gives away this card's answer."""
    res = run_agent(
        image_leak_judge_agent,
        JUDGE_PROMPT.format(
            question=card.front.text, answer=card.back.text, spoken=spoken
        ),
        model=model,
        model_settings={"max_tokens": 2000},
        tier=GENERATION,
        label="image leak judge",
    )
    return res.output


def _rewrite(
    card: PlainCard, image: BinaryContent | ImageUrl, model: str, previous: str
) -> str:
    """Regenerate a question-aware description, told what leaked last time."""
    extra = ""
    if previous:
        extra = (
            f"\nA previous attempt was rejected for giving away: {previous}\n"
            "Do not repeat that.\n"
        )
    res = run_agent(
        image_description_agent,
        [REWRITE_PROMPT.format(question=card.front.text, extra=extra), image],
        model=model,
        model_settings={"max_tokens": 8000, "temperature": 0.3},
        tier=GENERATION,
        label="image leak rewrite",
    )
    desc: ImageDescription = res.output
    return desc.perceptual.strip()


def _process_card(
    card: PlainCard, model: str, output_base: Path, max_attempts: int
) -> ImageLeakAuditEntry:
    """Judge one card and rewrite its front description until it stops leaking."""
    original = card.front.image_summary_perceptual or card.front.image_summary or ""
    entry = dict(
        card_id=card.card_id,
        attempts=0,
        severity_before="none",
        severity_after="none",
        what_leaked="",
        reasoning="",
        original_description=original,
        final_description=original,
    )
    try:
        verdict = _judge(card, original, model)
    except Exception as e:  # judge unavailable -> fail open, card kept as-is
        logger.warning(f"image-leak judge failed for {card.card_id}: {e}")
        return ImageLeakAuditEntry(
            **{
                **entry,
                "verdict": "judge_failed",
                "reasoning": f"{type(e).__name__}: {e}",
            }
        )

    entry["severity_before"] = verdict.severity
    entry["what_leaked"] = verdict.what_leaks
    entry["reasoning"] = verdict.reasoning
    if not verdict.leaks:
        return ImageLeakAuditEntry(**{**entry, "verdict": "clean"})

    image = _resolve_image(card, output_base)
    if image is None:
        return ImageLeakAuditEntry(
            **{**entry, "verdict": "unresolved", "severity_after": verdict.severity}
        )

    spoken, leaked_what = original, verdict.what_leaks
    for attempt in range(1, max_attempts + 1):
        entry["attempts"] = attempt
        try:
            spoken = _rewrite(card, image, model, leaked_what)
            verdict = _judge(card, spoken, model)
        except Exception as e:
            logger.warning(f"image-leak rewrite failed for {card.card_id}: {e}")
            break
        entry["severity_after"] = verdict.severity
        entry["reasoning"] = verdict.reasoning
        if not verdict.leaks:
            card.front.image_summary_perceptual = spoken
            return ImageLeakAuditEntry(
                **{**entry, "verdict": "rewritten", "final_description": spoken}
            )
        leaked_what = verdict.what_leaks

    # Budget exhausted: keep the best attempt -- a still-imperfect description that
    # was written answer-blind beats the original, which the judge already rejected.
    card.front.image_summary_perceptual = spoken
    return ImageLeakAuditEntry(
        **{**entry, "verdict": "unresolved", "final_description": spoken}
    )


def run_image_leak_gate(
    cards: list[PlainCard],
    model: str,
    output_base: Path,
    max_workers: int = 8,
    max_attempts: int = 2,
) -> tuple[list[PlainCard], list[ImageLeakAuditEntry]]:
    """Judge and repair every front-image card's spoken description.

    Cards are never dropped: a card whose description cannot be made clean keeps
    its best answer-blind attempt and is recorded as ``unresolved`` for review.

    Args:
        cards: Cards to gate. Only those with a front image and a description
            are assessed; the rest pass through untouched.
        model: pydantic-ai model string for both judging and rewriting.
        output_base: Pipeline output directory, used to resolve relative images.
        max_workers: Concurrency bound for per-card model calls.
        max_attempts: Regeneration attempts before giving up on a leaky card.

    Returns:
        The same card list (descriptions repaired in place) and one audit entry
        per assessed card.
    """
    targets = [
        c
        for c in cards
        if c.front.image_path
        and (c.front.image_summary_perceptual or c.front.image_summary)
    ]
    if not targets:
        return cards, []

    logger.info(f"image-leak gate: assessing {len(targets)} front-image cards")
    audit: list[ImageLeakAuditEntry] = []
    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        futs = {
            ex.submit(_process_card, c, model, output_base, max_attempts): c
            for c in targets
        }
        for f in as_completed(futs):
            audit.append(f.result())

    leaked = sum(1 for a in audit if a.verdict in ("rewritten", "unresolved"))
    unresolved = sum(1 for a in audit if a.verdict == "unresolved")
    logger.info(
        f"image-leak gate: {len(audit)} assessed, {leaked} leaked, "
        f"{leaked - unresolved} repaired, {unresolved} unresolved"
    )
    return cards, audit


def write_audit(audit: list[ImageLeakAuditEntry], path: Path) -> None:
    """Write the per-card gate outcome to ``path`` as JSON."""
    import json

    payload = [a.model_dump() for a in audit]
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
