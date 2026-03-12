---
id: j7t0d21ffi1dlhw8xb8g0u6
title: Image_processor
desc: ''
updated: 1772076526748
created: 1772076526748
---

## 2026.02.25 - Resize oversized remote images before sending to vision API

Remote images with dimensions exceeding 2000px (encoded in URL query params) are now downloaded, resized with Lanczos resampling, and re-encoded as base64 JPEG before being sent to the OpenAI vision model. This prevents API failures from oversized image payloads while preserving image quality at a reasonable resolution.

- Parses `height`/`width` query parameters from the image URL to detect oversized images
- Downloads and resizes using PIL, maintaining aspect ratio with a 2000px max dimension cap
- Converts to JPEG at 85% quality and re-encodes as a data URI

## 2026.03.12 - Migrate from OpenAI client to pydantic-ai agents and modernize code

Replaced direct `OpenAI` vision API calls with `text_agent.run_sync()` using pydantic-ai `BinaryContent` and `ImageUrl` for provider-agnostic image handling. Constructor now takes `model: str` instead of `openai_client: OpenAI`.

- Rewrote module with proper frontmatter docstring, Google-style docstrings (from NumPy-style), `from __future__ import annotations`.
- Replaced deprecated `typing.List`, `Dict`, `Optional`, `Tuple` with modern `list`, `dict`, `| None` syntax.
- Fixed `any` (builtin) to `Any` (typing) in all type annotations.
- Removed unused imports (`shutil`, `os`, `dotenv.load_dotenv`).
- Fixed `PILImage.LANCZOS` to `PILImage.Resampling.LANCZOS` and PIL type narrowing for `img.resize()`.
- Introduced `ImageInfo = dict[str, Any]` type alias for readability.
- All ruff and mypy --strict errors resolved. Part of Step 5 ([[plan.major-refactor-sequence.plan-0]]).
