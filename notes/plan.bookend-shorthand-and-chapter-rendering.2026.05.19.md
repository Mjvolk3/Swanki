---
id: fjbtbtyzeb2drgfoow0fv1n
title: Bookend Shorthand Dict + "Chapter N" Rendering
desc: ''
updated: 1779230475429
created: 1779230475429
---

## Context

Bookend audio for chapter-form citation keys currently funnels the chapter
number through `chapter_number_spoken`, which renders `"07"` as `"o seven"`
so listeners hear *"Hamming, Art Doing Science, 2020, o seven, artificial
intelligence two"*. The user wants the bookend to read `"Chapter 7"`
instead: the leading zero is a filesystem-sort convenience, not a thing
humans say aloud. The `chapter_number_spoken` helper has four other
consumers locked to the legacy `"o N"` form (its own unit tests assert it)
so we cannot rewrite it in place; the bookend branch must bypass it.

Two adjacent gaps fall out of the same review pass. First, the canonical
shorthand vocabulary used across the codebase (`CH`, `SI`, `S`/`SEC`,
`PART`, `APP`) is implicit -- scattered as inline regex callbacks in
`humanize_card_text_for_tts` -- with no single source of truth. We add a
`SHORTHAND_EXPANSIONS` dict in `swanki/utils/formatting.py` as that
canonical reference; only the `CH -> Chapter` entry is wired in this PR
(into the bookend chapter branch), the rest land as documented expansions
for future callers, especially the inert `_llm_guess_shorthand(token)`
stub we also add. Second, `parse_chapter_key` only matches the legacy
`_<NN>_<slug>` form even though `feedback_book_chapter_slug.md` calls for
accepting `_CH<NN>_<slug>` going forward. Renaming 30 ABS-published mp3s
and their parent dirs is disruptive; extending the regex to accept both
forms with identical output is the cheap win.

Why now: the 30 Hamming ch1-10 bookends already landed on AudiobookShelf
at commit `7a686f7` with the simple frame (lecture / summary / reading x
start / end). Pass-2 re-TTS will swap the `"o seven"` segment for
`"Chapter 7"` in-place; everything else (non-bookend chunk mp3s,
filenames, chunk-timeline structure) stays byte-identical so BookPlayer
just refreshes the affected items. We sequence the regen after the PR
merges so the embedded `_git_short_hash()` in the published zip metadata
points at the canonical merged SHA on `origin/main` rather than a branch
SHA that might shift under a rebase-merge.

## Relevant Files

- `swanki/utils/formatting.py` MODIFY -- add `SHORTHAND_EXPANSIONS` dict
  near `_LABEL_EXPANSION` at :461, extend `_CHAPTER_KEY_PATTERN` at :300
  to accept an optional `CH` prefix, add `_llm_guess_shorthand` stub.
  `parse_chapter_key` body at :305 stays untouched (the regex extension
  drives both forms). `chapter_number_spoken` at :337 and
  `humanize_chapter_slug_spoken` at :404 stay invariant.
- `swanki/audio/_common.py` MODIFY -- `build_bookend_text` chapter branch
  at :1629-1647; replace the `num_spoken = chapter_number_spoken(num_str)`
  line at :1639 with the inline `f"Chapter {int(num_str)}"` rendering.
  Drop the `chapter_number_spoken` import at :1620 only if no other
  call survives in the file (see Gotchas).
- `tests/test_audio_common.py` MODIFY -- `_CH_EXACT` at :620 flips wording;
  the 6 chapter-form bookend assertions at :623-652 update; the two
  roman-numeral cases at :655-676 update; add accept-both equivalence
  tests for `_NN_` vs `_CH<NN>_` for lecture / summary / reading.
- `tests/test_utils_formatting.py` MODIFY -- add `parse_chapter_key` tests
  for `_CH<NN>_<slug>` form, `SHORTHAND_EXPANSIONS` shape tests,
  `_llm_guess_shorthand` returns-`None` test.
- `scripts/regen_hamming_bookends_ch1_10.py` REFERENCE -- no code change;
  re-run post-merge from `main`. Idempotent: re-TTSes bookend mp3s
  in-place (filenames preserved), restitches (non-bookend chunks remain
  sha256-identical), `sync_to_zotero` uploads new versioned zip, then
  `abs_refresh` reflows the AudiobookShelf items.
- `scripts/abs_refresh.sh` REFERENCE -- final ABS sweep; honor the
  `/tmp/abs-refresh.lock` flock to avoid silent contention with the
  hourly cron run.
- `notes/swanki.utils.formatting.md` MODIFY -- append
  `## 2026.05.19 - SHORTHAND_EXPANSIONS + parse_chapter_key accepts _CH<NN>_`
  dated section recording the regex extension, the dict's canonical role,
  and the deliberate scope (`humanize_citation_key` is NOT routed through
  it).
- `notes/swanki.audio._common.md` MODIFY -- append
  `## 2026.05.19 - Bookend "Chapter N" rendering + SHORTHAND_EXPANSIONS`
  dated section explaining why the bookend branch bypasses
  `chapter_number_spoken`.
- `notes/user.mjvolk3.swanki.tasks.weekly.2026.17.md` MODIFY -- flip the
  pending bullet linking this plan note to completed when `wt-implement`
  lands the change; add a one-sentence summary before the link per the
  weekly-notes convention.

## Key Design Decisions

**Bookend chapter number renders as `f"Chapter {int(num_str)}"`, bypassing
`chapter_number_spoken`.** Reason: the legacy `"o N"` form has four
existing unit tests in `test_utils_formatting.py` locking it for other
callers; rewriting the helper would silently change unrelated audio. The
inline `int(num_str)` drops the leading zero (`"07" -> 7`) which is what
Fish Speech reads naturally as `"seven"`. Add a code comment at the
bookend call site spelling out the choice so a future reader does not
funnel it back through the helper.

**`SHORTHAND_EXPANSIONS` is canonical reference + bookend wiring only.**
The dict (`CH -> Chapter`, `SI -> Supplementary Information`, `S` /
`SEC -> Section`, `PART -> Part`, `APP -> Appendix`) lives near
`_LABEL_EXPANSION` so the two label vocabularies sit side by side. The
bookend branch reads the `CH` entry indirectly via the rendered string;
we do NOT route `humanize_citation_key` through it. That function has
8+ callers and the per-card prefix path
(`"MC-CH1-13:"` -> `humanize_card_text_for_tts`'s `_CHAPTER_BARE.sub`)
depends on the `CH` token surviving until the prose expander. The other
dict entries are documented expansions for the `_llm_guess_shorthand`
stub once it is wired, plus future callers who want a one-stop reference
instead of inventing their own mappings.

**`_CHAPTER_KEY_PATTERN` gains a non-capturing `(?:CH)?` group.** The
single regex stays the source of truth and both forms produce the same
`(base, num_str, slug)` tuple, so every downstream consumer of
`parse_chapter_key` (`build_bookend_text`, `humanize_chapter_slug`, the
restitch metadata path) accepts both forms with no further plumbing.
This closes the convention gap from `feedback_book_chapter_slug.md`
without touching the 30 published asset paths or the Hamming directory
names. Single-pattern regex extension is preferred over an alternation
branch so future captures (named groups, ordering) stay aligned.

**`_llm_guess_shorthand(token: str) -> str | None` is an intentional
stub.** Returns `None` today; docstring records the TODO with the user's
`2026.05.19` request to wire a Haiku / GPT-nano fallback for unknown
shorthand tokens. Stubbing it now means the dict and the fallback hook
ship together as a coherent surface, and future PRs do not have to
re-introduce the dict alongside the LLM call.

**Regen runs post-merge from `main`.** Rationale matches the generalized
`feedback_zotero_sync_commit_hash` lesson: the embedded `_git_short_hash`
in the published zip metadata should match what `origin/main` reports,
not a branch SHA that might shift under a rebase-merge. The regen
sequence is: land code + tests on a worktree branch, open PR, merge to
main, `git checkout main && git pull`, run
`python scripts/regen_hamming_bookends_ch1_10.py`, then
`scripts/abs_refresh.sh` (waiting on the flock).

## Approach

The mechanical surface area is small. Add the dict, extend the regex by
two characters, replace one line in the bookend branch, add a four-line
stub, update the test assertions to match the new wording, append two
dated dendron sections.

In `swanki/utils/formatting.py`, place `SHORTHAND_EXPANSIONS` immediately
after `_LABEL_EXPANSION` at :461 (the two are conceptually sibling
vocabularies). Keys are uppercase tokens, values are the spoken /
human-readable expansion. `_llm_guess_shorthand` lives next to it.
Extend `_CHAPTER_KEY_PATTERN` at :300 to:

```python
_CHAPTER_KEY_PATTERN = re.compile(
    r"^(?P<base>[A-Za-z][A-Za-z0-9]+)_(?:CH)?(?P<num>\d{1,3})_(?P<slug>[a-z][a-z0-9-]+)$"
)
```

In `swanki/audio/_common.py` at :1639, replace
`num_spoken = chapter_number_spoken(num_str)  # e.g. "01" -> "o one"`
with:

```python
# context_key uses int(num_str) directly; do NOT funnel through
# chapter_number_spoken -- it returns "o seven" for legacy callers.
num_spoken = f"Chapter {int(num_str)}"
```

The rest of the chapter branch (`context_key` assembly, `spoken_type`
mapping, start / end string templates) stays verbatim. The import of
`chapter_number_spoken` at :1620 can drop if no other code path in this
file calls it; verify with `rg "chapter_number_spoken" swanki/audio/_common.py`
before removing.

Test updates in `tests/test_audio_common.py`:
the `_CH_EXACT` constant at :620 changes from
`"Hamming, Art Doing Science, 2020, o three, history of computers hardware"`
to `"Hamming, Art Doing Science, 2020, Chapter 3, history of computers hardware"`.
The six bookend assertions at :623-652 then pick up the new wording via
the constant. The roman-numeral cases at :655-676 update their inline
strings from `"o seven, artificial intelligence two"` to
`"Chapter 7, artificial intelligence two"` (and `"o eight"` ->
`"Chapter 8"`). Add three new equivalence tests showing
`build_bookend_text(legacy_key, ...) == build_bookend_text(ch_prefixed_key, ...)`
for lecture / summary / reading.

Test additions in `tests/test_utils_formatting.py`: a basic
`parse_chapter_key("hammingArtDoingScience2020_CH03_history-of-computers-hardware")`
returning `('hammingArtDoingScience2020', '03', 'history of computers hardware')`;
an at-prefix variant (`"@..."`); an identical-to-legacy invariant test
asserting both forms yield the same tuple. `SHORTHAND_EXPANSIONS` shape
tests check the five expected keys map to the expected values.
`_llm_guess_shorthand("WAT")` returns `None`.

Dendron note updates record the rationale in the two affected module
notes per the project's "decision history" convention. The weekly note
gets the pending bullet flipped when the merge lands.

Post-merge regen sequence on `main`:

```bash
git checkout main && git pull --ff-only origin main
conda activate swanki
python scripts/regen_hamming_bookends_ch1_10.py
flock -w 300 200 < /tmp/abs-refresh.lock || true
scripts/abs_refresh.sh
```

The regen script preflights Fish via `swanki.audio.surgical.fish_speech_healthy`
and uses the `hamming-20260428T1135-science-vs-engineering` reference voice
matching the original render so re-TTSed bookends do not voice-shift.

## Gotchas

**Equivalence invariant is non-negotiable.** A test must assert
`build_bookend_text(legacy_key, ...) == build_bookend_text(ch_prefixed_key, ...)`
for at least one chapter per audio type. Without this, a future regex
tweak (`(?:CH)?` -> `(?:CH_)?` or similar) silently desyncs the two paths
and only manual listening would catch it.

**`SHORTHAND_EXPANSIONS` scope is bookend + stub only.** Do not route
`humanize_citation_key` through it; the per-card prefix path
(`humanize_card_text_for_tts`'s `_CHAPTER_BARE` and `_SECTION_BARE`
callbacks at :475-479) is the only other `CH` / `SEC` consumer and
already uses inline `int(...)` rendering. A future cleanup PR could
route those through the dict; that is explicitly out of scope here.

**`chapter_number_spoken` stays invariant.** Four existing test cases at
`tests/test_utils_formatting.py` lock the legacy `"o N"` form for the
helper's other callers. The bookend branch bypasses it via the inline
`int(num_str)` rendering. Code comment at the call site spells the
choice out.

**Commit-before-sync.** The regen runs from `main` AFTER merge so the
embedded `_git_short_hash()` in the published zip metadata is the
canonical merged SHA. Running from the worktree pre-merge would leave
the zip tagged with a branch SHA that may not match `origin/main` after
a rebase-merge -- not a functional break, but it muddies provenance.

**`abs_refresh` flock contention.** The hourly cron run holds
`/tmp/abs-refresh.lock` while sweeping. Use `flock -w 300 200 < /tmp/abs-refresh.lock`
before invoking `scripts/abs_refresh.sh` manually so a concurrent run
does not cause the manual call to exit silently.

**Pre-existing test failures.** `test_humanize_latex` and
`test_generate_reading_audio_mocked` fail on `main` today; both are
unrelated to this change. Exclude from judgment when running the suite.

**Drop the `chapter_number_spoken` import only if no other call survives
in `_common.py`.** Quick `rg` check before deleting. If anything else
still uses it (e.g. a chunk-naming helper), keep the import.

## Verification

**Unit (no Fish, no ABS).** Run
`pytest tests/test_audio_common.py tests/test_utils_formatting.py -x`:

- The six chapter-form bookend assertions for `_CH_KEY` pass with
  `"Chapter 3"` wording.
- The two roman-numeral cases for ch07 / ch08 pass with `"Chapter 7"`
  / `"Chapter 8"` plus the trailing roman-numeral word still spelled
  via `humanize_chapter_slug_spoken`.
- Three new accept-both equivalence tests for lecture / summary / reading
  pass.
- `parse_chapter_key` tests for `_CH<NN>_<slug>` and the identical-to-legacy
  invariant pass.
- `SHORTHAND_EXPANSIONS` shape test passes (five keys, expected values).
- `_llm_guess_shorthand` stub returns-`None` test passes.
- Existing `chapter_number_spoken` and `humanize_chapter_slug_spoken`
  tests stay green (invariants).

**Full suite.** `pytest -x` green except the two documented pre-existing
failures (`test_humanize_latex`, `test_generate_reading_audio_mocked`).

**Lint and types.** `ruff check swanki/utils/formatting.py swanki/audio/_common.py tests/`
plus `mypy swanki/utils/formatting.py swanki/audio/_common.py` per the
project's lint and type-checking strategies.

**Post-merge regen pass-2.** 30 mp3s re-stitched (10 chapters x 3 audio
types). Only the bookend mp3s + the final stitched per-type mp3 + the
`chunk_timeline.json` sidecar change; non-bookend chunk mp3s stay
sha256-identical (assert via `sha256sum` against a snapshot of the
pass-1 chunks dir). Zotero sync prints 30+ uploads at the new merged
main hash. `abs_refresh` logs `"boundaries shifted"` for Lecture /
Reading / Summary item `updatedAt` bumps and the chapters count stays
10 across all three audio types.

**Manual listen on BookPlayer (pull-to-refresh).** ch07 lecture START
reads *"This lecture is posted as Hamming, Art Doing Science, 2020,
Chapter 7, artificial intelligence two. Let's Begin."*; ch08 summary
END reads *"This concludes the summary. It is posted as Hamming, Art
Doing Science, 2020, Chapter 8, artificial intelligence three."*

## Open Questions

1. `SHORTHAND_EXPANSIONS` is canonical reference; only the `CH -> Chapter`
   entry is consumed by the bookend branch in this PR. `SI`, `S` / `SEC`,
   `PART`, `APP` land as documented expansions for future callers --
   especially `_llm_guess_shorthand` once wired. The inline regex
   callbacks `_CHAPTER_BARE` and `_SECTION_BARE` in
   `humanize_card_text_for_tts` keep the per-card prose path on `int(...)`
   rendering; a future cleanup could route them through the dict and is
   explicitly out of scope here. Assumption: documented expansions are
   not dead weight given the imminent stub-wiring follow-up.
2. `_llm_guess_shorthand` is intentionally inert. Wiring a Haiku /
   GPT-nano fallback for unknown shorthand tokens is a separate follow-up;
   the TODO comment cites the user's `2026.05.19` request verbatim.
3. The concurrent solution-manual worktree is assumed not to touch
   Hamming dirs / manifests during the regen. True today: solution-manual
   is a different paper batch, ABS items differ, Zotero rate limits are
   the only theoretical contention and have been fine in prior pass-1
   regens. If a future batch overlaps, gate the regen on the other
   worktree's job completion.
