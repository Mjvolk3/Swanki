---
id: estx713x13ymspbk1qym1ko
title: Projections
desc: ''
updated: 1781029302435
created: 1781029302435
---

## 2026.06.09 - Single home for projection routing

The citation-key fallback chain (`data.citationKey` -> `"Citation Key:"` regex
on `extra` -> Zotero item key), `resolve_library`, `classify`, and `group_key`
were copy-pasted across three scripts; they live here once. `projections.yml`
stays external hand-tuned infra data (`~/Documents/projects/infra/abs/`),
never Hydra-ized; every entry point takes a `projections_path` with that
expanduser default.

- Configs stay raw dicts deliberately: `scripts/swanki_anki_sync.py` and its
  tests consume the dict shape directly, and pydantic-izing them would force
  churn for no functional gain.
- `kind_for_key` infers Paper/Book from the `_CH##_` suffix alone -- used by
  the targeted refresh, which works from local artifacts without a Zotero
  round trip (the full refresh classifies from the Zotero item type).
