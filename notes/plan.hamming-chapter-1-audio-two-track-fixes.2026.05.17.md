---
id: bphjgy95omof91hn3k4som9
title: Hamming Ch1 Audio Two-Track Fixes
desc: ''
updated: 1778996941923
created: 1778996941923
---

## Context

Six orange Zotero annotations on the Hamming "Art of Doing Science and Engineering" Ch1 (Orientation) source PDF surface audible defects in the *current* on-disk reading audio. They collapse to **4 root causes**. We want a durable **two-track** fix, not a one-off patch:

- **Track A (zero-shot / feed-forward):** bake corrections into the generation pipeline so every *future* reading / lecture / summary render is clean without manual intervention.
- **Track B (surgical):** precisely repair the *current* Ch1 reading audio via `chunk_manifest.json` + `restitch_from_chunks` — re-TTS only the affected chunks, NO full pipeline regen (a full regen is slow and would re-roll the LLM, losing the hand-corrections RC2/RC4 require).

Root causes (verified against the live on-disk artifact — **do not re-derive**):

- **RC1 SECTION-BREAK LEAK** (annotations #1 p.2 "Second, when I went to Bell", #2 p.4 "learn new fields of knowledge when", #4 p.5 "In the position I found myself in at the Laboratories"). `expand_acronyms_for_tts()` runs *before* `split_transcript_by_sections()` in `reading.py` (`:190` then `:240`), `lecture.py` (`:865` then `:916`), `summary.py` (`:156` then `:206`). The regex `_STANDALONE_ACRONYM_RE = r"(?<![A-Za-z])([A-Z]{2,6})(?![A-Za-z])"` (`_common.py:360`). **SETTLED GROUND TRUTH:** in `SECTION_BREAK` the `_` before `BREAK` is a non-letter so the negative lookbehind is *satisfied*; the `-` after `K` is a non-letter so the lookahead is *satisfied*; `BREAK` is 5 caps within `{2,6}` so it matches and becomes `B-R-E-A-K`. `SECTION` is 7 letters so it does NOT match. Result on disk: literal `---SECTION_B-R-E-A-K---` in **chunk0** and **chunk31** of the live 58-chunk reading manifest. `split_transcript_by_sections` matches the literal `SECTION_BREAK_MARKER = "---SECTION_BREAK---"` (`_common.py:959,976`) so it misses the mangled form; Fish then *speaks* "section b-r-e-a-k". NOTE: two scouts mis-analyzed this (one claimed the result is `---S-E-C-T-I-O-N-_-B-R-E-A-K---`, one claimed the regex can't match at all) — **both WRONG**; the empirical on-disk artifact is authoritative.
- **RC2 DROPPED SENTENCE** (annotation #3 "was this dropped by the reading transcript?"). The source sentence "they arise so you will not be left behind, as so many good engineers are in the long run" is absent from **all 58 chunk texts** — an LLM Pass-2 omission in `generate_reading_audio()`; there is no completeness guard. It is co-located with the leaked marker at chunk31 but is a **different root cause**: fixing the marker does NOT regenerate the sentence.
- **RC3 JOKE PROSODY** (annotation #3 p.5). chunk37 "The past was once the future and the future will become the past." is rendered plain, no Fish delivery tag; there is no prompt guidance for aphorism / punchline prosody.
- **RC4 TABLE LINEARIZATION** (annotation #6 p.8). The "Personnel problems" machine-vs-human advantages table appears in chunk53/54 linearized as label/value pairs with `[pause]`; rows are partial/incomplete. No "read every table row across columns, drop none" rule exists.

**Already fixed this session (done — fold into the commit, do not re-plan):** `scripts/zotero_paper_import.py` `get_pdf_attachments()` and `scripts/zotero_annotations.py` `get_annotations()` had an unpaginated `zot.children()` call (caps at 100). The Hamming item has 147 children, so the source PDF (child > 100) was invisible and `/zotero-annotations` silently returned zero. Fixed by wrapping in `zot.everything(...)` (matches the existing pattern at `zotero_paper_import.py:170`). Verified: now returns all 6 orange annotations. These two one-line edits are applied on the main working tree (uncommitted).

Workstation = **gilahyper**: `audio=all`, `models=fish_speech` (local Fish at `http://localhost:8080`, `british-prof` voice), `anki=default`.

## Relevant Files

- `swanki/audio/_common.py` — **MODIFY**. `expand_acronyms_for_tts` `:363-387`; `_STANDALONE_ACRONYM_RE` `:360`; `SECTION_BREAK_MARKER` `:959`; `split_transcript_by_sections` `:976`; `humanize_latex` `:1506` (add row-wise table rule to its system prompt). REFERENCE for Track B: `text_to_speech` `:713`, `write_chunk_manifest` `:1152`, `restitch_from_chunks` `:1196`.
- `swanki/audio/reading.py` — **MODIFY**. `generate_reading_audio` `:42`; `humanize_latex` call `:137`; `expand_acronyms_for_tts` `:190`; `split_transcript_by_sections` `:240`; Pass-2 LLM ~`:150-167`. Add the deterministic completeness guard after Pass-2.
- `swanki/audio/lecture.py` — **REFERENCE** (`:865` expand, `:916` split). Fixed transitively by the in-function sentinel mask. Verify no separate marker handling.
- `swanki/audio/summary.py` — **REFERENCE** (`:156` expand, `:206` split). Same: fixed transitively. Verify no separate marker handling.
- `swanki/conf/models/fish_speech_hamming.yaml` — **MODIFY**. Per-paper `system_prompt_addendum` for RC3 prosody (confirmed: this file exists; `swanki/conf/prompts/book_voice.yaml` also exists — confirm which layer carries the addendum without perturbing the first-person book voice before editing).
- `scripts/regen_campagne_lecture_chunks.py` — **REFERENCE** pattern for the Track B tool (load manifest → index by `chunk["index"]` → `text_to_speech` per chunk → `restitch_from_chunks`).
- `swanki/audio/<new surgical helper>` + `scripts/<new CLI>` — **NEW**. Importable function in `swanki/` (testable, reuses `restitch_from_chunks` / `text_to_speech`) plus a thin `scripts/` CLI wrapper.
- `scripts/abs_set_chapter_titles.py` — **REFERENCE** for post-restitch republish.
- `scripts/zotero_paper_import.py` (`:195`) and `scripts/zotero_annotations.py` (`:73`) — **MODIFY (ALREADY DONE this session)**; fold the two one-line `zot.everything(...)` edits into this commit.
- `tests/test_audio_common.py` — **MODIFY**. Add sentinel-survives-expansion regression test + completeness-guard test + combined SAR-allowlist/override test.
- `tests/test_audio_reading.py` — **MODIFY** as needed for the completeness guard.
- Live Track B manifest — **REFERENCE / data**: `/scratch/projects/torchcell-scratch/Swanki_Data/hammingArtDoingScience2020/hammingArtDoingScience2020_01_orientation_12/reading_chunks/chunk_manifest.json` (verified: 58 chunks; has the `postprocessor` block; keys `audio_type, output_file, bookend_start, bookend_end, postprocessor, chunks`).

## Key Design Decisions

1. **RC1 Track A = sentinel protection inside `expand_acronyms_for_tts`** — NOT reordering split-before-expand, NOT a tolerant splitter. The scrubber pipeline order (`clean_markdown_for_tts → strip_chapter_filename_slug → expand_acronyms_for_tts → apply_pronunciation_overrides → strip_forbidden_fish_tags → add_tts_pauses`) is *intentional and documented* in `notes/swanki.audio._common.md` 2026-05-14: `apply_pronunciation_overrides` is deliberately *after* acronym expansion so per-paper YAML wins (SAR → S-A-R, then per-paper override). Reordering risks regressions across all three audio types. Instead, mask `SECTION_BREAK_MARKER` to an opaque placeholder with no `{2,6}`-uppercase run bounded by non-letters, run the acronym regex, then restore. One fix site inside `expand_acronyms_for_tts` → reading/lecture/summary all benefit.
2. **Track B target = the READING manifest only.** Lecture has only 26 chunks; chunk indices are **local per audio type**, never a shared index space. The surgical tool MUST take explicit `--audio-type` / `--manifest-path` and never assume a shared index. Lecture/summary Ch1 may carry the same leaked marker *independently* — check their own manifests separately (a scout checked the wrong audio type; do not repeat).
3. **RC1 surgical Ch1 patch needs hand-corrected chunk text.** `restitch_from_chunks` replays the existing `chunk["text"]` and does NOT re-run the LLM. So chunk31 must have BOTH the mangled marker removed AND the RC2 dropped sentence reinstated before re-TTS; chunk0 needs only the mangled marker removed; chunk37 gets a Fish delivery tag added; chunk53/54 get rewritten row-wise complete against source p.8.
4. **Track A guards, by layer:** RC4 table-linearization rule → Pass-1 `humanize_latex` system prompt (linearize *before* any summarization sees it). RC2 completeness guard → **deterministic** post-Pass-2 check using a `tiktoken` token-count ratio (warn if < ~95%), excluding legitimate LaTeX-humanization rewrites from the diff; **LOG a loud WARNING, do NOT auto-retry** (CLAUDE.md fail-fast; user decides). RC3 prosody → optional per-paper YAML `system_prompt_addendum` so it does not perturb the whitelisted first-person book voice in the lecture critic/refiner.
5. **Reusable surgical tool = importable `swanki/` function + thin `scripts/` CLI.** CLI args `--manifest-path --audio-type --chunk-indices`. Fish Speech health pre-flight (`curl http://localhost:8080`) before any re-TTS. Model `scripts/regen_campagne_lecture_chunks.py`: load manifest → index by `chunk["index"]` → `text_to_speech` per chunk (fish_speech provider, `british-prof` voice, speed ~1.1) → `restitch_from_chunks`.
6. **Post-restitch downstream is explicit ordered steps, not assumed:** re-upload mp3 to Audiobookshelf → re-set chapter titles via `scripts/abs_set_chapter_titles.py` → bump `libraryItem.updatedAt` (else BookPlayer serves stale cached audio). `content_key` filename regex expects `-<type>-<YYYYMMDDTHHMM>-<hash>.ext`. Keep the Zotero fox tag (the Zotero unicode marker) idempotent and re-zip the bundle if the deliverable changed (per `feedback_zotero_fox_tag.md`). Per `feedback_swanki_run_in_terminal.md`: do NOT auto-launch the long pipeline; the short Track B re-TTS+restitch commands are acceptable, but hand the user any long-running step.

## Approach

**Track A — feed-forward pipeline fixes**

A1. **RC1 sentinel mask** (`_common.py` `expand_acronyms_for_tts` `:363-387`). At function entry, replace every occurrence of `SECTION_BREAK_MARKER` with an opaque placeholder that contains no `{2,6}`-length uppercase run bounded by non-letters (e.g. a lowercase token like `\x00sectionbreak\x00` or a digit-padded sentinel — choose a token that round-trips and cannot itself be matched by `_STANDALONE_ACRONYM_RE`). Run `_STANDALONE_ACRONYM_RE.sub(_sub, text)` as today, then restore the placeholder back to `SECTION_BREAK_MARKER` before returning. The mask/restore must wrap the *whole* body so the allowlist and `_sub` logic are untouched. Disambiguating snippet:

```python
_SB_SENTINEL = "\x00sb\x00"  # no [A-Z]{2,6} run bounded by non-letters
text = text.replace(SECTION_BREAK_MARKER, _SB_SENTINEL)
text = _STANDALONE_ACRONYM_RE.sub(_sub, text)
return text.replace(_SB_SENTINEL, SECTION_BREAK_MARKER)
```

This is the single fix site; `reading.py`, `lecture.py`, `summary.py` all call this function, so all three are fixed without touching their files (verify lecture/summary do no separate marker handling — REFERENCE only).

A2. **RC4 table linearization** (`_common.py` `humanize_latex` `:1506` system prompt). Add an explicit rule: when humanizing a table, read **every row across all columns** in natural reading order, drop no row or cell, and do not collapse to label/value pairs that omit content. This runs in Pass-1 so all downstream summarization sees the fully linearized prose.

A3. **RC2 completeness guard** (`reading.py` after Pass-2, ~after `:167`). Deterministic check: tokenize the Pass-1 (post-`humanize_latex`) text and the Pass-2 output with `tiktoken`; compute a token-count ratio; if it drops below ~0.95, emit a **loud `logging.warning`** identifying the paper/chapter and the ratio. Exclude legitimate LaTeX-humanization rewrites from the comparison (compare against the post-humanize Pass-1 text, not raw LaTeX, so equation rewrites don't trip a false positive). **No auto-retry** — fail-fast, surface to the user.

A4. **RC3 prosody addendum** (`swanki/conf/models/fish_speech_hamming.yaml`). Add an optional per-paper `system_prompt_addendum` instructing aphorism/punchline lines to carry a Fish delivery tag for a slight pause + emphasis. Confirm the exact config layer (this file vs `book_voice.yaml`) so the addendum is additive and does NOT perturb the first-person book voice or trip the lecture critic/refiner first-person whitelist.

**Track B — surgical Ch1 reading repair**

B1. **New surgical helper** in `swanki/` (NEW): function `(manifest_path, audio_type, chunk_indices, edits)` — loads the manifest, indexes chunks by `chunk["index"]`, applies provided hand-corrected text to the targeted chunks, calls `text_to_speech` per targeted chunk (fish_speech, `british-prof`, speed ~1.1), then `restitch_from_chunks`. Thin `scripts/` CLI (NEW) exposing `--manifest-path --audio-type --chunk-indices` with a Fish health pre-flight (`curl http://localhost:8080`); abort the whole batch if Fish is down (no retry).

B2. **Hand-corrected chunk text** for the live reading manifest (path in Relevant Files): chunk0 — strip the mangled `---SECTION_B-R-E-A-K---` (restore proper marker or remove per how restitch treats markers); chunk31 — strip the mangled marker AND reinstate the RC2 sentence "they arise so you will not be left behind, as so many good engineers are in the long run"; chunk37 — add the RC3 Fish delivery tag to "The past was once the future and the future will become the past."; chunk53/54 — rewrite the Personnel-problems table row-wise, complete, against source p.8. (See Open Questions for the exact chunk set and verbatim-source policy.)

B3. **Re-TTS + restitch** only the patched chunks via the new tool. Validate the manifest has a `postprocessor` block first (Ch1 does — verified); do not touch `tail_buffer_ms=350` or `gain_match_target_dbfs=-25.0`.

B4. **Downstream republish** (explicit, ordered): upload restitched mp3 to Audiobookshelf → `scripts/abs_set_chapter_titles.py` to re-set chapter titles → bump `libraryItem.updatedAt`. Keep the `content_key` filename pattern `-<type>-<YYYYMMDDTHHMM>-<hash>.ext`. Re-zip the deliverable bundle and keep the Zotero fox tag (the Zotero unicode marker) idempotent. Hand any long-running step to the user.

**Commit**

C1. The `zot.everything(...)` pagination fixes were applied in the *main* working tree this session, but implementation runs in a fresh worktree branched from clean main — so the executor must **re-apply** both one-line edits in the worktree: `zotero_paper_import.py:195` `children = zot.children(item_key)` → `children = zot.everything(zot.children(item_key))` (keep the explanatory comment), and `zotero_annotations.py:73` `children = zot.children(att["key"])` → `children = zot.everything(zot.children(att["key"]))`. Re-verify with `python scripts/zotero_annotations.py hammingArtDoingScience2020 --color orange` (expect 6). Commit alongside the Track A code + tests. Update the relevant dendron module notes (`notes/swanki.audio._common.md`, `notes/swanki.audio.reading.md`, `notes/scripts.zotero_annotations.md`, `notes/scripts.zotero_paper_import.md`) and the weekly note per project workflow.

## Gotchas

- Fish server at `localhost:8080` must be up; there is no retry and a single chunk failure halts the batch — hence the pre-flight health check in the Track B tool.
- After restitch you MUST republish to Audiobookshelf AND bump `updatedAt` or BookPlayer serves stale cached audio.
- The manifest must carry the `postprocessor` block for a faithful restitch (Ch1 has it — verified; still validate defensively before re-TTS).
- `SWANKI_DATA` is empty in the shell env; the real root is `/scratch/projects/torchcell-scratch/Swanki_Data`. The CLAUDE.md conda path is wrong — use `~/miniconda3/envs/swanki/bin/python`, NOT `~/opt/...`.
- `load_dotenv(find_dotenv())` raises `AssertionError` when run from a heredoc — pass an explicit `dotenv_path`.
- Completeness-guard false-positive risk on legitimate LaTeX-humanization rewrites — compare against post-humanize Pass-1 text, exclude rewrites from the diff.
- The SAR allowlist and pronunciation override are complementary; the sentinel mask must not disturb that path — add a combined test.
- Do NOT revert `[pause]` → `[long pause]`: Fish renders `long` as an audible breath (documented 2026-04-26).
- Do NOT touch `tail_buffer_ms=350` / `gain_match_target_dbfs=-25.0` (empirically tuned).
- Hamming is a **book** → the first-person author voice must survive; the RC3 prosody addendum must not trip the lecture critic/refiner first-person whitelist.
- Pre-existing main test failures `test_humanize_latex` (`AttributeError` on `text_agent`) and `test_generate_reading_audio_mocked` (open-file) are NOT regressions — do not chase them.
- Many reprocessed Hamming dirs exist (`_0` .. `_12`) — only `_12` is the live Ch1. Risk of patching the wrong dir or audio type; always pass the explicit manifest path.

## Verification

- **Unit:** sentinel survives `expand_acronyms_for_tts` verbatim (input containing `SECTION_BREAK_MARKER` returns it unmangled) AND `split_transcript_by_sections` still strips the marker on the post-expand text.
- **Unit:** completeness guard warns on a synthetic ~10% drop and stays silent on a pure LaTeX-humanization rewrite (no false positive).
- **Unit:** combined SAR-allowlist + pronunciation-override test still green (sentinel mask did not disturb it).
- **Track B integrity:** after restitch, every untouched chunk mp3 is byte-identical (sha256 unchanged); only the patched chunk mp3s differ.
- **Tracking:** re-run `scripts/zotero_annotations.py hammingArtDoingScience2020 --color orange` to keep the annotation set tracked (should still surface all 6 after the pagination fix).
- **Manual listen:** the 5 patched reading chunks (0, 31, 37, 53, 54) — no spoken "section break"; the RC2 sentence is present at chunk31; chunk37 joke delivered with the tag; the chunk53/54 table read fully row-wise.
- **Lint/types:** `ruff` + `mypy` per project strategy on changed files only; pre-existing failures excluded.

## Resolved Decisions (was Open Questions)

1. **RC2 sentence source:** the executor extracts the missing sentence (and just enough surrounding context to locate the insertion point) **verbatim from the OCR'd Hamming source** (Mathpix markdown for Ch1, or the source PDF `G99UQY55`), splices it into chunk31's text at the correct position, and surfaces the chunk31 before/after text diff for user review before re-TTS.
2. **Track B chunk set:** patch **all 5** annotation-flagged Ch1 reading chunks in one pass — 0 and 31 (strip mangled marker; 31 also gets the RC2 sentence reinstated), 37 (RC3 Fish delivery tag), 53 and 54 (RC4 row-wise complete table rewrite vs source p.8).
3. **Track B execution:** the executor runs Track B **end-to-end** — Fish health pre-flight (`curl http://localhost:8080`, abort if down), per-chunk re-TTS, `restitch_from_chunks`, then the downstream ABS re-upload + `abs_set_chapter_titles.py` + `updatedAt` bump and the idempotent Zotero re-zip / fox tag. Stop and report if Fish is down or the postprocessor block is absent.
