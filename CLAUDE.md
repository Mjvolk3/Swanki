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

- ~/opt/miniconda3/envs/swanki/bin/Swanki python script.py
- On gilahyper, Mathpix CLI requires a TTY (`process.stdout.clearLine`). Wrap `conda run` with `script`:
  ```bash
  conda activate swanki && script -qc "bash /path/to/run.sh" /dev/null
  ```

## Workstation Defaults (gilahyper)

When running swanki on gilahyper, use these overrides:

- **`audio=all`** — generate per-card complementary audio alongside summary/lecture/reading. Applies to every paper.
- **`anki=default`** — no Anki client on this machine; `anki=auto_send` fails at pipeline end.
- **`models=fish_speech`** — local Fish Speech server at `http://localhost:8080` with the `british-prof` reference voice. Prefer this over ElevenLabs for TTS: no per-call cost, voice cloning stays on-box, and it sidesteps ElevenLabs rate limits.

Combined `.sh` template invocation:
```bash
swanki pdf_path=... citation_key=... +output_dir=... \
  audio=all anki=default models=fish_speech \
  pipeline.processing.confirm_before_generation=false
```

Other workstations (laptops without the Fish server / with Anki installed) should not inherit these — they're gilahyper-specific.

## Generation Queue

To run **many sources without babysitting blocking**, use the fire-and-forget serial queue instead of hand-writing a one-off batch script. Drop jobs and forget them — they drain one at a time.

- **Enqueue:** `scripts/swanki_enqueue.sh --pdf PATH --key CITATION_KEY [--content-key <key>_CH##_<slug>] [--voice fish_speech] [--author "Name"] [--extra "hydra.override=x"]`. Papers need just `--pdf --key`; book chapters add `--content-key` (output_dir is derived as `<key>/<content_key>`). Voice defaults to the `fish_speech` british-prof seminar; pass a clone (`fish_speech_bechtel`, `fish_speech_hamming`, …) for author-voiced books.
- **Drainer:** `scripts/swanki_queue.sh`, run by the `swanki-queue.service` systemd --user unit (enabled, survives reboot). Jobs land in `~/.swanki-queue/pending/` and move to `done/`/`failed/` with per-job logs in `logs/`.
- **Watch:** `tail -f ~/.swanki-queue/queue.log`, `journalctl --user -u swanki-queue -f`, `ls ~/.swanki-queue/pending` (depth), `systemctl --user status swanki-queue`.

**Why serial:** the single shared Fish TTS server is the bottleneck — one swanki run saturates all its workers — so `SWANKI_QUEUE_CONCURRENCY` (default 1) keys off **Fish capacity, not GPU count**. SLURM is overkill for one box + one Fish service. `SWANKI_QUEUE_EXECUTOR` (`local` | `noop` dry-run | `slurm` stub) is the forward-compat hook for the dual-purpose era. Each job runs the gilahyper default invocation (`audio=all anki=default ocr=mineru models=<voice> zotero=sync …`).

**Important:** the queue only serializes jobs **submitted through it** — a swanki run launched by hand stays outside it and will contend for Fish. Once the queue is in use, run everything through it. Full design/rationale: `notes/scripts.swanki_queue.md` ([[scripts.swanki_queue]]).

## Sync Terminology

When the user says any of these, they mean push the latest artifacts to the **self-hosted endpoints** (the user's ABS server + the headless Anki on gilahyper). The pipeline is finished; this is the delivery step.

- **"sync swanki data"** / **"sync to swanki servers"** / **"push to my servers"** → `bash scripts/swanki_sync.sh [--projection NAME] [--dry-run]`. Runs both halves: ABS audio refresh and headless Anki deck push.
- **"land on abs"** → audio half only. `bash scripts/abs_refresh.sh`. (Also invoked by `swanki_sync.sh`.)
- **"land on anki server"** / **"push to anki"** → deck half only. `python scripts/swanki_anki_sync.py [--projection NAME] [--dry-run]`. POSTs `importPackage` per latest `.apkg` then a single AnkiWeb `sync`.

**Zotero sync is still part of the loop** (`sync_to_zotero`, triggered at pipeline end when `zotero.sync=true`) — it produces the versioned `.apkg` and audio `.zip` attachments that the self-hosted endpoints read from. Conceptually it is **the backup / source-of-truth layer**, not the primary delivery channel. Users without their own servers still sideload from the Zotero attachments by hand; advanced users with their own ABS + headless Anki use the shortcuts above.

Prereqs and the headless Anki + AnkiConnect setup are documented in `notes/anki.headless-sync.md`.

## Weekly Notes

- When checking off a task in the weekly note, always add a one-sentence summary before the `[[link]]`. Never leave a checked item as just a bare link.

## Git Worktrees

We develop on multiple branches simultaneously using git worktrees. Each worktree lives at `~/projects/Swanki.worktrees/<branch>/` alongside the main repo at `~/projects/Swanki/`. Active worktrees and their tasks are tracked in weekly notes (e.g., `notes/user.mjvolk3.swanki.tasks.weekly.2026.10.md`).

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

## Dotfiles

Shared dotfiles are managed in `~/Documents/projects/dotfiles` (repo: `Mjvolk3/dotfiles`). Contains tmux config (`tmux/`) and Claude Code status line + keybindings (`claude/`). Run `install.sh` to symlink everything into place. `~/.claude/settings.json` points `statusLine` to `~/.claude/statusline.sh`, which is symlinked to the repo.

## Change Log

- This is automatically updated. Don't edit it directly.
