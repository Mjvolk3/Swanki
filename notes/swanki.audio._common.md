---
id: 0ddcdd33da14487abaca264
title: _common
desc: ''
updated: 1773142603440
created: 1773142603440
---

## 2026.03.10 - Shared TTS utilities extracted from monolithic audio module

Houses the cross-cutting audio helpers that all generation modules depend on: `chunk_text` (paragraph/sentence boundary splitting), `clean_markdown_for_tts` (strip formatting), `text_to_speech` (ElevenLabs API with FFmpeg speed adjustment), `combine_audio` (pydub crossfade merging), `validate_audio_file` (size and duration checks), and `filter_metadata` (academic metadata stripping).

## 2026.03.12 - Add explicit type annotation for TTS stream result

Added `data: bytes` annotation with `# type: ignore[arg-type]` to the `text_to_speech` stream join to satisfy mypy. The ElevenLabs SDK returns a union type that mypy cannot narrow through `hasattr`.

## 2026.03.13 - Section-aware audio infrastructure for quality improvements

Added five new functions to support real silence between sections, bookend announcements, and reliable acronym expansion across all audio types. Motivated by listening to the merzbacher paper's generated audio and identifying quality gaps: SSML `<break>` tags were unreliable, no start/end announcements existed, and acronyms were inconsistently expanded.

- `generate_silence(duration_ms, output_path)`: creates silent MP3 via pydub
- `split_transcript_by_sections(transcript, marker)`: splits on `---SECTION_BREAK---` markers
- `combine_audio_with_section_pauses(sections, output, ...)`: assembles section-grouped chunks with real silence gaps and optional bookend clips
- `generate_bookend_audio(citation_key, audio_type, position, ...)`: generates cached START/END TTS clips with humanized citation key; lecture variant includes paper title
- `extract_acronyms(text)`: regex extraction of `ACRONYM (Full Form)` and reverse patterns for injection into LLM prompts

## 2026.03.15 - TTS model tiering, paragraph chunking, and SSML pause injection

Three changes to reduce ElevenLabs costs and improve audio prosody.

- **TTS model tiering**: Added `DEFAULT_TTS_MODEL = "eleven_flash_v2_5"` and `LECTURE_TTS_MODEL = "eleven_multilingual_v2"`. The `text_to_speech()` function now accepts a `tts_model` parameter (defaults to flash). Reading, summary, cards, and bookends use the cheaper flash model (0.5x credits, 40k char limit); lecture explicitly passes the premium multilingual model for quality. Previously everything used `eleven_multilingual_v2` at 1 credit/char.
- **Paragraph-only chunking**: New `chunk_text_paragraphs()` splits only at paragraph boundaries, never mid-sentence. Used for lecture TTS to avoid prosody-breaking mid-sentence splits. Default max 4500 chars (vs 2000-3000 for `chunk_text`).
- **SSML pause injection**: New `add_tts_pauses()` inserts `<break time="0.7s" />` between paragraphs and `<break time="0.4s" />` after line-ending colons. ElevenLabs v2 models interpret these as natural AI-modeled pauses (not raw silence). Replaces the old approach of writing "[pause]" or "Pause." in transcripts, which the TTS model read aloud.

## 2026.04.03 - Fish Speech provider integration, LaTeX humanization, provider-aware pauses

Added self-hosted Fish Speech S2 Pro as an alternative TTS provider, eliminating ElevenLabs API dependency for audio generation. The core `text_to_speech()` function now dispatches to `_tts_elevenlabs()` or `_tts_fish_speech()` based on a `provider` key in `**tts_kwargs`, keeping all 10+ existing call sites unchanged.

- **Provider dispatch**: Refactored `text_to_speech()` to accept `**tts_kwargs` and route to private backend functions. `_tts_fish_speech()` POSTs to the Fish Speech `/v1/tts` endpoint with optional `reference_id` for voice cloning. Extracted speed adjustment into shared `_apply_speed()` helper.
- **SSML stripping**: `_strip_ssml()` removes ElevenLabs `<break>` tags before sending text to Fish Speech, which uses its own inline `[tag]` syntax.
- **Reference voice management**: `ensure_fish_speech_reference()` registers a WAV clip with the Fish Speech server via `/v1/references/add` (multipart upload), checking `/v1/references/list` first to avoid duplicates.
- **Provider-aware pauses**: `add_tts_pauses()` now accepts a `provider` parameter -- inserts SSML `<break>` tags for ElevenLabs, `[pause]`/`[short pause]` for Fish Speech.
- **LaTeX humanization**: New public `humanize_latex()` function with a dedicated `_LATEX_SYSTEM_PROMPT` that focuses the LLM solely on converting LaTeX to spoken form. Two-pass approach: humanize first, then generate transcript. Moved from reading.py-only to shared utility so card.py can use it.
- **Server discovery with fallback**: `_find_fish_speech_server()` scans ports 8080-8083 for an available Fish Speech server, falling back to wait-and-retry if all are busy. Enables multi-server parallel paper processing.
- **Audio truncation fix**: Reverted `chunk_length` to 200 (safe default), bumped `max_new_tokens` to 4096 for headroom. Timeout increased from 300s to 600s.
- **Richer inline pauses**: Fish Speech path now adds `[short pause]` after sentence-ending periods, not just paragraph breaks. Stacked tags are collapsed.

## 2026.04.15 - Multi-server Fish Speech parallelism

Scale Fish Speech audio generation across multiple GPU server instances by distributing chunks round-robin. A single paper's audio chunks now process concurrently instead of serially, cutting wall time roughly in proportion to the number of healthy servers.

- **Server discovery with caching**: `_discover_fish_speech_servers()` health-checks all `_FISH_SPEECH_PORTS` once and caches the healthy list. Re-discovers when the cached count is below the configured port count so late-starting servers get picked up.
- **Round-robin picker**: `_pick_fish_speech_server()` replaces the old "find one and wait" logic with a thread-safe global counter that hands out servers in rotation.
- **Parallel batch helper**: New `tts_chunks_parallel()` accepts `(text, output_path)` pairs and runs them through a `ThreadPoolExecutor` sized to the number of healthy servers. Falls back to sequential when only one server is available or only one chunk is queued.
- **Longer client timeout**: `_tts_fish_speech()` httpx client timeout bumped from 600s to 1800s to tolerate large chunks on slower GPUs.
- **Sentence-fallback chunking**: `chunk_text_paragraphs()` now pre-splits any single paragraph that exceeds `max_chars` at sentence boundaries, so no chunk ever exceeds the limit. Previously oversized paragraphs were emitted as-is, which Fish Speech would truncate.

## 2026.04.16 - Pause-based chunk transitions and chunk retention for surgical regeneration

Replaced 200ms cross-fade between TTS chunks with direct concatenation, letting Fish Speech `[long pause]` and ElevenLabs `<break>` tags supply transitions naturally. Crossfade was clipping sentence endings and the timbre mismatch across independently-synthesized chunks was audible. At the same time, chunk files are now retained instead of being deleted, so re-running TTS on a single bad chunk and restitching is possible without regenerating the whole audio.

- **Crossfade defaults flipped to 0**: `combine_audio()` and `combine_audio_with_section_pauses()` now default `crossfade_ms` / `chunk_crossfade_ms` to `0` instead of `200`. Existing call sites pass `chunk_crossfade_ms=0` explicitly so behavior is independent of the default.
- **`append_chunk_pause(text, provider)`**: Idempotent helper that appends `[long pause]` (Fish Speech) or `<break time="1.0s" />` (ElevenLabs) to the end of a chunk's text. The ElevenLabs idempotency check looks for any trailing self-closing SSML tag (`/>`), which is intentional -- we do not stack any trailing SSML.
- **`write_chunk_manifest(chunks_dir, audio_type, output_file, chunks, ...)`**: Writes `chunk_manifest.json` next to the chunk files. Records audio type, output filename, optional bookend filenames, and per-chunk index/section/text/file. Drives the surgical-regen workflow.
- **`restitch_from_chunks(manifest_path, output_path, ...)`**: Reads the manifest, groups chunk paths by section, and calls `combine_audio_with_section_pauses` to reassemble final audio. Asserts each chunk file exists before assembly so a missing chunk fails fast.

## 2026.04.17 - Expanded humanization prompt for ASCII math, units, inequalities, and stray dollars

`_LATEX_SYSTEM_PROMPT` now covers the full span of inline notation that reaches TTS, not just `$...$` delimited LaTeX. Orange annotations on the zvyagin paper's reading audio showed recurring failures on bare unicode Greek (e.g. "p_θ"), inequalities read as "greater than" when "more than" is more natural, unit abbreviations ("12 h" → "12 hours"), version numbers ("NCCL 2.10.3"), approximation tildes, and stray dollar signs leaking through from mathpix output. Card audio was already using this prompt; reading now shares it too (see `swanki.audio.reading`).

- **Stray-dollar rule**: Explicit instruction to delete any bare `$` not clearly delimiting a math expression, so the TTS never says "dollar" unless prose is about currency.
- **Inequalities**: `>` → "more than" (not "greater than"), `<` → "less than", `≥`/`≤` → "at least"/"at most".
- **Units**: numeric-adjacent `h`/`s`/`min`/`ms`/`bp`/`kb`/`Mb`/`GB`/`TB` expand to full words; acronym units like `CPU`/`GPU` stay as acronyms.
- **Version numbers**: `NCCL 2.10.3` → "N C C L version 2.10.3" — prefix "version" and keep the dotted sequence intact.
- **Bare Greek in prose**: covers the common case where a figure caption or inline math loses its delimiters after markdown conversion, leaving unicode Greek letters floating in prose.

## 2026.04.26 - Sentence-boundary pacing and Fish Speech punctuation/concat fixes

Three independent fixes targeting Fish Speech S2-Pro pacing and pronunciation. Fish is fully tag-driven for pauses (newlines aren't respected), so previous heuristics that relied on `\n\n` paragraph breaks produced lectures that "blazed through" any LLM output emitted as one long paragraph.

- `add_tts_pauses`: when no paragraph breaks exist, inject `[short pause]` every third sentence boundary (`(?<=[.!?])(?=\s+[A-Z])`). Restores lecture cadence without depending on LLM formatting.
- `append_chunk_pause`: chunk-end tag changed from `[long pause]` to `[pause]`. Fish was rendering `[long pause]` as an audible breath/sigh at every chunk concatenation point; `[pause]` is reliably silent. Real silence between chunks is now supplied deterministically by the combine helper.
- `combine_audio_with_section_pauses` gains two parameters:
  - `chunk_tail_trim_ms` — strip this many ms from the end of each chunk before concat (clip residual tag artifacts without cutting speech; lecture path uses 100 ms for Fish).
  - `chunk_pause_ms` — insert real `AudioSegment.silent()` gap between chunks within a section (lecture path uses 300 ms for Fish).
- New `_normalize_fish_speech_punct(text)` folds Unicode punctuation into ASCII before TTS: em-dash to comma+space, en-dash/minus to hyphen, curly quotes to straight, ellipsis to three periods, NBSP to space. Wired into `_tts_fish_speech` after SSML stripping. Fish's tokenizer was otherwise garbling these characters or dropping them silently.

## 2026.04.30 - Silence-aware trim, gain match, and crossfade co-existence

Three independent fixes to `combine_audio_with_section_pauses`, all driven by Hamming-book listener bookmarks reporting chunk-boundary artifacts (volume jumps, sigh between chunks, sentences crashing together, last syllable getting clipped). All three preserve intra-chunk dynamics — no compression, no flattening — and target only the seams.

### Silence-aware trim replaces blind tail cut

The blind `seg = seg[:len(seg) - chunk_tail_trim_ms]` cut was risky: if Fish rendered speech in the trim region, the trim chopped off the last word's decay tail. Replaced with a `pydub.silence.detect_silence` scan over the last `(chunk_tail_trim_ms + 200)` ms of the chunk:

- `silence_thresh = max(seg.dBFS - 16, -50.0)` — relative to chunk's own mean, so quiet chunks aren't over-trimmed.
- `min_silence_len = 80` — short enough to detect natural inter-word silence, long enough to ignore brief pops.
- `trailing` = silences whose end touches the scan window's end (within 30 ms tolerance).
- If no trailing silence is detected (chunk ends mid-speech), the chunk is left intact — no blind trim.
- If trailing silence is detected, we cut **inside** that silence with a `tail_buffer_ms = 350` post-speech buffer. This was tuned over v7-v9: 0 ms (cut at speech-silence transition) felt clipped, 150 ms still sounded clipped to the listener even though speech wasn't being cut, 350 ms gives enough room that no chunk is perceived as truncated. Fish's sigh-then-silence tag artifact still gets eaten when a chunk ends with one because the 350 ms buffer lands inside the silence portion before the silence ends.

Side effect: `chunk_tail_trim_ms` is now effectively a **scan-window** parameter (how far back to look for silence) rather than a guaranteed cut amount. Net trim varies per-chunk; ranges from "no trim" (speech to end) to "much more than `chunk_tail_trim_ms`" (long trailing silence + sigh).

### Per-chunk RMS gain match

`gain_match_target_dbfs` parameter (None disables, default None — preserves prior behavior for non-Fish callers). When set, each chunk + bookend is shifted by `(target - seg.dBFS)` so all components land at the same mean dBFS. Empirically the Hamming Fish output drifted ~2.5 dB chunk-to-chunk and bookends were 4-6 dB hotter than chunks. The shift is a single multiplicative scalar — pure gain, no compression, no peak limiting — so emphasized syllables stay loud relative to their surroundings within each chunk. Lecture path uses `-25.0` as the target (close to the Fish output's mean); silent segments (`dBFS == -inf`) skip the math.

### Crossfade and chunk_pause_ms now stack

Old code skipped `chunk_pause_ms` insertion when `chunk_crossfade_ms > 0` (the `if chunk_pause_ms > 0 and chunk_crossfade_ms == 0` guard). Removed the guard. Now both apply: silence is inserted first, then the next chunk crossfades into the trailing silence. Net effect is a smooth fade-in of the next chunk over the existing inter-chunk gap — addresses listener complaint about "abrupt prosody jump" at chunk transitions. Lecture path uses `chunk_pause_ms=700` + `chunk_crossfade_ms=50` together.

## 2026.05.14 - Hamming bookmark response: deterministic TTS-prep scrubbers + chapter-slug helper

Five new helpers + one constant land alongside `_normalize_fish_speech_punct` and follow the same "deterministic post-refine guard" idiom as `_strip_duplicate_openers` in lecture.py. They run between the refine loop and `add_tts_pauses`, in this order: `strip_chapter_filename_slug` -> `expand_acronyms_for_tts` -> `apply_pronunciation_overrides` -> `strip_forbidden_fish_tags`. The `detect_repeated_phrases` n-gram scanner is folded into the refine loop itself so a repeat triggers another iteration via `LectureTranscriptFeedback.repeated_phrases` + the new validator.

- `FISH_SPEECH_FORBIDDEN_TAGS` (constant): single source of truth for the 21 tags (`[sigh]`, `[inhale]`, `[exhale]`, `[clearing throat]`, ...) the writer prompts already forbid and the critic flags. The new `strip_forbidden_fish_tags` regex strips any leak through the LLM with a WARNING-level log so prompt drift surfaces instead of disappearing into the audio (Theme 9 — listener heard "breathing through a straw" sigh artifacts).
- `expand_acronyms_for_tts(text, allowlist)`: rewrites standalone uppercase 2-6-letter tokens as letter-by-letter (`SAR -> S-A-R`). Camel-case identifiers (`myACRONYM`, `ABCfoo`) are skipped via a `(?<![A-Za-z])`/`(?![A-Za-z])` lookaround. The allowlist (USA, NASA, DNA, RNA, ...) keeps already-pronounceable tokens intact. Theme 6 — fixes Hamming Ch 3 reading "SAR" as "say R".
- `apply_pronunciation_overrides(text, dict)`: whole-word case-sensitive substitution. Per-paper YAML carries the dict (`fish_speech_hamming.yaml` ships `Decisively -> "decisively,"`); empty dict is a no-op. Runs AFTER `expand_acronyms_for_tts` so a per-paper rewrite for a specific token wins over the generic letter-by-letter pass. Theme 7.
- `detect_repeated_phrases(transcript, n=5, threshold=3, min_distinct_content_words=3)`: n-gram shingle scanner with a stopword filter (drops "the way that you can" style chatter). Returns repeated phrases in descending frequency order. Wired into `_refine_transcript` so the LLM critic gets explicit phrases to vary on the next iteration. Theme 5 — caught the "his last observation he said" repetition the LLM critic missed.
- `strip_chapter_filename_slug(text)`: regex safety net that catches any raw `<base>_<NN>_<slug>` chapter content_key that leaks into transcript prose, replacing it with `Chapter <N>: <human slug>`. The proper humanization happens earlier in `generate_bookend_audio` via `humanize_chapter_slug`; this stripper is for stray interpolation. Theme 8.

`generate_bookend_audio` now branches on `humanize_chapter_slug`: when the citation_key matches the `<base>_<NN>_<slug>` shape, the lecture-start announcement reads "Chapter 3: history of computers hardware. From Hamming, Art Doing Science, 2020." instead of the listener-reported "zero three, history of computers hardware". Non-chapter inputs fall through to the existing `humanize_citation_key` path.

`combine_audio_with_section_pauses` is unchanged at the function level — the existing `tail_buffer_ms=350` constant remains the empirically-tuned sweet spot (v7=0 clipped, v8=150 clipped, v9=350 clean). Theme 1 (edge cutoffs) is addressed downstream of Theme 4 by the tighter chunk cap, which keeps body sentences from being cut mid-thought.

## 2026.05.14 - Strip chunk-boundary pause tags instead of appending one (Fish stutter fix)

Listener flagged audible stutter at every chunk boundary in the post-merge Hamming audio. Inspecting the chunk manifest text confirmed each Fish chunk ended with `\n[short pause]\n[pause]` — `add_tts_pauses` injects `[short pause]` after sentence-end+newline and `[pause]` between paragraphs, then the (now-removed) fish branch of `append_chunk_pause` added one more ` [pause]`. Fish renders these tokens as a brief audible artifact, then the deterministic `chunk_pause_ms=700` silence plays — listener perceives a double-beat stutter at every join.

Fish branch of `append_chunk_pause` now strips trailing AND leading pause tags via the new `strip_chunk_boundary_pause_tags` helper instead of appending one. Inter-chunk silence is supplied entirely by `combine_audio_with_section_pauses` `chunk_pause_ms`. Mid-chunk pause tags are preserved — they signal complex-sentence comprehension breaks or dramatic effect (the listener's stated design principle).

ElevenLabs branch unchanged: the `<break time="1.0s" />` SSML tag IS the pause mechanism for ElevenLabs (no deterministic inter-chunk silence at concat time), so the append behavior is correct for that provider.

Test fallout: `test_append_chunk_pause_fish_speech` and `test_append_chunk_pause_strips_trailing_whitespace` updated; new tests cover trailing-tag stripping (single, stacked, mixed forms), leading-tag stripping, mid-chunk preservation, and idempotency.

## 2026.05.14 - generate_bookend_audio rewritten for chapter form (Theme 8 follow-up)

Per direct user spec, the lecture bookend for chapter inputs now reads the citation key exactly as written, with the chapter number rendered in spoken form ("01" -> "o one"). Old form dropped the leading zero and re-ordered components ("Chapter 3: history of computers hardware. From Hamming, Art Doing Science, 2020.") -- new form preserves the slug structure ("Hamming, Art Doing Science, 2020, o three, history of computers hardware") inside a "this lecture is posted as" / "this concludes" frame plus a "Let's begin chapter N, slug" opener.

- START (chapter): `"This lecture is posted as: {base humanized}, {num spoken}, {slug humanized}. Let's begin chapter {N}, {slug humanized}."`
- END (chapter):   `"This concludes chapter {N}, {slug humanized}, which is posted as: {base humanized}, {num spoken}, {slug humanized}."`
- Non-chapter (regular paper) bookend retains the prior `"Today's lecture is posted as: ... We are covering: ..."` and `"And with that we conclude: ..."` form unchanged.

Driven by the new `parse_chapter_key` + `chapter_number_spoken` helpers in `swanki/utils/formatting.py`. No change to the bookend cache file naming or the `text_to_speech` plumbing.

## 2026.05.15 - Postprocessor knobs persisted in chunk_manifest, restitch reads them back

Bug surfaced after the surgical bookend regen earlier today: listener heard "extremely short, unnatural" gaps between chunks on Hamming Ch1. Root cause: `restitch_from_chunks` hardcoded `chunk_crossfade_ms=0` and never forwarded `chunk_pause_ms` / `chunk_tail_trim_ms` / `gain_match_target_dbfs`. When the original `lecture.py` render passed those (700/250/-25.0/50/5000) and the surgical script later called `restitch_from_chunks` to rebuild from new bookends + existing chunks, the boundary-fix bundle was silently dropped, producing back-to-back chunks with zero gap.

Fix: the manifest now records the boundary-fix knobs in a `postprocessor` key at write time (added optional kwarg on `write_chunk_manifest`); `restitch_from_chunks` reads them back and passes them through to `combine_audio_with_section_pauses`. Caller-side overrides on `restitch_from_chunks` (`section_pause_ms`, `bookend_pause_ms` args) still win over the manifest, for ad-hoc tweaks. Older manifests without the field default to `{}` so restitch falls back to legacy zero-gap behavior (matches the prior bug behavior — explicit, not regressed).

Lecture / summary / reading callers updated to pass the dict. Tests cover the regression (chunk_pause_ms=700 in manifest -> 700ms inter-chunk silence in restitched output) and caller-override precedence.

## 2026.05.15 - Content-aware inter-chunk silence (paragraph vs sentence)

User stated design principle: deterministic concat-time silence between chunks (not Fish pause tags) is the safe default — pure mathematical zero, no risk of mic-pickup artifacts inside the gap. But the silence DURATION shouldn't be uniform; it should be sized for the kind of source-text break the gap spans. Bigger gap when the chunker landed at a paragraph boundary (`\n\n`); smaller gap when the chunker had to subdivide a paragraph mid-sentence to stay under `max_chars`.

Three changes:

1. **`chunk_text_paragraphs` returns `list[tuple[str, str]]`** (breaking change to callers). Each tuple is `(chunk_text, boundary_type)` where `boundary_type` describes the PRECEDING gap relative to the previous chunk in the same section: `"paragraph"` (this chunk starts a fresh paragraph) or `"sentence"` (this chunk continues a paragraph that was sub-divided to fit the cap). The first chunk in a section defaults to `"paragraph"` -- the section-level gap is handled separately by `combine_audio_with_section_pauses`'s `section_pause_ms`.

2. **`combine_audio_with_section_pauses` gains two parallel kwargs** (additive, no signature break for legacy callers): `chunk_boundaries: Sequence[list[str]] | None` (per-chunk boundary types parallel to `sections`) and `chunk_pause_ms_by_boundary: dict[str, int] | None` (boundary-keyed silence map). When both are provided, the per-boundary map supersedes the uniform `chunk_pause_ms`. Missing keys fall back to `chunk_pause_ms`. ElevenLabs and other legacy callers pass neither -> uniform behavior preserved.

3. **Manifest persistence:** each chunk dict gains a `boundary` key; `postprocessor.chunk_pause_ms_by_boundary` records the map. `restitch_from_chunks` reads them back so a future surgical regen reproduces the original render's content-aware silences (without this, restitch would default to uniform `chunk_pause_ms` and lose the paragraph-vs-sentence distinction).

Lecture / summary / reading callers updated. Fish YAML defaults: `{paragraph: 1100, sentence: 500}` -- listener can tweak per-paper via the existing per-config override mechanism. The uniform `chunk_pause_ms: 700` stays as the fallback.

## 2026.05.16 - build_bookend_text extracted + chapter form mirrored to summary + reading

User flagged that the chapter-aware bookend rewrite from 2026.05.14 only applied to lecture audio -- summary and reading on chapter inputs fell through to the legacy `START: {humanize_citation_key}.` form which still mis-reads the chapter number ("zero three" instead of "o three"). Hamming's existing summary + reading mp3s on ABS are also pinned to commit ff0567a (Apr 27, before any of the recent fixes), so a re-render is needed regardless.

Two changes:

1. **`build_bookend_text(citation_key, audio_type, position, paper_title=None) -> str`** extracted as a pure function from `generate_bookend_audio`. Pure-function shape makes the text rules unit-testable without a TTS dependency (9 new tests cover all chapter / non-chapter × lecture / summary / reading × start / end combinations).

2. **Chapter branch now fires for `audio_type in ("lecture", "summary", "transcript")`** -- previously only "lecture". Summary and reading get a symmetric "Here is the {audio_type} of chapter N, slug" opener / "the {audio_type} of chapter N, slug" closer subject, framed by the same "This {audio_type} is posted as: ..." / "This concludes ..., which is posted as: ..." wrapper. The internal `audio_type="transcript"` (legacy name for what reading.py passes) renders as the user-facing word "reading" in the spoken text. Non-chapter inputs preserve the legacy forms (lecture: "Today's lecture is posted as: ..."; summary/transcript: "START:/END: ...").

## 2026.05.17 - RC1 section-break sentinel protection + RC4 table linearization

Two feed-forward fixes from the Hamming Ch1 audio plan
([[plan.hamming-chapter-1-audio-two-track-fixes.2026.05.17]]); both make
every future reading/lecture/summary render clean without manual
intervention.

**RC1 -- the spoken "section break" bug.** `expand_acronyms_for_tts` runs
before `split_transcript_by_sections` (an intentional, documented scrubber
order: pronunciation overrides must follow acronym expansion). But
`_STANDALONE_ACRONYM_RE = (?<![A-Za-z])([A-Z]{2,6})(?![A-Za-z])` matched
`BREAK` inside `---SECTION_BREAK---`: the `_` before it satisfies the
lookbehind, the `-` after it the lookahead, and `BREAK` is a 5-letter run
(`SECTION` is 7, so it was spared). The marker became
`---SECTION_B-R-E-A-K---`, which the literal splitter no longer matched, so
it survived into chunk text and Fish spoke "section b-r-e-a-k". Fix: mask
`SECTION_BREAK_MARKER` to an all-lowercase NUL-delimited placeholder
(`_SECTION_BREAK_TTS_MASK`, cannot match the regex, cannot collide with
transcript text) for the duration of the acronym pass, then restore. One
fix site inside `expand_acronyms_for_tts`; reading/lecture/summary all
benefit, and lecture's literal-marker `_strip_duplicate_openers` logic
becomes robust too. Chosen over reordering the pipeline (regression risk
across three audio types) or a marker-tolerant splitter (leaves corruption
in the text for any other consumer).

**RC4 -- truncated tables.** Added an explicit table block to
`_LATEX_SYSTEM_PROMPT` (Pass-1 `humanize_latex`, so linearization happens
before any summarization sees it): read every table row across all columns
as one clause, drop no row or cell, never collapse a row to its label. The
closing "only transform math/units/symbols" constraint was widened so it
no longer contradicts the new table rule.

## 2026.05.18 - Exact chunk-time mapping: shared _accumulate_timeline + sidecar

Re-deriving chunk timing independently drifted ~5s/~11s on Hamming lectures
(the ~11s was the un-counted trailing `bookend_end`+pause; ~5s was
`detect_silence` tail-trim + crossfade rounding). A chunk's mp3 footprint is
content-dependent (the silence-aware `_load` trim) and crossfade overlaps
shorten the timeline, so it is unknowable without loading the files --
prediction is impossible. Fix: one assembly traversal that also yields the
timing.

- `_accumulate_timeline` extracted from `combine_audio_with_section_pauses`:
  performs the identical per-segment ops (gain-match, `_load` trim,
  boundary-keyed gaps, section pauses, bookends, crossfade) and returns
  `(combined, ChunkTimeline)` with offsets read off the running `combined`
  object -- exact by construction. `combine` is now a thin wrapper (single
  export site) returning the `ChunkTimeline`; byte-identical to before
  (verified by a determinism test + an independent-oracle test that recomputes
  offsets from the loaded segment lengths and matches exactly).
- `restitch_from_chunks` captures that measured timeline, stamps the
  manifest-true `index`/`audio_type`, and writes a frozen-pydantic
  `chunk_timeline.json` sidecar next to the manifest. `_manifest_combine_inputs`
  factored out so restitch and the query fallback share one manifest->combine
  translation.
- Public query API (exported from `swanki/audio/__init__.py`):
  `chunk_time_window(source, audio_type, idx, *, absolute_offset_ms=0)`,
  `time_to_chunk(...)` (inverse; nearest chunk for a gap position),
  `chunk_time_window_abs(..., preceding_chapter_durations_ms=...)` for
  ABS-stitched audiobooks. All read the sidecar (recompute via the SAME
  accumulator if missing -- never an independent re-derivation) and assert
  `audio_type` (chunk indices are audio-type-local). Frozen constants
  (`tail_buffer_ms=350`, gain target, paragraph=1100/sentence=500) untouched.

## 2026.05.19 - Bookend "Chapter N" rendering via SHORTHAND_EXPANSIONS

User flagged the bookend's chapter-number rendering as imprecise: the chapter
form (landed earlier today as the simple "This {type} is posted as ...
Let's Begin." frame) routed `chapter_number_spoken("07")` -> "o seven" into
the context_key, so Fish read "...o seven, artificial intelligence two...".
"o seven" is the citation-key style spoken form (matches the written "07")
but the bookend reads better as **"Chapter 7"** -- explicit chapter label,
no leading-zero phonetics, Fish reads the integer naturally as "chapter
seven".

Single-line change in the chapter branch of `build_bookend_text`: replaced
`num_spoken = chapter_number_spoken(num_str)` with
`num_spoken = f"{SHORTHAND_EXPANSIONS['CH']} {int(num_str)}"`. The literal
"Chapter" word comes from the new canonical dict in
[[swanki.utils.formatting]] so future callers ride the same source of truth.
`chapter_number_spoken` stays invariant -- it returns "o seven" for legacy
callers (per-card audio prefix, sync log, etc.); the bookend is the only
spot that needed the cleaner form. A regression-guard test asserts
`"Chapter 3" in out` and `"o three" not in out` so a future revert is
caught immediately. Combined with the 2026.05.19a `humanize_chapter_slug_spoken`
roman-numeral fix, ch07 reads cleanly: *"This lecture is posted as Hamming,
Art Doing Science, 2020, Chapter 7, artificial intelligence two. Let's Begin."*

## 2026-05-21 — Fish Speech port list is env-configurable

`_FISH_SPEECH_PORTS` now derives from `SWANKI_FISH_PORTS` (default `8080,8081,8082`), dropping `8083` so GPU 3 can be reserved for MinerU OCR (`scripts/free-gpu-for-mineru.sh`). Discovery already tolerates missing ports via try/except; restoring the 4th Fish server is a matter of setting `SWANKI_FISH_PORTS=8080,8081,8082,8083`. See [[plan.transition-ocr-to-mineru-dual-path.2026.05.19]].

## 2026.05.22 - `humanize_latex` self-heals chunk-level collapse

New helper `_humanize_chunk_with_completeness` wraps each Pass-1 chunk in a
per-chunk completeness check: if the LLM output's token count drops below
`_HUMANIZE_CHUNK_MIN_RATIO=0.5` of the input, retries up to
`_CHUNK_RETRY_ATTEMPTS=3` times with a stricter "do not drop prose"
addendum, then falls back to the raw input chunk so source content always
reaches Pass-2. Replaces the prior all-or-nothing empty-output fallback
that let the Hamming Ch1 240-char stub slip through. The 0.5 floor allows
legitimate math-heavy compression (`$\alpha$` → "alpha" is ~50%) while
catching catastrophic collapse (Hamming Ch1 was 0.0075).

`text_agent` is now imported at module level (was previously imported
inside `humanize_latex`'s body), matching `card.py`/`summary.py`/
`lecture.py`/`reading.py` and giving mock-patching consistent behavior.

See [[swanki.audio.reading]] (2026.05.22) for the matching Pass-2
self-healing in `reading.py` and the removal of the paper-level
`_READING_COVERAGE_MIN_RATIO` hard-fail.

## 2026.05.25 - Default Fish port probe list back to 4 ports (auto-use all GPUs)

Reversed the 2026-05-21 exclusion of port 8083. The discovery code at
`_discover_fish_speech_servers` already health-checks each port and tolerates
missing servers, so the right behavior is to probe one port per GPU and let
discovery decide which are alive -- not to hardcode-exclude a port "for
MinerU" when MinerU sits idle for ~99% of each paper's runtime.

Trade-off accepted: when MinerU runs its ~30-60s OCR pass at paper start,
fish-3 contends with it on GPU 3. For the next ~3h of audio generation
(complementary cards, summary, reading, lecture), fish-3 has full use of
GPU 3. Net: ~30-60s contention buys ~3h of extra TTS capacity per paper.

User flagged the prior design as too low-level: capacity should follow
GPU count via probing, not be configured via env var.
`SWANKI_FISH_PORTS` remains as an override for >4-GPU machines.

## 2026.05.27 - `filter_metadata` two-tier skip logic + biosec retry on humanize_latex

Two related fixes after the swansonVirtualLabAI2025 reading came out at 24
seconds despite the per-chunk completeness fix logging "87.9% / 0 fallbacks":

**1. `filter_metadata` was stripping 99.9% of Nature-style papers.** The
prior implementation lumped section-level patterns (References,
Acknowledgments) and line-level patterns (DOI URL, e-mail) into one
`skip_patterns` list and triggered persistent skip-mode on any match.
swansonVirtualLabAI2025's page-1 line 2 was just `https://doi.org/...` —
the URL pattern caught it, set `skip_mode = True`, and skip-mode never
exited because Nature OCR uses H1 (`# Article`, `# Discussion`) for body
sections and the exit check was `line.startswith("##")` (H2 only). Result:
74,426 chars of source → 65 chars of filtered output (just the title).

Split into two lists:
- `section_skip_patterns` -- enter *persistent* skip-mode (References,
  Competing interests, Author block, Acknowledgments, bibliography entries,
  `\\author{`, `\\end{document}`).
- `line_skip_patterns` -- skip ONLY the matched line, no state (DOI URL,
  e-mail, "Published online:", `\\title{`). These were the ones that
  shouldn't drag the rest of the doc into skip-mode.

Also broadened the skip-mode exit from `startswith("##")` to
`startswith("#")` so Nature-style H1 body headings bring it back off.

Re-test results: swanson 0.1%→85.7%, singh 32.1%→90.8%, qu 78.9%→97.6%,
aygun 100%→100%, hu/fernandez each ≥99.5% kept. No regressions.

**2. `humanize_latex` chunks now wrap their `text_agent.run_sync` call in
`with_safety_retry`** (from [[swanki.llm.safety]]). qu died at exactly
this call last night despite all other biosec-prone agents being wrapped
in the 2026.05.24 commit. `text_agent` was the last unprotected gate in
the reading pipeline. Re-raises after preamble retries are exhausted --
the chunk-level token-ratio fallback below only engages on legit short
outputs, not biosec refusals (those mean the content itself is
unrenderable as audio, not under-tokenized).

See [[swanki.audio.reading]] (2026.05.27) for the matching Pass-2 wrap
and the implication chain (filter_metadata bug → tiny input → tiny
transcript → 24s reading audio).

## 2026.05.29 - `verbalize_bit_strings` pipeline-wide TTS scrubber

Hamming chapter 10 (coding theory) is built around codewords written as bare
binary strings ("11", "0110", "1011010"). The TTS path had no rule for
isolated binary tokens, so every engine read them as cardinals: "11" → "eleven",
"0110" → "one hundred ten". Annotation review found 8/21 lecture chunks and
18/43 reading chunks in ch10 corrupted this way. The fix is a deterministic
pre-TTS scrubber, `verbalize_bit_strings(text, max_len=32)`, that rewrites
isolated binary tokens into hyphenated digit-words ("110" → "one-one-zero")
so the engine reads each digit separately. Plan:
[[plan.bit-string-verbalizer-hamming-annotations.2026.05.29]].

Design:

- **Regex** `(?<![A-Za-z0-9_/:])(?<!\d[.,])[01]{2,max_len}(?![A-Za-z0-9_/:])(?![.,]\d)`.
  The min length 2 leaves bare single "0"/"1" alone. The boundary tests reject
  *number-continuation* punctuation only -- a digit abutting `.`/`,` -- so
  decimals (`1.5`, `0.01`), thousands-commas (`1,000`), years (`2020` has a
  non-binary digit), identifiers (`v01`, `chunk0`), paths/times (`a/01`,
  `10:01`) are protected, while a codeword followed by *sentence* punctuation
  (`"as 0, 00, 01, and 11."`) still verbalizes. This is the key deviation from
  the plan's literal flat-exclusion regex, which would have skipped every
  codeword followed by a comma -- i.e. the actual ch10 case. Idempotent: the
  emitted digit-words contain no binary run, so a second pass is a no-op
  (verified on the real ch10 transcript).

- **Placement**: in all four audio-module scrubber chains
  (lecture/reading/summary/card), AFTER acronym expansion and BEFORE
  pronunciation overrides. The passes are orthogonal (`expand_acronyms_for_tts`
  only matches `[A-Z]{2,6}` letters, never digits); placing it before
  pronunciations preserves the "overrides win last" invariant.

- **Gating**: provider-agnostic, on the toggle only (NOT `is_fish_for_prep`).
  Binary-as-cardinal is wrong on Fish and ElevenLabs alike. Default-on via
  `prep_cfg.get("verbalize_bit_strings", True)` so it fires even where the
  `preprocessor:` block is absent (elevenlabs `default.yaml`). The
  `fish_speech.yaml` keys (`verbalize_bit_strings`, `bit_strings_max_len`)
  mirror the in-code defaults; they document, not activate. Disable per-paper
  with `verbalize_bit_strings: false` in a `fish_speech_<paper>.yaml`.

- **`SECTION_BREAK_MARKER`** needs no masking (unlike the acronym pass): the
  marker is uppercase letters + hyphens with no binary run, so the lookarounds
  already protect it.

- **Prompt addenda** (belt-and-suspenders): lecture rule 17 in
  `default.yaml` `lecture_system`; reading rule 10 in the hardcoded
  `system_prompt` in [[swanki.audio.reading]] (no `reading_system` key exists
  in the YAML, so the request's "addendum in default.yaml" lands in
  `reading.py` for reading). Both instruct the LLM to read codewords
  digit-by-digit; the deterministic scrubber is the real guarantee.

Dry-run on the real ch10 lecture transcript rewrote 5 codeword lines
correctly (e.g. "0, 10, 110, and 111" → "0, one-zero, one-one-zero, and
one-one-one", bare "0" preserved), touched no decimal/year/identifier, and
was idempotent.

Follow-up (post-merge, from `main`): Hamming ch1-10 annotation review --
ch1-9 surgical edits via `/audio-fix-from-annotations`, ch10 full audio
regen (now that the verbalizer is present) with the ABS bookmark
clear-and-remark step. See the plan note Part B.

## 2026.05.30 - Extract public `preprocess_for_tts` (single scrubber-chain source)

`preprocess_for_tts(text, tts_kwargs, *, add_pauses, clean_markdown=True)` is
now the one definition of the deterministic pre-TTS scrubber order:
optional `clean_markdown_for_tts` -> `strip_chapter_filename_slug` ->
`expand_acronyms_for_tts` (fish) -> `verbalize_bit_strings` ->
`apply_pronunciation_overrides` -> `strip_forbidden_fish_tags` (fish) ->
optional `add_tts_pauses`. `card.py`'s private `_preprocess_for_tts` now
delegates with `add_pauses=False, clean_markdown=False`; the new
[[swanki.audio.comment_edit]] calls it with `add_pauses=True`. The `add_pauses`
flag is load-bearing because `add_tts_pauses` is NOT idempotent -- it must run
once on fresh prose and never on already-paused stored chunk text. lecture/
reading/summary still inline the chain; folding them onto this helper is a
recommended follow-up. Plan:
[[plan.swanki-comment-driven-chunk-edits.2026.05.30]].

## 2026.05.30 - Asymmetric bookend pauses (split + persist on restitch)

Replaced the single `bookend_pause_ms` (500, used for both the after-start and
before-end gaps, no trailing silence) with three knobs in
`combine_audio_with_section_pauses` / `_accumulate_timeline`:
`bookend_start_pause_ms` (300, front plays in fast), `bookend_end_pause_ms`
(2000, distinct break before the end bookend), and a NEW
`bookend_trailing_pause_ms` (1500, silence AFTER the end bookend, gated on an
end bookend existing). Driven by Hamming ABS lecture comments 53.6m/65.6m/75.9m
(autoplay needs a clear chapter break). Plan:
[[plan.audio-bookend-pauses-conceptual-prompt.2026.05.30]].

`restitch_from_chunks` gains the 3 override params and PERSISTS any provided
override into the manifest's postprocessor block, so later surgical /
[[swanki.audio.comment_edit]] restitches inherit the new pauses (they read the
manifest, not the caller args). Precedence: override > manifest key > global
default. Backward-compatible: old manifests (no bookend keys) resolve to the
global defaults via `.get(key, default)` everywhere, so existing-paper
restitches don't crash (regression test:
`test_restitch_old_manifest_without_bookend_keys_uses_defaults`). The second
`_accumulate_timeline` caller (the `_ensure_timeline` recompute fallback) was
updated in lockstep. Globals live in `fish_speech.yaml` postprocessor; all
three audio types (lecture/reading/summary) read+forward+persist them.

## 2026.06.02 - Roman-numeral guard in expand_acronyms_for_tts

Fish read "World War II" as "one one". Root cause was NOT `verbalize_bit_strings` (matches `[01]` digits only — Hamming codewords stay safe) but `expand_acronyms_for_tts`: its `_STANDALONE_ACRONYM_RE = [A-Z]{2,6}` letter-spells any uppercase run, so `II` -> `I-I` exactly like `MIT` -> `M-I-T`. Confirmed in Hamming ch1/ch3 lecture cleaned markdown ("World War I-I").

Fix: a `_ROMAN_NUMERAL_WORDS` map (`II`->"two", `III`->"three", `VII`..`XX`); `_sub` returns the cardinal word for those tokens instead of letter-spelling. The keys are I/V/X-only, so real initialisms needing letter-spelling (`MD`, `CV`, `DC`, `MC`, `CI`, `MM`, ...) are absent and unchanged. `IV` (intravenous) and `VI` (the vi editor) are deliberately EXCLUDED — they collide with initialisms and keep letter-spelling, so there is NO regression for them. Single-letter `I`/`V`/`X` never reach the expander (its floor is 2 letters). Catches "World War II/III", "Part VII", "Henry VIII", "Chapter IX", "Section XV" pipeline-wide. Distinct from `humanize_chapter_slug_spoken` (`swanki.utils.formatting`), which only handles trailing Roman tokens in chapter-slug bookends, not body prose. Tests in `tests/test_audio_common.py` (`test_expand_acronyms_for_tts_roman_numerals_become_words` + ambiguous/acronym/codeword guards). Plan: [[plan.verbalizer-roman-numeral-guard.2026.06.02]].

## 2026.06.06 - Balanced chunker + per-chunk onset fade (fish opt-in)

`chunk_text_paragraphs` gains two keyword-only params: `soft_max_chars: int |
None = None` and `min_sentences_per_chunk: int = 1`. When `soft_max_chars` is
`None` (every non-fish caller -- reading/summary/elevenlabs and the existing
tests) the legacy greedy packer runs unchanged and output is byte-identical;
when set, dispatch goes to a new `_chunk_balanced`. The balanced path splits
each over-soft paragraph into `ceil(char_len / soft_max_chars)` near-equal
sentence groups (`_balanced_sentence_groups`, greedy against `total/k` with a
15% overshoot tolerance), packs units toward the soft target (lifting an
undersized current chunk up to the hard `max_chars` cap when the next unit
fits), then enforces the min-sentence invariant by merging any lone-sentence
chunk into its SMALLER adjacent neighbor that still fits the cap, else the
larger, else accepting it lone (a paragraph-of-one at a section edge, or a
single sentence too long to merge -- the safe long survivor). Boundary typing:
the first group of a split paragraph keeps `"paragraph"`, the rest are
`"sentence"` (preserves the 500ms mid-paragraph gap vs the 1100ms paragraph
gap); a merge follows the EARLIER chunk's boundary, so the first chunk stays
`"paragraph"`. Units join with `"\n\n"`, sentences within a unit with `" "` --
matching legacy join semantics, so the manifest `text` and inter-chunk pacing
are consistent. The motivation is Fish's per-chunk prosodic arc (hard onset ->
settle -> fast/monotone tail), which turns "musical" at seams under
single-sentence chunks (uptone on a declarative) and high size variance.

Why balanced-from-paragraphs rather than a post-pass on the greedy output (the
plan's framing): it directly reproduces the validated S8 sweep and the non-fish
risk is fully contained by the `soft_max_chars is None` gate, so there is no
upside to threading a second pass through the greedy list. Validated text-only
over Hamming CH01-10 with the SHIPPED code (reconstructing each section from the
live manifests): old (`max_chars=700`) -> new (`soft=500, cap=650, min2`) moves
mean 515->423, median 547->408, stdev 146->95, max 700->650, single-sentence
13->1 (the survivor is the safe ~280-char long sentence); CH04 the worst,
single-sentence 5->0, stdev 185->91. Numbers match the plan's S8 target
(295/423/95/1).

Onset fade: `_accumulate_timeline` / `combine_audio_with_section_pauses` /
`restitch_from_chunks` / `_ensure_timeline` gain a `chunk_onset_fade_ms: int =
0` param. In the `_load` closure a `seg.fade_in(chunk_onset_fade_ms)` is applied
AFTER `_gain_match` (so it shapes final levels) and before the
`append(crossfade=...)`. At Fish's 44.1kHz, 25ms ~= 1102 samples -- rounds the
hard onset without dulling the re-attack. 0 = off keeps non-fish byte-identical.
`restitch_from_chunks`/`_ensure_timeline` read it back from the manifest
postprocessor so surgical restitches inherit it. KNOWN open item: the 25ms
fade_in overlaps the 50ms `append` crossfade region -- a mild double-attenuation
at the seam that needs a listen-check before broad audio rollout (text A/B does
not exercise it). Config knobs (`soft_max_chars: 500`, `min_sentences_per_chunk:
2`, `chunk_onset_fade_ms: 25`, `max_chars: 700->650`) live in `fish_speech.yaml`
and the three voice-clone variants (hamming/bechtel/audrey). Plan:
[[plan.smarter-lecture-tts-chunking.2026.06.06]].

## 2026.06.06 — single-port discovery for SLURM serverless Fish

Documented (no behavior change needed) that `SWANKI_FISH_PORTS` already collapses
to one server when set to a single port. Under the SLURM per-job model
([[scripts.swanki_job]]) each job brings up one Fish on a job-private host port and
exports `SWANKI_FISH_PORTS=<that port>`, so `_discover_fish_speech_servers`
probes only that one server -- no probing of the legacy 8080-8083 fleet. The job
waits on `/v1/health` before any TTS, so the single server is up by first call.
Covered by `tests/test_audio_fish_port_resolution.py`. Part of
[[plan.slurm-native-serverless-fish.2026.06.06]].

## 2026.06.06 - Demote `verbalize_bit_strings` to per-paper opt-in (default off)

ABS bookmarks on Kuchel ch01 and non-coding Hamming chapters surfaced the scrubber
mangling ordinary decimals: "10 and 100" garbled, "100" digit-spelled and spammed. Root
cause is structural — the `[01]{2,32}` pattern cannot tell a binary codeword from a
decimal made only of 0/1 digits (`10`, `100`, `1000`, `11`), and it ran as an unbounded
global `re.sub` **default-on** at all four call sites (`prep_cfg.get(..., True)`).

Flipped the `preprocess_for_tts` call-site default (`:144`) and the lecture/reading/summary
call sites to `False`. The function body and regex are unchanged; the key stays live so a
dense-codeword source re-enables it via `verbalize_bit_strings: true` in a
`fish_speech_<paper>.yaml`. Decisive evidence: a byte diff of Hamming CH10 (`coding-theory-i`)
raw LLM transcript vs the post-scrubber transcript is identical with zero bare `[01]{2,}`
tokens — the LLM already emits word-form codewords from the prompt rule alone, so the
scrubber was a no-op on the one chapter it exists for. Default-off therefore carries zero
demonstrated CH10 regression while stopping the false positives everywhere else. Rejected
cue-gating (window brittleness, test churn, no-op on CH10 anyway). See
[[plan.scope-binary-codeword-tts.2026.06.06]]; scrubber origin was `#18`
([[plan.bit-string-verbalizer-hamming-annotations.2026.05.29]]).

## 2026.06.07 - ensure_fish_speech_reference honors dynamic Fish port (SLURM fix)

`ensure_fish_speech_reference` dialed the raw `server_url` (default
`http://localhost:8080`) for `/v1/references/list` and `/v1/references/add`,
bypassing `_discover_fish_speech_servers`. Under the SLURM-native serverless
Fish (PR #38, `e9c6a48`) each job's Fish listens on a dynamic
`SWANKI_FISH_PORTS` port (e.g. 8148), not 8080, so the reference call was
refused with `[Errno 111] Connection refused` BEFORE any TTS -- the TTS path
worked because it goes through `_pick_fish_speech_server` ->
`_discover_fish_speech_servers`, but the reference path did not. Fix: resolve
`server_url = _discover_fish_speech_servers(server_url)[0]` at the top of the
function, exactly like the TTS path. `_discover` falls back to `[server_url]`
when nothing else is healthy, so local 8080 runs are byte-identical. Validated:
CH01 SLURM canary (job 851) went from dying at ~2.5 min to COMPLETED, 27-chunk
lecture rendered. Bug owned by the SLURM session (PR #38); landed here per their
greenlight. Separately observed: per-job Fish runs uncompiled (COMPILE=0) at
~3.6 tok/s -> ~1.3 h/chapter; `SWANKI_FISH_COMPILE=1` is the lever under test.

## 2026.06.08 - Resilient Fish TTS client (retry + re-discover)

`_tts_fish_speech` now retries the `/v1/tts` POST up to `_FISH_TTS_MAX_ATTEMPTS`
(env `SWANKI_FISH_TTS_ATTEMPTS`, default 4) with backoff (2/5/15/30s), forcing
`_discover_fish_speech_servers(..., force=True)` between attempts so a server
that restarted on its port is re-found. Catches `httpx.HTTPError` (covers
`RemoteProtocolError` "Server disconnected" + `ConnectError` + transient 5xx);
only a genuine repeated failure raises.

Motivation: in the concurrent Hamming CH02-CH10 SLURM batch, 6/9 jobs failed
late (~chunk 30 of 32) with `RemoteProtocolError: Server disconnected` -- the
per-job Fish dropped the TTS connection mid-generation and the client had ZERO
retry, so one blip killed a 70-minute run. Ruled out: GPU collision (fixed),
host/cgroup RAM (MaxRSS ~16G, no OOM-killer in dmesg), clean CUDA OOM (no
`torch.OutOfMemoryError` logged), GPU Xid, disk-full, timeout. The retry is also
the diagnostic: if it recovers, Fish was alive (transient drop); if it can't
reconnect, Fish truly died and `swanki_job.sbatch` needs a restart-supervisor
(layer 2). Architecture decision: keep the HTTP/server boundary (env isolation
local; portable to cloud/hosted Fish) and harden the client -- retry/backoff is
exactly what a future cloud endpoint needs too. Plan discussion in-session
2026.06.08; pairs with the SLURM serverless work (PR #38/#40).

## 2026.06.09 - Mixed pause-tag stacks collapse (the stacked-marker bug)

`add_tts_pauses` (fish path) stacked `[short pause]` against `[pause]` at every
intra-chunk paragraph break ending in a period: the paragraph rule inserts
`[pause]`, then the sentence rule fires on the same boundary, and the old
collapse regexes only deduped SAME-type runs. Fish renders every tag (the
`[pause]` one as an audible breath -- the artifact `chunk_tail_trim_ms` exists
to clip at chunk ends), so each surviving stack was a mid-chunk pause+breath
artifact. Found via a CH03 review comment; 28 stacks existed across the live
Hamming chapters (CH07 alone had 10).

- New `collapse_stacked_pause_tags`: any run of >=2 adjacent pause tags keeps
  its strongest tag (`[long pause]` > `[pause]` > `[short pause]`). Runs as the
  final step of `add_tts_pauses` and is exported for the remediation mode in
  [[scripts.swanki_audio_edit]].
- The generation prompts (default.yaml + book_voice.yaml section 12) now also
  instruct the LLM to never place two pause tags adjacent, so stacks are
  guarded at both layers.
- `add_tts_pauses` remains non-idempotent overall (the every-3-sentences
  injector shifts on re-runs) -- the preprocess-once invariant stands.

## 2026.06.09 - `write_chunk_manifest` records the gen `speed`

Added a `speed` field to the chunk manifest, threaded from `generate_{lecture,reading,
summary}_audio` (each already had `speed` in scope). It is the source of truth a later
surgical edit uses to re-TTS the replacement chunk at the SAME speed instead of guessing
(see [[swanki.audio.comment_edit]], same date). `None` when a caller omits it; legacy
manifests without the field fall back to `edit_chunk`'s per-audio-type map.

## 2026.07.20 - `verbalize_large_numbers`: spell big cardinals out for TTS

Second listener report of the same defect. A jakobson ABS bookmark at 7:27
(2026-07-09) said "a lot of the numbers being read off are botched, especially
the larger numbers" — 851, 1,225, 826, 6400, 6476, 923, 1200, 1000 — and it was
patched by hand that evening with four `edit_chunk` calls. The Kuchel CH05
reading track needed the same repair across 26 chunks. Regenerating the
jakobson lecture reproduced it immediately (15 numerals across 8 of 64 chunks),
which is the signal that this belongs in the pipeline, not in a runbook.

`verbalize_large_numbers(text, min_value=100)` rewrites bare integers as cardinal
words via a local `_cardinal_words` helper (no new dependency; `num2words` is not
in the env). It is **opt-out, default on**, which is a deliberate departure from
`verbalize_bit_strings` sitting right above it in the chain. That one imposes
per-digit semantics and genuinely cannot tell a codeword from a decimal, so it
had to be demoted to opt-in (2026.06.06). Spelling a cardinal out is
meaning-preserving, so it carries no equivalent risk.

Guards, all covered by tests:

- Numbers below `min_value` are left as numerals — engines read 1..99 correctly
  and the numeral is easier to proofread in the saved transcript.
- Bare four-digit numbers in 1500-2099 are skipped as year-like; TTS already
  says "twenty twenty-five", which "two thousand twenty-five" would replace.
- Comma-grouped numbers are always spelled out regardless of magnitude — the
  comma is itself a mis-read risk.
- The regex refuses identifiers (`ERG11`), decimals (`1.5`), times (`10:30`),
  hyphenated ranges (`Fig. 5-11`), and digit-suffixed words (`1990s`).
- Idempotent: the output contains no digits.

Ordering matters and is asserted by
`test_preprocess_for_tts_bit_strings_win_over_large_numbers`: the scrubber runs
directly AFTER `verbalize_bit_strings`, so on a dense-codeword paper (Hamming)
`110` has already become `one-one-zero` and cannot be re-read as "one hundred
ten". Wired identically into `preprocess_for_tts` (card path) and the duplicated
chains in `lecture.py`, `reading.py`, and `summary.py`. Knob documented in
`swanki/conf/models/fish_speech.yaml` as `verbalize_large_numbers` /
`large_number_min`.

Two `preprocess_for_tts` tests that asserted on `110` were switched to the
sub-100 codeword `11` so they still test bit-string opt-in without the new
default-on scrubber confounding them.
