---
id: gvq4c4ctaxsukqoc4s6kq6d
title: '21'
desc: ''
updated: 1784673710345
created: 1784673710345
---

## Context

The audio pipeline can ship transcripts that are word-fluent but factually or
structurally wrong, and nothing today catches it. Three failures surfaced in
production this session, all on the READING and LECTURE transcript tracks:

1. **Source-fidelity drift.** On CH03 the reading Pass-2 LLM spliced the clause
   "as small as 22 nucleotide residues long" out of one source page and injected
   it into three unrelated reading chunks. The only guard at that boundary is a
   token-count length-ratio floor (`_PASS2_CHUNK_MIN_RATIO = 0.85` in
   `swanki/audio/reading.py`), which is blind to insertions and duplications: a
   chunk that drops one sentence and gains another nets out near 1.0 and passes.
2. **Wrong acronym expansion.** On CH03/CH04 a two-layer interaction produced a
   phantom enzyme. Pass-2 rule 2 does first-use expansion ("adenosine
   triphosphate, ATP") once per document; then `expand_acronyms_for_tts`
   (`swanki/audio/_common.py:661`) letter-spells the surviving token
   "ATP" -> "A-T-P". The two compose to "adenosine triphosphate, A-T-P
   sulfurylase" -- a nonexistent name -- with neither layer aware of the other.
3. **Incorrect / outdated content.** No pass checks whether a claim in the
   transcript is simply wrong or stale relative to current knowledge.

The existing card correctness gate (`swanki/pipeline/card_correctness.py`,
PR `#24`) is the right structural model but does not help here: it hooks at
`generate_outputs`, and `audio_only` runs skip that path entirely, so
audio-only regenerations get zero correctness coverage. This plan adds a
**separate, report-only audio correctness critic** that lives on the audio path,
survives `audio_only`, emits a per-chapter JSON audit per track, and never
mutates audio. Modes 1+2 are pure deterministic (stdlib `difflib`, no LLM, cheap)
and default ON; mode 3 is the single optional LLM factual pass, default OFF.

## Relevant Files

| Path                                              | Action    | Purpose                                                                                                                                              | Stance       |
|---------------------------------------------------|-----------|------------------------------------------------------------------------------------------------------------------------------------------------------|--------------|
| `swanki/audio/reading_correctness.py`             | NEW       | Critic module: normalized clause diff + acronym-double-emit validator + optional factual hook; per-chapter audit writer                              | n-a          |
| `swanki/audio/reading.py`                         | MODIFY    | Emit per-chunk fidelity signal inside Pass-2 loop (~307-314); run acronym validator on final `tts_transcript` (~370)                                 | in-flux      |
| `swanki/audio/lecture.py`                         | MODIFY    | Optional LLM claims-level factual hook (default off)                                                                                                 | in-flux      |
| `swanki/pipeline/pipeline.py`                     | MODIFY    | New audio-path hook at `generate_reading_audio` (~2372) / `generate_lecture_audio` (~2424) call sites; write the two audits; double-nest config read | in-flux      |
| `swanki/llm/agents.py`                            | MODIFY    | Register factual-pass agent additively next to `card_correctness_agent` (~51); reuse `get_model_string` (~87)                                        | stable       |
| `swanki/models/cards.py`                          | MODIFY    | Add new audio audit Pydantic models near `CardCorrectnessAssessment` (~1293)                                                                         | stable       |
| `swanki/audio/_common.py`                         | REFERENCE | `expand_acronyms_for_tts` (~661), `_ROMAN_NUMERAL_WORDS` (~633), `extract_acronyms` (~2355) -- validator must mirror their rules                     | in-flux      |
| `swanki/pipeline/card_correctness.py`             | REFERENCE | Structural template: verdict shape, fail-open, `write_audit` atomic pattern (~294)                                                                   | stable       |
| `swanki/conf/audio_correctness_gate/default.yaml` | NEW       | Hydra group: per-track + per-mode toggles, model override                                                                                            | n-a          |
| `swanki/conf/config.yaml`                         | MODIFY    | Register group in defaults list (~12) AND top-level null slot (~28)                                                                                  | provisional  |
| `swanki/conf/audio/reading.yaml`                  | REFERENCE | Preprocessor block holds `acronym_allowlist` the validator honors                                                                                    | undocumented |
| `notes/swanki.audio.reading_correctness.md`       | NEW       | Paired dendron design note (mandatory)                                                                                                               | n-a          |
| `tests/test_reading_correctness.py`               | NEW       | Paired test file: real fixtures for modes 1+2, monkeypatch for mode 3                                                                                | n-a          |

## Key Design Decisions

1. **New report-only audio-path hook, not a reuse of the card chokepoint.**
   The card gate fires at `generate_outputs`, which `audio_only` skips; audio
   regens would get no coverage. So orchestration + audit emission is a NEW hook
   at the `generate_reading_audio` / `generate_lecture_audio` call sites in
   `pipeline.py` (~2372/2424), because that is the one place both full runs and
   `audio_only` runs pass through. The fidelity signal is COLLECTED inside the
   `reading.py` Pass-2 loop; the audit is WRITTEN by the new hook.

2. **Deterministic checks default ON, LLM check default OFF.** Modes 1+2 have no
   API cost and catch the exact failures we saw, so gating them behind an
   opt-in would leave the known bugs unguarded; they run by default. Mode 3 is
   the only network call and can be noisy, so it is opt-in, mirroring how the
   card gate resolves its model (gate override else `get_model_string(llm)`).

3. **Diff at the Pass-2 input->output boundary, not against page files.** The
   check compares `chunk` (post-humanize source window) to `chunk_transcript`
   (Pass-2 output) inside the loop, a natural 1:1 pair needing no alignment.
   Diffing against `clean-md-singles/page-*.md` was rejected: Pass-2 tokenizes
   post-humanize text into 3000-token `cl100k_base` windows over reordered prose,
   which map to no page boundary, making page-level alignment intractable.

4. **New Pydantic models, new writer -- not `write_audit` reuse.** The audio
   audit records chunk index, inserted/duplicated/dropped blocks, acronym
   findings, and a `fell_back` flag -- a different schema from `CardAuditEntry`.
   We follow `write_audit`'s atomic temp-then-rename `json.dump(indent=2,
   ensure_ascii=False)` PATTERN but define new models and a new writer, because
   calling the card writer with a foreign schema would be wrong.

5. **Normalize both sides before diffing.** Legitimate, meaning-preserving
   Pass-2 edits (acronym first-use expansion, "et al" / citation collapse,
   `---SECTION_BREAK---` markers, per-digit codeword spelling) must not flood the
   diff. Both sides are normalized first; SequenceMatcher then runs over
   sentence-normalized tokens and only residual inserted/duplicated/dropped
   blocks are flagged.

6. **`fell_back` -> `not_assessed`, never `pass`.** When Pass-2 exhausts its
   retries (`_CHUNK_RETRY_ATTEMPTS`) it returns the humanized input verbatim, so
   output==input makes the diff trivially clean -- but that cleanliness is
   meaningless. Such chunks are marked `not_assessed`, not `pass`, so the audit
   never launders a fallback as a verified-clean chunk.

7. **Reading gets the clause diff; lecture does not.** Lecture is reformulated
   first-person prose (openings, roadmaps, SI injection), so a clause-exact diff
   floods false positives. Lecture receives ONLY the optional LLM factual pass
   (claims, not wording). Reading receives both deterministic checks plus, if
   enabled, the factual pass.

8. **One Hydra group, not two.** A single `audio_correctness_gate` group carries
   per-track (reading/lecture) and per-mode toggles. Rejected: two sibling
   groups (`reading_correctness_gate` + `lecture_correctness_gate`), which
   doubles registration sites and config surface for two checks that share one
   audit shape and one hook. (Recorded in Open Questions.)

9. **Calibration lives in the prompt, high-acceptance, factual-only.** Mirroring
   the card gate's `GATE_INSTRUCTIONS`: the factual pass is a factual-error
   catcher with a VERY HIGH acceptance rate, when-in-doubt-PASS, style out of
   bounds. Calibration is expressed in the prompt, not baked into model choice.

10. **Fail-fast except fail-open on assessment failure.** Following the card gate
    (fail-open precedent, commit `14fbfab`): an LLM assessment that errors or
    exhausts safety retries yields `assessment_failed`, is kept and logged, and
    never blocks or mutates. Deterministic-path bugs fail fast.

## Approach

**Critic module (`swanki/audio/reading_correctness.py`).** Modeled on
`card_correctness.py` but wired as a separate report-only audio-path hook. It
holds: the two deterministic reading functions, the acronym validator, the
optional lecture factual function, the new Pydantic models' orchestration, and
the new atomic audit writer.

**Reading check 1 -- normalized clause diff (deterministic, default on).**
Collected per-chunk inside the Pass-2 loop at `reading.py:~307-314`. For each
`(chunk, chunk_transcript, fell_back)` triple: if `fell_back`, record the chunk
as `not_assessed` and skip diffing. Otherwise normalize both sides, run
`difflib.SequenceMatcher` over sentence-normalized tokens, and record residual
`inserted` / `duplicated` / `dropped` blocks with the chunk index. Normalization
rules: strip `---SECTION_BREAK---`; collapse citations and "et al"; treat
acronym first-use expansion ("X (Full Form)" -> "Full Form, X") and per-digit
codeword spelling as ALLOWED edits (align them out before comparison); lowercase
and split on sentence boundaries.

**Reading check 2 -- acronym double-emit validator (deterministic, default
on).** Run ONCE post-scrubber on the final `tts_transcript` (`reading.py:~370`),
because the phantom name only exists after `expand_acronyms_for_tts` runs. Using
`extract_acronyms` (`_common.py:~2355`) semantics and the same letter-spell rule
set, detect the pattern where an expanded first-use ("adenosine triphosphate,
ATP") is immediately followed by the letter-spelled form of the same acronym
("A-T-P ..."), i.e. "adenosine triphosphate, A-T-P sulfurylase". Honor the
Roman-numeral carve-out (`_ROMAN_NUMERAL_WORDS`, `_common.py:~633`) so "II"->"two"
is never flagged, and honor the `acronym_allowlist` from `conf/audio/reading.yaml`.
This REPORTS a known generator gap (Pass-2 rule 2 expands once per doc but rule 9
leaves each chunk blind to others); the critic does not fix the generator.

**Lecture factual pass (LLM, default off).** An optional claims-level factual
check in `lecture.py` that assesses claims not wording, with the card-gate model
resolution (gate override else `get_model_string(llm)`) and a new agent
registered additively in `agents.py`. Verdicts follow the card gate:
`pass` / `fixed` / `dropped` / `assessment_failed` (fail-open). Report-only --
`fixed`/`dropped` verdicts are recorded, never applied to audio.

**Audit emission (new hook).** Two collection points feed ONE per-chapter audit
per track. For reading: the per-chunk fidelity blocks accumulate in the Pass-2
loop and the acronym findings come from the single post-scrubber call; the new
hook at `generate_reading_audio` writes `reading-correctness-assessment.json`.
For lecture: the factual verdicts feed `lecture-correctness-assessment.json` via
the hook at `generate_lecture_audio`. Both writers use the atomic
temp-then-rename `json.dump(indent=2, ensure_ascii=False)` pattern with a
`summary` count block plus per-chunk / per-claim entries.

**Config wiring.** New group `conf/audio_correctness_gate/default.yaml` with
`enabled: true`, `report_only: true`, per-track and per-mode toggles, and a
`model` override slot. Registered in BOTH `config.yaml` places: the defaults list
(~12) and the top-level null slot (~28). Read at the hook via the double-nest
form `cfg.get("audio_correctness_gate", {}).get("audio_correctness_gate", {})`
(see Gotchas).

## Gotchas

1. **Page-diff is intractable** (see Decision 3). Sidestep: diff the in-loop
   `chunk` vs `chunk_transcript` pair only.
2. **Legit transforms look like drift** (see Decision 5). Sidestep:
   normalize/align them out before SequenceMatcher so only residual blocks flag.
3. **Lecture is not verbatim** (see Decision 7). Sidestep: no clause diff on
   lecture; claims-level LLM pass only.
4. **Two-layer acronym.** The phantom name exists only after BOTH Pass-2 rule 2
   and `expand_acronyms_for_tts` run. Sidestep: validate the FINAL
   `tts_transcript` (post-scrubber), not the raw transcript, and honor the same
   allowlist + Roman-numeral carve-out.
5. **Config double-nest silent no-op.** Hydra group values land under
   `cfg["audio_correctness_gate"]["audio_correctness_gate"]`; a single `.get`
   silently returns `None` and disables everything. Sidestep: register in BOTH
   config sites and read via the double `.get(group, {}).get(group, {})`.
6. **`fell_back` masks drift** (see Decision 6). Sidestep: mark `not_assessed`.
7. **pydantic-ai v2 breaking release.** `pydantic-ai` is currently unbounded in
   deps (installed 1.51.0); per scout web-search, a breaking v2.0 landed
   2026-06-23. Sidestep: pin `pydantic-ai>=1.51,<2` as out-of-PR-scope hygiene so
   a silent major bump does not break `agents.py`.
8. **Module-name conflation.** `swanki/ocr/reading_order.py` (OCR box reorder,
   untracked) is NOT `swanki/processing/reading_reorder.py` (figure reorder,
   called at `reading.py:201`); neither is a diff reference. Sidestep: the diff
   reference is the in-loop Pass-2 pair, nothing else.
9. **Stale docstring copy.** The card gate's `write_audit` docstring history
   mentioned `.yaml` while writing `.json`; do not copy stale wording -- write
   fresh docstrings.

## Verification

**Tests (`tests/test_reading_correctness.py`, stronger than the card gate).**

- Mode 1: feed a fixture where the "as small as 22 nucleotide residues long"
  clause is spliced into a chunk whose source window lacks it; assert the diff
  reports it as `inserted`/`duplicated`. Feed a clean chunk; assert no findings.
  Feed a `fell_back=True` chunk; assert `not_assessed`, not `pass`. No LLM mock.
- Mode 2: feed "adenosine triphosphate, A-T-P sulfurylase" on the final
  `tts_transcript`; assert the double-emit is flagged. Feed "II"->"two" and an
  allowlisted acronym; assert NOT flagged. No LLM mock.
- Mode 3: monkeypatch the assessment function (as `tests/test_card_correctness.py`
  monkeypatches `_assess_card`) to return canned verdicts; assert `assessment_failed`
  is fail-open and report-only leaves audio untouched.

**Commands.**

- `/ruff` and `/mypy` on the changed files.
- `~/opt/miniconda3/envs/swanki/bin/Swanki python -m pytest tests/test_reading_correctness.py -q`
- Regression: `pytest tests/test_card_correctness.py tests/test_audio_*.py -q`.

**Manual smoke.** Mode 2's acronym check runs over CH03's final `tts_transcript`:
confirm the "adenosine triphosphate, A-T-P sulfurylase" double-emit is flagged.
Mode 1's fidelity diff needs the in-loop Pass-2 input->output pair, which the
`chunk_manifest` does NOT store (output text only) -- so it cannot be smoke-tested
by scanning the manifest; re-run CH03 reading with the hook enabled and confirm
the "22 nucleotide" splice is flagged. Then confirm no `.mp3` is modified
(report-only) and that `reading-correctness-assessment.json` shows a `summary`
block, per-chunk entries, and `not_assessed` for any fallback chunk.

## Open Questions

- **One Hydra group vs two.** We proceed with ONE group
  (`audio_correctness_gate`) carrying per-track + per-mode toggles; confirm this
  over two sibling groups before implementation lands.
