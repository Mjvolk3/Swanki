---
id: pe8eh3ouyxdwcswa8h14k9v
title: Plan 0
desc: ''
updated: 1773155684414
created: 1773153098252
---

## Context

Some users want audio outputs (especially lectures) without generating flashcards. The pipeline currently forces all stages to run sequentially — card generation is the most expensive stage (many LLM calls) and blocks audio generation even when audio doesn't need cards.

Three of four audio types are independent of cards:

| Audio Type           | Minimum Pipeline Stages Required                |
|----------------------|-------------------------------------------------|
| Reading              | 1-3 (PDF split → markdown → clean)              |
| Lecture              | 1-4 (+ image processing)                        |
| Summary              | 1-5 (+ document summary generation)             |
| Card (complementary) | 1-8 (+ card gen + output gen) — **needs cards** |

The audio functions in `swanki/audio/` are already pure and standalone — the coupling exists only in `pipeline.py:process_full()` orchestration.

## Which Refactor First?

**Do audio decoupling first, then pydanticAI migration.**

Reasons:

1. **Orthogonal changes** — audio decoupling modifies pipeline control flow (which stages run); pydanticAI migration modifies LLM client code (how stages call models). They touch the same file but different code paths.
2. **Immediate user value** — audio decoupling ships the lecture-only feature users are asking for. PydanticAI migration delivers no new functionality (same behavior, different library).
3. **Small and low-risk** — ~30 lines of branching logic in `process_full()`. PydanticAI is 13+ call sites across 3+ files.
4. **No rework** — the pipeline flow changes survive the pydanticAI migration unchanged since they're about which stages run, not which LLM client is used.
5. **Validates the decoupling claim** — actually running audio without cards proves that summary/lecture/reading are truly independent before we rearrange the LLM layer underneath them.

## Design

### New config key: `mode`

Add `mode` to the top-level Hydra config. Two values:

- `full` (default) — current behavior, all stages run
- `audio_only` — skip card generation, output generation, APKG export, Anki sending

```yaml
# .swanki_config/config.yaml
mode: full  # "full" or "audio_only"
```

User invocation:

```bash
# Lecture only — no cards generated
swanki pdf_path=paper.pdf citation_key=smith2023 mode=audio_only audio.audio.generate_lecture=true

# All non-card audio
swanki pdf_path=paper.pdf citation_key=smith2023 mode=audio_only audio=full

# Convenience preset (new)
swanki pdf_path=paper.pdf citation_key=smith2023 mode=audio_only audio=lecture_only
```

### Pipeline flow with `mode=audio_only`

Current `process_full()` flow (lines 193-366):

```
Stage 1:   PDF split                    ← ALWAYS (shared)
Stage 2:   Markdown conversion          ← ALWAYS (shared)
Stage 3:   Markdown cleaning            ← ALWAYS (shared)
Stage 4:   Image processing             ← SKIP if only reading audio requested (optimization, defer)
Stage 5:   Document summary generation  ← SKIP if no summary audio requested (optimization, defer)
Stage 5.5: Estimate card count          ← SKIP in audio_only
Stage 5.6: User confirmation prompt     ← SKIP in audio_only
Stage 6:   Card generation loop         ← SKIP in audio_only
Stage 7:   Store citation key           ← ALWAYS (needed for audio file naming)
Stage 8:   generate_outputs()           ← SKIP in audio_only (writes card markdown)
Stage 9:   generate_audio()             ← RUN (with cards=[] guard for complementary)
Stage 9b:  Re-export APKG with audio    ← SKIP in audio_only (needs cards)
Stage 10:  Send to Anki                 ← SKIP in audio_only (needs cards)
```

### Minimal changes in `generate_audio()`

The `generate_audio()` method (lines 2136-2417) already checks each audio flag independently. The only change needed is a guard at the complementary audio block (line 2202):

```python
# Line 2202: Add guard for empty cards
if audio_config.get("generate_complementary", False):
    if not cards:
        logger.warning(
            "Complementary audio requires cards. Skipping in audio_only mode."
        )
    else:
        # ... existing complementary audio code ...
```

And skip the "write cards with audio" block (line 2341) when cards is empty — this already works since it's behind `if audio_config.get("generate_complementary", False)` and iterates `cards`, but we add the same guard for clarity.

### Summary audio with `summary=None`

In audio_only mode with no summary audio requested, `doc_summary` would be `None` if we skip stage 5. But the `generate_audio()` signature requires `summary: DocumentSummary`. Two options:

- **Option A (simple):** Always run stage 5 in audio_only mode. Summary generation is fast (single LLM call) and the `DocumentSummary` is useful metadata. This means only card generation (stage 6) is skipped.
- **Option B (optimized):** Make `summary` optional in `generate_audio()`, skip stage 5 if no summary audio is requested. More complex, saves one LLM call.

**Recommend Option A** — always generate the document summary. It's one LLM call, and the summary file itself is useful output even in audio_only mode.

Similarly, always run image processing (stage 4) — it's needed for lecture audio and produces useful output.

### Simplified flow for audio_only

With Option A, the audio_only path is very simple — the only skipped stages are 5.5 through 8:

```python
mode = self.config.get("mode", "full")

if mode == "full":
    # Stages 5.5-8: estimate, confirm, generate cards, write outputs
    ...
elif mode == "audio_only":
    all_cards = []
    outputs = {}
    self.citation_key = citation_key
```

Then stages 9-10 run with existing guards.

## Files to Modify

### 1. `.swanki_config/config.yaml` — add mode key

```yaml
# Add after existing keys
mode: full
```

### 2. `swanki/pipeline/pipeline.py` — branch in `process_full()`

**In `process_full()` (around line 256):** After stage 5 (summary generation), add mode check to skip stages 5.5-8.

**In `generate_audio()` (line 2202):** Add guard for empty `cards` list at the complementary audio block.

**In `generate_audio()` (line 2341):** The "write cards with audio" block is already guarded by `generate_complementary` flag, but add `if cards:` guard for safety.

### 3. `swanki/__main__.py` — update help text

Add `mode=audio_only` to the help text examples (around line 209):

```
  mode=<full|audio_only>                Pipeline mode (audio_only skips card generation)
```

And add example:

```
  # Generate only lecture audio (no cards)
  swanki pdf_path=paper.pdf citation_key=smith2023 mode=audio_only audio.audio.generate_lecture=true
```

### 4. `.swanki_config/audio/lecture_only.yaml` — new convenience preset

```yaml
audio:
  generate_complementary: false
  generate_summary: false
  generate_reading: false
  generate_lecture: true
  lecture_speed: 1.1
  format: mp3
  quality: high
```

## Edge Cases

1. **`mode=audio_only` with `audio=none`** — produces no audio output. Log a warning: "audio_only mode with no audio types enabled produces no output."
2. **`mode=audio_only` with `generate_complementary=true`** — complementary audio needs cards. Log a warning and skip it.
3. **`mode=audio_only` with `create_anki_deck=true`** — APKG needs cards. Already guarded by `"cards_audio" in outputs` check at line 345.
4. **`mode=audio_only` with `anki.auto_send=true`** — sending needs cards. Already guarded since `all_cards` is empty.

## Verification

1. **Full pipeline unchanged:** `swanki pdf_path=paper.pdf citation_key=test` produces identical output to before
2. **Audio-only lecture:** `swanki pdf_path=paper.pdf citation_key=test mode=audio_only audio.audio.generate_lecture=true` generates lecture audio, no cards, no APKG
3. **Audio-only with complementary warning:** `swanki pdf_path=paper.pdf citation_key=test mode=audio_only audio=full` generates summary/reading/lecture audio, logs warning about skipping complementary, no cards
4. **Audio-only with no audio:** `swanki pdf_path=paper.pdf citation_key=test mode=audio_only audio=none` logs warning about no output
5. **Existing tests pass:** `pytest tests/` — no regressions

## Sequencing Note (see [[plan.major-refactor-sequence.plan-0]])

This is **step 1** of the major refactor sequence. Config changes go to `.swanki_config/` now and will be migrated to `swanki/conf/` in step 2 (config refactor). The `mode` key and `lecture_only.yaml` preset added here will be carried forward.

### Quality gates for this step

- All new/modified code must pass `mypy --strict` on touched files
- Google-style docstrings on any new/modified functions
- Frontmatter updated via `/update-py-notes` for touched `.py` files
- Unit tests for `mode=audio_only` branch in `process_full()` (mock LLM calls)
- Sphinx docs updated if any public API changes
- `ruff check` and `ruff format` pass

## Scope

- ~15 lines of branching logic in `process_full()`
- ~5 lines of guard in `generate_audio()`
- ~3 lines in `config.yaml`
- ~5 lines in `__main__.py` help text
- 1 new audio preset file (12 lines)
- The `swanki/audio/` package has **zero changes**
