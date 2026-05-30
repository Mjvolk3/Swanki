"""
swanki/pipeline/glossary.py
[[swanki.pipeline.glossary]]
https://github.com/Mjvolk3/Swanki/tree/main/swanki/pipeline/glossary.py
Test file: tests/test_glossary.py

Glossary mode: LLM-assisted enumeration of definition units from OCR'd
markdown, a per-term card plan, batched definition-card generation, and a
hard-fail coverage audit. Used by mode=glossary (whole-document override). The
shape mirrors swanki.pipeline.problem_set (enumerate, plan, generate, audit)
minus the statement/solution pairing and reference resolution -- a glossary
term and its definition are co-located, so there is nothing to pair.
"""

import logging
from collections import Counter
from typing import Any

import yaml

from ..llm.agents import (
    definition_card_gen_agent,
    get_model_string,
    glossary_enumeration_agent,
)
from ..models.cards import PlainCard
from ..models.document import DocumentSummary
from ..models.glossary import (
    DefinitionCardBatchResponse,
    DefinitionCardPlan,
    GlossaryEnumerationResponse,
    GlossaryTag,
    GlossaryUnit,
    slugify_term,
)
from .problem_set import CoverageError

logger = logging.getLogger(__name__)


def enumerate_glossary(
    clean_md_files: list[Any], config: dict[str, Any]
) -> list[GlossaryUnit]:
    """LLM-assisted enumeration of definition units from cleaned markdown.

    Concatenates the per-page markdown and asks ``glossary_enumeration_agent``
    to return one ``GlossaryUnit`` per dictionary headword. LLM-assisted (not
    regex) because MinerU's per-page layout for a dense two-column wordlist is
    not regex-stable.

    Args:
        clean_md_files: Per-page cleaned markdown files.
        config: Hydra config dict (prompts + model selection).

    Returns:
        Enumerated GlossaryUnits with ``char_count`` populated.
    """
    full_text = "\n\n".join(f.read_text() for f in clean_md_files)
    g_prompts = config.get("prompts", {}).get("prompts", {}).get("glossary", {})
    system_prompt = g_prompts.get("definition_enumeration", "")
    models_config = config.get("models", {}).get("models", {}).get("llm", {})

    result = glossary_enumeration_agent.run_sync(
        full_text,
        instructions=system_prompt,
        model=get_model_string(models_config),
    )
    response: GlossaryEnumerationResponse = result.output
    for unit in response.units:
        unit.char_count = len(unit.term) + len(unit.definition)
    return response.units


def classify_definition_plan(
    unit: GlossaryUnit, glossary_cfg: dict[str, Any]
) -> DefinitionCardPlan:
    """Decide how many cards to emit for one glossary unit.

    v1: exactly one ``definition_main`` card per term regardless of length.
    ``long_entry_chars`` is the hook for the future elaboration upgrade
    (encyclopedia long entries); for GRE wordlists every entry is short and maps
    to a single card.

    Args:
        unit: The enumerated glossary unit.
        glossary_cfg: The ``pipeline.glossary`` config block.

    Returns:
        A DefinitionCardPlan (always one card in v1).
    """
    long_entry_chars = glossary_cfg.get("long_entry_chars", 600)
    if unit.char_count > long_entry_chars:
        logger.debug(
            "Term %r body %d chars exceeds long_entry_chars=%d; v1 still emits "
            "one card (elaboration deferred).",
            unit.term,
            unit.char_count,
            long_entry_chars,
        )
    return DefinitionCardPlan(n_cards=1, include_main=True)


def _format_definition_batch_prompt(
    units: list[GlossaryUnit],
    citation_key: str,
    generate_example: bool,
) -> str:
    """Build the user prompt for one batch of terms."""
    lines = [
        f"Generate EXACTLY {len(units)} cards -- one card per term below, in the "
        "same order as listed.",
        f"Citation key: {citation_key}",
        f"Include a usage example sentence on each back: {generate_example}",
        "",
        "Terms (number. term :: definition):",
    ]
    for i, unit in enumerate(units, start=1):
        lines.append(f"{i}. {unit.term} :: {unit.definition}")
    return "\n".join(lines)


def generate_cards_for_terms(
    units: list[GlossaryUnit],
    plans: list[DefinitionCardPlan],
    citation_key: str,
    config: dict[str, Any],
) -> list[PlainCard]:
    """Batched definition-card generation via definition_card_gen_agent.

    Each ``include_main`` unit yields one ``definition_main`` card. The card
    subtype and the canonical GlossaryTag are stamped from code AFTER the LLM
    call (the LLM defaults card_subtype to "regular" and does not know the tag
    scheme), and surplus cards beyond the batch's term count are dropped so
    every shipped card corresponds to an enumerated term. Count drift surfaces
    in the coverage audit.

    Args:
        units: Enumerated glossary units.
        plans: Per-unit card plans (1:1 with units).
        citation_key: Citation key for the tag and card prefix.
        config: Hydra config dict.

    Returns:
        Generated PlainCards, one per main unit.
    """
    main_units = [u for u, p in zip(units, plans, strict=True) if p.include_main]
    g_cfg = config.get("pipeline", {}).get("glossary", {})
    batch_size = g_cfg.get("batch_size", 25)
    generate_example = g_cfg.get("generate_example", True)
    g_prompts = config.get("prompts", {}).get("prompts", {}).get("glossary", {})
    system_prompt = g_prompts.get("definition_card_gen", "")
    models_config = config.get("models", {}).get("models", {}).get("llm", {})

    all_cards: list[PlainCard] = []
    for start in range(0, len(main_units), batch_size):
        batch = main_units[start : start + batch_size]
        user_prompt = _format_definition_batch_prompt(
            batch, citation_key, generate_example
        )
        result = definition_card_gen_agent.run_sync(
            user_prompt,
            instructions=system_prompt,
            model=get_model_string(models_config),
        )
        response: DefinitionCardBatchResponse = result.output

        # Pair returned cards to terms by order; stamp subtype + canonical tag;
        # drop any surplus cards so nothing untagged ships. The audit catches a
        # short return (missing term).
        for unit, card in zip(batch, response.cards, strict=False):
            card.card_subtype = "definition_main"  # type: ignore[assignment]
            tag = GlossaryTag(
                citation_key=citation_key, term_slug=slugify_term(unit.term)
            ).render()
            for required in ("vocabulary", "gre", tag):
                if required not in card.tags:
                    card.tags.append(required)
            all_cards.append(card)
    return all_cards


def audit_coverage(
    units: list[GlossaryUnit],
    cards: list[PlainCard],
    citation_key: str,
    *,
    strict: bool = True,
) -> None:
    """Hard-fail coverage audit: exactly one definition_main card per term.

    Keys on a parsed :class:`GlossaryTag` (term slug), counting via ``Counter``
    so it catches missing, duplicate, AND extra term slugs.

    Args:
        units: Enumerated glossary units.
        cards: Generated cards.
        citation_key: Citation key the tags are scoped to.
        strict: Raise on any discrepancy (default). When False, warn instead.

    Raises:
        CoverageError: If any term is missing, duplicated, or extra (strict).
    """
    enumerated = {slugify_term(u.term) for u in units}
    counts: Counter[str] = Counter()
    for card in cards:
        if card.card_subtype != "definition_main":
            continue
        for tag in card.tags:
            parsed = GlossaryTag.parse(tag, citation_key)
            if parsed is not None:
                counts[parsed.term_slug] += 1

    missing = {s for s in enumerated if counts[s] == 0}
    duplicated = {s for s in enumerated if counts[s] > 1}
    extra = set(counts) - enumerated
    if missing or duplicated or extra:
        if strict:
            raise CoverageError(missing=missing, extra=extra, duplicated=duplicated)
        logger.warning(
            "Glossary coverage discrepancy (non-strict): missing=%s duplicated=%s "
            "extra=%s",
            sorted(missing),
            sorted(duplicated),
            sorted(extra),
        )


def run_glossary_override(
    pipeline: Any,
    cleaned_files: list[Any],
    doc_summary: DocumentSummary,
    strict: bool = True,
) -> list[PlainCard]:
    """Whole-document glossary runner: enumerate, plan, generate, audit.

    Used by ``mode=glossary``. Persists ``glossary-units.yaml`` and
    ``cards-debug.yaml`` BEFORE the audit so a coverage failure preserves the
    generated definitions for inspection.

    Args:
        pipeline: The Pipeline instance (config + state + output_base + keys).
        cleaned_files: Per-page cleaned markdown for the whole document.
        doc_summary: DocumentSummary from the summary stage (unused for plain
            wordlists; kept for signature parity with the override contract).
        strict: Raise if zero terms are enumerated (default).

    Returns:
        The generated cards.
    """
    config = pipeline.config
    citation_key = pipeline.citation_key
    g_cfg = config.get("pipeline", {}).get("glossary", {})

    units = enumerate_glossary(cleaned_files, config)
    if not units:
        if strict:
            raise RuntimeError(
                "No glossary terms enumerated. Verify the input PDF is a "
                "wordlist/glossary and OCR produced readable markdown."
            )
        logger.warning("No glossary terms found; skipping glossary pipeline.")
        return []

    plans = [classify_definition_plan(unit, g_cfg) for unit in units]
    cards = generate_cards_for_terms(units, plans, citation_key, config)

    # Persist artifacts BEFORE the audit so a hard-fail preserves the evidence.
    output_base = pipeline.output_base
    units_path = output_base / "glossary-units.yaml"
    units_path.write_text(
        yaml.safe_dump([u.model_dump() for u in units], sort_keys=False)
    )
    logger.info(f"Wrote glossary units artifact: {units_path}")

    debug_path = output_base / "cards-debug.yaml"
    debug_path.write_text(
        yaml.safe_dump(
            {
                "n_units": len(units),
                "n_cards": len(cards),
                "subtype_counts": dict(Counter(c.card_subtype for c in cards)),
                "cards": [
                    {
                        "front": c.front.text[:200],
                        "back": c.back.text[:200],
                        "tags": list(c.tags),
                        "card_subtype": c.card_subtype,
                    }
                    for c in cards
                ],
            },
            sort_keys=False,
        )
    )
    logger.info(f"Wrote cards debug artifact: {debug_path}")

    audit_coverage(units, cards, citation_key, strict=strict)
    return cards
