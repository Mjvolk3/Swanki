
import argparse
import importlib.util
import json
import os
import re
import subprocess
import sys
import warnings
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel
from PyPDF2 import PdfReader
from pyzotero import zotero

# Import pdf_classifier directly to avoid triggering swanki/__init__.py
# (which pulls in Pipeline → instructor → anthropic, not available in base env)
_spec = importlib.util.spec_from_file_location(
    "pdf_classifier",
    Path(__file__).resolve().parent.parent / "swanki" / "utils" / "pdf_classifier.py",
)
_mod = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = _mod
_spec.loader.exec_module(_mod)
classify_pdf = _mod.classify_pdf

load_dotenv()

ZOTERO_API_KEY = os.environ["ZOTERO_API_KEY"]
ZOTERO_LIBRARY_ID = os.environ["ZOTERO_LIBRARY_ID"]

SWANKI_DATA = Path(__file__).resolve().parent.parent.parent / "Swanki_Data"
QPDF = "qpdf"

# Headings that mark the start of non-educational content (references,
# acknowledgments, etc.).  Cut pages matching these.
#
# NOTE: We omit short mid-page headings like "Author Information",
# "Author Contributions", "Competing Interests", "Notes" because
# journals often place these partway through a page that still has
# real content above.  The headings below reliably start a section
# that fills the rest of the page (and beyond) with non-educational text.
END_MATTER_PATTERNS = re.compile(
    r"^[■□▪▸►]?\s*("
    r"References|REFERENCES|Bibliography|BIBLIOGRAPHY|Literature Cited"
    r"|Acknowledg(?:e)?ments?|ACKNOWLEDG(?:E)?MENTS?"
    r"|Supporting Information|SUPPORTING INFORMATION"
    r"|Supplementary (?:Information|Materials?)|SUPPLEMENTARY (?:INFORMATION|MATERIALS?)"
    r"|Online [Cc]ontent"
    r"|Author [Cc]ontributions|AUTHOR CONTRIBUTIONS"
    r"|Declaration of [Ii]nterests?|DECLARATION OF INTERESTS?"
    r"|Competing [Ii]nterests?|COMPETING INTERESTS?"
    r")\s*$",
    re.IGNORECASE,
)

# Headings that resume educational content after a non-educational gap
# (e.g. Extended Data figures after references in Nature papers, STAR
# Methods + supplemental figures after references in Cell papers).
RESUME_EDUCATIONAL_PATTERNS = re.compile(
    r"^[■□▪▸►]?\s*("
    r"Extended Data"
    r"|STAR\s*[★✩]?\s*METHODS|STAR\s*[★✩]?\s*Methods|Star\s*Methods"
    r"|Supplemental [Ff]igures?"
    r"|Supplementary [Ff]igures?"
    r")\b",
    re.IGNORECASE,
)

# Headings that mark content to cut at the very end (reporting summaries,
# checklists appended by publishers).
TAIL_CUT_PATTERNS = re.compile(
    r"("
    r"nature\s+portfolio"
    r"|Reporting [Ss]ummary"
    r"|REPORTING SUMMARY"
    r")",
    re.IGNORECASE,
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
    keep_ranges: list[tuple[int, int]]  # 0-indexed [start, end)
    kept_pages: int
    clean_pdf: Path
    sh_script: Path
    used_llm: bool
    si_start_page: int | None = None


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


def _is_main_article(att: dict) -> bool:
    """Heuristic: return True if attachment looks like the main article PDF."""
    data = att["data"]
    title = (data.get("title") or "").lower()
    filename = (data.get("filename") or "").lower()
    # Zotero auto-imports typically title the main PDF "Full Text PDF"
    if "full text" in title:
        return True
    # SI/supplementary indicators in title or filename
    si_indicators = ("supplement", "si", "moesm", "esm", "supporting info")
    if any(s in title for s in si_indicators):
        return False
    if any(s in filename for s in si_indicators):
        return False
    return True


def get_pdf_attachments(zot: zotero.Zotero, item_key: str) -> list[dict]:
    """Return PDF attachment items for a parent item, main article first."""
    children = zot.children(item_key)
    pdfs = [c for c in children if c["data"].get("contentType") == "application/pdf"]
    # Sort so main article comes first, SI/supplementary after
    pdfs.sort(key=lambda a: (0 if _is_main_article(a) else 1))
    return pdfs


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


def _classify_pages_regex(pdf_path: Path) -> tuple[list[str], int]:
    """Classify each page as 'keep', 'cut', or 'resume' using regex.

    Returns (labels, total_pages) where labels[i] is the classification.
    """
    warnings.filterwarnings("ignore")
    reader = PdfReader(str(pdf_path), strict=False)
    total = len(reader.pages)
    labels = ["keep"] * total

    in_cut_zone = False
    for i, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        lines = [line.strip() for line in text.split("\n")]

        # Check if this page resumes educational content
        if in_cut_zone:
            for line in lines:
                if RESUME_EDUCATIONAL_PATTERNS.search(line):
                    in_cut_zone = False
                    break

        # Check if this page starts non-educational content
        if not in_cut_zone:
            for line in lines:
                if END_MATTER_PATTERNS.match(line):
                    in_cut_zone = True
                    break

        # Check if this page starts tail-end publisher content (always cut)
        for line in lines:
            if TAIL_CUT_PATTERNS.search(line):
                in_cut_zone = True
                break

        if in_cut_zone:
            labels[i] = "cut"

    return labels, total


def _labels_to_ranges(labels: list[str]) -> list[tuple[int, int]]:
    """Convert page labels to keep-ranges (0-based, end-exclusive)."""
    ranges: list[tuple[int, int]] = []
    start = None
    for i, label in enumerate(labels):
        if label == "keep":
            if start is None:
                start = i
        else:
            if start is not None:
                ranges.append((start, i))
                start = None
    if start is not None:
        ranges.append((start, len(labels)))
    return ranges


def cut_pdf(input_pdf: Path, output_pdf: Path, start: int, end: int) -> None:
    """Cut a PDF using qpdf (0-based start, end-exclusive)."""
    # qpdf uses 1-based inclusive page ranges
    # Exit code 3 = warnings (e.g. minor PDF structural issues) but success
    result = subprocess.run(
        [QPDF, str(input_pdf), "--pages", ".", f"{start + 1}-{end}", "--", str(output_pdf)],
    )
    if result.returncode not in (0, 3):
        result.check_returncode()


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
        f"audio=all anki=default "
        f"pipeline.processing.confirm_before_generation=false\n"
    )
    return sh_path


def _get_keep_ranges_llm(pdf_path: Path) -> tuple[list[tuple[int, int]], int]:
    """Use LLM classifier to get keep-ranges. Returns (keep_ranges, total_pages)."""
    plan = classify_pdf(pdf_path)
    total = len(plan.pages)
    print(f"  LLM classification:")
    for p in plan.pages:
        status = "KEEP" if p.keep else "CUT"
        print(f"    Page {p.page}: {p.label} [{status}]")
    return plan.keep_ranges, total


def _get_keep_ranges_regex(pdf_path: Path) -> tuple[list[tuple[int, int]], int]:
    """Use regex fallback to get keep-ranges. Returns (keep_ranges, total_pages)."""
    labels, total = _classify_pages_regex(pdf_path)
    ranges = _labels_to_ranges(labels)

    cut_pages = [i + 1 for i, l in enumerate(labels) if l == "cut"]
    if cut_pages:
        ranges_str = ", ".join(f"{s+1}-{e}" for s, e in ranges)
        print(f"  Regex fallback: keeping [{ranges_str}], cutting pages {cut_pages}")
    else:
        print(f"  Regex fallback: no end-matter detected, keeping all {total} pages")

    return ranges, total


def _get_keep_ranges(pdf_path: Path) -> tuple[list[tuple[int, int]], int, bool]:
    """Get keep-ranges via LLM (preferred) or regex fallback.

    Returns (keep_ranges, total_pages, used_llm).
    """
    if os.environ.get("OPENAI_API_KEY"):
        try:
            ranges, total = _get_keep_ranges_llm(pdf_path)
            return ranges, total, True
        except ImportError as e:
            print(f"  LLM classifier unavailable ({e}), using regex fallback")
    else:
        print("  OPENAI_API_KEY not set, using regex fallback")
    ranges, total = _get_keep_ranges_regex(pdf_path)
    return ranges, total, False


def clean_pdf(output_dir: Path, citation_key: str) -> PrepareResult:
    """Classify pages, cut keep-ranges, unite, and write .sh script."""
    main_pdf = output_dir / f"{citation_key}.pdf"
    si_pdf = None
    for name in (f"{citation_key}_si.pdf", f"{citation_key}_SI.pdf", f"{citation_key}_si1.pdf"):
        candidate = output_dir / name
        if candidate.exists():
            si_pdf = candidate
            break

    keep_ranges, total, used_llm = _get_keep_ranges(main_pdf)

    # Cut each keep-range from the main PDF
    cut_pieces: list[Path] = []
    for i, (start, end) in enumerate(keep_ranges):
        piece = output_dir / f"{citation_key}_range{i}.pdf"
        cut_pdf(main_pdf, piece, start, end)
        cut_pieces.append(piece)
        print(f"  Keep range: pages {start + 1}-{end} of {total}")

    kept_pages = sum(end - start for start, end in keep_ranges)
    si_start_page: int | None = None

    # Cut SI if present
    if si_pdf:
        si_start_page = kept_pages
        si_ranges, si_total, _ = _get_keep_ranges(si_pdf)
        for i, (start, end) in enumerate(si_ranges):
            piece = output_dir / f"{citation_key}_si_range{i}.pdf"
            cut_pdf(si_pdf, piece, start, end)
            cut_pieces.append(piece)
        si_kept = sum(end - start for start, end in si_ranges)
        print(f"  SI: kept {si_kept} of {si_total} pages")

    # Unite into _clean.pdf
    clean_path = output_dir / f"{citation_key}_clean.pdf"
    unite_pdfs(cut_pieces, clean_path)
    print(f"  Created: {clean_path}")

    # Write .sh script
    sh_path = write_sh_script(output_dir, citation_key)
    print(f"  Created: {sh_path}")

    # Write _meta.json with SI boundary info
    meta_path = output_dir / f"{citation_key}_meta.json"
    meta_path.write_text(json.dumps({"si_start_page": si_start_page}, indent=2))
    print(f"  Created: {meta_path}")

    return PrepareResult(
        citation_key=citation_key,
        total_pages=total,
        keep_ranges=keep_ranges,
        kept_pages=kept_pages,
        clean_pdf=clean_path,
        sh_script=sh_path,
        used_llm=used_llm,
        si_start_page=si_start_page,
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
            method = "LLM" if result.used_llm else "regex"
            ranges_str = ", ".join(f"{s+1}-{e}" for s, e in result.keep_ranges)
            print(
                f"  Summary: {result.kept_pages}/{result.total_pages} pages kept "
                f"({method}), ranges: [{ranges_str}]"
            )

    print(f"\nDone. Processed {len(args.keys)} paper(s).")


if __name__ == "__main__":
    main()
