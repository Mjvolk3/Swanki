---
id: qwn40s9t72hnqfsrjakyy3j
title: Models
desc: ''
updated: 1773789878354
created: 1773789878354
---

## 2026.03.17 - Add Pydantic models for structured presentation output

Defines the data models that the LLM returns via instructor: `FigureRef` (page + crop box + label), `MermaidDiagram`, `Slide` (title, content, speaker notes, figures, layout), `PresentationSpec` (user instructions), and `Presentation` (complete slide deck). These enforce structured output so slide generation is controlled by schema rather than prompt engineering.
