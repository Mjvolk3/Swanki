## Dendron Paths

Example:
[[Paper|Paper]] exists here `/Swanki/notes/Paper.md`

Example

![](./assets/images/fix_cloze.md.issue-with-cloze-card-no-data-in-extra.png) exists here `Swanki/notes/assets/images/fix_cloze.md.issue-with-cloze-card-no-data-in-extra.png`

## Coding Advice

- Don't be superfluous
- Don't use try except blocks - fail fast minimize other types of exception coding like by using excessive conditionals

## Python File Format

Every `.py` file starts with a single frontmatter docstring. The module description (if any) goes in the same block -- never a separate docstring.

```python
"""
swanki/audio/card.py
[[swanki.audio.card]]
https://github.com/Mjvolk3/Swanki/tree/main/swanki/audio/card.py
Test file: tests/test_audio_card.py

Flashcard audio generation with cloze handling and citation prefixing.
"""
```

Use **Google-style docstrings** for functions and classes (`Args:`, `Returns:`, `Raises:`). Ruff enforces `convention = "google"`. Keep docstrings concise -- no verbose parameter descriptions that duplicate type annotations. Pydantic models use `Field(description="...")` instead of docstrings for fields.

## Pydantic Models

- We want to use pydantic models to structure output as much as possible as opposed to controlling output by changing prompts.

## Files

- Tests should go in `tests/`

## Data Formats (YAML vs JSON)

- **YAML for hand-edited config** — Hydra config groups (`swanki/conf/**`) and anything a human authors/tunes by hand.
- **JSON for emitted output** — machine-written artifacts the pipeline produces (audit logs, run records, structured results). Use `json.dump(payload, f, indent=2, ensure_ascii=False)` so prose and unicode stay readable.
- Some legacy emitted artifacts (`problem-pairings.yaml`, `section-classification.yaml`, `cards-debug.yaml`, `provenance.yaml`) predate this rule and are still YAML; migrate them to JSON opportunistically, not in unrelated PRs.

## Code Execution

- `~/miniconda3/envs/swanki/bin/python script.py` — the conda root is `~/miniconda3`
  on gilahyper (it is `~/opt/miniconda3` on the Mac), so prefer `conda activate swanki`
  over a hardcoded interpreter path when a script may run on either machine.
- Activate rather than calling the interpreter directly whenever the code shells out:
  `ffmpeg`/`ffprobe` are only on `PATH` inside the env, and the test suite fails ~37
  tests with `FileNotFoundError: 'ffmpeg'` without it.
- Only when running `ocr=mathpix` (the default is `ocr=mineru`): the Mathpix CLI
  requires a TTY (`process.stdout.clearLine`), so wrap the call with `script`:
  ```bash
  conda activate swanki && script -qc "bash /path/to/run.sh" /dev/null
  ```

## Workstation Defaults (gilahyper)

When running swanki on gilahyper, use these overrides:

- **`audio=all`** — generate per-card complementary audio alongside summary/lecture/reading. Applies to every paper.
- **`anki=default`** — no Anki *client* on this machine; `anki=auto_send` fails at pipeline end. (Delivery to the headless AnkiConnect server is a separate step — see Sync Terminology.)
- **`ocr=mineru`** — local GPU OCR; `ocr=mathpix` is the paid fallback and needs a TTY.
- **`models=fish_speech`** — Fish Speech with the `british-prof` reference voice. Prefer it over ElevenLabs: no per-call cost, voice cloning stays on-box, no rate limits. Under SLURM the server is brought up **per job** on a derived free port (`SWANKI_FISH_PORTS`), so the `server_url: http://localhost:8080` in `conf/models/fish_speech.yaml` is only the fallback for a hand-run outside SLURM.
- The `llm` block uses **`provider: openai-responses`**, not `openai`. Reasoning models refuse function tools on `/v1/chat/completions`, and every swanki agent uses structured output. See [[swanki.llm.agents]] 2026.07.27 before "fixing" that back.

Prefer `scripts/swanki_enqueue.sh` (see Generation Queue) over a hand-written `.sh` — the
sbatch already applies these. For a one-off hand run:
```bash
swanki pdf_path=... citation_key=... +output_dir=... \
  audio=all anki=default ocr=mineru models=fish_speech zotero=default \
  pipeline.processing.confirm_before_generation=false
```

Other workstations (laptops without the Fish server / with Anki installed) should not inherit these — they're gilahyper-specific.

## Generation Queue

To run **many sources without babysitting blocking**, enqueue jobs and forget them.
**SLURM is the live path** — set `SWANKI_QUEUE_EXECUTOR=slurm`. The Docker Fish fleet and
the bash drainer are retired; do not start them.

- **Enqueue:** `SWANKI_QUEUE_EXECUTOR=slurm scripts/swanki_enqueue.sh --pdf PATH --key CITATION_KEY [--content-key <key>_CH##_<slug>] [--voice fish_speech] [--author "Name"] [--extra "hydra.override=x"] [--singleton] [--after JOBID]`. Papers need just `--pdf --key`; book chapters add `--content-key` (output_dir is derived as `<key>/<content_key>`). Voice defaults to the `fish_speech` british-prof seminar; pass a clone (`fish_speech_bechtel`, `fish_speech_hamming`, …) for author-voiced books. Prints the jobid on stdout for chaining; `DRY_RUN=1` previews without submitting.
- **One GPU at a time.** Swanki shares the box with science sweeps and may hold **one** GPU. Submitting N chapters at once is fine, but chain them with `--singleton` (or `--after <jobid>`) so only one runs — two concurrent jobs means two GPUs. Verify with `squeue` that only one `swanki` job is RUNNING.
- **Per job:** `sbatch --gres=gpu:1` (`scripts/swanki_job.sbatch`) brings Fish up **in-job** via `apptainer --nv` (baked `.sif`) on a derived free port exported as `SWANKI_FISH_PORTS`, runs OCR+cards+TTS pinned to the allocated GPU (local index 0 via the ambient `CUDA_VISIBLE_DEVICES`), delivers Zotero then Anki (flock-serialized) at end-of-job, then tears Fish down. Idle swanki uses zero GPU. Hardcodes `audio=all anki=default ocr=mineru models=<voice> zotero=default`.
- **ABS** is deferred to a no-GPU `--dependency=singleton` finalizer (`scripts/swanki_finalize_abs.sbatch`), submitted per chapter as `--dependency="singleton,afterok:<jobid>"` with a **per-chapter `SWANKI_ABS_DIRTY` path**. The per-chapter flag is load-bearing: with the shared default flag, a finalizer that is mid-refresh deletes a newer chapter's flag on completion and that chapter silently never reaches ABS.
- **Watch:** `squeue`, `~/.swanki-queue/logs/slurm-<jobid>.log`, `sacct -j <jobid> --format=JobID,State,Elapsed,ExitCode -X`.

**Legacy local drainer** (`scripts/swanki_queue.sh` + `swanki-queue.service`): the systemd
unit is no longer installed, and the executor still defaults to `local` — so
`SWANKI_QUEUE_EXECUTOR=slurm` must be set explicitly or the enqueue silently writes a JSON
spec that nothing will drain. Design/rationale for the old serial queue:
`notes/scripts.swanki_queue.md` ([[scripts.swanki_queue]]); migration record:
`notes/runbook.slurm-cutover.md` ([[runbook.slurm-cutover]]) / `scripts/slurm_cutover.sh`.

## Sync Terminology

When the user says any of these, they mean push the latest artifacts to the **self-hosted endpoints** (the user's ABS server + the headless Anki on gilahyper). The pipeline is finished; this is the delivery step.

- **"sync swanki data"** / **"sync to swanki servers"** / **"push to my servers"** → `bash scripts/swanki_sync.sh [--projection NAME] [--dry-run]`. Runs both halves: ABS audio refresh and headless Anki deck push.
- **"land on abs"** → audio half only. `bash scripts/abs_refresh.sh`. (Also invoked by `swanki_sync.sh`.)
- **"land on anki server"** / **"push to anki"** → deck half only. `python scripts/swanki_anki_sync.py [--projection NAME] [--dry-run]`. POSTs `importPackage` per latest `.apkg` then a single AnkiWeb `sync`.

**Zotero sync is still part of the loop** (`sync_to_zotero`, triggered at pipeline end when `zotero.sync=true`) — it produces the versioned `.apkg` and audio `.zip` attachments that the self-hosted endpoints read from. Conceptually it is **the backup / source-of-truth layer**, not the primary delivery channel. Users without their own servers still sideload from the Zotero attachments by hand; advanced users with their own ABS + headless Anki use the shortcuts above.

Prereqs and the headless Anki + AnkiConnect setup are documented in `notes/anki.headless-sync.md`.

### Clear ABS Prologue comments after a multi-chapter book rewrite

ABS bookmarks (the notes left in the BookPlayer/"Prologue" app) are **feedback to be actioned**: they flag content to correct. So whenever a **large rewrite/re-render spanning multiple chapters of a book** lands on ABS, clearing **all** of that book's Prologue comments is part of the delivery, not an afterthought. Two reasons:

- **Ambiguity.** A comment left open reads as "not yet addressed." Once its issue is fixed and re-delivered, leaving the bookmark makes it unclear whether the fix shipped. Clearing is how "done" is signaled.
- **Timestamp drift.** Re-rendering shifts chunk times, so old bookmark timestamps point at the wrong audio. Stale bookmarks don't auto-migrate ([[feedback_abs_clear_and_remark]]) — they get "messed up" against the new audio.

Mechanism (whole-item, per book): `~/miniconda3/envs/swanki/bin/python scripts/abs_clear_bookmarks.py --citation-key <bookKey> --yes` (dry-run without `--yes`). Bookmarks are filed under the parent item, so one whole-item clear sweeps every chapter's comments at once. Do this **after** the audio has landed on ABS (Zotero → `targeted_refresh`), as the final step of the rewrite. For a single surgical edit this is optional; for a multi-chapter sweep it is the default. Verify zero remain with `scripts/abs_bookmarks.py`.

## Weekly Notes

- When checking off a task in the weekly note, always add a one-sentence summary before the `[[link]]`. Never leave a checked item as just a bare link.

## Git Worktrees

We develop on multiple branches simultaneously using git worktrees. The main repo is
`~/Documents/projects/Swanki/`; worktrees live in a **different tree** at
`~/projects/Swanki.worktrees/<branch>/` (note: not `~/projects/Swanki/`, which does not
exist). Confirm with `git worktree list` rather than assuming either path. Active
worktrees and their tasks are tracked in weekly notes
(`notes/user.mjvolk3.swanki.tasks.weekly.<year>.<week>.md`).

**Shared data.** `SWANKI_DATA` points to the sibling `Swanki_Data/` directory and is the same across all worktrees (no per-worktree copy needed). Only repo-internal paths (`WORKSPACE_DIR`, `ASSET_IMAGES_DIR`) get rewritten by the setup script.

**Shared auto memory.** `scripts/setup-worktree.sh` symlinks each worktree's Claude Code auto memory directory to the main repo's memory directory (`~/.claude/projects/.../memory/`). This means all worktrees and the main repo read and write the same `MEMORY.md` and topic files. When writing to auto memory, be aware that another Claude Code agent in a different worktree may be doing the same -- keep writes additive, don't overwrite entire files, and use topic-specific files to reduce conflicts.

**Concurrent agents.** Multiple Claude Code sessions may be active across worktrees at the same time, each working on a different branch/feature. Do not assume you are the only agent running. This is especially relevant for auto memory writes and any shared resources.

### Worktree Merge Workflow

When a worktree branch is ready to land:

1. **Single branch:** rebase onto main, push, open PR, merge, then clean up.
2. **Batch (multiple independent branches):** merge sequentially -- rebase first branch onto main, merge its PR, update main, rebase next branch, repeat. Each feature gets its own clean merge with linear history. Do NOT use integration branches.

After merging:

```bash
git worktree remove --force ~/projects/Swanki.worktrees/<branch>
git branch -d <branch>
gh api repos/Mjvolk3/Swanki/git/refs/heads/<branch> --method DELETE
```

**Weekly note conflicts:** `.gitattributes` sets `merge=union` on `notes/user.mjvolk3.swanki.tasks.weekly.*.md`, so git automatically keeps lines from both sides. No manual resolution needed for this file.

**Other conflict files** (e.g. `__init__.py`): resolve manually -- all additions are additive, so keep both sides.

## Finding Rationale for Changes

To understand why a code change was made, check the dendron module note (`notes/swanki.<module>.md`). Each dated section documents what changed and why. This is the primary source of decision history for the codebase.
