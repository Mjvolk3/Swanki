"""
scripts/run_mineru_swanki.py
[[scripts.run_mineru_swanki]]
https://github.com/Mjvolk3/Swanki/tree/main/scripts/run_mineru_swanki.py

MinerU OCR worker, run under the isolated `swanki-mineru` conda env (Python 3.11,
torch<2.11). Invoked as a subprocess by swanki/ocr/mineru.py. Stdlib-only at module
top so it imports cleanly under the isolated env without pulling swanki (3.13) deps.

Usage::

    python scripts/run_mineru_swanki.py \
        --pdf-path /abs/path/to/paper.pdf \
        --out-dir /abs/path/to/output_base/mineru-raw \
        --backend pipeline \
        --lang en \
        --method auto

Flattens MinerU's nested output tree ({scratch}/{stem}/auto/{stem}.md + siblings)
into a flat layout next to --out-dir. Exit codes: 0 ok, 2 PDF missing, 3 no md
produced, 4 HF_HOME underivable.
"""

# NOTE: HF_HOME must be on os.environ BEFORE `mineru.cli.common` is imported --
# MinerU reads the HF cache path at import time. The subprocess prologue
# (swanki/ocr/mineru.py) sets it; `_ensure_hf_home` re-asserts it with a
# $SWANKI_DATA fallback so manual invocations also work. The import is therefore
# deferred into main() and the import-at-top rule is waived for that one line.

import argparse
import os
import shutil
import sys
from pathlib import Path


def _parse_args() -> argparse.Namespace:
    """Parse CLI arguments for the MinerU worker."""
    parser = argparse.ArgumentParser(
        description="Run MinerU OCR on a PDF and flatten outputs next to --out-dir.",
    )
    parser.add_argument("--pdf-path", required=True, type=Path, help="Absolute path to input PDF")
    parser.add_argument("--out-dir", required=True, type=Path, help="Flat output directory")
    parser.add_argument(
        "--backend",
        default="pipeline",
        choices=["pipeline", "vlm-auto-engine", "hybrid-auto-engine"],
        help="MinerU parsing backend (default: pipeline)",
    )
    parser.add_argument("--lang", default="en", help="OCR language hint (default: en)")
    parser.add_argument(
        "--method",
        default="auto",
        choices=["auto", "txt", "ocr"],
        help="MinerU parse method (default: auto)",
    )
    return parser.parse_args()


def _find_first(root: Path, name: str) -> Path | None:
    """Return the first match for `name` under `root`, or None."""
    matches = list(root.rglob(name))
    return matches[0] if matches else None


def _ensure_hf_home() -> None:
    """Make sure HF_HOME is set before MinerU is imported.

    The subprocess prologue sets it explicitly. On a manual invocation that
    didn't, fall back to $SWANKI_DATA/models/mineru/hf_cache.
    """
    if "HF_HOME" in os.environ:
        Path(os.environ["HF_HOME"]).mkdir(parents=True, exist_ok=True)
        return
    data_root = os.environ.get("SWANKI_DATA")
    if not data_root:
        print(
            "ERROR: HF_HOME unset and SWANKI_DATA unset; cannot derive MinerU cache location",
            file=sys.stderr,
        )
        sys.exit(4)
    hf_home = Path(data_root) / "models" / "mineru" / "hf_cache"
    hf_home.mkdir(parents=True, exist_ok=True)
    os.environ["HF_HOME"] = str(hf_home)


def main() -> int:
    """Parse args, run MinerU do_parse, flatten outputs next to --out-dir."""
    args = _parse_args()
    pdf_path: Path = args.pdf_path.resolve()
    out_dir: Path = args.out_dir.resolve()
    stem = pdf_path.stem

    if not pdf_path.is_file():
        print(f"ERROR: PDF not found: {pdf_path}", file=sys.stderr)
        return 2

    out_dir.mkdir(parents=True, exist_ok=True)
    _ensure_hf_home()

    # MinerU import MUST come after HF_HOME setup (see module note).
    from mineru.cli.common import do_parse  # type: ignore[import-not-found]  # noqa: E402, I001, PLC0415

    scratch = out_dir / f".mineru_scratch_{stem}"
    scratch.mkdir(parents=True, exist_ok=True)

    pdf_bytes = pdf_path.read_bytes()
    do_parse(
        output_dir=str(scratch),
        pdf_file_names=[stem],
        pdf_bytes_list=[pdf_bytes],
        p_lang_list=[args.lang],
        backend=args.backend,
        parse_method=args.method,
    )

    md_src = _find_first(scratch, f"{stem}.md")
    if md_src is None:
        print(f"ERROR: MinerU produced no {stem}.md under {scratch}", file=sys.stderr)
        return 3

    auto_dir = md_src.parent
    content_list_src = auto_dir / f"{stem}_content_list.json"
    middle_json_src = auto_dir / f"{stem}_middle.json"
    images_src = auto_dir / "images"

    shutil.copy2(md_src, out_dir / f"{stem}.md")
    if content_list_src.exists():
        shutil.copy2(content_list_src, out_dir / f"{stem}_content_list.json")
    if middle_json_src.exists():
        shutil.copy2(middle_json_src, out_dir / f"{stem}_middle.json")
    # Keep the "images/" directory name (not "{stem}_images") so the relative
    # img_path in content_list.json ("images/xxx.jpg") resolves against out_dir
    # directly in swanki/ocr/mineru.py's splitter.
    if images_src.is_dir():
        dest_images = out_dir / "images"
        if dest_images.exists():
            shutil.rmtree(dest_images)
        shutil.copytree(images_src, dest_images)

    shutil.rmtree(scratch, ignore_errors=True)

    print(f"OK: {pdf_path.name} -> {out_dir}/{stem}.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
