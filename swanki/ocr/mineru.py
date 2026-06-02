"""
swanki/ocr/mineru.py
[[swanki.ocr.mineru]]
https://github.com/Mjvolk3/Swanki/tree/main/swanki/ocr/mineru.py
Test file: tests/test_ocr_mineru_split.py

MinerU OCR via an isolated subprocess (swanki-mineru conda env), then split the
flat content_list.json into per-page md-singles/page-N.md to match the Mathpix
contract. Fresh every run -- no idempotency short-circuit.
"""

import json
import logging
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

from pypdf import PdfReader

from swanki.processing.markdown_cleaner import _natural_sort_key

logger = logging.getLogger(__name__)

# content_list.json block types that are page noise, not card content.
# "discarded" is MinerU's own noise bucket (running heads, footers, reprint
# lines) -- confirmed against a real run; MinerU's flat .md omits these too.
_SKIP_TYPES = frozenset(
    {"discarded", "header", "footer", "page_number", "page_footnote", "aside_text"}
)


def _resolve_mineru_python(ocr_config: dict[str, Any]) -> str:
    """Resolve the ``swanki-mineru`` interpreter, machine-independently.

    Order: the configured ``python_bin`` if it exists on disk; else the
    ``swanki-mineru`` env sitting beside the running interpreter's conda env;
    else the configured path unchanged (so the subprocess fails with a clear
    path). This survives differing conda roots across machines -- e.g.
    ``~/miniconda3`` on gilahyper vs ``~/opt/miniconda3`` elsewhere -- without a
    per-run override.
    """
    configured: str = os.path.expanduser(
        ocr_config.get("python_bin", "~/opt/miniconda3/envs/swanki-mineru/bin/python")
    )
    if Path(configured).exists():
        return configured
    exe = Path(sys.executable).resolve()
    if "envs" in exe.parts:
        envs_dir = Path(*exe.parts[: exe.parts.index("envs") + 1])
        sibling = envs_dir / "swanki-mineru" / "bin" / "python"
        if sibling.exists():
            logger.info(
                "MinerU python_bin %s not found; using sibling env %s",
                configured,
                sibling,
            )
            return str(sibling)
    return configured


def convert_pdf_mineru(
    pdf_path: Path | None,
    output_base: Path,
    ocr_config: dict[str, Any],
) -> list[Path]:
    """Run MinerU on the whole PDF, then split output into per-page markdown.

    Args:
        pdf_path: Original source PDF (the per-page split is not used here).
        output_base: Pipeline output directory; writes md-singles/ and images/.
        ocr_config: The models.ocr config subtree (mineru knobs).

    Returns:
        Naturally-sorted list of per-page markdown paths (md-singles/page-N.md).

    Raises:
        RuntimeError: If pdf_path is None, SWANKI_DATA/hf_home is underivable,
            or the MinerU subprocess exits non-zero.
    """
    if pdf_path is None:
        raise RuntimeError("MinerU OCR requires source_pdf_path (unset on resume).")

    raw_dir = output_base / "mineru-raw"
    if raw_dir.exists():
        shutil.rmtree(raw_dir)  # fresh every run -- never reuse stale OCR
    raw_dir.mkdir(parents=True)

    hf_home_cfg = ocr_config.get("hf_home")
    if not hf_home_cfg and not os.getenv("SWANKI_DATA"):
        raise RuntimeError("Set SWANKI_DATA or models.ocr.hf_home for MinerU")
    hf_home = hf_home_cfg or f"{os.getenv('SWANKI_DATA', '')}/models/mineru/hf_cache"
    hf_home = os.path.expandvars(os.path.expanduser(hf_home))

    env = os.environ.copy()
    env.update(
        {
            "CUDA_VISIBLE_DEVICES": str(ocr_config.get("cuda_visible_devices", "3")),
            "HF_HOME": hf_home,
            "MINERU_MODEL_SOURCE": "huggingface",
            "MINERU_DEVICE_MODE": ocr_config.get("device_mode", "cuda"),
        }
    )

    python_bin = _resolve_mineru_python(ocr_config)
    runner = str(
        Path(__file__).resolve().parents[2]
        / ocr_config.get("runner", "scripts/run_mineru_swanki.py")
    )
    cmd = [
        python_bin,
        runner,
        "--pdf-path",
        str(pdf_path),
        "--out-dir",
        str(raw_dir),
        "--backend",
        ocr_config.get("backend", "pipeline"),
        "--lang",
        ocr_config.get("lang", "en"),
        "--method",
        ocr_config.get("method", "auto"),
    ]
    logger.info(f"Running MinerU on {pdf_path.name} (GPU {env['CUDA_VISIBLE_DEVICES']})")
    proc = subprocess.run(
        cmd, env=env, capture_output=True, text=True, timeout=ocr_config.get("timeout", 3600)
    )
    if proc.returncode != 0:
        raise RuntimeError(f"MinerU failed (exit {proc.returncode}): {proc.stderr[-2000:]}")

    stem = pdf_path.stem
    num_pages = len(PdfReader(str(pdf_path)).pages)
    pages = split_content_list_to_pages(
        raw_dir / f"{stem}_content_list.json", raw_dir, output_base, num_pages
    )
    logger.info(f"MinerU produced {len(pages)} page markdown files")
    return sorted(pages, key=_natural_sort_key)


def _render_block(block: dict[str, Any], raw_dir: Path, images_dir: Path) -> str | None:
    """Render one content_list block to markdown, or None if it should be skipped.

    Image blocks have their referenced file copied into images_dir so downstream
    image resolution (output_base/images/...) finds them.
    """
    btype = block.get("type")
    if btype in _SKIP_TYPES:
        return None

    if btype == "text":
        text = str(block.get("text", ""))
        level = block.get("text_level")
        if level:
            return "#" * int(level) + " " + text
        return text

    if btype == "equation":
        return str(block.get("text", ""))

    if btype == "image":
        img_path = block.get("img_path")
        if not img_path:
            return None
        name = Path(img_path).name
        src = raw_dir / img_path
        if src.exists():
            shutil.copy2(src, images_dir / name)
        caption = " ".join(block.get("image_caption", []) or [])
        md = f"![]({'images/' + name})"
        return f"{md}\n\n{caption}" if caption else md

    if btype == "table":
        caption = " ".join(block.get("table_caption", []) or [])
        body = str(block.get("table_body", ""))
        return f"{caption}\n\n{body}" if caption else body

    # Unknown / other types: emit any text we can, else skip.
    fallback = block.get("text")
    return str(fallback) if fallback else None


def split_content_list_to_pages(
    content_list_path: Path,
    raw_dir: Path,
    output_base: Path,
    num_pages: int,
) -> list[Path]:
    """Split MinerU's flat content_list.json into per-page markdown files.

    Groups blocks by page_idx and emits md-singles/page-N.md for every page in
    1..num_pages (empty file for pages with no content) so the per-page index
    stays contiguous and 1:1 with the source PDF -- downstream stages index
    these positionally.

    Args:
        content_list_path: Path to <stem>_content_list.json.
        raw_dir: MinerU flat output dir (holds images/ referenced by img_path).
        output_base: Pipeline output dir; writes md-singles/ and images/.
        num_pages: Authoritative source PDF page count.

    Returns:
        List of all written page markdown paths.
    """
    md_singles_dir = output_base / "md-singles"
    images_dir = output_base / "images"
    md_singles_dir.mkdir(parents=True, exist_ok=True)
    images_dir.mkdir(parents=True, exist_ok=True)

    blocks = json.loads(content_list_path.read_text())

    by_page: dict[int, list[str]] = {}
    for block in blocks:
        page_idx = int(block.get("page_idx", 0))
        rendered = _render_block(block, raw_dir, images_dir)
        if rendered is not None:
            by_page.setdefault(page_idx, []).append(rendered)

    page_files: list[Path] = []
    for n in range(1, num_pages + 1):
        content = "\n\n".join(by_page.get(n - 1, []))
        page_path = md_singles_dir / f"page-{n}.md"
        page_path.write_text(content)
        page_files.append(page_path)

    return page_files
