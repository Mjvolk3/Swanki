---
id: zlhrip3v2472us8my9haoor
title: '02'
desc: ''
updated: 1780429003970
created: 1780429003970
---

## Problem

Fish reads "World War II" as "one one" / "I-I". Confirmed on Hamming ch1 + ch3 lecture cleaned markdown ("World War **I-I**").

## Root cause (scouts corrected the initial guess)

NOT the bit-string verbalizer (`verbalize_bit_strings`, PR #18) — that matches `[01]{2,32}` DIGITS only, so Hamming codewords are safe and untouched. The culprit is the **acronym expander** `expand_acronyms_for_tts` (`swanki/audio/_common.py:419-464`), regex `_STANDALONE_ACRONYM_RE = (?<![A-Za-z])([A-Z]{2,6})(?![A-Za-z])`. It letter-spells any 2-6 uppercase run: `MIT`->`M-I-T` (intended) but also `II`->`I-I`, `III`->`I-I-I` (bug). Fish-only, runs before `verbalize_bit_strings`. Single-letter `I` is already safe (floor is 2). A `_ROMAN_TO_WORD` map already exists in `swanki/utils/formatting.py` (used by `humanize_chapter_slug_spoken` for bookend slugs only, not body prose).

## Fix (minimal, no-regression)

In `expand_acronyms_for_tts`, before letter-spelling a matched token, map it to its cardinal word IF it is an UNAMBIGUOUS uppercase Roman numeral. Add a module-level constant in `_common.py`:

```python
# Roman numerals (uppercase, >=2 letters) the acronym expander would otherwise
# letter-spell ("World War II" -> "I-I" -> Fish "one one"). Map the UNAMBIGUOUS
# ones to a cardinal word. Excludes IV (intravenous) and VI (the vi editor),
# which collide with real initialisms and so keep the default letter-spelling
# (NO regression). Single-letter I/V/X never reach the expander (floor is 2).
_ROMAN_NUMERAL_WORDS = {
    "II": "two", "III": "three", "VII": "seven", "VIII": "eight", "IX": "nine",
    "XI": "eleven", "XII": "twelve", "XIII": "thirteen", "XIV": "fourteen",
    "XV": "fifteen", "XVI": "sixteen", "XVII": "seventeen", "XVIII": "eighteen",
    "XIX": "nineteen", "XX": "twenty",
}
```

`_sub` becomes:
```python
def _sub(m):
    tok = m.group(1)
    if tok in skip:
        return tok
    if tok in _ROMAN_NUMERAL_WORDS:
        return _ROMAN_NUMERAL_WORDS[tok]
    return "-".join(tok)
```

Why this set / these exclusions:
- Letters are C/D/M-free, so real initialisms like `MD`, `CV`, `DC`, `MC`, `CI`, `MM` are NOT in the map and keep letter-spelling (correct). The only I/V/X collisions are `IV` (intravenous) and `VI` (vi editor) — deliberately excluded, so they behave EXACTLY as today (no regression).
- Everything mapped (`II, III, VII, VIII, IX, XI..XX`) has no common English initialism, so converting to a word is safe and catches "World War II/III", "Part VII", "Henry VIII", "Chapter IX", "Section XV".
- Output is lowercase ("two"); TTS reads it identically to "Two".

## Tests — `tests/test_audio_common.py` (near the existing `test_expand_acronyms_*`)

- `expand_acronyms_for_tts("World War II")` -> `"World War two"`; `"World War III"` -> `"World War three"`.
- `"Part VII"` -> `"Part seven"`; `"Henry VIII"` -> `"Henry eight"`; `"Chapter IX"` -> `"Chapter nine"`.
- Acronyms unaffected: `"the SAR system"` -> `"the S-A-R system"`; `"MIT"` -> `"M-I-T"`; allowlist `{"USA"}` still skips `USA`.
- No-regression for ambiguous: `"the IV bag"` -> `"the I-V bag"`; `"VI"` -> `"V-I"`.
- Initialisms with C/D/M unaffected: `"MD"` -> `"M-D"`, `"CV"` -> `"C-V"`.
- Codewords still verbalize (separate rule, sanity): `verbalize_bit_strings("the codeword 111")` -> `"the codeword one-one-one"`; `expand_acronyms_for_tts` leaves digits alone.
- Full chain (fish cfg): `preprocess_for_tts("World War II ...", fish_tts_kwargs)` contains `"World War two"`, not `"I-I"`.

## Module note

Append `## 2026.06.02 - Roman-numeral guard in expand_acronyms_for_tts` to `notes/swanki.audio._common.md`: the "World War II"->"I-I" incident, that the acronym expander (not the bit-string verbalizer) was the cause, the unambiguous-roman map with IV/VI excluded (no regression), and that single-letter I/V/X never reach the expander.

## Scope

In: `_ROMAN_NUMERAL_WORDS` const + the `_sub` change in `expand_acronyms_for_tts` + tests + module note.
Out: provider-agnostic roman handling (the bug is the Fish acronym path), context-gating, monarch names beyond the map, `IV`/`VI` disambiguation, touching `verbalize_bit_strings` or `humanize_chapter_slug_spoken`. The ch1/ch3 lecture audio was already hand-patched today (edit_chunk -> "World War Two"); this stops recurrence pipeline-wide.
