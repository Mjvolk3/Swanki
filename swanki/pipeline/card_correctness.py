"""
swanki/pipeline/card_correctness.py
[[swanki.pipeline.card_correctness]]
https://github.com/Mjvolk3/Swanki/tree/main/swanki/pipeline/card_correctness.py
Test file: tests/test_card_correctness.py

Post-generation LLM correctness gate. Each generated card is assessed against
its source context and the document summary by the configured model; correct
cards pass, clearly-fixable cards are repaired in place, and unfixable cards are
quarantined out of the deck. Every verdict is logged to
``<output_base>/correctness-assessment.yaml`` so the deck is auditable. A card
the gate cannot assess (agent error or exhausted safety retries) is kept
fail-open and logged as ``assessment_failed`` -- the gate never silently drops
an unjudged card.
"""

from __future__ import annotations

import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import yaml

from ..llm.agents import card_correctness_agent
from ..llm.safety import with_safety_retry
from ..models.cards import CardAuditEntry, CardCorrectnessAssessment, PlainCard
from ..models.document import DocumentSummary

logger = logging.getLogger(__name__)


GATE_INSTRUCTIONS: str = (
    "You are a meticulous subject-matter fact-checker for spaced-repetition "
    "flashcards. You are given the SOURCE TEXT a card was generated from, a "
    "DOCUMENT SUMMARY for context, and one FLASHCARD with a front (prompt) and "
    "back (answer). Decide whether the card teaches correct, unambiguous "
    "information.\n\n"
    "Return one verdict:\n"
    "- 'pass': the card is factually correct and unambiguous as written.\n"
    "- 'fixed': the card contains a real error (a factual mistake, a wrong "
    "answer, internally contradictory or nonsensical answer options, or a "
    "question whose premise is false) AND the correct version is clear. Supply "
    "corrected_front and/or corrected_back with the minimal change that makes "
    "it correct. Preserve the card's format: multiple-choice stays "
    "multiple-choice, cloze deletions stay cloze, a definition stays a "
    "definition.\n"
    "- 'dropped': the card is wrong and you cannot determine a clearly-correct "
    "version (e.g. every multiple-choice option is wrong, or the prompt is "
    "irreparably ambiguous).\n\n"
    "Critical: a card may be a FAITHFUL transcription of the source and still "
    "be wrong, because the source itself can contain errors. Judge correctness "
    "against established reality, not mere fidelity to the source. Do not drop "
    "or fix a card merely because it is terse or stylistically plain -- only "
    "act on genuine correctness problems. Always give a concise reason."
)


def _summary_context(summary: DocumentSummary) -> str:
    """Build a compact document-context block for the assessment prompt."""
    return (
        f"Title: {summary.title}\n"
        f"Main topic: {summary.main_topic}\n"
        f"Summary: {summary.summary}"
    )


def _card_block(card: PlainCard) -> str:
    """Render a card's front/back (and image summaries) for the prompt."""
    lines = [
        f"Subtype: {card.card_subtype}",
        f"Front: {card.front.text}",
        f"Back: {card.back.text}",
    ]
    if card.front.image_summary:
        lines.append(f"Front image summary: {card.front.image_summary}")
    if card.back.image_summary:
        lines.append(f"Back image summary: {card.back.image_summary}")
    return "\n".join(lines)


def _build_prompt(
    card: PlainCard, source_context: str, summary: DocumentSummary
) -> str:
    """Assemble the per-card correctness-assessment prompt."""
    return (
        "DOCUMENT SUMMARY\n"
        f"{_summary_context(summary)}\n\n"
        "SOURCE TEXT\n"
        f"{source_context}\n\n"
        "FLASHCARD\n"
        f"{_card_block(card)}"
    )


def _assess_card(
    card: PlainCard,
    source_context: str,
    summary: DocumentSummary,
    model_string: str,
) -> CardCorrectnessAssessment | None:
    """Assess one card.

    Returns:
        The agent's :class:`CardCorrectnessAssessment`, or ``None`` if the call
        failed after safety retries -- the caller treats ``None`` as
        ``assessment_failed`` and keeps the card (fail-open).
    """
    prompt = _build_prompt(card, source_context, summary)
    try:
        result = with_safety_retry(
            card_correctness_agent,
            prompt,
            instructions=GATE_INSTRUCTIONS,
            model=model_string,
            label=f"correctness {card.card_id}",
        )
    except Exception as e:
        logger.error(
            "correctness gate could not assess card %s: %s; keeping fail-open",
            card.card_id,
            e,
        )
        return None
    return result.output


def _apply_assessment(
    card: PlainCard, assessment: CardCorrectnessAssessment | None
) -> tuple[PlainCard | None, CardAuditEntry]:
    """Resolve a card against its assessment into (kept_card, audit_entry).

    ``kept_card`` is ``None`` only for a ``dropped`` verdict. A ``fixed`` card
    is returned as a copy with corrected front/back text; ``pass`` and
    ``assessment_failed`` return the card unchanged.
    """
    card_id = card.card_id or ""
    if assessment is None:
        entry = CardAuditEntry(
            card_id=card_id,
            card_subtype=card.card_subtype,
            verdict="assessment_failed",
            reason="assessment call failed after retries; kept fail-open",
            original_front=card.front.text,
            original_back=card.back.text,
        )
        return card, entry

    if assessment.verdict == "dropped":
        entry = CardAuditEntry(
            card_id=card_id,
            card_subtype=card.card_subtype,
            verdict="dropped",
            reason=assessment.reason,
            original_front=card.front.text,
            original_back=card.back.text,
        )
        return None, entry

    if assessment.verdict == "fixed":
        new_front = (
            card.front.model_copy(update={"text": assessment.corrected_front})
            if assessment.corrected_front
            else card.front
        )
        new_back = (
            card.back.model_copy(update={"text": assessment.corrected_back})
            if assessment.corrected_back
            else card.back
        )
        fixed = card.model_copy(update={"front": new_front, "back": new_back})
        entry = CardAuditEntry(
            card_id=card_id,
            card_subtype=card.card_subtype,
            verdict="fixed",
            reason=assessment.reason,
            original_front=card.front.text,
            original_back=card.back.text,
            corrected_front=new_front.text,
            corrected_back=new_back.text,
        )
        return fixed, entry

    entry = CardAuditEntry(
        card_id=card_id,
        card_subtype=card.card_subtype,
        verdict="pass",
        reason=assessment.reason,
        original_front=card.front.text,
        original_back=card.back.text,
    )
    return card, entry


def run_correctness_gate(
    cards: list[PlainCard],
    doc_summary: DocumentSummary,
    source_context: str,
    model_string: str,
    *,
    max_workers: int = 8,
) -> tuple[list[PlainCard], list[CardAuditEntry]]:
    """Assess every card concurrently and return (kept_cards, audit).

    Each card is judged independently by ``model_string`` against
    ``source_context`` and ``doc_summary``. Passed and fail-open cards are kept
    unchanged, fixed cards are kept with corrected text, dropped cards are
    excluded. The audit has exactly one entry per input card, in input order.

    Args:
        cards: Generated cards to assess.
        doc_summary: Document summary supplying topical context.
        source_context: Cleaned source text the cards were generated from.
        model_string: Resolved pydantic-ai model string (e.g.
            ``"openai:gpt-5.5"``).
        max_workers: Concurrency bound for per-card assessment calls.

    Returns:
        A tuple of the kept-card list (drives every downstream writer) and the
        per-card audit-entry list.
    """
    if not cards:
        return [], []

    assessments: list[CardCorrectnessAssessment | None] = [None] * len(cards)
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_index = {
            executor.submit(
                _assess_card, card, source_context, doc_summary, model_string
            ): i
            for i, card in enumerate(cards)
        }
        for future in as_completed(future_to_index):
            assessments[future_to_index[future]] = future.result()

    kept: list[PlainCard] = []
    audit: list[CardAuditEntry] = []
    for card, assessment in zip(cards, assessments):
        kept_card, entry = _apply_assessment(card, assessment)
        audit.append(entry)
        if kept_card is not None:
            kept.append(kept_card)

    counts = {
        "total": len(audit),
        "kept": len(kept),
        "passed": sum(1 for e in audit if e.verdict == "pass"),
        "fixed": sum(1 for e in audit if e.verdict == "fixed"),
        "dropped": sum(1 for e in audit if e.verdict == "dropped"),
        "assessment_failed": sum(
            1 for e in audit if e.verdict == "assessment_failed"
        ),
    }
    logger.info(
        "correctness gate: %d cards -> %d kept (%d pass, %d fixed, "
        "%d assessment_failed), %d dropped",
        counts["total"],
        counts["kept"],
        counts["passed"],
        counts["fixed"],
        counts["assessment_failed"],
        counts["dropped"],
    )
    return kept, audit


def write_audit(audit: list[CardAuditEntry], path: Path) -> None:
    """Write gate decisions to ``path`` atomically (temp file then rename).

    The payload is a ``summary`` count block plus one ``cards`` entry per
    assessed card. A crashed run never leaves a half-written audit.
    """
    payload = {
        "summary": {
            "total": len(audit),
            "passed": sum(1 for e in audit if e.verdict == "pass"),
            "fixed": sum(1 for e in audit if e.verdict == "fixed"),
            "dropped": sum(1 for e in audit if e.verdict == "dropped"),
            "assessment_failed": sum(
                1 for e in audit if e.verdict == "assessment_failed"
            ),
        },
        "cards": [entry.model_dump() for entry in audit],
    }
    tmp = path.with_suffix(path.suffix + ".tmp")
    with open(tmp, "w") as f:
        yaml.safe_dump(payload, f, sort_keys=False, allow_unicode=True)
    tmp.rename(path)
