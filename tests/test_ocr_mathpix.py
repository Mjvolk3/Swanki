"""
tests/test_ocr_mathpix.py
[[tests.test_ocr_mathpix]]

Mathpix per-page OCR tests (mpx invocation mocked).
"""

import subprocess
from pathlib import Path

import pytest

from swanki.ocr.mathpix import convert_pages_mathpix


def _make_pages(tmp_path: Path, n: int) -> list[Path]:
    pdf_dir = tmp_path / "pdf-singles"
    pdf_dir.mkdir()
    pages = []
    for i in range(1, n + 1):
        p = pdf_dir / f"page-{i}.pdf"
        p.write_bytes(b"%PDF-1.4")
        pages.append(p)
    return pages


def _fake_run_factory(tmp_path: Path, fail_stems: set[str]):
    md_dir = tmp_path / "md-singles"

    def fake_run(cmd, **kwargs):
        # cmd = ["script", "-qc", "mpx convert 'src' 'dst'", "/dev/null"]
        inner = cmd[2]
        dst = Path(inner.split("'")[-2])
        stem = dst.stem
        rc = 1 if stem in fail_stems else 0
        if rc == 0:
            md_dir.mkdir(parents=True, exist_ok=True)
            dst.write_text(f"# {stem}\n")
        return subprocess.CompletedProcess(cmd, rc, stdout="", stderr="boom" if rc else "")

    return fake_run


def test_mathpix_skips_failed_pages(tmp_path, monkeypatch):
    pages = _make_pages(tmp_path, 3)
    monkeypatch.setattr(
        subprocess, "run", _fake_run_factory(tmp_path, fail_stems={"page-2"})
    )
    result = convert_pages_mathpix(pages, tmp_path)
    names = [p.name for p in result]
    assert names == ["page-1.md", "page-3.md"]


def test_mathpix_raises_when_all_fail(tmp_path, monkeypatch):
    pages = _make_pages(tmp_path, 2)
    monkeypatch.setattr(
        subprocess, "run", _fake_run_factory(tmp_path, fail_stems={"page-1", "page-2"})
    )
    with pytest.raises(RuntimeError, match="Failed to convert any"):
        convert_pages_mathpix(pages, tmp_path)


def test_mathpix_natural_sort(tmp_path, monkeypatch):
    pages = _make_pages(tmp_path, 10)
    monkeypatch.setattr(subprocess, "run", _fake_run_factory(tmp_path, fail_stems=set()))
    result = convert_pages_mathpix(pages, tmp_path)
    names = [p.name for p in result]
    assert names.index("page-2.md") < names.index("page-10.md")
