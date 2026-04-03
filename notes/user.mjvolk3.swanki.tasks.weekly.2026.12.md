---
id: ybd7pbkmfbi2ftclm3l4qa6
title: '12'
desc: ''
updated: 1775113636225
updated: 1775112135144
created: 1773789797704
---
## 2026.03.17

- [x] Built `swanki/presentation/` package for generating Reveal.js slide presentations from Swanki-processed paper data with LLM-driven content, figure extraction, and pandoc rendering [[swanki.presentation]]
- [x] Generated 18-slide Merzbacher FCL paper presentation with cropped figure panels, KaTeX math, mermaid diagrams, and pointer plugin [[plan.presentation-generation-revealjs]]
- [x] Documented Reveal.js presentation pain points (image sizing, overflow, no WYSIWYG) and evaluated programmatic PPTX alternatives (python-pptx, Marp, pandoc) -- recommending python-pptx for future [[scratch.2026.03.17.presentation-generation-experience]]

## 2026.03.19

- [x] Wrote plan for replacing ElevenLabs with open-source TTS models (F5-TTS, Kokoro-82M, Fish S2 Pro) running via Docker/Slurm on GPU workstation with 4x RTX 6000 [[plan.open-source-tts]]
- [x] Fixed VS Code keybindings for moving editor tabs between groups when terminal has focus (added `terminal.integrated.commandsToSkipShell` for all 6 `ctrl+alt+{u,o,i,k,j,l}` bindings)
