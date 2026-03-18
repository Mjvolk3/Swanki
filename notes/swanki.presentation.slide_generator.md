---
id: 3iikem69b4gvavyw232rn69
title: Slide_generator
desc: ''
updated: 1773789880679
created: 1773789880679
---

## 2026.03.17 - Add LLM-driven slide content generation

Single instructor call with `response_model=Presentation` generates the full slide deck structure from document summary + image descriptions + user instructions. System prompt guides academic style, figure placement, and layout choices. Follows the same instructor pattern as `pipeline.py`'s `generate_document_summary()`.
