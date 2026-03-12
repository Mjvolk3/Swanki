"""Round-trip and constraint tests for Pydantic output models.

Validates that models used as LLM output types can be constructed,
serialized, and deserialized without errors, and that field constraints
catch invalid data before it wastes API tokens.
"""

import pytest
from pydantic import ValidationError

from swanki.models.cards import (
    AudioTranscriptFeedback,
    CardContent,
    CardFeedback,
    CardGenerationResponse,
    LectureTranscriptFeedback,
    PlainCard,
)
from swanki.models.document import DocumentSummary, ImageSummary

# ── Helpers ──────────────────────────────────────────────────────────────


def _make_summary_text(words: int = 200) -> str:
    return " ".join(["word"] * words)


def _make_card() -> PlainCard:
    return PlainCard(
        front=CardContent(text="What is X?"),
        back=CardContent(text="X is Y."),
        tags=["test"],
    )


# ── ImageSummary ─────────────────────────────────────────────────────────


class TestImageSummary:
    def test_round_trip(self) -> None:
        img = ImageSummary(
            page_idx=0,
            image_url="fig1.png",
            summary="A diagram of a neural network",
            alt_text="Neural network diagram",
            context="Section 3 discusses architectures.",
        )
        data = img.model_dump()
        rebuilt = ImageSummary(**data)
        assert rebuilt == img

    def test_extra_fields_forbidden(self) -> None:
        with pytest.raises(ValidationError, match="extra"):
            ImageSummary(
                page_idx=0,
                image_url="fig.png",
                summary="test",
                bogus_field="should fail",
            )

    def test_summary_too_long(self) -> None:
        with pytest.raises(ValidationError, match="too long"):
            ImageSummary(
                page_idx=0,
                image_url="fig.png",
                summary=_make_summary_text(301),
            )


# ── DocumentSummary ──────────────────────────────────────────────────────


class TestDocumentSummary:
    def test_round_trip(self) -> None:
        doc = DocumentSummary(
            title="Test Paper",
            authors=["Author A"],
            main_topic="Testing",
            key_contributions=["Contribution 1"],
            methodology="Experimental",
            summary=_make_summary_text(200),
        )
        data = doc.model_dump()
        rebuilt = DocumentSummary(**data)
        assert rebuilt == doc

    def test_summary_too_short(self) -> None:
        with pytest.raises(ValidationError, match="too short"):
            DocumentSummary(
                title="T",
                authors=["A"],
                main_topic="T",
                key_contributions=["C"],
                methodology="M",
                summary="Too short.",
            )

    def test_summary_too_long(self) -> None:
        with pytest.raises(ValidationError, match="too long"):
            DocumentSummary(
                title="T",
                authors=["A"],
                main_topic="T",
                key_contributions=["C"],
                methodology="M",
                summary=_make_summary_text(1501),
            )

    def test_too_many_contributions(self) -> None:
        with pytest.raises(ValidationError):
            DocumentSummary(
                title="T",
                authors=["A"],
                main_topic="T",
                key_contributions=["C1", "C2", "C3", "C4", "C5", "C6"],
                methodology="M",
                summary=_make_summary_text(200),
            )


# ── CardGenerationResponse ───────────────────────────────────────────────


class TestCardGenerationResponse:
    def test_round_trip(self) -> None:
        resp = CardGenerationResponse(cards=[_make_card()])
        data = resp.model_dump()
        rebuilt = CardGenerationResponse(**data)
        assert len(rebuilt.cards) == 1

    def test_empty_cards_rejected(self) -> None:
        with pytest.raises(ValidationError, match="at least one card"):
            CardGenerationResponse(cards=[])


# ── CardFeedback ─────────────────────────────────────────────────────────


class TestCardFeedback:
    def test_round_trip(self) -> None:
        fb = CardFeedback(feedback=["Issue 1"], done=False)
        data = fb.model_dump()
        rebuilt = CardFeedback(**data)
        assert rebuilt.done is False
        assert rebuilt.feedback == ["Issue 1"]

    def test_done_with_no_issues(self) -> None:
        fb = CardFeedback(feedback=[], done=True)
        assert fb.done is True


# ── AudioTranscriptFeedback ──────────────────────────────────────────────


class TestAudioTranscriptFeedback:
    def test_round_trip(self) -> None:
        fb = AudioTranscriptFeedback(feedback=[], done=True)
        data = fb.model_dump()
        rebuilt = AudioTranscriptFeedback(**data)
        assert rebuilt.done is True


# ── LectureTranscriptFeedback ────────────────────────────────────────────


class TestLectureTranscriptFeedback:
    def test_round_trip(self) -> None:
        fb = LectureTranscriptFeedback(
            feedback=[],
            done=True,
            word_count=500,
            meets_length_target=True,
            si_balance=True,
        )
        data = fb.model_dump()
        rebuilt = LectureTranscriptFeedback(**data)
        assert rebuilt.word_count == 500
        assert rebuilt.meets_length_target is True

    def test_si_balance_defaults_true(self) -> None:
        fb = LectureTranscriptFeedback(
            feedback=[], done=True, word_count=100, meets_length_target=True
        )
        assert fb.si_balance is True
