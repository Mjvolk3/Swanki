---
id: liewxsi9yx6jrg7sf66mius
title: Open-Source Pipeline - MinerU OCR + Gemma 4 LLM
desc: Replace Mathpix with MinerU, OpenAI with Gemma 4 31B via vLLM, support single-GPU sequential and multi-GPU parallel modes
updated: 1776366659544
created: 1776302823728
---

Plan: Open-Source Pipeline -- MinerU OCR + Gemma 4 LLM

## Context

Swanki currently depends on two closed-source cloud services:

1. **Mathpix CLI** (`mpx convert`) for PDF-to-markdown OCR -- called per-page in `pipeline.py:517` via `os.system()`.
2. **OpenAI API** (gpt-5.2) for all text generation (card gen, summaries, feedback, audio transcripts, image summarization) and vision (image processing) -- routed through `llm/agents.py:get_model_string()`.

Fish Speech TTS is already open-source and self-hosted on gilahyper (4x RTX 6000 Ada, 46 GB each) via SLURM jobs 839--842.

**Goal:** Replace both cloud services with self-hosted open-source alternatives:

- **MinerU** (opendatalab/MinerU) for PDF-to-markdown+images OCR
- **Gemma 4 31B Dense IT** (Int4 quantized, ~16 GB) via **vLLM** for all text AND vision generation

**Two GPU modes must be supported:**

1. **Single-GPU sequential:** MinerU batch -> Gemma vLLM server -> Fish Speech server. Only one service occupies the GPU at a time. Servers spin up and tear down between phases.
2. **Multi-GPU parallel:** Gemma on one GPU, Fish Speech on 1--3 GPUs, MinerU as batch on any available GPU. Servers coexist. Current behavior for Fish Speech already works this way.

**Test paper:** `/scratch/projects/torchcell-scratch/Swanki_Data/luoWhenCausalInference2020`

## Approach

### Architecture Decision: Phase-Based GPU Orchestration

The pipeline stages naturally partition into three GPU phases:

```
Phase 1 -- OCR (MinerU, batch, no server)
  PDF -> markdown + extracted images
  GPU loaded/unloaded by MinerU internally

Phase 2 -- LLM (Gemma 4 vLLM server)
  Image summarization (vision)
  Document summary generation
  Card generation + self-refinement
  Card feedback
  Audio transcript generation (all four types) -> saved to sidecar files
  Slide generation

Phase 3 -- TTS (Fish Speech server)
  TTS from saved transcript sidecars (cards, summary, reading, lecture)
```

In multi-GPU mode, phases 2 and 3 overlap (Gemma and Fish Speech run on separate GPUs). In single-GPU mode, they are strictly sequential.

### Key Design Decisions

1. **MinerU processes whole PDFs, not per-page.** The current pipeline splits PDFs into pages first, then OCRs each page. MinerU takes the whole PDF and outputs a single markdown file + extracted images. We split MinerU's output back into per-page files using page boundary markers, preserving compatibility with the downstream segmenter and per-page card generation.

2. **pydantic-ai base_url for vLLM.** The `get_model_string()` function currently returns a `"provider:model"` string. For vLLM, we need to return a `pydantic_ai.models.openai.OpenAIModel` object with a custom `base_url`. pydantic-ai's `.run_sync(model=...)` accepts both strings and model objects, so this is backward-compatible.

3. **Audio sidecar pattern.** The audio modules already save transcripts to disk (card.py saves to `complementary_transcripts/`, reading/summary/lecture save to their own transcript dirs). We add a `tts_enabled: bool` parameter to each audio generator. When False, they do all LLM work and save transcripts but skip TTS calls. A new `tts_from_transcripts()` function reads saved transcripts and runs TTS. This keeps the refactoring minimal and makes transcript regeneration independent of TTS.

4. **Generalized server pool.** Extract the Fish Speech health-check + round-robin pattern from `_common.py` into a reusable `ServerPool` class. Both Fish Speech and vLLM use it.

5. **Slide generator port.** The only file using `instructor.patch(OpenAI())` is `slide_generator.py`. Port it to pydantic-ai with the `Presentation` response model, eliminating the instructor dependency for this path.

## File Specifications

### `swanki/ocr/__init__.py` (NEW)

**Purpose:** OCR package init, re-exports MinerU converter.

**Skeleton:**

```python
"""
swanki/ocr/__init__.py
[[swanki.ocr]]
https://github.com/Mjvolk3/Swanki/tree/main/swanki/ocr/__init__.py

OCR processing package for PDF-to-markdown conversion.
"""

from .mineru import MinerUConverter

__all__ = ["MinerUConverter"]
```

### `swanki/ocr/mineru.py` (NEW)

**Purpose:** Wraps MinerU (`magic-pdf`) for whole-PDF OCR, splits output into per-page markdown files matching the existing `md-singles/page-N.md` structure.

**Depends on:** `magic_pdf` (MinerU Python API), `pathlib`, `re`, `logging`

**Types:**

- No Pydantic models needed -- returns `list[Path]` like existing `convert_to_markdown()`

**Functions:**

- `MinerUConverter.__init__(self, output_base: Path, device: str = "cuda:0")` -- stores output paths
- `MinerUConverter.convert_pdf(self, pdf_path: Path) -> list[Path]` -- runs MinerU on the whole PDF, splits output into `md-singles/page-N.md` files, copies extracted images to appropriate location
  - Calls MinerU via `magic_pdf` Python API (not CLI) for better error handling
  - MinerU output includes page boundary markers (`\n---\n` between pages or page-header comments)
  - Splits the single markdown into per-page files using `_split_by_pages()`
  - Copies extracted images to `md-singles/` so relative paths resolve
  - Returns sorted list of page markdown paths
- `MinerUConverter._split_by_pages(self, markdown: str, images_dir: Path) -> list[str]` -- splits MinerU markdown at page boundaries
  - MinerU inserts `<!-- Page N -->` or horizontal rules between pages
  - Falls back to splitting at `##` headers if no page markers found
  - Rewrites image paths from MinerU's `images/` dir to the correct relative path
- `MinerUConverter._rewrite_image_paths(self, content: str, source_images_dir: Path, target_dir: Path) -> str` -- copies images and updates markdown image references to local paths

**Skeleton:**

```python
class MinerUConverter:
    def __init__(self, output_base: Path, device: str = "cuda:0") -> None:
        self.output_base = output_base
        self.md_singles_dir = output_base / "md-singles"
        self.device = device

    def convert_pdf(self, pdf_path: Path) -> list[Path]:
        from magic_pdf.data.data_reader_writer import FileBasedDataWriter, FileBasedDataReader
        from magic_pdf.pipe.UNIPipe import UNIPipe

        self.md_singles_dir.mkdir(parents=True, exist_ok=True)
        # ... run MinerU, split output, return page paths
```

### `swanki/infra/__init__.py` (NEW)

**Purpose:** Infrastructure package for server lifecycle and GPU orchestration.

```python
"""
swanki/infra/__init__.py
[[swanki.infra]]
https://github.com/Mjvolk3/Swanki/tree/main/swanki/infra/__init__.py

Server lifecycle management and GPU orchestration.
"""

from .gpu_orchestrator import GpuOrchestrator
from .server_pool import ServerPool

__all__ = ["GpuOrchestrator", "ServerPool"]
```

### `swanki/infra/server_pool.py` (NEW)

**Purpose:** Generalized health-check + round-robin server pool. Replaces the Fish Speech-specific code in `_common.py:264-322`.

**Depends on:** `httpx`, `threading`, `logging`

**Types:**

- `ServerPool` -- thread-safe server discovery and round-robin selection

**Functions:**

- `ServerPool.__init__(self, name: str, ports: list[int], health_path: str, base_host: str = "http://localhost")` -- configure pool
- `ServerPool.discover(self, force: bool = False) -> list[str]` -- health-check all ports, cache healthy list, re-discover when cached list is smaller than port list
- `ServerPool.pick(self) -> str` -- round-robin across healthy servers (thread-safe)
- `ServerPool.count(self) -> int` -- number of healthy servers
- `ServerPool.reset(self) -> None` -- clear cached discovery state

**Skeleton:**

```python
class ServerPool:
    def __init__(
        self,
        name: str,
        ports: list[int],
        health_path: str,
        base_host: str = "http://localhost",
    ) -> None:
        self._name = name
        self._ports = ports
        self._health_path = health_path
        self._base_host = base_host
        self._lock = threading.Lock()
        self._index = 0
        self._healthy: list[str] = []
        self._discovered = False

    def discover(self, force: bool = False) -> list[str]:
        if self._discovered and not force and len(self._healthy) >= len(self._ports):
            return self._healthy
        healthy = []
        for port in self._ports:
            url = f"{self._base_host}:{port}"
            try:
                r = httpx.get(f"{url}{self._health_path}", timeout=10.0)
                if r.status_code == 200:
                    healthy.append(url)
            except httpx.HTTPError:
                continue
        if not healthy:
            healthy = [f"{self._base_host}:{self._ports[0]}"]
        self._healthy = healthy
        self._discovered = True
        return healthy

    def pick(self) -> str:
        servers = self.discover()
        with self._lock:
            server = servers[self._index % len(servers)]
            self._index += 1
        return server

    def count(self) -> int:
        return len(self.discover())

    def reset(self) -> None:
        self._healthy = []
        self._discovered = False
        self._index = 0
```

### `swanki/infra/vllm_server.py` (NEW)

**Purpose:** Manage vLLM server process lifecycle (start, health-check, stop). Used by `GpuOrchestrator` in single-GPU mode.

**Depends on:** `subprocess`, `httpx`, `time`, `logging`, `signal`

**Functions:**

- `VllmServer.__init__(self, model_name: str, port: int = 8090, device: str = "cuda:0", quantization: str = "awq", max_model_len: int = 32768)` -- configure vLLM launch params
- `VllmServer.start(self) -> None` -- launch vLLM as subprocess, poll `/health` until ready (timeout 120s)
  - Command: `python -m vllm.entrypoints.openai.api_server --model {model_name} --port {port} --device {device} --quantization {quantization} --max-model-len {max_model_len} --trust-remote-code`
  - Sets `CUDA_VISIBLE_DEVICES` based on device
- `VllmServer.stop(self) -> None` -- SIGTERM the subprocess, wait for exit, clear GPU memory
- `VllmServer.is_healthy(self) -> bool` -- check `/health` endpoint
- `VllmServer.__enter__` / `__exit__` -- context manager for automatic cleanup
- `VllmServer.base_url` property -- returns `http://localhost:{port}/v1`

**Skeleton:**

```python
class VllmServer:
    def __init__(
        self,
        model_name: str,
        port: int = 8090,
        device: str = "cuda:0",
        quantization: str = "awq",
        max_model_len: int = 32768,
    ) -> None:
        self.model_name = model_name
        self.port = port
        self.device = device
        self.quantization = quantization
        self.max_model_len = max_model_len
        self._process: subprocess.Popen | None = None

    @property
    def base_url(self) -> str:
        return f"http://localhost:{self.port}/v1"

    def start(self) -> None:
        gpu_id = self.device.split(":")[-1] if ":" in self.device else "0"
        env = {**os.environ, "CUDA_VISIBLE_DEVICES": gpu_id}
        cmd = [
            "python", "-m", "vllm.entrypoints.openai.api_server",
            "--model", self.model_name,
            "--port", str(self.port),
            "--quantization", self.quantization,
            "--max-model-len", str(self.max_model_len),
            "--trust-remote-code",
        ]
        self._process = subprocess.Popen(cmd, env=env)
        self._wait_healthy(timeout=120)

    def stop(self) -> None:
        if self._process:
            self._process.terminate()
            self._process.wait(timeout=30)
            self._process = None

    def __enter__(self): self.start(); return self
    def __exit__(self, *_): self.stop()
```

### `swanki/infra/gpu_orchestrator.py` (NEW)

**Purpose:** Orchestrate GPU-phase transitions for single-GPU mode. In multi-GPU mode, acts as a no-op passthrough.

**Depends on:** `VllmServer`, `subprocess`, `logging`

**Types:**

- `GpuOrchestrator` -- manages phase transitions

**Functions:**

- `GpuOrchestrator.__init__(self, mode: str, gpu_device: str = "cuda:0", gemma_config: dict, fish_config: dict)` -- mode is "single-gpu" or "multi-gpu"
- `GpuOrchestrator.ocr_phase(self) -> ContextManager` -- in single-gpu: ensures GPU is free. In multi-gpu: no-op
- `GpuOrchestrator.llm_phase(self) -> ContextManager` -- in single-gpu: starts vLLM, yields, stops vLLM. In multi-gpu: no-op (assumes server already running)
- `GpuOrchestrator.tts_phase(self) -> ContextManager` -- in single-gpu: starts Fish Speech, yields, stops Fish Speech. In multi-gpu: no-op
- `GpuOrchestrator.vllm_base_url` property -- returns vLLM base URL for pydantic-ai
- `GpuOrchestrator.fish_speech_url` property -- returns Fish Speech server URL

### `swanki/conf/models/gemma4.yaml` (NEW)

**Purpose:** Hydra config for Gemma 4 via vLLM + Fish Speech TTS.

```yaml
models:
  llm:
    provider: openai
    model: gemma-4-31b-it
    base_url: http://localhost:8090/v1
    temperature: 0.7
    max_retries: 3
  tts:
    provider: fish_speech
    server_url: http://localhost:8080
    reference_id: british-prof
    reference_audio_path: ""
    reference_text: ""
    temperature: 0.8
    format: mp3
  gpu:
    mode: single-gpu
    device: "cuda:0"
    gemma_model: nvidia/Gemma-4-31B-IT-NVFP4
    gemma_quantization: fp8
    gemma_port: 8090
    gemma_max_model_len: 32768
    fish_speech_port: 8080
```

### `swanki/llm/agents.py` (MODIFY)

**Current state:** `get_model_string()` at line 40 returns `"provider:model"` string. No base_url support.

**Changes:**

1. Import `pydantic_ai.models.openai.OpenAIModel` at top
2. Modify `get_model_string()` to accept and use `base_url`:

```python
def get_model_string(config: dict[str, str]) -> str | OpenAIModel:
    """Build a pydantic-ai model string or object from Hydra config.

    Args:
        config: Dict with optional 'provider', 'model', and 'base_url' keys.

    Returns:
        Model string like ``"openai:gpt-4"`` or an ``OpenAIModel`` for custom endpoints.
    """
    provider = config.get("provider", "openai")
    model = config.get("model", "gpt-4")
    base_url = config.get("base_url")

    if base_url:
        from pydantic_ai.models.openai import OpenAIModel
        return OpenAIModel(model, base_url=base_url)

    return f"{provider}:{model}"
```

This is backward-compatible: existing configs without `base_url` get the current string behavior. Gemma4 config with `base_url` gets an `OpenAIModel` object.

3. Update the `__init__.py` re-export if needed (the return type changes to `str | OpenAIModel` but callers just pass it to `.run_sync(model=...)` which accepts both).

### `swanki/audio/_common.py` (MODIFY)

**Current state:** Fish Speech server pool hardcoded at lines 264-322. TTS functions have no skip mechanism.

**Changes:**

1. **Replace hardcoded Fish Speech pool with `ServerPool`** (lines 264-322): Remove `_FISH_SPEECH_PORTS`, `_server_lock`, `_server_index`, `_healthy_servers`, `_servers_discovered`, `_discover_fish_speech_servers()`, `_pick_fish_speech_server()`. Replace with:

```python
from ..infra.server_pool import ServerPool

_fish_pool: ServerPool | None = None

def get_fish_speech_pool(base_url: str = "http://localhost:8080") -> ServerPool:
    global _fish_pool
    if _fish_pool is None:
        from urllib.parse import urlparse
        parsed = urlparse(base_url)
        host = f"{parsed.scheme}://{parsed.hostname}"
        _fish_pool = ServerPool(
            name="fish_speech",
            ports=[8080, 8081, 8082, 8083],
            health_path="/v1/health",
            base_host=host,
        )
    return _fish_pool
```

2. **Update `_tts_fish_speech()`** (line 348): Use `get_fish_speech_pool(server_url).pick()` instead of `_pick_fish_speech_server(server_url)`.

3. **Update `tts_chunks_parallel()`** (line 467): Use `get_fish_speech_pool(...).count()` instead of `len(_discover_fish_speech_servers(...))`.

### `swanki/audio/card.py` (MODIFY)

**Current state:** `generate_card_audio()` at line 324 interleaves LLM transcript generation with TTS per card.

**Changes:**

1. **Add `tts_enabled` parameter to `generate_card_audio()`:**

```python
def generate_card_audio(
    card: PlainCard,
    ...
    tts_enabled: bool = True,
    **tts_kwargs: object,
) -> tuple[str, str | None]:
```

2. **When `tts_enabled=False`:** generate transcripts, save to sidecar files (already done by `_save_card_transcripts()`), store on card objects, but skip all `text_to_speech()` calls and `combine_audio()` calls. Return filenames that would be generated (for later matching).

3. **Add `synthesize_card_audio_from_transcript()` function:**

```python
def synthesize_card_audio_from_transcript(
    card: PlainCard,
    card_index: int,
    audio_dir: Path,
    elevenlabs_api_key: str,
    voice_id: str | None = None,
    citation_key: str | None = None,
    speed: float = 1.0,
    **tts_kwargs: object,
) -> tuple[str, str | None]:
    """Synthesize audio from pre-generated transcripts stored on the card."""
```

This reads `card.audio_front_transcript` and `card.audio_back_transcript` (already set during transcript generation) and runs TTS only.

### `swanki/audio/reading.py` (MODIFY)

**Current state:** `generate_reading_audio()` does LLM (LaTeX humanize + transcript gen) then TTS.

**Changes:**

1. **Add `tts_enabled: bool = True` parameter.** When False: generate transcript, save to `full_read/{stem}_transcript.md`, but skip all `text_to_speech()` / `tts_chunks_parallel()` calls.

2. **Add `synthesize_reading_audio_from_transcript()` function:** Reads saved transcript file, runs TTS pipeline (chunking, parallel dispatch, assembly).

### `swanki/audio/summary.py` (MODIFY)

**Changes:** Same pattern as reading.py. Add `tts_enabled` param and `synthesize_summary_audio_from_transcript()`.

### `swanki/audio/lecture.py` (MODIFY)

**Changes:** Same pattern. Add `tts_enabled` param and `synthesize_lecture_audio_from_transcript()`.

### `swanki/pipeline/pipeline.py` (MODIFY)

**Current state:** 2827 lines. Orchestrates the full pipeline.

**Changes:**

1. **`convert_to_markdown()` (line 476):** Replace Mathpix with MinerU.

```python
def convert_to_markdown(self, pages: list[Path]) -> list[Path]:
    """Convert PDF to markdown using MinerU or Mathpix."""
    models_config = self.config.get("models", {}).get("models", {})
    ocr_provider = models_config.get("ocr", {}).get("provider", "mathpix")

    if ocr_provider == "mineru":
        from ..ocr.mineru import MinerUConverter
        gpu_config = models_config.get("gpu", {})
        device = gpu_config.get("device", "cuda:0")
        converter = MinerUConverter(self.output_base, device=device)
        # MinerU takes the original PDF, not split pages
        return converter.convert_pdf(self.state.pdf_path)
    else:
        # Existing Mathpix path (unchanged)
        ...
```

2. **`process_full()` (line 153):** Add GPU orchestration.

Before any GPU work, create the orchestrator:

```python
models_config = self.config.get("models", {}).get("models", {})
gpu_config = models_config.get("gpu", {})
gpu_mode = gpu_config.get("mode", "multi-gpu")

if gpu_mode == "single-gpu":
    from ..infra.gpu_orchestrator import GpuOrchestrator
    orchestrator = GpuOrchestrator(
        mode="single-gpu",
        gpu_device=gpu_config.get("device", "cuda:0"),
        gemma_config=gpu_config,
        fish_config=models_config.get("tts", {}),
    )
else:
    orchestrator = None
```

Phase 1 -- OCR: Run MinerU (if single-gpu, OCR loads/unloads its own models):

```python
if orchestrator:
    with orchestrator.ocr_phase():
        markdown_files = self.convert_to_markdown(pages)
else:
    markdown_files = self.convert_to_markdown(pages)
```

Phase 2 -- LLM: Start vLLM if single-gpu, run all LLM-dependent stages:

```python
if orchestrator:
    with orchestrator.llm_phase():
        cleaned_files = self.clean_markdown(markdown_files)
        image_summaries = self.process_images(cleaned_files)
        doc_summary = self.generate_document_summary(cleaned_files, image_summaries)
        # ... card gen, refinement, feedback ...
        # Audio transcripts (tts_enabled=False)
        self.generate_audio(cards, doc_summary, outputs, cleaned_files, image_summaries, tts_enabled=False)
else:
    # Existing flow unchanged
    ...
```

Phase 3 -- TTS: Start Fish Speech if single-gpu, run TTS from transcripts:

```python
if orchestrator:
    with orchestrator.tts_phase():
        self.synthesize_audio_from_transcripts(cards, doc_summary, outputs)
```

3. **`generate_audio()` (line 1828):** Add `tts_enabled: bool = True` parameter. Pass it through to each audio generator.

4. **New method `synthesize_audio_from_transcripts()`:** Calls the `synthesize_*_from_transcript()` functions for each audio type that was configured.

### `swanki/presentation/slide_generator.py` (MODIFY)

**Current state:** Uses `instructor.patch(OpenAI())` at line 65.

**Changes:**

1. Replace instructor with pydantic-ai:

```python
from pydantic_ai import Agent
from swanki.presentation.models import Presentation, PresentationSpec

_slide_agent: Agent[None, Presentation] = Agent(
    output_type=Presentation, retries=3
)

class SlideGenerator:
    def __init__(self, model: str = "openai:gpt-4o") -> None:
        self.model = model

    def generate(
        self,
        spec: PresentationSpec,
        doc_summary_text: str,
        image_summaries: dict[str, str],
    ) -> Presentation:
        user_prompt = USER_PROMPT_TEMPLATE.format(...)
        result = _slide_agent.run_sync(
            user_prompt,
            instructions=SYSTEM_PROMPT,
            model=self.model,
        )
        return result.output
```

2. Remove `import instructor` and `from openai import OpenAI`.

### `swanki/conf/models/gemma4.yaml` -- OCR section addition

Add OCR config alongside LLM/TTS:

```yaml
models:
  ocr:
    provider: mineru
    device: "cuda:0"
  llm:
    provider: openai
    model: gemma-4-31b-it
    base_url: http://localhost:8090/v1
    temperature: 0.7
    max_retries: 3
  tts:
    provider: fish_speech
    server_url: http://localhost:8080
    reference_id: british-prof
    temperature: 0.8
    format: mp3
  gpu:
    mode: single-gpu
    device: "cuda:0"
    gemma_model: nvidia/Gemma-4-31B-IT-NVFP4
    gemma_quantization: fp8
    gemma_port: 8090
    gemma_max_model_len: 32768
```

### `scripts/slurm/fish-speech.sbatch` (NEW)

**Purpose:** Document the current Fish Speech SLURM job setup (currently undocumented, jobs 839-842 were launched ad-hoc).

```bash
#!/bin/bash
#SBATCH --job-name=fish-speech
#SBATCH --partition=main
#SBATCH --gres=gpu:rtx6000:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --time=UNLIMITED
#SBATCH --output=logs/fish-speech-%j.log

# Usage: sbatch --export=GPU_ID=0,PORT=8080 fish-speech.sbatch
# Launch 4 instances: for i in 0 1 2 3; do sbatch --export=GPU_ID=$i,PORT=$((8080+i)) fish-speech.sbatch; done

GPU_ID=${GPU_ID:-0}
PORT=${PORT:-8080}

export CUDA_VISIBLE_DEVICES=$GPU_ID

docker run --gpus "device=$GPU_ID" \
  -p $PORT:8080 \
  --name fish-speech-$GPU_ID \
  --rm \
  fishaudio/fish-speech:latest \
  tools/api_server.py --listen 0.0.0.0:8080
```

### `scripts/slurm/gemma-vllm.sbatch` (NEW)

**Purpose:** Template for launching Gemma 4 vLLM as a SLURM job.

```bash
#!/bin/bash
#SBATCH --job-name=gemma-vllm
#SBATCH --partition=main
#SBATCH --gres=gpu:rtx6000:1
#SBATCH --cpus-per-task=16
#SBATCH --mem=64G
#SBATCH --time=UNLIMITED
#SBATCH --output=logs/gemma-vllm-%j.log

GPU_ID=${GPU_ID:-0}
PORT=${PORT:-8090}

export CUDA_VISIBLE_DEVICES=$GPU_ID

python -m vllm.entrypoints.openai.api_server \
  --model nvidia/Gemma-4-31B-IT-NVFP4 \
  --port $PORT \
  --quantization fp8 \
  --max-model-len 32768 \
  --trust-remote-code \
  --gpu-memory-utilization 0.95
```

### `tests/test_mineru.py` (NEW)

**Test cases:**

- `test_convert_pdf_produces_page_files` -- given a test PDF, MinerU produces `md-singles/page-N.md` files
- `test_image_extraction` -- MinerU extracts images and markdown references resolve
- `test_page_splitting_accuracy` -- page boundary detection matches expected page count
- `test_image_path_rewriting` -- image paths in markdown point to correct local files
- `test_fallback_when_no_page_markers` -- splits at headers if MinerU doesn't emit page markers

### `tests/test_server_pool.py` (NEW)

**Test cases:**

- `test_discover_healthy_servers` -- mock httpx to return healthy/unhealthy, verify discovery
- `test_round_robin_distribution` -- verify pick() cycles through servers evenly
- `test_thread_safety` -- concurrent pick() calls don't produce index errors
- `test_rediscovery_on_fewer_servers` -- when cached list shrinks, re-discovers
- `test_fallback_to_first_port` -- when no servers healthy, falls back to first port

### `tests/test_gpu_orchestrator.py` (NEW)

**Test cases:**

- `test_single_gpu_phases_sequential` -- verify phases don't overlap in single-gpu mode
- `test_multi_gpu_passthrough` -- verify no server management in multi-gpu mode
- `test_vllm_start_stop` -- mock subprocess, verify start waits for health, stop sends SIGTERM
- `test_context_manager_cleanup` -- verify server stopped even on exception

### `pyproject.toml` (MODIFY)

**Changes:**

1. Add `magic-pdf` (MinerU) to dependencies
2. Add `vllm` to optional dependencies (not everyone needs it)
3. Keep `instructor` for now (only used by legacy path, removal is a follow-up)

## Edge Cases

1. **MinerU produces no page markers.** Fall back to splitting at `##` headers, or if no headers, treat entire document as one "page" (the segmenter will handle chunking).

2. **MinerU image paths differ from Mathpix CDN URLs.** MinerU uses local relative paths. The `ImageProcessor._generate_image_summary()` already handles local images via `BinaryContent` (line 191-216). No change needed there.

3. **vLLM server fails to start (OOM, wrong model, etc.).** `VllmServer.start()` has a 120s timeout. If health check fails, raise with clear error message including GPU memory state.

4. **Gemma 4 structured output compatibility.** vLLM supports `guided_json` for structured output via the OpenAI-compatible API. pydantic-ai's OpenAI provider uses `response_format` which maps to this. Must empirically test with `card_gen_agent` (complex nested Pydantic model) before declaring the swap complete.

5. **Single-GPU memory fragmentation.** After stopping vLLM, CUDA memory may not fully release. If Fish Speech fails to start, add explicit `torch.cuda.empty_cache()` between phases, or use `CUDA_VISIBLE_DEVICES` isolation.

6. **Audio transcript files missing (interrupted run).** `synthesize_*_from_transcript()` functions should check for transcript file existence and log clear errors rather than crashing.

7. **Existing Mathpix config still works.** The `convert_to_markdown()` change is gated on `ocr.provider`. Default configs keep `mathpix` behavior. Users opt in to MinerU via `models=gemma4`.

8. **pydantic-ai OpenAI provider requires `OPENAI_API_KEY`.** When using vLLM, set `OPENAI_API_KEY=dummy` in the gemma4 config or environment. vLLM doesn't validate keys.

9. **Lecture module has duplicate `_humanize_latex` and `_LATEX_SYSTEM_PROMPT`.** Both `_common.py:870` and `reading.py:287` have their own copies. Not in scope for this plan, but the plan should not break this duplication.

10. **MinerU GPU memory consumption.** MinerU's layout analysis and OCR models use ~6-10 GB. In single-GPU mode, this must fully unload before vLLM starts. MinerU's Python API should handle this if we don't hold references to its models.

## Verification

1. **Unit tests:**

   ```
   pytest tests/test_mineru.py tests/test_server_pool.py tests/test_gpu_orchestrator.py -xvs
   ```

2. **Type check:**

   ```
   mypy swanki/ocr/ swanki/infra/ swanki/llm/agents.py swanki/audio/_common.py
   ```

3. **Lint:**

   ```
   ruff check swanki/ocr/ swanki/infra/ swanki/llm/agents.py swanki/audio/ swanki/pipeline/pipeline.py swanki/presentation/slide_generator.py
   ```

4. **Integration test (single-GPU, test paper):**

   ```bash
   # Ensure no other GPU jobs running
   squeue  # should show no jobs

   # Run pipeline with gemma4 config
   swanki pdf_path=/scratch/projects/torchcell-scratch/Swanki_Data/luoWhenCausalInference2020/luoWhenCausalInference2020.pdf \
     citation_key=luoWhenCausalInference2020 \
     models=gemma4 \
     audio=all
   ```

5. **Verify output quality:**
   - Check `md-singles/` for complete page extraction (compare page count to original PDF)
   - Check `image-summaries/` for vision model output quality
   - Check `cards-plain.md` for card quality and structured output compliance
   - Check audio files for TTS quality
   - Compare results to a run with `models=default` (OpenAI) for quality regression

## Execution

To implement, start a new Claude Code session:

```
/read-codebase
```

Then:

```
Implement the plan at notes/plan.open-source-pipeline-mineru-ocr-gemma-4-llm.2026.04.15.md. Read the plan first, then implement each file specification in order. Run verification after each file. Commit with /update-notes -> /stage -> /commit after each logical unit.
```

**Implementation order (respects dependencies):**

1. `swanki/infra/server_pool.py` + tests (no deps)
2. `swanki/infra/vllm_server.py` (depends on 1)
3. `swanki/infra/gpu_orchestrator.py` + tests (depends on 2)
4. `swanki/llm/agents.py` modification (independent)
5. `swanki/conf/models/gemma4.yaml` (depends on 4)
6. `swanki/audio/_common.py` modification (depends on 1)
7. `swanki/audio/card.py` modification (depends on 6)
8. `swanki/audio/reading.py` modification (depends on 6)
9. `swanki/audio/summary.py` modification (depends on 6)
10. `swanki/audio/lecture.py` modification (depends on 6)
11. `swanki/ocr/mineru.py` + tests (independent)
12. `swanki/pipeline/pipeline.py` modification (depends on all above)
13. `swanki/presentation/slide_generator.py` modification (depends on 4)
14. SLURM scripts (independent)
15. Integration test on `luoWhenCausalInference2020`

## Critic Review

A full-codebase critic review was performed. All findings have been addressed below.

### Feasibility Issues (all resolved)

**F1. `pipeline.py:1952` imports `_discover_fish_speech_servers` directly.**
The line `from ..audio._common import _discover_fish_speech_servers` in `pipeline.py:1952` will break after the `_common.py` refactor removes that function. **Fix:** add to `pipeline.py` MODIFY spec: change this import to `from ..infra.server_pool import ServerPool` and update the usage at line 1955 to use `get_fish_speech_pool(server_url).count()` instead of `len(_discover_fish_speech_servers(server_url))`. Also update the import at line 1952-1953.

**F2. Type annotation mismatch: `model: str` in audio generators.**
`get_model_string()` now returns `str | OpenAIModel`. All four audio generators (`card.py:30`, `reading.py:40`, `summary.py:37`, `lecture.py:41`) have `model: str = "openai:gpt-5-mini"` parameters. pydantic-ai's `.run_sync(model=...)` accepts both types, so these annotations should widen to `model: str | Any = "openai:gpt-5-mini"` or use a type alias. **Fix:** define `ModelType = str | Any` in `llm/agents.py` and re-export it. Update all audio module `model:` params to use it. For simplicity the implementation can just use `model: str | object` since pydantic-ai is duck-typed on this parameter.

**F3. vLLM `--device` flag does not exist.**
vLLM uses `CUDA_VISIBLE_DEVICES` env var, not a `--device` CLI flag. **Fix:** Remove `--device` from the `VllmServer.start()` command. GPU selection is already done via `CUDA_VISIBLE_DEVICES` in the env dict.

**F4. `OPENAI_API_KEY` must be set for pydantic-ai's OpenAI provider.**
When using vLLM, pydantic-ai still looks for `OPENAI_API_KEY`. **Fix:** `VllmServer.start()` should set `OPENAI_API_KEY=not-needed` in its env. Also add a note in `gemma4.yaml` comments and in `.env.example`.

**F5. Fish Speech lifecycle in `GpuOrchestrator.tts_phase()` is unspecified.**
The existing Fish Speech deployment uses Docker containers via SLURM. In single-GPU mode, the orchestrator needs to start/stop a Fish Speech container. **Fix:** `GpuOrchestrator.tts_phase()` will launch Fish Speech via `docker run --rm --gpus device={gpu_id} -p {port}:8080 fishaudio/fish-speech:latest` as a subprocess (same as current SLURM jobs but without sbatch). Use the same health-check pattern as vLLM. Add a `FishSpeechServer` class in `swanki/infra/fish_speech_server.py` mirroring `VllmServer`.

### Completeness Gaps (all resolved)

**C1. `swanki/infra/fish_speech_server.py` is missing.**
Added to file specs. Mirrors `VllmServer` but launches Docker container.

**C2. `swanki/audio/__init__.py` needs re-exports for new synthesize functions.**
The new `synthesize_*_from_transcript()` functions need to be importable. **Fix:** add re-exports to `audio/__init__.py`.

**C3. `swanki/processing/__init__.py` unchanged but `MarkdownConverter` may need updating.**
`MarkdownConverter` is dead code (not used by the main pipeline path). No change needed. Can be deprecated in a follow-up.

**C4. Duplicate `gemma4.yaml` listing.**
The plan listed the yaml twice (lines 305 and 575). **Fix:** These are one file. The second listing adds the `ocr:` section. The final yaml should contain all three sections (ocr, llm, tts, gpu).

**C5. `pipeline.py` MODIFY spec is underspecified (rated RED by critic).**
Additional detail for the `pipeline.py` changes:

- **Where to insert orchestrator creation:** After `self.state = ProcessingState(...)` at line 215, before the stage loop begins.
- **`convert_to_markdown()` change location:** Lines 476-541. The MinerU branch bypasses the page-by-page loop entirely. The `pages` parameter is still passed (from `split_pdf`) but ignored when using MinerU (MinerU re-reads the original PDF).
- **`split_pdf()` still runs:** In MinerU mode, `split_pdf()` still runs to get page count (used by segmenter). But its output is not fed to OCR. Alternatively, `convert_to_markdown()` with MinerU can also return page count from MinerU's metadata. For simplicity: skip `split_pdf()` entirely when using MinerU and get page count from MinerU output.
- **`generate_audio()` with `tts_enabled=False`:** Guard each `text_to_speech()`, `tts_chunks_parallel()`, and `combine_audio*()` call behind `if tts_enabled:`. The transcript generation and saving already happen before TTS in each audio module.
- **`synthesize_audio_from_transcripts()` skeleton:**

```python
def synthesize_audio_from_transcripts(
    self,
    cards: list[PlainCard],
    summary: DocumentSummary,
    outputs: dict[str, Path],
) -> None:
    """Run TTS from pre-generated transcript sidecars (single-GPU phase 3)."""
    audio_config = self.config.get("audio", {}).get("audio", {})
    # ... setup tts_kwargs same as generate_audio() lines 1872-1908 ...

    if audio_config.get("generate_complementary", False) and cards:
        from ..audio.card import synthesize_card_audio_from_transcript
        for i, card in enumerate(cards):
            front_fn, back_fn = synthesize_card_audio_from_transcript(
                card, i + 1, audio_dir, elevenlabs_api_key, voice_id,
                self.citation_key, speed, **tts_kwargs
            )
            # ... set audio URIs on cards ...

    if audio_config.get("generate_summary", False):
        from ..audio.summary import synthesize_summary_audio_from_transcript
        synthesize_summary_audio_from_transcript(
            transcript_dir=self.output_base / "summary_transcript",
            output_path=summary_audio_path,
            # ... same TTS params ...
        )
    # ... repeat for reading and lecture ...
```

- **Direct import fix (line 1952-1953):** Replace:

  ```python
  from ..audio._common import _discover_fish_speech_servers
  ```

  With:

  ```python
  from ..audio._common import get_fish_speech_pool
  ```

  And update line 1955:

  ```python
  num_servers = get_fish_speech_pool(
      str(tts_kwargs.get("server_url", "http://localhost:8080"))
  ).count()
  ```

### Specification Quality Summary

After addressing the above findings:

| File Spec | Rating |
|-----------|--------|
| `swanki/ocr/__init__.py` | GREEN |
| `swanki/ocr/mineru.py` | YELLOW (MinerU API specifics need empirical testing) |
| `swanki/infra/__init__.py` | GREEN |
| `swanki/infra/server_pool.py` | GREEN |
| `swanki/infra/vllm_server.py` | GREEN (after --device removal) |
| `swanki/infra/fish_speech_server.py` | GREEN (new, mirrors vllm_server) |
| `swanki/infra/gpu_orchestrator.py` | GREEN (after Fish Speech lifecycle clarification) |
| `swanki/conf/models/gemma4.yaml` | GREEN |
| `swanki/llm/agents.py` | GREEN |
| `swanki/audio/_common.py` | GREEN |
| `swanki/audio/card.py` | YELLOW (TTS guard points identifiable from code) |
| `swanki/audio/reading.py` | YELLOW (same) |
| `swanki/audio/summary.py` | YELLOW (same) |
| `swanki/audio/lecture.py` | YELLOW (same) |
| `swanki/pipeline/pipeline.py` | YELLOW (improved from RED with added detail) |
| `swanki/presentation/slide_generator.py` | GREEN |
| SLURM scripts | GREEN |
| Tests | YELLOW (test cases clear, implementation requires mocking) |
| `pyproject.toml` | GREEN |

All RED ratings resolved. Remaining YELLOW items are implementable by an agent that reads the existing code alongside the plan.
