---
id: rz2nv62o4zk4epm59yztqxm
title: '29'
desc: ''
updated: 1780072034493
created: 1780072034493
---

## Context

Hamming-chapter audio (citation key `hammingArtDoingScience2020`) is built around coding theory: error-correcting codes, parity, and codewords expressed as bare binary strings ("11", "0110", "1011010"). The TTS path has no rule for isolated binary tokens, so Fish/ElevenLabs read them as cardinal numbers: "11" becomes "eleven", "0110" becomes "one hundred ten", "1011010" becomes a seven-digit number. This destroys the per-digit codeword semantics that the lecture is explaining — a listener cannot follow a Hamming-distance argument when the codewords are read as base-ten integers. Annotation review of the existing Hamming audio found 8 of 21 lecture chunks and 18 of 43 reading chunks in chapter 10 (the coding-theory chapter) corrupted this way; chapters 1-9 have only scattered surgical issues.

The fix is a deterministic pre-TTS scrubber that rewrites isolated binary tokens into hyphenated digit-words ("110" -> "one-one-zero"), which every TTS engine reads cleanly digit-by-digit. It must be pipeline-wide and default-on so no existing or future paper silently mis-reads bit strings, with a length cap (32) so genuinely long numeric IDs are left alone.

Two deliverables:

1. **Verbalizer code** (executed in the worktree): new pure-text function `verbalize_bit_strings` in `swanki/audio/_common.py`, wired into the four audio-module scrubber chains AFTER acronym expansion and BEFORE pronunciation overrides, a config mirror in `fish_speech.yaml`, prompt addenda in `default.yaml` (lecture) and `reading.py` (reading), and tests in `tests/test_audio_common.py`.
2. **Hamming annotation runbook** (executed from `main` AFTER the verbalizer merges): a documented plan of action — NOT code in this worktree — to extract/triage orange annotations for chapters 1-10, apply surgical edits to ch1-9 via the `audio-fix-from-annotations` skill, and do a full audio regen of ch10 (which depends on the verbalizer being present) with the ABS bookmark clear-and-remark step.

## Relevant Files

| Path | Action | Purpose | Stance |
| --- | --- | --- | --- |
| `swanki/audio/_common.py` | MODIFY | Home of `verbalize_bit_strings` (~after L429, next to `apply_pronunciation_overrides`) | provisional — active scrubber module |
| `swanki/audio/lecture.py` | MODIFY | Insert verbalizer in scrubber chain at ~L855 (after acronym, before pronunciations) | in-flux — scrubber chain live since 2026.05.14 |
| `swanki/audio/reading.py` | MODIFY | Insert verbalizer at ~L338; add reading prompt addendum in hardcoded system prompt (~L243) | provisional — mirrors lecture + holds hardcoded reading prompt |
| `swanki/audio/summary.py` | MODIFY | Insert verbalizer at ~L156 (after acronym, before pronunciations) | provisional — mirrors lecture |
| `swanki/audio/card.py` | MODIFY | Insert verbalizer in `_preprocess_for_tts` at ~L63 (after acronym, before pronunciations) | stable — `_preprocess_for_tts` feeds 5 TTS sites |
| `swanki/conf/models/fish_speech.yaml` | MODIFY | Add `verbalize_bit_strings: true` + `bit_strings_max_len: 32` under `preprocessor:` (~L31) | stable — has `preprocessor:` block |
| `swanki/conf/prompts/default.yaml` | MODIFY | Lecture prompt addendum inside `lecture_system` (block ends ~L384) | stable |
| `tests/test_audio_common.py` | MODIFY | Verbalizer unit tests, mirroring acronym/pronunciation patterns | stable |
| `notes/swanki.audio._common.md` | MODIFY | Dated rationale section for the new function | provisional — dendron decision log |
| `.claude/skills/audio-fix-from-annotations/SKILL.md` | REFERENCE | Runbook tooling for ch1-9 surgical edits | reference only |
| `.claude/skills/zotero-annotations/SKILL.md` | REFERENCE | Extract orange annotations by citation key + color | reference only |
| `scripts/abs_clear_bookmarks.py` | REFERENCE | Clear ABS bookmarks before ch10 full regen | reference only |

## Key Design Decisions

1. **Function lives in `_common.py` with the same shape as the existing scrubbers.** `verbalize_bit_strings(text, max_len=32) -> str` sits next to `expand_acronyms_for_tts` (~L377) and `apply_pronunciation_overrides` (~L410): a module-level compiled regex, a pure-text body, fail-fast (no try/except), a Google-style docstring. *Why:* consistency with the existing scrubber API makes the four wiring sites uniform and the tests trivially parallel to the acronym tests.

2. **Placement: AFTER acronym expansion, BEFORE pronunciation overrides** (follows the user's request). *Why:* the passes are functionally orthogonal — `expand_acronyms_for_tts` only matches `[A-Z]{2,6}` uppercase letter runs and never touches digits, so the verbalizer cannot collide with it in either order. Placing the verbalizer before pronunciations preserves the documented "overrides win last" invariant (`apply_pronunciation_overrides` docstring, L415-417): a per-paper override is still the final word on any token. **Rejected:** placing before acronym expansion — no functional benefit, and it visually breaks the established "acronym then overrides" reading order.

3. **Gated on the TOGGLE ONLY, provider-agnostic — NOT gated on `is_fish_for_prep`.** Read `prep_cfg.get("verbalize_bit_strings", True)` and `prep_cfg.get("bit_strings_max_len", 32)`. *Why:* binary-token-as-cardinal is wrong on every engine, not just Fish — the precedent is `apply_pronunciation_overrides`, which is already provider-agnostic. The default of `True` (not `False`) is what makes "pipeline-wide default-on" truthful: the ElevenLabs `default.yaml` has NO `preprocessor:` block, so `prep_cfg` is `{}` there and only a `True` default fires the pass. The `fish_speech.yaml` keys are an explicit, documentable mirror of the defaults, not the activation gate. **Rejected:** fish-only gating (`is_fish and ...`) — would leave ElevenLabs papers mis-reading bit strings and contradicts "pipeline-wide".

4. **Regex: lookaround-bounded runs of `[01]` of length 2..max_len, mapped to hyphen-joined digit-words.** Pattern `(?<![A-Za-z0-9_.,/:-])[01]{2,N}(?![A-Za-z0-9_.,/:-])` with `N = max_len`. *Why each piece:* the min length 2 leaves bare single "0"/"1" untouched (they read fine as words and appear constantly in prose); the exclusion sets on both sides (letters, digits, `_ . , / : -`) protect decimals (`1.5`, `0.01`), thousands-commas (`1,000`), years and integers containing a non-binary digit (`2020` contains "2", never matches), identifiers (`v01`, `chunk0`, `H110N`), paths/times (`a/01`, `10:01`); the hyphen in the exclusion set is what makes the substitution **idempotent** — the emitted "one-one-zero" cannot re-match because every digit-word now abuts a hyphen. Bare "00"/"11"/"01" (length >= 2) DO expand by design — that is exactly the codeword case. **Rejected:** matching any digit run (would mangle every number); word-boundary `\b` only (would still fire inside `1.5` and re-match its own output).

5. **`SECTION_BREAK_MARKER` needs NO masking.** The acronym pass masks `---SECTION_BREAK---` (L401-407) because "BREAK" is a 5-letter run it would letter-spell. The verbalizer only matches `[01]` runs; the marker is uppercase letters + hyphens with no binary run of length >= 2, so the lookaround exclusion already protects it. *Why this matters:* replicating the mask/restore dance here would be dead code — explicitly omit it.

6. **Prompt addenda are belt-and-suspenders, added as generic TTS guidance.** The deterministic verbalizer is the real guarantee; the prompt nudge reduces the chance the LLM emits a verbalize-unfriendly form (e.g. spacing out digits oddly) upstream. The lecture system prompt lives in `default.yaml` (`lecture_system`, L230-384) — addendum goes there. The reading system prompt is HARDCODED in `reading.py` (~L201-249), NOT in YAML — addendum goes into that string (~after L243). Summary and card transcripts get no prompt addendum (the verbalizer covers them; their prompts are elsewhere and the LLM rarely emits bare bit strings into them). *See Open Questions* re: the request's "reading addendum in default.yaml" wording.

## Approach

### Part A — Verbalizer code (worktree implementation)

**The function.** Add to `swanki/audio/_common.py` after `apply_pronunciation_overrides` (~L429). Module-level constants then the function:

```python
_BIT_WORDS = {"0": "zero", "1": "one"}

def verbalize_bit_strings(text: str, max_len: int = 32) -> str:
    """Rewrite isolated binary tokens as hyphenated digit-words for TTS.
    ...
    "110" -> "one-one-zero" so a TTS engine reads codewords digit-by-digit
    instead of as the cardinal "one hundred ten".
    """
```

The substitution callback maps each matched run `m.group(0)` to `"-".join(_BIT_WORDS[c] for c in run)`. The pattern embeds `max_len`, so it can't be a fixed module constant — compile it inside the function (see Gotcha 3).

Idempotency and safety follow from Decision 4's regex; verify both in tests, do not add runtime guards.

**The four wirings.** Each site already reads `prep_cfg` defensively (`_prep_raw = tts_kwargs.get("preprocessor"); prep_cfg = _prep_raw if isinstance(_prep_raw, dict) else {}`). Insert the verbalizer step immediately after the acronym block and before the `pronunciations` block, in all four:

- `lecture.py` ~L852-853 (between `expand_acronyms_for_tts` and `pronunciations = ...`)
- `reading.py` ~L338-339
- `summary.py` ~L156-157
- `card.py` `_preprocess_for_tts` ~L63-64

The inserted block in each (operating on the local var — `cleaned` in lecture/reading/summary, `out` in card):

```python
if prep_cfg.get("verbalize_bit_strings", True):
    cleaned = verbalize_bit_strings(
        cleaned, max_len=int(prep_cfg.get("bit_strings_max_len", 32))
    )
```

Note: NOT gated on `is_fish_for_prep` (Decision 3). Add `verbalize_bit_strings` to each module's import from `._common` (the import lists already pull `expand_acronyms_for_tts`, `apply_pronunciation_overrides`, etc.). Update the order-rationale comment at each site to name the new step ("acronym -> verbalize bit strings -> pronunciation overrides -> ...").

**Config mirror.** In `swanki/conf/models/fish_speech.yaml`, under `preprocessor:` (after `acronym_allowlist`, ~L31), add with explanatory comments:

```yaml
      # Rewrite isolated binary tokens ("110") as digit-words ("one-one-zero")
      # so TTS reads codewords digit-by-digit, not as cardinals ("one hundred
      # ten"). Provider-agnostic; default-on pipeline-wide. Cap skips long IDs.
      verbalize_bit_strings: true
      bit_strings_max_len: 32
```

These are an explicit mirror of the in-code defaults, NOT the activation gate (Decision 3).

**Prompt addenda.** In `default.yaml` `lecture_system` block, add a short rule (e.g. as a new numbered item alongside the NO LATEX / NO CITATIONS rules) instructing: when reading binary codewords or bit strings, read each digit separately ("one, one, zero"), never as a single number. In `reading.py`'s hardcoded `system_prompt` string (~after rule 8, L243), add one sentence with the same instruction. Keep both generic — beneficial for any document, not Hamming-specific.

**Tests** in `tests/test_audio_common.py`, mirroring the `expand_acronyms_for_tts` test block. Import `verbalize_bit_strings`. Cover: basic expansion ("110" -> "one-one-zero", "11" -> "one-one", "0110" -> "zero-one-one-zero"); min-length 2 (bare "0"/"1" untouched); idempotency (running twice == running once); decimals/commas/years protected ("1.5", "0.01", "1,000", "2020", "v01", "chunk0" unchanged); `max_len` cap (a 33-char binary run with default cap left alone, expanded when within cap); mixed sentence with codewords and prose; `SECTION_BREAK_MARKER` survives untouched. Use plain `assert`, no fixtures needed.

**Notes.** Append a dated section to `notes/swanki.audio._common.md` recording the function, the regex rationale, and the placement/gating decisions (this is the codebase's decision log per CLAUDE.md).

### Part B — Hamming comment runbook (post-merge, from `main`)

Documented plan of action to execute AFTER the verbalizer PR merges; the worktree PR ships ONLY Part A. The real comments are **13 ABS Lecture bookmarks** (`citation_key = hammingArtDoingScience2020`, item `3d4a9ce9-...`), created 2026-05-24 to 05-26 against the 2026-05-19 audio currently on ABS — NOT Zotero orange annotations. (Round 1: 45 bookmarks Apr 27 - May 20 were addressed by the 05-19 regen and archived in `notes/swanki.audio.hamming-bookmarks-archive.2026.05.21.md`; these 13 are Round 2, all unaddressed.) Fetch them with `scripts/abs_bookmarks.py` (the `note` field is the comment; `time` lags the issue by minutes, so map to chapter via the lecture-concat boundaries and content-match the chunk).

**Decision: ch10 = full regen; everything else = surgical.** The ch10 "100"-as-cardinal spam is pervasive (verbalizer fixes it wholesale) AND the ch10 notes ask for structural/conceptual changes a transcript regen handles — chunk surgery can't. The other chapters' comments are localized.

1. **Land Part A first.** Merge the verbalizer PR. Ch10 regen depends on the verbalizer being active or it reproduces the bug.

2. **Chapter 10 — full audio regen (lecture + reading + summary + cards)** against `main`, gilahyper defaults (`audio=all anki=default models=fish_speech`, `confirm_before_generation=false`). This regen carries THREE coupled fixes, not just the verbalizer:
   - **Codewords** (118.7m "111 repeated", 125.2m + 126.8m "100 spamming over 100 times"): the verbalizer renders `100`->"one-zero-zero", `111`->"one-one-one".
   - **"zero" -> "Jairo" Fish mispronunciation** (120.0m): the verbalizer EMITS many "zero" tokens, so this quirk is amplified, not fixed, by Part A. Add a per-paper pronunciation override (phonetic respelling of "zero") under `preprocessor.pronunciations` in `fish_speech_hamming.yaml` BEFORE regenerating. This is the one Part-A-adjacent code change Part B introduces.
   - **Conceptual strength / prosody** (128.0m "examples confusing, want concept points stronger", 127.4m question up-tone on "exact symbols I utter"): regenerate the ch10 lecture transcript and lean on the critic/refine pass to land a stronger conceptual takeaway after each worked example.

   Full regen produces new chunk timings, so ABS bookmarks do NOT auto-migrate: run `scripts/abs_clear_bookmarks.py` for the ch10 item, then re-mark by hand after the new audio lands. Do NOT build a timestamp-migration tool.

3. **All other chapters — surgical edits via `audio-fix-from-annotations`** (maps a bookmark to its exact chunk via the chunk_timeline, re-TTS's only that chunk, restitches, republishes after one review gate; does NOT touch ABS bookmarks). One chapter at a time, review, proceed:
   - ch3 (29.1m) "light as a human dimension" — surgical transcript edit + re-TTS of that chunk.
   - ch5 (62.7m) Jack Kane anecdotes split/disorganized — surgical transcript edit (or accept if it mirrors the source).
   - ch9 (104.0m) "dimensional space" jammed together — surgical re-TTS (spacing).
   - ch9 (112.3m) theory-vs-practice example needs more depth — surgical transcript edit + re-TTS.
   - **Bookend pause/gap cluster** (53.6m larger pause after "this concludes the lecture"; 65.6m ~2s gap on bookend back-end for the autoplay break; 75.9m small gap before the bookend): these are NOT per-chunk re-TTS — they are a bookend/stitch pause-config change that applies to ALL lectures. Adjust the bookend trailing/leading pause in the postprocessor/stitch config and re-stitch the affected chapter boundaries (no re-TTS). Track as its own small task, not a per-chapter surgical edit.

4. **Verify** by spot-listening the ch10 codeword chunks (confirm digit-by-digit + no "Jairo") and each surgically-edited chunk. Tag the Zotero parent item with the fox emoji on successful re-upload.

Record this runbook in a dated dendron note (e.g. `notes/swanki.audio.hamming-comments-runbook.2026.05.29.md`) so it is executable from `main` independently of the worktree.

## Gotchas

1. **`humanize_latex` runs before the preprocessor pipeline** (cards: after humanize_latex; lecture/reading: after transcript generation). Math already expanded to words is plain prose by the time the verbalizer sees it, and the regex won't re-touch it — the idempotency boundary protects it. *Sidestep:* no special handling; just confirm a test with a math-expanded sentence is unchanged.

2. **`default.yaml` (ElevenLabs) has no `preprocessor:` block.** If the verbalizer defaulted to `False` it would never fire for ElevenLabs. *Sidestep:* default `True` in every `.get("verbalize_bit_strings", True)` call (Decision 3) — this is the entire reason the default is `True`, not a stylistic choice.

3. **Per-call `re.compile` with a variable `max_len`.** Because the pattern embeds `max_len`, you cannot compile a single module constant unless you fix `max_len`. *Sidestep:* compile inside the function (the `re` module caches recent patterns and these are tiny) or cache by `max_len` in a dict — do NOT hardcode 32 into a module constant, since callers may override the cap via config.

4. **Idempotency depends on the hyphen being in the lookaround exclusion set.** Drop the hyphen and "one-one-zero" re-matches the trailing "...zero" boundary oddly and a second pass corrupts output. *Sidestep:* keep `-` in BOTH lookbehind and lookahead exclusion sets; assert idempotency in tests.

5. **Default-on flips behavior for ALL existing callers/papers.** Every already-generated paper that re-runs audio will now verbalize bit strings. This is intended ("pipeline-wide default-on") but means any paper containing legitimate bare binary-looking tokens of length 2-31 (rare: e.g. a deliberately-written "10" meaning the number ten and NOT a codeword) will read as "one-zero". *Sidestep:* the cap and the digit-must-be-binary constraint already minimize this; if a specific paper needs it off, set `verbalize_bit_strings: false` in its `fish_speech_<paper>.yaml`. Note this in the PR description.

6. **Comment drift at the four wiring sites.** Each site has a multi-line order-rationale comment naming the pass sequence. *Sidestep:* update all four comments to include the verbalize step, or the next reader will think the chain skips it.

## Verification

Run from the worktree with the conda env (`~/miniconda3/envs/swanki`):

1. **Unit tests:** `pytest tests/test_audio_common.py -q` — all green, including the new verbalizer cases.
2. **Lint:** `ruff check` on the five changed `.py` files (`_common.py`, `lecture.py`, `reading.py`, `summary.py`, `card.py`) — clean.
3. **Types:** `mypy` on the same five files — clean (the function is `str -> str` with an `int` kwarg; no new typing surface).
4. **Import check:** `python -c "from swanki.audio._common import verbalize_bit_strings; print(verbalize_bit_strings('the codeword 1011010 has parity 11'))"` — confirm output reads `one-zero-one-one-zero-one-zero` and `one-one`.
5. **Dry-run on the real transcript:** locate the ch10 lecture cleaned transcript (`*_transcript_cleaned_markdown.md` under the Hamming ch10 output dir in `SWANKI_DATA`), pipe it through `verbalize_bit_strings`, and eyeball a diff (`difflib`/`git diff --no-index`): every changed line should be a bit-string -> digit-words rewrite, with NO decimals, years, or identifiers touched. This is the load-bearing real-data check before relying on it for the ch10 regen.
6. **Config sanity:** confirm Hydra still composes with the new `fish_speech.yaml` keys — a quick `swanki ... --cfg job` (or the existing config-load test) shows `verbalize_bit_strings: true` and `bit_strings_max_len: 32` present and the rest of the tree intact.

## Open Questions

1. **Reading prompt location deviation.** The request says "reading addendum in default.yaml", but the reading system prompt is HARDCODED in `reading.py` (~L201-249), not in any YAML file (`default.yaml` has only `lecture_system`, no `reading_system`). The plan resolves this by editing the hardcoded string in `reading.py`. Flagging so the user is aware the reading addendum landed in `reading.py`, not `default.yaml` — the lecture addendum did go to `default.yaml` as requested.
