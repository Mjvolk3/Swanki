---
id: ip5337u5e3jsdysuznzxl79
title: '30'
desc: ''
updated: 1780182904680
created: 1780182904680
---

## Context

Two GLOBAL/structural audio changes driven by Hamming ABS lecture comments.

(1) **Asymmetric bookend pauses.** Today `combine_audio_with_section_pauses` uses a
single `bookend_pause_ms` (default 500) in two places: after the start bookend
(`_common.py` L1286) and before the end bookend (L1345). There is NO silence AFTER
the end bookend. ABS comments at 53.6m / 65.6m / 75.9m flag bookend pacing: the
front bookend should play almost immediately, the end bookend wants a distinct break
before it, and the file should not slam shut on the closing bookend. Split the one
knob into three: `bookend_start_pause_ms` (~300), `bookend_end_pause_ms` (~2000),
and a NEW `bookend_trailing_pause_ms` (~1500, silence after the end bookend).

(2) **Conceptual-strength lecture prompt.** ABS comment at 128.0m flags that the
closing summary lists takeaways but does not crystallize the single most important
conceptual idea the worked examples illustrate. Refine the EXISTING conclusion rule
in `book_voice.yaml` (Hamming/books only) without adding a section or word budget.

This note is the PR (worktree) plan. The re-stitch-all execution + ABS republish are
a POST-MERGE RUNBOOK, captured in
`notes/swanki.audio.hamming-comments-runbook.2026.05.29.md`, NOT in the PR.

## Relevant Files

| Path | Action | Purpose | Stance |
|------|--------|---------|--------|
| `swanki/audio/_common.py` | MODIFY | 3-knob split in `combine_audio_with_section_pauses` + `_accumulate_timeline`; trailing-pause site; `restitch_from_chunks` 3 new overrides + persist-to-manifest | provisional / core change |
| `swanki/conf/models/fish_speech.yaml` | MODIFY | 3 new postprocessor keys (300/2000/1500) | provisional |
| `swanki/conf/prompts/book_voice.yaml` | MODIFY | refine existing conclusion rule (~L341) | provisional |
| `swanki/audio/lecture.py` | MODIFY | read 3 keys from `post_cfg`, forward to combine, persist in manifest postprocessor (~L987/L1019) | provisional |
| `swanki/audio/reading.py` | MODIFY | same call-site forward + manifest persist (~L470) | provisional |
| `swanki/audio/summary.py` | MODIFY | same call-site forward + manifest persist (~L293) | stable / YAML-driven, inherits |
| `scripts/regen_hamming_bookends_ch1_10.py` | MODIFY | pass + persist new values on the all-chapter restitch loop | provisional |
| `swanki/audio/surgical.py` | REFERENCE | must stay safe (L93 asserts postprocessor present, not shape); do NOT add knobs | reference |
| `swanki/audio/comment_edit.py` | REFERENCE | reads manifest postprocessor + restitches; must stay safe | reference |
| `swanki/audio/card.py` | REFERENCE | uses `combine_audio` (no bookends); untouched | reference |
| `swanki/models/cards.py` | REFERENCE | `LectureTranscriptFeedback.meets_length_target` word-count guardrail for prompt change | reference |
| `tests/test_audio_common.py` | MODIFY | asymmetric bookend test + keyless-manifest restitch regression | provisional |
| `tests/test_audio_timeline.py` | MODIFY | check/adjust any `bookend_pause_ms` timeline assertions | provisional |
| `notes/swanki.audio._common.md` | MODIFY | dated rationale section | provisional |
| `notes/swanki.audio.hamming-comments-runbook.2026.05.29.md` | REFERENCE | post-merge runbook extends here | reference |

## Key Design Decisions

1. **Three new knobs, retire the old single `bookend_pause_ms`.**
   `bookend_start_pause_ms` (after start bookend), `bookend_end_pause_ms` (before end
   bookend), `bookend_trailing_pause_ms` (NEW — after end bookend). Why: the request
   is asymmetric pacing; one symmetric knob cannot express it, and trailing silence
   has no current site at all. The old `bookend_pause_ms` parameter is removed from
   the public signatures of `combine_audio_with_section_pauses` and
   `_accumulate_timeline` (it has no external persisted state to honor — see #2).

2. **Resolution precedence: `override param > manifest postprocessor key > global
   default`, via `.get(key, default)` everywhere.** Old manifests have NO bookend key
   (it was never persisted — confirmed: lecture.py manifest postprocessor block omits
   any bookend key), so they resolve to the NEW global defaults (300/2000/1500). NO
   back-compat mapping of the old single `bookend_pause_ms` is needed because nothing
   was ever stored to honor. Rejected: a legacy `bookend_pause_ms -> start/end`
   mapping branch — dead code, since no manifest carries that key.

3. **`restitch_from_chunks` gains 3 new override params AND persists them into the
   manifest postprocessor block.** When an override is provided, write it into
   `manifest["postprocessor"]` as part of the restitch (and write the manifest back to
   disk). Why decisive: later `edit_chunk` / surgical / comment_edit re-stitches read
   the manifest, so the new pauses MUST live in the manifest or precise per-chunk fixes
   silently revert to defaults. Rejected: override-only (manifest keeps stale/absent
   values → precise fixes revert); rejected: separate rewrite-then-plain-restitch step
   (clumsier, bypasses restitch's own override path). NOTE: `restitch_from_chunks`
   currently does NOT rewrite the manifest at all (it writes the timeline sidecar), so
   persisting the postprocessor block is a new write — add it.

4. **One global set of 3 knobs in `fish_speech.yaml` postprocessor, applied to
   lecture + reading + summary.** NOT per-audio-type. Why: bookend pause semantics are
   about the bookend mechanism, which is type-agnostic; the fact that comments are
   lecture-specific is irrelevant to where the silence sits. `card.py` uses
   `combine_audio` (no bookends) — do NOT add knobs there.

5. **Prompt change in `book_voice.yaml` ONLY, refining the existing conclusion rule.**
   NOT `default.yaml` — that would silently change every paper unvalidated. Refine the
   existing rule (~L341, "CONCLUDE WITH SUMMARY: 3-5 takeaways") into a stronger
   single-concept takeaway after worked examples. Do NOT add a new section or new word
   budget; stay within the existing 3-5 takeaway count and the 50%+10% word budget.
   Word it as a quality/emphasis directive ("the closing takeaways should crystallize
   the single most important conceptual idea the worked examples illustrate") and
   STATE the concept itself — NEVER label it "deep" or "important" (that trips rule 11
   NO META-COMMENTARY ABOUT DEPTH, ~L349, and oscillates the critic loop). Rejected:
   changing `reading.py` — its system prompt is HARDCODED (not YAML) and reading is not
   the target; leave it.

6. **PR vs runbook split.** PR = code + config + prompt + tests. The re-stitch-all
   EXECUTION (all 10 Hamming chapters) + ABS republish + clear/re-mark bookmarks =
   POST-MERGE RUNBOOK. Why: matches prior plans; the heavy artifact regeneration and
   the human ABS step do not belong in a reviewable diff.

## Approach

**Core (`_common.py`).** In `_accumulate_timeline`, replace the single
`bookend_pause_ms` parameter with `bookend_start_pause_ms` and `bookend_end_pause_ms`,
and add `bookend_trailing_pause_ms`. The start-bookend block (L1280–1286) inserts
`bookend_start_pause_ms` of silence — already gated on `bookend_start` existing. The
end-bookend block (L1344–1351) inserts `bookend_end_pause_ms` BEFORE the end bookend,
then after appending the end bookend and computing its Span, appends
`bookend_trailing_pause_ms` of silence and re-reads `len(combined)` into
`timeline.total_duration_ms`. The trailing-pause site is gated on `bookend_end` being
present (no end bookend → no trailing silence). Mirror the same parameter rename in
`combine_audio_with_section_pauses`, which just forwards to `_accumulate_timeline`,
and update its docstring (the current `bookend_pause_ms` doc line at L1386).

Note `total_duration_ms` is set AFTER this block (L1353), so trailing silence is
naturally included — confirm it stays after the trailing append.

**Restitch + persist (`restitch_from_chunks`).** Replace the `bookend_pause_ms`
override param with three: `bookend_start_pause_ms`, `bookend_end_pause_ms`,
`bookend_trailing_pause_ms` (all `int | None = None`). Resolve each as
`override if not None else int(post.get(key, <default>))` with defaults 300/2000/1500.
Forward the three resolved values into `combine_audio_with_section_pauses`. Then, when
ANY of the three overrides was provided, write the resolved values back into
`inp.manifest["postprocessor"]` and persist via
`manifest_path.write_text(json.dumps(inp.manifest, indent=2))` BEFORE (or alongside)
the existing sidecar write. This is the new persistence behavior from decision #3.
Keep `_manifest_combine_inputs` returning `post = manifest.get("postprocessor") or {}`
so a keyless manifest yields `{}` and every `.get` falls through to the new defaults.

**Call sites (lecture / reading / summary).** Each already reads
`post_cfg = tts_kwargs.get("postprocessor")` (or equivalent) and forwards a cluster of
keys to `combine_audio_with_section_pauses`. Add three reads —
`bookend_start_pause_ms = int(post_cfg.get("bookend_start_pause_ms", 300))` etc. —
forward them to the combine call, and add the same three keys to the manifest
`postprocessor` dict written via `write_chunk_manifest` (lecture ~L1019, reading
~L470, summary ~L293). This persists the bookend pauses on FIRST render so any later
surgical/comment_edit restitch inherits them with no override needed.

**Config (`fish_speech.yaml`).** Add to the `postprocessor` block:
`bookend_start_pause_ms: 300`, `bookend_end_pause_ms: 2000`,
`bookend_trailing_pause_ms: 1500`. `fish_speech_hamming.yaml` does not override
`postprocessor`, so it inherits these — no edit there.

**Prompt (`book_voice.yaml`).** Reword the existing conclusion rule per decision #5.
Keep the 3-5 count and the 50%+10% budget; make it an emphasis directive that names
the concept and forbids depth meta-commentary implicitly by construction.

**Driver (`regen_hamming_bookends_ch1_10.py`).** The existing loop regenerates bookend
mp3s then calls `restitch_from_chunks(man_path, final)` with no overrides. Update the
call to pass the three new values explicitly (300/2000/1500) so the runbook re-stitch
persists them into each chapter manifest. Re-stitch is pure pydub, NO Fish; bookend
TEXT is unchanged so `generate_bookend_audio` is not re-invoked for the pause change.

**Notes.** Append a dated rationale section to `notes/swanki.audio._common.md`
covering the knob split, the persist-on-override behavior, and the precedence rule.

## Gotchas

1. **Old manifests lack bookend keys** — `restitch` / `surgical` / `comment_edit` must
   not crash. Sidestep: `.get(key, default)` everywhere (decision #2); `post` already
   defaults to `{}` in `_manifest_combine_inputs`. Add a regression test: restitch a
   keyless OLD manifest → no crash, resolves to the new defaults.

2. Plain restitch of an old manifest yielding the new defaults is intended; the runbook
   passes overrides that PERSIST (decision #3) so later precise fixes read the same values.

3. **`chunk_timeline.json` + ABS bookmark drift.** Re-stitching shifts every offset
   and the bookend Spans. Do NOT migrate timestamps. Clear + re-mark bookmarks
   (`scripts/abs_clear_bookmarks.py`). The ch1-9 per-chunk comments are content-matched
   and captured in the runbook note, so offset drift does not lose them.

4. Keep the trailing append INSIDE the `if bookend_end` block (both pause sites gated on
   bookend existence — see Approach). One global set, all 3 types (decision #4); `card.py` untouched.

5. **Prompt budget + rule 11.** Stay within the 50%+10% word budget
   (`LectureTranscriptFeedback.meets_length_target`: `word_count <= target*1.1` in
   `models/cards.py`) and the 3-5 takeaway count; book_voice only; refine the existing
   rule, no new section; state the concept, never its importance. Verifying a sample
   chapter regen stays within budget / critic `done=True` is a RUNBOOK check (needs an
   LLM call) — NOT a PR unit test.

6. **Commit-before-sync for the republish** (runbook step) — `sync_to_zotero` embeds
   the git HEAD short hash as provenance; commit the post-rebase HEAD first.

7. **No open GH issues touch this; one unrelated worktree active.** Keep new keys
   additive so concurrent worktree restitches stay safe.

## Verification

- `~/opt/miniconda3/envs/swanki/bin/Swanki python -m pytest tests/test_audio_common.py
  tests/test_audio_timeline.py -q` passes.
- New asymmetric test: build sections with both bookends, call
  `combine_audio_with_section_pauses` with start=300/end=2000/trailing=1500, assert via
  `ChunkTimeline` Spans that (a) `bookend_start.end_ms` + 300 == first section start,
  (b) gap between last section end and `bookend_end.offset_ms` == 2000, and (c)
  `total_duration_ms - bookend_end.end_ms` == 1500. Mirror the existing
  `test_combine_audio_with_section_pauses_bookends` (~L265).
- New keyless-manifest regression: write a manifest whose `postprocessor` block has NO
  bookend keys (or is absent), call `restitch_from_chunks` with no overrides → no crash;
  resolved pauses equal 300/2000/1500.
- New persist test: call `restitch_from_chunks` WITH the three overrides, reload the
  manifest JSON, assert the three keys are now present with the override values.
- `ruff check` + `mypy` clean on the changed Python files (signature change is
  source-compatible: the only caller passing `bookend_pause_ms` was `restitch_from_chunks`
  itself; grep to confirm no other caller passes the retired kwarg).
- Manual: regenerate one short lecture with `models=fish_speech`, confirm front bookend
  plays almost immediately, a distinct break precedes the end bookend, and silence
  follows it before the file ends. (Runbook-level, optional in PR.)

## Open Questions

1. **Default values 300/2000/1500** are starting points, tunable after listening (the
   existing `section_pause_ms` is already 5000, a different regime — bookend pauses are
   deliberately shorter). Adjust in `fish_speech.yaml` post-merge if the ABS listen
   suggests otherwise.
2. **No manifest schema-version field exists.** New keys are additive + defaulted, so
   no version bump. Note for future readers: manifests written before 2026.05.30 lack
   the three bookend keys and resolve to the new global defaults.
