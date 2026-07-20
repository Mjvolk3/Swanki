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

## 2026.06.09 - Multi-chunk edits + the --export comma gotcha

`swanki_audio_edit.py --idx` now accepts a LIST (split on `,` / `:` / whitespace),
applied sequentially in one Fish session. Sequential edits on the same manifest
compound correctly: each `edit_chunk` re-reads the manifest (with prior edits
applied) and restitches, so order is well-defined. This is the right shape for
multiple comments on one chapter -- one Fish cold-start, not N -- and it is also
why the edits MUST be serial: two parallel jobs on the same manifest would race
the restitch + `chunk_timeline.json` rewrite.

**Gotcha (cost a wasted job):** SLURM `sbatch --export=ALL,VAR=val,...` uses commas
as its own delimiter, so `SWANKI_EDIT_IDX="9,19"` in the `--export` list is parsed
as `SWANKI_EDIT_IDX=9` plus a garbage `19"` token -- the job silently edits only
chunk 9. Use a colon in the SLURM submit (`SWANKI_EDIT_IDX=9:19`), or `export` the
var in the shell first and pass bare `--export=ALL`. The launcher accepts all three
separators so the colon form just works.

First multi-chunk use: Hamming CH02 lecture chunks 9 + 19 (speech-only re-rolls),
from two 2026-06-08 ABS bookmarks (chunk 9 "ends on a strange nonconclusive note",
chunk 19 "blip"). Paired with the bookmark-wipe-on-replace policy: the two
addressed bookmarks are deleted after the new audio lands. See
[[project_abs_crud_build]] (windowed-wipe default, still to be automated).

## 2026.06.09 - Default slurm log path moved out of the repo root

Direct `sbatch scripts/swanki_audio_edit.sbatch` submissions dumped `slurm-%j.log`
into the submit cwd (the repo root) because the header's relative `--output` was
only ever overridden by `swanki_enqueue.sh` (`$QUEUE_DIR/logs/slurm-%j.log`).
All three sbatch headers now default to the same absolute
`/home/michaelvolk/.swanki-queue/logs/` location (SBATCH directives do not
expand `~`/`$HOME`, hence the literal path -- consistent with the queue's
convention), and `slurm-*.log` is gitignored as a backstop. Found while running
the CH03 surgical-edit chain by hand.

## 2026.06.09 - --collapse-pauses remediation mode

New mutually-exclusive mode (`SWANKI_EDIT_MODE=collapse_pauses`): per index,
collapse stacked pause tags in the STORED manifest text via
`collapse_stacked_pause_tags`, then re-roll verbatim through the speech_only
path; chunks with no stack are skipped. Deliberately does NOT use the new_text
path -- stored text is post-preprocessor and `add_tts_pauses` is not
idempotent, so re-running the full chain would stack tags again (exactly how
the CH03 chunk-3 pause insert became a triple). Built to remediate the 28
stacked chunks across the live Hamming chapters ([[swanki.audio._common]]).

### Gotcha: concurrent edit jobs get SIGKILLed (2026.06.09)

Running 4 edit jobs in parallel (one per GPU) killed 6 of 9: each victim died
~4:10 after ITS start mid-TTS with a bare SIGKILL (no kernel OOM logged, SLURM
state FAILED not OUT_OF_MEMORY, MaxRSS well under the 32G request), exactly one
survivor per scheduling wave. The same workloads rerun strictly sequentially
(afterany chain) all completed. Root cause undiagnosed -- until it is, submit
edit jobs ONE AT A TIME. Recovery note: stdout is block-buffered, so a killed
job's log under-reports progress; the collapse/text state on disk is ahead of
the log.

## 2026.07.20 - `--verbalize-numbers` retrofit mode

Fourth edit mode, the same shape as `--collapse-pauses`: rewrite the STORED
(post-preprocessor) chunk text deterministically, skip chunks the transform
leaves unchanged, then re-roll verbatim through the `speech_only` path. Applies
`verbalize_large_numbers` (see [[swanki.audio._common]] 2026.07.20), which
retrofits the scrubber onto a lecture rendered before it existed — no LLM
re-run, no re-chunking, and no risk of the `add_tts_pauses` double-stacking that
the `new_text` path would cause. Pass the full index range and let it skip the
clean chunks.
