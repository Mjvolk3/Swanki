---
id: d0fc4da13d1749ed892f14e
title: Source Corrections
desc: ''
updated: 1784697803674
created: 1784697803674
---

Paired module note for `swanki/audio/source_corrections.py`.

## 2026.07.22 — Source-corrections apply layer (opt-in) shipped

Turned a **Swanki correction** into a first-class, durable source feature. The
report-only reading critic (`swanki/audio/reading_correctness.py`, PR #51)
*detects* source-fidelity divergences but never mutates audio; its module note
said "corrections are the next layer". This is that layer: an **opt-in APPLY
pass** that reads a HAND-AUTHORED per-chapter YAML spec and re-voices the
affected chunks. It is a **higher bar** than the critic (every `override` is
human-verified against the printed source) and is **NEVER** auto-populated from
critic findings.

### What shipped

- **`swanki/audio/source_corrections.py`** (NEW) — `apply_source_corrections()`:
  load + validate the spec, group by track, per correction locate the chunk
  containing `wrong_text` (linear scan of `manifest["chunks"]`), substitute
  `wrong_text -> corrected_text`, and re-TTS that one chunk **verbatim** via
  `edit_chunk(..., speech_only=True, restitch=False)`. One `restitch_from_chunks`
  per track after all substitutions. Atomic JSON audit
  (`<track>-corrections-audit.json`) with one `CorrectionAuditEntry` per
  correction.
- **`swanki/models/cards.py`** (MODIFY) — `SourceCorrection` (authored spec row:
  `id`, `track`, `wrong_text`, `corrected_text`, `reason`, `kind`, optional
  `note_text`; `@model_validator` requires `reason` for `override`, forbids
  `note_text` for `restoration`) and `CorrectionAuditEntry` (emitted outcome).
- **`swanki/audio/comment_edit.py`** (MODIFY) — `edit_chunk` gains
  `restitch: bool = True`; a batch passes `restitch=False` so the single stitch
  is hoisted out. Everything else (archive, re-TTS, manifest write, edit-log) is
  unchanged; the 11 existing tests still pass.
- **`swanki/conf/audio_correctness_gate/default.yaml`** (MODIFY) — new
  `corrections` sub-block: `apply_corrections: false`, `spec_dir: null`.
- **`swanki/pipeline/pipeline.py`** (MODIFY) — after the reading/lecture audit
  hooks, a `_apply_corrections` closure (double-nested config read) applies the
  spec when enabled and a `<citation_key>.yaml` exists under `spec_dir`. Opt-in,
  no-op by default.

### Key decisions

- **override vs restoration branches purely on the authored `kind`** — never
  inferred. `override` = the source is genuinely wrong: substitute AND (reading
  only) splice a spoken `[pause] Swanki correction: the source says X, but Y is
  correct, because ... [pause]` note **mid-chunk** (never at a chunk boundary,
  where `append_chunk_pause` strips the framing `[pause]` tags). `restoration` =
  mechanical fix (number-bug, splice, OCR garble, Try->Tyr): substitute
  **silently**.
- **Verbatim re-roll, not the auto-scrub `new_text` path** — the applier
  assembles the final chunk text pre-shaped and stores it to `chunk["text"]`,
  then re-rolls via `speech_only=True` (no re-preprocess), so a note containing
  `C 10 H 16` or `minus 0.32 V` is spoken as authored rather than mangled by
  `verbalize_large_numbers` / `expand_acronyms_for_tts`.
- **Reading fails loud; lecture is `not_applicable` on a literal miss** — a
  reading `wrong_text` that no longer matches is a real error (raises); lecture
  is paraphrased first-person prose (no spoken notes even for overrides, no LLM
  rewrite in v1) so a miss records `not_applicable`.
- **Idempotency via per-chunk `applied_corrections` ids** — checked BEFORE the
  `wrong_text` scan (whose needle is gone after a prior apply); apply-twice ==
  apply-once.

### Verification

`tests/test_source_corrections.py` (10 tests, fixtures from the Kuchel
spoken/silent list): override spoken-note mid-chunk + `[pause]` survival,
pre-shaped `note_text` formula survival, silent restoration, reading not-found
raises, idempotency, lecture not-applicable, lecture literal silent substitution,
and the three Pydantic validators. `tests/test_audio_comment_edit.py` (11)
confirms `restitch=False` did not regress. mypy clean on the new file; ruff
clean on all changed files.

### Out of scope (v1)

Generation-time / Pass-2 integration, spoken lecture notes, LLM lecture
rewriting, and auto-application of critic findings — all deferred.
