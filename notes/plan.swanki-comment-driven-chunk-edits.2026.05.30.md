---
id: 2f3jf2bbekqc70u7w24z6mh
title: '30'
desc: ''
updated: 1780177332671
created: 1780177332671
---

## Context

Comment-driven precise audio edits today live in two places that don't compose. `scripts/fix_hamming_lecture_ch04_ch05.py` is a bespoke one-off: it hardcodes paths, the Fish reference voice, and the *exact replacement transcript text* inline, then calls `surgical.regenerate_and_restitch`. The `.claude/skills/audio-fix-from-annotations` skill orchestrates the human-facing flow (classify orange Zotero/ABS comments -> match to chunks -> one review gate -> apply -> publish) but the "apply" step has no swanki-native home for the *content rewrite*, so every new fix risks another bespoke `fix_*.py` or Claude free-typing the replacement transcript inline (which silently skips the TTS preprocessor that every surrounding chunk went through).

The goal is 0-shot audio quality; precise edits are the bridge until we get there. This plan builds `swanki/audio/comment_edit.py` as the swanki-native "apply" engine: an LLM agent classifies/rewrites one chunk, an `edit_chunk` dispatcher runs the *correct preprocessor on new prose only*, re-TTSs, restitches via the same leaf primitive `surgical.py` uses, and writes a full `_edits/` intervention audit trail. Claude Code still classifies and the user still approves (in the skill), but the actual rewrite + re-TTS + restitch is swanki code called with args.

**Architecture split (authoritative).** Moves INTO `comment_edit.py`: the chunk-edit agent, the `edit_chunk` dispatcher, the preprocessor-on-new-text, the `_edits/` audit trail. STAYS in the skill: comment classification, the single human-review gate, ABS clear+remark under flock, publish sequencing (commit -> rebase -> sync_to_zotero -> abs_refresh). Section-level regeneration and publishing are OUT OF SCOPE; conceptual/stylistic comments (vs. a single bad chunk) are handled by editing `conf/prompts/*.yaml`, not here.

## Relevant Files

| Path | Action | Purpose | Stance |
|---|---|---|---|
| `swanki/audio/comment_edit.py` | NEW | `chunk_edit_agent` invocation, `edit_chunk` dispatcher, preprocessor-on-new-text, `_edits/` audit trail | the new engine |
| `swanki/audio/_common.py` | MODIFY | Extract public `preprocess_for_tts(...)` as the single scrubber-chain source of truth | stable/recently in-flux; touch only the new helper |
| `swanki/audio/card.py` | MODIFY | Delegate private `_preprocess_for_tts` to the new shared helper (`add_pauses=False`) | stable; minimal delegation only |
| `swanki/models/cards.py` | MODIFY | Add `ChunkEditResponse` beside `AudioTranscriptFeedback`/`LectureTranscriptFeedback` | provisional |
| `swanki/llm/agents.py` | MODIFY | Register `chunk_edit_agent` | stable; one-line additive |
| `swanki/audio/surgical.py` | REFERENCE | Share leaf primitives; do NOT add a preprocess hook here | stable; leave alone |
| `swanki/llm/safety.py` | REFERENCE | Wrap the agent call in `with_safety_retry` | stable |
| `scripts/abs_bookmarks.py` | REFERENCE | Comment source (ABS bookmarks) consumed by the skill | stable |
| `scripts/zotero_annotations.py` | REFERENCE | Comment source (orange Zotero highlights) consumed by the skill | stable |
| `.claude/skills/audio-fix-from-annotations/SKILL.md` | MODIFY | Phase 5 calls `edit_chunk` instead of `regenerate_and_restitch` directly; classification + gate + publish unchanged | living doc |
| `notes/swanki.audio.comment_edit.md` | NEW | Dendron module note (rationale/decision log) | new |
| `tests/test_audio_comment_edit.py` | NEW | Unit tests with fake manifest + patched TTS/restitch | new |
| `tests/test_audio_common.py` | MODIFY | Tests for `preprocess_for_tts` (pause vs no-pause, idempotence) | new tests, existing file |

## Key Design Decisions

1. **Preprocessor applies to NEW prose only; `speech_only` re-rolls stored text verbatim.** Stored `chunk["text"]` is already post-scrubbers AND post-`add_tts_pauses` (lecture.py builds `tts_transcript = add_tts_pauses(cleaned)` then chunks it — confirmed at `lecture.py:850-867`). So `edit_chunk` feeds `text_to_speech` exactly:
   - `speech_only`: `chunk["text"]` unchanged (already shaped — re-running anything would double-process).
   - agent rewrite: `add_tts_pauses(scrubbers(clean_markdown_for_tts(agent.revised_text)))`.
   - explicit `new_text`: same full-chain treatment.
   **Why:** `verbalize_bit_strings`/`expand_acronyms`/`apply_pronunciation` are idempotent, but `add_tts_pauses` is NOT — it re-injects `[pause]` on blank lines, after `:`/`.`-newline, and every 3rd sentence (`_common.py:56-99`). Re-running it on stored text double-pauses. Scrubbers-only on new text would leave new chunks pause-starved versus neighbors, so `add_tts_pauses` IS included for new prose. Rejected: a single uniform path for both actions — it cannot satisfy "verbatim for speech_only" and "fully shaped for new text" at once.

2. **Extract one shared `preprocess_for_tts` into `_common.py`; do not duplicate.** Signature: `preprocess_for_tts(text, tts_kwargs, *, add_pauses, clean_markdown=True) -> str`. Order is the single source of truth: optional `clean_markdown_for_tts` -> `strip_chapter_filename_slug` -> `expand_acronyms_for_tts` (fish only) -> `verbalize_bit_strings` (default-on) -> `apply_pronunciation_overrides` -> `strip_forbidden_fish_tags` (fish only) -> optional `add_tts_pauses`. `card.py`'s private `_preprocess_for_tts` becomes a thin delegate with `add_pauses=False, clean_markdown=False` (cards skip markdown clean + pauses today, `card.py:48-49`). `comment_edit.py` calls it with `add_pauses=True`. Rejected: a 5th inline copy in `comment_edit.py`. Refactoring lecture/reading/summary's three inline copies to call the helper is RECOMMENDED-BUT-OPTIONAL follow-up — out of scope here to avoid destabilizing three large files in one PR.

3. **`ChunkEditResponse` lives in `swanki/models/cards.py`.** Fields (all `Field(description=...)`, per project Pydantic convention): `action: Literal["edit_text", "speech_only", "needs_section_regen", "cannot_fix"]`; `revised_text: str | None`; `rationale: str`. Placed beside `AudioTranscriptFeedback`/`LectureTranscriptFeedback` (`cards.py:1364-1384`) where the other audio-feedback models already live. `needs_section_regen` and `cannot_fix` are terminal signals the dispatcher refuses to auto-apply (they escalate back to the human / skill).

4. **Voice/`tts_kwargs` is caller-supplied; fail loud if a Fish reference is missing.** Consistent with `surgical.regenerate_and_restitch` (`surgical.py:54`), the caller passes `tts_kwargs`; the skill sources `reference_id`/`speed` from the paper's `conf/models/fish_speech_<paper>.yaml`. `edit_chunk` asserts before any TTS: if `tts_kwargs["provider"] == "fish_speech"` and `reference_id` is missing/empty, raise. Rejected: storing the voice in the manifest — it duplicates config that is already authoritative in `fish_speech_<paper>.yaml`, inviting drift.

5. **`edit_chunk` does its own re-TTS but reuses `restitch_from_chunks` directly.** It must inject the preprocessor on new text, which `regenerate_and_restitch` deliberately does NOT do (surgical's contract is "render exactly this text"; its `None` path re-renders stored text after an *upstream code* fix, so adding pauses there would corrupt it). So `edit_chunk` owns the TTS call and calls the same leaf `restitch_from_chunks(manifest_path, output_path, section_pause_ms=...)` that surgical calls (it already rewrites the `chunk_timeline.json` sidecar). The two modules share leaf primitives (`text_to_speech`, `restitch_from_chunks`, `fish_speech_healthy`) but own their dispatch. Do NOT add a preprocess hook to `regenerate_and_restitch`.

6. **`speech_only` relies on Fish temperature 0.8 for a fresh take; no determinism flag.** Re-rolling the stored verbatim text at temperature 0.8 yields a different prosody — that IS the intent for "delivery was bad." No Fish seed is surfaced; a deterministic flag would be dead config, and the human approves each result anyway. Rejected: adding a seed/deterministic knob.

## Approach

`comment_edit.py` exposes one primary callable, `edit_chunk`, plus the agent invocation it dispatches through. The skill resolves the live dir, `audio_type`, and the matched chunk index (Phases 1-4, unchanged), then for each approved intervention calls `edit_chunk` with: `manifest_path`, `idx`, the `comment` text, the matched chunk's current text, an optional human-overridden `new_text`, the `tts_kwargs` (with the paper's Fish reference voice), `speed`, and `section_pause_ms`.

**Classification path.** When the skill hands `edit_chunk` a comment but no explicit `new_text`, the function invokes `chunk_edit_agent` via `with_safety_retry(chunk_edit_agent, user_msg, instructions=..., model=get_model_string(cfg), label="chunk edit <idx>")`. The agent sees the comment, the chunk's current text, and the section/context; it returns a `ChunkEditResponse`. `action == "edit_text"` carries `revised_text`; `action == "speech_only"` means "text is fine, delivery isn't"; `needs_section_regen`/`cannot_fix` are non-applicable terminals that `edit_chunk` surfaces (returns/raises with the rationale) so the human escalates — the dispatcher never silently no-ops. When the skill passes an explicit human-authored `new_text`, the agent is bypassed and the action is forced to `edit_text` (the human is final arbiter, per the skill's gate).

**Render path.** Guard `tts_kwargs` (Decision 4) and assert the manifest has a `postprocessor` block (matching `surgical.py:93`) and the right `audio_type`. Resolve the chunk dict by `index`. Then dispatch on action:
- `speech_only`: `render_text = chunk["text"]` (verbatim).
- `edit_text`: `render_text = preprocess_for_tts(revised_or_new_text, tts_kwargs, add_pauses=True)` and persist the *raw* revised text into `chunk["text"]` (so the manifest transcript stays the post-pause shape — match what lecture.py stores: it stores the post-`add_tts_pauses` chunk text; therefore persist the preprocessed `render_text`, not the raw agent prose, to keep manifest semantics identical to a fresh gen). Write the manifest back.

Then re-TTS only that one chunk's mp3 (`chunks_dir / chunk["file"]`, in place) via `text_to_speech(render_text, voice_id="", output_path=out, api_key="", speed=speed, **tts_kwargs)`, and `restitch_from_chunks(manifest_path, output_path, section_pause_ms=...)`. Return the restitched output path plus the edited chunk's new `(start_ms, end_ms)` from `chunk_time_window(chunks_dir, audio_type, idx)` so the skill can report the new MM:SS for ABS re-marking.

**Audit trail.** A `_edits/` subdir INSIDE the `*_chunks/` dir. BEFORE each overwrite: archive the prior chunk audio + text to `_edits/chunk{idx}_{UTCisostamp}.mp3` and `.txt` (the first edit auto-captures the original baseline; repeated edits to one chunk yield its full evolution), and snapshot the full manifest to `_edits/manifest_{stamp}.json`. AFTER the restitch, append ONE record per intervention to `_edits/edits_log.jsonl`: `{ts, idx, comment, old_text, new_text, action, rationale, output_file, git_hash}`. `git_hash` is captured at write time (`git rev-parse --short HEAD`). `restitch_from_chunks` reads explicit `chunk["file"]` names from the manifest, so the `_edits/` subdir is never globbed as real chunks — but any zip/scan packer MUST be told to ignore `_edits/`.

The single short snippet that disambiguates the render dispatch:

```python
if action == "speech_only":
    render_text = chunk["text"]                       # verbatim re-roll (temp 0.8)
else:  # edit_text
    render_text = preprocess_for_tts(new_prose, tts_kwargs, add_pauses=True)
    chunk["text"] = render_text                       # manifest stays post-pause shaped
```

## Gotchas

1. **`add_tts_pauses` non-idempotence** is the core trap — see Decision 1 for the full rule (preprocess NEW prose only; `speech_only` verbatim).
2. **A re-TTS chunk with a different duration shifts downstream offsets.** `restitch_from_chunks` rewrites `chunk_timeline.json`, but absolute MM:SS of later chunks move. Sidestep: do NOT try to migrate ABS bookmark timestamps; the standing rule is clear+remark (the skill clears ABS bookmarks under flock and re-marks). `edit_chunk` returns the edited chunk's new window via `chunk_time_window` so the human re-marks against the correct time.
3. **Fish has no retry; one bad chunk aborts the call.** Sidestep: the skill pre-flights `fish_speech_healthy(server_url)` before calling `edit_chunk`; temperature-0.8 non-determinism is intentional for `speech_only`, not a failure.
4. **A wrong/empty Fish `reference_id` silently renders in a default voice** — hence Decision 4's fail-loud guard before any TTS.
5. **`_edits/` orphaned on a full regen.** A full pipeline regen creates a new `*_NN_slug_<N>` dir, leaving the old `_edits/` behind. This is inherent — a full regen is a fresh baseline. Sidestep: document it; the `_edits/` trail is per-dir, not migrated. Also ensure `_edits/` is never globbed as chunks (it isn't, because restitch uses explicit filenames) and is excluded from zip/scan packers.
6. **Stale `git_hash` if uncommitted.** `edits_log`'s `git_hash` and `sync_to_zotero`'s embedded hash go stale if edits aren't committed before sync. Publishing lives in the skill (commit -> rebase -> sync), but note `edit_chunk` records `git_hash` at write time, so re-syncing after a rebase is the skill's job (already its rule).
7. **Legacy manifests may lack a `postprocessor` block.** `surgical.py:93` asserts it; `edit_chunk` MUST assert the same, failing loud — without it, restitch can't reproduce the original silence/gain.
8. **Biosec refusal on the rewrite.** The agent rewriting CRISPR/viral-adjacent chunk text can trip `invalid_prompt`. Sidestep: wrap `chunk_edit_agent` in `with_safety_retry(..., label="chunk edit <idx>")` (Decision 3 path); `EDU_CONTEXT_PREAMBLE` routes around it.

## Verification

- `tests/test_audio_comment_edit.py` (NEW), patterned on `tests/test_audio_surgical.py` (fake manifest + fake chunk mp3s, `@patch` on `text_to_speech` and `restitch_from_chunks`, no real TTS, no real LLM — patch `chunk_edit_agent.run_sync`/`with_safety_retry` to return a canned `ChunkEditResponse`):
  - `edit_text` path: asserts `text_to_speech` is called with preprocessed text (pause tags present), manifest `chunk["text"]` updated, exactly the named chunk's mp3 path passed, `restitch_from_chunks` called once.
  - `speech_only` path: asserts `text_to_speech` called with the stored text VERBATIM (no extra `[pause]` injected), manifest text unchanged.
  - Missing-`reference_id` guard: `provider=fish_speech` without `reference_id` raises before any TTS.
  - Missing-`postprocessor` manifest: raises (mirrors surgical's assert).
  - `needs_section_regen`/`cannot_fix`: no TTS/restitch; surfaces rationale.
  - Audit trail: `_edits/` created, baseline chunk `.mp3`+`.txt` archived, `manifest_*.json` snapshot present, one `edits_log.jsonl` line with all required keys.
- `tests/test_audio_common.py` (MODIFY): `preprocess_for_tts` with `add_pauses=True` injects pause tags; with `add_pauses=False` matches card.py's prior behavior; the scrubber-only portion is idempotent; fish-only steps are no-ops for `provider != fish_speech`.
- Run: `~/opt/miniconda3/envs/swanki/bin/python -m pytest tests/test_audio_comment_edit.py tests/test_audio_common.py tests/test_audio_surgical.py -q` (and `ruff`/`mypy` per project skills). No real Fish/network in tests.
- pydantic-ai usage mirrors existing code exactly (`agent.run_sync(msg, instructions=..., model=..., model_settings=...)`, `output_type=...`, `with_safety_retry`); no library-version behavior is asserted that needs a web cite — the codebase already runs these APIs.

## Open Questions

1. **`_edits/` retention policy.** Recommend never auto-prune (the evolution trail is cheap and is the whole point); add a cap only if the user later asks. Confirm "never prune" is acceptable.
2. **`clean_markdown_for_tts` on agent output.** Recommend running it (`clean_markdown=True`) for fidelity — agent prose is likely a no-op for it, but it guarantees new text matches the lecture chain, which DOES clean markdown first. One-line confirm that running it on agent output is desired.
