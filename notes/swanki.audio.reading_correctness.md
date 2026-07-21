---
id: 2fa0aea9601dc1a1c85d5cef
title: Reading Correctness
desc: ''
updated: 1784675451782
created: 1784675451782
---

## 2026.07.21 - Report-only audio correctness critic (reading + lecture)

New module `swanki/audio/reading_correctness.py`. A report-only critic on the
**audio path** — unlike `swanki/pipeline/card_correctness.py` (PR #24), which
hooks at `generate_outputs` and is skipped entirely by `audio_only` runs, so
audio-only regenerations previously had zero correctness coverage. This critic
emits a per-chapter JSON audit per track and **never mutates audio**.

Plan: [[plan.audio-reading-correctness-critic.2026.07.21]].

### Three checks

1. **Reading clause diff (deterministic, default ON).** For each Pass-2
   `(input window, transcript output, fell_back)` triple collected inside the
   `reading.py` loop, `diff_chunk` normalizes both sides and runs
   `difflib.SequenceMatcher` over sentence-normalized tokens, flagging only
   residual `inserted` / `duplicated` / `dropped` blocks. Catches the CH03
   "as small as 22 nucleotide residues long" splice that the length-ratio floor
   (`_PASS2_CHUNK_MIN_RATIO`) is blind to.
2. **Acronym double-emit validator (deterministic, default ON).** Run once on
   the FINAL `tts_transcript` (post-scrubber), where the phantom name exists.
   Detects `<expansion>, <letter-spelled acronym>` adjacency ("adenosine
   triphosphate, A-T-P") and cross-chunk double-expansion of the same acronym.
3. **Lecture factual pass (LLM, default OFF).** Claims not wording, very high
   acceptance, `assessment_failed` fail-open. Report-only: `fixed`/`dropped`
   are recorded, never applied.

### Key decisions (from the plan)

- **New hook, not card-gate reuse.** Orchestration + audit emission live at the
  `generate_reading_audio` / `generate_lecture_audio` call sites in
  `pipeline.py` — the one place both full and `audio_only` runs pass through.
  The fidelity signal is COLLECTED inside `reading.py`'s Pass-2 loop (via a
  `ReadingCorrectnessCollector`); the audit is WRITTEN by the hook.
- **Diff the in-loop Pass-2 pair, not page files.** Post-humanize 3000-token
  `cl100k_base` windows over reordered prose map to no page boundary, so
  page-level alignment is intractable. The `(chunk, chunk_transcript)` pair is
  a natural 1:1.
- **Normalize before diffing** so legit meaning-preserving edits (acronym
  first-use expansion, "et al"/citation collapse, `---SECTION_BREAK---`, per-
  digit codeword spelling) don't flood the diff.
- **`fell_back` → `not_assessed`, never `pass`.** A verbatim-fallback chunk has
  a trivially clean diff; marking it `not_assessed` stops the audit laundering
  it as verified-clean.
- **Reading gets the clause diff; lecture does not** (reformulated first-person
  prose floods a clause-exact diff). Lecture receives only the optional factual
  pass.
- **Deterministic ON, LLM OFF.** Modes 1+2 have no API cost and guard the known
  bugs, so they default on; mode 3 is the single network call, opt-in.
- **Fail-fast except fail-open on assessment failure**, mirroring the card gate
  precedent (commit `14fbfab`).
- **One Hydra group** `audio_correctness_gate` carries per-track + per-mode
  toggles. Registered in BOTH `config.yaml` sites (defaults list + top-level
  null slot); read double-nested
  `cfg.get("audio_correctness_gate", {}).get("audio_correctness_gate", {})` to
  avoid the silent single-`.get` no-op.

### Models (`swanki/models/cards.py`)

`ReadingChunkFidelity`, `AcronymDoubleEmitFinding`, `LectureFactualAssessment`
(agent output), `LectureFactualEntry` (audit entry). Agent
`lecture_factual_agent` registered additively in `swanki/llm/agents.py`.

### Outputs

`reading-correctness-assessment.json` / `lecture-correctness-assessment.json`
under `output_base`, written atomically (temp-then-rename,
`json.dump(indent=2, ensure_ascii=False)`) with a `summary` count block plus
per-chunk / per-claim entries. Tests: `tests/test_reading_correctness.py`
(real fixtures for modes 1+2, monkeypatched mode 3).
