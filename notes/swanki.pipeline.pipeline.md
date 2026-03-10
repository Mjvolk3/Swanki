---
id: gc296t2rsgc6sx28n224rgq
title: Pipeline
desc: ''
updated: 1773013975831
created: 1773013975831
---

## 2026.03.08 - Integrate ApkgExporter for direct .apkg output

Wire the new `ApkgExporter` into the pipeline so that `.apkg` files are generated alongside markdown card output when `create_anki_deck` is configured. The exporter runs after plain card writing (step 8) and again after audio generation (step 9b) to produce a final deck with audio URIs. This removes the dependency on a running AnkiConnect instance for basic deck creation.

## 2026.03.10 - Update audio imports to new swanki.audio package

Redirect audio function imports from `..utils.audio` to `..audio` following the refactor of the monolithic audio module into a standalone package.
