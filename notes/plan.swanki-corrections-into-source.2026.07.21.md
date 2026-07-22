---
id: l50r2eo25ujb5irdehh7o47
title: '21'
desc: ''
updated: 1784696291901
created: 1784696291901
---

## Context

The Kuchel sweep (`notes/swanki.audio.kuchel-comments-runbook.2026.06.09.md`, 2026.07.21 section) produced a hand-authored, hand-verified list of source-fidelity fixes: 14 spoken overrides plus a silent-restoration list. Today those exist only as prose in a runbook and get replayed by throwaway scratchpad scripts (`scratchpad/apply_edits.py`). This plan makes a **Swanki correction** a first-class, structured, durable source feature: a `{wrong_text, corrected_text, reason, kind}` record, authored per chapter in YAML, applied to the reading/lecture **manifest chunk text** and re-TTS'd through the shipped surgical edit path.

Two behaviors, branched purely on the authored `kind`:
- **override** — the source is genuinely wrong. Substitute the corrected prose AND splice a spoken `[pause] Swanki correction: the source says X, but Y is correct, because ... [pause]` note into the chunk so the listener hears the dispute.
- **restoration** — a mechanical fix (number-bug, splice removal, OCR-garble to readable, Try->Tyr). Substitute **silently**; no spoken note.

This builds directly on the report-only critic `swanki/audio/reading_correctness.py` (PR `#51`) but is **strictly separate** from it. `#51` detects and writes JSON audits; it NEVER mutates audio, and its module note already says "corrections are the next layer". Corrections are that layer: a **higher bar** than the critic (hand-authored, every override verified against the printed source), an **opt-in apply layer** that is NEVER auto-populated from critic findings. The gap `#51` leaves is exactly this: turning a verified finding into corrected, re-voiced audio without re-implementing re-TTS or drifting the manifest / `chunk_timeline.json` / mp3 / ABS bookmarks out of sync.

## Relevant Files

| Path | Action | Purpose | Stance |
|---|---|---|---|
| `swanki/audio/source_corrections.py` | NEW | The apply layer: load YAML spec, per-correction substitute + (override) splice note, verbatim re-TTS via chunk-edit, one restitch/track, JSON audit. | new |
| `swanki/models/cards.py` | MODIFY | Add `SourceCorrection` (authored spec row, `Literal` kind + `@model_validator`) and `CorrectionAuditEntry` (emitted outcome). | stable pattern (add near `ReadingChunkFidelity` ~1356) |
| `swanki/audio/comment_edit.py` | MODIFY | `edit_chunk` gains optional `restitch=False` so a multi-chunk batch re-TTS's each chunk then restitches ONCE per track. | in-flux |
| `swanki/audio/reading_correctness.py` | MODIFY | Update the header note: the "next layer" now exists at `source_corrections.py`; critic stays report-only. | in-flux (merged 2026.07.21) |
| `swanki/pipeline/pipeline.py` | MODIFY | After the reading/lecture audit hooks (L2372-2407 / L2449-2496), invoke the apply layer when config enables it. | in-flux |
| `swanki/conf/audio_correctness_gate/default.yaml` | MODIFY | Add a `corrections` sub-block (`apply_corrections: false`, `spec_dir`) beside the reserved `report_only` slot. | reference |
| `swanki/conf/config.yaml` | REFERENCE | Gate already registered (defaults L13, top-level null L30); no change unless a new group. | stable |
| `swanki/audio/_common.py` | REFERENCE | `append_chunk_pause` L223 (strips boundary pauses), `preprocess_for_tts` L129, `verbalize_large_numbers` L838, `expand_acronyms_for_tts` L661, `write_chunk_manifest` L1900. | stable |
| `swanki/pipeline/card_correctness.py` | REFERENCE | `run_correctness_gate` / `write_audit` shape to mirror (pass/fixed/dropped, atomic JSON). | stable |
| `swanki/conf/corrections/<citation_key>.yaml` (or `spec_dir`) | NEW (data) | Hand-authored per-chapter corrections spec. | new |
| `tests/test_source_corrections.py` | NEW | Fixture-driven tests from the Kuchel 14-spoken/silent list. | new |
| `notes/swanki.audio.source-corrections.md` | NEW | Paired dendron module note. | new |

## Key Design Decisions

1. **Post-hoc authored spec applied to manifest chunks — reject generation-time / Pass-2.** Pass-2 windows are pre-scrub and regenerated every run; the manifest chunks are the durable post-scrub artifact that survives `audio_only` reruns and is what `edit_chunk` already mutates. Applying at generation time would re-run on every gen, couple corrections to LLM rewriting, and put mutation inside the critic/generation code. Corrections are a **separate post-hoc pass over the manifest**.

2. **Override-note chunks are re-rolled VERBATIM (speech_only semantics) — reject the auto-scrub `new_text` path.** `edit_chunk`'s `new_text` path runs `append_chunk_pause(preprocess_for_tts(raw_new, ..., add_pauses=True))` (comment_edit.py L284), and `preprocess_for_tts` runs `verbalize_large_numbers` (>=100, default-on) and `expand_acronyms_for_tts`. A correction note routinely contains `C10H16` or `minus 0.32 V`; the scrubber would mangle them to spoken garbage. So the apply layer **assembles the final chunk text itself, pre-shaped**, and re-rolls it verbatim — the `speech_only` path re-TTS's `chunk["text"]` as-is with no re-preprocess (L265, L287-288).

3. **The spoken note is PRE-SHAPED by the author/assembler, not scrubbed.** Formulas and quantities are written the way TTS should say them (`C 10 H 16`, `minus zero point three two volts`). Because the assembled string is stored to the manifest and re-rolled verbatim, what is authored is exactly what is spoken. The corrected *prose* substitution is ordinary reading text (already scrub-clean in the source); only the note needs pre-shaping.

4. **`edit_chunk` gains `restitch=False`; the batch restitches ONCE per track.** Honors "don't re-implement re-TTS": each correction still re-TTS's its one chunk through `edit_chunk`, but the single `restitch_from_chunks` call (comment_edit.py L314) is hoisted out and called once per track after all substitutions. Matches the runbook batch precedent (CH05: 26 chunks x ~122s restitch each saved). Only the existing restitch call moves; the re-TTS mechanics are untouched.

5. **`kind` is an authored REQUIRED field; branch purely on it, NEVER infer.** override vs restoration is a human judgment about whether the source is genuinely wrong. `SourceCorrection.kind` is `Literal["override","restoration"]`, required. The applier branches on it and never guesses from the text or from critic findings.

6. **override -> spoken note; restoration -> silent.** Encodes the runbook contract: a genuine source dispute must be voiced ("Swanki correction: the source says X, but Y is correct, because ..."); a mechanical restoration (number-bug, splice, OCR garble, Try->Tyr) is fixed silently because there is nothing for the listener to adjudicate.

7. **Reading = full support; lecture = silent, literal-match-only, else `not_applicable`.** Reading gets literal substitution + spoken-note-on-override + silent-on-restoration. Lecture is first-person reformulated prose: no spoken notes even for overrides (runbook CH03 Phe 38), and no LLM rewriting in v1. A lecture correction applies only if `wrong_text` literally appears in a lecture chunk (silent substitution); otherwise the applier records `not_applicable` and flags for manual handling. No LLM-mediated lecture rewriting in v1.

8. **Reading substitution FAILS LOUD when `wrong_text` is not found.** A correction that no longer matches (source re-OCR'd, chunk boundaries shifted) is a real error, not a no-op. Reading raises; lecture records `not_applicable` (its prose is expected to diverge).

9. **The note is spliced MID-chunk, never at chunk start/end.** `append_chunk_pause` strips leading+trailing `[pause]` tags for Fish (comment_edit / _common.py L223) — a boundary note's framing pauses would vanish and Fish would run it into the neighbor. Splicing mid-chunk keeps the internal `[pause]` tags intact.

10. **Idempotency via per-chunk applied-ids in the manifest.** Each correction has a stable id; on apply the id/hash is stored on the chunk record, and an already-present id short-circuits. Re-running the spec is a no-op (apply-twice == apply-once), so a chapter can be re-swept safely.

11. **Config under `audio_correctness_gate.corrections`, default off; NEVER auto-apply critic findings.** Reuses the reserved enforcing slot beside `report_only`. `apply_corrections: false` by default — the report-only critic and this apply layer share config surface but the apply layer is strictly opt-in and reads a **hand-authored** spec, never the critic's JSON audit. Higher bar, human-verified, opt-in.

## Approach

**The YAML spec.** Per chapter, `swanki/conf/corrections/<citation_key>.yaml` (or the config `spec_dir`), a list of `SourceCorrection` rows:

- `id: str` — stable, e.g. `ch03-phe-55`; the idempotency key.
- `track: Literal["reading","lecture"]`
- `wrong_text: str` — literal substring that must appear in the target chunk.
- `corrected_text: str` — replacement prose (plain reading text).
- `reason: str` — the "because ..." clause; required for override, surfaced in the spoken note.
- `kind: Literal["override","restoration"]` — required; drives spoken-vs-silent.
- `note_text: str | None` — optional pre-shaped spoken-note override (formulas/quantities written as spoken). When absent for an override, the applier assembles the default template from `corrected_text` + `reason`; author supplies this whenever the note contains formulas/numbers. A `@model_validator` requires `reason` (and permits `note_text`) when `kind=="override"`, and forbids `note_text` when `kind=="restoration"`.

**The batch applier flow** (`apply_source_corrections(manifest_paths, spec, tts_kwargs, ...)` in `source_corrections.py`):

1. Load + validate the spec (Pydantic parses each row; invalid kind/missing reason fails at load).
2. Group corrections by track/manifest. For each correction:
   - Locate the chunk containing `wrong_text` (linear scan of `manifest["chunks"]`). Reading: **assert found, fail loud** if not. Lecture: if not found, record `CorrectionAuditEntry(status="not_applicable")` and continue.
   - Short-circuit if the chunk already carries this correction id (idempotency) -> `status="already_applied"`.
   - Substitute `wrong_text` -> `corrected_text` in the chunk text.
   - If `kind=="override"` and track is reading: assemble the pre-shaped note and **splice it mid-chunk** (after the sentence containing the substitution, never at the chunk boundary).
   - Store the assembled verbatim text back to `chunk["text"]`, append the applied id to a `chunk["applied_corrections"]` list.
   - Re-TTS this one chunk verbatim: `edit_chunk(manifest_path, idx, speech_only=True, tts_kwargs=..., restitch=False)` (speech_only re-rolls the already-shaped stored text; `restitch=False` defers the stitch).
3. After all substitutions for a track: `restitch_from_chunks(manifest_path, output_file)` **once**.
4. Emit the JSON audit atomically (temp-then-rename), one `CorrectionAuditEntry` per correction: id, track, chunk_index, kind, status (`applied` / `already_applied` / `not_applicable`), `spoken` (bool), wrong/corrected snippets, git hash.

The default spoken note (when `note_text` is absent) is `[pause] Swanki correction: the source says {wrong_text}, but {corrected_text} is correct, because {reason} [pause]`; `_splice_after_substitution` inserts it after the substitution sentence — never at `chunk[0]`/`[-1]`, where `append_chunk_pause` would strip the framing pauses — and stores the result verbatim to `chunk["text"]` for the `speech_only` re-roll.

**Config wiring.** In `audio_correctness_gate/default.yaml` add under the existing block:
```yaml
  corrections:
    apply_corrections: false            # opt-in apply layer; never on by default
    spec_dir: null                      # dir of <citation_key>.yaml specs
```
Read it in `pipeline.py` with the **double-nested** access already used for the gate (`self.config.get("audio_correctness_gate",{}).get("audio_correctness_gate",{})`, L2375/2452) — a single `.get` silently returns `{}`. Both `config.yaml` sites already register the group (defaults L13, null slot L30); no new registration needed.

**Pipeline hook.** After `write_reading_audit` (L2406) and `write_lecture_audit` (L2495), when `corrections.apply_corrections` and a spec exists for `citation_key`, call `apply_source_corrections` on the just-written manifest(s), then re-run the targeted ABS refresh path already used by surgical edits (bookmarks do not migrate — the restitch rewrites `chunk_timeline.json`).

**Fish-context requirement.** `edit_chunk` asserts a `reference_id` for `fish_speech` (comment_edit.py L257). The apply layer therefore requires a live Fish context (`SWANKI_FISH_PORTS`, reference voice in `tts_kwargs`); it is invoked inside a Fish-up run/job, same as any surgical edit.

## Gotchas

1. **Boundary-pause stripping** (rationale: Decision 9). **Sidestep:** always splice mid-chunk (`_splice_after_substitution`), and test that internal `[pause]` tags survive the store->re-roll chain.

2. **Scrubber mangles formulas/quantities** (rationale: Decisions 2-3). **Sidestep:** never use the `new_text` path for override-note chunks; pre-shape the note, store the assembled string, re-roll via `speech_only=True` (verbatim, no re-preprocess).

3. **`kind` inference** (rationale: Decision 5). **Sidestep:** `kind` is a required authored `Literal`; branch on it only; no heuristic from text or critic findings.

4. **Idempotency double-speak** (rationale: Decision 10). Re-running a spec would otherwise splice the note twice / substitute a now-absent `wrong_text`. **Sidestep:** store applied ids on the chunk, short-circuit already-applied; test apply-twice == apply-once.

5. **Reading-verbatim vs lecture-paraphrase** (rationale: Decisions 7-8). **Sidestep:** reading fails loud on not-found; lecture records `not_applicable` and applies only on a literal match. No LLM lecture rewriting in v1.

6. **Config double-nest** (mechanism: Approach / Config wiring). **Sidestep:** double-nest exactly as L2375/2452; unit-test that `apply_corrections` flips.

7. **Fish live context** (requirement: Approach / Fish-context). Missing `reference_id` renders the edited chunk in the wrong voice (the `edit_chunk` assert at L257 fires first). **Sidestep:** require `SWANKI_FISH_PORTS` + reference voice; run inside a Fish-up job; assert early.

8. **Pre-commit hook.** Lint only the files this change touches (`/ruff`, `/mypy` on the changed set); `--no-verify` if the hook blocks.

9. **pydantic-ai major pin.** pydantic-ai **v2.0 shipped 2026-06-23** (web-sourced; installed here is 1.51.0, `pyproject` is unbounded `>=0.1`). v2 has real breaking changes (RetryConfig, evaluator removal). **Sidestep:** opportunistically pin `>=1.0,<2` while touching deps — do NOT introduce new pydantic-ai API surface in this PR.

## Verification

**Tests** (`tests/test_source_corrections.py`, fixtures from the Kuchel 14-spoken/silent list — CH03 55/60/79/190, CH02 89/90/122/54/126/157, CH04 48/60, CH05 15/35; silent set: number-bug, splices 35/37/143/272, ATP 174, OCR 6/40, Try->Tyr 150):

- override reading chunk gets the spoken note AND its internal `[pause]` tags survive the store->`speech_only` re-roll (no boundary strip of the mid-chunk pauses).
- restoration chunk is substituted with NO spoken note.
- `wrong_text` not found in a reading chunk **raises**.
- apply-twice == apply-once (idempotency: second run all `already_applied`, chunk text unchanged, note not duplicated).
- config flag flips: `apply_corrections=false` -> no mutation; `true` -> applied.
- lecture correction whose `wrong_text` is absent -> `CorrectionAuditEntry.status == "not_applicable"`, no mutation.
- Pydantic: `kind` outside the `Literal` fails; override without `reason` fails the `@model_validator`; restoration with `note_text` fails.

**Commands:** `/ruff` and `/mypy` on the changed files only; `pytest tests/test_source_corrections.py tests/test_audio_comment_edit.py` (the latter to confirm `restitch=False` did not regress the 11 existing edit tests).

**Manual smoke:** inside a Fish-up job, apply a 2-3 row spec (one override, one restoration) to a real chapter reading manifest; confirm the re-TTS'd override chunk audibly contains "Swanki correction: ..." with the pre-shaped formula spoken correctly, the restoration chunk is silent, and exactly ONE restitch fired (check `chunk_timeline.json` mtime + a single restitch log line).

## Open Questions

None blocking. Two points resolved by recommendation: (a) lecture overrides whose `wrong_text` does not literally match are **deferred** to manual handling via `not_applicable` (no LLM rewrite in v1) — we proceed. (b) The idempotency key is the authored `id` (stable, human-readable) with the applied-id list stored on the chunk record; a content hash is unnecessary given ids are unique per spec — we proceed with `id`.
