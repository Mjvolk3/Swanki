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
