---
id: 0ltb6tnuikdyy1zswq4uph7
title: 09
desc: ''
updated: 1772137856820
created: 1772072267037
---
## 2026.02.25

- [x] Ported skills, scripts, VS Code tasks, and pre-commit config from iBioFoundry-AI; switched from black/isort to ruff [[workspace.ibiofoundry-ai.update.plan-0]]
- [x] Resize oversized remote images before sending to vision API in image_processor [[swanki.processing.image_processor#20260225---resize-oversized-remote-images-before-sending-to-vision-api]]
- [x] Added git worktree setup script, .gitattributes merge=union for weekly notes, and updated .gitignore
- [x] Added Zendron and other workspace dirs to Claude Code settings
- [x] Set dendron note ref aliasMode to none for insertNoteLink and copyNoteLink to avoid aliases by default
- [x] Added montanolopezPhysiologicalLimitationsOpportunities2022 to CO-Biotech2026 paper list [[scratch.2026.02.06.104018-CO-Biotech2026-papers]]
- [x] Implemented zotero-paper-import script and skill -- download, cut refs, prepare _clean.pdf and .sh in one command [[scripts.zotero_paper_import]]
- [x] Plan for Zotero-to-Swanki_Data automation: download PDFs by citation key, cut refs, produce_clean.pdf and .sh [[swanki.zotero-paper-import.plan-0]]
- [ ] Integrate with book player.

## 2026.02.26

- [x] Added qpdf fallback so malformed PDFs that crash PyPDF2 are still split page-by-page [[swanki.processing.pdf_processor#20260226---add-qpdf-fallback-for-malformed-pdfs]]

***

- [ ] Cite pydantic in paper.
- [ ] Integrate edits from @Shekhar-Mishra
