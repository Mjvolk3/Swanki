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
