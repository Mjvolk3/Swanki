---
id: scr1swankifinalizeabs0singleton
title: Swanki Finalize ABS (sbatch)
desc: ''
updated: 1780790000000
created: 1780790000000
---

`scripts/swanki_finalize_abs.sbatch` -- the debounced ABS refresh as a SLURM
singleton job.

## 2026.06.06 - created

The bash drainer fired one ABS refresh on the busy->idle edge. Under SLURM,
parallel independent jobs have no single idle edge, so each [[scripts.swanki_job]]
touches an `abs-dirty` flag after Anki delivery and this job -- submitted with
`--dependency=singleton --job-name=swanki-abs` (baked into the script) -- runs
`python -m swanki.delivery finalize-abs` exactly once at a time, clearing the flag
on success. No GPU. Mirrors the drainer's `finalize_abs()` semantics
([[scripts.swanki_queue]]). See [[runbook.slurm-cutover]].

## 2026.06.09 - Default slurm log path moved out of the repo root

Header `--output` fallback now `/home/michaelvolk/.swanki-queue/logs/slurm-abs-%j.log`
(same root-pollution fix as [[scripts.swanki_audio_edit]]).
