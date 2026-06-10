---
id: t1wdykzz6nspnddcxrt6wlh
title: Comment_edit
desc: ''
updated: 1780179297372
created: 1780179297372
---

## 2026.05.30 - Comment-driven precise chunk edits + `_edits/` audit trail

New swanki-native "apply" engine for the audio-fix-from-annotations workflow,
generalizing the one-off `scripts/fix_hamming_lecture_ch04_ch05.py`. Plan:
[[plan.swanki-comment-driven-chunk-edits.2026.05.30]].

`edit_chunk(manifest_path, idx, *, comment | new_text | speech_only,
tts_kwargs, speed, model, section_pause_ms)` applies ONE reviewer comment to
ONE chunk and restitches. Three paths:

- `speech_only=True` -> re-roll the stored chunk text VERBATIM (Fish
  temperature 0.8 gives a fresh take). No preprocessing -- the stored text is
  already shaped.
- `comment=...` (typical) -> `chunk_edit_agent` (in [[swanki.llm.agents]],
  `ChunkEditResponse` in [[swanki.models.cards]], wrapped in
  `with_safety_retry`) returns `{action, revised_text?, rationale}`.
  `edit_text` rewrites; `speech_only` re-rolls; `needs_section_regen` /
  `cannot_fix` are returned WITHOUT touching audio (the human escalates --
  conceptual/stylistic fixes go to `conf/prompts/*.yaml`, not here).
- `new_text=...` -> caller's verbatim replacement prose.

Key correctness decision: the preprocessor runs on NEW prose ONLY. Stored
chunk text is already post-scrubbers, post-`add_tts_pauses`, AND
post-`append_chunk_pause` (boundary tags stripped) -- and `add_tts_pauses` is
NOT idempotent. So `edit_text` runs
`append_chunk_pause(preprocess_for_tts(new_prose, tts_kwargs, add_pauses=True))`
to match exactly what a fresh full-gen builds and stores, then persists that
shaped text to the manifest. `speech_only` never re-preprocesses. See
[[swanki.audio._common]] for the extracted `preprocess_for_tts` helper.

Does its own re-TTS (must inject the preprocessor, which
`surgical.regenerate_and_restitch` deliberately does not) but reuses the same
leaf `restitch_from_chunks` (which rewrites `chunk_timeline.json`). Fail-loud
guards: missing `postprocessor` block (mirrors surgical), missing Fish
`reference_id` (wrong-voice insurance). Audit: a `_edits/` subdir inside each
`*_chunks/` dir gets, before each overwrite, `chunk{idx}_{UTCstamp}.mp3`+`.txt`
(first edit captures the baseline; repeated edits trace evolution) and
`manifest_{stamp}.json`; after restitch, one `edits_log.jsonl` record
(`ts, idx, comment, old_text, new_text, action, rationale, output_file,
git_hash`). `restitch_from_chunks` reads explicit `chunk["file"]` names, so
`_edits/` is never globbed as real chunks. A full pipeline regen creates a new
`*_NN_slug_<N>` dir, orphaning the old `_edits/` -- inherent (a full regen is a
fresh baseline). Classification, the review gate, and publishing stay in the
audio-fix-from-annotations skill.

## 2026.06.09 - `edit_chunk` speed defaults to the original-gen speed for the audio type

`edit_chunk` carried a hardcoded `speed=1.1` default — which happens to match the
*summary* config but NOT lecture (1.0) or reading (1.2). So any lecture/reading chunk
edited without an explicit `speed=` came out audibly faster than its neighbors at the
splice. It already read `audio_type` from the manifest but ignored it for speed.

Fix: `speed` now defaults to `None` and resolves in priority order — (1) the caller's
explicit `speed=`, (2) the manifest's new `speed` field (written at gen time by
`write_chunk_manifest`), (3) a per-`audio_type` fallback map `_SPEED_BY_AUDIO_TYPE`
(lecture 1.0 / summary 1.1 / reading 1.2 / card 1.6) for legacy manifests that predate
the field. So a surgical edit always re-TTSs at the speed the chapter was generated at,
and callers (the audio-fix skill) no longer need to pass `speed` at all. The map mirrors
`swanki/conf/audio/*.yaml`. See [[swanki.audio._common]] (same date) for the manifest
field. Also repaired two `test_audio_comment_edit` tests left red by the codeword-scope
default-off change (PR #39): they now opt the scrubber on via the preprocessor config.
