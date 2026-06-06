---
id: 9509rs1ch96ll5r998b2cg9
title: '06'
desc: ''
updated: 1780781146781
created: 1780781146781
---

## Context

Fish Speech renders each TTS chunk with a per-chunk prosodic arc: a loud/hard
onset, a settle into natural speech, then a fast/monotone tail. That arc is
pleasant inside a well-sized paragraph but turns "musical" (unnatural,
sing-song) at chunk seams under two chunking pathologies:

1. **Single-sentence chunks.** A chunk that is exactly one sentence gives Fish
   no room to settle, and its tail often lands on a question-like *uptone* even
   on a flatly declarative statement. This is the harmful failure mode.
2. **High size variance.** When chunk sizes swing widely, the onset/settle/tail
   arc is inconsistent seam-to-seam, so the listener hears a lurching cadence
   instead of steady lecture pacing.

The fix is to **adapt chunking** (and add a tiny audio touch-up) — we do NOT
overfit the authored text to TTS. Lectures stay written for humans; only the
*partitioning* of that prose into TTS chunks changes.

**Validated offline sweep (Hamming CH01-10, text-only).** Current production
chunking: 253 chunks, mean 493 chars, stdev 158, max 699, with **20
single-sentence chunks (8%)** — the harmful set — clustered in
CH01/03/04/05/07/09 and entirely absent from CH02/06/08/10. The winning swept
setting **S8** (soft target 500 / hard cap 650, balanced even-split,
min-2-sentence invariant) yields: 295 chunks, mean 423, median 408, stdev 95,
max 649, single-sentence **20 -> 1** — and the lone survivor is a safe ~280-char
long sentence that needs no settle room. Lower stdev (158 -> 95) directly tames
the variance pathology.

Plus a **conservative per-chunk linear onset fade-in** (~25ms, config-gated
`chunk_onset_fade_ms`, `0` = off) applied at chunk stitching. It rounds only the
harsh hard onsets while preserving the pleasant re-attacks the user likes.

**Out of scope.** No rewriting of lecture prose for TTS. No full audio
regeneration. The CH03/CH04 deliverable here is a **text-only A/B** of the new
chunk distribution; actual re-TTS of CH03/CH04 and the ABS-bookmark
clear/re-mark is a separate, deferred, user-approved step (see Open Questions).

## Relevant Files

| Path | Action | Purpose | Stance |
|---|---|---|---|
| `swanki/audio/_common.py` | MODIFY | Add opt-in second-pass balanced repack + min-2-sentence invariant to `chunk_text_paragraphs`; add onset fade in `_load()` | IN-FLUX (25+ dated entries thru 2026.06.02) |
| `swanki/audio/lecture.py` | MODIFY | Wire `soft_max_chars` + `chunk_onset_fade_ms` from `tts_kwargs` into chunker + stitch call | STABLE (latest 2026.05.31) |
| `swanki/conf/models/fish_speech.yaml` | MODIFY | `max_chars` 700->650 (hard), add `soft_max_chars: 500`, add `chunk_onset_fade_ms: 25` | STABLE config (no paired note) |
| `tests/test_audio_common.py` | MODIFY | Unit tests for even-split, merge precedence, escape hatches, hard cap, byte-identical non-fish default | n/a |
| `.../hammingArtDoingScience2020/hammingArtDoingScience2020_CH03_history-of-computers-hardware/lecture_transcript/*_transcript_cleaned_markdown.md` | REFERENCE | A/B source CH03 | n/a |
| `.../hammingArtDoingScience2020_CH04_history-of-computers-software/lecture_transcript/*_transcript_cleaned_markdown.md` | REFERENCE | A/B source CH04 (EXCLUDE `_CH04_..._4card_BAK`) | n/a |

Transcript root: `/scratch/projects/torchcell-scratch/Swanki_Data/hammingArtDoingScience2020/`.

## Key Design Decisions

1. **Additive signature, preserved defaults (resolution a).** Add optional
   keyword params to `chunk_text_paragraphs` — keep the existing
   `(text, max_chars=4500)` defaults intact. The new balanced logic activates
   ONLY when the fish caller opts in. *Why:* non-fish callers (reading.py,
   summary.py, retts script, existing tests) must stay byte-identical; an
   additive signature with off-by-default behavior guarantees that.

2. **Second pass, not a rewrite (resolution b).** The balanced even-split +
   min-2-sentence repack is a NEW opt-in pass layered AFTER the existing stable
   greedy packer (`_common.py:321-340`). *Why:* the greedy loop is load-bearing
   and well-tested; rewriting it risks regressing non-fish output and the
   manifest contract. A post-pass that takes the greedy chunk list and
   re-balances is isolatable and reversible.

3. **`soft_max_chars` is new and additive; `max_chars` stays the hard cap
   (resolution c).** Fish config carries both: `max_chars: 650` (hard, never
   exceeded) and `soft_max_chars: 500` (balancing target). No key is renamed.
   *Why:* the greedy first pass still guarantees the absolute cap; the soft
   target only drives how the second pass distributes sentences within that cap.

4. **Hard cap 700 -> 650 is acceptable (resolution e).** It is a config knob,
   not a code constant, and aligns with the prior "Fish decays past ~700" intent
   with margin. *Why:* it does not conflict with "Hamming fully regenerated
   2026-06-01" because the deliverable here is text-only A/B — no re-TTS lands.

5. **A/B verified by a THROWAWAY script (resolution d).** Distribution numbers
   are produced by a disposable text-only script whose output goes in the PR /
   this note; we do NOT commit a bespoke `scripts/` tool. *Why:* durable
   coverage belongs in `tests/test_audio_common.py`; a one-shot measurement
   script is noise in the repo.

6. **Even-split metric is char-based (open decision, chosen).** Split an
   over-soft paragraph into `ceil(char_len / soft_max_chars)` groups, then
   distribute WHOLE sentences across those groups balancing by char count.
   *Why:* char count is the quantity Fish's arc actually responds to; sentence
   count would let one long sentence dominate a "balanced" group.

7. **Even-split group boundary typing (open decision, chosen).** The first
   even-split group keeps boundary `"paragraph"`; the remaining groups are
   `"sentence"`. *Why:* this preserves the intra-paragraph short gap (500ms)
   between subdivided pieces vs the 1100ms paragraph gap, matching the manifest
   contract (`boundary ∈ {paragraph, sentence}`, first chunk always
   `paragraph`). Stated explicitly because it affects pacing AND the manifest.

8. **Min-2-sentence merge precedence (open decision, chosen).** When a chunk is
   a single sentence, try to merge into the **smaller neighbor** first; if that
   would exceed the hard cap, try the **larger neighbor**; if both would exceed
   the cap, **accept the lone chunk**. Lone chunks are also accepted when the
   single-sentence chunk is a paragraph-of-one at the section start/end with no
   mergeable neighbor, or when the sentence itself is too long to settle (the
   S8 ~280-char survivor). *Why:* smaller-neighbor-first minimizes resulting
   variance; the escape hatches keep the cap inviolable and avoid pathological
   loops.

9. **Onset fade lives in `_load()` after gain-match, before append (frozen
   constants untouched).** `seg = seg.fade_in(onset_ms)` is inserted in
   `_common.py:_load` between `_gain_match(seg)` (1288) and the
   `append(..., crossfade=)` (1329). *Why:* gain-match must see the true dBFS
   first; fading after gain-match shapes only the leading edge. The frozen
   empirical constants (`tail_buffer_ms=350`, `gain_match_target_dbfs=-25.0`,
   pause map 1100/500) change only via config knobs, never in code.

## Approach

**Second-pass balanced repack.** `chunk_text_paragraphs` gains optional kwargs:
`soft_max_chars: int | None = None` and `min_sentences_per_chunk: int = 1`
(fish passes `2`). Stages 1-2 (split + greedy pack to `max_chars`) run
unchanged. When `soft_max_chars` is set, a NEW Stage 3 runs:

- For each greedy chunk whose char length exceeds `soft_max_chars` AND that came
  from a single source paragraph, recompute the sentence list and re-split into
  `ceil(char_len / soft_max_chars)` groups, distributing whole sentences to
  balance total chars across groups. First group inherits the chunk's boundary;
  subsequent groups get `"sentence"` (Decision 7).
- Then a min-sentences pass merges single-sentence chunks per the precedence in
  Decision 8. The hard `max_chars` cap is re-checked on every merge so it is
  never exceeded.

When `soft_max_chars is None` (all non-fish callers), Stage 3 is skipped and the
function returns the exact legacy greedy result — byte-identical.

Merge precedence (the one disambiguating snippet):

```text
for chunk c that is a single sentence:
    small, large = sorted((prev, next), key=len)   # existing neighbors only
    if small and len(small) + len(c) <= max_chars:  merge c into small
    elif large and len(large) + len(c) <= max_chars: merge c into large
    else:                                            keep c as a lone chunk
```

**Onset fade.** `_accumulate_timeline` (and thus
`combine_audio_with_section_pauses` / `restitch_from_chunks`) reads a new
`chunk_onset_fade_ms: int = 0` param. In `_load()`:

```python
seg = _gain_match(seg)
if chunk_onset_fade_ms > 0:
    seg = seg.fade_in(chunk_onset_fade_ms)
return seg
```

`pydub.AudioSegment.fade_in` is already importable (`_common.py:21`). At Fish's
44100Hz, 25ms ≈ 1102 samples — well above any click threshold and inaudible as
a level change, so it rounds the hard onset without dulling the re-attack.

**Config wiring.** `lecture.py` resolves the knobs from `tts_kwargs`:
`chunking_cfg.get("soft_max_chars")` (None if absent -> legacy behavior) is
passed to `chunk_text_paragraphs(..., soft_max_chars=..., min_sentences_per_chunk=2)`
for the fish path only; `postprocessor.get("chunk_onset_fade_ms", 0)` is threaded
into the stitch call. `fish_speech.yaml` gets `max_chars: 650`,
`soft_max_chars: 500`, and `chunk_onset_fade_ms: 25`. ElevenLabs / non-fish
configs ship none of these keys, so their resolved values default to legacy /
off and their byte output is unchanged.

**Text-only A/B method.** A throwaway script reads the CH01-10 cleaned
transcripts, runs `chunk_text_paragraphs` under old vs new params, and prints the
per-chapter distribution. No Fish server, no audio, no committed artifact
(Decision 5). Expected results are in Verification.

## Gotchas

1. **Pre-existing CI red — do not adopt.** main already has ~50 mypy errors
   (incl. `_common.py:898` `float()`, `tts_kwargs: object` splats, `zotero.py`)
   and a failing `test_audio_presets_renamed`. Isolate NEW mypy errors with grep
   against a baseline; do not attribute the pre-existing red to this work, and do
   NOT change the `text_to_speech` signature.

2. **Byte-identical non-fish path.** reading.py, summary.py, the retts script,
   and existing chunker tests must produce identical output. Guard: Stage 3 and
   the onset fade are both strictly gated (`soft_max_chars is None`,
   `chunk_onset_fade_ms == 0`). A regression test asserts the legacy default
   path is unchanged.

3. **Frozen empirical constants.** `tail_buffer_ms=350`,
   `gain_match_target_dbfs=-25.0`, pause map `paragraph:1100 / sentence:500` are
   tuned and stay in code; expose new behavior only via config knobs.

4. **`_4card_BAK` exclusion.** The CH04 transcript dir has a sibling
   `_CH04_..._4card_BAK`; the A/B script must read the canonical
   `_CH04_history-of-computers-software` dir only.

5. **Additive manifest schema.** `chunk_manifest.json` `chunks[]` keeps
   `{index, section, text, file, boundary}` with `boundary ∈
   {paragraph, sentence}`, first chunk always `paragraph`, text = raw source
   prose. Even-split groups must emit valid boundary values (Decision 7); any
   field additions must be ADDITIVE — downstream `restitch_from_chunks`, the
   query API (`chunk_time_window` / `time_to_chunk`), `/audio-fix-from-annotations`,
   and `surgical.py` depend on this shape.

6. **Onset fade + crossfade double-attenuation.** The 25ms `fade_in` is applied
   pre-append, then `append(crossfade=50ms)` overlaps the same leading region —
   possible mild double-attenuation at the seam. Flag as a **listen-check before
   broad rollout**; out of scope for the text-only deliverable.

7. **Boundary typing changes pause pacing.** Mislabeling even-split groups as
   `paragraph` would insert 1100ms gaps mid-paragraph. Decision 7 (first group
   `paragraph`, rest `sentence`) is load-bearing for cadence — verify in tests.

8. **Fish server only needed for actual audio.** The text-only A/B and all unit
   tests run without `localhost:8080`; only the deferred re-TTS step needs Fish.

## Verification

**Unit tests (`tests/test_audio_common.py`, durable coverage):**

- Even-split: an over-soft single paragraph splits into the expected number of
  near-equal-char groups; first group boundary `paragraph`, rest `sentence`.
- Merge-into-smaller-neighbor: a single-sentence chunk merges into the smaller
  adjacent chunk when under cap.
- Escape hatches: single-sentence chunk at section start/end with no mergeable
  neighbor stays lone; single sentence that would push both neighbors over cap
  stays lone; an over-cap-length single sentence stays lone (S8 survivor).
- Hard cap never exceeded under the new pass for any input.
- Non-fish default path (`soft_max_chars=None`, `min_sentences_per_chunk=1`)
  returns byte-identical output to today — pin against the existing
  700-cap / oversize-fallback / packing / two-paragraph tests.

**Text-only A/B (throwaway script, results -> PR/note):** reproduce ~S8 over
CH01-10 — ~295 chunks, mean ~420, stdev ~95, single-sentence ~1 — and report
CH03 and CH04 old-vs-new distributions (count, mean, stdev, max, single-sentence
count).

**Lint/type isolation:** run ruff on changed files; run mypy and diff against the
pre-existing baseline so only NEW errors surface (grep the touched files).

**Commit trio:** paired dendron notes are `notes/swanki.audio._common.md` and
`notes/swanki.audio.lecture.md`.

## Open Questions

1. **Even-split boundary typing.** Confirm Decision 7 (first even-split group
   `paragraph`, rest `sentence`) — the one choice that visibly shifts inter-chunk
   pacing and the manifest.

2. **Deferred re-TTS.** Confirm that actual re-TTS of Hamming CH03/CH04 with the
   new chunking — plus the ABS-bookmark clear and re-mark — is deferred to a
   separate approved step, and that this PR ships only the chunker/config/onset
   changes + the text-only A/B evidence.
