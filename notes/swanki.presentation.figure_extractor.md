---
id: 3y6rnqb4bufz2eaakld1ltm
title: Figure_extractor
desc: ''
updated: 1773789879489
created: 1773789879489
---

## 2026.03.17 - Add figure extraction and cropping from PDFs

Extracts figures from PDF pages using `pdftoppm` (poppler) at 300 DPI and optionally crops sub-panels using PIL. In practice, Mathpix CDN URLs with server-side cropping proved more reliable for initial extraction, with local PIL cropping from downloaded composites for sub-panel isolation (e.g., splitting Fig 2 into panels a-f).
