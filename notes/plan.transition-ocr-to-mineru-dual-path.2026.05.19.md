---
id: y1tumqecayoqw3mvc4tbt0e
title: '19'
desc: ''
updated: 1779233798920
created: 1779233798920
---

Plan: Transition OCR to MinerU (Dual-Path with Mathpix)

## Context

Swanki's OCR layer is currently Mathpix-only. The live path is `Pipeline.convert_to_markdown()` (`swanki/pipeline/pipeline.py:594-659`), which splits the PDF into per-page PDFs (`pdf-singles/page-N.pdf`) and shells out `mpx convert` once per page via `os.system`, producing `md-singles/page-N.md`. Mathpix is a paid cloud service (`$0.01-0.05`/page) and emits inconsistent markdown (CDN image URLs vs LaTeX `\includegraphics` blocks -- see `swanki/processing/markdown_cleaner.py` 2026-01-17 note), which forces downstream cleanup branching and audio-layer scrubbing (`swanki/audio/_common.py` LATEX prompt, `swanki/audio/reading.py` "mathpix link" ban).

We want to add MinerU as a second, GPU-local, zero-cost OCR backend while keeping Mathpix available, because Mathpix remains superior for handwriting (relevant to Bishop-style handwritten worked-solution PDFs in solution-manual mode). MinerU emits local relative image paths (no CDN), which removes a class of downstream artifacts. The sibling project iBioFoundry-AI already runs MinerU 2.x in production; its `ibiofoundry_ai/tools/_ocr_backend.py` and `ibiofoundry_ai/_runners/run_mineru.py` are the reference implementation we adapt here.

No related GitHub issues exist; all prior planning lives in `notes/plan.open-source-pipeline-mineru-ocr-gemma-4-llm.2026.04.15.md` (broader Mathpix+OpenAI replacement; its `magic_pdf` API references are STALE -- MinerU 2.x uses `from mineru.cli.common import do_parse`). This plan supersedes that note's OCR section, scoped to OCR-only and dual-path.

## Operator Directives (from 2026-05-21)

1. **OCR fresh every time.** Do NOT port iBioFoundry-AI's `md_is_fresh` idempotency short-circuit (`_ocr_backend.py:204`). The MinerU path re-OCRs on every run until MinerU output proves stable and consistent. Matches current Mathpix behavior.
2. **Free one GPU for MinerU.** gilahyper has 4x RTX 6000 Ada; all four are pinned by Fish Speech docker containers (`device=0..3` -> ports `8080..8083`). Stop the `device=3`/`8083` container and pin MinerU to GPU 3 via `CUDA_VISIBLE_DEVICES=3`. Swanki's Fish discovery (`swanki/audio/_common.py:593`) must stop assuming 4 servers.
3. **Track the dependency in pyproject + env.** MinerU 2.x supports Python 3.13 on Linux, but `mineru[pipeline]` drags torch+torchvision+paddleocr (multi-GB). Swanki publishes to PyPI (`upload_to_pypi = true`), so MinerU MUST NOT enter core `dependencies`. It goes in an isolated `swanki-mineru` conda env (Python 3.11, mirroring iBioFoundry-AI) invoked via subprocess, plus an optional-dependencies marker for discoverability.

## Approach

**Dual-path via a `models.ocr.provider` switch**, mirroring the existing TTS provider switch (`pipeline.py:1999-2057`, which branches `if tts_provider == "fish_speech"`). No Protocol/factory machinery -- Swanki's convention is string-branch dispatch on a config key. A new `ocr:` subtree is added to `swanki/conf/models/*.yaml` alongside `llm:` and `tts:`. Default `provider: mathpix` so existing behavior is preserved; MinerU is opt-in.

**Isolated env + subprocess for MinerU.** MinerU runs under `~/opt/miniconda3/envs/swanki-mineru/bin/python` (Python 3.11, torch<2.11). Swanki (Python 3.13) invokes it through a thin stdlib-only runner `scripts/run_mineru_swanki.py` (adapted from iBioFoundry-AI's `run_mineru.py`). The subprocess boundary cleanly solves three problems at once: CUDA-runtime isolation, GPU pinning (`CUDA_VISIBLE_DEVICES=3`), and the HF_HOME-before-import ordering gotcha (MinerU reads the HF cache path at import time).

**Preserve the `md-singles/page-N.md` contract.** Page-level markdown is load-bearing downstream (section_classifier page labels, segmenter page-offset map, problem_set partitioner, per-page image-card placement at `pipeline.py:382-393`). MinerU emits ONE flat `<stem>.md` plus `<stem>_content_list.json` (block-level reading order, each block carrying a `page_idx`). The MinerU path OCRs the whole original PDF once (one model load, fast) then splits the output into `md-singles/page-N.md` by grouping `content_list.json` blocks on `page_idx`. This keeps every downstream consumer unchanged.

**Why whole-PDF, not per-page, for MinerU.** Feeding the already-split `pdf-singles/page-N.pdf` to MinerU one-at-a-time would reload the model per page (seconds each) -- prohibitively slow. Mathpix per-page is cheap because it is a network call; MinerU per-page is not. So the MinerU branch ignores the `pages` argument and consumes the original PDF.

## File Specifications

Implementation order respects dependencies: runner script -> ocr package -> pipeline wiring -> config -> deps/env -> GPU helper -> tests.

### `scripts/run_mineru_swanki.py` (NEW)

**Purpose:** Stdlib-only MinerU worker, run under the `swanki-mineru` conda env. Adapted from `/home/michaelvolk/Documents/projects/iBioFoundry-AI/ibiofoundry_ai/_runners/run_mineru.py`. Lives outside the `swanki` package so it imports cleanly under Python 3.11 without pulling swanki (Python 3.13) deps.
**Depends on:** only stdlib (`argparse`, `os`, `shutil`, `sys`, `json`, `pathlib`) + MinerU (deferred import).

**Functions:**

- `_parse_args() -> argparse.Namespace` -- args: `--pdf-path` (required Path), `--out-dir` (required Path), `--backend` (default `pipeline`, choices `pipeline|vlm-auto-engine|hybrid-auto-engine`), `--lang` (default `en`), `--method` (default `auto`, choices `auto|txt|ocr`).
- `_ensure_hf_home() -> None` -- if `HF_HOME` set, mkdir and return; else derive from `SWANKI_DATA` env (`$SWANKI_DATA/models/mineru/hf_cache`); if neither, print error to stderr and `sys.exit(4)`. (iBioFoundry-AI keys off `DATA_ROOT`; Swanki uses `SWANKI_DATA`.)
- `_find_first(root, name) -> Path | None` -- `root.rglob(name)` first match.
- `main() -> int` -- resolve pdf-path/out-dir; if PDF missing return 2; mkdir out-dir; `_ensure_hf_home()`; **then** `from mineru.cli.common import do_parse` (deferred, after HF_HOME); run `do_parse(output_dir=str(scratch), pdf_file_names=[stem], pdf_bytes_list=[pdf_bytes], p_lang_list=[lang], backend=backend, parse_method=method)`; locate `{stem}.md` under scratch; if none return 3; flatten `{stem}.md`, `{stem}_content_list.json`, `{stem}_middle.json`, `images/` -> `out-dir/{stem}.md`, `out-dir/{stem}_content_list.json`, `out-dir/{stem}_middle.json`, `out-dir/{stem}_images/`; rmtree scratch; print `OK:` and return 0.

**Skeleton:** clone `run_mineru.py:35-171` verbatim with two changes: (a) `_ensure_hf_home` reads `SWANKI_DATA` not `DATA_ROOT`; (b) drop the slurm-marker docstring references. Keep the deferred `# noqa: E402, I001, PLC0415` import comment explaining the HF_HOME ordering.

**Exit-code contract (consumed by `swanki/ocr/mineru.py`):** 0 ok, 2 PDF missing, 3 no md produced, 4 HF_HOME underivable.

### `swanki/ocr/__init__.py` (NEW)

**Purpose:** OCR provider dispatch. Single public entry the pipeline calls.
**Depends on:** `swanki.ocr.mathpix`, `swanki.ocr.mineru`.

**Functions:**

- `convert_to_markdown(provider: str, *, pages: list[Path], pdf_path: Path, output_base: Path, ocr_config: dict) -> list[Path]`
  - `if provider == "mathpix": return convert_pages_mathpix(pages, output_base)`
  - `if provider == "mineru": return convert_pdf_mineru(pdf_path, output_base, ocr_config)`
  - else `raise ValueError(f"Unknown OCR provider {provider!r}; use 'mathpix' or 'mineru'")`

**Skeleton:**

\`\`\`python
"""
swanki/ocr/__init__.py
[[swanki.ocr]]
https://github.com/Mjvolk3/Swanki/tree/main/swanki/ocr/__init__.py
Test file: tests/test_ocr_dispatch.py

OCR provider dispatch (mathpix | mineru) returning per-page markdown paths.
"""
from pathlib import Path

from swanki.ocr.mathpix import convert_pages_mathpix
from swanki.ocr.mineru import convert_pdf_mineru

__all__ = ["convert_to_markdown", "convert_pages_mathpix", "convert_pdf_mineru"]


def convert_to_markdown(provider, *, pages, pdf_path, output_base, ocr_config):
    if provider == "mathpix":
        return convert_pages_mathpix(pages, output_base)
    if provider == "mineru":
        return convert_pdf_mineru(pdf_path, output_base, ocr_config)
    raise ValueError(f"Unknown OCR provider {provider!r}; use 'mathpix' or 'mineru'")
\`\`\`

### `swanki/ocr/mathpix.py` (NEW)

**Purpose:** Mathpix per-page OCR, extracted verbatim from `pipeline.py:620-659`.
**Depends on:** stdlib `subprocess`; `_natural_sort_key` -- **import from `swanki.processing.markdown_cleaner`** (its true definition site), NOT from `swanki.pipeline.pipeline` (which only re-imports it at line 54). Importing from `pipeline.py` would load the heavy pipeline module and create a circular import, because `pipeline.convert_to_markdown` does `from ..ocr import ...`. (Critic finding 1.)

**Functions:**

- `convert_pages_mathpix(pages: list[Path], output_base: Path) -> list[Path]`
  - mkdir `output_base / "md-singles"`.
  - for each `page_pdf`: `md_path = md_singles_dir / (page_pdf.stem + ".md")`; run `proc = subprocess.run(["script", "-qc", f"mpx convert '{page_pdf}' '{md_path}'", "/dev/null"], capture_output=True, text=True, timeout=300)`. (Upgrade from current `os.system`: the `script -qc` pseudo-TTY wrap matches CLAUDE.md's documented Mathpix TTY requirement and iBioFoundry-AI `_ocr_backend.py:108`, and lets us capture stderr.)
  - **Success check uses `proc.returncode == 0` (a real exit code), NOT `os.system`'s shift-encoded return.** Keep on success when `proc.returncode == 0 and md_path.exists() and md_path.stat().st_size > 0`; on failure log `proc.stderr[-500:]` and continue.
  - `raise RuntimeError("Failed to convert any PDF pages to markdown.")` if none.
  - `return sorted(markdown_files, key=_natural_sort_key)`.

**Edge case:** behavior must be byte-for-byte equivalent to the current loop so existing pipelines are unaffected when `provider=mathpix`.

### `swanki/ocr/mineru.py` (NEW)

**Purpose:** Run the MinerU subprocess on the whole PDF, then split flat output into `md-singles/page-N.md`.
**Depends on:** stdlib `subprocess`, `os`, `json`, `shutil`, `logging`, `pathlib`, `typing.Any`; `PyPDF2` (already a core dep, for authoritative page count); `_natural_sort_key` from **`swanki.processing.markdown_cleaner`** (same circular-import fix as mathpix.py).

**Functions:**

- `convert_pdf_mineru(pdf_path: Path | None, output_base: Path, ocr_config: dict[str, Any]) -> list[Path]`
  0. **Guard (Critic finding / edge case 8):** `if pdf_path is None: raise RuntimeError("MinerU OCR requires the source PDF path; process_full did not set source_pdf_path.")`
  1. `raw_dir = output_base / "mineru-raw"`; if it exists `shutil.rmtree` it (Directive 1: never reuse stale OCR), then mkdir.
  2. Build env: copy `os.environ`, set `CUDA_VISIBLE_DEVICES = str(ocr_config.get("cuda_visible_devices", "3"))`, `HF_HOME = <resolved hf_home>` (see step 2a), `MINERU_MODEL_SOURCE = "huggingface"`, `MINERU_DEVICE_MODE = ocr_config.get("device_mode", "cuda")`.
  2a. **Lazy HF_HOME resolution (Critic finding 3 / 4):** do NOT read an `${oc.env:...}`-interpolated yaml value. Resolve here: `hf_home = ocr_config.get("hf_home") or (os.getenv("SWANKI_DATA", "") + "/models/mineru/hf_cache")`; expand `~`/vars; if it resolves empty, `raise RuntimeError("Set SWANKI_DATA or models.ocr.hf_home for MinerU")`. This keeps the SWANKI_DATA dependency on the MinerU path only, never on the default Mathpix path.
  3. `python_bin = os.path.expanduser(ocr_config.get("python_bin", "~/opt/miniconda3/envs/swanki-mineru/bin/python"))`; `runner = str(Path(__file__).resolve().parents[2] / ocr_config.get("runner", "scripts/run_mineru_swanki.py"))` (parents[2] = repo root: `swanki/ocr/mineru.py` -> `swanki/ocr` -> `swanki` -> root; correct in worktrees too).
  4. `cmd = [python_bin, runner, "--pdf-path", str(pdf_path), "--out-dir", str(raw_dir), "--backend", ocr_config.get("backend", "pipeline"), "--lang", ocr_config.get("lang", "en"), "--method", ocr_config.get("method", "auto")]`.
  5. `proc = subprocess.run(cmd, env=env, capture_output=True, text=True, timeout=ocr_config.get("timeout", 3600))`; `if proc.returncode != 0: raise RuntimeError(f"MinerU failed (exit {proc.returncode}): {proc.stderr[-2000:]}")`.
  6. `stem = pdf_path.stem`; `content_list = raw_dir / f"{stem}_content_list.json"`.
  7. `num_pages = len(PdfReader(str(pdf_path)).pages)` -- authoritative page count for empty-page backfill (step in splitter).
  8. `page_files = split_content_list_to_pages(content_list, raw_dir, output_base, num_pages)`.
  9. `return sorted(page_files, key=_natural_sort_key)`.

- `split_content_list_to_pages(content_list_path: Path, raw_dir: Path, output_base: Path, num_pages: int) -> list[Path]`
  - `md_singles_dir = output_base / "md-singles"`; `images_dir = output_base / "images"`; mkdir both. **Images go to `output_base/images/` NOT `md-singles/` (Critic finding: completeness).** `image_processor.py:209-215` resolves local image refs against `clean_md_singles_dir.parent/url` and `output_base/url`; with the ref written as `images/<name>` and the file at `output_base/images/<name>`, candidate `output_base/url` matches.
  - `blocks = json.loads(content_list_path.read_text())` -- a flat list, each block carries `type` and `page_idx` (0-based int). **Documented MinerU 2.x pipeline-backend schema** (from opendatalab.github.io/MinerU output_files reference, confirmed 2026-05-21):
    - `text` -- fields `text`, optional `text_level` (present ONLY on headings: 1, 2, ...), `page_idx`. There is NO separate `"title"` type in the pipeline backend; headings are `type:"text"` + `text_level`.
    - `equation` -- fields `text` (already `$$...$$`), `text_format`, `img_path`, `page_idx`.
    - `image` -- fields `img_path`, `image_caption` (a LIST), `image_footnote`, `page_idx`. (Note: `image_caption`, not `img_caption`.)
    - `table` -- fields `img_path`, `table_caption` (list), `table_footnote`, `table_body` (HTML), `page_idx`.
    - Noise types to SKIP: `header`, `footer`, `page_number`, `page_footnote`, `aside_text` (running heads / pagination -- not card content).
  - group blocks by `page_idx`; for each page render markdown in list order:
    - `text` with `text_level` -> `"#" * int(block["text_level"]) + " " + block["text"]`
    - `text` without `text_level` -> `block["text"]`
    - `equation` -> `block["text"]`
    - `image` -> copy `raw_dir / block["img_path"]` to `images_dir / Path(block["img_path"]).name`, emit `![](images/<name>)` (optionally append `image_caption` joined)
    - `table` -> emit `table_body` (HTML passes through; the LLM card stage handles it), optionally prefixed by joined `table_caption`
    - skip noise types listed above
  - **Capture a real `content_list.json` during implementation to confirm the schema** (run MinerU once on a sample PDF after env setup), but the documented schema above is sufficient to author the splitter and a hand-built unit fixture without blocking on the live run.
  - **Empty-page backfill (Critic finding: page-index invariant is load-bearing).** Emit `md_singles_dir / f"page-{n}.md"` for EVERY `n` in `1..num_pages`, writing an empty (or image-only) file for pages with no blocks. `section_classifier.py` indexes `clean_md_files[page_idx]` and `pipeline.py:383` aligns `image_summaries[page_idx]` positionally, so the per-page file count MUST equal `split_pdf`'s page count, contiguous, natural-sortable. A missing page desyncs every later page.
  - return list of all written page paths.

**Skeleton:**

\`\`\`python
from typing import Any
from PyPDF2 import PdfReader
from swanki.processing.markdown_cleaner import _natural_sort_key

def convert_pdf_mineru(pdf_path, output_base, ocr_config):
    if pdf_path is None:
        raise RuntimeError("MinerU OCR requires source_pdf_path (unset on resume).")
    raw_dir = output_base / "mineru-raw"
    if raw_dir.exists():
        shutil.rmtree(raw_dir)          # Directive 1: never reuse stale OCR
    raw_dir.mkdir(parents=True)
    hf_home = ocr_config.get("hf_home") or f"{os.getenv('SWANKI_DATA', '')}/models/mineru/hf_cache"
    hf_home = os.path.expandvars(os.path.expanduser(hf_home))
    if not os.getenv("SWANKI_DATA") and not ocr_config.get("hf_home"):
        raise RuntimeError("Set SWANKI_DATA or models.ocr.hf_home for MinerU")
    env = os.environ.copy()
    env.update({
        "CUDA_VISIBLE_DEVICES": str(ocr_config.get("cuda_visible_devices", "3")),
        "HF_HOME": hf_home,
        "MINERU_MODEL_SOURCE": "huggingface",
        "MINERU_DEVICE_MODE": ocr_config.get("device_mode", "cuda"),
    })
    python_bin = os.path.expanduser(ocr_config.get("python_bin", "~/opt/miniconda3/envs/swanki-mineru/bin/python"))
    runner = str(Path(__file__).resolve().parents[2] / ocr_config.get("runner", "scripts/run_mineru_swanki.py"))
    cmd = [python_bin, runner, "--pdf-path", str(pdf_path), "--out-dir", str(raw_dir),
           "--backend", ocr_config.get("backend", "pipeline"),
           "--lang", ocr_config.get("lang", "en"),
           "--method", ocr_config.get("method", "auto")]
    proc = subprocess.run(cmd, env=env, capture_output=True, text=True,
                          timeout=ocr_config.get("timeout", 3600))
    if proc.returncode != 0:
        raise RuntimeError(f"MinerU failed (exit {proc.returncode}): {proc.stderr[-2000:]}")
    stem = pdf_path.stem
    num_pages = len(PdfReader(str(pdf_path)).pages)
    pages = split_content_list_to_pages(
        raw_dir / f"{stem}_content_list.json", raw_dir, output_base, num_pages)
    return sorted(pages, key=_natural_sort_key)
\`\`\`

### `swanki/pipeline/pipeline.py` (MODIFY)

**Current state:** `process_full()` (line 153) calls `self.convert_to_markdown(pages)` at line 254. `convert_to_markdown()` (594-659) is the Mathpix per-page loop. TTS provider switch at 1999-2057 is the dispatch template. Fish discovery imported at 2098-2102.

**Changes:**

1. **Store source PDF.** In `process_full`, after `self.output_base` is set and before the split (~line 248), add `self.source_pdf_path = pdf_path`. The MinerU branch needs the original PDF (the `pages` arg is per-page splits it ignores).
2. **Rewrite `convert_to_markdown` body (620-659) to dispatch:**
   - `ocr_cfg = self.config.get("models", {}).get("models", {}).get("ocr", {})` -- the doubled `models` key is correct (Hydra group nesting; confirmed at `pipeline.py:1995`).
   - **`self.config` is already a plain dict here**, not a DictConfig: `swanki/__main__.py:30` does `OmegaConf.to_container(cfg, resolve=True)` before `Pipeline(config)`. So `ocr_cfg` is a plain dict and needs no conversion. (The TTS `_sub` helper at 2008-2018 only keeps a defensive `isinstance(node, DictConfig)` check that falls through for dicts -- harmless to mirror, but not required here.)
   - `provider = ocr_cfg.get("provider", "mathpix")`
   - `from ..ocr import convert_to_markdown as _ocr_convert` (deferred import inside the method -- avoids the cycle on the pipeline side)
   - `return _ocr_convert(provider, pages=pages, pdf_path=getattr(self, "source_pdf_path", None), output_base=self.output_base, ocr_config=ocr_cfg)`
   - keep the method docstring but update "Uses Mathpix" -> "Dispatches to the configured OCR provider (mathpix | mineru)".
3. **Do NOT change** the `process_full` call site at 254 (signature unchanged).

### `swanki/audio/_common.py` (MODIFY)

**Current state:** `_FISH_SPEECH_PORTS = [8080, 8081, 8082, 8083]` (line 593). Discovery (604-638) probes each port, skips dead ones via try/except, caches, re-probes only while `len(healthy) < len(_FISH_SPEECH_PORTS)`.

**Changes (Directive 2):**

1. Make the port list env-overridable so freeing GPU 3 doesn't cause perpetual re-probing of a permanently-dead 8083:
   `_FISH_SPEECH_PORTS = [int(p) for p in os.getenv("SWANKI_FISH_PORTS", "8080,8081,8082").split(",")]`
   Default drops 8083 (GPU 3 reserved for MinerU). Confirm `os` is imported in this module (add if missing).
2. No other change needed -- discovery already tolerates missing ports.

### `swanki/conf/models/default.yaml` (MODIFY)

**Current state:** `models: {llm, tts}`. **Change:** add sibling `ocr` block:

\`\`\`yaml
  ocr:
    provider: mathpix          # mathpix | mineru
    # --- mineru-only knobs (ignored when provider=mathpix) ---
    python_bin: ~/opt/miniconda3/envs/swanki-mineru/bin/python
    runner: scripts/run_mineru_swanki.py
    cuda_visible_devices: "3"  # GPU freed from Fish (Directive 2)
    # hf_home omitted on purpose: mineru.py resolves it lazily from
    # $SWANKI_DATA/models/mineru/hf_cache. Do NOT use ${oc.env:SWANKI_DATA}
    # here -- it would force SWANKI_DATA at compose time even on the Mathpix
    # default path (Critic finding 3/4). Set hf_home explicitly only to override.
    device_mode: cuda
    backend: pipeline          # pipeline | vlm-auto-engine | hybrid-auto-engine
    lang: en
    method: auto               # auto | txt | ocr
    timeout: 3600
\`\`\`

### `swanki/conf/models/fish_speech.yaml` and `fish_speech_{audrey,bechtel,hamming}.yaml` (MODIFY)

**Change:** add the same `ocr:` block as `default.yaml` to `fish_speech.yaml` (the gilahyper default). The three per-paper variants inherit via Hydra group merge from their base -- verify whether they `defaults:`-include `fish_speech` or are standalone; if standalone, add the `ocr:` block to each. Keep `provider: mathpix` default everywhere (opt into MinerU per-run with `models.ocr.provider=mineru`).

### `pyproject.toml` (MODIFY)

**Change:** add to `[project.optional-dependencies]` (Directive 3, marker only -- real install is the conda env):

\`\`\`toml
mineru = ["mineru[pipeline]>=2.0.0,<3", "torch<2.11", "torchvision<0.26", "huggingface_hub>=0.23"]
\`\`\`

Add a comment that this extra is documentation/discoverability; production install uses the isolated `swanki-mineru` conda env (see `env/swanki-mineru-requirements.txt`). Do NOT add to core `dependencies` (PyPI bloat).

### `env/swanki-mineru-requirements.txt` (NEW)

**Purpose:** isolated MinerU env, cloned from `iBioFoundry-AI/env/ibfai-mineru-requirements.txt`.

\`\`\`
# env/swanki-mineru-requirements.txt
# Isolated MinerU 2.x OCR env. MinerU bundles its own torch CUDA runtime +
# torch-based PaddleOCR fork; keep it out of the swanki (3.13) env.
# Create: mamba create -n swanki-mineru python=3.11 && pip install -r env/swanki-mineru-requirements.txt
# Runner: scripts/run_mineru_swanki.py
mineru[pipeline]>=2.0.0,<3
torch<2.11
torchvision<0.26
huggingface_hub>=0.23
\`\`\`

### `scripts/setup-mineru-env.sh` (NEW)

**Purpose:** one-shot env creation + first-run model warmup. Idempotent.
**Contents:** `set -euo pipefail`; create `swanki-mineru` conda env at python 3.11 if absent; `pip install -r env/swanki-mineru-requirements.txt`; mkdir `$SWANKI_DATA/models/mineru/hf_cache`; print next-steps (run `scripts/free-gpu-for-mineru.sh`, then a test invocation). Models download lazily on first `do_parse`.

### `scripts/free-gpu-for-mineru.sh` (NEW)

**Purpose:** stop the Fish container on `device=3`/`8083` to free GPU 3 (Directive 2), with a restart counterpart.
**Contents:** find the docker container publishing `8083` (`docker ps --filter publish=8083 -q`), `docker stop` it; echo that GPU 3 is now free for MinerU and that `SWANKI_FISH_PORTS` already excludes 8083. Provide a commented restart command (the original `docker run ... --gpus device=3 ... -p 8083:8080 ...` line from the running process table). **Do NOT auto-run on import** -- this is an explicit operator action.

### `tests/test_ocr_dispatch.py` (NEW)

**Test cases:**
- `test_dispatch_mathpix_routes_to_mathpix` -- monkeypatch `swanki.ocr.convert_pages_mathpix` to a sentinel; assert `convert_to_markdown("mathpix", ...)` calls it with `pages`/`output_base`.
- `test_dispatch_mineru_routes_to_mineru` -- monkeypatch `convert_pdf_mineru`; assert called with `pdf_path`/`ocr_config`.
- `test_dispatch_unknown_provider_raises` -- `pytest.raises(ValueError)` for `provider="paddle"`.

### `tests/test_ocr_mineru_split.py` (NEW)

**Test cases:**
- `test_split_groups_blocks_by_page` -- given a fixture `content_list.json` with blocks across `page_idx` 0/1/2, assert three `page-1.md`/`page-2.md`/`page-3.md` written, content partitioned correctly.
- `test_split_renders_headings_and_equations` -- `text_level` -> `##`, equation block preserved.
- `test_split_copies_images_and_rewrites_path` -- image block's `img_path` file is copied into `md-singles/` and the emitted `![](...)` points at the copied name.
- Fixture: `tests/fixtures/mineru/sample_content_list.json` -- hand-build from the documented schema in the `split_content_list_to_pages` spec (text+`text_level` heading, plain text, equation, image with `img_path`, table with `table_body`, plus a `header`/`page_number` noise block to assert it's skipped, and a page with zero content blocks to assert empty-page backfill). Confirm against a real MinerU run during implementation and reconcile if any field differs.

### `tests/test_ocr_mathpix.py` (NEW)

**Test cases:**
- `test_mathpix_skips_failed_pages` -- monkeypatch `subprocess.run` to fail for `page-2.pdf`, succeed others; assert it's omitted and others returned sorted.
- `test_mathpix_raises_when_all_fail` -- all fail -> `RuntimeError`.
- `test_mathpix_natural_sort` -- `page-10.md` sorts after `page-2.md`.

### `notes/swanki.ocr.md`, `notes/swanki.ocr.mathpix.md`, `notes/swanki.ocr.mineru.md` (NEW)

**Purpose:** CLAUDE.md mandates a paired dendron module note per source file ("Finding Rationale for Changes"). Create one per new `swanki/ocr/*.py`. An autonomous run should produce these via `/update-src-notes` after the code lands (the skill auto-generates dated sections), not hand-write them. The runner script `scripts/run_mineru_swanki.py` follows the bash/script note convention if `/update-src-notes` covers `scripts/`.

## Conventions (apply to every new file)

- **Frontmatter docstring (ruff + CLAUDE.md).** Each new `.py` opens with the single frontmatter docstring block: module path, `[[dotted.module]]`, GitHub URL, `Test file: tests/...`, then a one-line description. No separate module docstring. Example header is shown in the `swanki/ocr/__init__.py` skeleton above; replicate the shape for `mathpix.py`, `mineru.py`, and the runner.
- **mypy strict (`pyproject.toml:123`, py3.13).** Fully annotate every signature: `provider: str`, `pages: list[Path]`, `pdf_path: Path | None`, `output_base: Path`, `ocr_config: dict[str, Any]`, `-> list[Path]`. No bare `dict`/`list` generics. `mineru` itself is imported only inside `scripts/run_mineru_swanki.py`, which lives OUTSIDE the `swanki*` package scan (`[tool.setuptools.packages.find] include = ["swanki*", "hydra_plugins*"]`), so mypy never sees the `mineru` import and no `ignore_missing_imports` override is needed.
- **No try/except padding (CLAUDE.md "fail fast").** The Mathpix per-page warn-and-continue is the one existing exception (preserve it). Elsewhere let errors raise.
- **`swanki.ocr` is auto-packaged** by the existing `packages.find` glob `swanki*` -- no pyproject change needed for the new package.
- **markdown_cleaner is MinerU-safe; do NOT "fix" it.** `markdown_cleaner.py` substitutions target Mathpix LaTeX (`\section{}`->`##`, `\(\)`->`$$`, `\begin{figure}\includegraphics{}`->`![]()`). MinerU emits standard GFM, so these no-op cleanly and pass MinerU markdown through unchanged. The only cleaner-adjacent concern is image-path resolution, already handled by writing images to `output_base/images/`.

## Edge Cases

1. **content_list.json schema (documented).** MinerU 2.x does NOT emit `<!-- Page N -->` markers in the `.md` (the 04-15 plan's assumption is wrong). The authoritative page signal is `page_idx` per block in `content_list.json`. The exact pipeline-backend schema is documented and reproduced in the `split_content_list_to_pages` spec above (text/equation/image/table fields + noise types to skip), so the splitter and a hand-built unit fixture can be authored without a live run. Still capture a real `content_list.json` during implementation as a confirmation fixture (run MinerU once after env setup); if any field name differs from the documented schema, reconcile then.
2. **Pages with no text blocks** (pure-figure pages) must still emit a `page-N.md` (possibly image-only) so the page index sequence has no gaps -- downstream page->segment mapping assumes contiguous pages.
3. **MinerU image paths** are relative to the raw output dir. They must be copied into `md-singles/` so `ImageProcessor` (resolution candidates at `image_processor.py:209-215`) finds them; otherwise image cards break.
4. **First run downloads ~6-10 GB** of HF models; the subprocess timeout (default 3600s) must accommodate cold start. `scripts/setup-mineru-env.sh` should optionally warm the cache.
5. **GPU 3 must actually be free.** If `free-gpu-for-mineru.sh` wasn't run, MinerU on a Fish-occupied GPU 3 OOMs or contends. The runner logs the visible device; document the operator step.
6. **`MINERU_DEVICE_MODE=cuda` is mandatory** -- MinerU silently runs CPU (~30s/page) without it.
7. **Mathpix path must be untouched** when `provider=mathpix` (default). Parity test (`test_ocr_mathpix.py`) guards this.
8. **`source_pdf_path` on resume.** If the pipeline is ever resumed mid-run without re-calling `process_full`, `self.source_pdf_path` may be unset; the MinerU branch should `raise` a clear error if it's `None`.

## Verification

1. Unit tests: `~/opt/miniconda3/envs/swanki/bin/python -m pytest tests/test_ocr_dispatch.py tests/test_ocr_mineru_split.py tests/test_ocr_mathpix.py -xvs`
2. Type check: `mypy swanki/ocr/__init__.py swanki/ocr/mathpix.py swanki/ocr/mineru.py`
3. Lint: `ruff check swanki/ocr/ scripts/run_mineru_swanki.py`
4. Mathpix regression: run an existing paper with default config; confirm `md-singles/page-N.md` identical to a pre-change run.
5. MinerU end-to-end (manual, on gilahyper): `bash scripts/setup-mineru-env.sh`; `bash scripts/free-gpu-for-mineru.sh`; run a paper with `models.ocr.provider=mineru`; confirm `md-singles/page-N.md` produced, images present, cards generate, Fish audio still works on the 3 remaining servers.

## Execution

To implement, start a new Claude Code session in a worktree:

\`\`\`
/read-codebase pipeline ocr audio
\`\`\`

Then:

\`\`\`
Implement the plan at notes/plan.transition-ocr-to-mineru-dual-path.2026.05.19.md. Read the plan first. Implement file specs in the stated order (runner -> ocr package -> pipeline wiring -> config -> deps/env -> GPU helper -> tests). For Edge Case 1, run MinerU on a real PDF first to capture the true content_list.json schema before writing the splitter. Run verification after each file. Commit with /update-notes -> /stage -> /commit after each logical unit.
\`\`\`

## Critic Review

A critic agent reviewed the draft against the live codebase. Findings and resolutions:

1. **`_natural_sort_key` import source was wrong (circular-import risk).** The helper is defined in `swanki/processing/markdown_cleaner.py`; `pipeline.py:54` only re-imports it. Importing from `swanki.pipeline.pipeline` would load the heavy pipeline module and cycle against `pipeline -> ..ocr`. **RESOLVED:** both `mathpix.py` and `mineru.py` specs now import from `swanki.processing.markdown_cleaner`.
2. **MinerU image placement bug.** `image_processor.py:209-215` resolves local refs against `output_base/url` and `clean_md_singles_dir.parent/url`, not `md-singles/`. **RESOLVED:** splitter now writes images to `output_base/images/` and emits `![](images/<name>)`.
3. **`${oc.env:SWANKI_DATA}` would break even the Mathpix default path** if `.env` isn't sourced at compose time (resolution happens in `__main__.py:30` before `load_dotenv`). **RESOLVED:** dropped the yaml interpolation; `hf_home` resolves lazily inside `mineru.py` from `os.getenv("SWANKI_DATA")`, isolating the dependency to the MinerU path.
4. **`self.config` is a plain dict, not DictConfig** (per `__main__.py:30`). **RESOLVED:** pipeline spec corrected -- no OmegaConf conversion needed.
5. **Page-index invariant is load-bearing.** `section_classifier.py` and `pipeline.py:383` index per-page lists positionally. **RESOLVED:** splitter now backfills an empty `page-N.md` for every page in `1..num_pages` (count from `PyPDF2.PdfReader`), guaranteeing contiguity.
6. **`pdf_path is None` on resume.** **RESOLVED:** added an explicit guard at the top of `convert_pdf_mineru`.
7. **`os.system` -> `subprocess.run` exit-code semantics.** **RESOLVED:** mathpix spec checks `proc.returncode == 0`, not the shifted `os.system` code.
8. **Missing dendron module notes + frontmatter/mypy/ruff conventions.** **RESOLVED:** added a Conventions section and a notes spec (`/update-src-notes` after code lands).
9. **Fixture sequencing.** **RESOLVED:** capture the real `content_list.json` fixture before authoring the splitter and its tests.

Verified-correct as drafted (no change needed): doubled `models.models` key access; line ranges (`convert_to_markdown` 620-659, TTS switch 1992-2059); `_FISH_SPEECH_PORTS` at `_common.py:593` with `os` not yet imported (add it); all 5 model yamls are standalone (each needs its own `ocr:` block); no Hydra structured-config/schema to update; `[project.optional-dependencies]` already exists; `Path(__file__).resolve().parents[2]` correctly resolves repo root from `swanki/ocr/mineru.py` (worktree-safe).

**Specification quality after fixes:** GREEN -- runner, `ocr/__init__.py`, pipeline MODIFY, `_common.py` MODIFY, pyproject, env/scripts. GREEN (was YELLOW/RED) -- `mathpix.py`, `mineru.py`, model yamls, tests, now that the corrections above are folded in. The one residual unknown is MinerU's exact `content_list.json` schema, deliberately deferred to an empirical capture step (Edge Case 1) rather than guessed.
