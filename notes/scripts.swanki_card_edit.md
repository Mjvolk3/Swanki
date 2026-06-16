---
id: xtebfozdnl8j7coopuvw2kz
title: Swanki_card_edit
desc: ''
updated: 1781900000000
created: 1781900000000
---

## 2026.06.15 - SLURM-native surgical card audio edit launcher + Anki swap

Thin launcher mirroring [[scripts.swanki_audio_edit]] for CARD audio. Applies
ONE precise edit to ONE chunk of ONE card side via
[[swanki.audio.card_edit]] (`edit_card_chunk`) against the job-private Fish
server (`SWANKI_FISH_PORTS`). Plan:
[[plan.precise-card-audio-editing.2026.06.15]].

`scripts/swanki_card_edit.py`:

- Args: `--card-manifest` (or `--output-dir` + `--card-uuid`), `--side`,
  `--idx` (tts-chunk-local), one of `--speech-only` / `--comment` / `--new-text`,
  `--voice`, `--model` (comment path), optional `--anki`.
- Reuses `swanki_audio_edit.build_fish_tts_kwargs` to assemble `tts_kwargs` from
  the `swanki/conf/models/<voice>.yaml` config, resolves the in-job Fish URL
  from `SWANKI_FISH_PORTS`, calls `ensure_fish_speech_reference` to register the
  voice on the in-job server BEFORE editing, then dispatches to
  `edit_card_chunk`.
- `swap_anki_media(side_mp3, sound_filename, url)` (decoupled, called only when
  `--anki` is passed): AnkiConnect `storeMediaFile` writes the base64 of the
  rewritten side mp3 under the EXISTING `[sound:...]` filename (stable, so the
  note reference is untouched) then one `sync`. Kept OUTSIDE `edit_card_chunk`
  so the editor stays pure and testable; defaults the filename to the side mp3
  basename.

`scripts/swanki_card_edit.sbatch`: copy of `swanki_audio_edit.sbatch` -- one
GPU, serverless Fish in-job via `apptainer --nv` (Fish bring-up block verbatim),
derive a free port, health-poll, export `SWANKI_FISH_PORTS`, run
`swanki_card_edit.py`, tear Fish down. Inputs via `SWANKI_CARD_*` env vars
(`SWANKI_CARD_MANIFEST/SIDE/IDX/MODE/VOICE/PAYLOAD/MODEL/ANKI`).

Retires `scripts/regen_card_audio_side.py` + `.sbatch` (their whole-side re-TTS
behavior is folded into `edit_card_chunk`'s fallback).
