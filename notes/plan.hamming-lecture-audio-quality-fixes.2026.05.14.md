---
id: p0edbeatip2sddbcgx4ihg9
title: '14'
desc: ''
updated: 1778740554825
created: 1778740554825
---

# Hamming lecture audio-quality fixes

## Context

Between 2026-04-27 and 2026-05-14 the user dropped 33 BookPlayer bookmarks against `Swanki-Book-Lecture/hammingArtDoingScience2020`. The annotations cluster into 12 themes — the dominant complaint (Theme 4) is monotone "droning on" at the tail of long fish-speech chunks, and a NEW theme since the Apr-30 boundary-fix bundle is inter-topic transition abruptness (Theme 12: chapter 2's "space and time" pivot "comes out of nowhere"). The prior boundary-fix bundle (`tail_buffer_ms=350`, `chunk_pause_ms=700`, `chunk_crossfade_ms=50`, `gain_match_target_dbfs=-25.0`) addressed the most aggressive clipping but did not touch chunker shape, post-refine guards beyond duplicate-opener stripping, or pronunciation overrides. This plan fixes all 12 themes without regressing the first-person book voice critic patches landed Apr-30, and without reverting the Apr-26 `[long pause]` -> `[pause]` change that solved the audible-breath artifact.

It also corrects two unit tests on `main` (`tests/test_audio_common.py:351,375`) that have been wrong since 2026-04-26: they assert `[long pause]` against a production helper that now emits `[pause]`. Production stays; the tests change.

No kanban issue is associated with this work.

## Relevant Files

| Path | Purpose | Tag |
|------|---------|-----|
| `swanki/audio/_common.py` | Chunker (`chunk_text_paragraphs`), `append_chunk_pause`, `combine_audio_with_section_pauses` (tail-buffer constant at line 830), `_normalize_fish_speech_punct`, post-refine scrubbers | MODIFY |
| `swanki/audio/lecture.py` | Lecture writer + critic + refine loop, `_strip_duplicate_openers` (line 117) — the precedent for new deterministic guards | MODIFY |
| `swanki/audio/summary.py` | Summary audio path; shares `_common` chunker/post-refine layer | REFERENCE |
| `swanki/audio/reading.py` | Reading audio path; same shared layer | REFERENCE |
| `swanki/audio/card.py` | Per-card audio; pronunciation overrides apply via shared TTS path | REFERENCE |
| `swanki/models/cards.py` | `LectureTranscriptFeedback` (line 1352) — extend with `bridge_quality` and `repeated_phrase` dimensions | MODIFY |
| `swanki/utils/formatting.py` | `humanize_citation_key` (line 184) — extend to absorb chapter slugs (`*_03_history-of-computers-hardware` -> "Chapter three, history of computers and hardware") | MODIFY |
| `swanki/conf/models/fish_speech.yaml` | Base fish-speech config; add nested `tts.{preprocessor,chunking,postprocessor}` sub-trees | MODIFY |
| `swanki/conf/models/fish_speech_hamming.yaml` | Per-paper override; pronunciation table (SAR -> "sar"; Decisively phoneme override) lives here, NOT in base | MODIFY |
| `swanki/conf/models/fish_speech_audrey.yaml` | Sibling per-paper variant; mirror new sub-tree skeleton (no per-paper overrides yet) | MODIFY |
| `swanki/conf/models/fish_speech_bechtel.yaml` | Same as audrey | MODIFY |
| `swanki/conf/prompts/default.yaml` | Lecture writer prompt; add bridging-sentence instruction for sections after the first | MODIFY |
| `swanki/conf/prompts/book_voice.yaml` | Book-voice prompt twin; mirror bridging instruction (must keep first-person whitelist intact) | MODIFY |
| `swanki/pipeline/pipeline.py` | Load-bearing flat-listed `tts_kwargs` dict at lines 1902-1908; add three nested keys via single `OmegaConf.to_container(resolve=True)` conversion | MODIFY |
| `tests/test_audio_common.py` | Fix the two broken assertions at lines 351 and 375; add coverage for chunker `max_chars=700`, `gain_match_target_dbfs`, `chunk_pause_ms`, slug stripper, repeated-phrase detector, sigh-tag scrubber | MODIFY |
| `tests/test_audio_lecture.py` | Add tests for `bridge_quality` critic dimension and refiner first-person whitelist preservation | MODIFY (or NEW if absent) |
| `tests/test_formatting.py` | Add cases for chapter-slug humanization | MODIFY (or NEW if absent) |
| `/scratch/hammingArtDoingScience2020/rerun_hamming_lectures.sh` | Existing batch regen entry-point; rerun after merge to validate against the 33 bookmarks | REFERENCE |
| `scripts/abs_refresh.sh` | Pushes regenerated mp3s to BookPlayer; invoked as `scripts/abs_refresh.sh hammingArtDoingScience2020` after rerun | REFERENCE |

## Key Design Decisions

1. **Do NOT revert `[pause]` -> `[long pause]`.** The Apr-26 design note (`swanki.audio._common#20260426...`) records that Fish renders the long form as audible breath/sigh — exactly the Theme 9 artifact the user is still hearing in older audio. The two failing tests at `tests/test_audio_common.py:351,375` are stale; production is correct. Fix the tests.

2. **Theme 1 (edge cutoffs) is downstream of Theme 4 (monotone tail).** `tail_buffer_ms=350` at `swanki/audio/_common.py:830` is the empirical sweet spot (v7=0 clipped, v8=150 clipped, v9=350 clean — see Apr-30 dendron entry). The "edge cutoff" listener perception is most likely sentence-cut-mid-thought from the chunker, not waveform truncation. Tightening `max_chars` fixes both themes via the same lever.

3. **Theme 4 fix: tighten `chunk_text_paragraphs` `max_chars` cap to ~700 and add an in-paragraph sentence-fallback branch for over-budget paragraphs.** Rejected: a new sentence-greedy `chunk_text_sentences` helper. Paragraph boundaries are a real prosodic signal; pure sentence packing would lose them and read worse. Add a parameter + fallback to the existing function instead of forking.

4. **Theme 12 (transition abruptness) gets a writer-prompt instruction AND a critic dimension, not a deterministic check.** Add one line to both `default.yaml` and `book_voice.yaml`: every section after the first must open with one sentence bridging from the prior topic. Add `bridge_quality: bool` to `LectureTranscriptFeedback` so the refine loop can flag and rewrite weak openers. No regex can validate "thematic continuity"; the critic is the right layer. Both inherit the existing first-person whitelist so book voice survives.

5. **Pronunciation overrides live in `fish_speech_hamming.yaml`, not the base `fish_speech.yaml`.** SAR ("Synthetic Aperture Radar") and "Decisively" are Hamming-domain context; other papers shouldn't inherit them. Per-paper Hydra variants are the right scope.

6. **YAML shape: nested sub-trees under `models.tts.{preprocessor,chunking,postprocessor}`.** Each sub-tree is a dict passed through to the audio layer as a nested dict in `tts_kwargs`. Single `OmegaConf.to_container(resolve=True)` conversion at the pipeline.py build site keeps the audio layer decoupled from Hydra's `DictConfig`. Per-paper variants override individual sub-keys via Hydra's normal merge.

7. **Theme 8 (filename slug leaking into intro audio) needs a grep pass, not just a function edit.** The slug `hammingArtDoingScience2020_03_history-of-computers-hardware` is being interpolated raw somewhere in chapter-intro/bookend script generation. Find every site, then route it through an extended `humanize_citation_key` that also handles `_NN_chapter-slug` suffixes.

8. **Repeated-phrase detector (Theme 5), filename-slug stripper (Theme 8), and sigh-tag scrubber (Theme 9) all live on the existing `_strip_duplicate_openers` / `_normalize_fish_speech_punct` post-refine layer.** No new architectural surface — these are deterministic guards in the same idiom as the existing duplicate-opener and Fish-tag whitelist code.

9. **Out of scope:** pinning `pydantic-ai`, pydub/audioop speculation (verify-don't-act — production audio works today; one-line `python -c "import pydub; from pydub import AudioSegment"` is the only check needed), bookend-audio caching (no cache exists; nothing to invalidate).

10. **Theme 10 (chronology drift, Babbage placement) is a critic-prompt nudge, not an algorithmic fix.** Add a one-line "preserve source-text chronology of named historical figures" item to the lecture critic prompt. Cheap, low-risk; refine loop owns it.

11. **Theme 11 (intra-passage verbal connectives) folds into the writer prompt, not the critic.** A "use connective phrases between consecutive sentences within a passage" sentence in `default.yaml`/`book_voice.yaml` is enough; flagging missing connectives in the critic would over-trigger and regress book voice.

## Approach

The work decomposes into five layers, each independently testable. Execution order matters because layer 5 (pipeline.py wiring) is load-bearing — without it, the YAML sub-trees added in layer 1 are silently dropped.

**Layer 1 — Hydra config sub-trees (`swanki/conf/models/fish_speech*.yaml`).** Add three nested groups under `models.tts`: `preprocessor` (acronym/word pronunciation table, sigh-tag scrubber toggles), `chunking` (`max_chars`, `min_chars`, `paragraph_priority`), `postprocessor` (`gain_match_target_dbfs`, `chunk_pause_ms`, `chunk_tail_trim_ms`, `chunk_crossfade_ms`). Base `fish_speech.yaml` carries empty/default sub-trees; `fish_speech_hamming.yaml` overrides only the pronunciation table. Audrey/Bechtel variants get the empty skeleton so the merge shape is uniform.

```yaml
# swanki/conf/models/fish_speech.yaml (illustrative shape)
tts:
  provider: fish_speech
  server_url: http://localhost:8080
  reference_id: british-prof
  preprocessor:
    pronunciations: {}      # per-paper variants fill this
    strip_forbidden_tags: true
  chunking:
    max_chars: 700
    paragraph_priority: true
  postprocessor:
    gain_match_target_dbfs: -25.0
    chunk_pause_ms: 700
    chunk_crossfade_ms: 50
```

**Layer 2 — pipeline.py wiring (`swanki/pipeline/pipeline.py:1902-1908`).** The flat-listed dict only forwards five hand-named keys; nested sub-trees would be silently dropped. Replace with a single `OmegaConf.to_container(tts_config, resolve=True)` call (or equivalent), then build `tts_kwargs` by merging in the three sub-trees as nested dicts. This is the load-bearing edit — without it, layer 1 has no effect.

**Layer 3 — chunker and audio assembly (`swanki/audio/_common.py`).** Tighten `chunk_text_paragraphs` to accept `max_chars` (default 700) and add a within-paragraph sentence-fallback branch when a single paragraph exceeds the cap. Wire `postprocessor` knobs (`gain_match_target_dbfs`, `chunk_pause_ms`, `chunk_crossfade_ms`) through to `combine_audio_with_section_pauses` so they become test-reachable; do NOT touch the `tail_buffer_ms=350` constant at line 830. Add deterministic post-refine scrubbers in the `_normalize_fish_speech_punct` neighborhood: a sigh/breath tag scrubber (Theme 9) that strips any tag not on the existing whitelist, a repeated-phrase detector (Theme 5) that removes consecutive near-duplicates above a similarity threshold, and a filename-slug stripper (Theme 8) called on every site identified by the grep pass. Extend `humanize_citation_key` in `swanki/utils/formatting.py:184` to handle `_NN_chapter-slug` suffixes (zero-padded chapter number -> "chapter three", slug -> spaces).

**Layer 4 — writer prompts and critic dimensions.** In `swanki/conf/prompts/default.yaml` and `book_voice.yaml`, add: (a) one sentence requiring a bridging opener for every section after the first (Theme 12); (b) one sentence about intra-passage verbal connectives (Theme 11); (c) one critic-prompt line preserving source-text chronology of named figures (Theme 10). In `swanki/models/cards.py:1352`, extend `LectureTranscriptFeedback` with `bridge_quality: bool` and `repeated_phrase: bool` dimensions plus matching critic-prompt items. The refiner already whitelists first-person framings; the new dimensions inherit that contract — verify by reading the existing whitelist code path before editing the critic prompt. Use `model_validate(dump | {...})` to construct any update copies (Pydantic 2 `model_copy(update=...)` does not re-run validators).

**Layer 5 — `lecture.py` post-refine sequencing.** The deterministic scrubbers added in layer 3 must run AFTER refine and BEFORE TTS — same insertion point as `_strip_duplicate_openers` (`swanki/audio/lecture.py:117`). Order: duplicate-opener -> repeated-phrase -> slug-stripper -> sigh-tag -> Fish-tag normalization. No new public surface; just call sites.

**Test layer.** Fix `tests/test_audio_common.py:351,375` to assert `[pause]`. Add coverage for the previously-untested `combine_audio_with_section_pauses` parameters (`gain_match_target_dbfs`, `chunk_pause_ms`, `chunk_tail_trim_ms`, `chunk_crossfade_ms` > 0). Add chunker tests for `max_chars=700` and the in-paragraph fallback. Add tests for the slug stripper, repeated-phrase detector, and sigh-tag scrubber. Add a critic test for `bridge_quality` and a refiner test confirming the first-person whitelist still wins ("I think", "in my view", "we will see" survive a regenerate cycle).

## Gotchas

1. **Reverting `[pause]` -> `[long pause]` re-introduces Theme 9.** The two stale test assertions look like the source of truth, but they have been wrong since 2026-04-26. The dendron entry `swanki.audio._common#20260426...` is the authority. Fix the tests; production is right.

2. **`tts_kwargs` at `swanki/pipeline/pipeline.py:1902-1908` is a flat hand-listed dict.** Adding nested sub-trees to YAML without editing this site means they get silently dropped — no error, no warning, audio quality just doesn't change. Layer 5 of the layer-stack must precede or co-merge with the YAML edits. This is the single load-bearing edit.

3. **Hydra config groups don't auto-merge across variants.** `book_voice.yaml` duplicates `default.yaml`'s schema; `fish_speech_hamming.yaml` duplicates `fish_speech.yaml`'s schema. Adding a sub-tree to the base file does NOT propagate — each per-paper variant must mirror the new sub-tree skeleton or Hydra's merge will leave gaps.

4. **`OmegaConf.DictConfig` is not a `dict`.** Passing it directly to a Pydantic model constructor or to `**kwargs` works in some places and silently misbehaves in others. Convert once at the pipeline.py build site with `OmegaConf.to_container(tts_config, resolve=True)` before doing any dict construction or pydantic validation.

5. **Pydantic 2 `model_copy(update=...)` does not re-run validators.** When constructing modified `LectureTranscriptFeedback` instances (e.g., in a test or refine helper), use `model_validate(instance.model_dump() | {...})` instead. Otherwise constraints on the new `bridge_quality`/`repeated_phrase` fields silently slip through.

6. **`generate_bookend_audio` does NOT cache.** Bookend audio is regenerated every run, so changing `humanize_citation_key` takes effect on the very next pipeline invocation — no cache invalidation step needed. (The trap is the inverse: assuming a cache exists and writing invalidation code that does nothing.)

7. **First-person book voice must survive every refine cycle.** The Apr-30 critic + refiner whitelist ("I think", "in my view", "we will see") is the only thing keeping Hamming's voice from being normalized into third-person lecture style. New critic dimensions (`bridge_quality`, `repeated_phrase`) and new writer prompt lines must not introduce instructions that conflict with the whitelist. Read `swanki/audio/lecture.py` whitelist code before editing prompts.

8. **`tail_buffer_ms=350` at `swanki/audio/_common.py:830` is empirically tuned.** v7=0 clipped, v8=150 clipped, v9=350 clean. Don't "round" or "simplify" it. The deliberator concluded Theme 1 is downstream of Theme 4; the chunker fix should obviate the urge to touch this.

9. **Fish-tag whitelist is small and load-bearing.** Allowed: `[pause]`, `[short pause]`, `[long pause]` (section boundaries only), `[emphasis]`, `[excited]`, `[delight]`, `[gasp]`, `[laughing tone]`, `[chuckle]`, `[amused]`, `[thoughtful]`, `[curious]`, `[serious]`, `[sincere]`. The new sigh-tag scrubber must use this exact list as its allowlist — anything else (including hallucinated `[inhale]`, `[exhale]`, `[sigh]`, `[clearing throat]`) gets stripped.

10. **pydub on Python 3.13 is a verify-don't-act item.** Production audio works today. One-line check (`python -c "from pydub import AudioSegment; AudioSegment.silent(100)"`) is sufficient; do not preemptively pin or upgrade.

## Verification

- `pytest tests/test_audio_common.py tests/test_audio_lecture.py tests/test_formatting.py` — all green, including the corrected `[pause]` assertions and the new coverage.
- `python -c "from pydub import AudioSegment; AudioSegment.silent(100)"` — confirms pydub still operational on the workstation Python.
- `bash /scratch/hammingArtDoingScience2020/rerun_hamming_lectures.sh` — regenerate all Hamming chapter lectures with the new chunker, post-refine guards, and pronunciation overrides.
- `bash scripts/abs_refresh.sh hammingArtDoingScience2020` — push regenerated mp3s to BookPlayer (uses the Apr-25 stale-mp3 replacement path, so phantom chapters won't recur).
- Re-listen against the original 33 BookPlayer bookmarks. Per theme, confirm:
  - Theme 1 (edge cutoffs): no perceived clipping at chunk boundaries.
  - Theme 2 (volume jumps): no sharp level changes at chunk starts.
  - Theme 4 (droning tail): chunks feel finite; no "running on" past the natural close of a thought.
  - Theme 6 (SAR): pronounced as "sar", not "say R".
  - Theme 7 (Decisively): single-word glitch resolved.
  - Theme 8 (filename slug): chapter intros read "Chapter three, history of computers and hardware", never the raw slug.
  - Theme 12 (transitions): chapter 2 "space and time" pivot has a bridging sentence; no other section opens cold.
- Spot-check one non-Hamming paper's lecture audio (e.g., Audrey or Bechtel) to confirm the first-person book voice still survives the new critic dimensions.
- `git grep -n "long pause" swanki/` — should match only legitimate usage (section boundaries), not the deprecated chunk-pause path.
