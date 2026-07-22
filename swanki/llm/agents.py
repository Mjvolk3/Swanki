"""
swanki/llm/agents.py
[[swanki.llm.agents]]
https://github.com/Mjvolk3/Swanki/tree/main/swanki/llm/agents.py

Centralized pydantic-ai agent registry — one agent per output type.
"""

from pydantic_ai import Agent

from ..models.cards import (
    AudioTranscriptFeedback,
    CardCorrectnessAssessment,
    CardFeedback,
    CardGenerationResponse,
    ChunkEditResponse,
    LectureFactualAssessment,
    LectureTranscriptFeedback,
)
from ..models.document import DocumentSummary, ImageDescription
from ..models.glossary import (
    DefinitionCardBatchResponse,
    GlossaryEnumerationResponse,
)
from ..models.problem_set import (
    CardPlanResponse,
    ProblemCardBatchResponse,
    ProblemEnumerationResponse,
    ProblemPairingResponse,
)
from ..models.sections import ClassificationResult

# ── Structured-output agents ───────────────────────────────────────────
document_summary_agent: Agent[None, DocumentSummary] = Agent(
    output_type=DocumentSummary, retries=3
)
card_gen_agent: Agent[None, CardGenerationResponse] = Agent(
    output_type=CardGenerationResponse, retries=3
)
card_feedback_agent: Agent[None, CardFeedback] = Agent(
    output_type=CardFeedback, retries=2
)
audio_feedback_agent: Agent[None, AudioTranscriptFeedback] = Agent(
    output_type=AudioTranscriptFeedback, retries=2
)
lecture_critic_agent: Agent[None, LectureTranscriptFeedback] = Agent(
    output_type=LectureTranscriptFeedback, retries=3
)
chunk_edit_agent: Agent[None, ChunkEditResponse] = Agent(
    output_type=ChunkEditResponse, retries=2
)
card_correctness_agent: Agent[None, CardCorrectnessAssessment] = Agent(
    output_type=CardCorrectnessAssessment, retries=3
)
lecture_factual_agent: Agent[None, LectureFactualAssessment] = Agent(
    output_type=LectureFactualAssessment, retries=3
)
image_description_agent: Agent[None, ImageDescription] = Agent(
    output_type=ImageDescription, retries=3
)

# ── Solution-manual mode agents ────────────────────────────────────────
section_classifier_agent: Agent[None, ClassificationResult] = Agent(
    output_type=ClassificationResult, retries=2
)
problem_enumeration_agent: Agent[None, ProblemEnumerationResponse] = Agent(
    output_type=ProblemEnumerationResponse, retries=3
)
problem_pairing_agent: Agent[None, ProblemPairingResponse] = Agent(
    output_type=ProblemPairingResponse, retries=2
)
card_plan_classifier_agent: Agent[None, CardPlanResponse] = Agent(
    output_type=CardPlanResponse, retries=2
)
problem_card_gen_agent: Agent[None, ProblemCardBatchResponse] = Agent(
    output_type=ProblemCardBatchResponse, retries=3
)

# ── Glossary mode agents ───────────────────────────────────────────────
glossary_enumeration_agent: Agent[None, GlossaryEnumerationResponse] = Agent(
    output_type=GlossaryEnumerationResponse, retries=3
)
definition_card_gen_agent: Agent[None, DefinitionCardBatchResponse] = Agent(
    output_type=DefinitionCardBatchResponse, retries=3
)

# ── Raw-text agent (shared across all plain-text calls) ───────────────
text_agent: Agent[None, str] = Agent(output_type=str, retries=3)


def get_model_string(config: dict[str, str]) -> str:
    """Build a pydantic-ai model string from Hydra config.

    Args:
        config: Dict with optional 'provider' and 'model' keys.

    Returns:
        Model string like ``"openai:gpt-4"`` or ``"anthropic:claude-..."``.
    """
    provider = config.get("provider", "openai")
    model = config.get("model", "gpt-4")
    return f"{provider}:{model}"
