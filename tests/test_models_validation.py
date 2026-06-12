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
from swanki.models.document import DocumentSummary, ImageDescription, ImageSummary

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

    def test_perceptual_defaults_none_for_old_records(self) -> None:
        # Records serialized before the split have no `perceptual` key; they must
        # still deserialize (forward-only guarantee).
        old = {
            "page_idx": 0,
            "image_url": "fig.png",
            "summary": "A diagram of a neural network",
            "extracted_text": None,
            "alt_text": "",
            "context": "",
        }
        rebuilt = ImageSummary(**old)
        assert rebuilt.perceptual is None

    def test_perceptual_round_trip(self) -> None:
        img = ImageSummary(
            page_idx=0,
            image_url="fig.png",
            summary="Dark-field improves contrast without staining.",
            perceptual="Bright cell outlines against a black background.",
        )
        assert ImageSummary(**img.model_dump()) == img


# ── ImageDescription ─────────────────────────────────────────────────────


class TestImageDescription:
    def test_round_trip(self) -> None:
        desc = ImageDescription(
            perceptual="Bright cell outlines against a black background.",
            interpretive="Dark-field improves contrast without staining because "
            "cells scatter oblique light.",
        )
        assert ImageDescription(**desc.model_dump()) == desc
        assert desc.perceptual != desc.interpretive

    def test_both_fields_required(self) -> None:
        with pytest.raises(ValidationError):
            ImageDescription(perceptual="only what is visible")

    def test_extra_fields_forbidden(self) -> None:
        with pytest.raises(ValidationError, match="extra"):
            ImageDescription(
                perceptual="visible",
                interpretive="meaning",
                bogus="nope",
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


# ── PlainCard.user_feedback round-trip ───────────────────────────────────


class TestPlainCardUserFeedback:
    def test_default_is_empty_string(self) -> None:
        card = _make_card()
        assert card.user_feedback == ""

    def test_to_md_omits_marker_when_empty(self) -> None:
        md = _make_card().to_md()
        assert "<!-- user-feedback:" not in md

    def test_to_md_emits_marker_when_set(self) -> None:
        card = PlainCard(
            front=CardContent(text="What is X?"),
            back=CardContent(text="Y"),
            tags=["t"],
            user_feedback="answer feels rote",
        )
        md = card.to_md()
        assert "<!-- user-feedback: answer feels rote -->" in md
        # Marker precedes the tag line
        tag_idx = md.index("- #t")
        marker_idx = md.index("<!-- user-feedback:")
        assert marker_idx < tag_idx

    def test_extract_cards_round_trip(self) -> None:
        from swanki.processing.anki_processor import extract_cards

        card = PlainCard(
            front=CardContent(text="What is X?"),
            back=CardContent(text="Y is the answer"),
            tags=["t"],
            user_feedback="needs example",
        )
        md = card.to_md()
        parsed = extract_cards(md.splitlines())
        assert len(parsed) == 1
        assert parsed[0]["user_feedback"] == "needs example"
        # Marker is stripped from front/back content
        assert "user-feedback" not in parsed[0]["front"]
        assert "user-feedback" not in parsed[0]["back"]


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
