---
id: hrgpekoh09ylrxvjuhdufoc
title: Swanki_replace_card
desc: ''
updated: 1783475209000
created: 1783475209000
---

## 2026.07.07 - SLURM-native surgical card replacement harness

`scripts/swanki_replace_card.py` + `scripts/swanki_replace_card.sbatch` mirror the
stable [[scripts.swanki_card_edit]] trio, dispatching to
[[swanki.audio.card_replace]] `replace_card` instead of `edit_card_chunk`. Plan:
[[plan.surgical-card-replacement.2026.07.07]].

**CLI (`swanki_replace_card.py`).** Resolves the card manifest from `--card-manifest`
OR `--output-dir` + `--card-uuid`; reads the new side prose from `--new-front` /
`--new-back` (or `--new-front-file` / `--new-back-file`). Reuses
`swanki_audio_edit.build_fish_tts_kwargs` to assemble `tts_kwargs` from the voice yaml
against the job-private Fish (`SWANKI_FISH_PORTS`), registers the reference voice via
`ensure_fish_speech_reference`, and resolves the AnkiConnect endpoint via
`delivery.targets.anki.default_ankiconnect_url` (env override `ANKICONNECT_URL`).
`--voice` and `--citation-key` are required; `--note-id` is the text-only override;
`--no-sync` skips the final AnkiWeb sync. The collection mutation only fires with
`--anki` — WITHOUT it the tool prints the resolved plan (dry-run) and touches nothing,
a safety default given `replace_card` is inherently a live patch.

**sbatch (`swanki_replace_card.sbatch`).** Same in-job Fish bring-up as
`swanki_card_edit.sbatch`: one allocated GPU, serverless Fish via `apptainer --nv`
(`COMPILE=0` — a short edit does not amortize compile), a curl `/v1/health` gate, then
export `SWANKI_FISH_PORTS`, `conda activate swanki`, run the CLI, and tear Fish down via
a bash `trap` (NOT the SLURM epilog, which reaps cross-job GPU procs). Inputs are env
vars (`SWANKI_CARD_MANIFEST`, `SWANKI_CARD_CITEKEY`, `SWANKI_CARD_FRONT`,
`SWANKI_CARD_BACK`, `SWANKI_CARD_VOICE`, `SWANKI_CARD_NOTEID`, `SWANKI_CARD_ANKI`,
`SWANKI_CARD_NOSYNC`).

First real use: replace the 5 mis-shipped alcamo cards (CH01, CH03, CH04 x2, CH05).
Pre-flight each card's `card_chunks/{uuid}_manifest.json` presence — audio+field path
when present, `--note-id` text-only when absent.
