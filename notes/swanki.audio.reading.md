---
id: adeac28210904270923c96e
title: Reading
desc: ''
updated: 1773142603440
created: 1773142603440
---

## 2026.03.10 - Full document reading with two-pass LLM processing

Extracted from monolithic audio module. Uses a two-pass approach: (1) `_humanize_latex` converts all LaTeX to natural text in 8000-token chunks, (2) LLM generates reading-optimized transcript in 3000-token chunks. Audio is chunked at a stricter 2000-char limit for quality.

## 2026.03.12 - Migrate from OpenAI client to pydantic-ai agents

Replaced direct `OpenAI` client calls with shared `text_agent` from `swanki.llm.agents` in both `generate_reading_audio` and `_humanize_latex`. Removed `openai_client` parameter -- functions now accept `model: str` in pydantic-ai format. Manual retry loops replaced by agent-level `retries=3`. Part of Step 5 ([[plan.major-refactor-sequence.plan-0]]).

## 2026.03.13 - Section-aware assembly, metadata filtering, no-filler pauses, bookends, acronyms

Addresses issues heard in merzbacher paper audio: university addresses and dates read aloud, filler text between sections instead of silence, no bookend announcements, and inconsistent acronym expansion.

- **Metadata filtering**: `filter_metadata()` now applied to content before LLM processing, stripping affiliations, emails, "Received/Accepted/Published" dates, and references
- **No-filler section breaks**: Replaced SSML `<break time="2.0s"/>` with `---SECTION_BREAK---` markers; prompt explicitly forbids filler text or transitions between sections
- **Figure handling**: New prompt instruction to announce figures with pause/`Figure X`/pause/description pattern instead of skipping them
- **Section-aware assembly**: Replaced flat `combine_audio` with `combine_audio_with_section_pauses` for real silence between sections
- **Bookends**: Generates START/END citation key announcements via `generate_bookend_audio`
- **Acronyms**: `extract_acronyms()` scans source text and injects definitions into the LLM prompt

## 2026.03.15 - Flash TTS model and SSML pause injection

Switched from `eleven_multilingual_v2` (1 credit/char) to `eleven_flash_v2_5` (0.5x credits, 40k char limit) for reading audio -- quality is sufficient for straight readings and costs half as much. Added `add_tts_pauses()` after `clean_markdown_for_tts()` to insert SSML `<break>` tags at paragraph boundaries for natural pacing.

## 2026.04.03 - Fish Speech tts_kwargs passthrough and provider-aware pauses

Added `**tts_kwargs` parameter to `generate_reading_audio()` for Fish Speech provider support. All `text_to_speech()`, `generate_bookend_audio()`, and `add_tts_pauses()` calls now forward provider info. Pause insertion uses `[pause]`/`[short pause]` tags for Fish Speech instead of SSML `<break>`.
- **Paragraph-only chunking for Fish Speech**: Switches to `chunk_text_paragraphs()` with 2000 char max when using Fish Speech to avoid mid-sentence audio truncation. Section pauses increased to 3s.

## 2026.04.15 - Parallel chunk dispatch across Fish Speech servers

Reading audio now flattens chunks across all sections into one job list and dispatches via `tts_chunks_parallel()` when Fish Speech is the provider, then regroups paths by section index for the section-paused combine step. Same pattern as lecture/summary so a multi-server deployment processes a paper's audio concurrently.

## 2026.04.16 - Reading chunks retained in `reading_chunks/` with manifest

Reading audio chunks now live under `reading_chunks/` and are kept after combination, paired with a `chunk_manifest.json` so a single bad chunk can be re-TTS'd and the reading restitched via `restitch_from_chunks()`. Same shape as lecture and summary -- consistency of the chunks-plus-manifest layout across audio types is the point.

- Each chunk gets `append_chunk_pause(text, provider)` before TTS so direct concatenation (no crossfade) sounds seamless.
- Bookends are written into `reading_chunks/`, co-located with the chunks they bracket.
- `combine_audio_with_section_pauses()` is invoked with `chunk_crossfade_ms=0` explicitly. The cleanup `unlink()` block is gone.

## 2026.04.17 - Consolidate humanization; caption, citation, acronym, and transition rules

Orange annotations on the zvyagin reading audio surfaced a cluster of pipeline defects: LaTeX dollar signs leaking through, figure titles clipped mid-read, image URLs being read aloud, acronyms expanded twice, "et al" pronounced verbatim, and filler "uh" sounds at section starts. Fixes target each category, plus a deduplication of the LaTeX humanization path so reading and card audio share one prompt.

- **Single humanization source**: Removed local `_LATEX_SYSTEM_PROMPT` + `_humanize_latex` (~80 lines of duplicated code). Reading now imports `humanize_latex` from `_common`, so prompt improvements for one audio type automatically benefit the others. `test_audio_reading::test_humanize_latex` patches the `_common.text_agent` import path now.
- **Figure/Table captions read as atomic blocks**: Rule 3 rewritten. Reader inserts three section breaks around each figure/table — one before "Figure N", one between "Figure N" and the caption body, one after the caption. Reads the ENTIRE caption (title AND description) as one continuous block. Explicit ban on reading image URLs, mathpix links, or alt-text markers (which were being narrated verbatim on the zvyagin run).
- **Acronym repeat-expansion ban**: Rule 2 tightened. Expand ONCE on first occurrence, then use the acronym alone. Extracted acronym map in the prompt reinforces "expand each ONCE". Prevents "Artificial Intelligence" and "BERT" from being defined twice in the same document.
- **Citation format**: New rule 5. Author-year only; drop "et al" entirely. `Greaney et al. (2021)` → `Greaney, 2021`. Multiple citations: `Greaney, 2021; Zost, 2020; Ju, 2020`.
- **No filler at section starts**: Rule 4 explicitly forbids "uh", "um", "ah" or any vocalized non-word at the beginning of a section, and reiterates the `[pause]` marker ban.
- **`model: str` required**: Same treatment as card/lecture/summary — no hardcoded `gpt-5-mini` fallback; caller must pass config LLM.

## 2026.05.14 - Mirror lecture.py audio fixes for consistency across types

Same wiring as `swanki/audio/summary.py` 2026.05.14 — pre-TTS scrubber pipeline, YAML-driven `chunking.max_chars`, and YAML-driven `postprocessor.*` knobs piped through to `combine_audio_with_section_pauses`. Reading audio now picks up the boundary-fix bundle (gain match, inter-chunk silence, tail trim, crossfade) and the deterministic acronym / pronunciation / forbidden-tag scrubbers that landed for lecture in the Hamming PR. Defaults preserve prior behavior for elevenlabs callers.

## 2026.05.17 - RC2 completeness guard + RC3 prosody addendum

From the Hamming Ch1 audio plan
([[plan.hamming-chapter-1-audio-two-track-fixes.2026.05.17]]).

**RC2 -- silent Pass-2 drops.** Pass-2 (audio-optimization LLM) dropped a
source sentence in Hamming Ch1 with no detection. Added
`reading_coverage_ratio(source, transcript)` -- a pure, tiktoken-based
token-count ratio extracted as a module function for unit-testability (cf.
`build_bookend_text`) -- and a guard after Pass-2 that compares the
transcript against the *post-humanize* Pass-1 text (not raw LaTeX, so
equation rewrites are not miscounted) and emits a loud `logging.warning`
when coverage `< _READING_COVERAGE_MIN_RATIO` (0.95). No auto-retry: Pass-2
only ever expands text, so a shortfall is a real omission; fail loud and
let the user decide (CLAUDE.md fast-fail).

**RC3 -- flat aphorism delivery.** Optional per-paper
`preprocessor.system_prompt_addendum` (carried through the existing
`tts_kwargs["preprocessor"]` pass-through, so no pipeline plumbing change
and papers without the key are unaffected) is appended verbatim to the
Pass-2 system prompt. Reading-only by design: it does not touch the lecture
critic/refiner first-person book-voice whitelist. The Hamming addendum
(`swanki/conf/models/fish_speech_hamming.yaml`) instructs aphorism/
punchline isolation as one-sentence paragraphs -- Fish emotion tags are
force-stripped and the prompt forbids literal `[pause]`, so paragraph
placement (which `add_tts_pauses` brackets with real silence) is the only
delivery lever that survives.

## 2026.05.22 - Per-chunk completeness retry replaces the paper-level hard-fail floor

The 0.95 paper-level `_READING_COVERAGE_MIN_RATIO` guard was too coarse:
qiu's reading at 94.2% tripped a hard-fail that aborted the whole paper for
what was likely small natural variance (image-URL stripping + a paragraph
the LLM trimmed). At the same time, the guard's empty-output fallback in
both passes was too narrow -- a Pass-2 chunk returning 70% of its input
slid through silently. The user's directive: "fix the reason for incomplete
readings; there shouldn't be any floor for readings."

Replaced the paper-level guard with two surgical, self-healing per-chunk
checks:

- **Pass-1 (`_humanize_chunk_with_completeness` in `_common.py`)**: per-chunk
  floor `0.5`. Math-heavy chunks legitimately compress
  (`$\alpha + \beta = \gamma$` → "alpha plus beta equals gamma" is ~50%),
  so the floor only catches structural collapse. The Hamming Ch1 disaster
  was 0.0075. Retries up to 3× with a stricter "do not drop prose" addendum;
  if every attempt is below the floor, returns the raw input chunk so
  Pass-2 still sees the source verbatim.
- **Pass-2 (`_pass2_chunk_with_completeness` in `reading.py`)**: per-chunk
  floor `0.85`. Pass-2 only ever expands (acronym first-use, citation
  rendering, SECTION_BREAK markers); a chunk below 0.85 is a real omission
  -- the qiu-class summarization-tendency failure. Same retry+fallback
  shape; fallback returns the humanized input chunk so content survives.

The paper-level `_READING_COVERAGE_MIN_RATIO` constant and its `RuntimeError`
hard-fail are removed. `reading_coverage_ratio()` survives as a pure
diagnostic function; the paper-level ratio is logged at INFO along with a
per-pass fallback count for telemetry.

Tightened Pass-2 prompt rules #8 and #9 -- the two that invited omission --
so the LLM doesn't preemptively "smooth" or de-dupe within a chunk:

- Rule #7: extended with "Every sentence in the input must appear in the
  output; if a sentence feels redundant or off-topic, include it verbatim
  anyway. Omission of any sentence is a failure."
- Rule #8: rewritten from "Make the text flow naturally for listening, not
  reading" to "The source is already prose; do NOT smooth, condense, or
  rephrase to make it 'flow better'. Render exactly what is written."
- Rule #9: scoped to "WITHIN THIS CHUNK ONLY" so the LLM doesn't omit
  sentences it imagines were already covered by earlier chunks it cannot
  see.

`text_agent` lifted to module level in `_common.py` for consistent
mock-patching (matches `card.py`/`summary.py`/`lecture.py`/`reading.py`).

## 2026.05.27 - Pass-2 chunk generation now safety-retry-aware

Mirror of the [[swanki.audio._common]] 2026.05.27 wrap of humanize_latex:
`_pass2_chunk_with_completeness`'s `text_agent.run_sync` is now wrapped in
`with_safety_retry`. Same rationale -- same content that biosec-refuses in
Pass-1 can refuse in Pass-2 (same prompts, same model). The chunk-level
token-ratio retry+fallback below the safety wrap only engages on legit
short outputs; a biosec refusal across all 3 preamble attempts re-raises
because that chunk's content is unrenderable as audio.

Combined with the 2026.05.27 `filter_metadata` fix that prevented Nature
papers from being 99.9%-stripped upstream, qu and swanson should now be
able to land cleanly even though their content (CRISPR / SARS-CoV-2
nanobody) is the most biosec-prone in the iCBF batch.

## 2026.05.29 - Wired `verbalize_bit_strings` + reading prompt addendum

Added the bit-string verbalizer step to the scrubber chain (after acronym
expansion, before pronunciation overrides; provider-agnostic, default-on).
Also added binary-codeword rule 10 to the HARDCODED `system_prompt` string in
this module -- the reading system prompt is not in `default.yaml` (no
`reading_system` key), so the prompt addendum lands here, not in YAML. See
[[swanki.audio._common]] (2026.05.29) for the function and rationale. Plan:
[[plan.bit-string-verbalizer-hamming-annotations.2026.05.29]].
