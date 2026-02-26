"""Download PDFs from Zotero, cut references, and prepare for Swanki."""

import argparse
import os
import re
import subprocess
import warnings
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel
from PyPDF2 import PdfReader
from pyzotero import zotero

load_dotenv()

ZOTERO_API_KEY = os.environ["ZOTERO_API_KEY"]
ZOTERO_LIBRARY_ID = os.environ["ZOTERO_LIBRARY_ID"]

SWANKI_DATA = Path(__file__).resolve().parent.parent.parent / "Swanki_Data"
SWANKI_CUT = "/Users/michaelvolk/opt/miniconda3/envs/swanki/bin/swanki-cut"

REF_PATTERNS = re.compile(
    r"^(References|REFERENCES|Bibliography|BIBLIOGRAPHY|Literature Cited)\s*$"
)


class ZoteroConfig(BaseModel):
    """Zotero API connection config."""

    library_id: str
    api_key: str
    library_type: str = "user"


class DownloadResult(BaseModel):
    """Result of downloading PDFs for a citation key."""

    citation_key: str
    item_key: str
    pdf_paths: list[Path]


class PrepareResult(BaseModel):
    """Result of the full import+clean pipeline for one key."""

    citation_key: str
    total_pages: int
    refs_page: int | None
    kept_pages: int
    clean_pdf: Path
    sh_script: Path


def connect(config: ZoteroConfig) -> zotero.Zotero:
    """Create a Zotero API client."""
    return zotero.Zotero(config.library_id, config.library_type, config.api_key)


def citation_key_to_words(citation_key: str) -> list[str]:
    """Split a camelCase citation key into individual words.

    E.g. 'montanolopezPhysiological2022' -> ['montanolopez', 'Physiological', '2022']
    """
    s = re.sub(r"([a-z])([A-Z])", r"\1 \2", citation_key)
    s = re.sub(r"([a-zA-Z])(\d)", r"\1 \2", s)
    s = re.sub(r"(\d)([a-zA-Z])", r"\1 \2", s)
    return s.split()


def _match_citation_key(item: dict, citation_key: str) -> bool:
    """Check if a Zotero item matches a citation key."""
    data = item["data"]
    extra = data.get("extra", "")
    if f"Citation Key: {citation_key}" in extra:
        return True
    if data.get("citationKey") == citation_key:
        return True
    return False


def find_item_by_citation_key(zot: zotero.Zotero, citation_key: str) -> dict:
    """Find a Zotero item matching a citation key.

    Splits the camelCase key into words and searches with progressively
    fewer terms (Zotero API ANDs all terms). Filters client-side on
    BetterBibTeX `Citation Key:` in `extra` or Zotero 7 `citationKey`.
    Falls back to `qmode=everything`.
    """
    words = citation_key_to_words(citation_key)
    title_words = [w for w in words if w[0].isupper()]
    queries = []
    if title_words:
        queries.append(" ".join(title_words))
    queries.append(" ".join(words))
    if len(title_words) > 2:
        queries.append(" ".join(title_words[:2]))

    for query in queries:
        for qmode in (None, "everything"):
            kwargs = {"q": query}
            if qmode:
                kwargs["qmode"] = qmode
            items = zot.items(**kwargs)
            for item in items:
                if _match_citation_key(item, citation_key):
                    return item
    raise LookupError(f"No Zotero item found for citation key: {citation_key}")


def get_pdf_attachments(zot: zotero.Zotero, item_key: str) -> list[dict]:
    """Return PDF attachment items for a parent item."""
    children = zot.children(item_key)
    return [
        c
        for c in children
        if c["data"].get("contentType") == "application/pdf"
    ]


def download_pdfs(
    zot: zotero.Zotero, citation_key: str, output_dir: Path
) -> DownloadResult:
    """Download all PDFs for a citation key into output_dir."""
    item = find_item_by_citation_key(zot, citation_key)
    item_key = item["key"]
    attachments = get_pdf_attachments(zot, item_key)
    assert attachments, f"No PDF attachments found for {citation_key} ({item_key})"

    output_dir.mkdir(parents=True, exist_ok=True)
    pdf_paths: list[Path] = []

    for i, att in enumerate(attachments):
        if i == 0:
            filename = f"{citation_key}.pdf"
        else:
            filename = f"{citation_key}_si{i}.pdf"
        dest = output_dir / filename
        content = zot.file(att["key"])
        dest.write_bytes(content)
        pdf_paths.append(dest)
        print(f"  Downloaded: {dest}")

    return DownloadResult(
        citation_key=citation_key, item_key=item_key, pdf_paths=pdf_paths
    )


# --- PDF cleaning ---


def find_references_page(pdf_path: Path) -> tuple[int | None, int]:
    """Find the page containing a references heading. Returns (page_index, total)."""
    warnings.filterwarnings("ignore")
    reader = PdfReader(str(pdf_path), strict=False)
    total = len(reader.pages)
    for i, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        for line in text.split("\n"):
            if REF_PATTERNS.match(line.strip()):
                return i, total
    return None, total


def cut_pdf(input_pdf: Path, output_pdf: Path, start: int, end: int) -> None:
    """Cut a PDF using swanki-cut (0-based, end-exclusive)."""
    subprocess.run(
        [SWANKI_CUT, "-s", str(start), "-e", str(end), str(input_pdf), str(output_pdf)],
        check=True,
    )


def unite_pdfs(inputs: list[Path], output: Path) -> None:
    """Combine PDFs using pdfunite."""
    subprocess.run(
        ["pdfunite", *[str(p) for p in inputs], str(output)],
        check=True,
    )


def write_sh_script(output_dir: Path, citation_key: str) -> Path:
    """Write the swanki .sh runner script."""
    clean_pdf = output_dir / f"{citation_key}_clean.pdf"
    sh_path = output_dir / f"{citation_key}.sh"
    sh_path.write_text(
        f"#!/bin/bash\n\n"
        f"swanki pdf_path={clean_pdf} citation_key={citation_key} "
        f"+output_dir=../Swanki_Data/{citation_key}/{citation_key} "
        f"audio=full anki=auto_send "
        f"pipeline.processing.confirm_before_generation=false\n"
    )
    return sh_path


def clean_pdf(output_dir: Path, citation_key: str) -> PrepareResult:
    """Detect references, cut, unite, and write .sh script."""
    main_pdf = output_dir / f"{citation_key}.pdf"
    si_pdf = None
    for name in (f"{citation_key}_si.pdf", f"{citation_key}_SI.pdf", f"{citation_key}_si1.pdf"):
        candidate = output_dir / name
        if candidate.exists():
            si_pdf = candidate
            break

    # Detect references in main PDF
    refs_page, total = find_references_page(main_pdf)
    if refs_page is not None:
        keep_end = refs_page + 1
        print(f"  References detected at page {refs_page}, keeping pages 0:{keep_end} of {total}")
    else:
        keep_end = total
        print(f"  No references heading detected ({total} pages), keeping all pages")

    # Cut main PDF
    cut_pieces: list[Path] = []
    main_cut = output_dir / f"{citation_key}_cut.pdf"
    cut_pdf(main_pdf, main_cut, 0, keep_end)
    cut_pieces.append(main_cut)

    # Cut SI if present
    if si_pdf:
        si_refs, si_total = find_references_page(si_pdf)
        si_keep = (si_refs + 1) if si_refs is not None else si_total
        si_cut = output_dir / f"{citation_key}_si_cut.pdf"
        cut_pdf(si_pdf, si_cut, 0, si_keep)
        cut_pieces.append(si_cut)
        print(f"  SI: kept {si_keep} of {si_total} pages")

    # Unite into _clean.pdf
    clean_path = output_dir / f"{citation_key}_clean.pdf"
    unite_pdfs(cut_pieces, clean_path)
    print(f"  Created: {clean_path}")

    # Write .sh script
    sh_path = write_sh_script(output_dir, citation_key)
    print(f"  Created: {sh_path}")

    return PrepareResult(
        citation_key=citation_key,
        total_pages=total,
        refs_page=refs_page,
        kept_pages=keep_end,
        clean_pdf=clean_path,
        sh_script=sh_path,
    )


# --- CLI ---


def main():
    """CLI: download PDFs from Zotero, clean, and prepare for Swanki."""
    parser = argparse.ArgumentParser(
        description="Download PDFs from Zotero, cut references, prepare for Swanki"
    )
    parser.add_argument(
        "keys", nargs="+", help="One or more citation keys to import"
    )
    parser.add_argument(
        "--output-root",
        type=Path,
        default=SWANKI_DATA,
        help=f"Root directory for output (default: {SWANKI_DATA})",
    )
    parser.add_argument(
        "--download-only",
        action="store_true",
        help="Only download PDFs, skip cleaning",
    )
    args = parser.parse_args()

    config = ZoteroConfig(library_id=ZOTERO_LIBRARY_ID, api_key=ZOTERO_API_KEY)
    zot = connect(config)

    for key in args.keys:
        print(f"\n=== {key} ===")
        output_dir = args.output_root / key
        download_pdfs(zot, key, output_dir)

        if not args.download_only:
            result = clean_pdf(output_dir, key)
            print(
                f"  Summary: {result.kept_pages}/{result.total_pages} pages kept, "
                f"refs at page {result.refs_page}"
            )

    print(f"\nDone. Processed {len(args.keys)} paper(s).")


if __name__ == "__main__":
    main()
