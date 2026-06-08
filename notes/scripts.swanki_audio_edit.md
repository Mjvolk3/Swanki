---
id: scr1swankiaudioedit0slurm
title: Swanki Audio Edit (SLURM surgical)
desc: ''
updated: 1780949000000
created: 1780949000000
---

## 2026.06.08 - SLURM-native surgical audio edit

Post-cutover ([[runbook.slurm-cutover]]) the persistent Docker Fish fleet at
`localhost:8080` is gone, so the `audio-fix-from-annotations` skill's apply step
(a single-chunk re-TTS via `swanki.audio.comment_edit.edit_chunk`) had no Fish to
hit. This pair restores that path the SLURM-native way: one `--gres=gpu:1` job
brings Fish up in-job on its allocated GPU (the same `apptainer exec --nv` cgroup
child as [[scripts.swanki_job]]), runs exactly one `edit_chunk`, and tears Fish
down. SLURM places it on whatever GPU is free, so it runs alongside in-flight
generation jobs without contention.

- **`scripts/swanki_audio_edit.sbatch`** - the one-GPU job. Inputs via env
  (`SWANKI_EDIT_MANIFEST`, `SWANKI_EDIT_IDX`, `SWANKI_EDIT_MODE` =
  speech_only|comment|new_text, `SWANKI_EDIT_VOICE`, `SWANKI_EDIT_SPEED`,
  `SWANKI_EDIT_PAYLOAD`, `SWANKI_EDIT_MODEL`). Reuses the proven Fish bring-up +
  health-wait + EXIT/TERM/INT reap. No Layer-2 supervisor: the edit is seconds of
  TTS, not a 70-minute run, so a respawn loop would be overkill.
- **`scripts/swanki_audio_edit.py`** - thin launcher. Builds the fish_speech
  `tts_kwargs` from `swanki/conf/models/<voice>.yaml` exactly as
  `pipeline._setup_tts` does (the manifest does NOT store the voice), overrides
  `server_url` to the job-private `SWANKI_FISH_PORTS`, and calls `edit_chunk`. It
  owns no edit logic - the agent rewrite / re-TTS / restitch / `_edits/` audit all
  stay in `edit_chunk` ([[swanki.audio.comment_edit]]).

Gotcha: `--speed` MUST match the chapter's original render speed (lecture =
`lecture_speed`, e.g. 1.0 for Hamming under `audio=all`), or the re-rolled chunk's
tempo drifts from its neighbors. The voice config and the chunk manifest do not
record speed; it comes from the `audio=` group, so the caller passes it.

First use: Hamming CH01 (orientation) lecture chunk 12 - an orange ABS bookmark
("whooshing sound right after obsolescence") drove a speech-only re-roll. Job 885
COMPLETED in ~4 min on the free GPU while 882/883/884 generated; new chunk-12
window (344663, 373824) ms.
