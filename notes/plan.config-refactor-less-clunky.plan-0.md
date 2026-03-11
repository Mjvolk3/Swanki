---
id: w6ifh0c7gtj5d4l8odiibzd
title: Plan 0
desc: ''
updated: 1773160296791
created: 1773157027809
---

## Context

The current config system has several pain points:

1. **Fragile location** — `.swanki_config/` lives in the project directory. If the dir is deleted, all config is lost. Per-citation voice/pipeline customizations (`.swanki_config_custom/`) are also project-local.
2. **1360-line ConfigGenerator** — hardcodes every default into Python strings, then writes them as YAML files on first run. Maintenance burden; defaults exist in code but are only usable after generation.
3. **Auto-population creates issues** — interactive first-run prompt, regeneration concerns, generated files that look editable but get overwritten.
4. **Non-obvious preset names** — `essential.yaml` means complementary + summary. `all_but_reading.yaml` means complementary + summary + lecture. The user can't tell what's enabled without opening the file.
5. **Custom configs aren't auto-loaded** — `.swanki_config_custom/` exists with per-citation-key model/pipeline overrides, but no code loads them. Users must manually specify `models=dennettDarwinsDangerousIdea1996` on the CLI, and that only works if the file is in `.swanki_config/models/`.

## Design: Three-Tier Config (like git config)

The config system follows the same pattern as git config, `.claude/`, and other tools — three layers with increasing specificity:

| Priority    | Layer        | Location                 | Purpose                                     |
|-------------|--------------|--------------------------|---------------------------------------------|
| 1 (highest) | **Local**    | `.swanki/` (project dir) | Per-project overrides                       |
| 2           | **Global**   | `~/.swanki/` (home dir)  | User preferences, per-citation voices       |
| 3 (lowest)  | **Defaults** | `swanki/conf/` (package) | Software defaults, shipped with pip install |

Higher priority wins on conflict. CLI overrides (`swanki ... key=value`) sit above all three.

### Architecture

```
swanki/conf/                           # DEFAULTS — shipped with pip install, never edited
  config.yaml                          # Main Hydra config with defaults list
  audio/
    none.yaml
    all.yaml
    complementary_summary.yaml         # Was "essential"
    complementary_summary_lecture.yaml  # Was "all_but_reading"
    lecture.yaml                        # New, for audio_only mode
  pipeline/
    default.yaml
    standard.yaml
    larger.yaml
    smaller.yaml
  models/
    default.yaml
    openai_tts.yaml
  prompts/
    default.yaml
    technical.yaml
  output/
    default.yaml
  anki/
    default.yaml
    auto_send.yaml
    custom_deck.yaml
  refinement/
    default.yaml
    strict.yaml
    minimal.yaml
    disabled.yaml

~/.swanki/                             # GLOBAL — user preferences, durable across projects
  models/                              # Per-citation voices and model choices
    MV-LL.yaml
    dennettDarwinsDangerousIdea1996.yaml
    nishitaniSelfovercomingNihilism1990.yaml
    popperLogicScientificDiscovery2002.yaml
    spiegelhalterArtStatistics2019.yaml
  pipeline/                            # Per-citation card counts
    dennettDarwinsDangerousIdea1996.yaml
    nishitaniSelfovercomingNihilism1990.yaml
  models/default.yaml                  # Override package default with your preferred model
  audio/my_preset.yaml                 # Custom audio presets

.swanki/                               # LOCAL — per-project overrides (optional, like .git/config)
  models/default.yaml                  # This project always uses a specific model
  pipeline/default.yaml                # This project always uses specific card counts
```

### How Hydra Finds All Three

Hydra `SearchPathPlugin` with three providers in priority order:

```python
from pathlib import Path
from hydra.plugins.search_path_plugin import SearchPathPlugin

class SwankiSearchPathPlugin(SearchPathPlugin):
    def manipulate_search_path(self, search_path):
        # 3. Package defaults (lowest priority)
        search_path.append(provider="swanki-defaults", path="pkg://swanki/conf")

        # 2. Global user preferences (medium priority)
        global_config = Path.home() / ".swanki"
        if global_config.exists():
            search_path.append(provider="swanki-global", path=f"file://{global_config}")

        # 1. Local project overrides (highest priority)
        local_config = Path.cwd() / ".swanki"
        if local_config.exists():
            search_path.append(provider="swanki-local", path=f"file://{local_config}")
```

### Resolution Examples

```bash
# Uses package default model
swanki models=default
# → swanki/conf/models/default.yaml

# User has a global preferred model in ~/.swanki/models/default.yaml
# → ~/.swanki/models/default.yaml wins over package default

# User has a per-citation voice
swanki models=dennettDarwinsDangerousIdea1996
# → ~/.swanki/models/dennettDarwinsDangerousIdea1996.yaml

# Project-local override (e.g., a book project that always uses larger pipeline)
# .swanki/pipeline/default.yaml exists with num_cards_per_page=5
swanki pipeline=default
# → .swanki/pipeline/default.yaml wins over package and global

# CLI always wins
swanki models=default models.models.llm.model=gpt-5-nano
```

### What Goes Where

| What                                               | Where                                | Why                                          |
|----------------------------------------------------|--------------------------------------|----------------------------------------------|
| Software defaults (card counts, speeds, prompts)   | `swanki/conf/`                       | Version-controlled, updated with pip install |
| Your preferred default voice                       | `~/.swanki/models/default.yaml`      | Personal preference, applies everywhere      |
| Per-citation voices (Dennett = George, etc.)       | `~/.swanki/models/<citation>.yaml`   | Personal, reusable across projects           |
| Per-citation pipeline settings                     | `~/.swanki/pipeline/<citation>.yaml` | Personal, reusable across projects           |
| Custom audio presets                               | `~/.swanki/audio/`                   | Personal convenience presets                 |
| A book project that always uses larger pipeline    | `.swanki/pipeline/default.yaml`      | Project-specific, checked into project repo  |
| A project that always uses a specific audio preset | `.swanki/audio/default.yaml`         | Project-specific                             |

### What Happens to ConfigGenerator

**Delete it.** The 1360-line `generator.py` becomes unnecessary:

- Package defaults live in `swanki/conf/` as actual YAML files checked into the repo
- No generation, no interactive prompts, no first-run ceremony
- Users who want to see/edit defaults run `swanki --show-defaults` (prints `swanki/conf/` path)
- Users who want custom overrides create files in `~/.swanki/`

Replace with a tiny helper:

```python
# swanki/config/helpers.py
def show_defaults_path() -> Path:
    """Return path to package default configs."""
    return Path(__file__).parent.parent / "conf"

def user_config_dir() -> Path:
    """Return path to user config directory."""
    return Path.home() / ".swanki"

def init_user_config():
    """Copy package defaults to ~/.swanki/ for editing."""
    ...
```

### Audio Preset Naming

Rename to be self-documenting. The name IS the documentation.

| Old Name               | Enabled Flags                   | New Name                             |
|------------------------|---------------------------------|--------------------------------------|
| `none.yaml`            | (nothing)                       | `none.yaml`                          |
| `default.yaml`         | (nothing — identical to none)   | **Delete** — merge with none         |
| `essential.yaml`       | complementary, summary          | `complementary_summary.yaml`         |
| `all_but_reading.yaml` | complementary, summary, lecture | `complementary_summary_lecture.yaml` |
| `full.yaml`            | all four                        | `all.yaml`                           |
| (new)                  | lecture only                    | `lecture.yaml`                       |
| (new)                  | summary, lecture                | `summary_lecture.yaml`               |

With the audio_only mode refactor, the useful non-card presets are `lecture.yaml` and `summary_lecture.yaml`.

The `default` in `config.yaml` changes from `audio: default` to `audio: none` (same behavior, but no longer ambiguous).

### CLI Help and Discoverability

Since preset names are self-documenting, the help text becomes clearer:

```
Configuration Options:
  audio=<none|all|complementary_summary|complementary_summary_lecture|lecture|summary_lecture>
```

Add two new commands:

```bash
swanki --show-defaults    # Print package defaults path for reference
swanki --init-config      # Copy defaults to ~/.swanki/ for customization
```

### What Happens to `.swanki_config/` and `.swanki_config_custom/`

- `.swanki_config/` — **no longer generated**. If it exists from a previous install, it's ignored (Hydra points to `swanki/conf/` now). Add to `.gitignore`.
- `.swanki_config_custom/` — **migrated** to `~/.swanki/`. One-time move of the 12 citation-key YAML files.

## Migration Path

### Phase 1: Move defaults into package

1. Create `swanki/conf/` directory with all config files (copy from current `.swanki_config/`)
2. Rename audio presets
3. Update `config.yaml` defaults to reference new names
4. Add `swanki/conf/` to `pyproject.toml` package data
5. Change `@hydra.main(config_path="conf", ...)` in `__main__.py`
6. Verify: `swanki pdf_path=... citation_key=...` works with package defaults

### Phase 2: Add user override directory

1. Implement `SwankiSearchPathPlugin` for `~/.swanki/` search path
2. Register plugin in Hydra's plugin discovery
3. Move `.swanki_config_custom/` contents to `~/.swanki/`
4. Verify: `swanki models=MV-LL` finds `~/.swanki/models/MV-LL.yaml`

### Phase 3: Remove ConfigGenerator

1. Delete `swanki/config/generator.py` (1360 lines)
2. Replace with `swanki/config/helpers.py` (~30 lines)
3. Remove interactive prompt logic from `__main__.py`
4. Add `--show-defaults` and `--init-config` commands
5. Update help text

### Phase 4: Cleanup

1. Add `.swanki_config/` to `.gitignore`
2. Update README with new config approach
3. Remove `.swanki_config/` from repo if tracked
4. Remove `.swanki_config_custom/` after migration

## Sequencing Note (see [[plan.major-refactor-sequence.plan-0]])

This is **step 2** of the major refactor sequence.

### Prerequisite state from step 1 (audio decoupling)

When this step begins, the following already exist in `.swanki_config/`:

- `config.yaml` has `mode: full` key
- `audio/lecture_only.yaml` preset exists

These must be carried into `swanki/conf/` during migration. Specifically:

- Include `mode: full` in `swanki/conf/config.yaml`
- Include `lecture.yaml` (renamed from `lecture_only.yaml`) in `swanki/conf/audio/`

### What comes after

Steps 3-5 (segmentation, lecture transcript, pydanticAI) all benefit from `generator.py` being deleted — they write config directly to `swanki/conf/` and never touch the generator.

### Quality gates for this step

- All new/modified code must pass `mypy --strict` on touched files
- Google-style docstrings on `SwankiSearchPathPlugin`, `helpers.py` functions
- Frontmatter updated via `/update-py-notes` for touched `.py` files
- Unit tests for `SwankiSearchPathPlugin` search path resolution (all 3 tiers)
- Unit tests for `helpers.py` functions
- Sphinx docs updated for new CLI flags (`--show-defaults`, `--init-config`, `--config-info`)
- `ruff check` and `ruff format` pass

## Resolved Questions

1. **`~/.swanki/`** — confirmed. Obvious to the user when placed in home directory globals, matches `.claude/` pattern.

2. **Hydra SearchPathPlugin registration** — use `pyproject.toml` entry point:

    ```toml
    [project.entry-points."hydra_plugins"]
    swanki = "swanki.config.hydra_plugins"
    ```

    Create `swanki/config/hydra_plugins.py` with `SwankiSearchPathPlugin`. Hydra discovers it automatically via entry points at import time — no manual registration needed.

3. **Backward compatibility** — not a concern. We are the only user. Just delete `.swanki_config/` and `.swanki_config_custom/` after migrating.

4. **`pyproject.toml` package data** — add to existing `[tool.setuptools.package-data]`:

    ```toml
    [tool.setuptools.package-data]
    swanki = ["py.typed", "conf/**/*.yaml"]
    ```

    This ensures all YAML configs in `swanki/conf/` are included in the built distribution (wheel and sdist).

## Workflow Breakdown

### Scenario 1: Process a typical paper (no custom config)

```
swanki pdf_path=paper.pdf citation_key=smith2023 audio=all anki=auto_send
```

Config resolution:

```
CLI override:     audio=all, anki=auto_send
                  ↓ merges with
.swanki/ (local): (empty or doesn't exist — skipped)
                  ↓ falls back to
~/.swanki/ (global): (no models/default.yaml — skipped)
                  ↓ falls back to
swanki/conf/ (defaults): pipeline/default.yaml, models/default.yaml, audio/all.yaml, ...
                  ↓
RESOLVED CONFIG:  package defaults + CLI overrides applied
```

What the user does: **nothing** — package defaults always exist, no generation step.

### Scenario 2: Process Dennett with custom voice and card count

```
swanki pdf_path=dennett_ch7.pdf citation_key=dennett_ch7 \
  models=dennettDarwinsDangerousIdea1996 pipeline=dennettDarwinsDangerousIdea1996 \
  audio=complementary_summary anki=auto_send
```

Config resolution:

```
CLI override:     models=dennett..., pipeline=dennett..., audio=complementary_summary
                  ↓ merges with
.swanki/ (local): (no dennett files — skipped)
                  ↓ falls back to
~/.swanki/ (global): models/dennettDarwinsDangerousIdea1996.yaml  ← FOUND (George voice)
                     pipeline/dennettDarwinsDangerousIdea1996.yaml ← FOUND (1 card/page)
                  ↓ other groups fall back to
swanki/conf/ (defaults): audio/complementary_summary.yaml, anki/auto_send.yaml, ...
                  ↓
RESOLVED CONFIG:  Dennett voice + card count from ~/.swanki/, rest from package defaults
```

What the user does: **create files in `~/.swanki/` once**. No copy step. No ConfigGenerator.

### Scenario 3: A book project that always uses specific settings

Project dir: `~/projects/DennettBook/`

```
# ~/projects/DennettBook/.swanki/pipeline/default.yaml
processing:
  num_cards_per_page: 1
  cloze_cards_per_page: 0
```

```
swanki pdf_path=ch7.pdf citation_key=dennett_ch7 models=dennettDarwinsDangerousIdea1996
```

Config resolution:

```
CLI override:     models=dennett...
                  ↓ merges with
.swanki/ (local): pipeline/default.yaml ← FOUND (1 card/page, project-specific)
                  ↓ falls back to
~/.swanki/ (global): models/dennettDarwinsDangerousIdea1996.yaml ← FOUND (George voice)
                  ↓ other groups fall back to
swanki/conf/ (defaults): audio/none.yaml, anki/default.yaml, ...
                  ↓
RESOLVED CONFIG:  local pipeline + global voice + package defaults for everything else
```

What the user does: **create `.swanki/` in the book project dir**. No `pipeline=dennett...` needed on every CLI call — the project always uses those settings.

### Scenario 4: Override your personal default model globally

```
# ~/.swanki/models/default.yaml — your personal default, used everywhere
models:
  llm:
    provider: openai
    model: gpt-5.2-2025-12-11
    temperature: 0.7
    max_retries: 3
  tts:
    provider: elevenlabs
    voice_id: HDA9tsk27wYi3uq0fPcK  # Stuart — your preferred default voice
    model: eleven_monolingual_v2
    stability: 0.5
    similarity_boost: 0.5
```

Now every `swanki` run uses Stuart's voice by default, without specifying `models=MV-LL` on the CLI. The package `swanki/conf/models/default.yaml` is shadowed by your global override.

### Scenario 5: "Where are my configs?" — discoverability

The `~/.swanki/` location is a hidden dot-dir. To prevent the "I forgot where my configs are" problem, `swanki --config-info` prints all active config locations:

```bash
swanki --config-info
# Package defaults:  /path/to/site-packages/swanki/conf/
# Global config:     ~/.swanki/               (7 files)
# Local config:      .swanki/                 (not found)
#
# Global configs found:
#   models/MV-LL.yaml
#   models/dennettDarwinsDangerousIdea1996.yaml
#   models/nishitaniSelfovercomingNihilism1990.yaml
#   pipeline/dennettDarwinsDangerousIdea1996.yaml
#   ...

swanki --cfg job                    # Hydra built-in: dump fully resolved config
swanki --cfg job models=dennett...  # See resolved config with Dennett override
```

This makes `~/.swanki/` easy to rediscover. Also, the `swanki --help` text should mention `~/.swanki/` prominently.

### Summary: where each thing lives

| What                                    | Where                                | Lifetime                                                                     |
|-----------------------------------------|--------------------------------------|------------------------------------------------------------------------------|
| Software defaults (all settings)        | `swanki/conf/` (in package)          | Updated with `pip install`. Never edited. Visible in repo at `swanki/conf/`. |
| Your preferred voice/model              | `~/.swanki/models/default.yaml`      | Created once. Durable. Survives project deletion.                            |
| Per-citation voice (George for Dennett) | `~/.swanki/models/<citation>.yaml`   | Created once per citation. Durable.                                          |
| Per-citation card count                 | `~/.swanki/pipeline/<citation>.yaml` | Created once per citation. Durable.                                          |
| Custom audio presets                    | `~/.swanki/audio/<name>.yaml`        | Created when needed. Durable.                                                |
| Project-specific defaults               | `.swanki/` in project dir            | Optional. Rare. For e.g. book projects.                                      |

### What replaces what

| Old                                     | New                               | Notes                                   |
|-----------------------------------------|-----------------------------------|-----------------------------------------|
| `.swanki_config/` (generated defaults)  | `swanki/conf/` (package defaults) | No generation. Always exists.           |
| `.swanki_config_custom/` (staging area) | `~/.swanki/` (global config)      | No copy step. Hydra finds directly.     |
| ConfigGenerator (1360 lines)            | Deleted                           | Package defaults are static YAML files. |
| Copy from `_custom/` → `_config/`       | Gone                              | Files go directly to `~/.swanki/`.      |
| `audio=essential`                       | `audio=complementary_summary`     | Self-documenting name.                  |
