"""
tests/test_ocr_dispatch.py
[[tests.test_ocr_dispatch]]

OCR provider dispatch routing tests.
"""

from pathlib import Path

import pytest

import swanki.ocr as ocr


def test_dispatch_mathpix_routes_to_mathpix(monkeypatch):
    calls = {}

    def fake_mathpix(pages, output_base):
        calls["mathpix"] = (pages, output_base)
        return [Path("md-singles/page-1.md")]

    monkeypatch.setattr(ocr, "convert_pages_mathpix", fake_mathpix)
    result = ocr.convert_to_markdown(
        "mathpix",
        pages=[Path("pdf-singles/page-1.pdf")],
        pdf_path=Path("paper.pdf"),
        output_base=Path("/out"),
        ocr_config={},
    )
    assert result == [Path("md-singles/page-1.md")]
    assert calls["mathpix"] == ([Path("pdf-singles/page-1.pdf")], Path("/out"))


def test_dispatch_mineru_routes_to_mineru(monkeypatch):
    calls = {}

    def fake_mineru(pdf_path, output_base, ocr_config):
        calls["mineru"] = (pdf_path, output_base, ocr_config)
        return [Path("md-singles/page-1.md")]

    monkeypatch.setattr(ocr, "convert_pdf_mineru", fake_mineru)
    result = ocr.convert_to_markdown(
        "mineru",
        pages=[],
        pdf_path=Path("paper.pdf"),
        output_base=Path("/out"),
        ocr_config={"provider": "mineru"},
    )
    assert result == [Path("md-singles/page-1.md")]
    assert calls["mineru"] == (Path("paper.pdf"), Path("/out"), {"provider": "mineru"})


def test_dispatch_unknown_provider_raises():
    with pytest.raises(ValueError, match="Unknown OCR provider"):
        ocr.convert_to_markdown(
            "paddle",
            pages=[],
            pdf_path=None,
            output_base=Path("/out"),
            ocr_config={},
        )
