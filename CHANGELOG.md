# CHANGELOG



## v2.0.0 (2026-03-20)

### Breaking

* API: Major refactor — audio decoupling, config overhaul, pydantic-ai migration

Co-Authored-By: Claude Opus 4.6 (1M context) &lt;noreply@anthropic.com&gt; ([`d8d2f46`](https://github.com/Mjvolk3/Swanki/commit/d8d2f465325b9073ee2d88a3e5b2216a079be9c5))

### Unknown

* Bump version to 2.0.0 for major refactor release

Co-Authored-By: Claude Opus 4.6 (1M context) &lt;noreply@anthropic.com&gt; ([`675bc0c`](https://github.com/Mjvolk3/Swanki/commit/675bc0c4efe42447e06a1f0721ab6fb355181b91))

* Merge pull request #1 from Mjvolk3/major-refactor

Major refactor: audio, config, segmentation, lecture, pydantic-ai ([`bdf9958`](https://github.com/Mjvolk3/Swanki/commit/bdf9958d834b7f168950f0d63172dfea6a4fc4f3))

* Add dendron stub for audio manifest module

Co-Authored-By: Claude Opus 4.6 (1M context) &lt;noreply@anthropic.com&gt; ([`29e4ad3`](https://github.com/Mjvolk3/Swanki/commit/29e4ad33b24db36c1bca3e6de672952be7b406af))

* Add open-source TTS plan, week 12 notes, audio manifest module

- Plan for replacing ElevenLabs with F5-TTS/Kokoro/S2 Pro via Docker/Slurm
- Week 12 weekly task note
- Audio manifest module for tracking generated files

Co-Authored-By: Claude Opus 4.6 (1M context) &lt;noreply@anthropic.com&gt; ([`2aa27d0`](https://github.com/Mjvolk3/Swanki/commit/2aa27d027d5cac16b140573cc1516507ea268028))

* Audio quality overhaul: Great Courses lecture style, TTS cost reduction, prosody

- Rewrote lecture system prompt for Great Courses style (Sagan/Feynman/Lane tone, mandatory roadmap, spoken transitions, no meta-commentary, 25-35% length target)
- Added methods/SI section classifier with positional cascade — STAR Methods and subsequent subsections become enrichment context, not lecture sections
- Hard-capped lecture at min(source words, 4500 words / ~30 min) with sentence-boundary truncation
- Switched reading/summary/cards TTS from eleven_multilingual_v2 to eleven_flash_v2_5 (0.5x credit cost, 40k char limit); lecture keeps premium model
- Added paragraph-only TTS chunking for lecture (never splits mid-sentence) and SSML &lt;break&gt; tag injection at paragraph boundaries for all audio types
- Robust LaTeX brace auto-fix: final validator now fixes both excess and missing braces instead of crashing after 3 retries
- Rewrote humanize_citation_key() for proper year separation, hyphenated author names, and natural &#34;et al&#34; placement
- Summary prompt hardened: 1200-word cap, explicit ban on &#34;[pause]&#34; and letter-by-letter spelling
- Updated default TTS model config (conf/models/default.yaml) with model + lecture_model keys
- Updated test mocks to accept tts_model kwarg

Co-Authored-By: Claude Code (commit) &lt;noreply@anthropic.com&gt; ([`a1201c3`](https://github.com/Mjvolk3/Swanki/commit/a1201c342dc554c2c0fee59a5446e7591f6e1a32))

* Make /stage default to non-interactive, add /stage blocks for interactive mode

- Flip default behavior: `/stage` now stages all files without prompts
- Interactive block selection available via `/stage blocks`
- Update skill description, args, and examples to reflect new defaults

Co-Authored-By: Claude Code (commit) &lt;noreply@anthropic.com&gt; ([`a430618`](https://github.com/Mjvolk3/Swanki/commit/a430618e444095f9b550f42500b9e5dd8de9baf0))

* Organize audio quality vision into plan note, update weekly tasks

- Move audio quality criticism and learning workflow vision from scratch note into plan.audio-quality-vision
- Remove empty placeholder plan.start-end-audio-queue-non-complementary-audio.plan-0
- Add 2026.03.14 entries to weekly note for bookend cleanup and vision note

Co-Authored-By: Claude Code (commit) &lt;noreply@anthropic.com&gt; ([`961027b`](https://github.com/Mjvolk3/Swanki/commit/961027b6f0e67b3dcdb1e9a17bd1f5563c390029))

* Clean up bookend files after combining into final audio

- Delete intermediate bookend MP3s (_start.mp3, _end.mp3) after they are
  baked into the combined output, so only 3 final audio files remain
- Remove stale cache-hit logic from generate_bookend_audio since bookends
  are always regenerated and cleaned up per run

Co-Authored-By: Claude Code (commit) &lt;noreply@anthropic.com&gt; ([`1406d1d`](https://github.com/Mjvolk3/Swanki/commit/1406d1dc56f8b9b4deee3054a1840f71f0af36df))

* Audio quality: section pauses, bookends, metadata filter, acronyms, Zotero annotations

- Add section-aware audio infrastructure to _common.py: generate_silence, split_transcript_by_sections, combine_audio_with_section_pauses, generate_bookend_audio, extract_acronyms
- Replace SSML &lt;break&gt; tags with ---SECTION_BREAK--- markers for real silence between sections in reading, summary, and lecture
- Add START/END bookend announcements with humanized citation key for all audio types
- Apply filter_metadata to reading pipeline to strip affiliations, emails, and dates before LLM processing
- Remove filler text between sections in reading prompt -- silence only, no transitions
- Add figure announce pattern (pause/Figure X/pause/description) to reading prompt
- Enforce labeled lecture structure (Intro, Results, Conclusion) and tighten analogy rule
- Extract and inject acronym definitions into LLM prompts for reliable first-use expansion
- Add Zotero annotation extraction script and /zotero-annotations skill
- Add 14 new tests for infrastructure functions, update mocks in reading/summary tests

Co-Authored-By: Claude Code (commit) &lt;noreply@anthropic.com&gt; ([`1791c21`](https://github.com/Mjvolk3/Swanki/commit/1791c2128afecea50a84477387c2dfbab085751e))

* Span-based LaTeX auto-wrap, auto-fix validation instead of crash

- Replace lookbehind/lookahead auto-wrap with span-position checking to handle bare math adjacent to broken $ delimiters
- Extend sub+super pattern to match partially-braced forms (V_{i}^\max, V_{i}^max)
- Change validation to auto-wrap detected bare math (patterns 1-5) instead of raising ValueError
- Only unbalanced braces inside $...$ still raise errors for LLM retry
- Remove high-false-positive patterns 6 (Unicode Greek) and 7 (isolated capitals)
- Add plan and scratch notes for audio queue and transcript improvements

Co-Authored-By: Claude Code (commit) &lt;noreply@anthropic.com&gt; ([`736fde4`](https://github.com/Mjvolk3/Swanki/commit/736fde44fac7a85971e819a994956393fefb6bea))

* Auto-fix LaTeX in card validation, increase segment target to 6000 chars

- Add auto-fix for double closing braces in subscripts (_{ij}} -&gt; _{ij})
- Add auto-fix for unbalanced braces inside $...$ spans (append missing })
- Add auto-wrap for bare subscript/superscript patterns in $ delimiters
- Extend brace-balance validation to \(...\) delimiters
- Remove single-issue pass-through (all math issues now trigger retry)
- Add 14 context words to isolated variable detection (Pattern 7)
- Increase default target_chars from 4000 to 6000 to reduce segment count

Co-Authored-By: Claude Code (commit) &lt;noreply@anthropic.com&gt; ([`a9a2dbd`](https://github.com/Mjvolk3/Swanki/commit/a9a2dbddc3dfed1e32702288cd8c450cd96b7231))

* Fix Hydra plugin discovery, default to char segmentation, enable apkg export

- Add top-level hydra_plugins/swanki/ namespace package for Hydra 1.3.2 discovery
- Include hydra_plugins* in setuptools packages.find
- Switch all pipeline presets from page to char segmentation
- Enable create_anki_deck in output config for .apkg export
- Fix split LaTeX subscript braces (W_{i}j} -&gt; W_{ij}) with auto-fix regex
- Add brace-balance validation inside $...$ spans to trigger retry
- Increase image summary max_tokens from 300 to 1024 for pydantic-ai

Co-Authored-By: Claude Code (commit) &lt;noreply@anthropic.com&gt; ([`19f20b0`](https://github.com/Mjvolk3/Swanki/commit/19f20b05a71302b47509f4ea3b91f3fa45a39b98))

* tasks ([`c20ca37`](https://github.com/Mjvolk3/Swanki/commit/c20ca37f139679dfa09e2118b239c1189956d7dd))

* Pre-API hardening: delete legacy, ruff format, type modernization, new tests

- Delete swanki/legacy/ (31 files) and remove --legacy CLI path from __main__
- Rewire --send-to-anki to modern send_to_anki module instead of legacy md_to_anki
- Delete broken test scaffolds (test_first_module, test_anki_processor_tables)
- Apply ruff formatting across all modern modules (import sort, double quotes, line wrap)
- Modernize type annotations: Optional[X] -&gt; X | None, List -&gt; list, Dict -&gt; dict
- Add ConfigDict(extra=&#34;forbid&#34;) to Pydantic models; add alt_text/context to ImageSummary
- Add standard frontmatter docstrings (file path, dendron link, GitHub URL) to all modules
- Add mypy type-narrowing asserts and fix type annotations across 6 files
- Add 4 new test files (agents, config resolution, model validation, LLM smoke)
- Add cleanup plan notes and update dendron module notes + weekly

Co-Authored-By: Claude Code (commit) &lt;noreply@anthropic.com&gt; ([`2a6d36b`](https://github.com/Mjvolk3/Swanki/commit/2a6d36bf67e08722119eea64d11d5aae510838ad))

* Update dendron notes and weekly for Step 5 completion

- Add module notes for swanki.llm.__init__ and swanki.llm.agents
- Update weekly with Step 5 migration and cleanup entries

Co-Authored-By: Claude Code (commit) &lt;noreply@anthropic.com&gt; ([`08bfdfc`](https://github.com/Mjvolk3/Swanki/commit/08bfdfc278ba6a5b63d05140fcb9a46a2c161507))

* Migrate from instructor/OpenAI to pydantic-ai (Step 5)

- Add swanki/llm/ package with centralized agent registry (6 agents + get_model_string helper)
- Replace all 21 LLM call sites across 7 files with pydantic-ai agent.run_sync()
- Remove instructor, tenacity, and direct OpenAI client dependencies from pyproject.toml
- Add anthropic.yaml model preset for multi-provider support
- Rewrite image_processor.py with modern types, Google-style docstrings, and frontmatter
- Fix all ruff errors and mypy --strict issues; add missing stubs to ignore list
- Add docstrings to PageLabel/PDFCutPlan, fix ambiguous variable name in pdf_classifier
- Update all test mocks from OpenAI/instructor to pydantic-ai agents
- Add 5 new dendron notes and update 8 existing module notes

Co-Authored-By: Claude Code (commit) &lt;noreply@anthropic.com&gt; ([`443b2a7`](https://github.com/Mjvolk3/Swanki/commit/443b2a7e0da2422437392f544206d454154ca6ff))

* Update dendron notes and weekly for Step 4 completion

- Add dated sections to swanki.audio.lecture, swanki.models.cards, swanki.pipeline.pipeline notes
- Create tests.test_audio_lecture dendron note documenting 11 new tests
- Check off Step 4 prerequisite in pydanticAI WIP scratchpad
- Add Step 4 completion entry to weekly 2026.11

Co-Authored-By: Claude Code (commit) &lt;noreply@anthropic.com&gt; ([`74ba04a`](https://github.com/Mjvolk3/Swanki/commit/74ba04a897fc24a0ad71af23d76d15f4314d24cb))

* Add SI proportion constraint in critique prompt

- When si_reference_content is provided, append SI BALANCE CHECK to critique
- Instructs reviewer to flag sections where SI dominates (&gt;50%)
- Sets si_balance=False when imbalanced — soft prompt guidance

Co-Authored-By: Claude Opus 4.6 &lt;noreply@anthropic.com&gt; ([`cfe5f7f`](https://github.com/Mjvolk3/Swanki/commit/cfe5f7f0af0374bf7f16a55dd4816fc00af41a23))

* Add SI splitting, indexing, and contextual enrichment

- Add si_start_page param to generate_lecture_audio() for SI boundary
- Split markdown files into main vs SI; process images across both
- Add build_si_index() to parse SI markers (Extended Data Fig, Table S, etc.)
- Add extract_relevant_si() for per-section SI reference lookup with fuzzy matching
- Pass matched SI snippets to generate_and_validate_chunk() per section
- Single-pass path includes truncated SI content as reference material
- Append SI instructions to system prompt when SI is present
- Add si_balance field to LectureTranscriptFeedback model
- Read _meta.json in pipeline.py to get si_start_page
- Add lecture_si_instructions to default.yaml config
- Guard: si_start_page &gt;= len(files) falls back to no-SI mode
- No-SI path: exact backward-compatible behavior
- Fix pre-existing ruff issues in cards.py (unused var, raw docstring)
- Add frontmatter to cards.py, extend mypy overrides to models

Co-Authored-By: Claude Opus 4.6 &lt;noreply@anthropic.com&gt; ([`12631ac`](https://github.com/Mjvolk3/Swanki/commit/12631ac1acf119cc4bf7a6d51a878de49f7c327e))

* Broaden chunk_by_headers() to match unnumbered headers

- Try numbered pattern first (## 1.0 Title), fall back to unnumbered (## Methods)
- Require h2+ (#{2,}) to avoid matching h1 document titles
- Add tests for unnumbered-only and mixed header styles

Co-Authored-By: Claude Opus 4.6 &lt;noreply@anthropic.com&gt; ([`510a337`](https://github.com/Mjvolk3/Swanki/commit/510a337a62d64ce04f2e16e512ab0fc51dec277e))

* Refactor length control — remove per-section word budgets

- Remove section_budget_words/section_max_words from generate_and_validate_chunk()
- Use fixed max_completion_tokens=10000 for all sections
- Simplify critique prompt to quality-only checks (no per-section word enforcement)
- Add source_words param to _refine_transcript() for ratio-based length control
- Inject length-reduction feedback when transcript exceeds 70% of source
- Log warning when transcript is under 30% of source
- Update TARGET LENGTH guidance to &#34;40-60% of source manuscript length&#34;
- Add si_reference_content param stub to generate_and_validate_chunk()

Co-Authored-By: Claude Opus 4.6 &lt;noreply@anthropic.com&gt; ([`0851a67`](https://github.com/Mjvolk3/Swanki/commit/0851a67d27391cc939caaf5addaa0d5e26d45f5f))

* Track SI boundary — write _meta.json

- Add si_start_page field to PrepareResult
- Set si_start_page to kept_pages count when SI PDF is present
- Write {citation_key}_meta.json with si_start_page to output_dir

Co-Authored-By: Claude Opus 4.6 &lt;noreply@anthropic.com&gt; ([`8cc3cd0`](https://github.com/Mjvolk3/Swanki/commit/8cc3cd0e3b6f95a5527cab43ab2cd634dfb1eafd))

* Add character-based segmentation mode for card generation (Step 3)

- Create swanki/pipeline/segmenter.py with 4 utility functions: combine_markdown_files, split_into_segments, write_segment_files, build_segment_to_page_map
- Add segmentation stage in process_full() with char/page mode branching
- Rewrite card gen loop for document-order interleaving (text cards per segment, then image cards for covered pages)
- Delete generate_cards_with_context() (~333 lines of dead code)
- Rename _generate_cards_for_page_with_context to _generate_cards_for_segment
- Rename config keys: num_cards_per_page -&gt; cards_per_segment, cloze_cards_per_page -&gt; cloze_per_segment
- Remove dead chunk_size/overlap params from all pipeline config presets
- Add 11 unit tests in tests/test_segmenter.py
- Update test_pipeline_mode.py mock for method rename
- Mark Step 3 complete in pydanticAI migration WIP scratchpad

Co-Authored-By: Claude Code (commit) &lt;noreply@anthropic.com&gt; ([`67b1c9c`](https://github.com/Mjvolk3/Swanki/commit/67b1c9ca0ff576f2c702f00f57cda2a8ce4be18c))

* Replace ConfigGenerator with three-tier config system (Step 2)

- Delete 1354-line swanki/config/generator.py, replace with static YAML defaults in swanki/conf/ (23 files, 7 config groups)
- Add SwankiSearchPathPlugin for git-config-style three-tier resolution: package defaults (swanki/conf/), global user prefs (~/.swanki/), project-local overrides (.swanki/)
- Add swanki/config/helpers.py with package_defaults_path(), user_config_dir(), init_user_config(), show_config_info()
- Rename audio presets to self-documenting names: essential-&gt;complementary_summary, all_but_reading-&gt;complementary_summary_lecture, full-&gt;all, lecture_only-&gt;lecture; add summary_lecture preset
- Add --show-defaults, --init-config, --config-info CLI flags to __main__.py
- Register Hydra plugin via pyproject.toml entry point; add conf/**/*.yaml to package data
- Migrate .swanki_config_custom/ contents to ~/.swanki/
- Fix swanki/__init__.py: add frontmatter, use explicit re-exports to satisfy ruff F401
- 16 new tests (10 helpers + 6 plugin), 70 total pass

Co-Authored-By: Claude Opus 4.6 &lt;noreply@anthropic.com&gt; ([`6258464`](https://github.com/Mjvolk3/Swanki/commit/625846438767377b7d98c2b8d9d03efab2b64122))

* Add audio_only mode to skip card generation (Step 1)

- Add mode=audio_only branching in process_full() to skip stages 5.5-8
- Add cards guard in generate_audio() to skip complementary audio when cards list is empty
- Add mode: full config key and lecture_only.yaml audio preset
- Update CLI help text with mode and lecture_only options
- Add 6 unit tests for audio_only mode and complementary guard
- Fix pre-commit hooks: add frontmatter, hydra/omegaconf mypy stubs, pytest env path, type annotations
- Mark Step 1 complete in master plan and WIP scratchpad

Co-Authored-By: Claude Code (commit) &lt;noreply@anthropic.com&gt; ([`c3fa4ea`](https://github.com/Mjvolk3/Swanki/commit/c3fa4eadaacb4390a8192a5ef13bdbc5958cd511))

* just init ([`bd7d70f`](https://github.com/Mjvolk3/Swanki/commit/bd7d70f76bc34048aaa32717791315d7a7fbe2e3))

* Add presentation generation module with Reveal.js output

- Add swanki/presentation/ package: models, figure extractor, slide generator, renderer, CLI entry point (swanki-present)
- LLM-driven slide content via instructor with structured Pydantic output
- Figure extraction from PDFs via pdftoppm + PIL cropping for sub-panel isolation
- Reveal.js rendering via pandoc with KaTeX math, mermaid diagrams, pointer plugin
- Add /present Claude Code skill wrapping the CLI
- Recreate 12-slide Merzbacher FCL paper outline in scratch note
- Document Reveal.js experience and evaluate PPTX alternatives (python-pptx recommended)
- Add module notes, weekly note, and drawio asset

Co-Authored-By: Claude Code (commit) &lt;noreply@anthropic.com&gt; ([`b9475a9`](https://github.com/Mjvolk3/Swanki/commit/b9475a912f6e969ce833f0238f0902c81e1891a9))

* Add presentation generation plan, broadcast-wt skill, and scratch outline

- Add Reveal.js presentation generation plan for creating academic slide decks from Swanki-processed paper data
- Add broadcast-wt skill for rebasing worktree branches onto latest main
- Update merge-worktree skill
- Add scratch outline stub for Merzbacher FCL paper lit review
- Update swanki.output-apkg plan note
- Update weekly note with presentation feature task

Co-Authored-By: Claude Code (commit) &lt;noreply@anthropic.com&gt; ([`fe73706`](https://github.com/Mjvolk3/Swanki/commit/fe73706b27247314f6f15ff4149822bea9c60105))

* Fix zotero import attachment ordering and qpdf warnings

- Add _is_main_article() heuristic to sort main PDF before SI attachments
- Sort get_pdf_attachments() by title/filename so main article downloads first
- Tolerate qpdf exit code 3 (warnings) in cut_pdf() instead of raising error

Co-Authored-By: Claude Code (commit) &lt;noreply@anthropic.com&gt; ([`5935742`](https://github.com/Mjvolk3/Swanki/commit/5935742f2a77a689afa92009177fd28cdc610ef7))

* Fix worktree settings.json relative path resolution

- setup-worktree.sh now rewrites &#34;../&#34; prefixes in .claude/settings.json
  to the correct relative depth (e.g., &#34;../../&#34; for worktrees nested two
  levels from the projects directory)
- Uses python3 os.path.relpath for portable path computation
- Skips rewrite when worktree is at the same depth as the main repo

Co-Authored-By: Claude Opus 4.6 &lt;noreply@anthropic.com&gt; ([`ec8cb72`](https://github.com/Mjvolk3/Swanki/commit/ec8cb72ae49d4ea50cdc3977272fc036892b9060))

* Add multi-range PDF cutting to zotero paper import

- Replace broken swanki-cut with qpdf for page extraction
- Add state-machine page classifier that keeps article + Extended Data/STAR Methods/SI figures while cutting refs, acknowledgments, and publisher reporting summaries
- Add RESUME_EDUCATIONAL_PATTERNS and TAIL_CUT_PATTERNS regex sets for multi-range detection
- Update zotero-paper-import skill docs with qpdf usage and manual fallback instructions

Co-Authored-By: Claude Code (commit) &lt;noreply@anthropic.com&gt; ([`1cbe991`](https://github.com/Mjvolk3/Swanki/commit/1cbe9915c6f46fe912473c61a7aea2bac3e22d80))

* Fix VS Code test/coverage tasks to use correct conda env path

- Replace ${command:python.interpreterPath} with hardcoded swanki conda env path in swk-test-unit, swk-cov-run, and swk-cov-html tasks
- Update weekly note with task fix entry

Co-Authored-By: Claude Code (commit) &lt;noreply@anthropic.com&gt; ([`ba1411e`](https://github.com/Mjvolk3/Swanki/commit/ba1411e5b10ccc33dab8cf4d64f0d4be2a6c6bf7))

* Add rationale-finding guidance to CLAUDE.md

- Document dendron module notes as the primary source for understanding past code decisions
- Update weekly note

Co-Authored-By: Claude Code (commit) &lt;noreply@anthropic.com&gt; ([`c4736fb`](https://github.com/Mjvolk3/Swanki/commit/c4736fb38c3b14beb28ada0f807554da6e94568d))

* Add settings.local.json copy step to worktree setup

- Copy .claude/settings.local.json into new worktrees so Bash(*) permissions carry over automatically
- Update weekly note with worktree setup improvement

Co-Authored-By: Claude Code (commit) &lt;noreply@anthropic.com&gt; ([`7a2c4a8`](https://github.com/Mjvolk3/Swanki/commit/7a2c4a8e192e6b5810a86d3d17a494ddcabecef2))

* Add README badges and Codecov CI integration

- Add CI status, Codecov coverage, Ruff, mypy strict, Python 3.13, and MIT license badges to README
- Replace gist-based coverage badge with Codecov for public repo
- Add coverage XML generation and Codecov upload step to CI workflow
- Update weekly note

Co-Authored-By: Claude Code (commit) &lt;noreply@anthropic.com&gt; ([`260f970`](https://github.com/Mjvolk3/Swanki/commit/260f970c1fadc8ba7a786cca2ab5c0d074327e6d))

* Add pydanticAI migration WIP scratchpad with full call site inventory

- Create fine-grained WIP checklist covering all 21 LLM call sites across 7 files
- Break migration into 5 phases with per-call-site checkboxes and verification steps
- Update weekly tasks

Co-Authored-By: Claude Code (commit) &lt;noreply@anthropic.com&gt; ([`74a79a4`](https://github.com/Mjvolk3/Swanki/commit/74a79a43cd91485ff6dc253ecbbb6881a85e5b16))

* Fix setup-worktree.sh executable permission

- Set executable bit in git index so worktrees get it on checkout

Co-Authored-By: Claude Code (commit) &lt;noreply@anthropic.com&gt; ([`63d1c15`](https://github.com/Mjvolk3/Swanki/commit/63d1c15ed459fb416fce66dbb78ff708eda90c4a))

* Add setup: worktree VS Code task

- Add missing VS Code task entry for scripts/setup-worktree.sh

Co-Authored-By: Claude Code (commit) &lt;noreply@anthropic.com&gt; ([`e0cb364`](https://github.com/Mjvolk3/Swanki/commit/e0cb3649097100b6c89f940f69ecc67492a0a952))

* Add master refactor sequence plan, rename plans to plan.* namespace, and add sequencing notes

- Create master plan tying 5 refactors into ordered execution sequence with conflict resolutions
- Rename 5 plan notes into plan.* dendron namespace with updated cross-references
- Add sequencing notes and quality gates to each individual plan for inter-plan awareness
- Add migration risk section for instructor-to-pydanticAI self-critic/retry replication
- Add scripts.setup-worktree note and update weekly tasks
- Update workspace file

Co-Authored-By: Claude Code (commit) &lt;noreply@anthropic.com&gt; ([`4fb74fe`](https://github.com/Mjvolk3/Swanki/commit/4fb74fe21e28c1e52dea998ee1fc34607b0bb8b7))

* Add worktree infrastructure: docs, merge skill, permissions, and env template

- Add Git Worktrees section to CLAUDE.md with shared data, memory, and merge workflow docs
- Create merge-worktree skill for PR-based branch merging with cleanup
- Add worktree read/write/edit permissions to .claude/settings.json
- Add .env.example with key-safe environment variable template
- Update setup-worktree.sh to document SWANKI_DATA as shared across worktrees
- Update weekly note with worktree infrastructure task

Co-Authored-By: Claude Code (commit) &lt;noreply@anthropic.com&gt; ([`ff29c90`](https://github.com/Mjvolk3/Swanki/commit/ff29c90049bea11b0ab6e6e19ff11a77e06e2502))

* Purge settings.local.json from history, add project settings, and move command files to dendron notes

Co-Authored-By: Claude Opus 4.6 &lt;noreply@anthropic.com&gt; ([`d75faab`](https://github.com/Mjvolk3/Swanki/commit/d75faab6731702147c04e2777d9ef2b91cf7eb8f))

* Refactor monolithic audio module into swanki/audio package with 37 unit tests

Split the 2918-line swanki/utils/audio.py into a dedicated swanki/audio/
package with focused modules (_common, card, summary, reading, lecture),
add comprehensive unit tests with mocked APIs, and align pre-commit hooks
(add check-dendron-renames, add mypy deps for audio imports).

Co-Authored-By: Claude Opus 4.6 &lt;noreply@anthropic.com&gt; ([`1c84f0d`](https://github.com/Mjvolk3/Swanki/commit/1c84f0d887bca6c2f3b1be59c228187f1d2fe319))

* Add apkg output plan note and update week-09 weekly

- Add swanki.output-apkg.plan-0 planning note
- Update week-09 weekly with completed task entries

Co-Authored-By: Claude Code (commit) &lt;noreply@anthropic.com&gt; ([`3340680`](https://github.com/Mjvolk3/Swanki/commit/3340680fe4f6be9bac1f152ebaa868b16ad22d1c))

* Add LLM page classifier, ApkgExporter, and extract shared card-processing functions

- Add pdf_classifier with LLM-based page labeling for smarter end-matter detection
- Replace references-only regex with two-tier classification (LLM preferred, regex fallback)
- Expand regex to cut acknowledgments, supporting/supplementary information
- Extract card parsing, formatting, and HTML generation from AnkiProcessor to module-level functions
- Add ApkgExporter for direct .apkg deck creation without AnkiConnect dependency
- Integrate ApkgExporter into pipeline for output after card writing and audio generation
- Update zotero-paper-import skill and PrepareResult model for keep_ranges

Co-Authored-By: Claude Code (commit) &lt;noreply@anthropic.com&gt; ([`009cd79`](https://github.com/Mjvolk3/Swanki/commit/009cd79f9bc67b7dde4e7ed2d6355d62492b0265))

* Align CI/CD, linting, and dev tooling with iBioFoundry-AI standards

- Add CI workflow with mypy strict + ruff lint + coverage test jobs on Python 3.13
- Add mypy strict config and coverage config to pyproject.toml, bump to Python 3.13
- Add pre-commit hooks for mypy, docstring frontmatter checking, and markdown table prettifying
- Add .markdownlint.json with shared rule config
- Replace comment-style add_frontmatter.py with docstring-style version
- Add check_frontmatter.py and prettify_markdown_tables.py pre-commit scripts
- Add /mypy and /test-campaign skills, update /ruff and /stage workflows to include mypy
- Add VS Code tasks.json (swk-* tasks), launch.json, and full settings.json alignment
- Add pytest markers (llm, integration) for selective CI test runs
- Update .gitignore with agent working file patterns

Co-Authored-By: Claude Code (commit) &lt;noreply@anthropic.com&gt; ([`8a25d47`](https://github.com/Mjvolk3/Swanki/commit/8a25d47954bfe411ad9ff979ab3693600c51ebff))

* Add pipeline diagram and paper link to README for collaborator sharing ([`1e2152f`](https://github.com/Mjvolk3/Swanki/commit/1e2152f56c75f1f61a21e683e75a76dea3258046))

* Restore pdf_processor module note content after Dendron re-created the file

Co-Authored-By: Claude Opus 4.6 &lt;noreply@anthropic.com&gt; ([`ba19705`](https://github.com/Mjvolk3/Swanki/commit/ba1970513a641ab2e60099b393728c0b151593af))

* Add qpdf fallback for splitting malformed PDFs that PyPDF2 cannot handle

Co-Authored-By: Claude Opus 4.6 &lt;noreply@anthropic.com&gt; ([`9e529b9`](https://github.com/Mjvolk3/Swanki/commit/9e529b948c83e59c067350609d4e996006ba7df9))

* Check off plan-0 task with summary and add weekly note convention to CLAUDE.md

Co-Authored-By: Claude Opus 4.6 &lt;noreply@anthropic.com&gt; ([`977ed38`](https://github.com/Mjvolk3/Swanki/commit/977ed38ff9859ccc476e1b4cc6abaeffee221e3b))

* Rename zotero_import to zotero_paper_import for consistency with skill name

Co-Authored-By: Claude Opus 4.6 &lt;noreply@anthropic.com&gt; ([`51057bc`](https://github.com/Mjvolk3/Swanki/commit/51057bc201a6337a9558e2708bc6b3a2369e8543))

* Add zotero-paper-import script and skill for end-to-end paper preparation

Automates the full Zotero-to-Swanki pipeline: download PDFs by citation key,
detect and cut reference pages, create _clean.pdf, and write the .sh runner.

Co-Authored-By: Claude Opus 4.6 &lt;noreply@anthropic.com&gt; ([`deddc6d`](https://github.com/Mjvolk3/Swanki/commit/deddc6d26e448343efa367c0289d65d4de5b7862))

* Update dendron config, add zotero import plan, and update papers list

Set insertNoteLink/copyNoteLink aliasMode to none in dendron.yml, add
zotero-paper-import plan note, and add montanolopez2022 to CO-Biotech2026
paper list.

Co-Authored-By: Claude Opus 4.6 &lt;noreply@anthropic.com&gt; ([`7eb63e7`](https://github.com/Mjvolk3/Swanki/commit/7eb63e75ca6269735d267b64d46000662f8f0275))

* Update weekly note, Claude settings, and workspace config

- Update weekly 2026.09 with worktree setup and settings entries
- Add Zendron, Deep-Learning-Foundations-and-Concepts, instructor, openai-python to Claude Code additional directories
- Add CO-Biotech2026 papers to review list
- Add setup: worktree VS Code task to workspace

Co-Authored-By: Claude Code (commit) &lt;noreply@anthropic.com&gt; ([`8062085`](https://github.com/Mjvolk3/Swanki/commit/806208573920deb13e38a726fa76fc4bb414a2e2))

* feat: add git worktree setup from iBioFoundry-AI

- Add scripts/setup-worktree.sh for one-command worktree initialization
  (env file, PYTHONPATH, Claude Code shared memory, pre-commit hooks)
- Add .gitattributes with merge=union for weekly task notes
- Update .gitignore with .env.vscode, .claude/plans/, mermaid-filter.err,
  mypy cache, testmon, and coverage entries
- Add &#34;setup: worktree&#34; VS Code task

Co-Authored-By: Claude Code (commit) &lt;noreply@anthropic.com&gt; ([`b3b2ee4`](https://github.com/Mjvolk3/Swanki/commit/b3b2ee486c223c3db94bfa4e47204fe02757aa42))

* Add exported Paper files and update Claude settings

- Flat markdown with resolved transclusions via export_pod_md.sh
- PDF generated via bib_tex_pdf.sh with updated header-includes
- Update .claude/settings.local.json

Co-Authored-By: Claude Code (commit) &lt;noreply@anthropic.com&gt; ([`b41a16e`](https://github.com/Mjvolk3/Swanki/commit/b41a16e3776db6206d7ad895655a8ebbd8f91038))

* Add outstanding notes, scratch files, and clean_pdf command

- Add weekly task notes for weeks 2026.05 and 2026.07
- Update weekly task notes for 2025.23 and 2026.04
- Add scratch notes for CO-Biotech2026 papers and 2026.01.26
- Add .claude/commands/clean_pdf.md

Co-Authored-By: Claude Code (commit) &lt;noreply@anthropic.com&gt; ([`d7ab209`](https://github.com/Mjvolk3/Swanki/commit/d7ab209a15dc744cc7b07f5cedecc6aa460290cc))

* feat: port skills, scripts, and tooling from iBioFoundry-AI; switch to ruff

- Add 9 Claude Code skills: update-py-notes, update-tasks-weekly, pdf, save-plan, stage, commit, ruff, dendron-tree, gh-issue
- Replace black/isort/pydocstyle with ruff in pyproject.toml (E, F, I, UP, D rules, Google docstrings)
- Add .pre-commit-config.yaml with ruff-check, ruff-format, markdownlint, pytest hooks
- Update bib_tex_pdf.sh with SCRIPT_DIR-based paths, mermaid temp dir, Lua filter, pdf_subdir param
- Add break-long-code.lua filter and export_pod_md.sh transclusion resolver
- Update header-includes.tex with DejaVu Sans Mono, fvextra line wrapping, AlertTok fix
- Add dendron-tree.sh script and VS Code tasks for export pod, dendron tree, ruff
- Fix image_processor to resize oversized remote images before vision API calls

Co-Authored-By: Claude Code (commit) &lt;noreply@anthropic.com&gt; ([`9c17bd0`](https://github.com/Mjvolk3/Swanki/commit/9c17bd09f8ae1c5d1581ebda535ed6b8d2bf3a35))

* limits update ([`513fbcd`](https://github.com/Mjvolk3/Swanki/commit/513fbcd228d7045400626827c5b38191d3042b68))

* fix(audio): increase max_completion_tokens for reading transcript generation

Previously, reading transcript generation was hitting token limits with
max_completion_tokens=1000, causing &#39;finish_reason=length&#39; errors and
falling back to unrefined original markdown.

Increased to max_completion_tokens=8000 to accommodate:
- GPT-5.2&#39;s larger output capacity (16k-32k+ tokens)
- Full-page reading transcripts that need natural reformatting
- Dense technical content requiring more tokens

This fixes 9 reading transcript failures observed in adduriPredictingCellularResponses2025
processing (outputs/2026-01-21/20-20-48/__main__.log lines 5403-5459).

Changes:
- swanki/utils/audio.py:1478: 1000 → 8000 max_completion_tokens

Co-Authored-By: Claude Sonnet 4.5 &lt;noreply@anthropic.com&gt; ([`2f0ac70`](https://github.com/Mjvolk3/Swanki/commit/2f0ac708fd6cdd43825a6554deec06674fac3142))

* fix(markdown_cleaner): extract images from LaTeX figure blocks before removal

- Fix subscript auto-fix regex to actually add closing braces
- Add handling for subscripts without any braces (X_0 → X_{0})
- Allow single LaTeX issues to pass with warning (after auto-fix)
- Prevents infinite retry loops on math-heavy pages

Resolves page 19 validation failures by being more tolerant of
edge cases that auto-fix handles correctly.

Co-Authored-By: Claude Sonnet 4.5 &lt;noreply@anthropic.com&gt; ([`d1cbc32`](https://github.com/Mjvolk3/Swanki/commit/d1cbc322fb0731ec5d91b534ab933336ac80dee4))

* fix(validation): auto-fix incomplete LaTeX braces and improve audio error logging

Card validation:
- Auto-fix incomplete subscript braces before validation (X_{0 → X_{0})
- Ensure error messages suggest properly balanced LaTeX
- Improves retry success rate for math-heavy papers

Audio generation:
- Replace str.format() with Template.substitute() to safely handle LaTeX
- Fixes KeyError: &#39;tabular&#39; when refining lecture transcripts with tables
- Add detailed logging for malformed OpenAI responses

Co-Authored-By: Claude Sonnet 4.5 &lt;noreply@anthropic.com&gt; ([`0ce055f`](https://github.com/Mjvolk3/Swanki/commit/0ce055fad5b8aa704098951993e779ba695d2666))

* feat(logging): log output directory path at pipeline start

Prints the full absolute path to the output directory where cards and audio are saved, making it easy to click and navigate to outputs in terminal.

Co-Authored-By: Claude Sonnet 4.5 &lt;noreply@anthropic.com&gt; ([`aef2e8c`](https://github.com/Mjvolk3/Swanki/commit/aef2e8c5127b901d62c10ec0dba41527f9d051ce))

* fix(validation): improve LaTeX error messages with specific subscript formatting guidance

The validator now shows the exact problematic variables and explicitly instructs to use brackets after underscores (e.g., $X_{0}$ not $X_0$). This helps the LLM fix validation errors on retry, especially for math-heavy papers with dense subscript notation.

Co-Authored-By: Claude Sonnet 4.5 &lt;noreply@anthropic.com&gt; ([`33147d4`](https://github.com/Mjvolk3/Swanki/commit/33147d4b37d9a7153bd268d12892d9481e16c242))

* fix(markdown_cleaner): extract images from LaTeX figure blocks before removal

Previously, \begin{figure}...\end{figure} blocks were deleted before
extracting \includegraphics{url} image URLs, causing all images to be lost
for PDFs where Mathpix only outputs LaTeX format (no standalone markdown images).

Added _convert_figure_blocks_to_markdown() method that:
- Extracts \includegraphics{url} from figure blocks
- Extracts caption text from \caption{...} for alt text
- Converts to markdown ![caption](url) format
- Runs BEFORE block removal to preserve image URLs

This fixes image card generation for PDFs like guptaRetinalPigmentEpithelium2023
while maintaining compatibility with PDFs that have both markdown and LaTeX formats.

Changes:
- Added _convert_figure_blocks_to_markdown() method (lines 236-293)
- Modified _apply_cleaning() to call conversion before removal (line 258)
- Removed obsolete figure_blocks and includegraphics patterns from PATTERNS
- Documented fix in notes/swanki.processing.markdown_cleaner.md

Fixes regression introduced in 462ad84 (Dec 17, 2025).

Co-Authored-By: Claude Sonnet 4.5 &lt;noreply@anthropic.com&gt; ([`828c66a`](https://github.com/Mjvolk3/Swanki/commit/828c66a23c5c5b1f4535429b67023e685e80e300))

* cleaning up reading without figures, tables, etc and with humanized reading of latex. ([`462ad84`](https://github.com/Mjvolk3/Swanki/commit/462ad848e0e6026c387e368febfd10ec753c8a58))

* wip getting audio lecture to be more reasonable. Longer than summary, shorter than reading ([`e8d7cc2`](https://github.com/Mjvolk3/Swanki/commit/e8d7cc2339b84502b771a45e4cbc9a6dbb0db2e6))

* update card gen issues, Dennett ([`401dfb1`](https://github.com/Mjvolk3/Swanki/commit/401dfb1875b68fd4bd19f6feee2b56c667842c87))

* rm files not needed. ([`e436c75`](https://github.com/Mjvolk3/Swanki/commit/e436c751cabfa4b67033eac48629d2ea9ce0ff60))

* don&#39;t touch change log ([`8d0a92c`](https://github.com/Mjvolk3/Swanki/commit/8d0a92c38a5de81fe2b1b3df29f075a3f3939cc5))

* docs update ([`24ebbf5`](https://github.com/Mjvolk3/Swanki/commit/24ebbf51c438b93b4a47dfe921b9c1b138622771))

* refactor: improve cloze card generation and validation

- Enforce 1-5 word limit for cloze deletions
- Fix nested math delimiters in cloze cards ($...$ inside {{c1::}})
- Add space before }} when LaTeX ends with } to prevent rendering issues
- Convert image cards from cloze to Q&amp;A format automatically
- Improve audio generation with natural language flow
- Update prompts for better readability and transitions
- Add validation for duplicate tag lines in cards
- Fix LaTeX spacing issues (e.g., \mathrm{d}x vs \mathrm{d} x)

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude &lt;noreply@anthropic.com&gt; ([`5523368`](https://github.com/Mjvolk3/Swanki/commit/5523368adbf989f16bdac3827c740cc09ffbdbd4))

* dump ([`1c8f712`](https://github.com/Mjvolk3/Swanki/commit/1c8f712f611b5c125621f2760fa2e414e9d5cb17))

* image summaries more optimal ([`c047e87`](https://github.com/Mjvolk3/Swanki/commit/c047e8702506ef076a99fe94e9f2355c39db8071))

* fixed citation key reading issue ([`bff3b83`](https://github.com/Mjvolk3/Swanki/commit/bff3b839f8489b8137ec9e2f864d19acf9a0ac06))

* wip citation key botch ([`f09e20d`](https://github.com/Mjvolk3/Swanki/commit/f09e20dbb1d4e6fb702fc9abbb4776496888c351))

* wip ([`e1ff95c`](https://github.com/Mjvolk3/Swanki/commit/e1ff95cee834c5718c4cafa2f6178f601ffb32fa))

* configs better for audio ([`7755244`](https://github.com/Mjvolk3/Swanki/commit/77552447cbdf86e7c60d953e7dc7ae3e4bc4cbb0))

* cloze fix ([`82940a3`](https://github.com/Mjvolk3/Swanki/commit/82940a3cf1b4ff75849107b2981bba2546d1c4ef))

* user input on init ([`42c2dfd`](https://github.com/Mjvolk3/Swanki/commit/42c2dfd239a4e54061fdd4e1192b2db0bb5a5e86))

* refine ([`cfe4660`](https://github.com/Mjvolk3/Swanki/commit/cfe466056981185d6b755e3c186e2459c978ca27))

* self refine ([`4474fb7`](https://github.com/Mjvolk3/Swanki/commit/4474fb7b4498cab1faa613846417f8f481411474))

* all things work. prior to self refine refactor. ([`92ca457`](https://github.com/Mjvolk3/Swanki/commit/92ca45717e50cae5fe4d63b82460723de99aaa81))

* notes ([`29b0e57`](https://github.com/Mjvolk3/Swanki/commit/29b0e571cc472ab96ebf0be8e970595ff0b0eb6e))

* image summary in complementary audio now works. ([`cadd5c5`](https://github.com/Mjvolk3/Swanki/commit/cadd5c50286d72c7c2fdad2fe94c2dc79ab987ac))

* fix citation key read ([`329f4cc`](https://github.com/Mjvolk3/Swanki/commit/329f4ccadfa7c5eb32f344ac6da29ea84b4f2ff2))

* cloze cards now complementary audio correctly ([`9d422cf`](https://github.com/Mjvolk3/Swanki/commit/9d422cf0cdcbca47a2b720bf12ea61b2dceb6baf))

* draft ([`78bb2b7`](https://github.com/Mjvolk3/Swanki/commit/78bb2b727e8ded4f05b8f2b56cd6f5fdddc9452f))

* fixing cloze audio blank now works ([`ca902b9`](https://github.com/Mjvolk3/Swanki/commit/ca902b9755f2ba584b278eaa5896f640d5c99309))

* notes and bib ([`6b871df`](https://github.com/Mjvolk3/Swanki/commit/6b871df033646486627b6c23fc3dd411fb12f290))

* docs ([`c59b805`](https://github.com/Mjvolk3/Swanki/commit/c59b805a7d7ef0215801e20ac5efa341ab09b8ff))

* notes and paper ([`2338df9`](https://github.com/Mjvolk3/Swanki/commit/2338df97e83e5c282fc9eadf298283ae642fbca0))

* docs, pipeline tweaks, docs for paper ([`bf30ab3`](https://github.com/Mjvolk3/Swanki/commit/bf30ab3dca1c5892212b9889daa8e48405eb138f))

* docs ([`728415b`](https://github.com/Mjvolk3/Swanki/commit/728415bcaddfa7d0782b4840806020b4f8a1933f))

* workspace settings ([`c8c2821`](https://github.com/Mjvolk3/Swanki/commit/c8c2821bac2b746b1641e8e9fedda43b38382a72))

* dendron yaml ([`4482b58`](https://github.com/Mjvolk3/Swanki/commit/4482b5842137c822d9ebafe2b7b9220640ca4651))

* paper publish ([`2246998`](https://github.com/Mjvolk3/Swanki/commit/224699898407dcbb7af503506e18b04df9906184))

* no track dendron port cli ([`7e7105f`](https://github.com/Mjvolk3/Swanki/commit/7e7105f2456b5194d0c92c67c7e7a1b8dad03709))

* del old docs ([`bfdb0c7`](https://github.com/Mjvolk3/Swanki/commit/bfdb0c7c7bc584dbb6ac8198ad5329c0cc0d84b4))

* reqs update ([`35e16d7`](https://github.com/Mjvolk3/Swanki/commit/35e16d7f73389c990b66586c9d33b23eeeb9d664))

* read the docs ([`067c24d`](https://github.com/Mjvolk3/Swanki/commit/067c24dd96a4b19398a3196fdc539e91a9854a88))

* new audio ([`77ff37d`](https://github.com/Mjvolk3/Swanki/commit/77ff37d081f3de05519797ccb6c5258fc2593579))

* cloze working ([`d90f8a9`](https://github.com/Mjvolk3/Swanki/commit/d90f8a99791d7047fb3edb8dca49b22906157dc8))

* tags now working ([`0485973`](https://github.com/Mjvolk3/Swanki/commit/04859732f1fb311c576aaaf4a01650d684474ba8))

* claude refactor first step ([`dd74987`](https://github.com/Mjvolk3/Swanki/commit/dd749873afa8ffa6878c9e9b2877498e0ffec3da))

* refactor ([`3f3677b`](https://github.com/Mjvolk3/Swanki/commit/3f3677ba191e057211527c9b9102e989ac200337))

* pipeline working before major refactor ([`e2e3870`](https://github.com/Mjvolk3/Swanki/commit/e2e3870df390bc64d38da51a54a58371dd73791a))

* get cards from ankiconnect ([`c8becf6`](https://github.com/Mjvolk3/Swanki/commit/c8becf66f0ce17586eada1144d830684776a4014))

* mds ([`3221082`](https://github.com/Mjvolk3/Swanki/commit/3221082d72aa16b0dcedae02011bb97960bf8ba1))

* code dump with complementary audio ([`ea0f10e`](https://github.com/Mjvolk3/Swanki/commit/ea0f10e9f4105453ccd38fde1b7606dd77580b39))

* ignore and rm ([`051d22e`](https://github.com/Mjvolk3/Swanki/commit/051d22ec73293a652fe0c9345709e1b9208b2ca7))

* move out of dir ([`76c5ae7`](https://github.com/Mjvolk3/Swanki/commit/76c5ae761a8c28a330d77fb56ce9d6aabdb2c2f6))


## v1.0.2 (2024-08-26)

### Fix

* BLD: dotenv ([`abf5a78`](https://github.com/Mjvolk3/Swanki/commit/abf5a780f91fcadc95efb7759bfa90cc1ce79724))

### Unknown

* Merge remote-tracking branch &#39;refs/remotes/origin/main&#39; ([`6fc3083`](https://github.com/Mjvolk3/Swanki/commit/6fc30836f2028c977a01006388be8e8c25ed4b91))


## v1.0.1 (2024-08-25)

### Fix

* BLD: update reqs ([`989d24a`](https://github.com/Mjvolk3/Swanki/commit/989d24aa9ef805f2d7b5a6f9e1a6be1853c8d9d8))


## v1.0.0 (2024-08-25)

### Breaking

* API: update to 1 ([`e0985ac`](https://github.com/Mjvolk3/Swanki/commit/e0985ac1ef7ca937f8b86116f379aebf9c7064f2))


## v0.0.1 (2024-08-25)

### Fix

* BLD: semantic release ([`5082275`](https://github.com/Mjvolk3/Swanki/commit/50822753d07bc0614d40ada6b3cc754b96a1e505))

* BLD: semantic release ([`71de9d4`](https://github.com/Mjvolk3/Swanki/commit/71de9d4e02be12622a2a22deb85ffe6686853330))

* BLD: adjusted readmea and pypi builds ([`5e09ce0`](https://github.com/Mjvolk3/Swanki/commit/5e09ce07441981254a7ff886ee8eb1256d1c583d))

### Unknown

* vesrion added ([`61d4afc`](https://github.com/Mjvolk3/Swanki/commit/61d4afc79227218df61cc0fe48973a3d050aef0e))

* bulk update for pkg publish ([`bc6a85f`](https://github.com/Mjvolk3/Swanki/commit/bc6a85f780814b41eed9c02db6b122976016380a))

* dump ([`7b3267c`](https://github.com/Mjvolk3/Swanki/commit/7b3267c2a57fbf36a3856340b13a2b1ace0940af))

* Initial commit ([`d85b23a`](https://github.com/Mjvolk3/Swanki/commit/d85b23aadd590e624eb90f24d6e162898248e82b))
