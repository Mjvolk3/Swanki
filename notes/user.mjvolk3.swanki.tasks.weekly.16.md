---
id: 3q5fy1xegyfyty5glti1765
title: '16'
desc: ''
updated: 1776290433298
created: 1776290419183
---
## 2026.04.15

- [x] Distribute Fish Speech audio across multiple GPU servers via round-robin discovery and a parallel chunk helper [[swanki.audio._common]]
- [x] Flatten lecture chunks into one job list and dispatch in parallel for Fish Speech [[swanki.audio.lecture]]
- [x] Flatten reading chunks into one job list and dispatch in parallel for Fish Speech [[swanki.audio.reading]]
- [x] Flatten summary chunks into one job list and dispatch in parallel for Fish Speech [[swanki.audio.summary]]
- [x] Add content_key to the pipeline and parallelize card audio across Fish Speech servers [[swanki.pipeline.pipeline]]
- [x] Bundle Zotero uploads into a single zip per run and harden item lookup plus upload timeouts [[swanki.sync.zotero]]
- [x] Forward content_key from the CLI into the pipeline [[swanki.__main__]]
