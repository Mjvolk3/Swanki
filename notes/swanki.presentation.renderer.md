---
id: qgl4yo4ej143vo2lfztr3ki
title: Renderer
desc: ''
updated: 1773789881762
created: 1773789881762
---

## 2026.03.17 - Add Reveal.js HTML renderer via pandoc

Converts `Presentation` model to pandoc markdown (YAML front matter + slide separators) then renders to HTML via `pandoc -t revealjs`. Uses `markdown-implicit_figures` to suppress captions, KaTeX for math, mermaid-filter for diagrams (at 4x scale), and injects the quarto-ext/pointer plugin for laser pointer (Q key toggle). Lesson learned: Reveal.js requires extensive CSS overrides for academic use and a local HTTP server for Chrome compatibility. Future direction: switch to python-pptx for PPTX output.
