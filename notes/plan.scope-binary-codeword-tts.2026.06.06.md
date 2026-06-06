---
id: ed7rb0xje9hn0j0vkio63nk
title: '06'
desc: ''
updated: 1780787789682
created: 1780787789682
---

## Context

`verbalize_bit_strings()` (`swanki/audio/_common.py:680-719`) rewrites any run of
`[01]{2,32}` into hyphenated digit-words ("110" -> "one-one-zero") so coding-theory
codewords are read digit-by-digit instead of as cardinals ("one hundred ten"). It runs
as an unbounded global `re.sub` and is **default-ON** at four call sites
(`prep_cfg.get("verbalize_bit_strings", True)`). Introduced by `#18` (commit `987cc93`,
2026-05-29, `plan.bit-string-verbalizer-hamming-annotations.2026.05.29`).

The defect is structural: a decimal made only of 0/1 digits — `10`, `100`, `1000`, `11`
— is **indistinguishable** from a binary codeword, so ordinary numbers get mangled
everywhere the scrubber runs. Kuchel ch01 biochemistry garbled "10 and 100" and spammed
"100"; non-coding Hamming chapters hit the same. Surfaced again via ABS bookmarks — the
user's reported **SECOND recurrence**. Genuine codewords only matter in Hamming CH10
(`coding-theory-i`).

Compounding the data problem, the prompt rules themselves are self-contradictory. The
lecture rule (`swanki/conf/prompts/default.yaml:386`, rule 17 "BINARY CODEWORDS AND BIT
STRINGS") and the hardcoded reading rule (`swanki/audio/reading.py:248`, rule 10) both
use the example list `(e.g. 0, 10, 110, 1011)` — listing `10` as a codeword one clause
before "ordinary quantities stay as numerals." The LLM is told `10` is both.

**Decisive evidence for defaulting the scrubber OFF.** A byte-level diff of Hamming
CH10's RAW LLM lecture transcript against the POST-scrubber transcript is **identical in
the codeword region** and contains **zero bare `[01]{2,}` tokens**: the LLM already
emits word-form codewords ("zero", "one-zero", "one-one-zero", "one-one-one") from the
prompt rule alone. The scrubber has **never fired productively** on the one chapter it
exists for. Defaulting it OFF therefore carries zero demonstrated CH10 regression, while
defaulting it ON keeps mangling every 0/1-only decimal in every other source. The fix is
two-pronged: repair the prompt example lists (the actual instruction the LLM follows) at
all four prompt sites, and demote the scrubber to per-paper opt-in.

## Relevant Files

| Path | Action | Purpose | Stance |
| --- | --- | --- | --- |
| `swanki/audio/_common.py` | MODIFY | per-card call site (`:144`) -> default False; function body (`:680`) unchanged | in-flux |
| `swanki/audio/lecture.py` | MODIFY | lecture call site (`:839`) -> default False | in-flux |
| `swanki/audio/reading.py` | MODIFY | reading call site (`:344`) -> default False; hardcoded rule 10 (`:248`) prompt fix | in-flux |
| `swanki/audio/summary.py` | MODIFY | summary call site (`:159`) -> default False; ADD corrected binary rule to system prompt (`~:88`) | in-flux |
| `swanki/conf/prompts/default.yaml` | MODIFY | lecture rule 17 (`:386`) example-list fix + carve-out | n-a |
| `swanki/conf/prompts/book_voice.yaml` | MODIFY | ADD corrected binary rule to `lecture_system` block (`~:225`) — currently has none | undocumented |
| `swanki/conf/models/fish_speech.yaml` | MODIFY | flip documented mirror `verbalize_bit_strings: true` -> `false` (`:39`) + comment | stable |
| `tests/test_audio_common.py` | MODIFY | flip two default-ON preprocess tests; add CH10 opt-in fixture + prompt-example guard | n-a |
| `notes/plan.bit-string-verbalizer-hamming-annotations.2026.05.29.md` | REFERENCE | `#18` origin of the scrubber + prompt rule | stable |

## Key Design Decisions

1. **Fix the prompt example lists at all four prompt sites — not just the data layer.**
   The `(e.g. 0, 10, 110, 1011)` list is the literal instruction the LLM follows; while
   it names `10` as a codeword the model is licensed to verbalize ordinary tens. Trim
   `10` and `100` out of every example list (leaving `e.g. 0, 110, 1011`) and ensure the
   carve-out names them: "ordinary quantities like 10, 100, 1000 stay as numerals."
   Note `default.yaml:386` and `reading.py:248` ALREADY carry a bare carve-out ("...stay
   as numerals") — there the edit is trim-the-example + extend the carve-out to name
   `10/100/1000`; `book_voice.yaml` and `summary.py` have NO rule, so they receive the
   full corrected rule (cleaned example + carve-out).
   - `default.yaml:386` (lecture rule 17, YAML).
   - `book_voice.yaml` `lecture_system` (`~:225`) — ADD the corrected rule (block has
     none today); `book_voice` is a separate 452-line file that does NOT inherit from
     `default.yaml` and is selected via `prompts=book_voice`.
   - `reading.py:248` (rule 10, hardcoded Python string).
   - `summary.py` system prompt (`~:88`) — ADD the corrected rule as a new numbered rule
     (currently has no binary rule at all).
   *Why all four:* the prompt is the productive control (the LLM already self-verbalizes
   correctly when the rule is clean — see CH10 evidence). Fixing data defaults without
   fixing the contradictory examples leaves the door open for the LLM to mangle tens.

2. **Demote the scrubber to per-paper opt-in: flip all four call-site defaults
   `True` -> `False`.** Sites: `_common.py:144`, `lecture.py:839`, `reading.py:344`,
   `summary.py:159`. *Why:* the scrubber cannot disambiguate a 0/1-only decimal from a
   codeword, so any always-on posture is wrong on the common case (ordinary numbers) to
   defend the rare case (dense codewords) that the prompt already handles. CH10 shows the
   scrubber is a no-op where it was meant to fire, so off-by-default loses nothing real.

3. **Keep the config key and the function body unchanged; re-enable per paper.** The
   `verbalize_bit_strings` key stays live so a future dense-codeword paper sets
   `verbalize_bit_strings: true` in `fish_speech_<paper>.yaml` (the established
   per-paper override pattern). `verbalize_bit_strings()` itself is untouched — it works
   identically when explicitly enabled. *Why:* preserve the escape hatch without paying
   the always-on cost; minimal surface area, no behavior drift in the opt-in path.

4. **Rejected: cue-gating the scrubber (only fire near "codeword"/"bit string"/parity
   cues within a window).** *Why rejected:* (a) window-size is brittle — codewords drift
   arbitrarily far from their cue word, so any window both misses real codewords and
   still catches stray tens; (b) it breaks the existing ~12 boundary unit tests, forcing
   churn for no gain; (c) it is **a no-op on CH10 anyway** — the LLM emits word-form
   codewords, so there are no bare `[01]{2,}` tokens for a gated scrubber to act on.
   Gating adds complexity and risk to defend a code path that never fires. Default-off
   wins because it is the minimal change that matches the evidence: prompt does the work,
   scrubber is dormant insurance you switch on deliberately.

5. **Flip the documented mirror in `fish_speech.yaml:39` `true` -> `false`** with a
   comment that the toggle is now opt-in. *Why:* the comment block (`:33-38`) currently
   claims the key "mirrors the in-code defaults" and that modules "default the toggle to
   True." After decision 2 that is a lie; the documented mirror must track the real
   default or it misleads the next maintainer.

## Approach

Execution order — **prompts first, scrubber default second, config mirror third, tests
last** — so each layer is independently correct and the test diff lands against final
behavior.

**1. Prompt example lists (the productive fix).** Edit the four prompt sites per
decision 1. Concretely the example clause changes shape:

```
before:  ... binary codeword or bit string (e.g. 0, 10, 110, 1011), read each digit ...
after:   ... binary codeword or bit string (e.g. 0, 110, 1011), read each digit ...
         ... Lengths, counts, and ordinary quantities like 10, 100, 1000 stay as numerals.
```

For `default.yaml:386` and `reading.py:248` this is an edit-in-place of an existing rule.
For `book_voice.yaml` `lecture_system` and `summary.py` it is a NEW numbered rule (no
binary rule exists there today) carrying the cleaned example + carve-out. `summary.py`
and `reading.py` are hardcoded Python strings — the edits land in `.py`, not YAML.

**2. Scrubber default flip.** At `_common.py:144`, `lecture.py:839`, `reading.py:344`,
`summary.py:159` change `prep_cfg.get("verbalize_bit_strings", True)` to `... False`.
Nothing else at those sites moves; the guarded `verbalize_bit_strings(...)` call inside
each block is unchanged.

**3. Config mirror.** `fish_speech.yaml:39` -> `false` and rewrite the `:33-38` comment
to say the toggle is opt-in (set `true` in a `fish_speech_<paper>.yaml` for dense
codeword sources), not default-on.

**4. Tests** (per decisions in the Verification section's test list). Flip the two
default-ON preprocess assertions to default-OFF, add the re-enable assertion, add a CH10
opt-in regression fixture, and add a prompt-example guard. The ~12 `verbalize_bit_strings`
unit tests stay untouched (function unchanged).

**Out of scope:** the regex/body of `verbalize_bit_strings()`; cue-gating; any chunking
or balanced-chunker work (separate in-flux effort); migrating other prompt rules;
re-rendering audio (that is a manual smoke check, not part of this PR).

## Gotchas

1. **`book_voice.yaml` is not loaded by default** (`config.yaml` `prompts: default`).
   Editing it alone affects nothing unless `prompts=book_voice` is passed — which is
   exactly why `default.yaml` is also fixed. Which prompt a given book used is uncertain,
   so **both** are edited. Sidestep: edit both, do not assume one covers the other.
2. **`summary.py` and `reading.py` rules are hardcoded Python strings, not YAML.** The
   rule edits/additions land in `.py` string literals; grep for the rule text in the
   module, not in `conf/prompts/`.
3. **Active worktree `plan/slurm-native-serverless-fish` touches audio files.** Rebase
   conflicts are likely on `_common.py`/`lecture.py`/`reading.py`. Sidestep: the
   `wt-implement` skill handles rebase-retry; keep this change minimal and localized to
   the bit-string lines so conflicts stay trivial.
4. **`.pre-commit-config.yaml` pytest hook may carry a macOS-hardcoded python path.** On
   gilahyper the hook can fail to find the interpreter. Sidestep: run pytest directly
   with `~/miniconda3/envs/swanki/bin/python` instead of fighting the hook.
5. **Module notes for `_common`/`lecture`/`reading`/`summary` are all "in-flux"** (recent
   2026-06-06 balanced-chunker work). This change touches ONLY the bit-string default and
   the prompt examples — preserve every existing invariant in those notes; append, never
   rewrite.

## Verification

**Tests to write/update** (`tests/test_audio_common.py`):

- `test_preprocess_for_tts_runs_scrubbers` (`~:481`): currently asserts "one-one-zero"
  appears by default. Flip to assert the bit-string scrubber is **OFF** by default
  (`"110"` survives, `"one-one-zero"` absent), PLUS a paired assertion that
  `preprocessor: {verbalize_bit_strings: true}` re-enables it.
- `test_preprocess_for_tts_fish_only_steps_noop_for_elevenlabs` (`~:487`): drop the
  "verbalize is provider-agnostic so it still runs" assertion (now off by default); keep
  the acronym-fish-only check; add the same opt-in re-enable assertion.
- **NEW CH10 opt-in regression fixture:** feed the real CH10 codeword passage with the
  scrubber **explicitly invoked** and assert each codeword still verbalizes. Verify
  inputs against the function: `0, 10, 110, 111` -> `0, one-zero, one-one-zero,
  one-one-one` (bare single `0` stays; `verbalize_bit_strings()` floor is length-2). Use
  the real passage from the Hamming CH10 lecture transcript under `$SWANKI_DATA`. This
  guards the opt-in path against future regex regressions.
- **NEW prompt-example guard:** assert the lecture/reading/summary prompt strings no
  longer list `10` as a codeword example (e.g. the example list no longer contains
  `"10,"`). Pull the strings from the modules / load `default.yaml` via the same config
  the pipeline uses.
- The ~12 existing `verbalize_bit_strings()` unit tests stay UNCHANGED.

**Commands** (gilahyper interpreter, run pytest directly per Gotcha 4):

```bash
~/miniconda3/envs/swanki/bin/python -m pytest tests/test_audio_common.py -q
~/miniconda3/envs/swanki/bin/python -m mypy swanki/audio/_common.py swanki/audio/lecture.py \
  swanki/audio/reading.py swanki/audio/summary.py
~/miniconda3/envs/swanki/bin/python -m ruff check swanki/audio tests/test_audio_common.py
```

**Notes step.** The `/update-notes` (i.e. `/update-src-notes`) step in implementation
appends a dated **2026.06.06** section to `notes/swanki.audio._common.md`,
`notes/swanki.audio.reading.md`, `notes/swanki.audio.summary.md`, and
`notes/swanki.audio.lecture.md`, recording the default flip + prompt-example fix and the
`#18` cross-reference. Confirm these four notes gained the dated section before commit.

**Manual smoke.** Re-render Kuchel ch01 (a non-coding biochemistry source) and confirm
audio reads "one hundred" / "ten" for `100` / `10`, NOT "one-zero-zero" / "one-zero".
Then re-render Hamming CH10 (`coding-theory-i`) and confirm codewords are STILL spelled
digit-by-digit ("one-one-zero") — proving the prompt rule alone carries CH10 and the
scrubber default flip caused no codeword regression.
